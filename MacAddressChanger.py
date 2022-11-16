import os
import random
import time

# declaring all variables
macDatabase = []
pinnedMacs = []
interfaces = os.listdir("/sys/class/net/")  # path to interfaces
interface = ""
uIn = ""
mac = ""


def database_read():
    with open(r'mac_database.txt', 'r') as dataBaseFile:
        try:
            for line in dataBaseFile:
                x = line[:-1]
                macDatabase.append(x)
            print("Successfully read the Database")
        except ValueError:
            print("Reading the Database was unsuccessful")
    with open(r'pinned_macs.txt', 'r') as pinnedMacsFile:
        try:
            for line in pinnedMacsFile:
                x = line[:-1]
                pinnedMacs.append(x)
            print("Successfully read pinned MACs")
        except ValueError:
            print("Reading the pinned MACs was unsuccessful")


def database_add():

    with open(r'mac_database.txt', 'a') as dataBaseFile:
        try:
            dataBaseFile.write("\n" + str(input("Please input MAC: ")))
        except ValueError:
            print("Could not add MAC to Database")


def pin_add():
    with open(r'pinned_macs.txt', 'a') as pinnedMacsFile:
        try:
            pinnedMacsFile.write("\n" + str(input("Please input MAC: ")))
        except ValueError:
            print("Could not add MAC to Pins")


def mac_change():
    global uIn
    global interface
    global mac
    while True:
        print("Which interface would you like to change?")
        for i in range(0, len(interfaces)):
            print(str(i + 1) + ". " + interfaces[i])
        uIn = input("")
        try:
            interface = interfaces[int(uIn) - 1]
            break
        except IndexError or ValueError:
            pass

    while True:
        print("What kind of MAC do you want?")
        uIn = input("1. Custom MAC 2. Random MAC from Database 3. Pinned MAC\n")
        if uIn == "1":
            print("Please input a MAC (xx:xx:xx:xx:xx:xx)")
            mac = input("")
            break
        elif uIn == "2":
            mac = macDatabase[random.randint(0, len(macDatabase) - 1)]
            print("Your random MAC is: " + mac)
            break
        elif uIn == "3":
            print("PINNED MACS")
            for i in range(0, len(pinnedMacs)):
                print(str(i) + ". " + pinnedMacs[i])
            userinput = input("Please input number of desired MAC: ")
            mac = pinnedMacs[int(userinput)]
            break
        else:
            pass

    print("Attempting to change MAC address of " + interface + " to " + mac)
    os.system("sudo ip link set dev " + interface + " down")
    time.sleep(1)
    os.system("sudo ip link set " + interface + " address " + mac)
    time.sleep(1)
    os.system("sudo ip link set dev " + interface + " up")
    input("If you did not see any error messages, your attempt"
          " at changing your MAC was probably successful! Press Enter")
    print("=-=-=-=-=")


def main_menu():
    userinput = input("What would you like to do?\n1. Change MAC Address\n2. Add MAC to Database\n3. Pin a MAC\n"
                      "4. Quit\n")
    if userinput == "1":
        mac_change()
    elif userinput == "2":
        database_add()
    elif userinput == "3":
        pin_add()
    elif userinput == "4":
        quit()


# This is where the program actually starts
database_read()
while True:
    main_menu()

# illectrility
