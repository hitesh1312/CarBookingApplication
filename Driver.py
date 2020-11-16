import tkinter as Tk
import Login_Screen
from tkinter import messagebox as alert
from DataBaseManager import DbManager
from threading import Thread
import time



class Ride_acceptance_window():


    def reached_location(self,ride_details,user_details):
        count = 0
        while (True):
            time.sleep(1)
            count += 1
            if (count == 20):
                alert.showinfo("Info", "Hey ,"+ " You Reached destination!"+"\nRIDE ID: "+ride_details[6])
                DbManager.modify_ride_distribution_after_verification(self, "completed", ride_details[6])

                break

    def start_ride_window(self,ride_details,user_details,driver_winodw_mainscreen):

        def start_ride():
            Thread(target=Ride_acceptance_window.reached_location,args=(self,ride_details,user_details,)).start()
            start_ride_window.destroy()
            DbManager.modify_ride_distribution_after_verification(self,"ride_started",ride_details[6])
            driver_winodw_mainscreen.deiconify()


        start_ride_window = Tk.Tk()
        start_ride_window.geometry("280x340")
        start_ride_window.title("Start Ride window")

        ride_info = "RIDE ID:   " + ride_details[6] + "\n\nNAME: " + user_details[0] + ", " + user_details[
            1] + "\n\nNO OF PEOPLE:   " + ride_details[2] + "\n\n" + "LUGGAGE QUANTITY:  " + ride_details[3] \
                    + "\n\n" + "RIDE TYPE:    " + ride_details[4] + "\n\n CONTACT NUMBER:  " + str(
            user_details[3])

        heading = Tk.Label(start_ride_window, text="User Information")
        heading.place(x=80, y=10)

        ride_info_field = Tk.Label(start_ride_window, text=ride_info)
        ride_info_field.place(x=30, y=40)

        verify_button = Tk.Button(start_ride_window, text="START RIDE", width=15, height=2,command=start_ride)
        verify_button.place(x=60, y=270)
        start_ride_window.mainloop()



    def verify_customer_window(self,ride_details,user_details,driver_winodw_mainscreen):



        def verified_customer_msg():
            verify_customer_window.destroy()
            alert.showinfo("info", "Successfully verified!")
            Ride_acceptance_window.start_ride_window(self,ride_details,user_details,driver_winodw_mainscreen)



        def not_verified_customer_msg():
            DbManager.modify_ride_distribution_after_verification(self,"notverified",ride_details[6])
            verify_customer_window.destroy()
            driver_winodw_mainscreen.deiconify()
            alert.showinfo("info", "Verification Failed!")

        verify_customer_window = Tk.Tk()
        verify_customer_window.geometry("280x350")
        verify_customer_window.title("verification window")

        ride_info = "RIDE ID:   " + ride_details[6] +"\n\nNAME: "+user_details[0]+", "+user_details[1]+ "\n\nPICK-UP LOCATION:  " + ride_details[0] + "\n\n" + "NO OF PEOPLE:   " + ride_details[
                        2] + "\n\n" + "LUGGAGE QUANTITY:  " + ride_details[3] \
                    + "\n\n" + "RIDE TYPE:    " + ride_details[4] + "\n\n CONTACT NUMBER:  " + str(
            user_details[3])

        heading = Tk.Label(verify_customer_window, text="User Verification")
        heading.place(x=80, y=10)

        ride_info_field = Tk.Label(verify_customer_window, text=ride_info)
        ride_info_field.place(x=30, y=40)

        verify_button = Tk.Button(verify_customer_window, text="Verified", width=15, height=1, command=verified_customer_msg)
        verify_button.place(x=60, y=270)

        not_verify_button = Tk.Button(verify_customer_window, text=" Not Verified", width=15,height=1, command=not_verified_customer_msg)
        not_verify_button.place(x=60, y=300)

        verify_customer_window.mainloop()



    def accepted_ride_window_with_verify_button(self,accepted_ride_details,user_phone_no):

        def reached_location():
            individual_Accepted_ride_window_with_button.destroy()
            alert.showinfo("info","Hey, "+accepted_ride_details[5] +"\nyour driver has arrived at the location!")


        individual_Accepted_ride_window_with_button = Tk.Tk()
        individual_Accepted_ride_window_with_button.geometry("250x230")
        individual_Accepted_ride_window_with_button.title("Ride")

        ride_info = "RIDE ID:   " + accepted_ride_details[6] + "\nUSER NAME:    " + accepted_ride_details[
            5] + "\nPICK-UP LOCATION:  " + accepted_ride_details[0] + "\n" + "NO OF PEOPLE:   " + accepted_ride_details[
                        2] + "\n" + "LUGGAGE QUANTITY:  " + accepted_ride_details[3] \
                    + "\n" + "RIDE TYPE:    " + accepted_ride_details[4] + "\n\n CONTACT NUMBER:  " + str(
            user_phone_no[0])

        heading = Tk.Label(individual_Accepted_ride_window_with_button, text="Ride Information")
        heading.place(x=70, y=10)

        ride_info_field = Tk.Label(individual_Accepted_ride_window_with_button, text=ride_info)
        ride_info_field.place(x=30, y=40)

        verify_button = Tk.Button(individual_Accepted_ride_window_with_button, text="Reached Location", width=15, height=1,command=reached_location)
        individual_Accepted_ride_window_with_button.after(4000,verify_button.place(x=50, y=180))

        individual_Accepted_ride_window_with_button.mainloop()


    def accepted_ride_window(self,accepted_ride_details,user_phone_no):


        def ok_clicked():
            individual_Accepted_ride_window.destroy()
            Ride_acceptance_window.accepted_ride_window_with_verify_button(self,accepted_ride_details,user_phone_no)

        individual_Accepted_ride_window = Tk.Tk()
        individual_Accepted_ride_window.geometry("250x230")
        individual_Accepted_ride_window.title("Ride")

        ride_info = "RIDE ID:   "+accepted_ride_details[6]+"\nUSER NAME:    "+accepted_ride_details[5]+"\nPICK-UP LOCATION:  "+accepted_ride_details[0] + "\n" +"NO OF PEOPLE:   " +accepted_ride_details[2] + "\n" +"LUGGAGE QUANTITY:  "+ accepted_ride_details[3] \
                    + "\n" + "RIDE TYPE:    "+accepted_ride_details[4]

        heading = Tk.Label(individual_Accepted_ride_window, text="Ride Information")
        heading.place(x=70, y=10)

        ride_info_field = Tk.Label(individual_Accepted_ride_window, text=ride_info)
        ride_info_field.place(x=30, y=40)

        verify_button = Tk.Button(individual_Accepted_ride_window, text="OK", width=15, height=1,command=ok_clicked)
        verify_button.place(x=50, y=180)

        individual_Accepted_ride_window.mainloop()



    def ride_history_window(self,username):

        ride_history=DbManager.fetch_rides_distribution_of_driver(self,username)

        if(len(ride_history)!=0):

            ride_history_window = Tk.Tk()
            ride_history_window.title("Ride History")

            listbox = Tk.Listbox(ride_history_window,width=30,height=20)

            listbox.pack(side=Tk.LEFT, fill=Tk.BOTH)
            scrollbar = Tk.Scrollbar(ride_history_window)
            scrollbar.pack(side=Tk.RIGHT, fill=Tk.BOTH)



            for i in range(len(ride_history)):
                listbox.insert(Tk.END, "RIDE ID:    "+ride_history[i][1])
                if "REJECT" in ride_history[i][2]:
                    listbox.insert(Tk.END, "RIDE STATUS:    "+ride_history[i][2][:6])
                else:
                    listbox.insert(Tk.END, "RIDE STATUS:    "+ride_history[i][2])
                listbox.insert(Tk.END, "\n")

            listbox.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=listbox.yview)

            ride_history_window.mainloop()

        else:
            alert.showinfo("Info","No History available")


    def ride_window(self,drivername):

        ride_id=[]
        ride_id_verification=DbManager.fetch_pending_rides_for_distribution_rejected_verification(self)
        ride_id_rejected=DbManager.fetch_pending_rides_for_distribution_rejected(self,drivername)

        if ride_id_verification!=0:
            for i in ride_id_verification:
                ride_id.append(i[0])


            if ride_id_rejected!=0:
                for i in ride_id_rejected:
                    if i[0] in ride_id:
                        ride_id.remove(i[0])


                if(len(ride_id)==0):
                    ride_id=0


            if (ride_id == 0):
                alert.showinfo("info", "No Rides Available! ")

            else:
                pending_rides = DbManager.fetch_pending_rides(self, ride_id[0])

                def accept_result():
                    DbManager.modify_ride_distribution(self,ride_id[0],"accept",drivername)
                    individual_ride_window.destroy()
                    ride_details=DbManager.fetch_ride_details(self,ride_id[0])
                    user_phone_number=DbManager.fetch_user_phone_no(self,ride_details[5])

                    Ride_acceptance_window.accepted_ride_window(self,ride_details,user_phone_number)


                def reject_result():
                    DbManager.modify_ride_distribution(self,ride_id[0],"reject",drivername)
                    individual_ride_window.destroy()
                    Ride_acceptance_window.ride_window(self,drivername)

                individual_ride_window = Tk.Tk()
                individual_ride_window.geometry("250x200")
                individual_ride_window.title("Ride")

                ride_info = pending_rides[0] + "\n" + pending_rides[1] + "\n" + pending_rides[2] + "\n" + \
                            pending_rides[3] + "\n" + pending_rides[4]

                heading= Tk.Label(individual_ride_window, text="Ride Information")
                heading.place(x=70,y=10)

                ride_info_field = Tk.Label(individual_ride_window, text=ride_info)
                ride_info_field.place(x=90, y=40)

                e1 = Tk.Button(individual_ride_window, text="accept", width=10, height=1,command=accept_result)
                e2 = Tk.Button(individual_ride_window, text="reject", width=10, height=1,command=reject_result)

                e1.place(x=20,y=150)
                e2.place(x=120, y=150)

                individual_ride_window.mainloop()

        else:
            alert.showinfo("info", "No Rides Available! ")


class DriverScreen():

    global_username=""

    def driver_screen(self,username,firstname,lastname):
        global global_username
        global_username=username

        def verify_customer():

            ride_id_to_verify_customer=DbManager.get_ride_id_to_verify_customer(self,username)

            if(ride_id_to_verify_customer==0):
                ride_id_to_verify_customer_status = DbManager.fetch_ride_status_verification(self, username)
                if(ride_id_to_verify_customer_status==0 or ride_id_to_verify_customer_status[0][0]=="COMPLETED"):
                    alert.showinfo("Info","No rides accepted to verify!")
                elif(ride_id_to_verify_customer_status[0][0]=="RUNNING"):
                    alert.showinfo("Info","You are already running a ride!")

            else:
                ride_details=DbManager.fetch_ride_details(self,ride_id_to_verify_customer[0][0])
                user_Details=DbManager.fetch_user_details(self,ride_details[5])
                driver_window.withdraw()
                Ride_acceptance_window.verify_customer_window(self,ride_details,user_Details,driver_window)




        def view_history():
            Ride_acceptance_window.ride_history_window(self,username)


        def get_pending_rides_list():
            availability_status=DbManager.check_driver_availability(self,global_username)
            if(availability_status!=0):
                driver_status=DbManager.verify_driver_status(self,username)
                if(driver_status==0):
                    Ride_acceptance_window.ride_window(self,username)
                else:
                    alert.showinfo("info","Driver has already accepted a ride")
            else:
                alert.showinfo("Info","Turn on availabilty before accepting rides!")

        def on_closing():
            if alert.askokcancel("Quit", "Do you want to quit?"):
                DbManager.remove_active_user(self,global_username)
                driver_window.destroy()
                Login_Screen.LoginPage.login_screen(self)

        def logout():

            DbManager.remove_active_user(self, global_username)
            driver_window.destroy()
            Login_Screen.LoginPage.login_screen(self)

        def toggle():
            if availability_button.config('text')[-1] == 'Available':
                availability_button.config(text='Un-Available')
                current_status_of_driver="Un-Available"
                DbManager.modify_driver_availability(self,global_username,current_status_of_driver)
            else:
                availability_button.config(text='Available')
                current_status_of_driver="Available"
                DbManager.modify_driver_availability(self,global_username,current_status_of_driver)

        driver_window=Tk.Tk()
        driver_window.geometry("300x500")

        driver_window.title("Driver Main Page ")

        heading = Tk.Label(driver_window, text="Hello, \n"+ firstname+", "+lastname) #pass user name
        heading.place(x=10, y=10)

        availability_button = Tk.Button(driver_window,text="Un-Available",width=12, command=toggle)
        availability_button.place(x=170,y=10)

        avai_rides = Tk.Button(driver_window, text="Available Rides", width=15, height=2, command=get_pending_rides_list)
        avai_rides.place(x=80, y=100)

        verify_customer = Tk.Button(driver_window, text="Verify Customer",width=15,height=2,command=verify_customer)
        verify_customer.place(x=80, y=180)

        View_history_driver = Tk.Button(driver_window, text="View History", width=15, height=2,command=view_history)
        View_history_driver.place(x=80, y=260)

        logout_button = Tk.Button(driver_window, text="Logout", width=15, height=2,command=logout)
        logout_button.place(x=80, y=340)

        driver_window.protocol("WM_DELETE_WINDOW", on_closing)
        driver_window.mainloop()

