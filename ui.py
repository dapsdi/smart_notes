
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QListWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QLineEdit
    
)

class SmartNotes(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Розумні Замітки")
        self.resize(800, 600)

        #основні елементи
        self.text_field = QTextEdit() #поле для тексту замітки
        self.text_field.setPlaceholderText("Введіть текст замітки...")

        self.notes_list = QListWidget() #список заміток

        self.btn_create_note = QPushButton("Створити замітку")
        self.btn_delete_note = QPushButton("Видалити замітку")
        self.btn_save_note = QPushButton("Зберегти замітку")

        self.tag_list = QListWidget() #список тегів
 
        self.write_tag = QLineEdit() #текстове поле для тегів
        self.write_tag.setPlaceholderText("Введіть тег...")
        
        #кнопки для тегів

        self.btn_add_tag = QPushButton("Додати до замітки")
        self.btn_delete_tag = QPushButton("Відкріпити з замітки")
        self.btn_search_tag = QPushButton("Шукати за тегом")

        #права частина
        right_layout = QVBoxLayout()

        right_layout.addWidget(QLabel("Список заміток"))
        right_layout.addWidget(self.notes_list)

        right_layout.addWidget(self.btn_create_note)
        right_layout.addWidget(self.btn_save_note)
        right_layout.addWidget(self.btn_delete_note)

        right_layout.addWidget(QLabel("Список тегів"))
        right_layout.addWidget(self.tag_list)

        right_layout.addWidget(self.write_tag)
        right_layout.addWidget(self.btn_add_tag)
        right_layout.addWidget(self.btn_search_tag)

        # Головне компонування
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.text_field, 2)
        main_layout.addLayout(right_layout, 1)

        self.setLayout(main_layout)

#запуск
app = QApplication([])
window = SmartNotes()
