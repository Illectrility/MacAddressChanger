import re
import os
import time
import json
import random

# declaring all variables
macDatabase = []
pinnedMacs = []
macNotes = {}
interfaces = os.listdir("/sys/class/net/")  # path to interfaces
interface = ""  # if I don't declare this variable here, I get an error
mac = ""


def mac_input_check(address):
    if re.match(r'[a-zA-Z0-9]{2}:[a-zA-Z0-9]{2}:[a-zA-Z0-9]{2}:[a-zA-Z0-9]{2}:'
                r'[a-zA-Z0-9]{2}:[a-zA-Z0-9]{2}$', address):
        return True
    else:
        return False


def database_read():
    global macDatabase
    global pinnedMacs
    global macNotes
    # flushing the values, just to be safe
    macDatabase = []
    pinnedMacs = []
    with open(r'mac_database.txt', 'r') as dataBaseFile:
        try:
            for line in dataBaseFile:
                macDatabase.append(line)
            print("Successfully read the Database")
        except ValueError:
            print("Reading the Database was unsuccessful")
    with open(r'pinned_macs.txt', 'r') as pinnedMacsFile:
        try:
            for line in pinnedMacsFile:
                pinnedMacs.append(line)
            print("Successfully read pinned MACs")
        except ValueError:
            print("Reading the pinned MACs was unsuccessful")
    with open('mac_notes.json', 'r') as macNotesFile:
        mac_notes_data = macNotesFile.read()
        macNotes = json.loads(mac_notes_data)


def database_add():
    with open(r'mac_database.txt', 'a') as dataBaseFile:
        while True:
            userinput = input("Please input MAC (xx:xx:xx:xx:xx:xx): ")
            if mac_input_check(userinput):
                dataBaseFile.write(userinput + "\n")
                note_add(userinput)
                note_save()
                database_read()
            else:
                print("That was not a valid MAC address :/")
                time.sleep(1)
            break


def pin_add():
    with open(r'pinned_macs.txt', 'a') as pinnedMacsFile:
        while True:
            userinput = input("Please input MAC (xx:xx:xx:xx:xx:xx): ")
            if mac_input_check(userinput):
                pinnedMacsFile.write(userinput + "\n")
                note_add(userinput)
                note_save()
                database_read()
            else:
                print("That was not a valid MAC address :/")
                time.sleep(1)
            break


def note_save():
    with open('mac_notes.json', 'w') as macNotesFile:
        json.dump(macNotes, macNotesFile)


def note_add(address):
    global macNotes
    while True:
        u_in = input("Would you like to add a note for " + address + "? Y/n")
        if u_in.lower() == "y":
            if address in macNotes:
                print("This MAC already has a note attached to it: " + macNotes[address] + ". This will overwrite!")
            note = input("Please attach a note: ")
            u_in = input("Is '" + note + "' correct? Y/n")
            if u_in.lower() == "y":
                macNotes[address] = note
                break
            elif u_in.lower() == "n":
                pass
            else:
                print("Whoops, something went wrong")
                pass
        elif u_in.lower() == "n":
            break
        else:
            print("Whoops, something went wrong.")


def mac_change():
    global interfaces
    global interface
    global mac
    while True:
        print("Which interface would you like to change?")
        for i in range(0, len(interfaces)):
            print(str(i + 1) + ". " + interfaces[i])
        userinput = input("")
        try:
            interface = interfaces[int(userinput) - 1]
            break
        except IndexError:
            print("That didn't work :/ Try again.")

    while True:
        print("=-=-=-=-=\nWhat kind of MAC do you want?")
        userinput = input("1. Custom MAC 2. Random MAC from Database 3. Pinned MAC\n")
        if userinput == "1":
            print("Please input a MAC (xx:xx:xx:xx:xx:xx)")
            userinput = input("")
            if mac_input_check(userinput):
                mac = userinput
                break
            else:
                print("That was not a valid MAC address :/")
                time.sleep(1)
                pass
        elif userinput == "2":
            mac = macDatabase[random.randint(0, len(macDatabase) - 1)]
            print("Your random MAC is: " + mac)
            if mac in macNotes:
                print("Note: " + macNotes[mac])
            break
        elif userinput == "3":
            print("PINNED MACS")
            for i in range(0, len(pinnedMacs)):
                temp_mac = pinnedMacs[i]
                print(str(i) + ". " + temp_mac)
                if temp_mac in macNotes:
                    print("Note: " + macNotes[temp_mac])
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


def main_menu():
    print("=-=-=-=-=")
    userinput = input("What would you like to do?\n1. Change MAC Address\n2. Add MAC to Database\n3. Pin a MAC\n"
                      "4. Save\n5. Quit\n")
    if userinput == "1":
        mac_change()
    elif userinput == "2":
        database_add()
    elif userinput == "3":
        pin_add()
    elif userinput == "4":
        note_save()
    elif userinput == "5":
        quit()


print("Version 1.12")

database_read()
while True:
    main_menu()

# illectrility
