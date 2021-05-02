# --- --- ---
# imported modules/ libraries
import mysql.connector as sql
import csv
import os
import datetime as dt
import shutil as sht
import pathlib as pth
import time

# --- --- ---
# functions
def del_cache():
    if int(input("Sure: "))==1:
        del_dir=os.listdir(r"C:\Users\SATYA NADELA\Desktop\eBooks\bookCopy")
        for i in del_dir:
            os.remove((r"C:\Users\SATYA NADELA\Desktop\eBooks\bookCopy"+"\{}").format(i))
    else:
        print("Aborted.")
        
def directory(x):  # directory of undb folder.
    if x=="book":
        return(os.listdir(r"C:\Users\SATYA NADELA\Desktop\eBooks\undbBooks"))
    elif x=="mag":
        return(os.listdir(r"C:\Users\SATYA NADELA\Desktop\eBooks\undbMags"))

def curdate():
    _=dt.datetime.now().strftime
    return(_("%d")+"/"+_("%m")+"/"+_("%Y"))

def pname_it(x):
    return(x+r"\{}")

def renamove(v11,v12,v13):  # rename and move the file from input path.
    os.rename(v11,v12)
    sht.move(v12,v13)

def file_ext(x):  # extract file extension of file name argument.
    return(pth.Path(x).suffix)

def add_to_db(x,y):  # add the input book information to the sql db.
    if y=="book":
        seperate()
        bk_id=int(unique_id("book"))
        bk_name=input("name: ").lower()
        bk_author=input("author: ").lower()
        bk_pub=input("pub: ").lower()
        bk_ed=input("ed: ")
        bk_series=input("series: ").lower()
        bk_ext=file_ext(x)
        bk_line=input("line: ").lower()
        c.execute("insert into books values({},'{}','{}','{}','{}','{}','{}','{}')"\
                  .format(bk_id,bk_name,bk_author,bk_pub,bk_ed,bk_series,bk_ext,bk_line))
        seperate()
    elif y=="mag":
        seperate()
        mag_id=int(unique_id("mag"))
        mag_name=input("name: ").lower()
        mag_basis=input("enter d|w|m|y: ").lower()
        mag_year=int(input("year: "))
        mag_month=int(input("month: "))
        mag_date=int(input("date: "))
        mag_issue=int(input("issue: "))
        mag_pub=input("publisher: ").lower()
        c.execute("insert into magazines values({},'{}',{},{},{},'{}','{}',{})"\
                  .format(mag_id,mag_name,mag_year,mag_month,mag_date,mag_basis,mag_pub,mag_issue))
        seperate()
        
def unique_id(x):  # to generate unique book/magazine id for db primary key.
    if x=="book":
        c.execute("select id from books;")
    elif x=="mag":
        c.execute("select id from magazines;")
    data=c.fetchall()
    if data!=[]:
        l=[int(i[0]) for i in data]
        v=max(l)+1
        for i in range(1,v):
            if i not in l:
                return(str(i))
        else:
            return(str(v))
    elif data==[]:
        return("1")
    
def db_data(x):
    if x=="book":
        c.execute("select * from books;")
    elif x=="mag":
        c.execute("select * from magazines;")
    return(c.fetchall())

def table(x):
    data=db_data(x)
    print("fetching records...")
    for i in data:
        print(i)

def maggies():
    count=50
    c.execute("select distinct name,count(*) from magazines group by name;")
    for i in c.fetchall():
        print(i[0],(60-len(i[0]))*"-",i[1])

def backup(x):
    print(" "*20,"backing up data...")
    f=open("{} backup.txt".format(x),"a+")
    data=db_data(x)
    __=csv.writer(f)
    f.write(curdate()+"\n")
    __.writerows(data)
    f.close()
    print("backup success")

def seperate():
    print("----- "*3)

def search_book():
    search_str=input("Enter: ");found=[]
    for i in ["id","name","author","pub","ed","series","type","line"]:
        c.execute("select * from books where {} like '%{}%'".format(i,search_str))
        for j in c.fetchall():
            found.append(j)
    print("{} records found.".format(len(j)))
    for i in found:
        print(i)

# --- --- ---
# main program

def add_books():
    try:
        bks_dir=directory("book")
        book_no=0;more=1
        while more==1:
            old_name=bks_dir[book_no];print(old_name)
            new_name=unique_id("book")+file_ext(old_name)
            print(" "*20,"opening file...")
            sht.copyfile(pname_it(old_book_path).format(old_name),pname_it(copy_book_path)\
                         .format(old_name))
            os.startfile(pname_it(copy_book_path).format(old_name))
            print("--- 0:end|1:add to db|2:skip ---")
            _=int(input("Enter:"))
            if _==0:
                break
            elif _==1:
                print(" "*20,"renaming and moving...")
                renamove(pname_it(old_book_path).format(old_name),pname_it(old_book_path)\
                         .format(new_name),new_book_path)
                print(" "*20,"renamed({} to {}) and moved.".format(old_name,new_name))
                add_to_db(old_name,"book")
                print(" "*20,"adding to database...")
                print("added to database with id:",new_name)
                more=int(input("add more(0|1): "))
                book_no+=1
                continue
            elif _==2:
                sht.move(pname_it(r"C:\Users\SATYA NADELA\Desktop\eBooks\undbBooks")\
                         .format(old_name),r"C:\Users\SATYA NADELA\Desktop\eBooks\undbMags")
                book_no+=1
    except IndexError:
        print("No Books Found.")
        
old_mag_path=r"C:\Users\SATYA NADELA\Desktop\eBooks\undbMags"
new_mag_path=r"C:\Users\SATYA NADELA\Desktop\eBooks\dbMags"
copy_mag_path=r"C:\Users\SATYA NADELA\Desktop\eBooks\bookCopy"

def add_magazines():
    try:
        mag_dir=directory("mag")
        mag_no=0;more=1
        while more==1:
            old_name=mag_dir[mag_no];print(old_name)
            new_name=unique_id("mag")+file_ext(old_name)
            print(" "*20,"opening file...")
            sht.copyfile(pname_it(old_mag_path)\
                         .format(old_name),pname_it(copy_mag_path).format(old_name))
            os.startfile(pname_it(copy_mag_path)\
                         .format(old_name))
            print("--- 0:end|1:add to db|2:skip ---")
            _=int(input("Enter:"))
            if _==0:
                break
            elif _==1:
                print(" "*20,"renaming and moving...")
                renamove(pname_it(old_mag_path)\
                         .format(old_name),pname_it(old_mag_path).format(new_name),new_mag_path)
                print(" "*20,"renamed({} to {}) and moved.".format(old_name,new_name))
                add_to_db(old_name,"mag")
                print(" "*20,"adding to database...")
                print("added to database with id:",new_name)
                more=int(input("add more(0|1): "))
                mag_no+=1
                continue
            elif _==2:
                sht.move(pname_it(r"C:\Users\SATYA NADELA\Desktop\eBooks\undbMags")\
                         .format(old_name),r"C:\Users\SATYA NADELA\Desktop\eBooks\epubFiles")
                mag_no+=1
    except IndexError:
        print("No Magazines Found.")

# --- --- ---
def book_functions():
    print("\
          1 | add books\n\
          2 | take book backup\n\
          3 | see table\n\
          4 | search books\n\
          5 | exit\n\
          ")
    _=int(input("Enter: "))
    if _==1:
        add_books()
        del_cache()
    elif _==2:
        backup("book")
    elif _==3:
        table("book")
    elif _==4:
        search_book()
    elif _==5:
        functions()
    book_functions()

def mag_functions():
    print("\
          1 | add magazines\n\
          2 | take backup\n\
          3 | see table\n\
          4 | search magazine\n\
          5 | magazines count\n\
          6 | exit\n\
          ")
    __=int(input("Enter: "))
    if __==1:
        add_magazines()
    elif __==2:
        backup("mag")
    elif __==3:
        table("mag")
    elif __==4:
        maggies()
    elif __==6:
        functions()
    mag_functions()

def functions():
    print("\
          1 | Books\n\
          2 | Magazine\n\
          3 | \n\
          4 | \n\
          5 | \n\
          6 | Exit\
          ")
    ___=int(input())
    if ___==1:
        book_functions()
    elif ___==2:
        mag_functions()
    
db=sql.connect(host="localhost",user="root",password="password",database="elib",autocommit="True")
c=db.cursor()

if db.is_connected():
    print("Connected To Database.")        
    print(curdate())

old_book_path=r"C:\Users\SATYA NADELA\Desktop\eBooks\undbBooks"
new_book_path=r"C:\Users\SATYA NADELA\Desktop\eBooks\dbBooks"
copy_book_path=r"C:\Users\SATYA NADELA\Desktop\eBooks\bookCopy"

functions()
