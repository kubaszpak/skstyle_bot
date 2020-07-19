from selenium import webdriver
from time import sleep

def order_to_string(webdriver,order_number,domain):
    
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