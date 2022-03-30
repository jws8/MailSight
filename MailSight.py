#Email reader, sender, searcher, to attach to XLLibaries
#Author: Joshua A.W. Smith (https://www.github.com/jws8)
#Date: 1/26/2022
import smtplib, imaplib, email, ssl# pwinput
from types import NoneType

class MailSight():
    def __init__(self):
        #to make the program dynamic use these username and pw vars
        #self.pw_input = pwinput.pwinput()
        #self.username = str(input("enter username: "))
        #self.password = pwinput.pwinput(mask = "$")
        #use these for automation
        self.username = ""
        self.password = ""
        self.subject = ""
        self.body = ""
        self.RFC_ID = "(RFC822)"
        self.raw = NoneType
        self.selection = "inbox"
        self.user = NoneType
        #smtp protocol
        self.smtp_url = "smtp.gmail.com"
        #imap-->gmail protocol
        self.imap_url = "imap.gmail.com"
        #encrypted connection
        self.message = ""
        self.port = 465
        self.context = ssl.create_default_context()
        #dynamic program: self.receiving_email = str(input("where would you like to send this to?"))
        self.receiver_list = []
        self.inbox_item_list = []
    #verify that program is initialized
    print("Initializing MailSight...")

    def set_username_password(self, username, pw):
        self.username = username
        self.password = pw
        print("LOGGED IN")
    
    def app_logout(self):
        self.user.logout()
        print("LOGGED OUT")

    def read_mail(self, selection):
        self.selection = selection
        print(f"Selection: {selection}")
        #create a user object
        self.user = imaplib.IMAP4_SSL(self.imap_url)
        print("user defined...")
        #login
        self.user.login(self.username, self.password)
        #select imap object: inbox
        self.user.select(self.selection)
        self.user.list() #?
        t, all_data = self.user.uid("search", None, "ALL")
        self.inbox_item_list = all_data[0].split()
        print(self.inbox_item_list)
    #Not a working method
    def get_abit_data(self, b_num):
        t, data = self.user.uid("fetch", b"1", self.RFC_ID)
        print(data)
        
    def get_most_recent(self): #get most recent
        most_recent = self.inbox_item_list[-1]
        result, email_data = self.user.uid("fetch", most_recent, "(RFC822)")
        self.raw = email.message_from_bytes(email_data[0][1])
        print(self.raw)
        print("done")
    
    #params STR:subject_str, STR:message_str, LIST: address_list
    def send_mail(self, subject_str, message_str, address_list):
        with smtplib.SMTP_SSL(self.smtp_url, self.port, context = self.context) as user:
            user.ehlo()
            try: #this is verified to work ONLY for googles security third app denom: NOT an invalid password error (register meaning in params error: ...(530,))
                #1 hour later: registered meaning is defined as security error, not pw error #1//27/22 10:08PM 
                user.login(self.username, self.password)
            except smtplib.SMTPAuthenticationError: 
                print("\n IMPORTANT: \nYou need to change Gmail settings to allow \"less secure apps\"\n OR make sure your script uses the app_login method")
            self.receiver_list = address_list #change 2/16/22
            #passed in params
            subject = subject_str
            body = message_str
            message = f"Subject: {subject}\n\n{body}"
            user.sendmail(self.username, self.receiver_list, message)
            
        print("sent email!")

#Run Template
#my_gmail = MailSight()
#my_gmail.set_username_password("YourUserName", "YourPassword")
#email_list = ["johndoe@gmail.com, "marymartinez@gmail.com"]
#read mail example
#my_gmail.read_mail("inbox") 
#my_gmail.get_most_recent()
#my_gmail.app_logout() 
#send mail examples 
#my_gmail.send_mail("Subject", "Body", email_list)
#i = 0
#for i in range(len(email_list)):
 #   my_gmail.send_mail(email_list[i], my_gmail.raw, email_list[i])

