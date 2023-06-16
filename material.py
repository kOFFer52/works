from tkinter import *
from tkinter import ttk
from tkinter.ttk import Style
from tkinter import messagebox
import json
import os
import threading
import time
import os.path

#___________________________________________________________________ ПРОВОД ___________________________________________________________________#

def _save_add_wire(): # СОЗДАНИЕ НОВОГО ПРОВОДА
    global dict_name, dwi_b
    dict_name = wire_marking_entry.get()
    name = dict_name
    bwd_a = float(bwd_a_add.get()) # диаметр провода без изоляции А
    bwd_b = float(bwd_b_add.get()) # диаметр провода без изоляции Б
    its = float(its_add.get()) # толщина изоляции на две стороны
    stn = float(stn_add.get()) # сечение
    wom = float(wom_add.get()) # масса одного метра
    mtl = mtl_add.get() # материал
    wsp = wsp_add.get() # форма провода
    if bwd_b !=0:
        dwi_a = bwd_a + its
        dwi_b = bwd_b + its
    else:
        dwi_a = bwd_a + its
        dwi_b = 0.0
    # dwi_a = bwd_a + its # размеры с изолчцией А
    # dwi_b = bwd_b + its # размеры с изоляцией Б 

    # Создание файла с названием нового провода(словаря)
    file_path = os.path.join('Data', dict_name + '.dat')
    with open(file_path, 'w') as file:
        json.dump(dict_name, file)
         
    # Добавление в созданный файл информации 
    name = {'bwd_a':bwd_a, 'bwd_b':bwd_b, 'its':its, 'stn':stn, 'wom':wom, 'mtl':mtl, 'wsp':wsp, 'dwi_a':dwi_a, 'dwi_b':dwi_b}
    with open(file_path, 'w') as file:
        json.dump(name, file)
    
    # Добавление нового провода в listbox(добавление значения в словарь wiredict.dat)
    key = dict_name  # Новый ключ для словаря
    value = 1  # Получаем значение ключа из Entry
    wire_dictionary[key] = value  # Добавляем новый ключ и значение в словарь
    with open('Data\wiredict.dat', 'w') as f:  # Сохраняем измененный словарь в файл
        json.dump(wire_dictionary, f)
        
def _update_wire_brand_listbox(): # ОБНОВЛЕНИЕ LISTBOX С ДАННЫМИ( ДОБАВЛЕНИЕ НОВОГО ПРОВОДА )
    # Удаляем все элементы из Listbox
    wire_brand_listbox.delete(0, END)
    time.sleep(0.2)
    # Добавляем новые элементы из словаря
    for key in wire_dictionary:
        wire_brand_listbox.insert(END, key)

def _add_wire_destroy(): # ЗАКРЫТИЕ ОКНА СОХРАНЕНИЯ ПРОВОДА
    add_wire_window.destroy()

def _to_change_destroy(): # ЗАКРЫТИЕ ОКНА ПРАВКИ ЗАНЧЕНИЙ ПРОВОДА
    to_change_window.destroy()    

def _wire_save_threading(): # СОХРАНЕНИЕ, ОБНОВЛЕНИЕ И ВЫХОД ИЗ ОКНА ДОБАВЛЕНИЕ ПРОВОДА
    threading.Thread(target=_save_add_wire).start()
    threading.Thread(target=_add_wire_destroy).start()
    threading.Thread(target=_update_wire_brand_listbox).start()

def _add_wire(): # ОКНО ДОБАВЛЕНИЕ НОВОГО ПРОВОДА
    global add_wire_window
    add_wire_window = Toplevel(material)
    add_wire_window.geometry('360x325+1000+150')
    add_wire_window.title('Добавление провода')
    add_wire_window['bg'] = 'gray82'
    
    ########## СТАНДАРТНЫЕ АТРИБУТЫ ##########
    word_font = 'Arial 10'
    win_bg = 'gray82'
    ####################
    global wire_marking_entry, bwd_a_add, bwd_b_add, its_add, stn_add, wom_add, mtl_add, wsp_add
    # Маркировка провода
    wire_marking_label = Label(add_wire_window, text='Маркировака провода', bg=win_bg, font=word_font)
    wire_marking_label.place(x=10, y=10)
    wire_marking_entry = Entry(add_wire_window, width=15)
    wire_marking_entry.place(x=250, y=10)
    # Диаметр провода без изоляции
    bwd_label = Label(add_wire_window, text='Диаметр провода без изоляции, мм', bg=win_bg, font=word_font)
    bwd_label.place(x=10, y=40)
    bwd_a_add = Entry(add_wire_window, width=7)
    bwd_a_add.place(x=250, y=40)
    bwd_b_add = Entry(add_wire_window, width=7)
    bwd_b_add.place(x=298, y=40)
    # Толщина изоляции на две стороны
    its_label = Label(add_wire_window, text='Толщина изоляции на две стороны, мм', bg=win_bg, font=word_font)
    its_label.place(x=10, y=70)
    its_add = Entry(add_wire_window, width=15)
    its_add.place(x=250, y=70)
    # Cечение
    stn_label = Label(add_wire_window, text='Сечение, мм^2', bg=win_bg, font=word_font)
    stn_label.place(x=10, y=100)
    stn_add = Entry(add_wire_window, width=15)
    stn_add.place(x=250, y=100)
    # Масса одного метра
    wom_label = Label(add_wire_window, text='Масса одного метра, кг', bg=win_bg, font=word_font)
    wom_label.place(x=10, y=130)
    wom_add = Entry(add_wire_window, width=15)
    wom_add.place(x=250, y=130)
    # Материал
    mtl_label = Label(add_wire_window, text='Материал', bg=win_bg, font=word_font)
    mtl_label.place(x=10, y=160)
    mtl_add = ttk.Combobox(add_wire_window, values=['Медь','Алюминий'], width=15)
    mtl_add.current(0)
    mtl_add.place(x=250, y=160)
    # Форма провода [wsp]
    wsp_label = Label(add_wire_window, text='Форма провода', bg=win_bg, font=word_font)
    wsp_label.place(x=10, y=190)
    wsp_add = ttk.Combobox(add_wire_window, values=['Круглый','Прямоугольный'], width=15)
    wsp_add.current(0)
    wsp_add.place(x=250, y=190)
    # Кнопка - Сохранить
    save_add_button = Button(add_wire_window, text='Сохранить', command=_wire_save_threading)
    save_add_button.place(x=10, y=280)
    # Кнопка - Выйти 
    quit_wire_button = Button(add_wire_window, text='Выйти', command=add_wire_window.destroy)
    quit_wire_button.place(x=100, y=280)
    
def updates_wire_parameters_labels(event): # ОБНОВЛЕНИЕ ЗНАЧЕНИЙ ПРОВОДА В ОКНЕ СПРАВА ОТ LISTBOX
    global to_change_button, selected_value
    files = os.listdir('Data') # Получаем список файлов в папке
    for i in files:   
        selected_value = wire_brand_listbox.get(wire_brand_listbox.curselection()) # Получаем значение выбранное в listbox
        if selected_value in i:# Проверяем, соответствует ли выбранное значение названию файла в папке
            to_change_button['state'] = 'active' # активация кнопки - ИЗМЕНИТЬ
            # print('Выбранное значение соответствует названию файла в папке')
            with open('Data\\' + selected_value + '.dat', 'r') as f: # если соответствие найдено, открываем файл для чтения, помощью функции `open()` и прочитать его содержимое с помощью метода `read()`
                data = f.read() 
                dict = eval(data) #  Использовать функцию `eval()` для преобразования строки со словарем в объект
                bwd_label_a_value.configure(text=dict['bwd_a'])
                if dict['bwd_b'] > 0:                  
                    bwd_label_b_value.configure(text=dict['bwd_b'])
                else:
                    bwd_label_b_value.configure(text='')
                its_label_value.configure(text=dict['its'])
                stn_label_value.configure(text=dict['stn'])
                wom_label_value.configure(text=dict['wom'])
                mtl_label_value.configure(text=dict['mtl'])
                wsp_label_value.configure(text=dict['wsp'])
                dwi_label_a_value.configure(text=((dict['bwd_a'] + dict['its'])))
                if dict['bwd_b'] > 0:
                    dwi_label_b_value.configure(text=((dict['bwd_b'] + dict['its'])))
                else:
                    dwi_label_b_value.configure(text='')    
        else: # если соответствий не найдено, пропускаем
            # print('Выбранное значение не соответствует названию файла в папке')
            pass
 
def _del_wire(): # УАЛЕНИЕ ЗНАЧЕНИЯ(ПРОВОДА) ИЗ LISTBOX
    # получаем индекс выбранного элемента в listbox
    index = wire_brand_listbox.curselection()[0]
    # получаем ключ выбранного элемента
    key = wire_brand_listbox.get(index)
    # удаляем элемент из словаря по ключу
    del wire_dictionary[key]
    temp_dict = wire_dictionary
    with open('Data\\wiredict.dat', 'w') as file:
        json.dump(temp_dict, file)
    # удаляем элемент из listbox
    wire_brand_listbox.delete(index)

    # удаление файла из паки
    file_path = os.path.join('Data', key + '.dat') # указываем путь к файлу, который нужно удалить
    # if os.path.exists(file_path): # проверяем, существует ли файл
    os.remove(file_path) # удаляем файл
         
def _to_change(): # ИЗМЕНЕНИЕ(ПРАВКА) ЗНАЧЕНИЙ ПРОВОДА
    global to_change_window, dict_name, bwd_a_add, bwd_b_add, its_add, stn_add, wom_add, mtl_add, wsp_add, change_dict
    to_change_window = Toplevel(material)
    to_change_window.geometry('360x325+1000+150')
    to_change_window.title('Правка значений')
    to_change_window['bg'] = 'gray82'
    
    ########## СТАНДАРТНЫЕ АТРИБУТЫ ##########
    word_font = 'Arial 10'
    win_bg = 'gray82'
    ####################

    # Диаметр провода без изоляции
    bwd_label = Label(to_change_window, text='Диаметр провода без изоляции, мм', bg=win_bg, font=word_font)
    bwd_label.place(x=10, y=40)
    bwd_a_add = Entry(to_change_window, width=7)
    bwd_a_add.place(x=250, y=40)
    bwd_b_add = Entry(to_change_window, width=7)
    bwd_b_add.place(x=298, y=40)
    # Толщина изоляции на две стороны
    its_label = Label(to_change_window, text='Толщина изоляции на две стороны, мм', bg=win_bg, font=word_font)
    its_label.place(x=10, y=70)
    its_add = Entry(to_change_window, width=15)
    its_add.place(x=250, y=70)
    # Cечение
    stn_label = Label(to_change_window, text='Сечение, мм^2', bg=win_bg, font=word_font)
    stn_label.place(x=10, y=100)
    stn_add = Entry(to_change_window, width=15)
    stn_add.place(x=250, y=100)
    # Масса одного метра
    wom_label = Label(to_change_window, text='Масса одного метра, кг', bg=win_bg, font=word_font)
    wom_label.place(x=10, y=130)
    wom_add = Entry(to_change_window, width=15)
    wom_add.place(x=250, y=130)
    # Материал
    mtl_label = Label(to_change_window, text='Материал', bg=win_bg, font=word_font)
    mtl_label.place(x=10, y=160)
    mtl_add = ttk.Combobox(to_change_window, values=['Медь','Алюминий'], width=15)
    mtl_add.current(0)
    mtl_add.place(x=250, y=160)
    # Форма провода [wsp]
    wsp_label = Label(to_change_window, text='Форма провода', bg=win_bg, font=word_font)
    wsp_label.place(x=10, y=190)
    wsp_add = ttk.Combobox(to_change_window, values=['Круглый','Прямоугольный'], width=15)
    wsp_add.current(0)
    wsp_add.place(x=250, y=190)
  
    if selected_value in i:# Проверяем, соответствует ли выбранное значение названию файла в папке
        to_change_button['state'] = 'active' # активация кнопки - ИЗМЕНИТЬ
    with open('Data\\' + selected_value + '.dat', 'r') as f: # открываем файл для чтения, помощью функции `open()` и прочитать его содержимое с помощью метода `read()`
        data = f.read() 
        change_dict = eval(data) #  Использовать функцию `eval()` для преобразования строки со словарем в объект
        bwd_a_add.insert(END, change_dict['bwd_a'])
        bwd_b_add.insert(END, change_dict['bwd_b'])
        its_add.insert(END, change_dict['its'])
        stn_add.insert(END, change_dict['stn'])
        wom_add.insert(END, change_dict['wom'])
        # mtl_add.insert(END, change_dict['mtl']) # !!!!!!!!!!!!!!!!!!!!!
        # wsp_add.insert(END, change_dict['wsp']) # !!!!!!!!!!!!!!!!!!!!!

    # Кнопка - Сохранить
    save_add_button = Button(to_change_window, text='Сохранить', command=_save_change)
    save_add_button.place(x=10, y=280)
    # Кнопка - Выйти 
    quit_wire_button = Button(to_change_window, text='Выйти', command=_to_change_destroy)
    quit_wire_button.place(x=100, y=280)         
         
def _save_change(): # СОХРАНЕНИЕ ИЗМЕНЕННЫХ ЗНАЧЕНИЙ ПРОВОДА
    global bwd_a_add, bwd_b_add, its_add, stn_add, wom_add, mtl_add, wsp_add
    name = change_dict
    bwd_a = float(bwd_a_add.get())
    bwd_b = float(bwd_b_add.get())
    its = float(its_add.get())
    stn = float(stn_add.get())
    wom = float(wom_add.get())
    mtl = mtl_add.get()
    wsp = wsp_add.get()
    # Добавление в созданный файл информации 
    name = {'bwd_a':bwd_a, 'bwd_b':bwd_b, 'its':its, 'stn':stn, 'wom':wom, 'mtl':mtl, 'wsp':wsp, 'dwi':''}
    with open('Data\\' + selected_value + '.dat', 'w') as file:
        json.dump(name, file)

#___________________________________________________________________ ИЗОЛЯЦИЯ ___________________________________________________________________#

def _update_reil_profile_listbox(): # ОБНОВЛЕНИЕ LISTBOX С ДАННЫМИ( ДОБАВЛЕНИЕ НОВОЙ ИЗОЛЯЦИИ )
    # Удаляем все элементы из Listbox
    reil_profile_listbox.delete(0, END)
    time.sleep(0.2)
    # Добавляем новые элементы из словаря
    for key in reil_dictionary:
        reil_profile_listbox.insert(END, key)
        
def _updates_reil_profile_labels(event): # ОБНОВЛЕНИЕ ЗНАЧЕНИЙ ИЗОЛЯЦИИ В ОКНЕ СПРАВА ОТ LISTBOX
    global selected_value
    files = os.listdir('Data') # Получаем список файлов в папке
    for i in files:   
        selected_value = reil_profile_listbox.get(reil_profile_listbox.curselection()) # Получаем значение выбранное в listbox
        if selected_value in i:# Проверяем, соответствует ли выбранное значение названию файла в папке
            # to_change_button['state'] = 'active' # активация кнопки - ИЗМЕНИТЬ
            # print('Выбранное значение соответствует названию файла в папке')
            with open('Data\\' + selected_value + '.dat', 'r') as f: # если соответствие найдено, открываем файл для чтения, помощью функции `open()` и прочитать его содержимое с помощью метода `read()`
                data = f.read() 
                dict = eval(data) #  Использовать функцию `eval()` для преобразования строки со словарем в объект
                material_label_value.configure(text=dict['iso'])
                dimensions_a_rail_lab_value.configure(text=dict['dar'])
                dimensions_b_rail_lab_value.configure(text=dict['dbr'])
                weight_of_one_kilogram_lab_value.configure(text=dict['wok'])

        else: # если соответствий не найдено, пропускаем
            # print('Выбранное значение не соответствует названию файла в папке')
            pass

def _add_rack(): # ДОБАВЛЕНИЕ НОВОЙ РЕЙКИ
    global add_reil_window, add_reil_combo, add_reil_entry, dimensions_a_rail, dimensions_b_rail, weight_of_one_kilogram
    add_reil_window = Toplevel(material)
    add_reil_window.geometry('360x325+1000+150')
    add_reil_window.title('Добавление изоляции')
    add_reil_window['bg'] = 'gray82'    

    add_reil_combo_labal = Label(add_reil_window, text='Материал', font=word_font, bg=win_bg)
    add_reil_combo_labal.place(x=10, y=10)
    add_reil_values = ['Рейка','Межслоевая изоляция']
    add_reil_combo = ttk.Combobox(add_reil_window, values=add_reil_values, width=21)
    add_reil_combo.current(0)
    add_reil_combo.place(x=10, y=40)
    selected_add_reil_value = add_reil_combo.get()
    
    add_reil_entry_label = Label(add_reil_window, text='Название', font=word_font, bg=win_bg)
    add_reil_entry_label.place(x=10, y=70)
    add_reil_entry = Entry(add_reil_window, width=20)
    add_reil_entry.place(x=150, y=70)
    
    dimensions_a_rail_label = Label(add_reil_window, text='Размеры A рейки', font=word_font, bg=win_bg)
    dimensions_a_rail_label.place(x=10, y=100)
    dimensions_a_rail = Entry(add_reil_window, width=20, state=NORMAL)
    dimensions_a_rail.place(x=150, y=100)
    
    dimensions_b_rail_label = Label(add_reil_window, text='Размеры B рейки', font=word_font, bg=win_bg)
    dimensions_b_rail_label.place(x=10, y=130)
    dimensions_b_rail = Entry(add_reil_window, width=20, state=NORMAL)
    dimensions_b_rail.place(x=150, y=130)
    
    weight_of_one_kilogram_label = Label(add_reil_window, text='Масса 1м/кг', font=word_font, bg=win_bg)
    weight_of_one_kilogram_label.place(x=10, y=160)
    weight_of_one_kilogram = Entry(add_reil_window, width=20, state=NORMAL)
    weight_of_one_kilogram.place(x=150, y=160)
        
    save_reil_button = Button(add_reil_window, text='Сохранить', command=_reil_save_threading)
    save_reil_button.place(x=10, y=280)

    quit_reil_button = Button(add_reil_window, text='Выйти', command=add_reil_window.destroy)
    quit_reil_button.place(x=100, y=280)

def _del_rack(): # УДАЛЕНИЕ РЕЙКИ
    # получаем индекс выбранного элемента в listbox
    index = reil_profile_listbox.curselection()[0]
    # получаем ключ выбранного элемента
    key = reil_profile_listbox.get(index)
    # удаляем элемент из словаря по ключу
    del reil_dictionary[key]
    temp_dict = reil_dictionary
    with open('Data\\reildict.dat', 'w') as file:
        json.dump(temp_dict, file)
    # удаляем элемент из listbox
    reil_profile_listbox.delete(index)

    # удаление файла из паки
    file_path = os.path.join('Data', key + '.dat') # указываем путь к файлу, который нужно удалить
    # if os.path.exists(file_path): # проверяем, существует ли файл
    os.remove(file_path) # удаляем файл

def _reil_save(): # СОХРАНЕНИЕ РЕЙКИ
    global reil_dictionary
    arc = add_reil_combo.get()
    reil_dict_name = add_reil_entry.get()
    mn = reil_dict_name
    dar = float(dimensions_a_rail.get())
    dbr = float(dimensions_b_rail.get())
    wok = float(weight_of_one_kilogram.get())
    
    # Создание файла с названием нового провода(словаря)
    file_path = os.path.join('Data', reil_dict_name + '.dat')
    with open(file_path, 'w') as file:
        json.dump(reil_dict_name, file)
        
    # Добавление в созданный файл информации 
    name = {'iso':arc, 'mnt':mn, 'dar':dar, 'dbr':dbr, 'wok':wok}
    with open(file_path, 'w') as file:
        json.dump(name, file)
    
    # Добавление нового провода в listbox(добавление значения в словарь reildict.dat)
    key = reil_dict_name  # Новый ключ для словаря
    value = 1  # Получаем значение ключа из Entry
    reil_dictionary[key] = value  # Добавляем новый ключ и значение в словарь
    with open('Data\\reildict.dat', 'w') as f:  # Сохраняем измененный словарь в файл
        json.dump(reil_dictionary, f)
    
def _reil_destroy(): # ЗАКРЫТИЕ ОКНА ДОБАВЛЕНИЯ СЛОЯ
    add_reil_window.destroy()

def _reil_save_threading(): # СОХРАНЕНИЕ И ВЫХОД ИЗ ОКНВ ДОБАВЛЕНИЯ СЛОЯ
    threading.Thread(target=_reil_destroy).start()
    threading.Thread(target=_reil_save).start()        
    threading.Thread(target=_update_reil_profile_listbox).start()    
        
#___________________________________________________________________ ИЗОЛЯТОР ___________________________________________________________________#

def _update_insulator_listbox():
    # Удаляем все элементы из Listbox
    insulator_listbox.delete(0, END)
    time.sleep(0.2)
    # Добавляем новые элементы из словаря
    for key in insulator_dictionary:
        insulator_listbox.insert(END, key)

def _insulator_save():
    global dict_name
    dict_name = nie.get()
    name = dict_name
    # add_nie = float(nie.get())
    add_hie = float(hie.get())
    add_fce = float(fce.get())
    add_fse = float(fse.get())
    add_bie = float(bie.get())
    add_wokie = float(wokie.get())
    add_tic = tic.get()
    

    # Создание файла с названием нового провода(словаря)
    file_path = os.path.join('Data', dict_name + '.dat')
    with open(file_path, 'w') as file:
        json.dump(dict_name, file)
         
    # Добавление в созданный файл информации 
    name = {'hie':add_hie, 'fce':add_fce, 'fse':add_fse, 'bie':add_bie, 'wokie':add_wokie, 'tic':add_tic}
    with open(file_path, 'w') as file:
        json.dump(name, file)
    
    # Добавление нового провода в listbox(добавление значения в словарь wiredict.dat)
    key = dict_name  # Новый ключ для словаря
    value = 1  # Получаем значение ключа из Entry
    insulator_dictionary[key] = value  # Добавляем новый ключ и значение в словарь
    with open('Data\insdict.dat', 'w') as f:  # Сохраняем измененный словарь в файл
        json.dump(insulator_dictionary, f)

def _insulator_save_window_destroy():
    add_insulator_window.destroy()

def _add_insulator(): 
    global nie, hie, fce, fse, bie, wokie, tic, add_insulator_window
    add_insulator_window = Toplevel(material)
    add_insulator_window.geometry('360x325+1000+150')
    add_insulator_window.title('Добавление изолятора')
    add_insulator_window['bg'] = 'gray82'  
    
    add_name_insulator_label =  Label(add_insulator_window, text='Название', bg=win_bg)
    add_name_insulator_label.place(x=10, y=10)
    nie = Entry(add_insulator_window, text='Высота, мм')
    nie.place(x=230, y=10)

    add_height_insulator_label = Label(add_insulator_window, text='Высота, мм', bg=win_bg)
    add_height_insulator_label.place(x=10, y=40)
    hie = Entry(add_insulator_window, width=20)
    hie.place(x=230, y=40)
    
    add_f_compression_label = Label(add_insulator_window, text='F, сжат, кг', bg=win_bg)
    add_f_compression_label.place(x=10, y=70)
    fce = Entry(add_insulator_window, width=20)
    fce.place(x=230, y=70)
    
    add_f_stretching_label = Label(add_insulator_window, text='F, раст, кг', bg=win_bg)
    add_f_stretching_label.place(x=10, y=100)
    fse = Entry(add_insulator_window, width=20)
    fse.place(x=230, y=100)
    
    add_bending_insulator_label = Label(add_insulator_window, text='F, изгиб, кг', bg=win_bg)
    add_bending_insulator_label.place(x=10, y=130)
    bie = Entry(add_insulator_window, width=20)
    bie.place(x=230, y=130)
    
    add_weight_of_one_kilogram_insulator_label = Label(add_insulator_window, text='Масса ,кг', bg=win_bg)
    add_weight_of_one_kilogram_insulator_label.place(x=10, y=160)
    wokie = Entry(add_insulator_window, width=20)
    wokie.place(x=230, y=160)
    
    add_type_insulator_label = Label(add_insulator_window, text='Тип', bg=win_bg)
    add_type_insulator_label.place(x=10, y=190)
    tic = ttk.Combobox(add_insulator_window, values=['Опорный','Междуфазный'], width=15)
    tic.current(0)
    tic.place(x=230, y=190)
    
    save_insulator_button = Button(add_insulator_window, text='Сохранить', command=_insulator_save_threading)
    save_insulator_button.place(x=10, y=280)

    quit_insulator_button = Button(add_insulator_window, text='Выйти', command=add_insulator_window.destroy)
    quit_insulator_button.place(x=100, y=280)
    
def _insulator_save_threading():
    threading.Thread(target=_insulator_save).start()
    threading.Thread(target=_update_insulator_listbox).start()
    threading.Thread(target=_insulator_save_window_destroy).start()    
 
def _del_insulator():
    # получаем индекс выбранного элемента в listbox
    index = insulator_listbox.curselection()[0]
    # получаем ключ выбранного элемента
    key = insulator_listbox.get(index)
    # удаляем элемент из словаря по ключу
    del insulator_dictionary[key]
    temp_dict = insulator_dictionary
    with open('Data\\insdict.dat', 'w') as file:
        json.dump(temp_dict, file)
    # удаляем элемент из listbox
    insulator_listbox.delete(index)

    # удаление файла из паки
    file_path = os.path.join('Data', key + '.dat') # указываем путь к файлу, который нужно удалить
    # if os.path.exists(file_path): # проверяем, существует ли файл
    os.remove(file_path) # удаляем файл 
    
def _updates_insulator_labels(event):
    global selected_value
    files = os.listdir('Data') # Получаем список файлов в папке
    for i in files:   
        selected_value = insulator_listbox.get(insulator_listbox.curselection()) # Получаем значение выбранное в listbox
        if selected_value in i:# Проверяем, соответствует ли выбранное значение названию файла в папке
            to_change_insulator_button['state'] = 'active' # активация кнопки - ИЗМЕНИТЬ
            # print('Выбранное значение соответствует названию файла в папке')
            with open('Data\\' + selected_value + '.dat', 'r') as f: # если соответствие найдено, открываем файл для чтения, помощью функции `open()` и прочитать его содержимое с помощью метода `read()`
                data = f.read() 
                dict = eval(data) #  Использовать функцию `eval()` для преобразования строки со словарем в объект
                height_insulator_label_value.configure(text=dict['hie'])
                f_compression_label_value.configure(text=dict['fce'])
                f_stretching_label_value.configure(text=dict['fse'])
                bending_insulator_label_value.configure(text=dict['bie'])
                weight_of_one_kilogram_insulator_label_value.configure(text=dict['wokie'])
                type_insulator_label_value.configure(text=dict['tic'])

        else: # если соответствий не найдено, пропускаем
            # print('Выбранное значение не соответствует названию файла в папке')
            pass
    
def _to_change_insulator():
    global to_change_window_insulator, dict_name, change_dict, nie_add, hie_add, fce_add, fse_add, bie_add, wokie_add, tic_add
    to_change_window_insulator = Toplevel(material)
    to_change_window_insulator.geometry('360x325+1000+150')
    to_change_window_insulator.title('Правка значений')
    to_change_window_insulator['bg'] = 'gray82'
    
    ########## СТАНДАРТНЫЕ АТРИБУТЫ ##########
    word_font = 'Arial 10'
    win_bg = 'gray82'
    ####################

    # Название изолятора
    # nie_label = Label(to_change_window_insulator, text='Название', bg=win_bg, font=word_font)
    # nie_label.place(x=10, y=40)
    # nie_add = Entry(to_change_window_insulator, width=20)
    # nie_add.place(x=230, y=40)
    # Высота изолятора
    hie_label = Label(to_change_window_insulator, text='Высота, мм', bg=win_bg, font=word_font)
    hie_label.place(x=10, y=40)
    hie_add = Entry(to_change_window_insulator, width=20)
    hie_add.place(x=230, y=40)
    # F, сжат, кг
    fce_label = Label(to_change_window_insulator, text='F, сжат, кг', bg=win_bg, font=word_font)
    fce_label.place(x=10, y=70)
    fce_add = Entry(to_change_window_insulator, width=20)
    fce_add.place(x=230, y=70)
    # F, раст, кг
    fse_label = Label(to_change_window_insulator, text='F, раст, кг', bg=win_bg, font=word_font)
    fse_label.place(x=10, y=100)
    fse_add = Entry(to_change_window_insulator, width=20)
    fse_add.place(x=230, y=100)
    # F, изгиб, кг
    bie_label = Label(to_change_window_insulator, text='F, изгиб, кг', bg=win_bg, font=word_font)
    bie_label.place(x=10, y=130)
    bie_add = Entry(to_change_window_insulator, width=20)
    bie_add.place(x=230, y=130)
    # Масса ,кг
    wokie_label = Label(to_change_window_insulator, text='Масса ,кг', bg=win_bg, font=word_font)
    wokie_label.place(x=10, y=160)
    wokie_add = Entry(to_change_window_insulator, width=20)
    wokie_add.place(x=230, y=160)
    # Тип
    tic_label = Label(to_change_window_insulator, text='Тип', bg=win_bg, font=word_font)
    tic_label.place(x=10, y=190)
    tic_add = ttk.Combobox(to_change_window_insulator, values=['Опорный','Междуфазный'], width=18)
    tic_add.current(0)
    tic_add.place(x=230, y=190)

  
    if selected_value in i:# Проверяем, соответствует ли выбранное значение названию файла в папке
        to_change_button['state'] = 'active' # активация кнопки - ИЗМЕНИТЬ
    with open('Data\\' + selected_value + '.dat', 'r') as f: # открываем файл для чтения, помощью функции `open()` и прочитать его содержимое с помощью метода `read()`
        data = f.read() 
        change_dict = eval(data) #  Использовать функцию `eval()` для преобразования строки со словарем в объект

        hie_add.insert(END, change_dict['hie'])
        fce_add.insert(END, change_dict['fce'])
        fse_add.insert(END, change_dict['fse'])
        bie_add.insert(END, change_dict['bie'])
        wokie_add.insert(END, change_dict['wokie'])
        # tic_add.insert(END, change_dict['tic'])


    # Кнопка - Сохранить
    save_add_isolator_button = Button(to_change_window_insulator, text='Сохранить', command=_save_change_insulator_threading)
    save_add_isolator_button.place(x=10, y=280)
    # Кнопка - Выйти 
    quit_wire_isolator_button = Button(to_change_window_insulator, text='Выйти', command=_save_save_change_insulator_destroy)
    quit_wire_isolator_button.place(x=100, y=280)         
    
def _save_change_insulator():
    global hie_add, fce_add, fse_add, bie_add, wokie_add, tic_add
    name = change_dict
    hie = float(hie_add.get())
    fce = float(fce_add.get())
    fse = float(fse_add.get())
    bie = float(bie_add.get())
    wokie = float(wokie_add.get())
    tic = tic_add.get()
    # Добавление в созданный файл информации 
    name = {'hie':hie, 'fce':fce, 'fse':fse, 'bie':bie, 'wokie':wokie, 'tic':tic}
    with open('Data\\' + selected_value + '.dat', 'w') as file:
        json.dump(name, file)        

def _save_save_change_insulator_destroy():
    to_change_window_insulator.destroy()
               
def _save_change_insulator_threading():
    threading.Thread(target=_save_change_insulator).start()
    threading.Thread(target=_save_save_change_insulator_destroy).start()        
        
           
material = Tk()
material.geometry('500x370+500+150')
material['bg'] = 'gray82'
material.title('Выбор метериала')
material.iconbitmap(default='ico\material_favicon.ico')
########## СТАНДАРТНЫЕ АТРИБУТЫ ##########
word_font = 'Arial 10'
win_bg = 'gray82'
####################

########## СЛОВАРИ  СОКРАЩЕНИЯ ##########
# [bwd] bare wire diameter - диаметр провода без изоляции 
# [its] insulation thickness on two sides - толщина изоляции на две стороны 
# [stn] section - сечение 
# [wom] weight of one meter - масса одного метра 
# [mtl] material - материал 
# [wsp] wire shape - Форма провода 
# [dwi] dimensions with insulation - размеры с изоляцией 

# [mat] material - материл
# [dar] dimensions a rail - размеры рейки А
# [dbr] dimensions b rail - размеры рейки B
# [wok] weight_of_one_kilogram - масса 1 кг

# [nie] name_insulator - Название
# [hie] height_insulator - Высота, мм
# [fce] f_compression - F, сжат, кг
# [fse] f_stretching - F, раст, кг
# [bie] bending_insulator - 'F, изгиб, кг
# [wokie] weight_of_one_kilogram_insulator - масса изолятора
# [tic] type_insulator - тип изолятора


#############################

# Создание темы для названия вкладок
style = Style()
style.theme_use('default')
style.configure('TNotebook.Tab', background='white') # цвет фона названия вкладок ( Notebook )
style.configure('TFrame', background='gray82') # цвет фона вкладок ( Frame )
style.configure('Tab', focuscolor=style.configure('.')['background']) # убирает пунктирную линию вокруг названия
style.map('TNotebook', background= [('selected', 'white')])
style.theme_settings('default', {'TNotebook.Tab': {'configure': {'padding': [10, 5]}}}) # высота и ширина вкладок

# Создание Notebook виджета
tab_control = ttk.Notebook(material, width=250, height=250)
wire = ttk.Frame(tab_control)
isolation = ttk.Frame(tab_control)
insulator = ttk.Frame(tab_control)
tab_control.add(wire, text='Провод')
tab_control.add(isolation, text='Изоляция')
tab_control.add(insulator, text='Изолятор')
tab_control.pack(expand=1, fill='both')




#___________________________________________________________________ ВКЛАДКА ПРОВОД ___________________________________________________________________#
# Открытие wiredict.dat для чтения
with open('Data\wiredict.dat', 'r') as file:
    wire_dictionary = json.load(file)

wire_brand_label = Label(wire, text='Марка', font='Arial 14', bg=win_bg)
wire_brand_label.place(x=10, y=10)

# listbox с выбором типа провода
wire_brand_listbox = Listbox(wire, width=20, height=15)
wire_brand_listbox.place(x=10, y=50)
for i in wire_dictionary:
    wire_brand_listbox.insert(END, i)

########## ПАРАМЕТРЫ ##########
wire_parameters_label = Label(wire, text='Параметры', font='Arial 14', bg=win_bg)
wire_parameters_label.place(x=140, y=10)

# Frame подложка
wire_parameters_frame = Frame(wire, width=350, height=244, highlightbackground='black', highlightthickness=1)
wire_parameters_frame.place(x=140, y=50)

########### Labels со значением парпметров провода
# Диаметр голого провода
bwd_label = Label(wire_parameters_frame, text='Диаметр провода без изоляции, мм')
bwd_label.place(x=0, y=10)
bwd_label_a_value = Label(wire_parameters_frame, width=6, text='', relief=SOLID)
bwd_label_a_value.place(x=230, y=10)
bwd_label_b_value = Label(wire_parameters_frame, width=6, text='', relief=SOLID)
bwd_label_b_value.place(x=292, y=10)

# Толщина изоляции на две стороны
its_label = Label(wire_parameters_frame, text='Толщина изоляции на две стороны, мм')
its_label.place(x=0, y=40)
its_label_value = Label(wire_parameters_frame, width=15, text='', relief=SOLID)
its_label_value.place(x=230, y=40)

# Cечение
stn_label = Label(wire_parameters_frame, text='Сечение, мм^2')
stn_label.place(x=0, y=70)
stn_label_value = Label(wire_parameters_frame, width=15, text='', relief=SOLID)
stn_label_value.place(x=230, y=70)

# Масса одного метра
wom_label = Label(wire_parameters_frame, text='Масса одного метра, кг')
wom_label.place(x=0, y=100)
wom_label_value = Label(wire_parameters_frame, width=15, text='', relief=SOLID)
wom_label_value.place(x=230, y=100)

# Материал
mtl_label = Label(wire_parameters_frame, text='Материал')
mtl_label.place(x=0, y=130)
mtl_label_value = Label(wire_parameters_frame, width=15, text='', relief=SOLID)
mtl_label_value.place(x=230, y=130)

# Форма провода [wsp]
wsp_label = Label(wire_parameters_frame, text='Форма провода')
wsp_label.place(x=0, y=160)
wsp_label_value = Label(wire_parameters_frame, width=15, text='', relief=SOLID)
wsp_label_value.place(x=230, y=160)

# Размеры с изоляцией [dwi]
dwi_label = Label(wire_parameters_frame, text='Размеры с изоляцией')
dwi_label.place(x=0, y=190)
dwi_label_a_value = Label(wire_parameters_frame, width=6, text='', relief=SOLID)
dwi_label_a_value.place(x=230, y=190)
dwi_label_b_value = Label(wire_parameters_frame, width=6, text='', relief=SOLID)
dwi_label_b_value.place(x=292, y=190)

# Кнопка - Добавить провод
add_wire_button = Button(wire, text='Добавить', command=_add_wire)
add_wire_button.place(x=10, y=300)

# Кнопка - Удалить провод
del_wire_button = Button(wire, text='Удалить', command=_del_wire)
del_wire_button.place(x=80, y=300)

# Кнопка - Редактировать провод
to_change_button = Button(wire, text='Редактировать', state='disabled', command=_to_change)
to_change_button.place(x=400, y=300)

wire_brand_listbox.bind("<<ListboxSelect>>", updates_wire_parameters_labels) # Обновление функции updates_wire_parameters_label [ значений при выборе listbox ]


#___________________________________________________________________ ВКЛАДКА ИЗОЛЯЦИЯ ___________________________________________________________________#
# Открытие rackdict.dat для чтения
with open('Data\\reildict.dat', 'r') as file:
    reil_dictionary = json.load(file)
    
reil_profile_label = Label(isolation, text='Профиль', font='Arial 14', bg=win_bg)
reil_profile_label.place(x=10, y=10)

# listbox с выбором типа рейки
reil_profile_listbox = Listbox(isolation,  width=20, height=15)
reil_profile_listbox.place(x=10, y=50)
for i in reil_dictionary:
    reil_profile_listbox.insert(END, i)

# Кнопка - Добавить рейку
add_reil_button = Button(isolation, text='Добавить', command=_add_rack)
add_reil_button.place(x=10, y=300)

# Кнопка - Удалить рейку
del_reil_button = Button(isolation, text='Удалить', command=_del_rack)
del_reil_button.place(x=80, y=300)

########## ПАРАМЕТРЫ ##########
reil_parameters_label = Label(isolation, text='Параметры', font='Arial 14', bg=win_bg)
reil_parameters_label.place(x=140, y=10)

# Frame подложка
reil_parameters_frame = Frame(isolation, width=350, height=244, highlightbackground='black', highlightthickness=1)
reil_parameters_frame.place(x=140, y=50)

########### Labels со значением парпметров изоляции
material_label = Label(reil_parameters_frame, text='Материал', font=word_font)
material_label.place(x=0, y=10)
material_label_value = Label(reil_parameters_frame, width=15, relief=SOLID)
material_label_value.place(x=230, y=10)

dimensions_a_rail_lab = Label(reil_parameters_frame, text='Размеры рейки А', font=word_font)
dimensions_a_rail_lab.place(x=0, y=40)
dimensions_a_rail_lab_value = Label(reil_parameters_frame, width=15, relief=SOLID)
dimensions_a_rail_lab_value.place(x=230, y=40)

dimensions_b_rail_lab = Label(reil_parameters_frame, text='Размеры рейки B', font=word_font)
dimensions_b_rail_lab.place(x=0, y=70)
dimensions_b_rail_lab_value = Label(reil_parameters_frame, width=15, relief=SOLID)
dimensions_b_rail_lab_value.place(x=230, y=70)

weight_of_one_kilogram_lab = Label(reil_parameters_frame, text='Масса ,кг', font=word_font)
weight_of_one_kilogram_lab.place(x=0, y=100)
weight_of_one_kilogram_lab_value = Label(reil_parameters_frame, width=15, relief=SOLID)
weight_of_one_kilogram_lab_value.place(x=230, y=100)

reil_profile_listbox.bind("<<ListboxSelect>>", _updates_reil_profile_labels) # Обновление функции updates_wire_parameters_label [ значений при выборе listbox ]


#___________________________________________________________________ ВКЛАДКА ИЗОЛЯТОР ___________________________________________________________________#
# Открытие insdict.dat для чтения
with open('Data\\insdict.dat', 'r') as file:
    insulator_dictionary = json.load(file)

insulator_profile_label = Label(insulator, text='Тип', font='Arial 14', bg=win_bg)    
insulator_profile_label.place(x=10, y=10)    

insulator_listbox = Listbox(insulator, width=20, height=15)
insulator_listbox.place(x=10, y=50)    
for i in insulator_dictionary:
    insulator_listbox.insert(END, i)

# Кнопка - Добавить изолятор
add_insulator_button = Button(insulator, text='Добавить', command=_add_insulator)
add_insulator_button.place(x=10, y=300)

# Кнопка - Удалить изолятор
del_insulator_button = Button(insulator, text='Удалить', command=_del_insulator)
del_insulator_button.place(x=80, y=300)    

# Кнопка - Редактировать изолятор    
to_change_insulator_button = Button(insulator, text='Редактировать', state='disabled', command=_to_change_insulator)
to_change_insulator_button.place(x=400, y=300)

########## ПАРАМЕТРЫ ##########
insulator_parameters_label = Label(insulator, text='Параметры', font='Arial 14', bg=win_bg)
insulator_parameters_label.place(x=140, y=10)
# Frame подложка
insulator_parametr_frame = Frame(insulator, width=350, height=244, highlightbackground='black', highlightthickness=1)
insulator_parametr_frame.place(x=140, y=50)

########### Labels со значением парпметров изолятора
height_insulator_label = Label(insulator_parametr_frame, text='Высота, мм', font=word_font)
height_insulator_label.place(x=0, y=10)
height_insulator_label_value = Label(insulator_parametr_frame, width=15, relief=SOLID)
height_insulator_label_value.place(x=230, y=10)

f_compression_label = Label(insulator_parametr_frame, text='F, сжат, кг', font=word_font)
f_compression_label.place(x=0, y=40)
f_compression_label_value = Label(insulator_parametr_frame, width=15, relief=SOLID)
f_compression_label_value.place(x=230, y=40)

f_stretching_label = Label(insulator_parametr_frame, text='F, раст, кг', font=word_font)
f_stretching_label.place(x=0, y=70)
f_stretching_label_value = Label(insulator_parametr_frame, width=15, relief=SOLID)
f_stretching_label_value.place(x=230, y=70)

bending_insulator_label = Label(insulator_parametr_frame, text='F, изгиб, кг', font=word_font)
bending_insulator_label.place(x=0, y=100)
bending_insulator_label_value = Label(insulator_parametr_frame, width=15, relief=SOLID)
bending_insulator_label_value.place(x=230, y=100)

weight_of_one_kilogram_insulator_label = Label(insulator_parametr_frame, text='Масса ,кг', font=word_font)
weight_of_one_kilogram_insulator_label.place(x=0, y=130)
weight_of_one_kilogram_insulator_label_value = Label(insulator_parametr_frame, width=15, relief=SOLID)
weight_of_one_kilogram_insulator_label_value.place(x=230, y=130)

type_insulator_label = Label(insulator_parametr_frame, text='Тип', font=word_font)
type_insulator_label.place(x=0, y=160)
type_insulator_label_value = Label(insulator_parametr_frame, width=15, relief=SOLID)
type_insulator_label_value.place(x=230, y=160)

insulator_listbox.bind("<<ListboxSelect>>", _updates_insulator_labels) # Обновление функции updates_insulator_parameters_label [ значений при выборе listbox ]

material.mainloop()