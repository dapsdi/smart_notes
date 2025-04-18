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
        
        window.notes_list.itemClicked.connect(show_note)


def add_note():
    note_name, ok = QInputDialog.getText(window, "Додати замітку", "Назва замітки:")

    if ok and note_name:
        if note_name not in notes:
            notes[note_name] = {"текст": "", "теги": []}
            window.tag_list.addItems(notes[note_name]["теги"])
            print("Додано нову замітку:", note_name)
        else:
            print("Замітка з такою назвою вже існує.")


with open("notes_data.json", "r", encoding = "utf-8") as file:
    notes = json.load(file)

window.notes_list.addItems(notes)

window.btn_create_note.clicked.connect(add_note)

app.exec_() 
