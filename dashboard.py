from tkinter  import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
from employee import  employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass
import sqlite3
import os
import time

class IMS:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventory Management System | Developed By JoshicTech")
        self.root.config(bg="white")

        #===title====
        self.icon_title=PhotoImage(file="img/61.png")
        title=Label(self.root,text="Inventory Management System",image=self.icon_title,compound=LEFT,font=("times new roman",40,"bold"),bg="#010c48",fg="white",anchor="w",padx="20").place(x=0,y=0,relwidth=1,height=70)

        #===btn_logout===
        btn_logout=Button(self.root,text="Logout",command=self.logout,font=("times new roman",15,"bold"),bg="yellow",cursor="hand2").place(x=1150,y=10,height=50,width=150)

        #===clock===
        self.lb1_clock=Label(self.root,text="Welcome to Inventory Management System\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS",font=("times new roman",15),bg="#4d636d",fg="white")
        self.lb1_clock.place(x=0,y=70,relwidth=1,height=30)

        #===Left Menu===
        self.MenuLogo=Image.open("img/cart.png")
        self.MenuLogo=self.MenuLogo.resize((200,200),Image.ANTIALIAS)
        self.MenuLogo=ImageTk.PhotoImage(self.MenuLogo)

        LeftMenu=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        LeftMenu.place(x=0,y=102,width=200,height=565)

        Lb1_Menulogo=Label(LeftMenu,image=self.MenuLogo)
        Lb1_Menulogo.pack(side=TOP,fill=X)

        lb1_menu=Label(LeftMenu,text="Menu",font=("times new roman",20),bg="#009688").pack(side=TOP,fill=X)


        btn_employee=Button(LeftMenu,text="Employee",command=self.employee,font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_supplier=Button(LeftMenu,text="Supplier",command=self.supplier,font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_category=Button(LeftMenu,text="Category",command=self.category,font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_product=Button(LeftMenu,text="Products",command=self.product,font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_sales=Button(LeftMenu,text="Sales",command=self.sales,font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_exit=Button(LeftMenu,text="Exit",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)


        #===content===
        self.lb1_employee=Label(self.root,text="Total Employee\n[0]",bd=5,relief=RIDGE, bg="#33bbf9",font=("guody old style",20,"bold"))
        self.lb1_employee.place(x=300,y=120,height=150,width=300)

        self.lb1_supplier=Label(self.root,text="Total Suppliers\n[0]",bd=5,relief=RIDGE, bg="#ADFF2F",font=("guody old style",20,"bold"))
        self.lb1_supplier.place(x=650,y=120,height=150,width=300)

        self.lb1_category=Label(self.root,text="Total Category\n[0]",bd=5,relief=RIDGE, bg="#00FF7F",font=("guody old style",20,"bold"))
        self.lb1_category.place(x=1000,y=120,height=150,width=300)

        self.lb1_product=Label(self.root,text="Total Products\n[0]",bd=5,relief=RIDGE, bg="#FFFF00",font=("guody old style",20,"bold"))
        self.lb1_product.place(x=300,y=300,height=150,width=300)

        self.lb1_sales=Label(self.root,text="Total Sales\n[0]",bd=5,relief=RIDGE, bg="#9ACD32",font=("guody old style",20,"bold"))
        self.lb1_sales.place(x=650,y=300,height=150,width=300)

        #===Footer===
        lb1_footer=Label(self.root,text="IMS-Inventory Management System | Developed By JoshicTech\n For Any Technical Problem Contact us On: 0703294785",font=("times new roman",15),bg="#4d636d",fg="white").pack(side=BOTTOM,fill=X)

        self.update_content()
#=============================================================================================


    def employee(self):
        self.new_win=Toplevel(self.root)
        self.new_abj=employeeClass(self.new_win)


    def supplier(self):
        self.new_win=Toplevel(self.root)
        self.new_abj=supplierClass(self.new_win)    


    def category(self):
        self.new_win=Toplevel(self.root)
        self.new_abj=categoryClass(self.new_win) 

    def product(self):
        self.new_win=Toplevel(self.root)
        self.new_abj=productClass(self.new_win)   

    def sales(self):
        self.new_win=Toplevel(self.root)
        self.new_abj=salesClass(self.new_win)  

    def update_content(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()

        try:
            cur.execute("Select * from product")
            product=cur.fetchall()
            self.lb1_product.config(text=f'Total Products\n[ {str(len(product))} ]')

            cur.execute("Select * from category")
            category=cur.fetchall()
            self.lb1_category.config(text=f'Total Category\n[ {str(len(category))} ]')

            cur.execute("Select * from supplier")
            supplier=cur.fetchall()
            self.lb1_supplier.config(text=f'Total Supplier\n[ {str(len(supplier))} ]')

            cur.execute("Select * from employee")
            employee=cur.fetchall()
            self.lb1_employee.config(text=f'Total Employee\n[ {str(len(employee))} ]')
            bill=len(os.listdir('bill'))
            self.lb1_sales.config(text=f'Total Sales\n [{str(bill)}] ')

            time_=time.strftime("%I:%M:%S")
            date_=time.strftime("%d-%m-%Y")
            self.lb1_clock.config(text=f"Welcome to Inventory Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
            self.lb1_clock.after(200,self.update_content )

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def logout(self):
        self.root.destroy()
        os.system("python login.py")

if __name__=="__main__":
    root=Tk()
    obj=IMS(root)
    root.mainloop()