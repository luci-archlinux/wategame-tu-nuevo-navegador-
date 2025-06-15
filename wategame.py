import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit
from PyQt5.QtWebEngineWidgets import QWebEngineView
from whoosh.index import open_dir
from whoosh.qparser import QueryParser

class WategameBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wategame - Navegador con Búsqueda")
        self.setGeometry(100, 100, 800, 600)

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))

        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Introduce una URL o término de búsqueda")
        self.url_bar.returnPressed.connect(self.load_page)

        self.search_btn = QPushButton("Buscar")
        self.search_btn.clicked.connect(self.load_page)

        layout = QVBoxLayout()
        layout.addWidget(self.url_bar)
        layout.addWidget(self.search_btn)
        layout.addWidget(self.browser)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Cargar índice de búsqueda
        self.ix = open_dir("indexdir")

    def load_page(self):
        query_text = self.url_bar.text()
        
        if "." in query_text:  # Si el usuario ingresa una URL, cargarla directamente
            self.browser.setUrl(QUrl(query_text))
        else:  # Si es una búsqueda, consultar el motor
            results_html = self.search_results(query_text)
            self.browser.setHtml(results_html)

    def search_results(self, query_text):
        with self.ix.searcher() as searcher:
            query = QueryParser("content", self.ix.schema).parse(query_text)
            results = searcher.search(query)

            html = "<h2>Resultados de búsqueda:</h2><ul>"
            for r in results:
                html += f'<li><b>{r["title"]}</b></li>'
            html += "</ul>"

            return html

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WategameBrowser()
    window.show()
    sys.exit(app.exec_())


