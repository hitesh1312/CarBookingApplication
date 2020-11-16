import mysql.connector
from datetime import datetime

class DbManager():
    user_type=""

    def connect_to_db(self):

        conn = mysql.connector.connect(user='root', password='hitesh1312',host='127.0.0.1',database='cab_database', auth_plugin='mysql_native_password')
        cursor = conn.cursor()
        return (cursor,conn)

    def validate_credentials(self,username,password):

        cursor, conn = self.connect_to_db()
        query="select username,password,user_type,firstname,lastname from user_details where ( username=\""+username +"\" and password=\""+password+"\");"
        cursor.execute(query)
        val=cursor.fetchall()

        if(len(val)==0):
            return False,None,None,None
        else:
            return True,val[0][2],val[0][3],val[0][4]

    def remove_active_user(self,username):

        cursor, conn = self.connect_to_db()
        query = "select user_type from user_details where username=\""+username+"\";"
        cursor.execute(query)
        user_type = cursor.fetchone()

        if(user_type[0]=="DRIVER"):
            query = "delete from rider_availability where ( username=\"" + username + "\");"
            cursor.execute(query)

        query = "delete from active_users where ( username=\"" + username + "\");"
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()

    def remove_ride_no_driver_found(self, username):

        cursor, conn = self.connect_to_db()
        cursor.execute("select ride_id from rides where username=\""+username+"\"and ride_status=\"PENDING\";")
        ride_id=cursor.fetchall()
        query = "delete from ride_distribution where ride_status_name=\"" + ride_id[0][0] + "PENDING\";"
        query1 = "delete from rides where username=\"" + username + "\" and ride_status=\"PENDING\";"
        cursor.execute(query)
        cursor.execute(query1)
        conn.commit()
        cursor.close()
        conn.close()

    def active_users(self,username,password):

        cursor, conn = self.connect_to_db()
        query = "select * from user_details where ( username=\"" + username + "\" and password=\"" + password + "\");"
        cursor.execute(query)
        user_data = cursor.fetchone()

        if(user_data[5]=="DRIVER"):
            insert_query = "insert into rider_availability values(\""+ user_data[6] + "\",\"Un-Available\");"
            cursor.execute(insert_query)

        insert_query = "insert into active_users values(" + "\"" + user_data[0] + "\"," + "\"" + user_data[
            1] + "\"," + "\"" + user_data[2] + "\"," + "\"" + \
                       user_data[3] + "\"," + "\"" + user_data[4] + "\"," + "\"" + user_data[5] + "\"," + "\"" + user_data[6] + "\""+ ");"
        cursor.execute(insert_query)
        conn.commit()
        cursor.close()
        conn.close()

    def insertuser(self,user_data):

        cursor,conn=self.connect_to_db()
        insert_query="insert into user_details values("+"\""+user_data[0]+"\","+"\""+user_data[1]+"\","+"\""+user_data[2]+"\","+"\""+\
                     user_data[3]+"\","+"\""+user_data[4]+"\","+"\""+user_data[5]+"\","+"\"" + user_data[6] + "\","+"\""+user_data[7]+"\""+");"
        cursor.execute(insert_query)
        conn.commit()
        cursor.close()
        conn.close()

    def get_ride_id(self):

        cursor, conn = self.connect_to_db()
        query = "select ride_id from rides;"
        cursor.execute(query)
        list_of_ride_id=cursor.fetchall()
        cursor.close()
        conn.close()
        if len(list_of_ride_id)==0 :
            return 0
        else:
            return list_of_ride_id

    def get_ride_id_to_verify_customer(self,username):

        cursor, conn = self.connect_to_db()
        query = "select ride_id from ride_distribution where driver_name=\""+username+"\""+ "and ride_status=\"ACCEPT\";"
        cursor.execute(query)
        veriication_customer_ride_id=cursor.fetchall()
        cursor.close()
        conn.close()
        if len(veriication_customer_ride_id)==0:
            return 0
        else:
            return veriication_customer_ride_id

    def get_user_ride_status_for_timer(self, username):

        cursor, conn = self.connect_to_db()
        query = "select ride_status from rides where username=\"" + username + "\" and ride_status=\"PENDING\";"
        cursor.execute(query)
        list_of_user_ride_status = cursor.fetchall()
        cursor.close()
        conn.close()
        if len(list_of_user_ride_status) == 0:
            return 0
        else:
            return 1

    def get_user_ride_status(self,username):

        cursor, conn = self.connect_to_db()
        query = "select ride_status from rides where username=\""+username+"\";"
        cursor.execute(query)
        list_of_user_ride_status=cursor.fetchall()
        cursor.close()
        conn.close()
        if len(list_of_user_ride_status)==0:
            return []
        else:
            return list_of_user_ride_status

    def submitted_rides(self,ride_data):

        cursor, conn = self.connect_to_db()
        insert_query = "insert into rides values(" + "\"" + ride_data[0] + "\"," + "\"" + ride_data[
            1] + "\"," + "\"" + ride_data[2] + "\"," + "\"" + \
                       ride_data[3] + "\"," + "\"" + ride_data[4] + "\"," + "\"" + ride_data[5] + "\"," + "\"" + ride_data[6] + "\",\"PENDING\",\"\",\""+str(datetime.now())+"\");"

        insert_query_to_distribution_table = "insert into ride_distribution values(\"" +ride_data[6]+"PENDING\"," + "\"" + ride_data[6] + "\"," + "\"PENDING\",\"\",\""+str(datetime.now())+"\");"
        cursor.execute(insert_query)
        cursor.execute(insert_query_to_distribution_table)
        conn.commit()
        cursor.close()
        conn.close()

    def modify_driver_availability(self,username,driver_status):
        cursor, conn = self.connect_to_db()
        query = "UPDATE rider_availability SET availabilty =\"" + driver_status + "\"" + "WHERE username=\""+ username +"\";"
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()

    def check_driver_availability(self,name):
        cursor, conn = self.connect_to_db()
        if(name=="customer"):
            query = "select username from rider_availability where availabilty=\"Available\";"
        else:
            query = "select availabilty from rider_availability where username=\""+name+"\" and availabilty=\"Available\";"
        cursor.execute(query)
        availabilty_of_drivers = cursor.fetchall()
        cursor.close()
        conn.close()
        if len(availabilty_of_drivers)==0:
            return 0
        else:
            return 1

    def fetch_pending_rides(self,ride_id):
        cursor, conn = self.connect_to_db()
        query = "select username,ride_id,Ride_type,luggage_quantity,no_of_people from rides where ride_id=\"" +ride_id+ "\";"
        cursor.execute(query)
        list_of_avai_rides = cursor.fetchone()
        cursor.close()
        conn.close()
        if list_of_avai_rides is None:
            return 0
        else:
            return list_of_avai_rides

    def fetch_pending_rides_for_distribution(self,status,drivername):
        cursor, conn = self.connect_to_db()
        if(status=="accept"):
            query = "select ride_id,ride_status from ride_distribution where ride_status in (\"PENDING\");"
        else:
            query = "select ride_id,ride_status from ride_distribution where ride_status in (\"REJECT\");"
        cursor.execute(query)
        avai_rides_ID = cursor.fetchall()
        cursor.close()
        conn.close()
        if (len(avai_rides_ID)==0):
            return 0
        else:
            return avai_rides_ID

    def fetch_pending_rides_for_distribution_rejected_verification(self):
        cursor, conn = self.connect_to_db()
        query = "select ride_id from ride_distribution where ride_status in (\"PENDING\");"
        cursor.execute(query)
        avai_rides_ID = cursor.fetchall()
        cursor.close()
        conn.close()
        if (len(avai_rides_ID) == 0):
            return 0
        else:
            return avai_rides_ID

    def fetch_pending_rides_for_distribution_rejected(self, drivername):
        cursor, conn = self.connect_to_db()
        query = "select ride_id from ride_distribution where driver_name=\""+drivername+"\";"
        cursor.execute(query)
        avai_rides_ID = cursor.fetchall()
        cursor.close()
        conn.close()
        if (len(avai_rides_ID) == 0):
            return 0
        else:
            return avai_rides_ID

    def modify_ride_distribution(self,ride_id,acceptance_result,drivername):
        cursor, conn = self.connect_to_db()
        if (acceptance_result=="reject"):
            insert_query_to_distribution_table = "insert into ride_distribution values(\""+ride_id + "REJECT-"+drivername+ "\","  + "\"" + ride_id + "\"," + "\"REJECT-"+drivername+"\",\""+drivername+"\",\""+str(datetime.now())+"\");"
            cursor.execute(insert_query_to_distribution_table)

        else:
            query = "UPDATE ride_distribution SET ride_status =\"ACCEPT\",driver_name=\""+drivername+"\",datetime=\"" +str(datetime.now())+ "\" WHERE ride_id=\"" + ride_id + "\" and ride_status_name=\""+ride_id+"PENDING"+"\";"
            query1 = "UPDATE rides SET ride_status =\"ACCEPT\",driver_name=\""+drivername+"\",datetime=\"" +str(datetime.now())+ "\" WHERE ride_id=\"" + ride_id + "\";"
            cursor.execute(query1)
            cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()


    def verify_driver_status(self,drivername):
        cursor, conn = self.connect_to_db()
        query = "select ride_status from ride_distribution where driver_name=\"" + drivername + "\";"
        cursor.execute(query)
        availabilty_of_drivers = cursor.fetchall()
        status = []
        for i in range(len(availabilty_of_drivers)):
            status.append(availabilty_of_drivers[i][0])

        if ("ACCEPT" in status) or ("RUNNING" in status):
            return 1
        else:
            return 0

        cursor.close()
        conn.close()

    def fetch_rides_distribution_of_driver(self,drivername):
        cursor, conn = self.connect_to_db()
        query = "select * from ride_distribution where driver_name=\"" + drivername + "\" order by datetime desc;"
        cursor.execute(query)
        list_of_driver_rides = cursor.fetchall()
        cursor.close()
        conn.close()
        if list_of_driver_rides is None:
            return 0
        else:
            return list_of_driver_rides

    def fetch_ride_details(self,ride_id):
        cursor, conn = self.connect_to_db()
        query = "select * from rides where ride_id=\"" + ride_id + "\";"
        cursor.execute(query)
        ride_details = cursor.fetchone()
        cursor.close()
        conn.close()
        if ride_details is None:
            return 0
        else:
            return ride_details

    def fetch_ride_details_customer_history(self,username):
        cursor, conn = self.connect_to_db()
        query = "select * from rides where username=\"" + username + "\"and ride_status in (\"COMPLETED\",\"VERIFICATION-FAILED\") ORDER BY datetime DESC;"
        cursor.execute(query)
        ride_details = cursor.fetchall()
        cursor.close()
        conn.close()
        if len(ride_details)==0 :
            return 0
        else:
            return ride_details

    def fetch_customer_completed_destinations(self, username):
        cursor, conn = self.connect_to_db()
        query = "select destination from rides where username=\"" + username + "\"and ride_status=\"COMPLETED\";"
        cursor.execute(query)
        ride_details = cursor.fetchall()
        cursor.close()
        conn.close()
        if len(ride_details) == 0:
            return 0
        else:
            return ride_details

    def fetch_ride_details_customer_repeat(self, username,destination):
        cursor, conn = self.connect_to_db()
        query = "select * from rides where username=\"" + username + "\"and ride_status=\"COMPLETED\" and destination=\""+destination[0]+"\";"
        cursor.execute(query)
        ride_details = cursor.fetchall()
        cursor.close()
        conn.close()
        if len(ride_details) == 0:
            return 0
        else:
            return ride_details

    def fetch_ride_details_customer_ride_status(self, username):
        cursor, conn = self.connect_to_db()
        query = "select * from rides where username=\"" + username + "\"and ride_status in (\"ACCEPT\",\"RUNNING\",\"PENDING\");"
        cursor.execute(query)
        ride_details = cursor.fetchall()
        cursor.close()
        conn.close()
        if len(ride_details) == 0:
            return 0
        else:
            return ride_details

    def fetch_ride_status_verification(self,username):
        cursor, conn = self.connect_to_db()
        query = "select ride_status from rides where driver_name=\"" + username + "\" and ride_status not in (\"VERIFICATION-FAILED\");"
        cursor.execute(query)
        ride_details = cursor.fetchall()
        cursor.close()
        conn.close()
        if len(ride_details)==0:
            return 0
        else:
            return ride_details

    def fetch_user_details(self,username):
        cursor, conn = self.connect_to_db()
        query = "select * from user_details where username=\"" + username + "\";"
        cursor.execute(query)
        ride_details = cursor.fetchone()
        cursor.close()
        conn.close()
        if ride_details is None:
            return 0
        else:
            return ride_details

    def fetch_user_phone_no(self, username):
        cursor, conn = self.connect_to_db()
        query = "select phone_no from user_details where username=\"" + username + "\";"
        cursor.execute(query)
        customer_phone_number = cursor.fetchone()
        cursor.close()
        conn.close()
        if customer_phone_number is None:
            return 0
        else:
            return customer_phone_number


    def modify_ride_distribution_after_verification(self,verification_status,ride_id):
        cursor, conn = self.connect_to_db()

        if (verification_status=="ride_started"):
            query = "UPDATE ride_distribution SET ride_status =\"RUNNING\"" + "WHERE ride_id=\"" + ride_id + "\" and ride_status_name=\"" + ride_id + "PENDING" + "\";"
            query1 = "UPDATE rides SET ride_status =\"RUNNING\"WHERE ride_id=\"" + ride_id + "\";"

        elif (verification_status=="completed"):
            query = "UPDATE ride_distribution SET ride_status =\"COMPLETED\"" + "WHERE ride_id=\"" + ride_id + "\" and ride_status_name=\"" + ride_id + "PENDING" + "\";"
            query1 = "UPDATE rides SET ride_status =\"COMPLETED\"WHERE ride_id=\"" + ride_id + "\";"

        else:
            query = "UPDATE ride_distribution SET ride_status =\"VERFICATION-FAILED\"" + "WHERE ride_id=\"" + ride_id + "\" and ride_status_name=\"" + ride_id + "PENDING" + "\";"
            query1 = "UPDATE rides SET ride_status =\"VERIFICATION-FAILED\"WHERE ride_id=\"" + ride_id + "\";"

        cursor.execute(query)
        cursor.execute(query1)
        conn.commit()
        cursor.close()
        conn.close()
