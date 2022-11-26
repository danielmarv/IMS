from tkinter import *
from PIL import ImageTk
from tkinter import messagebox
import sqlite3
import os
import email_pass
import smtplib
import time

class Login_System:
    def __init__(self,root):
        self.root=root
        self.root.title("Login System | Developed By Daniel Marvin | JoshicTech")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="#fafafa")
        self.otp=''
        #=======images===========
        self.phone_image=ImageTk.PhotoImage(file="img/login.png")
        self.lbl_phone_image=Label(self.root,image=self.phone_image,bd=0).place(x=50,y=50)

        # ========Login Frame=======
        self.employee_id=StringVar()
        self.password=StringVar()

        login_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        login_frame.place(x=700,y=90,width=350,height=460)

        title=Label(login_frame,text="Login System",font=("Elephant",30,"bold"),bg="white").place(x=0,y=30,relwidth=1)

        lbl_user=Label(login_frame,text="Employee ID",font=("Andales",15),bg="white",fg="#767171").place(x=50,y=100)
        txt_employee_id=Entry(login_frame,textvariable=self.employee_id,font=("times new roman",15),bg="#ECECEC").place(x=50,y=140,width=250)


        lbl_pass=Label(login_frame,text="Password",font=("Andales",15),bg="white",fg="#767171").place(x=50,y=200)
        txt_pass=Entry(login_frame,textvariable=self.password,show="*",font=("times new roman",15),bg="#ECECEC").place(x=50,y=240,width=250)


        btn_login=Button(login_frame,command=self.login,text="Log in",font=("Arial Rounded MT Bold",15),bg="#00b0f0",activebackground="#00b0f0",fg="white",activeforeground="white",cursor="hand2").place(x=50,y=300,width=250,height=35)

        hr=Label(login_frame,bg="lightgray").place(x=50,y=370,width=250,height=2)
        or_=Label(login_frame,text="OR",bg="white",font=("times new roman",15,"bold")).place(x=150,y=360)

        btn_forget=Button(login_frame,command=self.forgot_window,text="Forgot Password",font=("times new roman",13),bg="white",fg="#00759e",bd=0,activebackground="white",activeforeground="#00759e").place(x=100,y=390)


        #====Frame 2============
        register_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        register_frame.place(x=700,y=570,width=350,height=60)

        lbl_reg=Label(register_frame,text="SUBSCRIBE | LIKE | SHARE",font=("times new roman",13,"bold"),bg="white").place(x=50,y=20)

        # self.send_email('xyz')        

#==============All Functions=============
    def login(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()

        try:
            if self.employee_id.get()=="" or self.password.get()=="":
                messagebox.showerror("Error","All Fields are required",parent=self.root)
            else:
                cur.execute("Select utype from employee where eid=? AND pass=?",(self.employee_id.get(),self.password.get()))
                user=cur.fetchone()
                if user==None:
                    messagebox.showerror("Error","Invalid EMPLOYEE ID/PASSWORD",parent=self.root)
                else:
                    print(user)
                    if user[0]=="Admin":
                        self.root.destroy()
                        os.system("python dashboard.py")
                    else:
                        self.root.destroy()
                        os.system("python billing.py")
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)


    def forgot_window(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.employee_id.get()=="":
                messagebox.showerror("Error","Employee ID Must be required",parent=self.root)
            else:
                cur.execute("Select email from employee where eid=? ",(self.employee_id.get(),))
                email=cur.fetchone()
                if email==None:
                    messagebox.showerror("Error","Invalid Employee ID, try again",parent=self.root)
                else:
                    # =====Forgot Window========
                    self.var_otp=StringVar()
                    self.var_new_pass=StringVar()
                    self.var_conf_pass=StringVar()
                    # call send_email_fuction()
                    chk=self.send_email(email[0])
                    if chk=='f':
                        messagebox.showerror("Error","Connection Error, try again",parent=self.root) 
                    else:
                        
                        self.forgot_win=Toplevel(self.root)
                        self.forgot_win.title('RESET PASSWORD')
                        self.forgot_win.geometry('400x350+500+100')
                        self.forgot_win.focus_force()

                        title=Label(self.forgot_win,text='Reset Password',font=('times new roman',15,'bold'),bg='#3f51b5',fg='white').pack(side=TOP,fill=X)
                        lbl_reset=Label(self.forgot_win,text='Enter OTP Sent on Registered Email',font=("times new roman",15)).place(x=20,y=60)


                        txt_reset=Entry(self.forgot_win,textvariable=self.var_otp,font=("times new roman",15),bg='lightyellow').place(x=20,y=100,width=250,height=30)
                        

                        lbl_new_pass=Label(self.forgot_win,text='New Password',font=("times new roman",15)).place(x=20,y=160)
                        txt_new_pass=Entry(self.forgot_win,textvariable=self.var_new_pass,font=("times new roman",15),bg='lightyellow').place(x=20,y=190,width=250,height=30)
                        

                        c_pass=Label(self.forgot_win,text='Confirm Password',font=("times new roman",15)).place(x=20,y=225)
                        txt_c_pass=Entry(self.forgot_win,textvariable=self.var_conf_pass,font=("times new roman",15),bg='lightyellow').place(x=20,y=255,width=250,height=30)
                        

                        self.btn_reset=Button(self.forgot_win,text="SUBMIT",command=self.validate_otp,font=("times new roman",15),bg='lightblue')
                        self.btn_reset.place(x=280,y=100,width=100,height=30)

                        self.btn_update=Button(self.forgot_win,text="Update",command=self.update_password,state=DISABLED, font=("times new roman",15),bg='lightblue')
                        self.btn_update.place(x=150,y=300,width=100,height=30)


        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
        
    def send_email(self,to_):
        s=smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        email_=email_pass.email_
        pass_=email_pass.pass_

        s.login(email_, pass_)

        self.otp=int(time.strftime("%H%M%S"))+int(time.strftime("%S"))
        subj='IMS-Reset Password OTP'
        msg=f'Dear Sir/Madam, \n\nYour Reset OTP is {str(self.otp)}. \n\n With Regards, \nIMS Team'
        msg="Subject:{}\n\n{}".format(subj,msg)
        s.sendmail(email_,to_,msg)
        chk=s.ehlo()
        if chk[0]==250:
            return 's'
        else:
            return 'f'


    def update_password(self):
        if self.var_new_pass.get()=="" or self.var_conf_pass.get()=="":
            messagebox.showerror("Error","Password is Required",parent=self.forgot_win)
        elif self.var_new_pass.get()!= self.var_conf_pass.get():
            messagebox.showerror("Error","New Password & Confirm Password should be same",parent=self.forgot_win)

        else:
            con=sqlite3.connect(database=r'ims.db')
            cur=con.cursor()
            try:
                cur.execute("Update employee SET pass=? where eid=?",(self.var_new_pass.get(),self.employee_id.get()))
                con.commit()
                messagebox.showinfo("Success","Password update Successfully",parent=self.forgot_win)
                self.forgot_win.destroy()
            except Exception as ex:
                messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
            
        


    def validate_otp(self):
        if int(self.otp)==int(self.var_otp.get()):
            self.btn_update.config(state=NORMAL)
            self.btn_reset.config(state=DISABLED)
        else:
            messagebox.showerror("Error","Invalid OTP,Try Again",parent=self.forgot_win)




root=Tk()
obj=Login_System(root)
root.mainloop()
