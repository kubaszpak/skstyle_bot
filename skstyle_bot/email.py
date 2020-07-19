import smtplib
from email.message import EmailMessage

def send_to_email(full_string, email, bot_email, bot_email_pw):

    msg = EmailMessage()
    msg['Subject'] = 'Skstyle Orders'
    msg['From'] = bot_email
    msg['To'] = email
    msg.set_content(full_string)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

        smtp.login(bot_email, bot_email_pw)

        smtp.send_message(msg)

        smtp.quit()