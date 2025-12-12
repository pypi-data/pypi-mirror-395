import os
import sys
import Orange
from Orange.widgets.widget import OWWidget, Input, Output
from AnyQt.QtWidgets import QApplication
import asyncio
import aiohttp
import html2text
from bs4 import BeautifulSoup

if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
    from Orange.widgets.orangecontrib.AAIT.utils import thread_management
    from Orange.widgets.orangecontrib.HLIT_dev.remote_server_smb import convert
    from Orange.widgets.orangecontrib.AAIT.utils.import_uic import uic
else:
    from orangecontrib.AAIT.utils.import_uic import uic
    from orangecontrib.HLIT_dev.remote_server_smb import convert
    from orangecontrib.AAIT.utils import thread_management

class ParseHMTL(OWWidget):
    name = "ParseHTML"
    description = "Parse website HTML. You need to provide url(s) in input."
    icon = "icons/html.png"
    if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
        icon = "icons_dev/html.png"
    priority = 3000
    gui = ""
    want_control_area = False
    category = "AAIT - TOOLBOX"
    gui = os.path.join(os.path.dirname(os.path.abspath(__file__)), "designer/owparserhtml.ui")

    class Inputs:
        data = Input("Data", Orange.data.Table)

    @Inputs.data
    def set_data(self, in_data):
        if in_data is None:
            return
        if "url" not in in_data.domain:
            self.error("input table need a url column")
            return
        self.data = in_data
        self.url_data = in_data.get_column("url")
        self.run()

    class Outputs:
        data = Output("Data", Orange.data.Table)

    def __init__(self):
        super().__init__()
        # Qt Management
        self.setFixedWidth(500)
        self.setFixedHeight(400)
        uic.loadUi(self.gui, self)

        self.data = None
        self.thread = None
        self.markdown = True
        self.run()

    def update_parameters(self):
        return


    def parse_html(self):
        """Execute le parsing"""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            results = loop.run_until_complete(self.parse_all_urls())
            loop.close()
            return results
        except Exception as e:
            self.error(str(e))
            return


    async def parse_all_urls(self, progress_callback=None):
        """Parse toutes les URLs de manière asynchrone"""
        results = []
        total = len(self.url_data)
        timeout = aiohttp.ClientTimeout(total=30)
        connector = aiohttp.TCPConnector(limit=5, limit_per_host=2)
        async with aiohttp.ClientSession(timeout=timeout, connector=connector,cookie_jar=aiohttp.CookieJar()) as session:
            for idx, url_data in enumerate(self.url_data):
                if progress_callback is not None:
                    progress_value = int((idx / total) * 100)
                    progress_callback(progress_value)
                try:
                    parsed = await self.parse_single_url(session, url_data)
                    results.append(parsed)

                except Exception as e:
                    results.append({
                        "url": url_data,
                        'content': '',
                        'meta_description': '',
                        'word_count': 0,
                        'status': f'error: {str(e)}'
                    })

        return results

    async def parse_single_url(self, session, url):
        """Parse une seule URL"""
        # Fetch HTML
        headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
        }
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                raise Exception(f"HTTP {response.status}")

            html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')

        meta_desc = ''
        meta_tag = soup.find('meta', attrs={'name': 'description'})
        if not meta_tag:
            meta_tag = soup.find('meta', property='og:description')
        if meta_tag:
            meta_desc = meta_tag.get('content', '')
        content = ''
        try:
            content = self._extract_main_content(soup)
        except Exception as e:
            print(e)
        word_count = len(content.split())
        return {
            "url": url,
            'content': content,
            'meta_description': meta_desc,
            'word_count': word_count,
            'status': 'success'
        }

    def _extract_main_content(self, soup):
        """Extrait le contenu principal et le convertit en Markdown"""
        main_selectors = [
            'article',
            'main',
            '[role="main"]',
            '.content',
            '.main-content',
            '#content',
            '.article-body',
            '.post-content'
        ]
        converter = html2text.HTML2Text()
        converter.ignore_links = False
        converter.ignore_images = False
        converter.body_width = 0
        for selector in main_selectors:
            main_elem = soup.select_one(selector)
            if main_elem:
                if self.markdown:
                    html = str(main_elem)
                    markdown = converter.handle(html)
                    if len(markdown.split()) > 100:
                        return markdown.strip()
                else:
                    paragraphs = main_elem.find_all('p')
                    if paragraphs:
                        text = ' '.join([p.get_text(strip=True) for p in paragraphs])
                        if len(text) > 100:
                                return text
        paragraphs = soup.find_all('p')
        if paragraphs:
            return ' '.join([p.get_text(strip=True) for p in paragraphs])

        return soup.get_text(strip=True, separator=' ')

    def run(self):
        self.error("")
        self.warning("")
        if self.data is None:
            return
        self.progressBarInit()
        self.thread = thread_management.Thread(self.parse_html)
        self.thread.progress.connect(self.handle_progress)
        self.thread.result.connect(self.handle_result)
        self.thread.finish.connect(self.handle_finish)
        self.thread.start()

    def handle_progress(self, progress) -> None:
        value = progress[0]
        text = progress[1]
        if value is not None:
            self.progressBarSet(value)
        if text is None:
            self.textBrowser.setText("")
        else:
            self.textBrowser.insertPlainText(text)

    def handle_result(self, result):
        data = convert.convert_json_implicite_to_data_table(result)
        self.Outputs.data.send(data)
        self.data = None

    def handle_finish(self):
        print("Generation finished")
        self.progressBarFinished()

    def post_initialized(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    my_widget = ParseHMTL()
    my_widget.show()

    if hasattr(app, "exec"):
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())

