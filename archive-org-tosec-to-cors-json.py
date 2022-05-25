import json
import requests
from bs4 import BeautifulSoup

version = "CORSFILEv1"
url = "https://ia801604.us.archive.org/view_archive.php?archive=/25/items/Commodore_Amiga_TOSEC_2012_04_10/Commodore_Amiga_TOSEC_2012_04_10.zip"
root_exp = "//archive.org/download/Commodore_Amiga_TOSEC_2012_04_10/Commodore_Amiga_TOSEC_2012_04_10.zip"
root_uri = "http://archive.org/download/Commodore_Amiga_TOSEC_2012_04_10/Commodore_Amiga_TOSEC_2012_04_10.zip"
file_name = "Commodore_Amiga_TOSEC_2012_04_10"
name = "TOSEC: Commodore Amiga (2012-04-10)"
filter = "" #for example, filter = "Demos"

base_list = []
disks = []

r = requests.get(url)
soup = BeautifulSoup(r.content, 'html5lib') 
table = soup.find('table', attrs = {'class':'archext'}) 
links = table.findAll('a', href=True)

for row in links:
    html = row
    name = row.text
    display_name = name.split("/")[-1]
    href = row['href']
    href = href.replace(root_exp, '')
    base = href.rpartition("%2F")
    rest = base[2]
    base = base[0] + base[1]
    if filter in base:
        if base not in base_list:
            print(base)
            base_list.append(base)
        base_index = base_list.index(base)
        disk = (display_name, base_index, rest)
        disks.append(disk)

data = {"version": version, "name": name, "root": root_uri, "bases": base_list, "items":disks}

json_out = json.dumps(data)

file_out = open(file_name + ".json", "w")
file_out.write(json_out)
file_out.close()