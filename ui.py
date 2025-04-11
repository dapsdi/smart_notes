
from PyQt5.QtWidgets import (
    QApplication,
    Qwidget,
    Qlabel,
    QpushButton,
    QListWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit
    
)

class SmartNotes(Qwidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Розумні Замітки")
        self.resize(800, 600)

        #основні елементи
        self.text_field = QTextEdit()
        self.notes_list = QListWidget()
        self.tag_list = QListWidget()

        self.write_tag = QlineEdit()

        #кнопки
        self.btn_create_note = QpushButton("Створити замітку")
        self.btn_delete_note = QpushButton("Видалити замітку")
        self.btn_save_note = QpushButton("Зберегти замітку")
        
         
