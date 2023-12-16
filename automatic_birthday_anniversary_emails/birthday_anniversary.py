import pandas as pd
import numpy as np
import csv

from io import BytesIO

import argparse
import random

from PIL import Image
import os, os.path
import time

from datetime import date
from datetime import datetime

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


class Greeting:
    
    def __init__(self,from_email,password, to_email,cc_list,from_name):
    
        # Define constants 
        self.MAX_BIRTHDAY_GREETINGS = 80 ## update the number when you add new message in birthday_message.csv
        self.EMPLOYEE_DETAILS_FILE = "employees.csv"
        self.GREETING_FILE = "birthday_messages.csv"
        self.from_email = from_email
        self.to_email = to_email
        self.cc_list = cc_list
        self.from_name = from_name
        self.password = password
        
        self.emp_details = pd.read_csv(self.EMPLOYEE_DETAILS_FILE,header=0)
        #print(self.emp_details)
        self.birthday_greeting = pd.read_csv(self.GREETING_FILE,header=0)
        #print(self.birthday_greeting)
        
        
       
       
    def create_birthday_email_subject_body(self,employee, message):
        email_subject = "Happy Birthday " + employee["Employee Name"]
        email_body = "Hi " + employee["Employee Name"] +","+ '<br>' + message + '<br><img src="cid:image1" width="600" height="300" text-align="center">' + "<br>Thanks,<br>" + self.from_name 
        return email_subject,email_body
        
    def create_work_anniversary_email_subject_body(self,employee, message):
        email_subject = "Happy anniversary " + employee["Employee Name"]
        email_body = "Hi " + employee["Employee Name"] +","+ '<br>' + message + '<br><img src="cid:image1" width="600" height="300" text-align="center">' + "<br>Thanks,<br>" + self.from_name 
        return email_subject,email_body
        
        
    def send_email(self,email_id,password,to_list,cc_list,email_subject, message_body, image):
        fromaddr = email_id
        toaddr = to_list
        env_address_list = to_list + ',' + cc_list
        
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            smtp.login(email_id, password)


            msgRoot = MIMEMultipart('related')
            msgRoot['Subject'] = email_subject
            msgRoot['From'] = fromaddr
            msgRoot['To'] = toaddr
            msgRoot['CC'] = cc_list
            msgRoot.preamble = ' '

            msgAlternative = MIMEMultipart('alternative')
            msgRoot.attach(msgAlternative)

            msgText = MIMEText('')
            msgAlternative.attach(msgText)
            ## Font setting here
            message_body = '<font face="Baguet Script" size="6" color="blue">' + message_body + '</font>'
            msgText = MIMEText(message_body, 'html', 'utf-8')
           # print msgText
            msgAlternative.attach(msgText)

            byte_buffer = BytesIO()
            image.save(byte_buffer, "PNG")
            #fp = open('severity_plot.png', 'rb')
            msgImage = MIMEImage(byte_buffer.getvalue())
            #fp.close()
            msgImage.add_header('Content-ID', '<image1>')
            msgRoot.attach(msgImage)

          

            text = msgRoot.as_string()
            smtp.sendmail(fromaddr,env_address_list.split(","),text)
           
        
        
        
    def send_birthday_greeting(self , employee):
        # Generate a random number betwee 0 &  max greeting
        birthday_message = random.randint(1,80)
        greet = self.birthday_greeting.iloc[birthday_message,0]
        
        bday_sub, bday_body = self.create_birthday_email_subject_body(employee,greet)
        birthday_image = random.randint(1, 21)
        image = Image.open(os.path.join("./images/",str(birthday_image) + ".jpg"))
        #print(employee["Email ID"])
        self.send_email(self.from_email,self.password,employee["Email ID"] , self.cc_list, bday_sub,bday_body,image)

    
    def send_anniversary_greeting(self, employee, service_year):
        # Generate a random number betwee 0 &  max greeting
        
        greet = "Congratulations on your " + str(service_year) + " year completion with our company! Wishing you many more successful years ahead!"
        #print(greet)
        bday_sub, bday_body = self.create_work_anniversary_email_subject_body(employee,greet)
        image_name_svc = service_year
        if service_year not in [1,3,5,10]:
            image_name_svc = 0
        
        random_image = random.randint(1,5)
        
        image_name = "./anniversary_images/" + str(random_image) +"."+ str(image_name_svc) + ".jpg"
        
        image = Image.open(image_name)
        #print(image_name)
        self.send_email(self.from_email,self.password,employee["Email ID"] , self.cc_list, bday_sub,bday_body,image)

    
    
    def send_greetings(self):
        # Iterate through engineers
        #print(self.emp_details)
        for index, employee in self.emp_details.iterrows():
            birthday = datetime.strptime(employee['Birthday'],'%Y-%m-%d')#.strftime("%m-%d")
            anniversary = datetime.strptime(employee['Work Anniversary'],'%Y-%m-%d')#.strftime("%m-%d")
            today = date.today()#.strftime("%m-%d")
            #print(type(employee))
            today_month = today.month
            today_day = today.day
            today_year = today.year
            birthday_month = birthday.month
            birthday_day = birthday.day
            
            anniversary_month = anniversary.month
            anniversary_day = anniversary.day
            anniversary_year = anniversary.year
            
            
            
            
            if today_month == birthday_month and today_day == birthday_day:
                self.send_birthday_greeting(employee)
                
            if today_month == anniversary_month and anniversary_day == today_day:
                self.send_anniversary_greeting(employee, today_year - anniversary_year)


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Add Arguments for login')
    parser.add_argument('--from_email', type=str,default="youremail@youremail.com")
    parser.add_argument('--to_email', type=str, default="youremail@youremail.com")
    parser.add_argument('--cc_list', type=str, default="youremail@youremail.com")
    parser.add_argument('--from_name', type=str,default="youremail@youremail.com")
    parser.add_argument('--password', type=str, default ="google app password")
    
    args = parser.parse_args()
    greeter = Greeting(args.from_email,args.password,args.to_email,args.cc_list, args.from_name)
    greeter.send_greetings()
