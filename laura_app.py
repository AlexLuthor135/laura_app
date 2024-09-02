import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog
from PyQt5.QtGui import QFont
from markdown_pdf import MarkdownPDF, Section

class MarkdownToPDFApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set window properties
        self.setWindowTitle('Markdown to PDF Converter')
        self.setGeometry(300, 300, 400, 200)
        
        # Layout
        layout = QVBoxLayout()
        
        # Title Label
        title = QLabel('Drag and Drop Markdown File', self)
        title.setFont(QFont('Arial', 18))
        layout.addWidget(title)
        
        # Button to Select File
        self.btn = QPushButton('Select Markdown File', self)
        self.btn.clicked.connect(self.showFileDialog)
        layout.addWidget(self.btn)
        
        # Status Label
        self.status_label = QLabel('', self)
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
        
    def showFileDialog(self):
        # Open file dialog to select markdown file
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Markdown Files (*.md)")
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            self.convertToPDF(file_path)

    def convertToPDF(self, file_path):
        # Read Markdown File
        with open(file_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # Create a MarkdownPDF object and add sections
        mdpdf = MarkdownPDF(toc_level=2)
        mdpdf.add_section(Section(markdown_content))
        
        # Set metadata
        mdpdf.meta["title"] = "Converted PDF"
        mdpdf.meta["author"] = "Your Name"
        
        # Save as PDF in the same directory
        pdf_path = os.path.splitext(file_path)[0] + ".pdf"
        mdpdf.save(pdf_path)
        
        self.status_label.setText(f"Converted to PDF: {pdf_path}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MarkdownToPDFApp()
    ex.show()
    sys.exit(app.exec_())
