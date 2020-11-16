import tkinter as Tk
import Login_Screen
from tkinter import messagebox as alert
from DataBaseManager import DbManager
import random
import time
from threading import Thread

class CustomerScreen():
    global_username=""



    def ride_status_window(self,ride_details):


        if(ride_details!=0):

            if ride_details[0][7]=="PENDING":
                alert.showinfo("Info","Searching for the drivers.\nPlease wait for few seconds")

            else:



                def ok_clicked():
                    customer_ride_status_window.destroy()

                customer_ride_status_window = Tk.Tk()
                customer_ride_status_window.geometry("500x330")
                customer_ride_status_window.title("Ride")

                ride_info = "RIDE ID:   "+ride_details[0][6]+"\nPICK-UP LOCATION:  "+ride_details[0][0] +"\nDESTINATION:  "+ride_details[0][1] +"\n" +"NO OF PEOPLE:   " +ride_details[0][2] + "\n" +"LUGGAGE QUANTITY:  "+ ride_details[0][3] \
                            + "\n" + "RIDE TYPE:    "+ride_details[0][4]+"\n\n"

                driver_details=DbManager.fetch_user_details(self,ride_details[0][8])
                driver_info="Driver Name:   "+driver_details[0]+", "+driver_details[1]+"\n" +"Driver Contact No:    "+ str(driver_details[3])

                ride_status_info=ride_info+"\n"+driver_info


                status = Tk.Label(customer_ride_status_window, text="STATUS:    "+ride_details[0][7])
                status.config(font=("Courier", 20))

                status.place(x=70, y=40)

                heading = Tk.Label(customer_ride_status_window, text="Ride Status")
                heading.place(x=220, y=10)

                ride_info_field = Tk.Label(customer_ride_status_window, text=ride_status_info)
                ride_info_field.place(x=140, y=90)

                ok_button = Tk.Button(customer_ride_status_window, text="OK", width=15, height=2,command=ok_clicked)
                ok_button.place(x=180, y=270)

                customer_ride_status_window.mainloop()

        else:
            alert.showinfo("Info","No ride booked!")

    def customer_ride_history_window(self, username):
        ride_history = DbManager.fetch_ride_details_customer_history(self, username)

        if(ride_history!=0):

            if(ride_history[0][7]!="PENDING"):

                customer_ride_history_window = Tk.Tk()
                customer_ride_history_window.title("Ride History")

                listbox = Tk.Listbox(customer_ride_history_window, width=30, height=20)

                listbox.pack(side=Tk.LEFT, fill=Tk.BOTH)
                scrollbar = Tk.Scrollbar(customer_ride_history_window)
                scrollbar.pack(side=Tk.RIGHT, fill=Tk.BOTH)

                for i in range(len(ride_history)):

                    listbox.insert(Tk.END, "RIDE ID:    " + ride_history[i][6])
                    listbox.insert(Tk.END, "DESTINATION:    " + ride_history[i][1])
                    listbox.insert(Tk.END, "DRIVER NAME:    " + ride_history[i][8])
                    listbox.insert(Tk.END, "RIDE STATUS:    " + ride_history[i][7])
                    listbox.insert(Tk.END, "\n")



                listbox.config(yscrollcommand=scrollbar.set)
                scrollbar.config(command=listbox.yview)

                customer_ride_history_window.mainloop()
            else:
                alert.showinfo("info","No History Avaialble")


        else:
            alert.showinfo("info","No History Avaialble")


    def customer_screen(self,username,firstname,lastname):

        global global_username
        global_username=username

        def ride_status_window():
            ride_history = DbManager.fetch_ride_details_customer_ride_status(self, global_username)
            CustomerScreen.ride_status_window(self,ride_history)

        def view_customer_history():
            CustomerScreen.customer_ride_history_window(self,global_username)

        def on_closing():
            if alert.askokcancel("Quit", "Do you want to quit?"):
                DbManager.remove_active_user(self,global_username)
                customer_window.destroy()
                Login_Screen.LoginPage.login_screen(self)

        def get_ride_form():
            driver_availability=DbManager.check_driver_availability(self,"customer")

            if(driver_availability==0):
                alert.showinfo("info", "No Drivers Available! ")
            else:
                customer_window.withdraw()
                RideForm.ride_form(self,customer_window,global_username)

        def logout():
            DbManager.remove_active_user(self, global_username)
            customer_window.destroy()
            Login_Screen.LoginPage.login_screen(self)

        customer_window=Tk.Tk()
        customer_window.geometry("300x400")

        customer_window.title("Customer Main Page ")

        heading = Tk.Label(customer_window, text="Hello, \n"+firstname+", "+lastname) #pass user name
        heading.place(x=10, y=10)

        book_a_ride = Tk.Button(customer_window, text="Book Ride",width=10,height=2,command=get_ride_form)
        book_a_ride.place(x=100, y=40)

        View_history = Tk.Button(customer_window, text="View History", width=10, height=2,command=view_customer_history)
        View_history.place(x=100, y=120)

        ride_status = Tk.Button(customer_window, text="Ride Status", width=10, height=2,command=ride_status_window)
        ride_status.place(x=100, y=200)

        logout_button = Tk.Button(customer_window, text="Logout", width=10, height=2,command=logout)
        logout_button.place(x=100, y=280)

        customer_window.protocol("WM_DELETE_WINDOW", on_closing)

        customer_window.mainloop()


class RideForm():
    global_username=""

    def timer_to_search_drivers(self,username):
        count=0
        while(True):
            time.sleep(1)
            count+=1
            if(count==30):
                status=DbManager.get_user_ride_status_for_timer(self,username)
                if(status==1):
                    DbManager.remove_ride_no_driver_found(self,username)
                    alert.showinfo("Info","No Drivers found. Try after some time!")

                    break
                else:
                    break




    def ride_form(self,customer_window,username):

        global global_username
        global_username=username


        def on_closing():
            if alert.askokcancel("Quit", "Are you sure you want to cancel ?"):

                ride_form_window.destroy()
                customer_window.deiconify()

        def submit_ride_form():
            check_user_ride_status=DbManager.get_user_ride_status(self,global_username)
            check_user_ride_status_list = []

            for i in range(len(check_user_ride_status)):
                check_user_ride_status_list.append(check_user_ride_status[i][0])

            if (("PENDING" in check_user_ride_status_list) or ("ACCEPT" in check_user_ride_status_list)or ("RUNNING" in check_user_ride_status_list)):
                alert.showinfo("info", "You have already requested for a ride!")

            else:
                list_of_ride_id = DbManager.get_ride_id(self)
                customer_ride_data = []

                customer_ride_data.append(current_location_textfield_entry.get())
                customer_ride_data.append(destination_location_textfield_entry.get())
                customer_ride_data.append(num_of_people_textfield_entry.get())
                customer_ride_data.append(num_of_luggage_textfield_entry.get())
                customer_ride_data.append(type_of_ride_Selector.get())
                customer_ride_data.append(global_username)

                while (True):
                    current_ride_id = username.upper() + str(random.randint(0, 10000))

                    if (list_of_ride_id == 0):
                        customer_ride_data.append(current_ride_id)
                        break
                    elif (current_ride_id not in list_of_ride_id):
                        customer_ride_data.append(current_ride_id)
                        break

                DbManager.submitted_rides(self, customer_ride_data)
                Thread(target=RideForm.timer_to_search_drivers,args=(self,global_username,)).start()
                alert.showinfo("info", "Ride submitted succesfully")


            ride_form_window.destroy()
            customer_window.deiconify()

        ride_form_window = Tk.Tk()
        ride_form_window.geometry("500x300")

        ride_form_window.title("Cab Booking Application Form")

        heading = Tk.Label(ride_form_window, text="Ride Details")
        heading.place(x=180, y=10)

        current_location_textfield = Tk.Label(ride_form_window, text="Current Location")
        destination_location_textfield = Tk.Label(ride_form_window, text="Destination Location")
        num_of_people_textfield = Tk.Label(ride_form_window, text="Num of People")
        num_of_luggage_textfield = Tk.Label(ride_form_window, text="Luggage Quantity")
        type_of_ride_textfield = Tk.Label(ride_form_window, text="Ride Type")


        current_location_textfield_entry = Tk.Entry(ride_form_window, width="30")
        destination_location_textfield_entry = Tk.Entry(ride_form_window, width="30")
        num_of_people_textfield_entry = Tk.Entry(ride_form_window, width="30")
        num_of_luggage_textfield_entry = Tk.Entry(ride_form_window, width="30")

        current_location_textfield.place(x=20, y=40)
        current_location_textfield_entry.place(x=170, y=40)

        destination_location_textfield.place(x=20, y=80)
        destination_location_textfield_entry.place(x=170, y=80)

        num_of_people_textfield.place(x=20, y=120)
        num_of_people_textfield_entry.place(x=170, y=120)

        num_of_luggage_textfield.place(x=20, y=160)
        num_of_luggage_textfield_entry.place(x=170, y=160)

        type_of_ride_textfield.place(x=20,y=200)
        Ride_Types = ["REGULAR", "VETETRAN", "EMERGENCY", ]

        type_of_ride_Selector = Tk.StringVar(ride_form_window)
        type_of_ride_Selector.set(Ride_Types[0])

        type_of_ride_dropdown = Tk.OptionMenu(ride_form_window, type_of_ride_Selector, *Ride_Types)
        type_of_ride_dropdown.place(x=170, y=200)

        submit_button = Tk.Button(ride_form_window, text="Submit Ride",command=submit_ride_form)
        submit_button.place(x=230, y=250)

        ride_form_window.protocol("WM_DELETE_WINDOW", on_closing)
        ride_form_window.mainloop()