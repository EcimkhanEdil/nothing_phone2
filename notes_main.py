#начни тут создавать приложение с умными заметками
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QInputDialog, QListWidget, QTextEdit, QLineEdit, QButtonGroup, QWidget, QHBoxLayout, QVBoxLayout, QGroupBox, QRadioButton, QPushButton, QLabel)
from random import shuffle,randint

import json

#notes={
#    'Добро пожаловать!':{
#        'текст':'Это самое лучшее приложение для заметок в мире!',
#        'теги':['добро','инструкция']
#    }
#}
#with open('notes_data.json','w')as file:
#    json.dump(notes,file)

app=QApplication([])

notes_win=QWidget()
notes_win.setWindowTitle('Умные дебики')
notes_win.resize(900,600)

list_notes=QListWidget()
list_notes_label=QLabel('Список дебиков')

baton_note_create=QPushButton('Создать дебика')
baton_note_del=QPushButton('Удалить дебика')
baton_note_save=QPushButton('Сохранить дебика')

field_tag=QLineEdit('')
field_tag.setPlaceholderText('Введите тег...')
field_text=QTextEdit()
button_tag_add=QPushButton('Добавить к заметке')
button_tag_del=QPushButton('Открепить от заметки')
baton_tag_search=QPushButton('Искать заметки по тегу')
list_tags=QListWidget()
list_tags_label=QLabel('Список тегов')

layout_notes=QHBoxLayout()
col_1=QVBoxLayout()
col_1.addWidget(field_text)

col_2=QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)
row_1=QHBoxLayout()
row_1.addWidget(baton_note_create)
row_1.addWidget(baton_note_del)
row_2=QHBoxLayout()
row_2.addWidget(baton_note_save)
col_2.addLayout(row_1)
col_2.addLayout(row_2)

col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)
row_3=QHBoxLayout()
row_3.addWidget(button_tag_add)
row_3.addWidget(button_tag_del)
row_4=QHBoxLayout()
row_4.addWidget(baton_tag_search)

col_2.addLayout(row_3)
col_2.addLayout(row_4)

layout_notes.addLayout(col_1,stretch=2)
layout_notes.addLayout(col_2,stretch=1)
notes_win.setLayout(layout_notes)

def add_tag():
    if list_notes.selectedItems():
        key=list_notes.selectedItems()[0].text()
        tag=field_tag.text()
        if not tag in notes[key]['теги']:
            notes[key]['теги'].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
        with open('notes_data.json','w',encoding='utf-8')as file:
            json.dump(notes,file,sort_keys=True,ensure_ascii=False)
        print(notes)
    else:
        print('Заметка для добавления тега не выбрана!')

def del_tag():
    if list_tags.selectedItems():
        key=list_notes.selectedItems()[0].text()
        tag=list_tags.selectedItems()[0].text()
        notes[key]['теги'].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]['теги'])
        with open('notes_data.json','w',encoding='utf-8')as file:
            json.dump(notes,file,sort_keys=True,ensure_ascii=False)
    else:
        print('Заметка для удаления тега не выбрана!')

def search_tag():
    print(baton_tag_search.text())
    tag=field_tag.text()
    if baton_tag_search.text()=='Искать заметки по тегу'and tag:
        print(tag)
        notes_filtered={}
        for note in notes:
            if tag in notes[note]['теги']:
                notes_filtered[note]=notes[note]
        baton_tag_search.setText('Сбросить поиск')
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)
        print(baton_tag_search.text())
    elif baton_tag_search.text()=='Сбросить поиск':
        field_tag.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
        baton_tag_search.setText('Искать заметки по тегу')
        print(baton_tag_search.text())
    else:
        pass

def add_note():
    note_name, ok = QInputDialog.getText(notes_win, 'Добавить заметку', 'Название заметки:')
    if ok and note_name!='':
        notes[note_name]={'текст':'','теги':[]}
        list_notes.addItem(note_name)
        list_tags.addItems(notes[note_name]['теги'])
        print(notes)

def show_note():
    key=list_notes.selectedItems()[0].text()
    print(key)
    field_text.setText(notes[key]['текст'])
    list_tags.clear()
    list_tags.addItems(notes[key]['теги'])

def save_note():
    if list_notes.selectedItems():
        key=list_notes.selectedItems()[0].text()
        notes[key]['текст']=field_text.toPlainText()
        with open('notes_data.json','w',encoding='utf-8')as file:
            json.dump(notes,file,sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print('Заметка для сохрарания не выбрана!')

def del_note():
    if list_notes.selectedItems():
        key=list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(notes)
        with open('notes_data.json','w',encoding='utf-8') as file:
            json.dump(notes,file,sort_keys=True,ensure_ascii=False)
        print(notes)
    else:
        print('Заметка для удаления не выбрана!')

baton_note_create.clicked.connect(add_note)
list_notes.itemClicked.connect(show_note)
baton_note_save.clicked.connect(save_note)
baton_note_del.clicked.connect(del_note)
button_tag_add.clicked.connect(add_tag)
button_tag_del.clicked.connect(del_tag)
baton_tag_search.clicked.connect(search_tag)

notes_win.show()

with open('notes_data.json','r',encoding='utf-8') as file:
    notes=json.load(file)
list_notes.addItems(notes)
app.exec_()