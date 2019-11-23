import requests
from bs4 import BeautifulSoup, Comment
import json
import re
url_main = 'http://www.kuet.ac.bd/index.php/welcome/transportation'

def download_data():
    try:
        page = requests.get(url_main)
        f = open("bus.html","w+")
        x = str((page.content))
        f.write(x)
        f.close()
        return
    except requests.exceptions.Timeout: #server down
        return
    except requests.exceptions.ConnectionError: #no internet
        return
def get_soup():
    download_data()
    f = open('bus.html', 'r',encoding='utf-8')
    soup = BeautifulSoup(f, 'html5lib')
    f.close()
    return soup

def get_data():
    soup = get_soup()
    fx = soup.find(class_='transport')
    table_header = fx.findAll('thead')
    table_data = fx.findAll('tbody')
    cnt =0
    full_data = []
    vehichle_arr = []
    phone_num_arr = []
    header_now = []
    for i in range(5):
        nowhead = table_header[i].findAll('th')
        header_now.clear()
        #get header names
        for j in nowhead:
            strtmp = j.text.replace("&","")
            strtmp = strtmp.replace(" ","")
            header_now.append(strtmp)
        #get table data
        table_row = table_data[i].findAll('tr') #all row in this table
        for j in table_row:
            row_data = j.findAll('td') #all data in this row
            if(len(row_data) == 4):
                print("Vehichle")
                vehichle_obj = {
                    header_now[0]: row_data[0].text.strip(),
                    header_now[1]: row_data[1].text.strip(),
                    header_now[2]: row_data[2].text.strip(),
                    header_now[3]: row_data[3].text.strip(),
                }
                vehichle_arr.append(vehichle_obj)
            elif(len(row_data) == 3):
                print("Phone Number")
                phone_num_obj = {
                    header_now[1]: row_data[1].text.strip(),
                    header_now[2]: row_data[2].text.strip(),
                }
                phone_num_arr.append(phone_num_obj)
    full_data.append({"bus":vehichle_arr})
    full_data.append({"phone":phone_num_arr})
    return full_data

def write_data(s="data.json"):
    f = open(s, 'w')
    fd = get_data()
    json.dump(fd, f)
    f.close()
