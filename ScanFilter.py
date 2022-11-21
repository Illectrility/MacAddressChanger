import re
import os

mac_addresses = []
file_list = []
mac_file = ""
file_name = ""
destination_file_name = ""


def read_directory():
    global file_list
    file_list = os.listdir()


def read_file():
    global file_name
    global mac_file
    with open(file_name, "r") as file:
        mac_file = file.read()


def save_file():
    global destination_file_name
    with open(destination_file_name, "w") as file:
        for mac in mac_addresses:
            file.write(mac + "\n")


def file_filter():
    global mac_file
    mac_file = mac_file.split()
    for index in mac_file:
        if re.match(r'[a-zA-Z0-9]{2}:[a-zA-Z0-9]{2}:[a-zA-Z0-9]{2}:[a-zA-Z0-9]{2}:[a-zA-Z0-9]{2}:'
                    r'[a-zA-Z0-9]{2}$', index):
            mac_addresses.append(index)
        else:
            pass
    print("The file '" + destination_file_name + "' should now contain a list of MACs that you can paste into the "
                                                 "database of the MAC-Changer.")


def main_menu():
    global destination_file_name
    global file_name
    u_in = input("What would you like to do? 1. Filter a new file 2. Quit\n")
    if u_in == "1":
        u_in = input("How would you like to select the file? 1. Enter file name 2. List directory\n")
        if u_in == "1":
            file_name = input("Please enter the file name: ")
        elif u_in == "2":
            for index in range(0, len(file_list)):
                print(str(index) + ". " + file_list[index])
            u_in = input("Put in the number of the file you would like to select: ")
            try:
                file_name = file_list[int(u_in)]
                u_in = input("What would you like to name the destination file? 1. Custom 2. Add 'filtered_'\n"
                             " (If you press Enter, the file will be named automatically)\n")
                if u_in == "1":
                    destination_file_name = input("Enter destination file name: ")
                elif u_in == "2":
                    destination_file_name = "filtered_" + file_name
                else:
                    destination_file_name = "arp-scan-filter-export.txt"
                read_file()
                file_filter()
                save_file()
            except ValueError:
                print("Whoops, something went wrong")
                pass
    if u_in == "2":
        quit()
    else:
        pass


read_directory()

print("Version 1.0")

while True:
    print("This program is built for command line outputs from arp-scan.\nIt works by looking through the file"
          " and saving every piece of data that matches the formatting of a MAC. It therefore should work with"
          " Nmap and similar tools, too.")
    main_menu()
