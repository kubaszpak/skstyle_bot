# skstyle_bot
Python Bot for sstore domain webshops admin panel

---
**Version 1.0.5**
---
It works on sstore version 4.9.3

## Purpose

Its main feature is storaging new orders in a file and every couple of hours sending an email with new clients' address stickers to put directly on a package

## Usage

To run: 

 - for now you need poetry as it is not a built package yet. You can install it with:

    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

 - download and add a chrome webdriver to your path

There is a great tutorial for that I found on YouTube (again if you are using Windows, on Mac you just have to unpack it and move it to !usr/local/bin):

https://www.youtube.com/watch?v=dz59GsdvUF8&t=1s

 - clone it into a directory and open cmd at it

 - you can also download this project with **pip install skstyle-bot==0.1.1** and use with importlib
   (sb = importlib.import_module("skstyle-bot") and sb.main())

 - run **poetry install --no-dev** 

 When you run it for the first time the program will ask you for your data and store it in secrets.json
 Every next time the program will read data from this file

 - run project with **poetry run main**

 If you have misspelled something you can change the data with

 - **poetry run set_data**

---
## Description
Running the program for the first time creates a new file called lastorder.txt and exits
Every next usage it will do the same but also if it detects that any new orders have been added to the list
it will email you the data of them such as clients information and shipment information
