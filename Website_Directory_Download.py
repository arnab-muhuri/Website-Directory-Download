"""
Created on 4th March 2022 by Arnab Muhuri PhD, Université de Sherbrooke
Email: arnab.muhuri@usherbrooke.ca
This code downloads the files in respective folders for an entire directory tree for a given website.
"""
from bs4 import BeautifulSoup
import requests
import urllib.request
from pathlib import Path
import winreg
import wget 
import os
import ssl 
ssl._create_default_https_context = ssl._create_unverified_context
delimiter = chr(92) 

url = 'https://donnees-data.asc-csa.gc.ca/users/OpenData_DonneesOuvertes/pub/RCM/Antarctica/' # your link here

def get_download_path():
    if os.name == 'nt':
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return os.path.join(os.path.expanduser('~'), 'downloads')

def RecurseLinks(base):
    f = urllib.request.urlopen(base)
    soup = BeautifulSoup(f.read())
    for anchor in soup.find_all('a'):
        href = anchor.get('href')
        if (href.startswith('/')):
            
            print (' ')
        elif (href.endswith('/')):
            
            RecurseLinks(base + href) 
        else:
             
            fil_bin.append(base + href)

fil_bin = []
RecurseLinks(url)

filt_lis = []
for lisfil in range(len(fil_bin)):
    if 'C=' not in fil_bin[lisfil]:
        filt_lis.append(fil_bin[lisfil])
    

dfg = filt_lis 
new_list = [s.replace('https://donnees-data.asc-csa.gc.ca/users/OpenData_DonneesOuvertes/pub/', "") for s in dfg] # modify here as per your link
new_list1 = [s.replace('/*.*', "") for s in new_list] 
dir_cre_lis = []
for dir_lin in range(len(new_list1)):
    temp_dir = new_list1[dir_lin][:new_list1[dir_lin].rfind('/')] 
    dir_cre_lis.append(temp_dir) 
    pathtest = Path(get_download_path() + delimiter + temp_dir)
    pathtest.mkdir(parents=True, exist_ok=True) 


for dwn_lis in range(len(dir_cre_lis)):
    output_directory = get_download_path() + delimiter + dir_cre_lis[dwn_lis]
    filename = wget.download(filt_lis[dwn_lis], out=output_directory) 