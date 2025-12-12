import re
import subprocess
import os

class Domain:
    path_bind="/etc/bind/zones/db.icodevn.net"
    main_domain="icodevn"
    dict_record={}
    pattern = re.compile(r"^([@\w\-.]+)\s+IN\s+([A-Z]+)\s+([^\s;]+)")

    def __init__(self):
        if not os.path.exists(self.path_bind):
            print("file did not exsits")
        print("Domain initialized")
    
    def add_record(self,subdomain, record_type,value):
        try:
            if subdomain in self.dict_record:
                raise Exception("subdomain already exists") 
            with open(self.path_bind, "a") as file:
                file.write(f"{subdomain} IN {record_type} {value}\n")
            self.dict_record[subdomain] = value
            self.updateLineDigit()
            subprocess.run(["systemctl", "restart", "bind9"], check=False)
        except Exception as e:
            raise Exception(e)
    def updateLineDigit(self):
        with open(self.path_bind, "r") as file:
            lines = file.readlines()
            
        for idx,line in enumerate(lines):
            if "Serial" in line:
                match = re.search(r'(\d+)', line)
                if match:
                    serial_number = match.group(1)
                    new_serial = str(int(serial_number) + 1)
                    lines[idx]=line.replace(serial_number, new_serial)
                    break
        with open(self.path_bind, "w") as file:
            file.writelines(lines)
                

    def delete_record(self,subdomain):
        try:
            if subdomain not in self.dict_record:
               raise Exception("subdomain not found")
            with open(self.path_bind,"r") as file:
                lines = file.readlines()
            with open(self.path_bind,"w") as file:
                for line in lines:
                    if subdomain not in line:
                        file.write(line)
            self.updateLineDigit()
            subprocess.run(["systemctl","reload","bind9"],check=False)
        except Exception as e:
            raise Exception(e)
    def getListReCord(self):
        try:
            with open(self.path_bind, "r") as file:
                print("File mode:", file.mode)
                for line in file:
                    line =line.strip()
                    if not line or line.startswith(";") or line.startswith("$"):
                        continue    
                    match  =self.pattern.match(line)
                    if match:
                        name,r_type,ip=match.groups()
                        if name =="@" and r_type =="NS":
                            continue
                        if name =="@":
                            self.dict_record[self.main_domain]=ip
                        self.dict_record[name]=ip
            print("Loaded records:", self.dict_record)
        except Exception as e:
            print(f"Error reading file: {str(e)}")
            
        
        
            
        