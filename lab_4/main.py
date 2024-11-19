from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from loguru import logger

logger.add("sys.stdout", format="{time} {level} {message}", level="INFO", colorize=True)

width,height="700","500"
framecolor="green"
notebookcolor = "purple"
fg="white"
fontsize=20


t=Tk()
t.geometry(width+"x"+height)
t.resizable(0,0)

usern = StringVar ()
usern2 = StringVar ()
userp = StringVar ()
usercn = StringVar ()

studentrno = StringVar()
studentn = StringVar()
phymarks = StringVar()
chemarks = StringVar()
mathmarks = StringVar()

f33=None
f22=None


def loggedin():
    logger.info("User logged in")
    nb=ttk.Notebook()
    nb.place(x=0,y=0,width=width,height=height)
    def tabchanged(a):
        if nb.index('current') == 5 :
            studentrno.set("") 
            studentn.set("")  
            phymarks.set("") 
            chemarks.set("") 
            mathmarks.set("")
            home()
            logger.info("Navigated to Home tab")
  
    nb.bind("<<NotebookTabChanged>>",tabchanged)
    insert(nb)
    search(nb)
    showa(nb)
    update(nb)
    delete(nb)
    logout(nb)


def insert(nb):
    f1=Frame(bg=notebookcolor)
    nb.add(f1,text="manan")
    Label(f1, text="Enter Roll.No. ",fg=fg, bg=notebookcolor, font=("", 17)).place(x=60, y=50)
    entryrn = Entry ( f1 , font = ( "" , 15 ) , width = 18 , textvariable = studentrno )
    entryrn.place(x=300, y=50)
    Label(f1, text="Enter Name",fg=fg, bg=notebookcolor, font=("", 17)).place(
        x=60, y=100)
    entryname = Entry(f1, font=("", 15), width=18 , textvariable = studentn)
    entryname.place(x=300, y=100)
    Label(f1, text="Physics Marks",fg=fg, bg=notebookcolor, font=("", 17)).place(
        x=60, y=150)
    entryphy = Entry(f1, font=("", 15), width=18 , textvariable = phymarks)
    entryphy.place(x=300, y=150)
    Label(f1, text="Chemistry Marks",fg=fg, bg=notebookcolor, font=("", 17)).place(
        x=60, y=200)
    entrychem = Entry(f1, font=("", 15), width=18 , textvariable = chemarks)
    entrychem.place(x=300, y=200)
    Label(f1, text="Mathematics Marks",fg=fg, bg=notebookcolor, font=("", 17)).place(
        x=60, y=250)
    entrymath = Entry(f1, font=("", 15), width=18 , textvariable = mathmarks)
    entrymath.place(x=300, y=250)
    def marksSubmit():
        global f33
        try :   
            db=sqlite3.connect('projectdb.db')
            cr=db.cursor()
            cr.execute(
                "insert into students(RNO,NAME,PHY,CHE,MATHS) VALUES('"+studentrno.get()+"','"+studentn.get()+"','"+phymarks.get()+"','"+chemarks.get()+"','"+mathmarks.get()+"')")
            db.commit()
            logger.info(f"Inserted data for Roll No: {studentrno.get()}")
        except sqlite3.Error as e:
            logger.error(f"Database error during insertion: {e}")
        finally :   
            db.close()
        print("success")
        showall(f33)
        studentrno.set("")
        studentn.set("")
        mathmarks.set("")
        phymarks.set("")
        chemarks.set("")
    Button(f1, text="Submit", font=("", 15),fg=fg, bg=notebookcolor,activebackground="blue"
           ,command=marksSubmit).place(x=int(width) / 3, y=int(height) / 2 + 100) 

def search(nb):
    global f22
    s1=StringVar()
    f2=Frame(bg = notebookcolor )
    nb.add(f2,text="Search")
    f22=f2
    Label(f2,text="Enter Roll. No.",bg=notebookcolor,fg="white",font=("",15)).place(x=int(width)/2-200,y=80)
    Entry(f2,textvariable=s1,font=("",11),justify="right").place(x=int(width)/2-50,y=85,width=150) 
    def searchdb():
        logger.info(f"Searching for Roll No: {s1.get()}")
        try :
            db=sqlite3.connect('projectdb.db')
            cr=db.cursor()  
            r1=cr.execute("select * from students where RNO='"+s1.get()+"'") 
            print(r1)
            for r in r1 :
                logger.info(f"Data found for Roll No {s1.get()}: {r}")
                Label(f2,text="Name is",bg=notebookcolor,fg="white",font=("",15)).place(x=int(width)/2-200,y=200)
                Label(f2,text="Physics marks",bg=notebookcolor,fg="white",font=("",15)).place(x=int(width)/2-200,y=250)
                Label(f2,text="Chemistry marks",bg=notebookcolor,fg="white",font=("",15)).place(x=int(width)/2-200,y=300)
                Label(f2,text="MAthematics marks",bg=notebookcolor,fg="white",font=("",15)).place(x=int(width)/2-200,y=350) 
                Label(f2,text=r[1],bg=notebookcolor,fg="white",font=("",15)).place(x=int(width)/2+50,y=200)
                Label(f2,text=r[2],bg=notebookcolor,fg="white",font=("",15)).place(x=int(width)/2+50,y=250)
                Label(f2,text=r[3],bg=notebookcolor,fg="white",font=("",15)).place(x=int(width)/2+50,y=300)
                Label(f2,text=r[4],bg=notebookcolor,fg="white",font=("",15)).place(x=int(width)/2+50,y=350)
                break
            else:
                logger.warning(f"No data found for Roll No: {s1.get()}")
                Label(f2,bg=notebookcolor).place(x=0,y=150,width=700,height=350)
            db.commit()
        except Exception as e:
            logger.error(f"Error occurred while searching for Roll No {s1.get()}: {e}")
        finally :   
            db.close()
            logger.info(f"Search operation completed for Roll No: {s1.get()}")
    Button(f2,text="Search",bg=notebookcolor,fg="white",command=searchdb,
        font=("",11)).place(x=int(width)/2+120,y=80,width=150)   

def showa(nb):
    global f33
    logger.info("Initializing 'Show All' tab")
    try:
        f3=Frame(bg=notebookcolor)
        nb.add(f3,text="Show All")
        f33=f3
        showall(f3)
    except Exception as e:
        logger.error(f"An error occurred in 'showa': {e}")

def showall(f3):
    logger.info("Starting 'showall' function")
    Label(f3,bg=notebookcolor).place(x=0,y=0,width=int(width),height=int(height))
    Label(f3,text="Roll No.",bg=notebookcolor,fg="white",font=("",15)).place(x=30,y=10)
    Label(f3,text="Name",bg=notebookcolor,fg="white",font=("",15)).place(x=180,y=10)
    Label(f3,text="Physics ",bg=notebookcolor,fg="white",font=("",15)).place(x=300,y=10)
    Label(f3,text="Chemistry",bg=notebookcolor,fg="white",font=("",15)).place(x=420,y=10)
    Label(f3,text="Mathematics",bg=notebookcolor,fg="white",font=("",15)).place(x=540,y=10)
    
    logger.info("Database connection initiated for 'showall'")
    try :    
        db=sqlite3.connect('projectdb.db')
        cr=db.cursor()
        r=cr.execute("select * from students")
        logger.info("Database query executed: SELECT * FROM students")
        x=30
        y=40
        for r1 in r:
            if r1[0] =="" :
                logger.warning("Skipped empty roll number entry")
                continue
            logger.debug(f"Displaying data for Roll No: {r1[0]}")   
            Label(f3,text=r1[0],font=("",11),bg=notebookcolor,fg="white").place(x=x,y=y)
            x += 150
            Label(f3,text=r1[1],font=("",11),bg=notebookcolor,fg="white").place(x=x,y=y)
            x += 120
            Label(f3,text=r1[2],font=("",11),bg=notebookcolor,fg="white").place(x=x,y=y)
            x += 120
            Label(f3,text=r1[3],font=("",11),bg=notebookcolor,fg="white").place(x=x,y=y)
            x += 120
            Label(f3,text=r1[4],font=("",11),bg=notebookcolor,fg="white").place(x=x,y=y)
            x = 30
            y+=20
        logger.info("All student data displayed successfully")
        db.commit()
    except Exception as e:
        logger.error(f"An error occurred in 'showall': {e}")
    finally :    
        db.close()
        logger.info("Database connection closed")

def update(nb):
    logger.info("Initializing 'update' function")
    en=StringVar()
    ep=StringVar()
    ec=StringVar()
    em=StringVar()
    f4=Frame(bg=notebookcolor)
    nb.add(f4,text="Update")
    Label(f4,text="Enter Roll. No.",bg=notebookcolor,fg="white",font=("",15)).place(x=int(width)/2-200,y=80)
    Entry(f4,textvariable=studentrno,font=("",11),justify="right").place(x=int(width)/2-50,y=85,width=150)
    def searchdb():
        logger.info(f"Searching for Roll No: {studentrno.get()}")
        try :
            db=sqlite3.connect('projectdb.db')
            cr=db.cursor()  
            r1=cr.execute("select * from students where RNO='"+studentrno.get()+"'")
            logger.info(f"Database query executed: SELECT * FROM students WHERE RNO={studentrno.get()}")
            print(r1)
            for r in r1 :
                logger.info(f"Record found: {r}")
                en.set(r[1])
                ep.set(r[2])
                ec.set(r[3])
                em.set(r[4]) 
                Label(f4,text="Name is",bg=notebookcolor,fg="white",font=("",15)).place(x=int(width)/2-200,y=200)
                Label(f4,text="Physics marks",bg=notebookcolor,fg="white",font=("",15)).place(x=int(width)/2-200,y=250)
                Label(f4,text="Chemistry marks",bg=notebookcolor,fg="white",font=("",15)).place(x=int(width)/2-200,y=300)
                Label(f4,text="MAthematics marks",bg=notebookcolor,fg="white",font=("",15)).place(x=int(width)/2-200,y=350) 
                Entry(f4,textvariable=en,bg="white",fg="red",font=("",15)).place(x=int(width)/2+50,y=200)
                Entry(f4,textvariable=ep,bg="white",fg="red",font=("",15)).place(x=int(width)/2+50,y=250)
                Entry(f4,textvariable=ec,bg="white",fg="red",font=("",15)).place(x=int(width)/2+50,y=300)
                Entry(f4,textvariable=em,bg="white",fg="red",font=("",15)).place(x=int(width)/2+50,y=350)
                def updatedata():
                    global f33
                    logger.info(f"Updating data for Roll No: {studentrno.get()}")
                    try :   
                        db=sqlite3.connect('projectdb.db')
                        cr=db.cursor()
                        cr.execute(
                            "update students set NAME='"+en.get()+"',PHY='"+ep.get()+"',CHE='"+ec.get()+"',MATHS='"+em.get()+"' where RNO='"+studentrno.get()+"'")
                        db.commit()
                        logger.info(f"Data updated for Roll No: {studentrno.get()}")
                    except Exception as e:
                        logger.error(f"Error updating data: {e}")
                    finally :   
                        db.close()
                        logger.info("Database connection closed after update")
                        showall(f33)
                Button(f4,text="Update",bg=notebookcolor,fg="white",command=updatedata,
                    font=("",11)).place(x=int(width)/2-200,y=400) 
                break
            else:
                logger.warning(f"No record found for Roll No: {studentrno.get()}")
                Label(f4,bg=notebookcolor).place(x=0,y=150,width=700,height=350)
            db.commit()
            
        except Exception as e:
            logger.error(f"Error in 'searchdb': {e}")
        finally :   
            db.close()
            logger.info("Database connection closed after search")
    Button(f4,text="Search",bg=notebookcolor,fg="white",command=searchdb,
        font=("",11)).place(x=int(width)/2+120,y=80,width=150)   


def delete(nb):
    logger.info("Initializing 'delete' function")
    s1=StringVar()
    f5=Frame(bg=notebookcolor)
    nb.add(f5,text="Delete")
    logger.info("Delete tab added to notebook")
    Label(f5,text="Enter Roll. No.",bg=notebookcolor,fg="white",font=("",15)).place(x=int(width)/2-200,y=80)
    Entry(f5,textvariable=s1,font=("",11),justify="right").place(x=int(width)/2-50,y=85,width=150)
    def deletedata():
        global f33
        logger.info(f"Attempting to delete record for Roll No: {s1.get()}")
        try :   
            db=sqlite3.connect('projectdb.db')
            cr=db.cursor()
            r1=cr.execute("select * from students where RNO='"+s1.get()+"'")
            for r in r1:
                logger.info(f"Record found for Roll No: {s1.get()} - {r}")
                cr.execute("delete from students where RNO='"+s1.get()+"'")
                messagebox.showinfo("Data Deleted",s1.get()+" roll numbered student's data deleted")
                break
            else:
                logger.warning(f"No record found for Roll No: {s1.get()}")
                messagebox.showinfo("Data not found",s1.get()+" roll numbered student's data not found")       
            db.commit()
        except Exception as e:
            logger.error(f"Error deleting record for Roll No: {s1.get()} - {e}")
        finally :   
            db.close()
            logger.info("Database connection closed after delete operation")
        showall(f33)


    Button(f5,text="Delete",bg=notebookcolor,fg="white",command=deletedata,
        font=("",11)).place(x=int(width)/2+120,y=80,width=150)   


def logout(nb):
    logger.info("Initializing 'logout' function")
    f6=Frame(bg= notebookcolor)
    nb.add(f6,text="Logout")
    Button(f6,text="logout",command=home).place(x=int(width)/2,y=int(height)/2)
    logger.info("Logout button clicked. Redirecting to home screen.")
 

def login():
    logger.info("Login function initiated")
    try :
        db = sqlite3.connect('projectdb.db')
        cr = db.cursor()
        logger.info("Database connection established")
        logger.info(f"Attempting login for username: {usern.get()}")
        got=cr.execute("select * from users where UNAME='"+usern.get()+"' AND UPASS='"+userp.get()+"'")
        for i in got :
            logger.info(f"User found: {i}")
            loggedin()
            usern2.set(usern.get())
            messagebox.showinfo("Its My First Python Project", "WELCOME "+usern2.get()+" !!")
            break
        else:
            logger.warning(f"Login failed: No user found for username {usern.get()}")
        db.commit()
        logger.info("Database changes committed")
    except Exception as e:
        logger.error(f"Error during login: {e}")
    finally :
        db.close()
        logger.info("Database connection closed")
    userp.set("")
    usern.set("")
    usercn.set("")
    logger.info("Input fields reset")

def testUserData():
    logger.info("Started validating user data")

    freeoferrors=[True,True,True]
    if len(usern.get())==0:
        freeoferrors[0]=False
        logger.warning("Validation failed: Username is empty")  
    if len(userp.get())<5:
        freeoferrors[1]=False
        logger.warning("Validation failed: Password is too short")
    if len (list (filter( lambda x:x!=" ", usern.get() ) ) ) == 0:
        freeoferrors[0]=False
        logger.warning("Validation failed: Username contains only spaces")
    if len(userp.get()) != len (list (filter (lambda x:x!=" ", userp.get() ))):
        logger.warning("Validation failed: Password contains spaces")
        freeoferrors[1]=False
    if len(usercn.get())!=10:
        freeoferrors[2]=False
        logger.warning("Validation failed: Contact number is not 10 digits long")

    try:
        for i in range(10):
            iWantNumbers = int(usercn.get()[i])
    except ValueError:
        freeoferrors[2]=False
        logger.warning("Validation failed: Contact number contains non-numeric characters")
    except IndexError:
        freeoferrors[2] = False
        logger.error("Validation failed: Contact number is shorter than expected")
    logger.info(f"Validation results: {freeoferrors}")
    return freeoferrors


def submit():
    logger.info("User registration process started")
    emsg=""
    if testUserData()==[True,True,True]:
        try :
            logger.info(f"Attempting to register user: {usern.get()}")
            db = sqlite3.connect('projectdb.db')
            cr = db.cursor()
            cr.execute(
                "insert into users(UNAME , UPASS , UCN) VALUES('"+usern.get()+"','"+userp.get()+"','"+usercn.get()+"')")
            db.commit()
            logger.info(f"User '{usern.get()}' successfully registered")
        except Exception as e:
            logger.error(f"Error occurred during user registration: {e}")
        finally:
            db.close()
            logger.info("Database connection closed after registration")
        messagebox.showinfo("Title", usern.get()+" succesfully Registered" )
        home()
    else:
        logger.warning("User data validation failed")
        elist=testUserData()
        emsg=""
        if elist[0]==False:
            emsg=emsg+"* Please Enter User Name\n"
            logger.warning("Validation failed: Missing or invalid username")
        if elist[1]==False :
            emsg = emsg + "* Password Too Short , min. 5 letters req.\n"
            logger.warning("Validation failed: Password too short or contains spaces")
        if elist[2]==False :
            emsg = emsg + "* Enter Valid 10 Digit Contact no.\n"
            logger.warning("Validation failed: Invalid contact number")     
        errormessage = Label( text=emsg, font=("Consolas", 11),
                                  fg="#aaff12", bg="red",width=47)
        errormessage.place(x=int(width) / 3-20, y=int(height) / 2 + 150)
        logger.info("Error message displayed to user")
        print("error")
    userp.set('')
    usern.set('')
    usercn.set('')


def loginPage():
    logger.info("Navigating to the Login Page")
    usern.set("")
    userp.set("")
    usercn.set("")
    logger.info("User input fields reset")
    loginpage=Frame(bg=framecolor)
    loginpage.place(x=0,y=0,width=width,height=height)
    logger.info("Login page frame created")

    Label(loginpage,text="Enter Name ",fg=fg,bg=framecolor,font=("",20)).place(x=60,y=100)
    Label(loginpage,text="Enter Password ",fg=fg ,bg=framecolor, font=("", 20)).place(
        x=60, y=190)
    entryname = Entry(loginpage,font=("", 20),fg=framecolor, width=18,textvariable=usern)
    entryname.place(x=300, y=100)
    entrypassword = Entry(loginpage,font=("", 20),fg=framecolor, width=18,show='*',textvariable=userp)
    entrypassword.place(x=300, y=190)
    logger.info("Input fields for username and password created")
    Button(loginpage,text="LogIn",font=("",15),fg=fg,bg=framecolor,
           command=login).place(x=int(width)/3,y=int(height) / 2+50)
    Button(loginpage,text="Back to Home",font=("",15),fg=fg,bg=framecolor,
           command=home).place(x=0,y=int(height)-50)
    Button(loginpage,text="Register",font=("",15),bg=framecolor,fg=fg,
           command=registerPage).place(x=int(width)-100,y=int(height)-50)


def registerPage():
    logger.info("Navigating to the Register Page")
    usern.set("")
    userp.set("")
    usercn.set("")
    logger.info("User input fields reset")

    framecolor = "green"
    registerpage = Frame(bg=framecolor)
    registerpage.place(x=0, y=0, width=width, height=height)
    logger.info("Register page frame created")

    Label(registerpage,text="Enter Name ", fg=fg,bg=framecolor, font=("", 20)).place(
        x=60, y=80)
    Label(registerpage,text="Enter Password ",fg=fg, bg=framecolor, font=("", 20)).place(
        x=60, y=170)
    Label(registerpage,text="Enter Contact no. ",fg=fg, bg=framecolor, font=("", 20)).place(
        x=60, y=260)
    logger.info("Labels for Name, Password, and Contact created")
    entryname = Entry(registerpage,font=("", 20),fg=framecolor, width=18,textvariable=usern)
    entryname.place(x=300, y=80)
    entrypassword = Entry(registerpage,font=("", 20),fg=framecolor, width=18,textvariable=userp)
    entrypassword.place(x=300, y=170)
    entrycontact = Entry(registerpage,font=("", 20),fg=framecolor, width=18,textvariable=usercn)
    entrycontact.place(x=300, y=260)
    logger.info("Input fields for Name, Password, and Contact created")
    Button(registerpage,text="Submit", font=("", 15),fg=fg, bg=framecolor,
           command=submit).place(x=int(width) / 3, y=int(height) / 2+100)
    Button(registerpage,text="Back to Home", font=("", 15),fg=fg, bg=framecolor,
           command=home).place(x=0, y=int(height) - 50)
    Button(registerpage,text="Log in", font=("", 15),fg=fg ,bg=framecolor,
           command=loginPage).place(x=int(width) - 100, y=int(height) - 50)

def home():
    logger.info("Navigating to the Home Page")
    homepage=Frame(bg=framecolor)
    homepage.place(x=0,y=0,width=width,height=height)
    logger.info("Home page frame created")

    Label(text="HOME PAGE",font=("",40),bg="#009900",fg=fg).place(x=int(width)/4,y=int(height)/10)
    logger.info("Home page title label created")

    blg=Button(homepage,text="Log in",font=("",20),fg=fg,bg=framecolor,width=10,height=1,
               command=loginPage)
    blg.place(x=int(width)/4-50,y=int(height)/2)
    logger.info("Log in button added")

    breg =Button(homepage,text="Register",font=("",20),fg=fg,bg=framecolor,width=10,height=1,
                 command=registerPage)
    breg.place(x=int(width)/2+50,y=int(height)/2)
    logger.info("Register button added")

logger.info("Program started")
try :
    logger.info("Connecting to the database...")
    db=sqlite3.connect('projectdb.db')
    cr=db.cursor()
    logger.info("Creating 'students' table if not exists...")
    cr.execute(
        "CREATE TABLE IF NOT EXISTS students(RNO text , NAME text , PHY text , CHE text , MATHS text)")
    db.commit()
    logger.info("'students' table created or already exists.")
    cr.execute(
        "CREATE TABLE IF NOT EXISTS users(UNAME text , UPASS text , UCN text)")
    db.commit()
    logger.info("'users' table created or already exists.")
except sqlite3.Error as e:
    logger.error(f"SQLite error occurred: {e}")
finally :   
    db.close()
    logger.info("Database connection closed.")
    
logger.info("Navigating to the Home Page")
home()

t.mainloop()
logger.info("Main loop started.")