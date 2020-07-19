from pathlib import Path
from time import sleep
from email.message import EmailMessage
from selenium import webdriver
import smtplib
import json
import os

class Skstyle:

    def __init__(self, username, password, email, domain, bot_email, bot_email_pw):

        self.username = username
        self.password = password
        self.email = email
        self.domain = domain
        self.bot_email = bot_email
        self.bot_email_pw = bot_email_pw

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=chrome_options)


        # logging
        self.driver.get(f"https://{domain}/admin/login.php")
        sleep(1)
        self.driver.find_element_by_xpath("//input[@name='email']").send_keys(username)
        sleep(1)
        self.driver.find_element_by_xpath("//input[@type='password']")\
            .send_keys(password)
        sleep(1)
        self.driver.find_element_by_xpath("//input[@value='Zaloguj']").click()
        sleep(1)

        self.driver.get(f"https://{domain}/admin/orders.php")
                
        

    def is_there_new_order(self):
        # checks if there is a new order
        # if you run it for the first time if returns None
        data_folder = Path('skstyle_bot/')
        file_to_open = data_folder / 'last_order.txt'
        if(file_to_open.is_file() and os.stat(file_to_open).st_size != 0):
            f = open(file_to_open, "r")
            last_printed_order = int(f.read())
            f.close()
        else:
            last_printed_order = None
        f = open(file_to_open, "w")
        latest_order = int(self.driver.find_element_by_xpath("/html/body/div[2]/form[2]/section[1]/div[2]/div[1]/div[2]").text)
        f.write(str(latest_order))
        f.close()
        return last_printed_order, latest_order



    def handle_orders(self,last_printed_order,latest_order):
        full_string_to_send = ''
        if(last_printed_order!=None):
            for order_number in range(last_printed_order + 1,latest_order + 1): # to include latest order
                current_order = order_to_file(self.driver,order_number,self.domain)
                full_string_to_send = full_string_to_send + current_order + '\n\n'
        if(full_string_to_send!=''):
            send_to_email(full_string_to_send,self.email,self.bot_email,self.bot_email_pw)
               

    def close(self):
        self.driver.quit()

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


def order_to_file(webdriver,order_number,domain):
    
    webdriver.get(f"https://{domain}/admin/orders.php?page=1&oID={order_number}&action=edit&ro=1#wysylka")

    # receiver info
    receiver_form_address_group = webdriver.find_element_by_xpath("//*[@id='receiverForm']/div")
    rows_receive = receiver_form_address_group.find_elements_by_xpath("./div[starts-with(@class,'row')]")
    contents = []
    for row in rows_receive:
        try:
            contents.append(row.find_element_by_xpath("./div[@class='content']"))
        except:
            continue

    # shipment info
    shipment_form_adrress_group = webdriver.find_element_by_xpath("//*[@id='shipmentForm']/div")
    rows_ship = shipment_form_adrress_group.find_elements_by_xpath("./div[starts-with(@class,'row')]")
    for row in rows_ship:
        try:
            contents.append(row.find_element_by_xpath("./div[@class='content']"))
        except:
            continue
    final_list = [content.text for content in contents if(content.text != '')]
    final_list.insert(0,str(order_number))
    sleep(3)
    return ' '.join(map(str,final_list)) # formatting this list into a string
    
def get_data():
    data_folder = Path('skstyle_bot/')
    file_to_open = data_folder / 'secrets.json'
    if(file_to_open.is_file() and os.stat(file_to_open).st_size != 0):
        with open(file_to_open , "r") as f:
            data = json.load(f)
            return data.get("login"),data.get("password"),data.get("email"),data.get("domain"),data.get("bot_email"),data.get("bot_email_pw")
    else:
        with open(file_to_open,"w") as f:
            login, password, email, domain, bot_email, bot_email_pw = input("Your login: "),\
                input("Your password: "), input("Your email: "), input("Your domain: "), input("Your bot's email: "), input("Your bot's email's password: ")
            personal_data = {}
            personal_data["login"]=login
            personal_data["password"]=password
            personal_data["email"]=email
            personal_data["domain"]=domain
            personal_data["bot_email"]=bot_email
            personal_data["bot_email_pw"]=bot_email_pw
            json.dump(personal_data, f)
            return login, password, email, domain, bot_email, bot_email_pw


def main():
    login, password, email, domain, bot_email, bot_email_pw = get_data()
    driver = Skstyle(login, password, email, domain, bot_email, bot_email_pw)
    last_printed_order, latest_order = driver.is_there_new_order()
    driver.handle_orders(last_printed_order,latest_order)
    driver.close()


