from bs4 import BeautifulSoup
import requests
import threading
import logging
import time
import chilkat
import glob, os
import chilkat
import json
import pandas as pd
from datetime import datetime
from six.moves.html_parser import HTMLParser
data=""
path=r"C:\Users\Avraham Harrar\Desktop\תרגילים עבודה\ex_1"
def a_contain_b(a,b):
    try:
        a.index(b)
    except ValueError:
        return False
    else:
        return True
class Airflight:
    def __init__(self,name,numflight,flight_from,flight_time,final_time,local_terminal,status):
        self.name=name
        self.numflight=numflight
        self.flight_from=flight_from
        self.flight_time=flight_time
        self.final_time=final_time
        self.local_terminal=local_terminal
        self.status=status
    def convert_air_to_json(self,name):
        val="fly"+str(name)
        data={
        "name"+str(i): self.name,
        "numflight"+str(i): self.numflight,
        "flight_from"+str(i):self.flight_from,
        "flight_time"+str(i):self.flight_time,
        "final_time"+str(i):self.final_time,
        "local_terminal"+str(i):self.local_terminal,
        "status"+str(i):self.status
        }
        return data
class Search_in_file():#that class make the search in the files
    def __init__(self,name_file):
        self.name_file=name_file
    def search_by_colums_name(self,column_name,search):#that fooncation get search name and column name and search in file 
        s=""
      
        with open(self.name_file) as f:
            s = " ".join([x.strip() for x in f]) #read from json file
        sb = chilkat.CkStringBuilder()
        sb.Append(s)
        #print(sb.getAsString())
        sb.Decode("json","utf-8")
        sb.Encode("json","utf-8")#decode the file
        #print(sb.getAsString())
        sb.Decode("json","utf-8")
        new_file=sb.getAsString()#fixer the file 
        new_file=new_file.replace(r"}{",",") 
        new_file=new_file.replace(r"{","")
        new_file=new_file.replace(r"}","")
        #print(new_file)
        liststrin=new_file.split(r",")#give as the data like column:datacolumn
        temp=[]
        for x in liststrin:
            temp=x.split(":")
            #print(a_contain_b(str(temp[0]),column_name))
            a_contain_b(str(temp[1]),search)
            if a_contain_b(str(temp[0]),column_name)and a_contain_b(str(temp[1]),search):
                print("#########")
        print("bye")

    	

class Trans_to_json_file:#get list of Airflight and convert them into file name
    def __init__(self, lsit_fli):
        self.lsit_fli=lsit_fli
        self.list_json=[]
    def create_json(self):
        count=0
        for i in self.lsit_fli:
            count+=1
            self.list_json.append(i.convert_air_to_json(count))
    def create_file_json(self,name_of_file):#convert list_json to file
        if(self.list_json==[]):
            return
        with open(name_of_file, "w") as write_file:
            for x in self.list_json:
                json.dump(x, write_file)
def get_data():
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0",
                   "Accept-Encoding":"gzip, deflate", "Accept":"application/json, text/javascript, */*; q=0.01",
                   "Cookie":"visid_incap_1276841=lpVRaqyMRJC2ZimbbSR3MCtuOV8AAAAAQ0IPAAAAAACA9lCWAZPsnDfWIRl3aS3m4eDDK8+Bka25; __utma=232678535.1057472770.1597599283.1597784934.1597791848.12; __utmz=232678535.1597599283.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); incap_ses_7213_1276841=HKkABtqeWhgypsieZLkZZJs7PF8AAAAAFLLfhw9y9/F4L5D8B9iYjg==; TS01512257=010f83961df117e3f219051907e569a3635b4632d0e41eed553d6ebfcff91d397de4e222716fe8b70cf0a782ae56931138dac17add; WSS_FullScreenMode=false; __utmc=232678535; __utmb=232678535.1.10.1597791848; __utmt=1"
                  ,"X-Requested-With": "XMLHttpRequest"
    }
    toreturns=[]
    URL='https://www.iaa.gov.il/he-IL/airports/BenGurion/_layouts/15/IAAWebSite/WS/FlightsUtils.asmx/LoadTable'
    name=""
    localcounter=1
    flight_from=""
    parms= { "josnFlightTableSettings": '{"Mode":"1","PageIndex":1,"SortExpression":"","SortDirection":"0","ItemsLimit":25,"ErrorMessage":"","PagerView":true,"FullWidth":true}',"airportId": "LLBG"  }
    rb = requests.post(URL, headers=headers,data=parms)#, proxies=proxies)
    htmlfile=BeautifulSoup(rb.text,features="lxml")#conver json file to html
    content = rb.content
    soup = BeautifulSoup(htmlfile.text,'html.parser')
    htmltable=soup.table
    soup1 =BeautifulSoup(str(htmltable),'html.parser')
    for column in soup1.find_all('tr'):
        tempx=column.find('td', attrs={'class':'flightIcons'})
        tempy =BeautifulSoup(str(tempx),'lxml')
        for d in tempy.find_all('a'):
            tempz =BeautifulSoup(str(d), 'lxml')
            for x in tempz.find_all('img'):
                name=x.get('alt')#name of company
     #   print("############")
      #  print(name)
       # print("############")
        tempx=column.find('td', attrs={'class':'FlightNum'})
        tempy =BeautifulSoup(str(tempx),'lxml')
        numflight=tempy.text#find the number flight
       # print("############")
        #print(numflight)     
       # print("############")
        tempx=column.find('td', attrs={'class':'FlightFrom'})
        tempy =BeautifulSoup(str(tempx), 'lxml')
        for x in tempy.find_all('span'):
            soup3=BeautifulSoup(str(x), 'lxml')
            flight_from=soup3.text#find flight from
       # print("############")    
       # print(flight_from)
      #  print("############")
        tempx=column.find('td', attrs={'class':'FlightTime'})
        tempy=BeautifulSoup(str(tempx), 'lxml')
        flight_time=tempy.text#find the flighttime
       # print("############")
      #  print(flight_time)
       # print("############")
        tempx=column.find('td', attrs={'class':'finalTime'})
        tempy=BeautifulSoup(str(tempx), 'lxml')
        final_time=tempy.text#find the finaltime
      #  print("############")
    #    print(final_time)
    #    print("############")
        tempx=column.find('td', attrs={'class':'localTerminal'})
        tempy=BeautifulSoup(str(tempx), 'lxml')
        local_terminal=tempy.text#find the localterminal
        tempx=column.find('td', attrs={'class':'status'})
        tempy=BeautifulSoup(str(tempx), 'lxml')
        status=tempy.text#find the localterminal
        #print("  "+name+"  "+numflight+"  "+flight_from+"  "+flight_time+"  "+final_time+"   "+local_terminal+"   " +status)
        if localcounter!=1:
            toreturn=Airflight(name,numflight,flight_from,flight_time,final_time,local_terminal,status)
            toreturns.append(toreturn)
        localcounter+=1
    return toreturns
def careate_the_data_and_make_files():
    print("get data thread")
    while True:
        logging.info("Thread get_data: starting")
        l=get_data()
        t=Trans_to_json_file(l)
        t.create_json()
        filename=str(time.time())+".json"
        t.create_file_json(filename)
        logging.info("Thread get_data: finishing")
        time.sleep(3000)

def search_in_files(colums,search):
    print("here")
    for file in glob.glob("*.json"):
        x=str(file)
        print(file)
        temp=Search_in_file(x)
        temp.search_by_colums_name("numflight","UA 084")


def main():
    colums=input("enter your column")
    search=input("enter your search")
    global path
    os.chdir(path)#insert dirctory place
    x = threading.Thread(target=careate_the_data_and_make_files) 
    x.start()
    y= threading.Thread(target=search_in_files,args=(colums,search))
    y.start()     
    x.join()
    y.join()
    logging.info("main thread")






if __name__ == "__main__":
    main()
