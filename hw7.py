#!/usr/bin/env python3

'''
Erik Miller's Foundations of Programming: hw7

To run this script, from the pycharm Terminal:
python hw7.py

Requires:
python3
'''

from sortedcontainers import SortedDict


def print_menu():
    print('1. Print Users')
    print('2. Add a User')
    print('3. Remove a User')
    print('4. Lookup a Username')
    print('5. Quit')
    print()

#Get input and control for type and limited set of options
def general_input(prompt, error_prompt, error_prompt2, type, max_attempts, remaining_attempts, defualt, defualt_text, limited, possible_responses):
    # set input counter to 0
    limit = 0

    while True:
        try:
            #check max guesses
            if limit == max_attempts:
                #If over max guesses then tell user what defualt value has been chosen.
                #Check to see if defualt error response is chosen
                if defualt_text == "":
                    print("Allowable attempts exceeded. User response has been set to {h1}".format(h1 = defualt))
                else:
                    #Print custom error response
                    print(defualt_text)
                user_input = defualt
                break
            else:
                #Add to guess limit counter
                limit += 1
                #replace single quotes with double to make input prompt work with eval_sting
                prompt = prompt.replace("'", '"')
                # combine user input strings and evaluate
                eval_string = type+"(input('"+prompt+"'))"
                user_input = eval(eval_string)
                #Check to see if remaining attempts is included in response
                if remaining_attempts == 1:
                    #If remaining attempts is included in response then define string
                    remaining_string = "{h1} attempts remaining.".format(h1 = int(max_attempts - limit))
                else:
                    #If remaining attempts is not included in response then set string to nothing
                    remaining_string = ""
                #Check to see if output is limited to a defined set
                if limited == 1:
                    if user_input in possible_responses:
                        break
                    else:
                        #Print either default error or custom error
                        if error_prompt2 == "":
                            print("Inputs are limited to the following: {h1}. {h2}".format(
                                h1=possible_responses, h2 = remaining_string))
                        else:
                            print("{h1} {h2}".format(h1 = error_prompt2, h2 = remaining_string))
                        continue
                break
        except ValueError:
                print(error_prompt," {h1}".format(h1 = remaining_string))

    return user_input


# Create dictionary with key = Names, value = user_name
usernames = SortedDict()
usernames['Summer'] = 'summerela'
usernames['William'] = 'GoofyFish'
usernames['Steven'] = 'LoLCat'
usernames['Zara'] = 'zanyZara'
usernames['Renato'] = 'songDude'

# setup counter to store menu choice
menu_choice = 0

# as long as the menu choice isn't "quit" get user options
while menu_choice != 5:
    # display your menu
    print_menu()

    # get menu choice from user
    input_choices = (1, 2, 3, 4, 5)
    menu_choice = general_input("Type in a number (1-5): ", "Input must be an integer from 1 to 5.","1. Print Users\n"\
        "2. Add a User\n3. Remove a User\n4. Lookup a User\n5. Quit\n", "int", 3, 0, 5, "", 1, input_choices)

    # view current entries
    if menu_choice == 1:
        print("Current Users:")
        for x, y in usernames.items():
            print("Name: {} \tUser Name: {} \n".format(x, y))

    # add an entry
    elif menu_choice == 2:
        print("Add User")
        name = input("Name: ")
        username = input("User Name: ")
        usernames[name] = username

    # remove an entry
    elif menu_choice == 3:
        print("Remove User")
        delete_option = general_input("Delete by user or user name? (Enter either 'user' or 'username'): ", "error1", "Enter either 'user' or 'username'.", "str", 3, 1, "user", "", 1, ["user", "username"])
        #Delete by user
        if delete_option == "user":
            name = general_input("Enter name to delete: ", "error1", "No entry with that name.", "str", 3, 1, "", "No names deleted.", 1, usernames)
            if name in usernames:
                # delete that entry
                del usernames[name]

        #Delete by username
        if delete_option == "username":
            #get user name from list of usernames
            name = general_input("Enter username to delete: ", "error1", "No entry with that username.", "str", 3, 1, "", "No usernames deleted.", 1, usernames.values())
            #find key matching that user name
            for key, value in usernames.iteritems():
                if value == name:
                    # delete that entry
                    del usernames[key]

    # view user name
    elif menu_choice == 4:
        print("Lookup User")
        #name = input("Name: ")
        name = general_input("Enter name: ", "error1", "No entry with that name.", "str", 3, 1, "", "Username not found.", 1, usernames)
        if name in usernames:
            print("Username for selected user {h1} is {h2}.".format(h1 = name, h2 = usernames[name]))
