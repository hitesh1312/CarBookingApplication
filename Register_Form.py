import tkinter as Tk
from tkinter import messagebox as alert
import Login_Screen
from DataBaseManager import DbManager

class RegisterFormPage(DbManager):

    def registeration_form(self):
        def on_closing():
            register_window.destroy()
            Login_Screen.LoginPage.login_screen(self)

        def on_submission():
            user_data=[]
            user_data.append(firstname_textfield_entry.get())
            user_data.append(lastname_textfield_entry.get())
            user_data.append(address_textfield_entry.get())
            user_data.append(contact_textfield_entry.get())
            user_data.append(emailid_textfield_entry.get())
            user_data.append(radio_button_selector.get())
            user_data.append(username_textfield_entry.get())
            user_data.append(password_textfield_entry.get())

            DbManager.insertuser(self,user_data)
            alert.showinfo("Info", "Registered Successfully")
            register_window.destroy()
            Login_Screen.LoginPage.login_screen(self)

        register_window = Tk.Tk()
        register_window.geometry("430x400")
        register_window.title("Cab Booking Application Form")
        heading = Tk.Label(register_window, text="Register Form")
        heading.place(x=180, y=10)

        firstname_textfield = Tk.Label(register_window, text="First Name")
        lastname_textfield = Tk.Label(register_window, text="Last Name")
        address_textfield = Tk.Label(register_window, text="Address")
        contact_textfield = Tk.Label(register_window, text="Phone No")
        emailid_textfield = Tk.Label(register_window, text="Email ID")
        usertype_textfield = Tk.Label(register_window, text="User Type")
        username_textfield = Tk.Label(register_window, text="UserName")
        password_textfield = Tk.Label(register_window, text="Password")


        firstname_textfield_entry = Tk.Entry(register_window, width="30")
        lastname_textfield_entry = Tk.Entry(register_window, width="30")
        address_textfield_entry = Tk.Entry(register_window, width="30")
        contact_textfield_entry = Tk.Entry(register_window, width="30")
        emailid_textfield_entry = Tk.Entry(register_window, width="30")
        username_textfield_entry = Tk.Entry(register_window, width="30")
        password_textfield_entry = Tk.Entry(register_window, width="30")

        firstname_textfield.place(x=20, y=40)
        firstname_textfield_entry.place(x=100, y=40)

        lastname_textfield.place(x=20, y=80)
        lastname_textfield_entry.place(x=100, y=80)

        address_textfield.place(x=20, y=120)
        address_textfield_entry.place(x=100, y=120)

        contact_textfield.place(x=20, y=160)
        contact_textfield_entry.place(x=100, y=160)

        emailid_textfield.place(x=20, y=200)
        emailid_textfield_entry.place(x=100, y=200)

        usertype_textfield.place(x=20,y=240)
        radio_button_selector = Tk.StringVar()

        customer_radio_button = Tk.Radiobutton(register_window, text="Customer", variable=radio_button_selector, value="CUSTOMER")
        customer_radio_button.place(x=100, y=240)

        driver_radio_button = Tk.Radiobutton(register_window, text="Driver", variable=radio_button_selector, value="DRIVER")
        driver_radio_button.place(x=200, y=240)

        username_textfield.place(x=20, y=280)
        username_textfield_entry.place(x=100, y=280)

        password_textfield.place(x=20, y=320)
        password_textfield_entry.place(x=100, y=320)

        submit_button = Tk.Button(register_window, text="Submit", command=on_submission)
        submit_button.place(x=200, y=360)

        register_window.protocol("WM_DELETE_WINDOW", on_closing)
        register_window.mainloop()