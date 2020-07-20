import json
import os
from pathlib import Path

def read_data_from_user(file_to_open):
    with open(file_to_open,"w+") as f:
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

def set_data():
    data_folder = Path('skstyle_bot/')
    file_to_open = data_folder / 'secrets.json'
    if(file_to_open.is_file() and os.stat(file_to_open).st_size != 0):
        with open(file_to_open , "r") as f:
            data = json.load(f)
            return data.get("login"),data.get("password"),data.get("email"),data.get("domain"),data.get("bot_email"),data.get("bot_email_pw")
    else:
        read_data_from_user(file_to_open)

def change_data():
    data_folder = Path('skstyle_bot/')
    file_to_open = data_folder / 'secrets.json'
    read_data_from_user(file_to_open)