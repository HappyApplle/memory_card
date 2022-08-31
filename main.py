from PyQt5.QtCore import Qt
import json
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTextEdit, QListWidget, QLineEdit, QLabel, QHBoxLayout, QVBoxLayout, QInputDialog

app = QApplication([])
main_win = QWidget()

create_note = QPushButton('Создать заметку')
delete_note = QPushButton('Удалить заметку')
save_note = QPushButton('Сохранить заметку')
add_to_note = QPushButton('Добавить к заметке')
unpin_from_note = QPushButton('Открепить от заметки')
find_in_note = QPushButton('Искать заметки по тегу')


text_note = QTextEdit()
list_note1 = QListWidget()
teg_note1 = QListWidget()
write_teg = QLineEdit()

list_note2 = QLabel('Список заметок')
teg_note2 = QLabel('Список тегов')

layout1 = QHBoxLayout()
layout1.addWidget(create_note)
layout1.addWidget(delete_note)

layout2 = QHBoxLayout()
layout2.addWidget(add_to_note)
layout2.addWidget(unpin_from_note)

layout3 = QVBoxLayout()
layout3.addWidget(list_note2)
layout3.addWidget(list_note1)
layout3.addLayout(layout1)
layout3.addWidget(save_note)
layout3.addWidget(teg_note2)
layout3.addWidget(teg_note1)
layout3.addWidget(write_teg)
layout3.addLayout(layout2)
layout3.addWidget(find_in_note)

layout4 = QHBoxLayout()
layout4.addWidget(text_note)

layout4.addLayout(layout3)

notes = {
    'Добро пожаловать!': {                                              # название заметки
        'текст': 'Это самое лучшее приложение для заметок в мире!',     # текст заметки
        'теги': ["добро", "инструкция"]                                 # теги заметки
    }
}

                                         # записать список заметок в json файл

with open("notes_data.json", 'r') as file:
    notes = json.load(file)

list_note1.addItems(notes)

def show_note():
    name = list_note1.selectedItems()[0].text()                         # получаем название заметки на которую нажали
    print(name)                                                         # вывести на консоль
    text_note.setText(notes[name]['текст'])                             # в большое текстовое поле выводим текст заметки
    teg_note1.clear()                                                   # очищаем поле тегов (убираем все предыдущие)
    teg_note1.addItems(notes[name]['теги'])                             # добавляем теги нажатой заметкив список тегов

def add_note():
    note_name, ok = QInputDialog.getText(main_win, 'Добавить заметку', 'НАзвание заметки:')
    if note_name and ok != "":
        notes[note_name] = {
            'текст': '',
            'теги': [],
        }
        list_note1.addItem(note_name)
        teg_note1.clear()

def del_note():
    if list_note1.selectedItems():
        name = list_note1.selectedItems()[0].text()
        del notes[name]
        list_note1.clear()                                              # очистка списка заметок
        teg_note1.clear()
        text_note.clear()
        list_note1.addItems(notes)                                       # возвращение всех заметок кроме удаленной

        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True)

        print(notes)
    else:
        print('Заметка для удаления не выбрана!')

def save_notee():
    if list_note1.selectedItems():
        key = list_note1.selectedItems()[0].text()                      # получаем название заметки

        notes[key]['текст'] = text_note.toPlainText()                   # сохраняем текст из большого текстовоого поля

        with open('notes_data.json', 'w') as file:                      # перезаписываем файл
            json.dump(notes, file, sort_keys=True)                       # перезаписываем файл

list_note1.itemClicked.connect(show_note)
create_note.clicked.connect(add_note)
delete_note.clicked.connect(del_note)
save_note.clicked.connect(save_notee)

main_win.setLayout(layout4)
main_win.show()
app.exec_()