import smtplib
import os
import imghdr
from email.message import EmailMessage


password = os.getenv("webcamapp")

sender = "jeremyabraham17@gmail.com"

receiver = "jeremyabraham17@gmail.com"

def send_email(image_path):
    print("send email started")
    
    email_message = EmailMessage()
    email_message["Subject"] = "New Object Captured"
    email_message.set_content("New Object has been detected")
    
    with open(image_path, "rb") as file:
        content = file.read()
        email_message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))
    
    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    try:
        gmail.login(sender, password)
        gmail.sendmail(sender,receiver, email_message.as_string())
        gmail.quit()
        print("Email sent!")
    except AttributeError as e:
        print("An error has happened", str(e))
    print("send email finish")
       
    #print("object has entered and left frame")

#if __name__ == "__main__":
#    send_email(image_path="")