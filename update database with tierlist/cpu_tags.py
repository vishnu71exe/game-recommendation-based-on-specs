import csv

count=0
cpu={} #full data from reference sheet
with open("data/cpu_data.csv","r",encoding="utf-8") as f:
    reader=csv.reader(f)
    
    for lines in reader:
        cpu[lines[0]]=lines[1]
        count+=1

with open("cpu_data_tagged.csv","a",encoding="utf-8",newline="") as f1:
    writer=csv.writer(f1)
    for i,j in cpu.items():
        if "Core i3" in i:
            writer.writerow([i,j,"i3"])
        elif "Core i5" in i:
            writer.writerow([i,j,"i5"])
        elif "Core i7" in i:
            writer.writerow([i,j,"i7"])
        elif "Core i9" in i:
            writer.writerow([i,j,"i9"])
        elif "Ryzen 3" in i:
            writer.writerow([i,j,"R3"])
        elif "Ryzen 5" in i:
            writer.writerow([i,j,"R5"])
        elif "Ryzen 7" in i:
            writer.writerow([i,j,"R7"])
        elif "Ryzen 9" in i:
            writer.writerow([i,j,"R9"])
        else:
            writer.writerow([i,j])   

