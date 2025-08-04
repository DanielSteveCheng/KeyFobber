import pyautogui
from pynput import mouse
import sys
import csv

instructions = []
rooms = {}

csvFile = "TestFile.csv"


def csvParser():
    with open(csvFile, 'r', newline='') as csvfile:
        # Create a csv.reader object
        csv_reader = csv.reader(csvfile)

        header = next(csv_reader)
        
        users = []
        
        for row in csv_reader:
            if row[1] == '':
                row[1] = 'A'
            users.append(row) # Each row is a list of strings
            print(row)

        users = sortRooms(users)
        return users

def on_click(x, y, button, pressed):

    if pressed:  
        print("""\t\t\tMouse clicked at ({x}, {y}) with button: {button}""".format(x=x, y=y, button=button))
        if button == button.middle:
            instructions.append(["Text",x,y])
        elif button == button.left:
            instructions.append(["Click",x,y])
        elif button == button.right:
            return False

    return True

def start_listening():
    instructions.clear()
    print("""
                    Listening for mouse clicks. Press right mouse button to stop.
                    """)
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

def getFileContents(file):

    users = []
    user = [None,None,None,None]  # [Room, Letter, Lastname, Firstname]

    for line in file:
        if line == "\n":
            if None not in user:
                user.append('2026')
                users.append(user)
            user = [None,None,None,None]
            continue
        elif line == "END":
            if None not in user:
                users.append(user)
            break
        
        l = line.split(": ")
        key = l[0]
        field = l[1][:-1]
        if key == "Room":
            user[0] = field
        elif key == "Letter":
            user[1] = field
        elif key == "Lastname":
            user[2] = field
        elif key == "Firstname":
            user[3] = field
        else:
            print("Invalid entry!")
    # print(users)
    users = sortRooms(users)
    # print(users)
    return users

def writeToFile(file, users):
    print("""
                    Updating LeaseData.txt with current user information...""")
    
    try:
        with open(file, 'w', encoding='utf-8') as f:
            for user in users:
                f.write("Room: {}\n".format(user[0]))
                f.write("Letter: {}\n".format(user[1]))
                f.write("Lastname: {}\n".format(user[2]))
                f.write("Firstname: {}\n".format(user[3]))
                f.write("\n")
            f.write("END")
        print("""                
                    LeaseData.txt updated successfully!""")
    except Exception as e:
        print("""
                    Error writing to file: {}""".format(e))
    

def sortRooms(users):
    users.sort(key=lambda x: (x[0],x[1]))  # Sort users by room number
    for i in users:
        rooms[i[0] + i[1]] = users.index(i)
    # print(users)
    writeToFile("LeaseData.txt", users)
    return users

def closeFile(file):
    try:
        file.close()
    except Exception as e:
        print("Error closing file: {}".format(e))
    sys.exit()
    
def printUser(user, ind):
    print("""
                      Entry: {index}
                      Name: {firstname} {lastname}
                      Room: {room}""".format(index=ind + 1, firstname=user[3], lastname=user[2], room=user[0] + user[1]))
    return

if __name__ == "__main__":

    # Start the script
    wait = input("""
                    --------------------------------------
                    
                    Welcome to the Keyfobber!
                    
                    Made by Daniel Cheng for the OneOnCentre Team <3

                    This script will help you automate the process of entering user data.
                 
                    Please follow the instructions below:

                        1. The script will initialize by listening for mouse clicks. It will record the following:
                        - Left Click: Click at the specified coordinates
                        - Middle Click: Type the next word at the specified coordinates. NOTE: Please ensure to left click on the field before clicking the middle button.
                        - Right Click: Stop the recording of mouse clicks

                        In order to properly automate the process, please make sure to click through all necessary buttons/fields in the right order from start to finish.
                    
                        2. After recording the clicks, the script will read the user data from a file named "LeaseData.txt". Please ensure this file is in the same directory as the script.
                    
                        3. The script will then prompt you to either process the next user, view the next user, view the number of users remaining, or exit the script.

                    Good Luck!

                    --------------------------------------

                    Press enter to continue...""")

    # Start listening for mouse clicks
    start_listening()
    print("""
                    Mouse clicks recorded.""")

    file = ""
    try:
        file = open("LeaseData.txt", 'r', encoding='utf-8')
        print("""
                    LeaseData.txt found!""")
    except:
        print("""
                    File not found! Please ensure that LeaseData.txt is in the same directory as this script.
                    Quitting...
              """)
        closeFile(file)

    try:
        file = open(csvFile, 'r', encoding='utf-8')
        print("""
                    CSV file found!""")
    except:
        print("""
                    File not found! Please ensure that CSV is in the same directory as this script.
                    Quitting...
              """)
        closeFile(file)
    
    entries = csvParser()
    pointer = 0
    
    while True:
        rm = input("""
                    --------------------------------------

                    Please input the room number you want to process (e.g. 1119A) or type "all" to start at the beginning of the list: """)
        if rm == "all":
            print("""
                    Starting from the beginning of the list...""")
            pointer = 0
            break
        elif rm in rooms:
            pointer = rooms[rm]
            print("""
                    Starting from room {}...""".format(rm))
            break
        else:
            print("""
                    Invalid room number! Please try again.""")

    user = entries[pointer]

    while True:

        print("""
                    --------------------------------------
              
                    Ready to process user:""")
        printUser(user, pointer)

        wait = input("""                    
                    [ ] Press "Enter" to process the next user
                    [X] Enter 'x' to exit
                     
                    Options:
                    
                    [1] Enter 1 to view next user
                    [2] Enter 2 to view all remaining users
                    [3] Enter 3 to reset mouse click recording
                    [4] Enter 4 to skip this user and continue
                    [5] Enter 5 to jump to a specific user
                     
                    Edit User Information:
                    
                    [6] Enter 6 to edit user information
                    [7] Enter 7 to delete user information
                    [8] Enter 8 to add a new user
                    
                    --------------------------------------
                    
                    Input: """)
        
        if wait == "":
            if pointer >= len(entries):
                print("""
                      No more users!""")
                closeFile(file)

        match wait:
            case "":
                fields = list(user)
                # print(user)
                fields[0] = fields[0] + fields[1]  # Combine room and letter for input
                del fields[1]  # Remove letter from user list
                for i in instructions:
                    
                    if i[0] == "Click":
                        pyautogui.click(x=i[1], y=i[2])
                        print("""\t\t\tClicking: {}""".format(str(i)))
                    elif i[0] == "Text":
                        if not fields:
                            print("No more words!")
                            continue
                        pyautogui.write(fields.pop(0))
                    else:
                        continue

                pointer += 1

                print("""
                      User processed:""")
                printUser(user, pointer)
                
                if pointer >= len(entries):
                    print("""
                    No more users!""")
                    closeFile(file)
                user = entries[pointer]
            case "1":
                next = None
                if pointer + 1 < len(entries):
                    next = entries[pointer + 1]

                    print("""
                    Next user:""")
                    printUser(next, pointer + 1)
                else:
                    print("""
                    No users left!""")
            case "2":
                
                for i in entries[pointer:]:
                    printUser(i, entries.index(i))
                print("""
                      Users remaining: {}""".format(len(entries) - pointer))
            case "3":
                print("""
                    Resetting mouse click recording...""")
                start_listening()
            
            case "4":
                print("""
                      Skipping user...""")
                printUser(user, pointer)
                pointer += 1
                if pointer >= len(entries):
                    print("""
                    No more users!""")
                    closeFile(file)
                user = entries[pointer]
            case "5":
                rm = input("""              
                    Please input the room number you want to jump to (e.g. 1119A): """)
                if rm in rooms:
                    pointer = rooms[rm]
                    user = entries[pointer]
                    print("""
                      Jumping to user...""")
                    printUser(user, pointer)
                else:
                    print("""
                      Invalid room number! Please try again.""")
            case "6":
                rm = input("""
                    Please input the room number you want to edit (e.g. 1119A): """)
                if rm in rooms:
                    p = rooms[rm]
                    user = entries[p]
                    print("""
                      Editing user:""")
                    printUser(user, p)
                    
                    new_room = input("""
                      New Room (leave blank to keep current): """)
                    new_letter = input("""
                      New Letter (leave blank to keep current): """)
                    new_lastname = input("""
                      New Lastname (leave blank to keep current): """)
                    new_firstname = input("""
                      New Firstname (leave blank to keep current): """)

                    if new_room:
                        user[0] = new_room
                    if new_letter:
                        user[1] = new_letter
                    if new_lastname:
                        user[2] = new_lastname
                    if new_firstname:
                        user[3] = new_firstname
                    
                    entries[p] = user

                    entries = sortRooms(entries)

                    print("""
                          User updated:""")
                    printUser(user, entries.index(user))

                    print(
                        """
                          Note: If you changed the room number or letter, the room will be sorted to its new position in the list."""
                    )
                    user = entries[pointer]

                else:
                    print("""
                      Invalid room number! Please try again.""")
            case "7":
                rm = input("""
                    Please input the room number you want to delete (e.g. 1119A): """)
                if rm in rooms:
                    p = rooms[rm]
                    user = entries[p]
                    print("""
                      Deleting user:""")
                    printUser(user, p)

                    del entries[p]
                    entries = sortRooms(entries)
                    
                    if pointer >= len(entries):
                        pointer = len(entries) - 1
                        if pointer < 0:
                            print("""
                            No more users!""")
                            closeFile(file)

                    user = entries[pointer]

                    print("""
                      User deleted.""")
            case "8":
                new_room = input("""
                    Please input the new room number (e.g. 1119): """)
                new_letter = input("""
                    Please input the new letter (e.g. A): """)
                new_lastname = input("""
                    Please input the new lastname: """)
                new_firstname = input("""
                    Please input the new firstname: """)
                if not new_room or not new_letter or not new_lastname or not new_firstname:
                    print("""
                    Invalid input! Please try again.""")
                    continue
                new_user = [new_room, new_letter, new_lastname, new_firstname]
                new_user.append('2026')
                if new_user not in entries:
                    entries.append(new_user)
                    entries = sortRooms(entries)
                    print("""
                    New user added:""")
                    printUser(new_user, entries.index(new_user))
                user = entries[pointer]

            case "x":
                print("""
                    Exiting script...""")
                closeFile(file)
            
        wait = input("""
                    Press enter to continue...""")
        
        

        