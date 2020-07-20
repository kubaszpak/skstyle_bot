from selenium import webdriver
from skstyle_bot import email
from skstyle_bot import data_manager
from skstyle_bot import order_handle
from time import sleep
from pathlib import Path
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
        f = open(file_to_open, "w+")
        latest_order = int(self.driver.find_element_by_xpath("/html/body/div[2]/form[2]/section[1]/div[2]/div[1]/div[2]").text)
        f.write(str(latest_order))
        f.close()
        return last_printed_order, latest_order



    def handle_orders(self,last_printed_order,latest_order):
        full_string_to_send = ''
        if(last_printed_order!=None):
            for order_number in range(last_printed_order + 1,latest_order + 1): # to include latest order
                current_order = order_handle.order_to_string(self.driver,order_number,self.domain)
                full_string_to_send = full_string_to_send + current_order + '\n\n'
        if(full_string_to_send!=''):
            email.send_to_email(full_string_to_send,self.email,self.bot_email,self.bot_email_pw)
               

    def close(self):
        self.driver.find_element_by_xpath("//a[class='fa fa-power-off important']").click()
        self.driver.quit()

def main():
    login, password, email, domain, bot_email, bot_email_pw = data_manager.set_data()
    driver = Skstyle(login, password, email, domain, bot_email, bot_email_pw)
    last_printed_order, latest_order = driver.is_there_new_order()
    driver.handle_orders(last_printed_order,latest_order)
    driver.close()

if __name__ == "__main__":
    main()
    



