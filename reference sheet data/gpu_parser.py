import csv
from bs4 import BeautifulSoup

INPUT_FILE = "gpu_benchmark.txt"
OUTPUT_FILE = "gpu_passmark.csv"

def convert(x):
    return int(x.replace(",",""))

# ---------- Read HTML ----------
with open(INPUT_FILE, "r", encoding="utf-8", errors="ignore") as f:
    html = f.read()


# ---------- Extract JavaScript ----------
soup = BeautifulSoup(html, "html.parser")

gpu_dat={}
for li in soup.find_all("li"):
    name_tag=li.find("span",class_="prdname")
    no_tag=li.find("span",class_="count")
    if name_tag and no_tag:
        name=name_tag.get_text()
        no=convert(no_tag.get_text())
        #gpu_dat[name]=convert(no)

        with open("gpu_data.csv","a",newline="",encoding="utf-8") as f:
            writer=csv.writer(f)
            writer.writerow([name,no])
        
    #gpu_dat[str(li.find("span",class_="prdname").get_text())]=convert(li.find("span",class_="count").get_text())
        print(name)

