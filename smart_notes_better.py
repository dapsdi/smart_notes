from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QListWidget,
    QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QInputDialog
)

class SmartNotes(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Розумні Замітки")
        self.resize(800, 600)

        # основні елементи
        self.text_field = QTextEdit()
        self.text_field.setPlaceholderText("Введіть текст замітки...")

        self.notes_list = QListWidget()

        self.btn_create_note = QPushButton("Створити замітку")
        self.btn_delete_note = QPushButton("Видалити замітку")
        self.btn_save_note = QPushButton("Зберегти замітку")

        self.tag_list = QListWidget()
        self.write_tag = QLineEdit()
        self.write_tag.setPlaceholderText("Введіть тег...")

        self.btn_add_tag = QPushButton("Додати до замітки")
        self.btn_delete_tag = QPushButton("Відкріпити з замітки")
        self.btn_search_tag = QPushButton("Шукати за тегом")

        # права частина
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
        right_layout.addWidget(self.btn_delete_tag)

        # головне компонування
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.text_field, 2)
        main_layout.addLayout(right_layout, 1)
        self.setLayout(main_layout)

# запуск
app = QApplication([])
window = SmartNotes()

notes = []  # тут буде список типу: [[назва, текст, [теги]], ...]
number_note = 0

# Завантаження заміток із файлів
while True:
    filename = f"{number_note}.txt"
    try:
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()
            if len(lines) >= 3:
                title = lines[0].strip()
                text = lines[1].strip()
                tags = lines[2].strip().split()
                note = [title, text, tags]
                notes.append(note)
                window.notes_list.addItem(title)
        number_note += 1
    except IOError:
        break

# Показ замітки при натисканні
def show_note():
    selected_items = window.notes_list.selectedItems()
    if selected_items:
        key = selected_items[0].text()
        for note in notes:
            if note[0] == key:
                window.text_field.setText(note[1])
                window.tag_list.clear()
                window.tag_list.addItems(note[2])
                break

# Додавання нової замітки
def add_note():
    note_name, ok = QInputDialog.getText(window, "Додати замітку", "Назва замітки:")
    if ok and note_name:
        new_note = [note_name, "", []]
        notes.append(new_note)
        window.notes_list.addItem(note_name)
        file_index = len(notes) - 1
        with open(f"{file_index}.txt", "w", encoding="utf-8") as file:
            file.write(note_name + "\n")
            file.write("\n")  # пустий текст
            file.write("\n")  # пусті теги
        print(f"Замітку '{note_name}' створено та збережено як {file_index}.txt")

window.notes_list.itemClicked.connect(show_note)
window.btn_create_note.clicked.connect(add_note)

window.show()
app.exec_()
