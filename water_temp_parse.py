import requests
from bs4 import BeautifulSoup
from datetime import datetime as dt


#info dict
location_infos = {'Cospudener See' : 'http://www.wassertemperatur.org/cospudener-see/',
                  'Kulkewitzer See' : 'http://www.wassertemperatur.org/kulkwitzer-see/',
                  'Mueritz' : 'http://www.wassertemperatur.org/mueritz/',
                  'Kuehlungsborn' : 'http://www.wassertemperatur.org/ostsee/kuehlungsborn/',
                  'Prerow' : 'http://www.wassertemperatur.org/ostsee/prerow/',
                  'Fehmarn' : 'http://www.wassertemperatur.org/ostsee/fehmarn/',
                  'Kohlberg' : 'http://www.wassertemperatur.org/ostsee/kolberg/',
                  'Wannsee' : 'http://www.wassertemperatur.org/wannsee/',
                  'Mirower See' : 'http://www.wassertemperatur.org/deutschland/mecklenburg-vorpommern/mirower-see/',
                  'Plauer See' : 'http://www.wassertemperatur.org/plauer-see/',
                  'Schweriner See' : 'http://www.wassertemperatur.org/schweriner-see/',
                  }

#path to archive file
file = 'd://coding//data_sets//water//temp_archive.csv'


def get_temp(url: str)-> list:
    #load page
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    #extract location and temp
    s = str(soup.find('h2'))
    location = s[s.find('>')+1:s.find('<',s.find('>'))]
    s = s[s.find('<',s.find('>'))+1:]
    temp = s[s.find('>')+1:s.find('<')]

    #extracct temp: divide in substrings, select (first) digit (10°C) 
    temp = [int(substr) for substr in temp.split() if substr.isdigit()][0]
    
    return [location.strip(), temp]


def write_results(file: str, location: str, temp: int):
    with open(file, 'a') as f:
        f.write(f'{dt.today().date()} , {location} , {temp}\n')
    return


def check_last_entry(file: str)->bool:
    #read file and check last entry
    try:
        with open(file) as f:
            try:
                lastline = list(f)[-1]
            except:
                print('file is empty')
                write_update = True
            else:
                last_entry_date = dt.strptime(lastline.split(',')[0].strip(),
                                              '%Y-%m-%d'
                                              ).date()
                write_update = last_entry_date != dt.today().date()
                print(f'last entry {last_entry_date}, '
                      f'write update {write_update}')

    except:
        print('file not found, write update')
        write_update = True

    return write_update


if __name__ == '__main__':
    write_update = check_last_entry(file)

    #iterate through all locations
    for location, url in location_infos.items():
        message, temp = get_temp(url)
        if write_update:
            write_results(file, location, temp)
        print(f'{message} {temp} °C')
