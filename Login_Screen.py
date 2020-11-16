import tkinter as Tk
import Register_Form
from DataBaseManager import DbManager
from Customer import CustomerScreen
from Driver import DriverScreen
from tkinter import messagebox as alert

class LoginPage(DbManager):


    def navigate_to_respective_screen(self,login_window,usertype,username,firstname,lastname):

        alert.showinfo("info", "successful login")
        login_window.destroy()

        if(usertype=="CUSTOMER"):
            CustomerScreen.customer_screen(self,username,firstname,lastname)

        elif(usertype=="DRIVER"):
            DriverScreen.driver_screen(self,username,firstname,lastname)


    def login_screen(self):

        def on_closing():
            login_window.destroy()

        def verify_user():

            login_result,usertype,firstname,lastname = DbManager.validate_credentials(self,username_textfield_entry.get(),passwrod_textfield_entry.get())

            if(login_result==True):
                DbManager.active_users(self,username_textfield_entry.get(),passwrod_textfield_entry.get())
                self.navigate_to_respective_screen(login_window,usertype,username_textfield_entry.get(),firstname,lastname)

            else:
                alert.showinfo("info","Invalid credentials")
                username_textfield_entry.delete(0,'end')
                passwrod_textfield_entry.delete(0,'end')

        def open_reg_window():
            login_window.destroy()
            Register_Form.RegisterFormPage.registeration_form(self)


        login_window = Tk.Tk()
        login_window.geometry("500x300")
        login_window.title("Cab Booking Application")

        heading = Tk.Label(login_window,text="Car Booking Application")
        heading.place(x=180, y=30)

        username_textfield = Tk.Label(login_window,text="Username")
        password_textfield = Tk.Label(login_window,text="Password")

        username_textfield_entry = Tk.Entry(login_window,width="30")
        username_textfield.place(x=70, y=80)

        passwrod_textfield_entry = Tk.Entry(login_window,width="30")
        password_textfield.place(x=70, y=120)

        username_textfield_entry.place(x=150, y=80)
        passwrod_textfield_entry.place(x=150, y=120)

        login_button = Tk.Button(login_window, text="Login",command=verify_user)
        login_button.place(x=255, y=160)

        register_text = Tk.Label(login_window,text="New User??")
        register_text.place(x=150, y=200)

        register_button = Tk.Button(login_window,text="Register", command=open_reg_window)
        register_button.place(x=245, y=200)

        login_window.protocol("WM_DELETE_WINDOW", on_closing)
        login_window.mainloop()




