import os
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QImage, QPixmap, QTextCursor

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QMenu,
    QMenuBar,
    QFileDialog,
    QMessageBox,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTextEdit,
    QPushButton,
    QScrollArea,
    QGridLayout,
    QSizePolicy,
    QInputDialog,
)
from PIL import Image

class DeselectableTextEdit(QTextEdit):
    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.clearFocus()

class ImageBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("JCaptioneer-v1")

        # Set the window icon
        self.setWindowIcon(QIcon("C:\\Users\\Seif\\Desktop\\JCaptioneer\\icon.ico"))
        self.setWindowTitle("JCaptioneer-v1")

        self.directory = None
        self.images = []
        self.current_image = None
        self.text_filename = None

        self.init_ui()

    def init_ui(self):
        # Style
        self.setStyleSheet("""
            QLabel {
                margin: 5px;
                border: 1px solid #cccccc;
                border-radius: 3px;
            }

            QLabel:hover {
                border: 1px solid #aaaaaa;
            }

            QLabel:focus {
                border: 1px solid #666666;
            }
        """)

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)

        self.file_menu = QMenu("File", self.menu_bar)
        self.menu_bar.addMenu(self.file_menu)

        self.choose_directory_action = self.file_menu.addAction("Choose Directory")
        self.choose_directory_action.triggered.connect(self.choose_directory)

        self.image_label = QLabel()
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.image_label)
        self.scroll_area.setWidgetResizable(True)

        self.textbox = DeselectableTextEdit()
        self.textbox.setWordWrapMode(3)
        self.textbox.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum))  # Keep this line

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_text)

        self.left_button = QPushButton("<")
        self.left_button.clicked.connect(self.show_previous_image)

        self.right_button = QPushButton(">")
        self.right_button.clicked.connect(self.show_next_image)

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.show_thumbnails)

        self.thumbnail_frame = QWidget()
        self.thumbnail_layout = QGridLayout()
        self.thumbnail_layout.setSpacing(10)  # Set spacing between grid items
        self.thumbnail_frame.setLayout(self.thumbnail_layout)
        self.thumbnail_scroll_area = QScrollArea()
        self.thumbnail_scroll_area.setWidget(self.thumbnail_frame)
        self.thumbnail_scroll_area.setWidgetResizable(True)


        self.choose_directory_button = QPushButton("Choose Directory")
        self.choose_directory_button.clicked.connect(self.choose_directory)
        self.layout.addWidget(self.choose_directory_button)
        
        self.add_prefix_suffix_action = self.file_menu.addAction("Add Prefix/Suffix")
        self.add_prefix_suffix_action.triggered.connect(self.add_prefix_suffix)

        self.find_replace_all_action = self.file_menu.addAction("Find & Replace All")
        self.find_replace_all_action.triggered.connect(self.find_replace_all)

        self.find_x_add_action = self.file_menu.addAction("Find X and Add After/Before")
        self.find_x_add_action.triggered.connect(self.find_x_add)

        self.dark_mode_action = self.file_menu.addAction("Dark Mode")
        self.dark_mode_action.setCheckable(True)
        self.dark_mode_action.toggled.connect(self.toggle_dark_mode)
        self.save_button.setObjectName("saveButton")



    def load_text(self):
        self.text_filename = os.path.splitext(self.images[self.current_image])[0] + ".txt"

        if os.path.exists(self.text_filename):
            with open(self.text_filename, "r") as file:
                self.textbox.setPlainText(file.read())
        else:
            self.textbox.setPlainText("")

    def show_thumbnails(self):
        self.clear_layout(self.layout)

        for i in reversed(range(self.thumbnail_layout.count())):
            self.thumbnail_layout.itemAt(i).widget().setParent(None)

        for index, image_path in enumerate(self.images):
            thumbnail_pixmap = QPixmap(image_path).scaled(150, 150, Qt.KeepAspectRatio, Qt.FastTransformation)

            thumbnail_label = QLabel()
            thumbnail_label.setPixmap(thumbnail_pixmap)
            thumbnail_label.setFixedSize(150, 150)
            thumbnail_label.mousePressEvent = lambda event, idx=index: self.show_image(idx)
            self.thumbnail_layout.addWidget(thumbnail_label, index // 4, index % 4)

        self.layout.addWidget(self.thumbnail_scroll_area)



    def show_image(self, index):
        self.current_image = index
        image_path = self.images[self.current_image]
        image = Image.open(image_path)
        if image.size[0] > 400 and image.size[1] > 400:
            image = image.resize((400, 400), Image.LANCZOS)
        image_qimage = QImage(image.tobytes("raw", "RGB"), image.size[0], image.size[1], QImage.Format_RGB888)
        image_qpixmap = QPixmap.fromImage(image_qimage)

        self.image_label.setPixmap(image_qpixmap)

        self.clear_layout(self.layout)
        self.layout.addWidget(self.scroll_area)

        control_layout = QVBoxLayout()
        nav_buttons_layout = QHBoxLayout()
        nav_buttons_layout.addWidget(self.left_button)
        nav_buttons_layout.addWidget(self.right_button)

        control_layout.addWidget(self.back_button)
        control_layout.addLayout(nav_buttons_layout)
        control_layout.addWidget(self.textbox)
        control_layout.addWidget(self.save_button)

        self.layout.addLayout(control_layout)

        self.load_text()
        self.image_label.setStyleSheet("border: none;")

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.setFocus()



    def show_next_image(self):
        if self.current_image is not None and self.current_image < len(self.images) - 1:
            self.show_image(self.current_image + 1)

    def show_previous_image(self):
        if self.current_image is not None and self.current_image > 0:
            self.show_image(self.current_image - 1)

    def choose_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Choose Directory")

        if directory:
            self.directory = directory
            self.load_images()

    def load_images(self):
        self.images = []  # clear previous images
        for file in os.listdir(self.directory):
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                image_path = os.path.join(self.directory, file)
                self.images.append(image_path)
                # Check and create txt file if it doesn't exist
                txt_path = os.path.splitext(image_path)[0] + ".txt"
                if not os.path.exists(txt_path):
                    with open(txt_path, "w") as txt_file:
                        txt_file.write("")

                # Add this line to display thumbnails after loading images
                self.show_thumbnails()



    def save_text(self):
        if self.text_filename:
            with open(self.text_filename, "w") as file:
                file.write(self.textbox.toPlainText())
            # Show a notification
            QMessageBox.information(self, "Info", "Text saved successfully.")
        else:
            QMessageBox.critical(self, "Error", "No text file loaded for current image.")



    def clear_layout(self, layout):
        for i in reversed(range(layout.count())):
            item = layout.takeAt(i)
            if item.widget() is not None:
                item.widget().setParent(None)
            else:
                self.clear_layout(item.layout())
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.show_thumbnails()
        elif event.key() == Qt.Key_Left:
            self.show_previous_image()
        elif event.key() == Qt.Key_Right:
            self.show_next_image()
        elif event.key() == Qt.Key_S and event.modifiers() == Qt.ControlModifier:
            self.save_text()
        else:
            super().keyPressEvent(event)

    def add_prefix_suffix(self):
        prefix, ok1 = QInputDialog.getText(self, "Prefix", "Enter the prefix:")
        suffix, ok2 = QInputDialog.getText(self, "Suffix", "Enter the suffix:")

        if ok1 and ok2:
            for root, _, files in os.walk(self.directory):
                for file in files:
                    if file.lower().endswith('.txt'):
                        old_path = os.path.join(root, file)
                        with open(old_path, "r") as f:
                            lines = [prefix + line.strip() + suffix for line in f]
                        with open(old_path, "w") as f:
                            f.write("\n".join(lines))

    def find_replace_all(self):
        find_text, ok1 = QInputDialog.getText(self, "Find", "Enter the text to find:")
        replace_text, ok2 = QInputDialog.getText(self, "Replace", "Enter the text to replace with:")

        if ok1 and ok2:
            for root, _, files in os.walk(self.directory):
                for file in files:
                    if file.lower().endswith('.txt'):
                        old_path = os.path.join(root, file)
                        with open(old_path, "r") as f:
                            content = f.read()
                        content = content.replace(find_text, replace_text)
                        with open(old_path, "w") as f:
                            f.write(content)

    def find_x_add(self):
        find_text, ok1 = QInputDialog.getText(self, "Find", "Enter the text to find:")
        add_text, ok2 = QInputDialog.getText(self, "Add", "Enter the text to add:")
        position, ok3 = QInputDialog.getItem(self, "Position", "Add text:", ["Before", "After"], editable=False)

        if ok1 and ok2 and ok3:
            for root, _, files in os.walk(self.directory):
                for file in files:
                    if file.lower().endswith('.txt'):
                        old_path = os.path.join(root, file)
                        with open(old_path, "r") as f:
                            lines = f.readlines()
                        with open(old_path, "w") as f:
                            for line in lines:
                                if find_text in line:
                                    if position == "Before":
                                        f.write(add_text + line)
                                    else:
                                        f.write(line.rstrip() + add_text + "\n")
                                else:
                                    f.write(line)


    def toggle_dark_mode(self, enabled):
        if enabled:
            self.setStyleSheet("""
                QMainWindow, QWidget, QScrollArea, QTextEdit, QMessageBox {
                    background-color: #262626;
                    color: white;
                }
                QLabel {
                    margin: 5px;
                    border: 1px solid #262626;
                    border-radius: 3px;
                }
                QLabel:hover {
                    border: 1px solid #aaaaaa;
                }
                QLabel:focus {
                    border: 1px solid #666666;
                }
                QPushButton {
                    background-color: #505050;
                    border: 1px solid #262626;
                    color: white;
                    border-radius: 3px;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #383838;
                }
                QPushButton:pressed {
                    background-color: #383838;
                }
                QPushButton#saveButton {
                    background-color: #4a9a7d;
                }
                QPushButton#saveButton:hover {
                    background-color: #3d816a;
                }
                QPushButton#saveButton:pressed {
                    background-color: #3d816a;
                }
                QMenuBar {
                    background-color: #262626;
                    color: white;
                }
                QMenuBar::item {
                    background-color: transparent;
                }
                QMenuBar::item:selected {
                    background-color: #383838;
                }
                QMenu {
                    background-color: #262626;
                    color: white;
                }
                QMenu::item:selected {
                    background-color: #383838;
                }
            """)
        else:
            self.setStyleSheet("""
                QLabel {
                    margin: 5px;
                    border: 1px solid #cccccc;
                    border-radius: 3px;
                }
                QLabel:hover {
                    border: 1px solid #aaaaaa;
                }
                QLabel:focus {
                    border: 1px solid #262626;
                }
            """)







if __name__ == "__main__":
    app = QApplication(sys.argv)
    image_browser = ImageBrowser()
    image_browser.setGeometry(100, 100, 800, 600)
    image_browser.show()
    sys.exit(app.exec_())