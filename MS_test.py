from MailSight import *
my_gmail = MailSight()
my_business_target_list = [""]
my_gmail.set_username_password("username", "password")
my_gmail.send_mail("Business Name", "Marketing", my_business_target_list)
