import sys
import os
import webbrowser
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton,
    QFileDialog, QWidget
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyPDF2 import PdfReader, PdfWriter

class PDFPageInverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Page Inverter")
        self.setGeometry(300, 300, 400, 400)
        self.file_path = None
        self.output_folder = None
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        # Title Label
        title_label = QLabel("PDF Inverter")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; text-align: center; color: #333;")
        title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title_label)

        # Label and button for selecting PDF
        self.file_label = self.add_label("Choose a PDF file")
        self.add_button("Browse PDF", self.select_pdf, "#6CA0DC")
        self.add_button("Open Selected PDF", self.open_pdf, "#85C1E9")

        # Label and button for selecting output directory
        self.output_label = self.add_label("Choose output folder")
        self.add_button("Browse Output Folder", self.select_output_folder, "#6CA0DC")
        self.add_button("Start Processing", self.invert_pdf, "#28a745")

        # Status label
        self.status_label = self.add_label("", color="red")

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def add_label(self, text, color="black"):
        label = QLabel(text)
        label.setStyleSheet(f"color: {color}; font-size: 14px;")
        self.layout.addWidget(label)
        return label

    def add_button(self, text, handler, color):
        button = QPushButton(text)
        button.setStyleSheet(
            f"background-color: {color}; color: white; padding: 8px; font-size: 14px; border-radius: 5px;"
        )
        button.clicked.connect(handler)
        self.layout.addWidget(button)

    def select_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select PDF File", "", "PDF Files (*.pdf)")
        if file_path:
            self.file_path = file_path
            self.file_label.setText(f"Selected file: {os.path.basename(file_path)}")

    def select_output_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if folder_path:
            self.output_folder = folder_path
            self.output_label.setText(f"Output folder: {folder_path}")

    def open_pdf(self):
        if not self.file_path:
            self.status_label.setText("Please select a PDF file to open.")
        else:
            webbrowser.open(self.file_path)

    def invert_pdf(self):
        if not (self.file_path and self.output_folder):
            self.status_label.setText("Please select both a PDF file and an output folder.")
            return
        try:
            reader = PdfReader(self.file_path)
            writer = PdfWriter()
            output = os.path.join(self.output_folder, f"{os.path.splitext(os.path.basename(self.file_path))[0]}_inverted.pdf")

            for page in reader.pages:
                page.rotate(180)
                writer.add_page(page)

            with open(output, "wb") as f:
                writer.write(f)

            self.status_label.setText(f"File saved successfully: {output}")
            webbrowser.open(self.output_folder)
        except Exception as e:
            self.status_label.setText(f"Error: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PDFPageInverter()
    window.show()
    sys.exit(app.exec_())
