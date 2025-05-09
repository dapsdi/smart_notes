from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QListWidget,
    QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QInputDialog, QMessageBox
)

import os
import json
import csv

class SmartNotes(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Розумні Замітки")
        self.resize(800, 600)
        app_style = """
            QWidget {
                background-color: #f6fbe7; /* very light olive background */
                font-family: Arial;
                font-size: 14px;
            }

            QPushButton {
                background-color: #b5c99a;     /* light olive green */
                border: 2px solid #7d8f69;     /* darker green border */
                border-radius: 10px;
                padding: 6px 12px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #c9dbac;     /* hover effect */
            }

            QTextEdit, QLineEdit {
                background-color: #ffffff;
                border: 2px solid #b5c99a;
                border-radius: 8px;
                padding: 4px;
            }

            QListWidget {
                background-color: #ffffff;
                border: 2px solid #b5c99a;
                border-radius: 8px;
                padding: 4px;
            }

            QLabel {
                font-weight: bold;
                color: #4f5d2f;
            }
        """
        self.setStyleSheet(app_style)


        #основні елементи
        self.text_field = QTextEdit()
        self.text_field.setPlaceholderText("Введіть текст замітки...")

        self.notes_list = QListWidget()
        
        #кнопки
        self.btn_create_note = QPushButton("Створити замітку")
        self.btn_delete_note = QPushButton("Видалити замітку")
        self.btn_save_note = QPushButton("Зберегти замітку")

        self.tag_list = QListWidget()
        self.write_tag = QLineEdit()
        self.write_tag.setPlaceholderText("Введіть тег...")

        self.btn_add_tag = QPushButton("Додати до замітки")
        self.btn_delete_tag = QPushButton("Відкріпити з замітки")
        self.btn_search_tag = QPushButton("Шукати за тегом")
        self.btn_clear_tags = QPushButton("Очистити теги")

        self.btn_export_csv = QPushButton("Експортувати в CSV")
        self.btn_import_csv = QPushButton("Імпортувати з CSV")

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
        right_layout.addWidget(self.btn_delete_tag)
        right_layout.addWidget(self.btn_clear_tags)

        right_layout.addWidget(self.btn_export_csv)
        right_layout.addWidget(self.btn_import_csv)

        #головне компонування

        # Ліва частина: поле для тексту з підписом
        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("Текст замітки"))
        left_layout.addWidget(self.text_field)


        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout, 2) #2 - це відносна вага, яка визначає, скільки місця займатиме ця частина
        main_layout.addLayout(right_layout, 1)
        self.setLayout(main_layout)

#запуск
app = QApplication([])
window = SmartNotes()

notes = []  #тут буде список типу: [[назва, текст, [теги]], ...]
number_note = 0

#завантаження заміток із файлів
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

#показ замітки при натисканні
def show_note():

    save_note() #зберігаємо замітку перед показом нової

    selected_items = window.notes_list.selectedItems() #отримуємо вибраний елемент
    if selected_items: #якщо вибрано елемент
        key = selected_items[0].text() #отримуємо текст вибраного елемента
        for note in notes:
            if note[0] == key: #якщо назва замітки співпадає з вибраною
                window.text_field.setText(note[1]) #встановлюємо текст у text_field
                window.tag_list.clear() #очищаємо список тегів
                window.tag_list.addItems(note[2]) #додаємо теги до tag_list
                
                break #виходимо з циклу, якщо знайшли замітку для редагування

#додавання нової замітки
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

#збереження замітки
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

#видалення замітки
def delete_note():
    selected_item = window.notes_list.selectedItems() #отримуємо вибраний елемент
    if selected_item:
        note_name = selected_item[0].text() #отримуємо текст вибраного елемента
        for note in notes: #перебираємо всі замітки
            if note[0] == note_name: #якщо назва замітки співпадає з вибраною
                filename = f"{note}.txt" #формуємо назву файлу  i - індекс замітки
                if os.path.exists(filename): #перевіряємо, чи файл існує
                    
                    reply = QMessageBox.question(
                        window, "Підтвердження видалення",
                        f"Ви впевнені, що хочете видалити замітку '{note_name}'?",
                        QMessageBox.Yes | QMessageBox.No,
                    )
                    if reply == QMessageBox.No:
                        return #якщо натиснули "Ні", виходимо з функції

                    os.remove(filename) #видаляємо файл
                    print(f"Замітку '{note_name}' видалено.")
                notes.pop(notes.index(note)) #видаляємо замітку з пам'яті
                window.notes_list.takeItem(window.notes_list.row(selected_item[0])) #видаляємо замітку зі списку
                window.text_field.clear() #очищаємо текстове поле
                window.tag_list.clear()
                
                break #виходимо з циклу, якщо знайшли замітку для редагування

#додавання тегу
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

#видалення тегу
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

def clear_tags():
    selected_item = window.notes_list.selectedItems() #отримуємо вибраний елемент
    if selected_item:
        note_name = selected_item[0].text() #отримуємо текст вибраного елемента
        for note in notes:
            if note[0] == note_name: #якщо назва замітки співпадає з вибраною
                note[2]= [] #очищаємо список тегів
                window.tag_list.clear() #очищаємо список тегів

                filename = f"{notes.index(note)}.txt" #формуємо назву файлу
                with open(filename, "w", encoding="utf-8") as file:
                    file.write(note[0] + "\n") #записати назву
                    file.write(note[1] + "\n") #записати текст
                    file.write("\n") #пусті теги
                    print(f"Теги очищено з замітки '{note_name}'.") 
                
                break #виходимо з циклу, якщо знайшли замітку для редагування

#експорт у CSV    
def export_to_csv(): #Ця функція бере всі замітки, які зараз є в пам’яті (у списку notes), 
                     #і зберігає їх у файл notes.csv, щоб потім можна було знову завантажити.

    with open("notes.csv", "w", encoding="utf-8", newline="") as file: #newline="": запобігає додатковим порожнім рядкам між записами у Windows. 
                                                                       #без цього в CSV-файлі могли б з'являтись зайві рядки
        
        writer = csv.writer(file) #створює об'єкт writer який дозволяє записувати рядки у CSV файл (по суті — як таблицю)
        
        writer.writerow(["Назва", "Текст", "Теги"]) #writerow() це метод для запису одного рядка у CSV файл
        
        for note in notes: #перебираємо список notes; 
                           #Кожна замітка це список: [назва, текст, [теги]]

            writer.writerow([note[0], note[1], " ".join(note[2])]) # " ".join(note[2]): перетворює список тегів на один рядок, розділений пробілами (щоб записати у файл)
                                                                   #(наприклад, ["важливо", "робота"] → "важливо робота")
    print("Усі замітки експортовано у notes.csv")

#імпорт з CSV
def import_from_csv(): #ця функція читає файл notes.csv 
                       #і завантажує всі замітки назад у програму додаючи їх до інтерфейсу

                       #1. відкриває notes.csv для читання

                       #2. csv.DictReader(file) читає файл як словники:
                       #{"Назва": ..., "Текст": ..., "Теги": ...}
                    
                       #3.для кожного рядка:
                            # зчитує назву, текст і теговий рядок.
                            # .split() перетворює теговий рядок у список

                       #4. додає замітку до списку notes

                       #5. виводить назву замітки в графічному інтерфейсі (notes_list). 

    if os.path.exists("notes.csv"):
        with open ("notes.csv", "r", encoding="utf-8") as file:
            reader = csv.Dictreader(file) #DictReader читає кожен рядок CSV файлу як словник
                                          #ключами словника є заголовки з першого рядка ("Назва", "Текст", "Теги")
            notes.clear
            window.notes_list.clear()

            for row in reader: #перебираємо по кожному рядку з файлу (у вигляді словника row)
                title = row["Назва"]
                text = row["Текст"] #дістаємо значення по ключах "Назва", "Текст" і "Теги".

                tags = row["Теги"].split() #.split() перетворює теговий рядок на список тегів.
                                           #наприклад: "важливо робота" до ["важливо", "робота"]

                notes.append[title, text, tags]
                window.notes_list.addItem(title)
        print("Замітки імпортовано з файлу notes.csv")
    else:
        print("Файл notes.csv не знайдено.")
            

#підключення функцій до кнопок
window.notes_list.itemClicked.connect(show_note)
window.btn_create_note.clicked.connect(add_note)
window.btn_save_note.clicked.connect(save_note)
window.btn_delete_note.clicked.connect(delete_note)

window.btn_add_tag.clicked.connect(add_tag)
window.btn_delete_tag.clicked.connect(delete_tag)
window.btn_search_tag.clicked.connect(clear_tags)

window.btn_export_csv.clicked.connect(export_to_csv)
window.btn_import_csv.clicked.connect(import_from_csv)

window.show()
app.exec_()
