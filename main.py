from tkinter import *
from tkinter import ttk
from tkinter.ttk import Style
from tkinter import messagebox
import tkinter as tk
import threading
import json
import subprocess
import os

# НЕ УДАЛЯТЬ!!!! ЖИЗНЕННО ВАЖНЕ СПИСКИ!!!!
winding_height_tab_list = [] # список label Высота намотки в таблице для высота расчетов
active_resistance_tab_list = [] # список label Активное сопротивление в таблице для высота расчетов
tab_frame = [] # список всех frame в таблице для смены цвета фона в уже созданной таблице, при смене цветовой темы
lab_frame = [] # список всех label в таблице для смены цвета фона в уже созданной таблице, при смене цветовой темы

def _clear_table(): # Очистка таблицы
    global winding_height_tab_list
    ########## Работа с элементами меню - Таблица (подменю) ##########
    tablemenu.entryconfig(0, state='active') # включение подменю - Создать
    tablemenu.entryconfig(1, state='disabled') # включение подменю - Очистить
    tablemenu.entryconfig(3, state='disabled') # включение подменю - Расчитать
    
    ########## Очистка таблицы ##########
    for widget in table_of_layers_and_insulations_frame.winfo_children():
        widget.destroy()
    table_of_layers_and_insulations_frame.configure(height=970)
    winding_height_tab_list = [] # обновляем список после очистки интерфейса ( без этого после очистки интерфейса не будет показывать значение расчетов высоты намотки в таблице )
    active_resistance_tab_list = [] # обновляем список после очистки интерфейса ( без этого после очистки интерфейса не будет показывать значение расчетов высоты намотки в таблице )
    
    ########## Очистка значений после расчетов ##########
    winding_height_calculation.configure(text='') # Высота намотки в мм
    outer_diameter_of_the_coil_calculation.configure(text='') # Внешний диаметр катушки
    
def _create_table(): # Создание таблицы
    global mother_frame, main_frame, parallels_entry_list, thickness_entry_list,number_of_turns_entry_list, wire_type_combo, winding_height_value_label, wire_type_list
    global type_of_insulation_list, winding_height_tab_list, tab_value, get_value
    
    line_canvas.destroy() # уничтожение элементов пустого пространства таблицы
    
    ########## Работа с элементами меню - Таблица (подменю) ##########
    tablemenu.entryconfig(0, state='disabled') # отключение подменю - Создать
    tablemenu.entryconfig(1, state='active') # включение подменю - Очистить
    tablemenu.entryconfig(3, state='active') # включение подменю - Расчитать
    
    get_value = number_of_layers_entry.get()
    
    parallels_entry_list = [] # список кол-ва параллелей 
    thickness_entry_list = []
    number_of_turns_entry_list = [] # список кол-ва витков слоя
    wire_type_list = [] # ТИП ПРОВОДА
    type_of_insulation_list = [] # ТИП ИЗОЛЯЦИИ
    
     
    # Создаем главный frame
    main_frame = tk.Frame(table_of_layers_and_insulations_frame)
    main_frame.pack(fill=tk.BOTH, expand=1)
    
    # Создаем canvas и scrollbar
    canvas = tk.Canvas(main_frame, width=1520, height=963, bg=win_bg)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
    scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Устанавливаем scrollbar на canvas
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    
    # Создаем frame с entry
    work_frame = tk.Frame(canvas)

    try:
        for tab_value in range(int(get_value)):
            mother_frame = Frame(work_frame, width=1520, height=100, highlightbackground='black', highlightthickness=1, bg=win_bg)
            mother_frame.pack()
            tab_frame.append(mother_frame)
            # ФРЕЙМ - СЛОЙ 1
            layer_frame = Frame(mother_frame, width=100, height=50, highlightbackground='black', highlightthickness=1, bg=win_bg)
            layer_frame.place(x=0, y=0)
            tab_frame.append(layer_frame)
            layer_label = Label(layer_frame, text=('СЛОЙ', int(tab_value+1)), bg=win_bg, fg=tab_fg)
            layer_label.place(x=25, y=15)
            lab_frame.append(layer_label)
            # ФРЕЙМ - ИЗОЛЯЦИЯ 1
            isolation_frame = Frame(mother_frame, width=100, height=48, highlightbackground='black', highlightthickness=1, bg=win_bg)
            isolation_frame.place(x=0, y=50)
            tab_frame.append(isolation_frame)
            isolation_label = Label(isolation_frame, text='ИЗОЛЯЦИЯ', bg=win_bg, fg=tab_fg)
            isolation_label.place(x=10, y=15)
            lab_frame.append(isolation_label)
            # ФРЕЙМ - ТИП ПРОВОДА
            wire_type_frame = Frame(mother_frame, width=150, height=50, highlightbackground='black', highlightthickness=1, bg=win_bg)
            wire_type_frame.place(x=100, y=0)
            tab_frame.append(wire_type_frame)
            wire_type_label = Label(wire_type_frame, width=12, height=1, text='Тип провода', bg=win_bg, fg=tab_fg)
            wire_type_label.place(x=30, y=0)
            lab_frame.append(wire_type_label)
            with open('Data\wiredict.dat', 'r') as f:
                wire_dictionary = json.load(f)
                wire_type_combo = ttk.Combobox(wire_type_frame, width=15, values=list(wire_dictionary))
                wire_type_combo.place(x=18, y=25)
                wire_type_list.append(wire_type_combo)
                # wire_type_combo.bind("<<ComboboxSelected>>", lambda event, combo=wire_type_combo: wire_type_list.append(combo.get()))  
            # ФРЕЙМ - ТИП ИЗОЛЯЦИИ
            type_of_insulation_frame = Frame(mother_frame, width=150, height=48, highlightbackground='black', highlightthickness=1, bg=win_bg)
            type_of_insulation_frame.place(x=100, y=50)
            tab_frame.append(type_of_insulation_frame)
            type_of_insulation_label = Label(type_of_insulation_frame, width=12, height=1, text='Тип изоляции', bg=win_bg, fg=tab_fg)
            type_of_insulation_label.place(x=30, y=0)
            lab_frame.append(type_of_insulation_label)
            # ФРЕЙМ - ВЫБОР ИЗОЛЯЦИИ
            with open('Data\\reildict.dat', 'r') as f:
                rack_dictionary = json.load(f)
                type_of_insulation_combo = ttk.Combobox(type_of_insulation_frame, width=15, values=list(rack_dictionary))
                type_of_insulation_combo.place(x=18, y=23)
                type_of_insulation_list.append(type_of_insulation_combo)
                # type_of_insulation_combo.bind("<<ComboboxSelected>>", lambda event, combo=type_of_insulation_combo: type_of_insulation_list.append(combo.get()))
            # ФРЕЙМ - КОЛИЧЕСТВО ПАРАЛЛЕЛЕЙ LABEL
            parallels_frame = Frame(mother_frame, width=150, height=50, highlightbackground='black', highlightthickness=1, bg=win_bg)
            parallels_frame.place(x=250, y=0)
            tab_frame.append(parallels_frame)
            parallels_label = Label(parallels_frame, width=18, height=1, text='Кол-во параллелей', bg=win_bg, fg=tab_fg)
            parallels_label.place(x=10, y=0)
            lab_frame.append(parallels_label)
            # КОЛИЧЕСТВО ПАРАЛЛЕЛЕЙ ENTRY
            parallels_entry = Entry(parallels_frame,width=20)
            parallels_entry.place(x=12, y=25)
            parallels_entry_list.append(parallels_entry)
            # ФРЕЙМ - ТОЛЩИНА
            thickness_frame = Frame(mother_frame, width=150, height=48, highlightbackground='black', highlightthickness=1, bg=win_bg)
            thickness_frame.place(x=250, y=50)
            tab_frame.append(thickness_frame)
            thickness_label = Label(thickness_frame, width=18, height=1, text='Толщина, мм', bg=win_bg, fg=tab_fg)
            thickness_label.place(x=5, y=0)
            lab_frame.append(thickness_label)
            # ТОЛЩИНА ENTRY
            thickness_entry = Entry(thickness_frame, width=20)
            thickness_entry.place(x=12, y=23)
            thickness_entry_list.append(thickness_entry)
            # КОЛИЧЕСТВО ВИТКОВ    
            number_of_turns_frame = Frame(mother_frame, width=110, height=99, highlightbackground='black', highlightthickness=1, bg=win_bg)
            number_of_turns_frame.place(x=400, y=0)
            tab_frame.append(number_of_turns_frame)
            number_of_turns_label = Label(number_of_turns_frame, width=13, height=1, text='Кол-во витков', bg=win_bg, fg=tab_fg)
            number_of_turns_label.place(x=0, y=0)
            lab_frame.append(number_of_turns_label) 
            # КОЛИЧЕСТВО ВИТКОВ ENTRY
            number_of_turns_entry = Entry(number_of_turns_frame, width=15) 
            number_of_turns_entry.place(x=5, y=25)
            number_of_turns_entry_list.append(number_of_turns_entry)
            # ФРЕЙМ - Высота намотки, мм/ расстояние между проводами, мм   
            winding_height_frame = Frame(mother_frame, width=140, height=99, highlightbackground='black', highlightthickness=1, bg=win_bg)
            winding_height_frame.place(x=510, y=0)
            tab_frame.append(winding_height_frame)
            winding_height_label = Label(winding_height_frame, text='Высота намотки, мм', bg=win_bg, fg=tab_fg)
            winding_height_label.place(x=10, y=0)
            lab_frame.append(winding_height_label)
            winding_height_value_label = Label(winding_height_frame, width=15, bg='white', relief=SOLID)
            winding_height_value_label.place(x=15, y=23)
            winding_height_tab_list.append(winding_height_value_label)
            # ФРЕЙМ - Ток слоя, А
            layer_current_frame = Frame(mother_frame, width=140, height=99, highlightbackground='black', highlightthickness=1, bg=win_bg)
            layer_current_frame.place(x=650, y=0)
            tab_frame.append(layer_current_frame)
            layer_current = Label(layer_current_frame, text='Ток слоя ,А', bg=win_bg, fg=tab_fg)
            layer_current.place(x=40, y=0)
            lab_frame.append(layer_current)
            layer_current_value_label = Label(layer_current_frame, width=15, bg='white', relief=SOLID)
            layer_current_value_label.place(x=15, y=23)
            # ФРЕЙМ - Плотность тока, А/мм2
            current_density_frame = Frame(mother_frame, width=160, height=99, highlightbackground='black', highlightthickness=1, bg=win_bg)
            current_density_frame.place(x=790, y=0)
            tab_frame.append(current_density_frame)
            current_density_label = Label(current_density_frame, text='Плотность тока, А/мм2', bg=win_bg, fg=tab_fg)
            current_density_label.place(x=10, y=0)
            lab_frame.append(current_density_label)
            current_density_value = Label(current_density_frame, width=15, bg='white', relief=SOLID)
            current_density_value.place(x=25, y=23)
            # ФРЕЙМ - Активное сопротивление, Ом
            active_resistance_frame = Frame(mother_frame, width=200, height=99, highlightbackground='black', highlightthickness=1, bg=win_bg)
            active_resistance_frame.place(x=950, y=0)
            tab_frame.append(active_resistance_frame)
            active_resistance_label = Label(active_resistance_frame, text='Активное сопротивление, Ом', bg=win_bg, fg=tab_fg)
            active_resistance_label.place(x=10, y=0)
            lab_frame.append(active_resistance_label)
            active_resistance_value = Label(active_resistance_frame, width=15, bg='white', relief=SOLID)
            active_resistance_value.place(x=45, y=23)  
            active_resistance_tab_list.append(active_resistance_value) 
            # ФРЕЙМ - Индуктивное сопротивление, Ом 
            inductive_resistance_frame = Frame(mother_frame, width=200, height=99, highlightbackground='black', highlightthickness=1, bg=win_bg)
            inductive_resistance_frame.place(x=1150, y=0)
            tab_frame.append(inductive_resistance_frame)        
            inductive_resistance_label = Label(inductive_resistance_frame, text='Индуктивное сопротивление', bg=win_bg, fg=tab_fg)
            inductive_resistance_label.place(x=10, y=0)
            lab_frame.append(inductive_resistance_label)
            inductive_resistance_value_label = Label(inductive_resistance_frame, width=15, bg='white', relief=SOLID)
            inductive_resistance_value_label.place(x=45, y=23)
            # ФРЕЙМ - Полное сопротивление, Ом
            total_resistance_frame = Frame(mother_frame, width=168, height=99, highlightbackground='black', highlightthickness=1, bg=win_bg)
            total_resistance_frame.place(x=1350, y=0)
            tab_frame.append(total_resistance_frame) 
            total_resistance_label = Label(total_resistance_frame, text='Полное сопротивление, Ом', bg=win_bg, fg=tab_fg)
            total_resistance_label.place(x=0, y=0)
            lab_frame.append(total_resistance_label)
            total_resistance_value_label = Label(total_resistance_frame, width=15, bg='white', relief=SOLID)
            total_resistance_value_label.place(x=30, y=23)
            
    except:
        messagebox.showerror('Ошибка ввода','Вводимое значение "Количество слоев" должно быть целым числом.')
        _clear_table() 
    # Устанавливаем frame с entry на canvas
    canvas.create_window((0, 0), window=work_frame, anchor='nw')

def _math_table(): # Расчет таблицы
    # получение данных из entry
    Ct = coil_type_combo.get() # Тип катушки
    Cu = climatic_use_combo.get() # Климатическое использование
    Un = rated_voltage_entry.get() # Номинальное напряжение
    In = rated_current_entry.get() # Номинальный ток
    Km = rated_resistance_entry.get() # Номинальное сопротивление
    Hz = network_frequency_entry.get() # Частота сети
    Nol = number_of_layers_entry.get() # Кол-во слоев
    Id = inner_diameter_entry.get() # Внутренний диаметр
    Nor = number_of_rays_entry.get() # Число лучей звезды
    Noi = number_of_insulators_entyry.get() # Число изоляторов
    Toi = type_of_insulators_combo.get() # Тип изолятора
    layer_value = number_of_layers_entry.get() # Кол-во слоев в таблице
    
    global winding_height_value_label
    # получение значений из кол-во параллелей (таблица)
    parallels_values = []
    for parallels_entry in parallels_entry_list:
        parallels_value = parallels_entry.get()
        parallels_values.append(parallels_value)
    # print('Кол-во параллелей: ')
    # print(parallels_values)

    # получение значений из толщина, мм (таблица)
    thickness_values = []
    for thickness_entry in thickness_entry_list:
        thickness_value = thickness_entry.get()
        thickness_values.append(thickness_value)
    # print('Толщина ,мм: ')    
    # print(thickness_values)
    
    # получение значений из кол-во витков (таблица)
    number_of_turns_values = []
    for number_of_turns_entry in number_of_turns_entry_list:
        number_of_turns_value = number_of_turns_entry.get()
        number_of_turns_values.append(number_of_turns_value)
    # print('Кол-во витков: ')
    # print(number_of_turns_values)
    
    # получение значений из кол-во параллелей (таблица)( parallels_entry_list )
    parallels_entry_values = []
    for parallels_entry in parallels_entry_list:
        parallels_entry_value = parallels_entry.get()
        parallels_entry_values.append(parallels_entry_value)
    
    # Получение выбранного значения в ТИП ПРОВДА(таблица)
    wire_type_tab_values = [] # список значений
    for wire_type_combo in wire_type_list:
        wire_type_value = wire_type_combo.get()
        wire_type_tab_values.append(wire_type_value)
    # print(wire_type_tab_values)
    
    # Получение значений bwd_a и bwd_b из файлов
    dwi_a_list = [] # список для хранения значений dwi_a
    dwi_b_list = [] # список для хранения значений dwi_b
    mtl_list = [] # список для хранения значений mtl ( материал )
    stn_list = [] # список для зранения значений сечения провода
    folder_path = 'Data' # путь к папке с файлами
    files = os.listdir(folder_path) # получаем список файлов в папке
    for dwi in wire_type_tab_values: # проходим по списку значений
        if f'{dwi}.dat' in files: # проверяем, есть ли файл с таким названием в папке
            with open(os.path.join(folder_path, f'{dwi}.dat'), 'r') as f: # если файл существует, открываем его и извлекаем данные
                data = f.read()
                dict_a = eval(data) # использовать функцию `eval()` для преобразования строки со словарем в объект
                dict_b = eval(data) # использовать функцию `eval()` для преобразования строки со словарем в объект
                dict_c = eval(data) # использовать функцию `eval()` для преобразования строки со словарем в объект
                dict_d = eval(data) # использовать функцию `eval()` для преобразования строки со словарем в объект
                dwi_a_list.append(dict_a['dwi_a']) # добавляем значение ключа 'dwi_a' в список
                dwi_b_list.append(dict_b['dwi_b']) # добавляем значение ключа 'dwi_b' в список
                mtl_list.append(dict_c['mtl']) # добавляем значение ключа 'mtl' в список (материал - mtl)
                stn_list.append(dict_d['stn']) # добавляем значение ключа 'stn' в список
    # print(mtl_list)
    # print(dict_a)            
    # print(dwi_a_list)
    # print(dwi_b_list)
    # Получение значений материала из выбранного ТИП ПРОВОДА(таблица)
    

    
    # Получение выбранного значения в ТИП ИЗОЛЯЦИИ(таблица)    
    type_of_insulation_tab_values = []
    for type_of_insulation_combo in type_of_insulation_list:
        type_of_insulation_value = type_of_insulation_combo.get()
        type_of_insulation_tab_values.append(type_of_insulation_value)
        
    # получение значений dar из файла
    '''
    Код нужен для автоматического вставления ключа 'dar' файлов изоляции(файлы содержат структура словаря), создании таблиц.
    '''
    dar_list = []
    folder_path = 'Data' # путь к папке с файлами
    files = os.listdir(folder_path) # получаем список файлов в папке
    for dar in type_of_insulation_tab_values: # проходим по списку значений
         if f'{dar}.dat' in files: # проверяем, есть ли файл с таким названием в папке
            with open(os.path.join(folder_path, f'{dar}.dat'), 'r') as f: # если файл существует, открываем его и извлекаем данные
                data_dar = f.read()
                dict_dar = eval(data_dar) # использовать функцию `eval()` для преобразования строки со словарем в объект
                dar_list.append(dict_dar['dar']) # добавляем значение ключа 'dar' в список





    #############################################################  Р А С Ч Е Т Ы  #############################################################  
          
          
          
    ########## РАСЧЕТЫ ВЫСОТЫ НАМОТКИ В ТАБЛИЦЕ  ##########
    # Конвертация значений number_of_turns_values из str в float
    number_of_turns_float = list(map(float, number_of_turns_values))

    # объединяем элементы функцией zip  ((dwi * parallels_values) * (number_of_turns_float + 1))
    winding_height = []     
    for wh_i, wh_j, wh_k in zip(dwi_a_list, parallels_values, number_of_turns_float):
        winding_height.append(float(wh_i) * float(wh_j) * (float(wh_k)+1))
    # print(number_of_turns_values)
    
    # Конвертация значений списка winding_height из float в str  
    winding_height_str = list(map(str, winding_height))  
 
    # вывод в winding_height_value_label результатов расчетов высоты намотки для каждого слоя ( оба способа рабочие )
    # for wh, tab_value in enumerate(winding_height):
    #     winding_height_tab_list[wh].config(text=tab_value)

    get_value_int = list(map(int, get_value)) # кол-во слоев не можт быть не целым
    for wh in range(get_value_int[0]): # получаем кол-во слоев 
        winding_height_tab_list[wh].configure(text=winding_height_str[wh])
      
    # Расчет максимальной высоты намотки в таблице     
    max_nember_in_winding_height = max(winding_height)
    #######################################################
    
    ########## РАСЧЕТ ТОЛЩИНЫ КАТУШКИ ( Coil thickness ) ( Ct ) ##########
    coil_thickness_list = [] # 
    for ct_i, ct_j in zip(dwi_a_list, dwi_b_list):
        coil_thickness_list.append(float(ct_i) + float(ct_j))
        
    # Ct = coil_thickness_list = [] + thickness_values = [] # сложить все значения этих двух списков
    total_coil = sum(coil_thickness_list) # подсчет суммы всех значений в списке coil_thickness_list
    thickness_values_float = list(map(float, thickness_values)) # конвертация str значений списка в int
    total_thickness = sum(thickness_values_float) # подсчет суммы всех значений в списке thickness_values_int ( thickness_values )
    Ct = total_coil + total_thickness # суммирование значений двух списков
    


    ########## РАСЧЕТ ВНЕШНЕГО ДИАМЕТРА КАТУШКИ ( Outer diameter of the coil ) ( Odc ) ##########
    try:
        Odc = float(Id) + (2 * float(Ct))
    except ValueError:
        messagebox.showerror('Ошибка ввода','Вводимое значение "Внутренний диаметр" должно быть числом.')
    # print(Odc)
    
    
    
    ########## РАСЧЕТ АТИВНОГО СОПРОТИВЛЕНИЯ ОБМОТКИ ( Active resistance of the winding ) ( R_act ) ##########
    active_resistance = [] # список для результатов расчетов Активного сопротивления(Добавлять расчеты в этот список), для присвоения этих значений в таблицу
    
    # Получение значения p_mat в зависимости от выбранного материала в слое
    mtl_value = [] # список числовых значений материалов     # 'Медь' == 0.018   # 'Алюминий' == 0.027
    copper_value = 0.018  # 'Медь'
    aluminum_value = 0.027  # 'Алюминий'
    for mtl in mtl_list:
        if mtl == 'Медь':
            mtl_value.append(copper_value)
        else:
            mtl_value.append(aluminum_value)
    # print(mtl_value)
    # print(mtl_list)
      
    # print('dwi_a:      ', dwi_a_list)
    # print('dar:        ', dar_list)
          
    '''РАСЧЕТЫ D'''
    # Расчет D_внутр_сл[n]:
    n = layer_value
    D_vnytr_n = []
    D_vnytr_sl_1 = float(Id)
    D_vnytr_n.append(D_vnytr_sl_1)
    D_prev = D_vnytr_sl_1

    for i in range(int(n)):
        D_vnytr_sl_n = float(D_prev) + (2 * float(dwi_a_list[i])) + (2 * float(dar_list[i]))
        D_prev = D_vnytr_sl_n
        D_vnytr_n.append(D_vnytr_sl_n)
    # print('D внтр сл[n]: ', D_vnytr_n)
    
    # Формула для расчета D_ср_сл[n]:
    # D_ср_сл[n] = D_внутр_сл[n] + а_сл[n]
    D_sr_sl_n = [a + b for a, b in zip(dwi_a_list, D_vnytr_n)]
    # print('D сред сл[n]: ', D_sr_sl_n)
    
    # Формула для расчета D_ср_внеш[n]:
    # D_ср_внеш[n] = D_ср_сл[n] + а_сл[n]
    D_vnesh_sl_n = [a + b for a, b in zip(dwi_a_list, D_sr_sl_n)]
    # print('D внеш сл[n]: ', D_vnesh_sl_n)

    # обозначения :

    # p_mat - удельное сопротивление материала обмотки ( p_мат ) ( берется из copper.dat и aluminum.dat - ключ "p_mat")
    # l_wire - длина провода слоя ( l_пр )
    # n - кол-во параллелей ( parallels_entry_values )
    # S_lcs - сечение проводов слоя ( S_пр )
    # Pi - 3.1415
    # D_ad - средний диаметр слоя ( D_сл_ср )
    # W_l - кол-во витков слоя ( W_сл ) ( number_of_turns_values )
    # S_wcs - площадь сечения провода ( Sсеч_пр, задается в BD ) ( stn )
    
    # S_lcs = n * S_wcs
    # l_wire = (Pi * D_ad) * (W_l * n)
    # R_act = p_mat(l_wire/(n * S_lcs))
    
    # обозначения :
    # D_idc - внутренний диаметр катушки ( D_внутр ) ( Id )
    # a_l - толщина слоев ( a_сл ) ( dwi_a )
    # a_i - толщина изоляции ( а_из ) ( dar )


    '''Расчеты R_активного'''
    # parallels_entry_list  # список кол-ва параллелей 
    # print(stn_list)
    # S_pr_n = mtl_value[n] * parallels_entry_list[n]
    s_pr_list = []

    # parallels_entry_list_float = list(map(float, parallels_entry_list))
    for n in range(len(parallels_values)):
        S_pr_n = float(mtl_value[n]) * float(parallels_values[n])
        s_pr_list.append(S_pr_n)
        # print(f"S_pr[{n}] = {S_pr_n}")
    # print('S_провода[n] : ', s_pr_list)
        
    Pi = 3.1415
    # l_пр ( длина провода слоя )
    # l_pr = Pi * D_sr  * W_sl * n
    # l_pr[n] = Pi * D_sr[n] * number_of_turns_entry_list[n] * parallels_entry_list[n] 
    l_pr_list = []
    for n in range(len(number_of_turns_values)):
        l_pr = float(Pi) * float(D_sr_sl_n[n]) * float(number_of_turns_values[n]) * float(parallels_values[n])
        l_pr_list.append(l_pr)
    # print('l_провода[n] : ', l_pr_list)

    # r_act_list = []
    for n in range(len(mtl_value)):
        R_act_n = float(mtl_value[n]) * (float(l_pr_list[n]) / (float(parallels_values[n]) * float(s_pr_list[n])))
        # r_act_list.append(R_act_n)
        active_resistance.append(R_act_n)
    # print('R_активное[n] : ', r_act_list)

    '''Заполнение label Активное сопротивление в таблице результатами расчетов'''
    # active_resistance # список для результатов расчетов Активного сопротивления(Добавлять расчеты в этот список), для присвоения этих значений в таблицу
    active_resistance_str = list(map(str, active_resistance)) # Конвертация значений списка active_resistance из float в str
    for ar in range(get_value_int[0]): # get_value_int стр.341
        active_resistance_tab_list[ar].configure(text=active_resistance_str[ar])
    sum_r_act = sum(active_resistance)
    ######################################################

    
    
    
    
    
    
    
    #############################################################  ПАРАМЕТРЫ КАТУШКИ ОБНОВЛЕНИЕ ЗНАЧЕНИЙ ############################################################# 
    winding_height_calculation.configure(text=max_nember_in_winding_height) # Высота намотки в мм
    outer_diameter_of_the_coil_calculation.configure(text=Odc) # Внешний диаметр катушки
    total_active_resistance_calculation.configure(text=sum_r_act) # Суммарное актвное сопротивление
    
    
    
    
def _wire_parameters(): # Запуск окна ВЫБОР МАТЕРИАЛА
    subprocess.Popen(['python', 'material.py'])

def _help():
    subprocess.Popen(['Python','help.py'])
    
def _about_message():
    ''' pa - pre alpha
        a - alpha
        b - beta
        r - release
        5.5.23( 5(1) - date, 5(2)- month, 23 - year)'''
    messagebox.showinfo(title='О программе', message='версия: pa_28.5.23, версия BD pa_4.5.23')

# def _error_ValueError(): # исключение на ввод целого числа
#     messagebox.showerror('Ошибка ввода','Вводимое значение кол-ва слоев должно быть целым числом.') 

#############################################################  ТЕМЫ ОФОРМЛЕНИЯ  ############################################################# 
def _default(): # СТАНДАРТНАЯ ТЕМА
    # Изменение цвета фона окон на gray82
    entrys = [rated_voltage_entry, rated_current_entry, rated_resistance_entry, network_frequency_entry, number_of_layers_entry, inner_diameter_entry,
            number_of_rays_entry, number_of_insulators_entyry]
    frames = [table_of_layers_and_insulations_frame, coil_attributes_frame, top_table_frame, coil_parameters_frame]
    labels = [coil_type_label, rated_voltage_label, rated_voltage_value, rated_current_label, rated_current_value, rated_resistance_label, rated_resistance_value, climatic_use_label,
            network_frequency_label, network_frequency_value, number_of_layers_label, inner_diameter_label, number_of_rays_label, number_of_insulators_label, type_of_insulators_label,
            winding_height_label, outer_diameter_of_the_coil_label, total_inductive_resistance_label,total_active_resistance_label,  total_coil_losses_label, coil_cooling_area_label,  
            coil_heat_flow_label, result_placement_insulators_label, star_inner_diameter_label, star_along_outer_diameter_label, flight_through_insulators_label, 
            compression_forces_label, stretching_forces_label, sigma_wires_label, electromagnetic_compatibility_distances_label, x_label, y_label, s_label] 
    calculations = [winding_height_calculation, outer_diameter_of_the_coil_calculation, total_inductive_resistance_calculation, coil_cooling_area_calculation, total_active_resistance_calculation,
                   total_coil_losses_calculation, coil_heat_flow_calculation, result_placement_insulators_calculation, star_inner_diameter_calculation, star_along_outer_diameter_calculation,
                   flight_through_calculation, compression_forces_calculation, stretching_forces_calculation, sigma_wires_calculation, electromagnetic_compatibility_distances_calculation,
                   x_calculation, y_calculation, s_calculation]
    default_theme_set = {'root_back':'gray82', 'win_bg':'gray82', 'frame_bg':'gray82', 'calculation':'snow', 'font_g':'black', 'frame_color':'black', 'entry':'black', 
                         'tab_fg':'black'}
    with open('Theme\default.thm', 'w') as f:  # Сохраняем измененный словарь в файл
        json.dump(default_theme_set, f)    
    root.configure(background='gray82')
    for frame in frames: # смена фона во всех frame
        frame.configure(bg='gray82')
    for calculation in calculations: # смена фона label calculation
        calculation.configure(bg='snow', highlightbackground='black')    
    for label in labels: # смена фона во сех label
        label.configure(bg='gray82')  
    for fg_font in labels: # смена цвета шрифта
        fg_font.configure(fg='black')  
    for frame_color in labels: # смена цвета рамки
        frame_color.configure(highlightbackground='black')
    for entry in entrys: # смена цвета всех entry, рамки всех entry , цвета шрифта всех entry не в таблице
        entry.configure(highlightbackground='black', bg='snow', fg='black')
    for frame in tab_frame: # смена цвета всех frame в таблице
        frame.configure(bg='gray82')
    for label in lab_frame: # смена цвета цвех label в таблице
        label.configure(bg='gray82', fg='black')                              
    root.update()

def _white(): # СВЕТЛАЯ ТЕМА
    # Изменение цвета фона окон на белый
    entrys = [rated_voltage_entry, rated_current_entry, rated_resistance_entry, network_frequency_entry, number_of_layers_entry, inner_diameter_entry,
            number_of_rays_entry, number_of_insulators_entyry]    
    frames = [table_of_layers_and_insulations_frame, coil_attributes_frame, top_table_frame, coil_parameters_frame]
    labels = [coil_type_label, rated_voltage_label, rated_voltage_value, rated_current_label, rated_current_value, rated_resistance_label, rated_resistance_value, climatic_use_label,
            network_frequency_label, network_frequency_value, number_of_layers_label, inner_diameter_label, number_of_rays_label, number_of_insulators_label, type_of_insulators_label,
            winding_height_label,  outer_diameter_of_the_coil_label, total_inductive_resistance_label,total_active_resistance_label,  total_coil_losses_label, coil_cooling_area_label,  
            coil_heat_flow_label,  result_placement_insulators_label, star_inner_diameter_label,  star_along_outer_diameter_label,  flight_through_insulators_label, 
            compression_forces_label,  stretching_forces_label,  sigma_wires_label, electromagnetic_compatibility_distances_label,  x_label,  y_label,  s_label] 
    calculations = [winding_height_calculation, outer_diameter_of_the_coil_calculation, total_inductive_resistance_calculation, coil_cooling_area_calculation, total_active_resistance_calculation,
                   total_coil_losses_calculation, coil_heat_flow_calculation, result_placement_insulators_calculation, star_inner_diameter_calculation, star_along_outer_diameter_calculation,
                   flight_through_calculation, compression_forces_calculation, stretching_forces_calculation, sigma_wires_calculation, electromagnetic_compatibility_distances_calculation,
                   x_calculation, y_calculation,  s_calculation]  
    default_theme_set = {'root_back':'snow', 'win_bg':'snow', 'frame_bg':'snow', 'calculation':'snow', 'font_g':'black', 'frame_color':'black', 'entry':'black', 
                         'tab_fg':'black'}    
    with open('Theme\default.thm', 'w') as f:  # Сохраняем измененный словарь в файл
        json.dump(default_theme_set, f)
    root.configure(background='snow')
    for frame in frames: # смена фона во всех frame
        frame.configure(bg='snow')
    for calculation in calculations: # смена фона label calculation
        calculation.configure(bg='snow', highlightbackground='black') 
    for label in labels: # смена фона во сех label
        label.configure(bg='snow')
    for fg_font in labels: # смена цвета шрифта
        fg_font.configure(fg='black')
    for frame_color in labels:
        frame_color.configure(highlightbackground='black')
    for entry in entrys: # смена цвета всех entry, рамки всех entry , цвета шрифта всех entry не в таблице
        entry.configure(highlightbackground='black', bg='snow', fg='black')  
    for frame in tab_frame: # смена цвета всех frame в таблице
        frame.configure(bg='snow')
    for label in lab_frame: # смена цвета цвех label в таблице
        label.configure(bg='snow', fg='black')                       
    root.update()

def _black(): # ТЕМНАЯ ТЕМА
    # Изменение цвета фона окон на черный
    entrys = [rated_voltage_entry, rated_current_entry, rated_resistance_entry, network_frequency_entry, number_of_layers_entry, inner_diameter_entry,
            number_of_rays_entry, number_of_insulators_entyry]
    frames = [table_of_layers_and_insulations_frame, coil_attributes_frame, top_table_frame, coil_parameters_frame]
    labels = [coil_type_label, rated_voltage_label, rated_voltage_value, rated_current_label, rated_current_value, rated_resistance_label, rated_resistance_value, climatic_use_label,
            network_frequency_label, network_frequency_value, number_of_layers_label, inner_diameter_label, number_of_rays_label, number_of_insulators_label, type_of_insulators_label,
            winding_height_label,  outer_diameter_of_the_coil_label, total_inductive_resistance_label,total_active_resistance_label,  total_coil_losses_label, coil_cooling_area_label,  
            coil_heat_flow_label,  result_placement_insulators_label, star_inner_diameter_label,  star_along_outer_diameter_label,  flight_through_insulators_label, 
            compression_forces_label,  stretching_forces_label,  sigma_wires_label, electromagnetic_compatibility_distances_label,  x_label,  y_label,  s_label] 
    calculations = [winding_height_calculation, outer_diameter_of_the_coil_calculation, total_inductive_resistance_calculation, coil_cooling_area_calculation, total_active_resistance_calculation,
                   total_coil_losses_calculation, coil_heat_flow_calculation, result_placement_insulators_calculation, star_inner_diameter_calculation, star_along_outer_diameter_calculation,
                   flight_through_calculation, compression_forces_calculation, stretching_forces_calculation, sigma_wires_calculation, electromagnetic_compatibility_distances_calculation,
                   x_calculation, y_calculation,  s_calculation] 
    default_theme_set = {'root_back':'gray25', 'win_bg':'gray25', 'frame_bg':'gray25', 'calculation':'gray25', 'font_g':'snow', 'frame_color':'snow', 'entry':'snow', 
                         'tab_fg':'snow'}    
    with open('Theme\default.thm', 'w') as f:  # Сохраняем измененный словарь в файл
        json.dump(default_theme_set, f) 
    root.configure(background='gray25')
    for frame in frames: # смена фона во всех frame
        frame.configure(bg='gray25')
    for calculation in calculations: # смена фона label calculation
        calculation.configure(bg='gray25', highlightbackground='snow') 
    for label in labels: # смена фона во сех label
        label.configure(bg='gray25')
    for fg_font in labels: # смена цвета шрифта
        fg_font.configure(fg='snow')  
    for frame_color in labels:
        frame_color.configure(highlightbackground='snow')
    for entry in entrys: # смена цвета всех entry, рамки всех entry , цвета шрифта всех entry не в таблице
        entry.configure(highlightbackground='snow', bg='gray25', fg='snow') 
    for frame in tab_frame: # смена цвета всех frame в таблице
        frame.configure(bg='gray25')
    for label in lab_frame: # смена цвета цвех label в таблице
        label.configure(bg='gray25', fg='snow')       
    root.update()      
            
def _dark_orange(): # Dark Orange2 ТЕМА
    # Изменение цвета фона окон на черный
    entrys = [rated_voltage_entry, rated_current_entry, rated_resistance_entry, network_frequency_entry, number_of_layers_entry, inner_diameter_entry,
            number_of_rays_entry, number_of_insulators_entyry]
    frames = [table_of_layers_and_insulations_frame, coil_attributes_frame, top_table_frame, coil_parameters_frame]
    labels = [coil_type_label, rated_voltage_label, rated_voltage_value, rated_current_label, rated_current_value, rated_resistance_label, rated_resistance_value, climatic_use_label,
            network_frequency_label, network_frequency_value, number_of_layers_label, inner_diameter_label, number_of_rays_label, number_of_insulators_label, type_of_insulators_label,
            winding_height_label,  outer_diameter_of_the_coil_label, total_inductive_resistance_label,total_active_resistance_label,  total_coil_losses_label, coil_cooling_area_label,  
            coil_heat_flow_label,  result_placement_insulators_label, star_inner_diameter_label,  star_along_outer_diameter_label,  flight_through_insulators_label, 
            compression_forces_label,  stretching_forces_label,  sigma_wires_label, electromagnetic_compatibility_distances_label,  x_label,  y_label,  s_label] 
    calculations = [winding_height_calculation, outer_diameter_of_the_coil_calculation, total_inductive_resistance_calculation, coil_cooling_area_calculation, total_active_resistance_calculation,
                   total_coil_losses_calculation, coil_heat_flow_calculation, result_placement_insulators_calculation, star_inner_diameter_calculation, star_along_outer_diameter_calculation,
                   flight_through_calculation, compression_forces_calculation, stretching_forces_calculation, sigma_wires_calculation, electromagnetic_compatibility_distances_calculation,
                   x_calculation, y_calculation,  s_calculation] 
    default_theme_set = {'root_back':'gray25', 'win_bg':'gray25', 'frame_bg':'gray25', 'calculation':'gray25', 'font_g':'dark orange2', 'frame_color':'dark orange2', 'entry':'dark orange2', 
                         'tab_fg':'dark orange2'}
    with open('Theme\default.thm', 'w') as f:  # Сохраняем измененный словарь в файл
        json.dump(default_theme_set, f) 
    root.configure(background='gray25')
    for frame in frames: # смена фона во всех frame
        frame.configure(bg='gray25')
    for calculation in calculations: # смена фона label calculation
        calculation.configure(bg='gray25', fg='dark orange2', highlightbackground='dark orange2') 
    for label in labels: # смена фона во сех label
        label.configure(bg='gray25')
    for fg_font in labels: # смена цвета шрифта
        fg_font.configure(fg='dark orange2')  
    for frame_color in labels:
        frame_color.configure(highlightbackground='dark orange2')
    for entry in entrys: # смена цвета всех entry, рамки всех entry , цвета шрифта всех entry не в таблице
        entry.configure(highlightbackground='dark orange2', bg='snow', fg='black')
    for frame in tab_frame: # смена цвета всех frame в таблице
        frame.configure(bg='gray25')
    for label in lab_frame: # смена цвета цвех label в таблице
        label.configure(bg='gray25', fg='dark orange2')    
    root.update()     
                
            
            
root = Tk()
root.geometry('1920x1000+0+0')
root.title('Калькулятор электрических катушек') # Расчет электромагнитного ядра катушки
root.iconbitmap(default='ico\main_favicon.ico') # настройка иконки главного окна

# Получение цвета фона главного окна из файла options.save
with open('Theme\default.thm', 'r') as f:
    color_set = json.load(f)
background_root = color_set['root_back']
win_bg = color_set['win_bg'] # фон 
frame_bg = color_set['frame_bg'] # фон всех фреймов
font_g = color_set['font_g']
calc_bg = color_set['calculation']
tab_fg = color_set['tab_fg']
root['bg'] = background_root # настройка цвета фона главного окна



########## МЕНЮ ##########
mainmenu = Menu(root) 
root.config(menu=mainmenu) 
root.option_add("*tearOff", FALSE)

filemenu = Menu(mainmenu, tearoff=0)
# filemenu.add_command(label='Сохранить...')
filemenu.add_separator()
filemenu.add_command(label='Выход', command=lambda:root.destroy())

tablemenu = Menu(mainmenu, tearoff=0)
tablemenu.add_command(label='Создать', command=_create_table)
tablemenu.add_command(label='Очистить', state='disabled', command=_clear_table)
tablemenu.add_separator()
tablemenu.add_command(label='Расчитать', state='disabled', command=_math_table)

materialmenu = Menu(mainmenu, tearoff=0)
materialmenu.add_command(label='Настройка материала', command=_wire_parameters)

optionsmenu = Menu(mainmenu, tearoff=0)
thememenu = Menu(optionsmenu)
thememenu.add_command(label='Стандартная', command=_default)
thememenu.add_command(label='Светлая', command=_white)
thememenu.add_command(label='Темная', command=_black)
thememenu.add_command(label='Dark Orange', command=_dark_orange)
optionsmenu.add_cascade(label='Темы', menu=thememenu)



helpmenu = Menu(mainmenu, tearoff=0)
# helpmenu.add_command(label='Помощь', command=_help)
helpmenu.add_command(label='О программе', command=_about_message)

mainmenu.add_cascade(label='Файл', menu=filemenu)
mainmenu.add_cascade(label='Таблица', menu=tablemenu)
mainmenu.add_cascade(label='Материал', menu=materialmenu)
mainmenu.add_cascade(label='Настройки', menu=optionsmenu)
mainmenu.add_cascade(label='Справка', menu=helpmenu)



########## СТАНДАРТНЫЕ АТРИБУТЫ ##########
word_font = 'Arial 10'
# win_bg = 'gray82'
####################

########## ТАБЛИЦА СЛОЕВ И ИЗОЛЯЦИЙ ##########
table_of_layers_and_insulations_frame = Frame(root, width=1530, height=970, bg=frame_bg, highlightbackground='black', highlightthickness=1)
table_of_layers_and_insulations_frame.place(x=380, y=10)

# создание линний на месте таблицы
line_canvas = Canvas(table_of_layers_and_insulations_frame, width=1520, height=964, bg=win_bg)
line_canvas.pack()
line_canvas.create_line(0, 0, 1520, 964, smooth=1)
line_canvas.create_line(0, 964, 1520, 0, smooth=1)
tip_label = Label(line_canvas, text='PRE ALPHA', font='Arial 36', bg=win_bg, relief=SOLID)
tip_label.place(x=620, y=450)

########## Атрибуты катушки ###########
coil_attributes_frame = Frame(root, width=360, height=200, bg=frame_bg, highlightbackground='black', highlightthickness=1)
coil_attributes_frame.place(x=10, y=10)
# ТИП КАТУШКИ
coil_type_label = Label(coil_attributes_frame, text='Тип катушки', bg=win_bg, fg=font_g, font=word_font)
coil_type_label.place(x=10, y=10)
coil_type_combo = ttk.Combobox(coil_attributes_frame, values=['PTOC','PTCT', 'PTCTГ', 'PTCTУ'],width=10)
coil_type_combo.current(0)
coil_type_combo.place(x=230, y=10)

# НОМИНАЛЬНОЕ НАПРЯЖЕНИЕ
rated_voltage_label = Label(coil_attributes_frame, text='Номинальное напряжение', bg=win_bg, fg=font_g,  font=word_font)
rated_voltage_label.place(x=10, y=40)
rated_voltage_entry = Entry(coil_attributes_frame, width=10, bg=calc_bg, fg=font_g, highlightbackground=font_g, highlightthickness=1)
rated_voltage_entry.place(x=230, y=40)
rated_voltage_value = Label(coil_attributes_frame, text='кВ', bg=win_bg, fg=font_g)
rated_voltage_value.place(x=320, y=40)

# НОМИНАЛЬНЫЙ ТОК
rated_current_label = Label(coil_attributes_frame, text='Номинальный ток', bg=win_bg, font=word_font, fg=font_g)
rated_current_label.place(x=10, y=70)
rated_current_entry = Entry(coil_attributes_frame, width=10, bg=calc_bg, fg=font_g, highlightbackground=font_g, highlightthickness=1)
rated_current_entry.place(x=230, y=70)
rated_current_value = Label(coil_attributes_frame, text='A', bg=win_bg, fg=font_g)
rated_current_value.place(x=320, y=70)

# НОМИНАЛЬНОЕ СОПРОТИВЛЕНИЕ
rated_resistance_label = Label(coil_attributes_frame, text='Номинальное сопротивление', bg=win_bg, font=word_font, fg=font_g)
rated_resistance_label.place(x=10, y=100)
rated_resistance_entry = Entry(coil_attributes_frame, width=10, bg=calc_bg, fg=font_g, highlightbackground=font_g, highlightthickness=1)
rated_resistance_entry.place(x=230, y=100)
rated_resistance_value = Label(coil_attributes_frame, text='Ом', bg=win_bg, fg=font_g)
rated_resistance_value.place(x=320, y=100)

# КЛИМАТИЧЕСКОЕ ИСПОЛЬЗОВАНИЕ
climatic_use_label = Label(coil_attributes_frame, text='Климатическое использование', bg=win_bg, font=word_font, fg=font_g)
climatic_use_label.place(x=10, y=130)
climatic_use_combo = ttk.Combobox(coil_attributes_frame, values=['У1','У3', 'УХЛ1', 'УХЛ3'], width=10)
climatic_use_combo.current(0)
climatic_use_combo.place(x=230, y=130)

# ЧАСТОТА СЕТИ
network_frequency_label = Label(coil_attributes_frame, text='Частота сети', bg=win_bg, font=word_font, fg=font_g)
network_frequency_label.place(x=10, y=160)
network_frequency_value = StringVar()
network_frequency_value.set('50')
network_frequency_entry = Entry(coil_attributes_frame, width=10, bg=calc_bg, fg=font_g, highlightbackground=font_g, highlightthickness=1, textvariable=network_frequency_value)
network_frequency_entry.place(x=230, y=160)
network_frequency_value = Label(coil_attributes_frame, text='Гц', bg=win_bg, fg=font_g)
network_frequency_value.place(x=320, y=160)
####################

########## Вторая сверху,слева  ТАБЛИЦА ##########
# Обводка фрейма таблицы
top_table_frame = Frame(root, width=360, height=170, bg=frame_bg, highlightbackground='black', highlightthickness=1)
top_table_frame.place(x=10, y=220)

# Количество слоев
number_of_layers_label = Label(top_table_frame, text='Количество слоев', bg=win_bg, font=word_font, fg=font_g)
number_of_layers_label.place(x=10, y=10)
number_of_layers_entry = Entry(top_table_frame, width=10, bg=calc_bg, fg=font_g, highlightbackground=font_g, highlightthickness=1)
number_of_layers_entry.place(x=230, y=10)
number_of_layers_entry.insert(0, '1') # значение по умолчанию

# Внутренний диаметр
inner_diameter_label = Label(top_table_frame, text='Внутренний диаметр', bg=win_bg, font=word_font, fg=font_g)
inner_diameter_label.place(x=10, y=40)
inner_diameter_entry = Entry(top_table_frame, width=10, bg=calc_bg, fg=font_g, highlightbackground=font_g, highlightthickness=1)
inner_diameter_entry.place(x=230, y=40)
inner_diameter_entry.insert(0, '0') # значение по умолчанию

# Число лучей звезды
number_of_rays_label = Label(top_table_frame, text='Число лучей звезды', bg=win_bg, font=word_font, fg=font_g)
number_of_rays_label.place(x=10, y=70)
number_of_rays_entry = Entry(top_table_frame, width=10, bg=calc_bg, fg=font_g, highlightbackground=font_g, highlightthickness=1)
number_of_rays_entry.place(x=230, y=70)

# Число изоляторов
number_of_insulators_label = Label(top_table_frame, text='Число изоляторов', bg=win_bg, font=word_font, fg=font_g)
number_of_insulators_label.place(x=10 , y=100)
number_of_insulators_entyry = Entry(top_table_frame, width=10, bg=calc_bg, fg=font_g, highlightbackground=font_g, highlightthickness=1)
number_of_insulators_entyry.place(x=230, y=100)

# Тип изоляторов
type_of_insulators_label = Label(top_table_frame, text='Тип изоляторов', bg=win_bg, font=word_font, fg=font_g)
type_of_insulators_label.place(x=10, y=130)

with open('Data\\insdict.dat', 'r') as f:
    insulator_dictionary = json.load(f)
    type_of_insulators_combo = ttk.Combobox(top_table_frame, width=15, values=list(insulator_dictionary))
    type_of_insulators_combo.current(0)
    type_of_insulators_combo.place(x=230, y=130)
####################



########## ПАРАМЕТРЫ КАТУШКИ ###########
coil_parameters_frame = Frame(root, width=360, height=580, bg=frame_bg, highlightbackground='black', highlightthickness=1)
coil_parameters_frame.place(x=10, y=400)

# Высота намотки
winding_height_label = Label(coil_parameters_frame, text='Высота намотки, мм', bg=win_bg, font=word_font, fg=font_g)
winding_height_label.place(x=10, y=10)
winding_height_calculation = Label(coil_parameters_frame, width=10, bg=calc_bg,  fg=font_g, highlightbackground=font_g, highlightthickness=1) # bg=calc_bg
winding_height_calculation.place(x=260, y=10)

# Внешний диаметр катушки
outer_diameter_of_the_coil_label = Label(coil_parameters_frame, text='Внешний диаметр катушки', bg=win_bg, font=word_font, fg=font_g)
outer_diameter_of_the_coil_label.place(x=10, y=40)
outer_diameter_of_the_coil_calculation = Label(coil_parameters_frame, width=10, bg=calc_bg,  fg=font_g, highlightbackground=font_g, highlightthickness=1)
outer_diameter_of_the_coil_calculation.place(x=260, y=40)

# Суммарное индуктивное сопротивление, Ом
total_inductive_resistance_label = Label(coil_parameters_frame, text='Сум-ое индук-ое сопр-ие, Ом', bg=win_bg, font=word_font, fg=font_g)
total_inductive_resistance_label.place(x=10, y=70)
total_inductive_resistance_calculation = Label(coil_parameters_frame, width=10, bg=calc_bg,  fg=font_g, highlightbackground=font_g, highlightthickness=1)
total_inductive_resistance_calculation.place(x=260, y=70)

# Суммарное активное сопротивление, Ом
total_active_resistance_label = Label(coil_parameters_frame, text='Сум-ое активное сопр-ие, Ом', bg=win_bg, font=word_font, fg=font_g)
total_active_resistance_label.place(x=10, y=100)
total_active_resistance_calculation = Label(coil_parameters_frame, width=10, bg=calc_bg,  fg=font_g, highlightbackground=font_g, highlightthickness=1)
total_active_resistance_calculation.place(x=260, y=100)

# Общие потери катушки, кВт
total_coil_losses_label = Label(coil_parameters_frame, text='Общие потери катушки, кВт', bg=win_bg, font=word_font, fg=font_g)
total_coil_losses_label.place(x=10, y=130)
total_coil_losses_calculation = Label(coil_parameters_frame, width=10, bg=calc_bg,  fg=font_g, highlightbackground=font_g, highlightthickness=1)
total_coil_losses_calculation.place(x=260, y=130)

# Площадь охлаждения катушки, м2
coil_cooling_area_label = Label(coil_parameters_frame, text='Площадь охлаждения катушки, м2', bg=win_bg, font=word_font, fg=font_g)
coil_cooling_area_label.place(x=10, y=160)
coil_cooling_area_calculation = Label(coil_parameters_frame, width=10, bg=calc_bg,  fg=font_g, highlightbackground=font_g, highlightthickness=1)
coil_cooling_area_calculation.place(x=260, y=160)

# Тепловой поток катушки, Вт/м2
coil_heat_flow_label = Label(coil_parameters_frame, text='Тепловой поток катушки, Вт/м2', bg=win_bg, font=word_font, fg=font_g)
coil_heat_flow_label.place(x=10, y=190)
coil_heat_flow_calculation = Label(coil_parameters_frame, width=10, bg=calc_bg,  fg=font_g, highlightbackground=font_g, highlightthickness=1)
coil_heat_flow_calculation.place(x=260, y=190)

# Результат расстановки изоляторов
result_placement_insulators_label = Label(coil_parameters_frame, text='Результат расстановки изоляторов', bg=win_bg, font=word_font, fg=font_g)
result_placement_insulators_label.place(x=10, y=220)
result_placement_insulators_calculation = Label(coil_parameters_frame, width=10, bg=calc_bg,  fg=font_g, highlightbackground=font_g, highlightthickness=1)
result_placement_insulators_calculation.place(x=260, y=220)

# Пролет по звезде по внутреннему диаметру, мм
star_inner_diameter_label = Label(coil_parameters_frame, text='Пролет по звезде по вну-му диа-ру, мм', bg=win_bg, font=word_font, fg=font_g)
star_inner_diameter_label.place(x=10, y=250)
star_inner_diameter_calculation = Label(coil_parameters_frame, width=10, bg=calc_bg,  fg=font_g, highlightbackground=font_g, highlightthickness=1)
star_inner_diameter_calculation.place(x=260, y=250)

# Пролет по звезде по наружниму диаметру, мм
star_along_outer_diameter_label = Label(coil_parameters_frame, text='Пролет по звезде по нар-му диа-ру, мм', bg=win_bg, font=word_font, fg=font_g)
star_along_outer_diameter_label.place(x=10, y=280)
star_along_outer_diameter_calculation = Label(coil_parameters_frame, width=10, bg=calc_bg,  fg=font_g, highlightbackground=font_g, highlightthickness=1)
star_along_outer_diameter_calculation.place(x=260, y=280)

# Пролет по изоляторам, мм
flight_through_insulators_label = Label(coil_parameters_frame, text='Пролет по изоляторам, мм', bg=win_bg, font=word_font, fg=font_g)
flight_through_insulators_label.place(x=10, y=310)
flight_through_calculation = Label(coil_parameters_frame, width=10, bg=calc_bg,  fg=font_g, highlightbackground=font_g, highlightthickness=1)
flight_through_calculation.place(x=260, y=310)

# Усилия сжатия, кН
compression_forces_label = Label(coil_parameters_frame, text='Усилия сжатия, кН', bg=win_bg, font=word_font, fg=font_g)
compression_forces_label.place(x=10, y=340)
compression_forces_calculation = Label(coil_parameters_frame, width=10, bg=calc_bg,  fg=font_g, highlightbackground=font_g, highlightthickness=1)
compression_forces_calculation.place(x=260, y=340)

# Усилия растяжения, кН
stretching_forces_label = Label(coil_parameters_frame, text='Усилия растяжения, кН', bg=win_bg, font=word_font, fg=font_g)
stretching_forces_label.place(x=10, y=370)
stretching_forces_calculation = Label(coil_parameters_frame, width=10, bg=calc_bg,  fg=font_g, highlightbackground=font_g, highlightthickness=1)
stretching_forces_calculation.place(x=260, y=370)

# Сигма провода
sigma_wires_label = Label(coil_parameters_frame, text='Сигма провода', bg=win_bg, font=word_font, fg=font_g)
sigma_wires_label.place(x=10, y=400)
sigma_wires_calculation = Label(coil_parameters_frame, width=10, bg=calc_bg,  fg=font_g, highlightbackground=font_g, highlightthickness=1)
sigma_wires_calculation.place(x=260, y=400)

# Расстояния электромагнитной совместимости
electromagnetic_compatibility_distances_label = Label(coil_parameters_frame, text='Расстояния электромаг-й совмес-ти', bg=win_bg, font=word_font, fg=font_g)
electromagnetic_compatibility_distances_label.place(x=10, y=430)
electromagnetic_compatibility_distances_calculation = Label(coil_parameters_frame, width=10, bg=calc_bg,  fg=font_g, highlightbackground=font_g, highlightthickness=1)
electromagnetic_compatibility_distances_calculation.place(x=260, y=430)

# Х, мм
x_label = Label(coil_parameters_frame, text='X, мм', bg=win_bg, font=word_font, fg=font_g)
x_label.place(x=10, y=460)
x_calculation = Label(coil_parameters_frame, width=10, bg=calc_bg,  fg=font_g, highlightbackground=font_g, highlightthickness=1)
x_calculation.place(x=260, y=460)

# У, мм
y_label = Label(coil_parameters_frame, text='Y, мм', bg=win_bg, font=word_font, fg=font_g)
y_label.place(x=10, y=490)
y_calculation = Label(coil_parameters_frame, width=10, bg=calc_bg,  fg=font_g, highlightbackground=font_g, highlightthickness=1)
y_calculation.place(x=260, y=490)

# S, мм
s_label = Label(coil_parameters_frame, text='S, мм', bg=win_bg, font=word_font, fg=font_g)
s_label.place(x=10, y=520)
s_calculation = Label(coil_parameters_frame, width=10, bg=calc_bg,  fg=font_g, highlightbackground=font_g, highlightthickness=1)
s_calculation.place(x=260, y=520)





root.mainloop()

    # labels = [coil_type_label, rated_voltage_label, rated_voltage_value, rated_current_label, rated_current_value, rated_resistance_label, rated_resistance_value, climatic_use_label,
    #         network_frequency_label, network_frequency_value, number_of_layers_label, inner_diameter_label, number_of_rays_label, number_of_insulators_label, type_of_insulators_label,
    #         winding_height_label, winding_height_calculation, outer_diameter_of_the_coil_label, outer_diameter_of_the_coil_calculation, total_inductive_resistance_label,
    #         total_inductive_resistance_calculation, total_active_resistance_label, total_active_resistance_calculation, total_coil_losses_label, total_coil_losses_calculation,
    #         coil_cooling_area_label, coil_cooling_area_calculation, coil_heat_flow_label, coil_heat_flow_calculation, result_placement_insulators_label, result_placement_insulators_calculation,
    #         star_inner_diameter_label, star_inner_diameter_calculation, star_along_outer_diameter_label, star_along_outer_diameter_calculation, flight_through_insulators_label, 
    #         flight_through_calculation, compression_forces_label, compression_forces_calculation, stretching_forces_label, stretching_forces_calculation, sigma_wires_label, sigma_wires_calculation,
    #         electromagnetic_compatibility_distances_label, electromagnetic_compatibility_distances_calculation, x_label, x_calculation, y_label, y_calculation, s_label, s_calculation]
    
        # labels = [coil_type_label, rated_voltage_label, rated_voltage_value, rated_current_label, rated_current_value, rated_resistance_label, rated_resistance_value, climatic_use_label,
        #     network_frequency_label, network_frequency_value, number_of_layers_label, inner_diameter_label, number_of_rays_label, number_of_insulators_label, type_of_insulators_label,
        #     winding_height_label, outer_diameter_of_the_coil_label, total_inductive_resistance_label,total_active_resistance_label, total_coil_losses_label,
        #     coil_cooling_area_label, coil_heat_flow_label, result_placement_insulators_label,star_inner_diameter_label, star_along_outer_diameter_label, flight_through_insulators_label, 
        #     compression_forces_label, stretching_forces_label, sigma_wires_label,electromagnetic_compatibility_distances_label, x_label, y_label, s_label]  