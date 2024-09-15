from PyQt5.QtWidgets import QGridLayout, QLabel, QWidget, QApplication
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import os, sys, re
from markdown2 import markdown  # Correct import for markdown
from weasyprint import HTML

# Optional: Set DYLD_LIBRARY_PATH if needed (commented out here)
# os.environ['DYLD_LIBRARY_PATH'] = '/opt/homebrew/lib:/opt/homebrew/Cellar/glib/2.82.0/lib:/opt/homebrew/Cellar/gobject-introspection/1.82.0/lib'

class MarkdownToPDFApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set window properties
        self.setWindowTitle('Laura App')
        self.setGeometry(300, 300, 400, 400)  # Initial size, can be adjusted

        # Layout
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins around the layout
        layout.setSpacing(0)  # Remove spacing between widgets
        self.setLayout(layout)

        # Enable drag and drop
        self.setAcceptDrops(True)

        # Image
        image_path = os.path.join('resources', 'image.png')
        self.image_label = QLabel(self)
        pixmap = QPixmap(image_path)
        self.pixmap = pixmap
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)  # Allow image to scale within the label
        self.image_label.setAlignment(Qt.AlignCenter)  # Center the image
        self.image_label.setSizePolicy(self.image_label.sizePolicy().Expanding, self.image_label.sizePolicy().Expanding)

        layout.addWidget(self.image_label, 0, 0, 1, 1)  # Add the image to the grid layout

        # Remove padding around the image
        self.image_label.setContentsMargins(0, 0, 0, 0)  # Ensure no padding inside the label

        # Status Label
        # self.status_label = QLabel('', self)
        # layout.addWidget(self.status_label, 1, 0)  # Add status label to the grid layout

        # Set minimum size for the window
        self.setMinimumSize(200, 150)  # Adjust according to your needs

    def dragEnterEvent(self, event):
        # Accept the drag event if the file has a '.md' extension
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        # Handle the file drop
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.endswith('.md'):
                self.convertToPDF(file_path)
            else:
                self.status_label.setText("Only Markdown files are supported!")

    def resizeEvent(self, event):
        self.updateImageSize()

    def updateImageSize(self):
        # Resize the image to fit the window, maintaining aspect ratio
        scaled_pixmap = self.pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        self.image_label.setPixmap(scaled_pixmap)

    def preprocess_obsidian_markdown(self, markdown_content):
        # Internal links
        markdown_content = re.sub(r'\[\[(.*?)\]\]', r'<a href="\1">Link</a>', markdown_content)

        # Embed files
        markdown_content = re.sub(r'!\[\[(.*?)\]\]', r'<img src="\1" alt="Image"/>', markdown_content)

        # Block references
        # Example for block references
        markdown_content = re.sub(r'!\[\[(.*?)#\^([^\]]+)\]\]', r'<a href="\1#\2">Block Reference</a>', markdown_content)

        # Comments
        markdown_content = re.sub(r'%%(.*?)%%', r'<!-- \1 -->', markdown_content)

        # Strikethroughs
        markdown_content = re.sub(r'~~(.*?)~~', r'<del>\1</del>', markdown_content)

        # Highlights
        markdown_content = re.sub(r'==([^=]*)==', r'<mark>\1</mark>', markdown_content)

        # Tasks
        markdown_content = re.sub(r'- \[ \] (.*?)\n', r'<li class="task incomplete">\1</li>\n', markdown_content)
        markdown_content = re.sub(r'- \[x\] (.*?)\n', r'<li class="task complete">\1</li>\n', markdown_content)

        # Callouts
        markdown_content = re.sub(r'> \[!(.*?)\]', r'<blockquote class="\1">', markdown_content)
        markdown_content = markdown_content.replace('</blockquote>', '</blockquote>')

        # Code blocks
        markdown_content = re.sub(r'```(\w*)\n(.*?)```', r'<pre><code class="\1">\2</code></pre>', markdown_content, flags=re.DOTALL)

        # Tables (improved handling for demonstration purposes)
        # Splits lines by newlines and creates rows for each line
        rows = markdown_content.split('\n')
        html_table = ''
        in_table = False

        for row in rows:
            if row.startswith('|'):
                if not in_table:
                    html_table += '<table>'
                    in_table = True
                cells = row.strip('|').split('|')
                html_table += '<tr>' + ''.join(f'<td>{cell.strip()}</td>' for cell in cells) + '</tr>'
            else:
                if in_table:
                    html_table += '</table>'
                    in_table = False
                html_table += row + '\n'

        if in_table:
            html_table += '</table>'

        markdown_content = html_table

        return markdown_content



    def convertToPDF(self, file_path):
        try:
            # Read Markdown File
            with open(file_path, 'r', encoding='utf-8') as f:
                markdown_content = f.read()

            # Preprocess Markdown for Obsidian-specific syntax
            html_content = self.preprocess_obsidian_markdown(markdown_content)
        
            # Convert Markdown to HTML
            html_content = markdown(html_content, extras=["fenced-code-blocks", "tables", "task_list"])
        
            # Convert HTML to PDF
            pdf_path = os.path.splitext(file_path)[0] + ".pdf"
            HTML(string=html_content).write_pdf(pdf_path)
        
            # self.status_label.setText(f"Converted to PDF: {pdf_path}")
        except Exception as e:
            # self.status_label.setText(f"Error: {str(e)}")
            print(f"Exception occurred: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MarkdownToPDFApp()
    ex.show()
    sys.exit(app.exec_())
