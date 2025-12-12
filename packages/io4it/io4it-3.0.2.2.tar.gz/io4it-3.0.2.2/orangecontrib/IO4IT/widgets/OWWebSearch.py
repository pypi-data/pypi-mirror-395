from datetime import datetime
from typing import List, Dict
from ddgs import DDGS
import os
import sys
import Orange
import re
from Orange.widgets.widget import Input, Output
from AnyQt.QtWidgets import QApplication, QPushButton, QLineEdit, QSpinBox, QDoubleSpinBox
import json
from Orange.widgets.settings import Setting

if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
    from Orange.widgets.orangecontrib.AAIT.utils import thread_management, base_widget
    from Orange.widgets.orangecontrib.HLIT_dev.remote_server_smb import convert
else:
    from orangecontrib.AAIT.utils import thread_management, base_widget
    from orangecontrib.HLIT_dev.remote_server_smb import convert

class WebSearch(base_widget.BaseListWidget):
    name = "WebSearch"
    description = "Search url website from a query with DDG."
    icon = "icons/websearch.png"
    if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
        icon = "icons_dev/websearch.png"
    priority = 3000
    gui = ""
    want_control_area = False
    category = "AAIT - TOOLBOX"
    gui = os.path.join(os.path.dirname(os.path.abspath(__file__)), "designer/owwebsearch.ui")
    # Settings
    selected_column_name = Setting("content")
    region = Setting('fr-fr')
    time_range = Setting('y')
    max_results = Setting(20)
    relevance_threshold = Setting(0.3)

    class Inputs:
        data = Input("Data", Orange.data.Table)

    @Inputs.data
    def set_data(self, in_data):
        self.data = in_data
        if in_data is None:
            self.Outputs.data.send(None)
            return
        if self.data:
            self.var_selector.add_variables(self.data.domain)
            self.var_selector.select_variable_by_name(self.selected_column_name)
        self.run()

    class Outputs:
        data = Output("Data", Orange.data.Table)


    def __init__(self):
        super().__init__()
        # Qt Management
        self.setFixedWidth(500)
        self.setFixedHeight(600)

        self.edit_region = self.findChild(QLineEdit, 'boxRegion')
        self.edit_region.setPlaceholderText("Region")
        self.edit_region.setText(self.region)
        self.edit_region.editingFinished.connect(self.update_parameters)

        self.edit_time_range = self.findChild(QLineEdit, 'boxTimeRange')
        self.edit_time_range.setPlaceholderText("Time Range")
        self.edit_time_range.setText(self.time_range)
        self.edit_time_range.editingFinished.connect(self.update_parameters)

        self.edit_max_results = self.bind_spinbox("boxMaxResults", self.max_results)
        self.edit_relevance_threshold = self.bind_spinbox("boxRelevanceThreshold", self.relevance_threshold, is_double=True)

        self.pushButton_run =self.findChild(QPushButton, 'pushButton_send')
        self.pushButton_run.clicked.connect(self.run)
        self.load_config()

    def bind_spinbox(self, name, value, is_double=False):
        widget_type = QDoubleSpinBox if is_double else QSpinBox
        box = self.findChild(widget_type, name)
        box.setValue(value)
        box.editingFinished.connect(self.update_parameters)
        return box

    def update_parameters(self):
        self.max_results = self.edit_max_results.value()
        self.relevance_threshold = self.edit_relevance_threshold.value()
        self.time_range = self.edit_time_range.text()
        self.region = self.edit_region.text()

    def load_config(self):
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../utils/config.json")
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        self.domain_context = config["domain_context"]
        self.stop_words = set(config["stop_words"])

    def detect_domain(self, query: str):
        """Détecte les domaines dans la requête"""
        query_lower = query.lower()
        detected = []

        for domain_key in self.domain_context.keys():
            if domain_key in query_lower:
                detected.append(domain_key)

        return detected

    def get_contextual_terms(self, query: str):
        """Récupère les termes contextuels basés sur le domaine"""
        domains = self.detect_domain(query)

        if not domains:
            return []

        context_terms = []
        for domain in domains:
            terms = self.domain_context.get(domain, [])[:3]
            context_terms.extend(terms)

        return context_terms

    def optimize_query(self, query: str):
        """Génère des variations optimisées"""
        query = self.clean_query(query)
        variations = []

        # Détecter noms scientifiques et dates
        scientific_names = self.detect_scientific_name(query)
        temporal_exprs = self.detect_temporal_expressions(query)
        key_phrases = self.extract_key_phrases(query)

        words = query.split()
        important_words = [
            w for w in words
            if len(w) >= 3 and w.lower() not in self.stop_words
        ]

        # Noms scientifiques entre guillemets
        if scientific_names:
            for sci_name in scientific_names:
                variations.append(f'"{sci_name}"')
                other_words = [w for w in important_words if w not in sci_name.split()]
                context = other_words[:3] + temporal_exprs
                if context:
                    variations.append(f'"{sci_name}" {" ".join(context)}')

        # Avec expressions temporelles
        if temporal_exprs and not scientific_names:
            if len(important_words) >= 1:
                non_temporal_words = []
                for word in important_words:
                    is_part_of_temporal = False
                    for temp_expr in temporal_exprs:
                        if word.lower() in temp_expr.lower():
                            is_part_of_temporal = True
                            break
                    if not is_part_of_temporal:
                        non_temporal_words.append(word)

                if non_temporal_words and temporal_exprs:
                    variations.append(f"{' '.join(non_temporal_words[:3])} {' '.join(temporal_exprs)}")

                if key_phrases and non_temporal_words:
                    main_phrase = key_phrases[0]
                    contains_temporal = any(temp in main_phrase for temp in temporal_exprs)
                    if not contains_temporal and len(main_phrase.split()) >= 2:
                        variations.append(f'"{main_phrase}" {" ".join(temporal_exprs)}')

        # Phrase clé entre guillemets
        if key_phrases and not scientific_names and not temporal_exprs:
            main_phrase = key_phrases[0]
            if len(main_phrase.split()) >= 2:
                variations.append(f'"{main_phrase}"')
                if len(key_phrases) > 1:
                    variations.append(f'"{main_phrase}" {key_phrases[1]}')

        # Ultra-simplifié
        if len(important_words) >= 2:
            simplified = ' '.join(important_words[:4])
            if temporal_exprs:
                for temp_expr in temporal_exprs:
                    if temp_expr.lower() not in simplified.lower():
                        simplified = f"{simplified} {temp_expr}"
            variations.append(simplified)
        elif len(important_words) == 1 and temporal_exprs:
            variations.append(f"{important_words[0]} {' '.join(temporal_exprs)}")

        # Enrichissement contextuel
        context_terms = self.get_contextual_terms(query)
        if context_terms and important_words:
            enriched_parts = important_words[:3] + context_terms[:2]
            if temporal_exprs:
                enriched_parts.extend(temporal_exprs)
            enriched = ' '.join(enriched_parts)
            variations.append(enriched)

        variations.append(query)

        # Dédupliquer
        seen = set()
        unique_variations = []
        for v in variations:
            v_clean = v.strip()
            if v_clean and v_clean not in seen and len(v_clean.split()) <= 10:
                seen.add(v_clean)
                unique_variations.append(v_clean)

        return unique_variations[:6]

    def calculate_relevance(self, query: str, title: str, snippet: str):
        """Calcule un score de pertinence"""
        query_lower = query.lower()
        title_lower = title.lower()
        snippet_lower = snippet.lower()

        query_words = [
            w for w in query_lower.split()
            if len(w) >= 3 and w not in self.stop_words
        ]

        if not query_words:
            return 0.5

        score = 0.0
        max_score = len(query_words)

        for word in query_words:
            if word in title_lower:
                score += 0.6
            elif word in snippet_lower:
                score += 0.4
            else:
                word_norm = self.normalize_text(word)
                title_norm = self.normalize_text(title_lower)
                snippet_norm = self.normalize_text(snippet_lower)

                if word_norm in title_norm:
                    score += 0.5
                elif word_norm in snippet_norm:
                    score += 0.3

        return min(score / max_score, 1.0)

    def normalize_text(self, text: str):
        """Normalise le texte"""
        accent_map = {
            'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
            'à': 'a', 'â': 'a', 'ä': 'a',
            'î': 'i', 'ï': 'i',
            'ô': 'o', 'ö': 'o',
            'ù': 'u', 'û': 'u', 'ü': 'u',
            'ç': 'c', 'ñ': 'n'
        }

        result = text.lower()
        for old, new in accent_map.items():
            result = result.replace(old, new)

        return result

    def filter_by_relevance(self, results: List[Dict], query: str):
        """Filtre avec vérification de fraîcheur"""
        from datetime import datetime, timedelta

        scored_results = []
        current_year = datetime.now().year

        for result in results:
            score = self.calculate_relevance(
                query,
                result.get('title', ''),
                result.get('body', result.get('snippet', ''))
            )

            # Pénaliser les vieux contenus
            title = result.get('title', '')
            snippet = result.get('body', result.get('snippet', ''))

            # Chercher des années dans le contenu
            years_found = re.findall(r'\b(20\d{2})\b', title + ' ' + snippet)
            if years_found:
                max_year = max(int(y) for y in years_found)
                year_diff = current_year - max_year

                # Pénalité selon l'ancienneté
                if year_diff > 2:
                    score *= 0.3
                elif year_diff > 1:
                    score *= 0.7

            result['relevance_score'] = score
            scored_results.append(result)

        filtered = [r for r in scored_results if r['relevance_score'] >= self.relevance_threshold]
        filtered.sort(key=lambda x: x['relevance_score'], reverse=True)

        return filtered

    def detect_scientific_name(self, query: str):
        """Détecte les noms scientifiques"""
        excluded_words = {'prix', 'cours', 'marché', 'janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet',
                          'août', 'septembre', 'octobre', 'novembre', 'décembre', 'année', 'mois', 'jour', 'monde',
                          'france', 'europe', 'production', 'commerce', 'export', 'import', 'aquaculture',
                          'distribution', 'habitat', 'recherche', 'étude', 'analyse', 'rapport'}
        context_words = {'prix', 'cours', 'marché', 'production', 'recherche', 'étude', 'analyse', 'rapport', 'habitat',
                         'aquaculture', 'distribution', 'ecology', 'biology', 'genetic', 'fishery', 'cultivation',
                         'harvest', 'spawning'}
        pattern = r'\b([a-zA-Z]{4,})\s+([a-zA-Z]{4,})\b'
        matches = re.finditer(pattern, query.lower())

        scientific_names = []
        for match in matches:
            word1, word2 = match.groups()

            if word1 in excluded_words or word2 in excluded_words:
                continue

            if word1 in context_words and word2 in context_words:
                continue

            if word1 in context_words:
                continue

            latin_suffixes = ('us', 'a', 'is', 'um', 'ae', 'i', 'ica', 'ensis', 'anus', 'ina', 'ella', 'ina')
            has_latin_ending = word2.endswith(latin_suffixes) or word1.endswith(latin_suffixes)

            if has_latin_ending:
                normalized = f"{word1.capitalize()} {word2.lower()}"
                if normalized not in scientific_names:
                    scientific_names.append(normalized)

        return scientific_names

    def detect_temporal_expressions(self, query: str):
        """Détecte les expressions temporelles"""
        temporal_patterns = [
            r'\b(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s+\d{4}\b',
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{4}\b',
            r'\b[QT][1-4]\s+\d{4}\b',
            r'\b(S[12]|premier|second|1er|2ème)\s+(semestre|trimestre)\s+\d{4}\b',
            r'\b(20\d{2})\b',
            r'\b(cette|l\'|cette)\s+(année|semaine|mois)\b',
            r'\b(dernier|dernière|prochain|prochaine)\s+(année|semaine|mois|trimestre)\b',
        ]

        found = []
        remaining_query = query

        for pattern in temporal_patterns:
            matches = re.finditer(pattern, remaining_query, re.IGNORECASE)
            for match in matches:
                expr = match.group()
                found.append(expr)
                remaining_query = remaining_query.replace(expr, ' ' * len(expr))

        return found

    def extract_key_phrases(self, query: str):
        """Extrait les phrases clés"""
        temporal_exprs = self.detect_temporal_expressions(query)

        temp_query = query
        temporal_tokens = {}
        for i, expr in enumerate(temporal_exprs):
            token = f"__TEMPORAL_{i}__"
            temporal_tokens[token] = expr
            temp_query = temp_query.replace(expr, token)

        words = temp_query.split()

        important_indices = []
        for i, word in enumerate(words):
            if word.startswith("__TEMPORAL_"):
                important_indices.append(i)
            elif len(word) >= 3 and word.lower() not in self.stop_words:
                important_indices.append(i)

        phrases = []
        if not important_indices:
            return []

        current_phrase = [words[important_indices[0]]]
        last_idx = important_indices[0]

        for idx in important_indices[1:]:
            if idx - last_idx <= 2:
                for j in range(last_idx + 1, idx + 1):
                    if words[j].lower() not in self.stop_words or len(current_phrase) == 1 or words[j].startswith(
                            "__TEMPORAL_"):
                        current_phrase.append(words[j])
            else:
                if len(current_phrase) >= 1:
                    phrase = ' '.join(current_phrase)
                    for token, expr in temporal_tokens.items():
                        phrase = phrase.replace(token, expr)
                    phrases.append(phrase)
                current_phrase = [words[idx]]
            last_idx = idx

        if len(current_phrase) >= 1:
            phrase = ' '.join(current_phrase)
            for token, expr in temporal_tokens.items():
                phrase = phrase.replace(token, expr)
            phrases.append(phrase)

        return phrases

    def clean_query(self, query: str):
        """Nettoie la requête"""
        query = query.strip()

        generic_prefixes = [
            r'^(les?\s+)?informations?\s+(disponibles?\s+)?(sur|concernant|relatif|au sujet)\s+',
            r'^(je\s+)?(cherche|recherche|veux|voudrais|souhaite)\s+',
            r'^(peux-tu|pouvez-vous|trouve|trouver)\s+',
            r'^(donne-moi|donnez-moi)\s+',
        ]

        for pattern in generic_prefixes:
            query = re.sub(pattern, '', query, flags=re.IGNORECASE)

        return query.strip()

    def search(self, use_optimization: bool = True):
        all_results = []
        seen_urls = set()

        if use_optimization:
            query_variations = self.optimize_query(self.query)
            queries_to_try = query_variations
        else:
            queries_to_try = [self.query]

        for idx, q in enumerate(queries_to_try, 1):
            if len(all_results) >= self.max_results:
                break

            try:
                with DDGS() as ddgs:
                    search_results = list(ddgs.text(
                        q,
                        region=self.region,
                        safesearch='off',
                        timelimit=self.time_range,
                        max_results=min(50, self.max_results * 3)
                    ))
                    filtered = self.filter_by_relevance(search_results, self.query)

                    new_count = 0
                    for r in filtered:
                        if r['href'] not in seen_urls:
                            seen_urls.add(r['href'])

                            result = {
                                'url': r['href'],
                                'title': r['title'],
                                'snippet': r.get('body', ''),
                                'source': 'DuckDuckGo',
                                'query': self.query,
                                'query_variation': q,
                                'relevance_score': r['relevance_score'],
                                'fetched_at': datetime.now().isoformat(),
                                'rank': len(all_results) + 1
                            }

                            all_results.append(result)
                            new_count += 1

                            if len(all_results) >= self.max_results:
                                break

            except Exception as e:
                print(e)
                continue

        return all_results[:self.max_results]

    def run(self):
        self.error("")
        self.warning("")
        if self.data is None:
            self.Outputs.data.send(None)
            return

        if not self.selected_column_name in self.data.domain:
            self.warning(f'Previously selected column "{self.selected_column_name}" does not exist in your data.')
            return

        self.query = self.data.get_column(self.selected_column_name)[0]

        self.progressBarInit()
        self.thread = thread_management.Thread(self.search)
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
        if result is None or len(result) == 0:
            self.Outputs.data.send(None)
            return
        data = convert.convert_json_implicite_to_data_table(result)
        self.Outputs.data.send(data)

    def handle_finish(self):
        self.progressBarFinished()

    def post_initialized(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    my_widget = WebSearch()
    my_widget.show()

    if hasattr(app, "exec"):
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())