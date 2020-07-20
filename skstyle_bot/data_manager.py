import json
import os

def read_data_from_user():
    login, password, email, domain, bot_email, bot_email_pw = input("Your login: "),input("Your password: "), input("Your email: "), input("Your domain: "), input("Your bot's email: "), input("Your bot's email's password: ")
    with open("secrets.json","w") as f:
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
    if(os.path.isfile("secrets.json")):
        with open("secrets.json" , "r") as f:
            data = json.load(f)
            return data.get("login"),data.get("password"),data.get("email"),data.get("domain"),data.get("bot_email"),data.get("bot_email_pw")
    else:
        return read_data_from_user()

def change_data():
    read_data_from_user()