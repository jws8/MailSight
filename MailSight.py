#Email reader, sender, searcher, to attach to XLLibaries
#Author: Joshua Wilson Smith (https://www.github.com/jws8)
#Date: 1/26/2022
import smtplib, email, ssl, imaplib, pwinput
#Must allow 3rd party "less-secure" applications to run in gmail settings
#: THIS IS NOT THE RECOMMENDED WAY OF LOGGING IN... USE OS 2/16/22
#A later version of MailSight will automate the local OS environment 
#but I'm a bit fuzzy, currently, on how to do this globally. 2/16/22 
class MailSight():
    def __init__(self):
        #self.pw_input = pwinput.pwinput()
        self.username = str(input("enter username: "))
        self.password = pwinput.pwinput(mask = "$")
        self.subject = ""
        self.body = ""
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
    #verify that program is initialized
    print("Starting program...")

    def read_mail(self):
        print("reading mail")
        #create a user object
        user = imaplib.IMAP4_SSL(self.imap_url)
        print("logging in")
        #login
        user.login(self.username, self.password)
        #select imap object: inbox
        user.select("inbox")
        user.list() #?
        t, data = user.uid("search", None, "ALL")
        inbox_item_list = data[0].split()
        #get most recent
        most_recent = inbox_item_list[-1]
        
        result, email_data = user.uid("fetch", most_recent, "(RFC822)")
        print(email_data)
        print("done")
    
    #params STR:subject_str, STR:message_str, LIST: address_list
    def send_mail(self, subject_str, message_str, address_list):
        with smtplib.SMTP_SSL(self.smtp_url, self.port, context = self.context) as user:
            user.ehlo()
            try: #this is verified to work ONLY for googles security third app denom: NOT an invalid password error (register meaning in params error: ...(530,))
                #1 hour later: registered meaning is defined as security error, not pw error #1//27/22 10:08PM 
                user.login(self.username, self.password)
            except smtplib.SMTPAuthenticationError: 
                print("\n IMPORTANT: \nYou need to change Gmail settings to allow \"less secure apps\"\n")
            self.receiver_list = address_list #change 2/16/22
            #passed in params
            subject = subject_str
            body = message_str
            message = f"Subject: {subject}\n\n{body}"
            user.sendmail(self.username, self.receiver_list, message)
        print("sent email!")
    
#Run Template
#my_gmail = MailSight()
#my_gmail.send_mail("Subject:", "Body:", email_list)

