
# coding: utf-8

# In[ ]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
import itertools
import requests
import time
import csv
from flatten_json import flatten
import os
import re
import json


# In[ ]:


def ExtractForQuery(file):
        #mon_fichier = open(file,"r")
        mon_fichier=open(file, encoding="utf8")
        soup = BeautifulSoup(mon_fichier, 'html.parser')
            ## extraction des liens des profile linkedin 
        true_link =[] 
        link_out =[] 
        url_list = [] 
        body = soup.body
        profil_h = body.find_all('h3') 
        for h in profil_h: 
                linkList = h.find_all('a') 
                for link in linkList: 
                        true_link.append(str(link.get('href')));

        ## changement des url pour utiliser www.linkedin.com
        for link in true_link:
            posfinal=link.find('&');
            if link[15:17]!="ww":
                link_out.append(link[7:posfinal].replace(link[15:17], "www")) 
            else:
                link_out.append(link[7:posfinal]);
        ## connexion à un profile linkedin pour que je puisse visualiser le contenu d'un profile importer par google
        client = requests.Session()
        HOMEPAGE_URL = 'https://www.linkedin.com'
        LOGIN_URL = 'https://www.linkedin.com/uas/login-submit'
        html = client.get(HOMEPAGE_URL).content
        soup1 = BeautifulSoup(html,'html.parser')
        csrf = soup1.find(id="loginCsrfParam-login")['value']
        login_information1 = {
            'session_key':'dorsaf.ep.selmi@gmail.com',
            'session_password':'dorsaf2017',
            'loginCsrfParam': csrf,
        }
        login_information2 = {
            'session_key':'script-linkedin@outlook.com',
            'session_password':'script123',
            'loginCsrfParam': csrf,
        }
        login_information3 = {
            'session_key':'medamineyahiaouii@gmail.com',
            'session_password':'medamine',
            'loginCsrfParam': csrf,
        }
        login_information4 = {
            'session_key':'sourour.kachoukh@gmail.com',
            'session_password':'sourour1',
            'loginCsrfParam': csrf,
        }
        login_information5 = {
            'session_key':'jamilayaakoubi6@gmail.com',
            'session_password':'jamila123456@31@',
            'loginCsrfParam': csrf,
        }
        
        #client.post(LOGIN_URL, data=login_information)
        try:
            client.post(LOGIN_URL, data=login_information1)
        except Exception as e2:
            client.post(LOGIN_URL, data=login_information2)
        except Exception as e3:
            client.post(LOGIN_URL, data=login_information3)
        except Exception as e4:
            client.post(LOGIN_URL, data=login_information4)
        except Exception as e5:
            client.post(LOGIN_URL, data=login_information5)
        headers = {'Accept-Encoding': 'identity'}
        
        ##parcour de la liste des profiles et extraction de ses informations vers un csv 
        for link_profile in link_out: 
            summary = ' '
            headline = ' '
            firstName = ' '
            lastName = ' '
            occupation = ' '
            locationName = ' '
            email = ' '
            print(link_profile)
            profile_url = client.get(link_profile, headers=headers)
            t0 = time.time()
            print(profile_url.status_code)
            if profile_url.status_code == 200:
                soup = BeautifulSoup(profile_url.content, 'html.parser')
                
                codes = soup.find_all("code")
                for code in codes:
                    if '{"data":{"patentView"' in code.text :
                            profile_code = code.text
                            Profile_inf = json.loads(profile_code.encode("utf-8"))
                            flatFirstInf= flatten(Profile_inf)
                            ## recuperation des informations d'un profile
                            for key in flatFirstInf:
                                if '_firstName' in key :
                                     firstName = flatFirstInf[key]
                                if '_lastName' in key :
                                      lastName = flatFirstInf[key]
                                if '_occupation' in key :
                                     occupation = flatFirstInf[key] 
                                if '_locationName' in key :
                                     locationName = flatFirstInf[key]
                                if '_headline' in key :
                                     headline = flatFirstInf[key]  
                                if 'summary' in key :
                                      summary =  flatFirstInf[key]  
                                #recuperation d'une adresse email soit à partir de resumé ou de son headline
                                match1 = re.search(r'[\w\.-]+@[a-z0-9._-]+\.[a-z]+', summary)
                                if  match1 != None:
                                     email = match1.group(0)
                                match2 = re.search(r'[\w\.-]+@[a-z0-9._-]+\.[a-z]+', headline)
                                if match2 != None:
                                      email = match2.group(0)
             ## sauvgarde des donnees extraites 
            with open("extract_information_profile.csv", "a",encoding='utf-8') as f_write:
                writer = csv.writer(f_write, delimiter=";")
                tableau = [[link_profile, firstName, lastName,occupation,locationName,headline,summary,email]]
                writer.writerows(tableau)

               #response_delay = time.time() - t0
               # time.sleep(10*response_delay) 
                time.sleep(20)
        return;


# In[ ]:


df_LinkedIn=pd.read_excel("LinkedIn.xlsx","Profiles")
df_Keywords=pd.read_excel("LinkedIn.xlsx","Keywds",header=None)
df_GRADE=pd.read_excel("LinkedIn.xlsx","Grade",header=None)


# In[ ]:


lL=(df_LinkedIn.iloc[:,1]).tolist()
lK=(df_Keywords.iloc[:,0]).tolist()
lG=(df_GRADE.iloc[:,0]).tolist()
listAll=itertools.product(lL,lK,lG)


# In[ ]:


with open("extract_information_profile.csv", "a",encoding='utf-8') as f_write:
    writer = csv.writer(f_write, delimiter=";")
    tableau = [["URL profile", "firstName", "lastName","occupation","location","headline","summary","email"]]
    writer.writerows(tableau)
for item in listAll:
   # print(element)
        var1 = str(item).replace("'","")
        var2 = var1.replace("(","")
        var3 = var2.replace(")","")
        var4 = var3.replace(" ","")
        var5 = var4.split(",")
       # print(var5[0])
       #print(var5[1])
       #print(var5[2])
       ##ajout boucle for pour pagination de resultat de google
        nbprofile = 0
        for count in range(0,50):
            time.sleep(20);
            tabUrl="https://www.google.tn/search?q=site%3A"   
            termURL=var5[0]+"+inurl%3Apub+OR+inurl%3Ain+-dir+"+var5[1]+"+"+var5[2]+"+gmail.com+OR+gmail.fr+OR+hotmail.com+OR+hotmail.fr+OR+yahoo.fr+OR+outlook.com+OR+live.fr"
            url=tabUrl+termURL+"\&ei=m3w9WuyXNJHMwALelovwAQ&start="+str(nbprofile)+"&sa=N&biw=848&bih=972" 
            print(url)
            htmlGoogle = requests.get(url)
            #print(htmlGoogle.content)
            page=htmlGoogle.content
           # cont = True
           # while cont==True:
           #     if "CAPTCHA" in str(page):
                   # resolveRecaptcha(url)
            #        cont = False
          #      else:
             #       cont=True;
            #htmlGoogle = requests.get(url)
            #page = htmlGoogle.content
            
            #
               
            
            f = open("HTMLResult.txt","w", encoding="utf8")
            f.write(str(page))
            f.close()
            ExtractForQuery("HTMLResult.txt")
            nbprofile= nbprofile + 10
            time.sleep(20);

