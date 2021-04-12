import smtplib

def sendmail():
    sender_mail = "dhairya.ad@somaiya.edu"
    receiver_mail = "dhairya189@gmail.com"
    password = "Dhairya.ad@123"
    message = "This is a new sample message"
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_mail, password)
    print("Login successful")
    server.sendmail(sender_mail, receiver_mail, message)
    print("Email sent successfully")

sendmail()