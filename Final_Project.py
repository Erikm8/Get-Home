#!/usr/bin/env python3

'''
Erik Miller's Foundations of Programming: Final_Project.py

To run this script, from the pycharm Terminal:
python Final_Project.py

Requires:
python3

Add modules required to install
requires instillation of beautifulsoup4 and requests

Functionality
Script searches Trulia.com based on given parameters and outputs all homes that are included in search
script outputs a file with all homes found previously
If new homes are found the file is updated and an email is sent to erikwmiller.python@gmail.com

'''


#Import required modules for email and print homes to file function.
import requests
from bs4 import BeautifulSoup


#import required modules for Trulia lookup function
import smtplib
import os
import time

#send an email
def email_function(to_email, from_email, password, subject, text):

    #Create email message
    message = "To: {h1}\r\nFrom: {h2}\r\nTo: {h3}\r\n"\
            "Subject: {h4}\r\n\r\n".format(h1 = to_email, h2 = from_email, h3 = to_email, h4 = subject)\
            + text

    #print(message)
    #log into server and send email
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(from_email,password)
    server.sendmail(from_email, to_email, message)
    server.quit()

#Print homes to file and email if any new homes
def home_ouput_file(homes, city, state, to_email, from_email, password, email):

    # Create dictionary for homes
    homes_dict = {}
    for x in homes:
        # Create dictionary with trulia ID as keys and link as values
        key = x.split('/')[2].split('-')
        key = key[0] + '-' + key[1]
        homes_dict[key] = 'https://www.trulia.com/' + x

    #Check if directory "Homes_For_Sale_Location" already exists and create if not
    dir_name = "Homes_For_Sale_" + city.replace(' ','_') + '_' +  state
    file_name = dir_name + '.txt'
    if os.path.isdir(dir_name)!= True:
        os.mkdir(dir_name)
        # Change to "Homes_For_Sale_Location" directory
        os.chdir("./" + dir_name)
        # Create output file
        outfile = open(file_name, "a")
        #Create header line
        outfile.write("Homes for sale in " + city + ' ' + state + '\n')
        #close file
        outfile.close()
    #change to directory if it already did exist
    else:
        os.chdir("./" + dir_name)

    #Try to open file and read homes already discovered
    file = "./" + dir_name + ".txt"
    try:
        f = open(file,'r')
        #check if homes are already found
        for line in f:
            #pull Trulia IDs out of file
            line = line.strip()
            ids = line.split(',')[0]
            #Check if Home is already in file
            if ids in homes_dict:
                #delete from dict if alreay in file
                del homes_dict[ids]
        f.close()
    #If file not found then create file with correct header
    except FileNotFoundError:
        # Create output file
        outfile = open(file_name, "a")
        # Create header line
        outfile.write("Homes for sale in " + city + ' ' + state + '\n')
        # close file
        outfile.close()

    #Write remaining homes to file and send email if email option is selected
    if len(homes_dict) > 0 and email == 1:
        #build string to print to file and add date and time to string
        print_string = time.strftime("%Y/%m/%d") + ' ' + time.strftime("%I:%M:%S") + '\n'
        email_string = ''
        for keys in homes_dict:
            print_string = print_string + keys + ', ' + homes_dict[keys] + '\n'
            email_string = email_string + homes_dict[keys] + '\n'
        #open file and print to end
        with open(file, 'a') as f:
            #print(print_string)
            f.write(print_string)
            f.close()


     #Send email if new homes were found
        subject = "Check out these houses in {h1} on {h2}!".format(h1 = city + ', ' + state, h2 = time.strftime("%Y/%m/%d"))
        text = "Check out these houses I found these houses for you!\n\n" + email_string

        email_function(to_email, from_email, password, subject, text)

    #Go back to top level directory
    os.chdir("..")

    return ()

#Get home listings from Trulia based on a set of input parameters
def get_trulia_links(city, state, price_min, price_max, bed_rooms,key_words, page_max):

    #Build base trulia url based on function inputs
    Location_str = city.replace(' ', '_') + ',' + state + '/'
    Beds_str = bed_rooms + 'p_beds/'
    Price_srt = price_min + '-' + price_max + '_price/'
    Key_words_str = '_' + key_words + '_keyword/'
    url = 'https://www.trulia.com/for_sale/' + Location_str + Beds_str + Price_srt + Key_words_str
    #print(url)
    #Get html code
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, "lxml")

    #Initiallize homes
    homes = []

    #Check to see if no homes were found
    tag = 'h3'  #h3 tag will show up if no homes are found
    all_tag = soup.find_all(tag)
    if len(all_tag) > 0:
        x = "Your search does not match any homes" in all_tag[0]
        #print(x)
        if x == True:
            #If no homes are found, return empty list
            return homes

    #Check total number of pages
    tag = 'a'
    class_type = 'backgroundBasic mrs bas pvs phm' #this class type is used for page navigation buttons
    all_tag = soup.find_all(tag, class_type)
    #Check for "last page" link
    if len(all_tag) > 0:
        Last_Page = str(all_tag[-1])
        #find last page number
        Last_Page = int(Last_Page.split('/')[-3].split('_')[0])
        #Reset Last_Page to 10 if over 10
        if Last_Page > page_max:
            Last_Page = page_max
    else:
        Last_Page = 1
    #print(Last_Page)

    #set tag and class for home links
    #Check for homes on page 1
    tag = 'div'
    class_type = 'cardFooter man ptn pbs'
    all_tag = soup.find_all(tag, class_type)
    #collect all inks
    #print("page 1")
    for x in all_tag:
        if x.has_attr('data-url'):
            #print(x.attrs['data-url'])
            homes.append(x.attrs['data-url'])

    #print(len(homes))
    #Check homes on other pages if more than 1
    if Last_Page > 1:
        for i in range(2 , Last_Page + 1):
            #print("page " + str(i))
            #Build new URL
            url_end = str(i) + '_p/'
            url_new = url + url_end

            #Call beautifulSoup again
            response = requests.get(url_new)
            content = response.content
            soup = BeautifulSoup(content, "lxml")
            #find all homes on next pages
            all_tag = soup.find_all(tag, class_type)
            for x in all_tag:
                if x.has_attr('data-url'):
                    homes.append(x.attrs['data-url'])
    #print(len(homes))
    return homes

#Put if main function here

#Email info
to_email = 'erikwmiller.python@gmail.com'
from_email = 'erikwmiller.python@gmail.com'
password = 'Python_is_fun'

#Call functions for location 1
city = 'Bend'
state = 'OR'
price_min = '0'
price_max = '500000'
bed_rooms = '3'
key_words = 'view'
page_max = 20
email = 1
#Lookup Homes in Location 1
homes_Bend = get_trulia_links(city, state, price_min, price_max, bed_rooms, key_words, page_max)
#Create file and email
home_ouput_file(homes_Bend , city, state, to_email, from_email, password, email)

#Call functions for location 1
city = 'Hood River'
state = 'OR'
price_min = '0'
price_max = '500000'
bed_rooms = '3'
key_words = 'view'
page_max = 20
email = 1
#Lookup Homes in Location 1
homes_HR = get_trulia_links(city, state, price_min, price_max, bed_rooms, key_words, page_max)
#Create file and email
home_ouput_file(homes_HR , city, state, to_email, from_email, password, email)

#Code Checks
#print ("Total homes in Bend = " + str(len(homes_Bend)))
#print ("Total homes in Hood River = " + str(len(homes_HR)))