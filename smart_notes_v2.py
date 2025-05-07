from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QListWidget,
    QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QInputDialog
)

import os
import json
import csv

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
    selected_items = window.notes_list.selectedItems() #отримуємо вибраний елемент
    if selected_items: #якщо вибрано елемент
        key = selected_items[0].text() #отримуємо текст вибраного елемента
        for note in notes:
            if note[0] == key: #якщо назва замітки співпадає з вибраною
                window.text_field.setText(note[1]) #встановлюємо текст у text_field
                window.tag_list.clear() #очищаємо список тегів
                window.tag_list.addItems(note[2]) #додаємо теги до tag_list
                
                break #виходимо з циклу, якщо знайшли замітку для редагування

# Додавання нової замітки
def add_note():
    note_name, ok = QInputDialog.getText(window, "Додати замітку", "Назва замітки:")
    if ok and note_name:
        new_note = [note_name, "", []] #нова замітка
        notes.append(new_note)
        window.notes_list.addItem(note_name)
        file_index = len(notes) - 1 #індекс нової замітки
        with open(f"{file_index}.txt", "w", encoding="utf-8") as file:
            file.write(note_name + "\n")
            file.write("\n")  # пустий текст
            file.write("\n")  # пусті теги
        print(f"Замітку '{note_name}' створено та збережено як {file_index}.txt")

def save_note():
    selected_item = window.notes_list.selectedItems() #отримуємо вибраний елемент
    if selected_item: 
        note_name = selected_item[0].text() #отримуємо текст вибраного елемента
        for note in notes: #перебираємо всі замітки
            if note[0] == note_name: #якщо назва замітки співпадає з вибраною
                note[1] = window.text_field.toPlainText()
                note[2] = [window.tag_list.item(i).text() for i in range(window.tag_list.count())] #пройти по всіх елементах у window.tag_list взяти їхній текст і записати в note[2] як список
                with open(f"{notes.index(note)}.txt", "w", encoding="utf-8") as file:
                    file.write(note[0] + "\n") #записати назву
                    file.write(note[1] + "\n") #записати текст
                    file.write(" ".join(note[2]) + "\n") #записати теги в один рядок чере пробіл
                break #виходимо з циклу, якщо знайшли замітку для редагування

                #note[2] = [window.tag_list.item(i).text() for i in range(window.tag_list.count())]
                #Цей рядок — ключовий для збереження тегів, бо він збирає актуальний список з інтерфейсу
                #і записує у структуру note, яку потім можна зберігати у файл та перетворювати в JSON, CSV

def delete_note():
    selected_item = window.notes_list.selectedItems() #отримуємо вибраний елемент
    if selected_item:
        note_name = selected_item[0].text() #отримуємо текст вибраного елемента
        for note in notes: #перебираємо всі замітки
            if note[0] == note_name: #якщо назва замітки співпадає з вибраною
                filename = f"{note}.txt" #формуємо назву файлу  i - індекс замітки
                if os.path.exists(filename): #перевіряємо, чи файл існує
                    os.remove(filename) #видаляємо файл
                    print(f"Замітку '{note_name}' видалено.")
                notes.pop(notes.index(note)) #видаляємо замітку з пам'яті
                window.notes_list.takeItem(window.notes_list.row(selected_item[0])) #видаляємо замітку зі списку
                window.text_field.clear() #очищаємо текстове поле
                window.tag_list.clear()
                
                break #виходимо з циклу, якщо знайшли замітку для редагування

def add_tag():
    selected_item = window.notes_list.selectedItems() #отримуємо вибраний елемент
    if selected_item:
        tag = window.write_tag.text() #отримуємо текст з поля введення тегу
        if tag:
            note_name = selected_item[0].text() #отримуємо текст вибраного елемента
            for note in notes:
                if note[0] == note_name and tag not in note[2]: #якщо назва замітки співпадає з вибраною і тег не входить до списку тегів
                    note[2].append(tag) 
                    window.tag_list.addItem(tag) #додаємо тег до списку тегів
                    filename = f"{notes.index(note)}.txt" #формуємо назву файлу
                    with open(filename, "w", encoding="utf-8") as file:
                        file.write(note[0] + "\n") #записати назву
                        file.write(note[1] + "\n") #записати текст
                        file.write(" ".join(note[2]) + "\n") #записати теги в один рядок чере пробіл
                    print(f"Тег '{tag}' додано до замітки '{note_name}'.")

                    break #виходимо з циклу якщо знайшли замітку для редагування

                    #if note[0] == key and tag not in note[2]:
                    #це умова яка перевіряє одночасно дві речі
                    
                    #по-перше чи ця замітка та, яку зараз вибрано? 
                    #чи ще не додано цей тег у цю замітку?

                    #це перевірка: знайди ту замітку яка зараз обрана 
                    #і якщо в ній ще немає введеного тегу тоді додавай


def delete_tag():
    note_names = window.notes_list.selectedItems() #отримуємо вибраний елемент
    tag_names = window.tag_list.selectedItems() #отримуємо вибраний тег

    if note_names and tag_names: #якщо вибрано елемент і тег
        note_name = note_names[0].text() #отримуємо текст вибраного елемента
        tag_name = tag_names[0].text() #отримуємо текст вибраного тегу
        
        for note in notes: #перебираємо всі замітки
            if note[0] == note_name and tag_name in note[2]: #якщо назва замітки співпадає з вибраною 
                                                             #і тег входить до списку тегів
                note[2].remove(tag_name) #видаляємо тег з замітки
                window.tag_list.takeItem(window.tag_list.row(tag_names[0])) #видаляємо тег зі списку
                filename = f"{notes.index(note)}.txt" #формуємо назву файлу

                with open(filename, "w", encoding="utf-8") as file:
                    file.write(note[0] + "\n") #записати назву
                    file.write(note[1] + "\n") #записати текст  
                    file.write(" ".join(note[2]) + "\n") #записати теги в один рядок чере пробіл
                print(f"Тег '{tag_name}' видалено з замітки '{note_name}'.")
                
                break #виходимо з циклу, якщо знайшли замітку для редагування    



window.notes_list.itemClicked.connect(show_note)
window.btn_create_note.clicked.connect(add_note)

window.show()
app.exec_()
