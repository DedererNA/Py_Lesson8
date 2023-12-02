import sqlite3 as sl
import os

conn = sl.connect("phonebook.db")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS tab
               (ID integer primary key AUTOINCREMENT,
               fname text NOT NULL,
               lname text,
               gender blob,
               phnumber integer)

               ;""")

cursor.execute("""CREATE TABLE IF NOT EXISTS nums
               (phnumber integer,
                num int,
               FOREIGN KEY (phnumber)  REFERENCES tab (phnumber) ON DELETE CASCADE)
               ;""")

# set="INSERT INTO tab (ID, fname, lname, gender, phnumber) values(?, ?, ?, ?, ?)"
# data=[
#     (1, 'Ivan', 'Ivanov', 'male', 1),
#     (2, 'Vlad', 'Ivanov', 'male', 2),
#     (3, 'Maxim', 'Smirnov', 'male', 3),
#     (4, 'Elena', 'Andreeva', 'female', 4),
#     (5, 'Alina', 'Vanina', 'female', 5)
# ]
# with conn:
#     conn.executemany(set, data)
# conn.commit
# set="INSERT INTO nums (phnumber, num) values (?, ?)"
# data=[
#     (1, 88005553535),
#     (1, 8900000000),
#     (2, 84951234567),
#     (3, 84990001122),
#     (4, 89059110911),
#     (5, 8901234567),
#     (5, 6250110)
# ]
# with conn:
#     conn.executemany(set, data)
# conn.commit

def add():
    max_id=cursor.execute("SELECT MAX(phnumber) FROM tab")
    new_id=int(cursor.fetchall()[0][0])
    
    print("Введите имя:")
    fname_in=input()
    while len(fname_in)==0:
        print("Неверный ввод! Введите имя:")
        fname_in=input()

    print("Введите фамилию:")
    print("Если фамилия вам неизвестна, введите '0'.")
    lname_in=input()
    while len(lname_in)==0:
        print("Неверный ввод! Если фамилия вам неизвестна, введите '0'.")
        print("Введите фамилию:")
        lname_in=input()
    if lname_in=='0':
        lname_in=""
    
    print("Введите пол:")
    print("Введите '0' для male или '1' для female.")
    gender_in=input()
    try:
        int(gender_in)
    except ValueError:
        gender_in=""
    while len(gender_in)==0 or (int(gender_in)!=0 and int(gender_in)!=1):
        print("Неверный ввод! Введите пол:")
        print("Введите '0' для male или '1' для female.")
        gender_in=input()
        try:
            int(gender_in)
        except ValueError:
            gender_in=""
    if gender_in==0:
        gender_in="male"
    else:
        gender_in="female"
    
    print("Введите телефон:")
    
    phnumber_in=input()
    try:
        int(phnumber_in)
    except ValueError:
        phnumber_in=""
    while len(phnumber_in)==0:
        print("Неверный ввод! Введите телефон:")
        phnumber_in=input()
        try:
            int(phnumber_in)
        except ValueError:
            phnumber_in=""
    phnumber_in=int(phnumber_in)

    data_tab=(fname_in, lname_in, gender_in, new_id+1)
    data_nums=(new_id+1, phnumber_in)

    cursor.execute("INSERT INTO tab (fname, lname, gender, phnumber) values(?, ?, ?, ?)", data_tab)
    cursor.execute("INSERT INTO nums (phnumber, num) values(?, ?)", data_nums)
    conn.commit()

def params(text):
    if text!="изменить":
        print("Чтобы "+ text +" ID, введите 'ID'.")
    print("Чтобы "+ text +" имя, введите 'fname'.")
    print("Чтобы "+ text +" фамилию, введите 'lname'.")
    print("Чтобы "+ text +" пол, введите 'gender'.")
    print("Чтобы "+ text +" номер телефона, введите 'phnumber'.")
    print("Введите команду:")
    inp=input()
    while ((inp!="ID" or text=="удалить") and inp!="fname" and inp!="lname" and inp!="gender" and inp!="phnumber"):
        print("Неверный ввод! Введите команду:")
        inp=input()
    return inp

def search():
    column=params("найти")    
    print("Введите текст для поиска:")
    user_input=input()
    cursor.execute("SELECT * FROM (SELECT fname, lname, gender, num FROM tab, nums WHERE tab.phnumber=nums.phnumber) WHERE " + column + "=?", (user_input, ))
    res=cursor.fetchall()
    for i in range(len(res)):
        print(res[i][0] + " " + res[i][1] + ", " + res[i][2] + ". Телефон:" + str(res[i][3]))

def edit():
    cursor.execute("SELECT ID FROM tab")
    list=cursor.fetchall()
    id=[]
    for i in range(len(list)):
       id.append(list[i][0]) 
    print("Введите ID для изменения:")
    inp_ID=input()
    try:
        int(inp_ID)
    except ValueError:
        inp_ID="" 
    while len(inp_ID)==0:
        print("Неверный ввод!")
        print("Введите ID для изменения:")
        inp_ID=input()
        try:
            int(inp_ID)
        except ValueError:
            inp_ID=""        
    while int(inp_ID) not in id:
        print("Такого ID не существует!")
        print("Введите ID для изменения:")
        inp_ID=input()
    
    column=params("изменить")

    if column=="gender":
        print("Введите '0' для male или '1' для female.")
        new_text=input()
        try:
            int(new_text)
        except ValueError:
            new_text=""
        while len(new_text)==0 or (int(new_text)!=0 and int(new_text)!=1):
            print("Неверный ввод!")
            print("Введите '0' для male или '1' для female.")
            new_text=input()
            try:
                int(new_text)
            except ValueError:
                new_text=""
        if new_text==0:
            new_text="male"
        else:
            new_text="female"
    
    elif column=="phnumber":
        print("Выберите номер телефона для изменения:")
        cursor.execute("SELECT num FROM nums WHERE phnumber=?", (int(inp_ID), ))
        cur=cursor.fetchall()
        for i in range(len(cur)):
            print(str(i+1) + ". " + str(cur[i][0]))
        print("Введите номер телефона для изменения:")
        num=input()
        try:
            int(num)
        except ValueError:
            num=""
        while num=="":
            print("Неверный ввод!")
            print("Введите № для изменения (1, 2, 3 и т.д.):")
            num=input()
        while (int(num), ) not in cur:
            print("Такой номер отсутсвует!")
            print("Введите номер телефона для изменения:")
            num=input()
            
        print("Введите новый текст:")
        new_text=input()
        try:
            int(new_text)
        except ValueError:
            new_text=""
        while len(new_text)==0:
            print("Неверный ввод!")
            new_text=input()
            try:
                int(new_text)
            except ValueError:
                new_text=""
        new_text=int(new_text)
    else:
        print("Введите новый текст:")
        new_text=input()
    

    if column!="phnumber":
        cursor.execute("UPDATE tab SET " + column + "=? WHERE ID=?", (new_text, int(inp_ID)))
    else:
        cursor.execute("UPDATE nums SET num=? WHERE num=?", (new_text, int(num)))
    conn.commit()

def add_phnum():
    cursor.execute("SELECT ID FROM tab")
    list=cursor.fetchall()
    id=[]
    for i in range(len(list)):
       id.append(list[i][0]) 
    print("Введите ID для изменения:")
    inp_ID=input()
    try:
        int(inp_ID)
    except ValueError:
        inp_ID="" 
    while len(inp_ID)==0:
        print("Неверный ввод!")
        print("Введите ID для изменения:")
        inp_ID=input()
        try:
            int(inp_ID)
        except ValueError:
            inp_ID=""        
    while int(inp_ID) not in id:
        print("Такого ID не существует!")
        print("Введите ID для изменения:")
        inp_ID=input()

    print("Введите дополнительный номер телефона:")
    new_text=input()
    try:
        int(new_text)
    except ValueError:
        new_text=""
    while len(new_text)==0:
        print("Неверный ввод!")
        new_text=input()
        try:
            int(new_text)
        except ValueError:
            new_text=""
    cursor.execute("INSERT INTO nums VALUES(?, ?)", (int(inp_ID), new_text))
    conn.commit()

def all():
    cursor.execute("SELECT * FROM (SELECT ID, fname, lname, gender, num FROM tab, nums WHERE tab.phnumber=nums.phnumber) ")
    res=cursor.fetchall()
    for i in range(len(res)):
        print("ID" + str(res[i][0]) + " " + res[i][1] + " " + res[i][2] + ", " + res[i][3] + ". Телефон:" + str(res[i][4]))

def delete():
    cursor.execute("SELECT ID FROM tab")
    list=cursor.fetchall()
    id=[]
    for i in range(len(list)):
       id.append(list[i][0]) 
    print("Введите ID для изменения:")
    inp_ID=input()
    try:
        int(inp_ID)
    except ValueError:
        inp_ID="" 
    while len(inp_ID)==0:
        print("Неверный ввод!")
        print("Введите ID для изменения:")
        inp_ID=input()
        try:
            int(inp_ID)
        except ValueError:
            inp_ID=""        
    while int(inp_ID) not in id:
        print("Такого ID не существует!")
        print("Введите ID для изменения:")
        inp_ID=input()
    cursor.execute("DELETE FROM tab WHERE ID=?", (inp_ID, ))
    conn.commit()

def clear():
    os.system("cls")

def com_list():
    print("\n")

    print("Для поиска по справочнику введите 'search'.")
    print("Для добавления нового контакта введите 'add'.")
    print("Для изменения контакта введите 'edit'.")
    print("Для добавления нового номера к контакту введите 'add_phnum'.")
    print("Для удаления контакта введите 'delete'.")
    print("Для просмотра всех контактов введите 'all'.")
    print("Для очистки консоли введите 'clear'.")
    print("Введите команду:")
    
    command=input()
    while command!="all" and command!="clear" and command!="search" and command!="add" and command!="delete" and command!="edit" and command!="add_phnum":
        print("Неверная команда!")
        print("Введите команду:")
        command=input()
    return exe(command)

def exe(command):
    
    list={'all':all, 'delete':delete, "search":search, 'add':add, 'edit':edit, 'clear':clear, 'add_phnum':add_phnum}
    
    list[command]()
    return com_list()

com_list()