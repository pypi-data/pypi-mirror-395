import os
import sys
import time
from pathlib import Path

from AnyQt.QtWidgets import QApplication
from Orange.widgets import widget
from Orange.widgets.utils.signals import Input, Output
from Orange.data import Domain, StringVariable, Table

# --- Docling Core and Docling ---
from docling.document_converter import DocumentConverter, AudioFormatOption
from docling.datamodel.base_models import InputFormat, ConversionStatus
from docling.pipeline.asr_pipeline import AsrPipeline
from docling.datamodel.pipeline_options import AsrPipelineOptions
from docling.datamodel import asr_model_specs
from docling.datamodel.document import ConversionResult

# --- Orange contrib Imports ---
if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
    from Orange.widgets.orangecontrib.AAIT.utils.thread_management import Thread
    from Orange.widgets.orangecontrib.AAIT.utils.import_uic import uic
else:
    from orangecontrib.AAIT.utils.thread_management import Thread
    from orangecontrib.AAIT.utils.import_uic import uic


# ----------------- Worker Function (Conversion ASR) ------------------
def _asr_conversion(file_path_str: str) -> list:
    """ASR conversion for a single MP3 file."""
    t0 = time.time()
    src = Path(file_path_str)

    # Define output directory and file
    out_dir = src.parent / "asr_md"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_md = out_dir.joinpath(f"{src.stem}.md")

    # Don't re-process if output file exists
    if out_md.exists():
        status = "ok"
        message = "cached"
        duration = time.time() - t0
        return [str(src), str(out_md), status, f"{duration:.2f}", message]

    status, message = "ok", ""  # Default status

    try:
        # Docling ASR configuration
        pipeline_options = AsrPipelineOptions()
        pipeline_options.asr_options = asr_model_specs.WHISPER_BASE

        converter = DocumentConverter(
            format_options={
                InputFormat.AUDIO: AudioFormatOption(
                    pipeline_cls=AsrPipeline,
                    pipeline_options=pipeline_options,
                )
            }
        )

        # Perform conversion
        result: ConversionResult = converter.convert(src)

        if result.status == ConversionStatus.SUCCESS:
            # New check: ensure text exists before exporting
            if hasattr(result.document, 'texts') and result.document.texts:
                markdown_content = result.document.export_to_markdown()
                out_md.write_text(markdown_content, encoding="utf-8")
                message = ""  # Conversion successful with text
            else:
                # Case where conversion is "successful" but no text is found
                markdown_content = "[Warning] Conversion réussie, mais aucun texte n'a été transcrit (audio silencieux ?)"
                out_md.write_text(markdown_content, encoding="utf-8")
                status = "ok"  # Still technically ok, but with a warning
                message = "Conversion réussie, mais aucun texte n'a été transcrit (audio silencieux ?)"
        else:
            status = "nok"
            message = f"Conversion failed with status: {result.status}"
            try:
                out_md.write_text(f"[Erreur ASR] {message}", encoding="utf-8")
            except Exception:
                pass

    except Exception as e:
        status = "nok"
        message = f"Error: {e}"
        try:
            out_md.write_text(f"[Erreur ASR] {message}", encoding="utf-8")
        except Exception:
            pass

    duration = time.time() - t0
    return [str(src), str(out_md), status, f"{duration:.2f}", message]


class OWDoclingASR(widget.OWWidget):
    name = "Docling ASR"
    description = "Convertit des fichiers audio (MP3) en texte (Markdown) via Docling."
    category = "IO4IT"  # You may need to change the category
    icon = "icons/asr.png"  # Assurez-vous que l'icône existe dans un dossier 'icons'
    gui = os.path.join(os.path.dirname(os.path.abspath(__file__)), "designer/owdoclingasr.ui")
    want_control_area = True
    priority = 1005

    class Inputs:
        data = Input("Files Table", Table)

    class Outputs:
        data = Output("ASR Markdown", Table)

    def __init__(self):
        super().__init__()
        self.setFixedWidth(470)
        self.setFixedHeight(300)
        uic.loadUi(self.gui, self)

        self.data = None
        self.thread = None
        self.result = None
        self.post_initialized()

    @Inputs.data
    def set_data(self, in_data: Table | None):
        self.data = in_data
        self.run()

    def run(self):
        if self.thread is not None and self.thread.isRunning():
            self.thread.safe_quit()

        if self.data is None:
            self.Outputs.data.send(None)
            return

        self.error("")
        try:
            self.data.domain["file_path"]
        except KeyError:
            self.error("La colonne 'file_path' est requise dans les données d'entrée.")
            return

        self.progressBarInit()

        # Récupérer et filtrer les chemins de fichiers
        try:
            paths = [Path(str(x)) for x in self.data.get_column("file_path")]
        except Exception as e:
            self.error(f"Impossible de lire la colonne 'file_path': {e}")
            self.Outputs.data.send(None)
            return

        files = [p for p in paths if p.exists() and p.suffix.lower() == ".mp3"]
        if not files:
            self.error("Aucun fichier .mp3 valide n'a été trouvé.")
            self.Outputs.data.send(None)
            self.progressBarFinished()
            return

        # Démarrer le thread de conversion
        self.thread = Thread(self._run_conversion, files)
        self.thread.progress.connect(self.handle_progress)
        self.thread.result.connect(self.handle_result)
        self.thread.finish.connect(self.handle_finish)
        self.thread.start()

    def _run_conversion(self, files: list[Path], progress_callback):
        """Fonction principale pour exécuter la conversion séquentielle."""
        results = []
        total_files = len(files)

        for i, file_path in enumerate(files):
            row = _asr_conversion(str(file_path))
            results.append(row)
            progress_callback((i + 1) / total_files * 100)

        # Construction de la table de sortie
        domain = Domain([], metas=[
            StringVariable("src_path"),
            StringVariable("output_md"),
            StringVariable("status"),
            StringVariable("duration_sec"),
            StringVariable("message"),
        ])

        table = Table.from_list(domain, results)
        return table

    def handle_progress(self, value: float) -> None:
        self.progressBarSet(value)

    def handle_result(self, result: Table):
        try:
            self.result = result
            self.Outputs.data.send(result)
        except Exception as e:
            print("An error occurred when sending out_data:", e)
            self.Outputs.data.send(None)
            return

    def handle_finish(self):
        self.progressBarFinished()

    def post_initialized(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    my_widget = OWDoclingASR()
    my_widget.show()
    if hasattr(app, "exec"):
        app.exec()
    else:
        app.exec_()