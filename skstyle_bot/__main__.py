from pathlib import Path
from time import sleep
from selenium import webdriver
# from skstyle_bot import secrets
import os

class Skstyle:
    def __init__(self,username,password,domain):
        self.domain = domain
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
        if(last_printed_order!=None):
            for order_number in range(last_printed_order + 1,latest_order + 1): # to include latest order
                order_to_file(self.driver,order_number,self.domain)

    def close(self):
        self.driver.quit()


def order_to_file(webdriver,order_number,domain):
    
    webdriver.get(f"https://{domain}/admin/orders.php?page=1&oID={order_number}&action=edit&ro=1#wysylka")


    receiver_form_address_group = webdriver.find_element_by_xpath("//*[@id='receiverForm']/div")
    rows_receive = receiver_form_address_group.find_elements_by_xpath("./div[starts-with(@class,'row')]")
    contents = []
    for row in rows_receive:
        try:
            contents.append(row.find_element_by_xpath("./div[@class='content']"))
        except:
            continue

    shipment_form_adrress_group = webdriver.find_element_by_xpath("//*[@id='shipmentForm']/div")
    rows_ship = shipment_form_adrress_group.find_elements_by_xpath("./div[starts-with(@class,'row')]")
    for row in rows_ship:
        try:
            contents.append(row.find_element_by_xpath("./div[@class='content']"))
        except:
            continue
    final_list = [content.text for content in contents if(content.text != '')]
    final_list.insert(0,str(order_number))
    print(final_list)
    sleep(3)
    

def main():
    driver = Skstyle(input("Your login: "),input("Your password: "),input("Your domain: "))
    # driver = Skstyle(secrets.username,secrets.password,secrets.domain)
    last_printed_order, latest_order = driver.is_there_new_order()
    driver.handle_orders(last_printed_order,latest_order)
    driver.close()


