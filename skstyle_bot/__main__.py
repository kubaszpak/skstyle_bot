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
        # self.driver.minimize_window()
        self.driver.get(f"https://{domain}/admin/login.php")
        sleep(1)
        self.driver.find_element_by_xpath("//input[@name='email']").send_keys(username)
        sleep(1)
        self.driver.find_element_by_xpath("//input[@type='password']")\
            .send_keys(password)
        sleep(1)
        self.driver.find_element_by_xpath("//input[@value='Zaloguj']").click()
        sleep(1)
        # this part was supposed to enable running also in minimized window
        try:
            self.driver.find_element_by_xpath("/html/body/header/nav/div/div[1]/ul/li[2]/a").click()
        except Exception:
            # this part lets you change the size of window while the script is on
            fa_fa_bars = self.driver.find_element_by_xpath("/html/body/header/nav/ul/li[2]/a")
            fa_fa_bars.click()
            sleep(1)
            orders_and_clients = fa_fa_bars.find_element_by_xpath("/html/body/header/nav/div/div[1]/ul/li[2]/a/span[2]")
            orders_and_clients.click()
            sleep(1)
            orders = orders_and_clients.find_element_by_xpath("/html/body/header/nav/div/div[1]/ul/li[2]/ul/li[1]/a/span")
            orders.click()
            sleep(1)
            orders_list = orders.find_element_by_xpath("/html/body/header/nav/div/div[1]/ul/li[2]/ul/li[1]/ul/li[1]/a")
            orders_list.click()
            sleep(1)
        except:
            # but you can also achieve the same effect with 
            # ugly way of doing the same thing
            self.driver.get(f"https://{domain}/admin/orders.php")
       

        

    def is_there_new_order(self):
        data_folder = Path('skstyle_bot/')
        file_to_open = data_folder / 'last_order.txt'
        if(file_to_open.is_file() and os.stat(file_to_open).st_size != 0):
            f = open(file_to_open, "r")
            last_printed_order = int(f.read())
            f.close()
            f = open(file_to_open, "w")
            latest_order = int(self.driver.find_element_by_xpath("/html/body/div[2]/form[2]/section[1]/div[2]/div[1]/div[2]").text)
            f.write(str(latest_order))
            #//div[@class='widthId']
            f.close()
            return last_printed_order
        else:
            f = open(file_to_open, "w")
            latest_order = (self.driver.find_element_by_xpath("/html/body/div[2]/form[2]/section[1]/div[2]/div[1]/div[2]").text)
            f.write(latest_order)
            f.close()
            return None

    def handle_orders(self,last_printed_order):
        order_section = self.driver.find_element_by_xpath("/html/body/div[2]/form[2]/section[1]/div[2]")
        orders = order_section.find_elements_by_xpath("./div[starts-with(@class,'row ')]")
        # for order in orders:
            # order_number = int(order.find_element_by_xpath("./div[@class='widthId']").text)
            # print(order_number)
            # if(order_number > last_printed_order):
                # print(order.find_element_by_xpath(".//a[starts-with(@href,'https://{domain}/admin/orders.php?page=1&oID')]").text)
                # order_to_file(order)
        order_number = int(orders[0].find_element_by_xpath("./div[@class='widthId']").text)
        # order_to_file(orders[0])
        self.driver.get(f"https://{self.domain}/admin/orders.php?page=1&oID={order_number}&action=edit&ro=1")

    def close(self):
        self.driver.quit()


def order_to_file(order,domain):
    order.find_element_by_xpath(f".//a[starts-with(@href,'https://{domain}/admin/orders.php?page=1&oID=')]").click()

def main():
    driver = Skstyle(input("Your login: "),input("Your password: "),input("Your domain: "))
    # driver = Skstyle(secrets.username,secrets.password,secrets.domain)
    last_printed_order = driver.is_there_new_order()
    if(last_printed_order!=None):
        driver.handle_orders(last_printed_order)
    driver.close()


