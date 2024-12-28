import sys
import os
import webbrowser
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QFileDialog, QWidget, QRadioButton, QButtonGroup, QComboBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyPDF2 import PdfReader, PdfWriter

'''
 ____   ____   _____  ___                            _
|  _ \ |  _ \ |  ___||_ _| _ __  __   __  ___  _ __ | |_   ___  _ __
| |_) || | | || |_    | | | '_ \ \ \ / / / _ \| '__|| __| / _ \| '__|
|  __/ | |_| ||  _|   | | | | | | \ V / |  __/| |   | |_ |  __/| |
|_|    |____/ |_|    |___||_| |_|  \_/   \___||_|    \__| \___||_|

'''
class PDFPageInverterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Inverter")
        self.setGeometry(300, 300, 300, 300)
        self.file_path = None
        self.output_folder = None
        self.inversion_option = "All"
        self.language = "EN"  # Default language

        self.init_ui()

    def init_ui(self):
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Set global font
        self.setFont(QFont("Arial", 10))

        # Title label
        self.title_label = QLabel("PDF Inverter")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(self.title_label)

        # File selection
        self.file_label = QLabel("Select or drop a PDF file")
        self.file_label.setAlignment(Qt.AlignCenter)
        self.file_label.setStyleSheet("font-size: 14px;")
        layout.addWidget(self.file_label)

        browse_pdf_button = QPushButton("Browse PDF")
        browse_pdf_button.clicked.connect(self.select_pdf)
        layout.addWidget(browse_pdf_button)

        open_pdf_button = QPushButton("Open Selected PDF")
        open_pdf_button.clicked.connect(self.open_pdf)
        layout.addWidget(open_pdf_button)

        # Enable drag and drop
        self.setAcceptDrops(True)

        # Output folder selection
        self.output_label = QLabel("Choose output folder")
        self.output_label.setAlignment(Qt.AlignCenter)
        self.output_label.setStyleSheet("font-size: 14px;")
        layout.addWidget(self.output_label)

        browse_folder_button = QPushButton("Browse Output Folder")
        browse_folder_button.clicked.connect(self.select_output_folder)
        layout.addWidget(browse_folder_button)

        # Inversion options
        options_label = QLabel("Choose inversion option")
        options_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(options_label)

        self.option_group = QButtonGroup()
        all_button = QRadioButton("All Pages")
        all_button.setChecked(True)
        even_button = QRadioButton("Even Pages")
        odd_button = QRadioButton("Odd Pages")

        self.option_group.addButton(all_button)
        self.option_group.addButton(even_button)
        self.option_group.addButton(odd_button)

        layout.addWidget(all_button)
        layout.addWidget(even_button)
        layout.addWidget(odd_button)

        # Start processing
        start_button = QPushButton("Start Processing")
        start_button.setStyleSheet("background-color: green; color: white;")
        start_button.clicked.connect(self.invert_pdf)
        layout.addWidget(start_button)

        # Status label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: red;")
        layout.addWidget(self.status_label)

        # Language selection
        language_label = QLabel("Language / 言語")
        language_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(language_label)

        language_dropdown = QComboBox()
        language_dropdown.addItems(["English", "日本語"])
        language_dropdown.currentIndexChanged.connect(self.set_language)
        layout.addWidget(language_dropdown)

        central_widget.setLayout(layout)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.endswith(".pdf"):
                self.file_path = file_path
                self.file_label.setText(f"Selected file: {os.path.basename(file_path)}")
                return
        self.status_label.setText("Invalid file. Please drop a valid PDF.")

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
            self.status_label.setText("No file selected. Please select a PDF.")
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

            for i, page in enumerate(reader.pages):
                if self.get_inversion_option() == "All" or \
                   (self.get_inversion_option() == "Even" and i % 2 == 1) or \
                   (self.get_inversion_option() == "Odd" and i % 2 == 0):
                    page.rotate(180)
                writer.add_page(page)

            with open(output, "wb") as f:
                writer.write(f)

            self.status_label.setStyleSheet("color: green;")
            self.status_label.setText(f"File saved successfully: {output}")
            webbrowser.open(self.output_folder)
        except Exception as e:
            self.status_label.setStyleSheet("color: red;")
            self.status_label.setText(f"Error: {e}")

    def get_inversion_option(self):
        for button in self.option_group.buttons():
            if button.isChecked():
                return button.text().split()[0]

    def set_language(self, index):
        if index == 0:  # English
            self.language = "EN"
            self.file_label.setText("Select or drop a PDF file")
            self.output_label.setText("Choose output folder")
            self.status_label.setText("")
        else:  # Japanese
            self.language = "JP"
            self.file_label.setText("PDFファイルを選択またはドロップしてください")
            self.output_label.setText("出力フォルダを選択")
            self.status_label.setText("")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PDFPageInverterApp()
    window.show()
    sys.exit(app.exec_())