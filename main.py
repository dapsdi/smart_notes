import json
from ui import window,app

from PyQt5.QtWidgets import (
    QInputDialog
)

def show_note():
    current_item = window.notes_list.selectedItems()
    if current_item:
        note_text = current_item[0].text()
        note_content = notes[note_text]["текст"]
        note_tags = notes[note_text]["теги"]

        window.text_field.setPlainText(note_content)
        window.tag_list.clear()
        window.tag_list.addItems(note_tags)
        
        


def add_note():
    note_name, ok = QInputDialog.getText(window, "Додати замітку", "Назва замітки:")

    if ok and note_name:
        if note_name not in notes:
            notes[note_name] = {"текст": "", "теги": []}
            window.notes_list.addItem(note_name)
            window.tag_list.addItems(notes[note_name]["теги"])
            print("Додано нову замітку:", note_name)
        else:
            print("Замітка з такою назвою вже існує.")

def del_note():
    selected_note = window.notes_list.currentItem()
    if selected_note:
        note_name = selected_note.text()
        notes.pop(note_name, None)
        with open("notes_data.json", "w", encoding = "utf-8") as file:
            json.dump(notes, file, ensure_ascii=False, indent=4)

        window.notes_list.clear()
        window.notes_list.addItems(notes) #оновлення списку заміток
        window.text_field.clear()
        window.tag_list.clear()
    else:
        print("Спочатку виберіть замітку для видалення.")

def save_notes():
    selected_note = window.notes_list.currentItem() #отримання вибраної замітки

    if selected_note:  #якщо вибрано замітку
        note_name = selected_note.text() #отримання назви замітки
        notes[note_name]["текст"] = window.text_field.toPlainText() #збереження тексту замітки
        with open("notes_data.json", "w", encoding = "utf-8") as file:
            json.dump(notes, file, ensure_ascii=False, indent=4)
    else:
        print("Спочатку виберіть замітку для збереження.")

def add_tag():
    selected_note = window.notes_list.currentItem() #отримання вибраної замітки
    if selected_note:
        note_name = selected_note.text() #отримання назви замітки
        tag_text = window.write_tag.text().strip() #отримання тексту тегу 
        if tag_text: #якщо тег не пустий
            if tag_text not in notes[note_name]["теги"]:
                notes[note_name]["теги"].append(tag_text)
                window.tag_list.addItem(tag_text)
                window.write_tag.clear()

                with open("notes_data.json", "w", encoding = "utf-8") as file:
                    json.dump(notes, file, ensure_ascii=False, indent=4)
                print("Тег додано:", tag_text)
            else:
                print("Тег вже існує в замітці.")
        else:
            print("Тег не може бути пустим.")
    else:
        print("Спочатку виберіть замітку для додавання тегу.")        

with open("notes_data.json", "r", encoding = "utf-8") as file:
    notes = json.load(file)

window.notes_list.addItems(notes)

#Прив'язка кнопок до функцій
window.btn_create_note.clicked.connect(add_note)
window.btn_delete_note.clicked.connect(del_note)
window.notes_list.itemClicked.connect(show_note)
window.btn_save_note.clicked.connect(save_notes)

window.show()
app.exec_() 
