'''
TODO: Create proper exception handling for the cases where:
            - Angel (as written) does not exist in spreadsheet
            - Mortal does not exist in spreadsheet (i.e. truncated list)
            - You notice that more than one possible Angel is detected
                - size of returned series?
        Consider doing moreOOP, and flexible file names. Details go into a
            list which is then returned. (e.g. full_name, room_number etc)
        Consider including a switch to check for whether you're searching for
            angel's details or the mortal's details.
        Consider including a search function, which prints out all name strings
            containing the search phrase, regardless of letter case.
'''

## Author: Samuel Lim (GitHub: Sam-limyr)
'''
This Python script was designed to streamline individual message-sending
to participants of tAngels 2019. This script relies on two main CSV files:
"Angel File.csv", which contains a loop or loops or angel-mortal pairings,
and "Data File.csv", which contains data for each participant.
To use, place both csv files in the same directory as this script, and
follow the instructions. Take note that the precise ordering of columns
in each csv file is important - identify which columns are used by examining
the code below. The formatted message below may also be modified as is
necessary.
'''

import pandas, math, pyperclip

def get_mortal_from_angel(angel_name):
    angel_file = pandas.read_csv("Angel File.csv", encoding="ISO-8859-1")

    series = angel_file[['Full Name']];

    for row in range(len(series)):
        item = series.iloc[row, 0]
        try:
            checker = math.isnan(item)
        except TypeError:
            if item.startswith(angel_name):
                return series.iloc[row + 1, 0]
    print("ERROR!! Tell Sam")
    return "ERROR!!"

def get_angel_telegram(angel_name):
    data_file = pandas.read_csv("Data File.csv", encoding="ISO-8859-1")
    series = data_file[data_file['Full Name'].isin([angel_name])]

    ## these series.iloc calls will vary based on precisely which columns you use
    try:
        tele_handle = series.iloc[0, 3]
    except IndexError:
        print("Error of some sort in get_angel_telegram()!")

    if tele_handle.startswith("'"):
        tele_handle = tele_handle.strip("'")
    if not tele_handle.startswith("@"):
        tele_handle = "@" + tele_handle

    return tele_handle

def get_mortal(mortal_name, angel_name):

    data_file = pandas.read_csv("Data File.csv", encoding="ISO-8859-1")
    series = data_file[data_file['Full Name'].isin([mortal_name])]

    ## these series.iloc calls will vary based on precisely which columns you use
    full_name = series.iloc[0, 0]
    room_number = series.iloc[0, 1] + "-" + series.iloc[0, 2]
    likes = series.iloc[0, 8]
    dislikes = series.iloc[0, 9]
    prank_level = series.iloc[0, 10]
    prank_vetoes = series.iloc[0, 11]

    try:
        if math.isnan(prank_vetoes):
            prank_vetoes = "None."
    except TypeError:
        pass
    
    return r'''
A twinkling of fairy dust sparkles through the air...

Hello and welcome to tAngels 2019, {}!

Your Mortal's name is < {} >.
Their room number is < {} >.

They like: < {} >

They dislike: < {} >

Their indicated prank level is < {} >.

If they have indicated any, their prank vetoes are < {} >.

REMEMBER: do not intentionally reveal your identity to your mortal, even if they are your friend!

Have fun, and let the fairytale begin!
      '''.format(angel_name, full_name, room_number, likes, dislikes, prank_level, prank_vetoes)

def get_own_details(own_name):

    data_file = pandas.read_csv("Data File.csv", encoding="ISO-8859-1")
    series = data_file[data_file['Full Name'].isin([own_name])]

    ## these series.iloc calls will vary based on precisely which columns you use
    full_name = series.iloc[0, 0]
    room_number = series.iloc[0, 1] + "-" + series.iloc[0, 2]
    likes = series.iloc[0, 8]
    dislikes = series.iloc[0, 9]
    prank_level = series.iloc[0, 10]
    prank_vetoes = series.iloc[0, 11]

    try:
        if math.isnan(prank_vetoes):
            prank_vetoes = "None."
    except TypeError:
        pass
    
    return r'''
A twinkling of fairy dust sparkles through the air...

Hello and welcome to tAngels 2019, ***PLACEHOLDER NAME***!

Your Mortal's name is < {} >.
Their room number is < {} >.

They like: < {} >

They dislike: < {} >

Their indicated prank level is < {} >.

If they have indicated any, their prank vetoes are < {} >.

REMEMBER: do not intentionally reveal your identity to your mortal, even if they are your friend!

Have fun, and let the fairytale begin!
      '''.format(full_name, room_number, likes, dislikes, prank_level, prank_vetoes)

def parse_instruction(mode, angel_name):
    while True:
        if mode == "mortal":
            pyperclip.copy(get_mortal(get_mortal_from_angel(angel_name), angel_name))
            return "Copied mortal's details to clipboard.\n"
        elif mode == "angel":
            pyperclip.copy(get_own_details(angel_name))
            return "Copied angel's own details to clipboard.\n"
        else:
            print("Please enter a valid instruction!")

while True:
    print("Input the name of the Angel you want to search for.")
    angel_name = input()
    print("The Angel's telegram handle is " + get_angel_telegram(angel_name))
    print("Mode? 'angel' to get angel's own details, 'mortal' to get mortal's details")
    print(parse_instruction(input(), angel_name))
    
