'''
TODO: Create proper exception handling for the cases where:
            - Angel (as written) does not exist in spreadsheet
            - Mortal does not exist in spreadsheet (i.e. truncated list)
            - You notice that more than one possible Angel is detected
                - size of returned series?
        Consider doing moreOOP, and flexible file names. Details go into a
            list which is then returned. (e.g. full_name, room_number etc)
        Consider including a search function, which prints out all name strings
            containing the search phrase, regardless of letter case.
'''

## Author: Samuel Lim (GitHub: Sam-limyr)

help = '''
This Python script was designed to streamline individual message-sending
to participants of tAngels 2019. This script relies on two main CSV files:
angel_file_path, which contains a loop or loops or angel-mortal pairings,
and data_file_path, which contains data for each participant.
To use, create and place both csv files in the same directory as this script,
and follow the instructions below. Take note that the precise ordering of 
columns in each csv file is important - identify which columns are used by
examining the code below. The formatted message below may also be modified 
as is necessary.

IMPORTANT:
The file names ('angel_file_path' and 'data_file_path') listed below must 
be changed!!

Note:
Format for angel_file_path - all names in one column; separate with spaces 
if multiple loops exist.
Format for data_file_path - rows are participants, columns are fields. The 
ordering of the fields is somewhat flexible; you need to change the formatted 
message below. The specific ordering of the fields is reflected precisely 
in the series.iloc calls commented below, so those values must be changed 
as well.
'''

import pandas, math, pyperclip

## Change these two variables to reflect desired name changes to the angel and data files.
angel_file_path = 'C://Users//S//AppData//Local//Programs//Python//Python36//MY SCRIPTS//Test folder//Angel File.csv'
data_file_path = 'C://Users//S//AppData//Local//Programs//Python//Python36//MY SCRIPTS//Test folder//Data File.csv'

def count_occurrences_of_name_in_file(full_name, file_path):
    #file_being_examined = pandas.read_csv(file_path, encoding="ISO-8859-1")
    #name_series = file_being_examined[column_name].items()
    name_series = read_pandas_column_series_from_file('Full Name', file_path)
    number_of_name_occurences = 0
    for name in name_series:
        if name == full_name:
            number_of_name_occurences += 1
    return number_of_name_occurences

def verify_if_name_exists_in_file(full_name, file_path):
    return count_occurrences_of_name_in_file(full_name, file_path) > 0

def verify_if_multiple_names_exist_in_file(full_name, file_path):
    return count_occurrences_of_name_in_file(full_name, file_path) > 1

def read_pandas_row_series_from_file(row_name, file_path):
    file_being_examined = pandas.read_csv(file_path, encoding="ISO-8859-1")
    series = file_being_examined[file_being_examined['Full Name'].isin([row_name])]

def read_pandas_column_series_from_file(column_name, file_path):
    file_to_parse = pandas.read_csv(file_path, encoding="ISO-8859-1")
    series = file_to_parse[[column_name]]
    return series   

def get_mortal_from_angel(angel_name):
    if not verify_if_name_exists_in_file(angel_name, angel_file_path):
        print("No Angel with that name exists in the Angel File!")
    elif verify_if_multiple_names_exist_in_file(angel_name, angel_file_path):
        print("Multiple Angels with that name exist in the Angel File!")
    else:
        series = read_pandas_column_series_from_file("Full Name", angel_file_path)

        #angel_file = pandas.read_csv(angel_file_path, encoding="ISO-8859-1")
        #series = angel_file[['Full Name']]

        for row in range(len(series)):
            item = series.iloc[row, 0]
            try:
                checker = math.isnan(item)
            except TypeError:
                if item.startswith(angel_name):
                    return series.iloc[row + 1, 0]


def clean_up_telegram_handle_formatting(telegram_handle):
    tele_handle = telegram_handle
    if tele_handle.startswith("'"):
        tele_handle = tele_handle.lstrip("'")
    if not tele_handle.startswith("@"):
        tele_handle = "@" + tele_handle
    return tele_handle

def get_angel_telegram(angel_name):

    test = '''try:
        data_file = pandas.read_csv(data_file_path, encoding="ISO-8859-1")
    except FileNotFoundError as error:
        print(type(error))
        print(error.args)
        print(error)
    
    series = data_file[data_file['Full Name'].isin([angel_name])]'''
    
    if not verify_if_name_exists_in_file(angel_name, data_file_path):
        print("No Angel with that name exists in the Data File!")
    elif verify_if_multiple_names_exist_in_file(angel_name, data_file_path):
        print("Multiple Angels with that name exist in the Data File!")
    else:
        series = read_pandas_row_series_from_file(angel_name, data_file_path)
                
        ## these series.iloc calls will vary based on precisely which columns you use
        try:
            tele_handle = series.iloc[0, 3]
            return clean_up_telegram_handle_formatting(tele_handle)
        except IndexError:
            print("Error of some sort in get_angel_telegram()!")

def create_formatted_message(mortal_name, angel_name):
    data_file = pandas.read_csv(data_file_path, encoding="ISO-8859-1")
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


## this function is used for obtaining the details of a given person, perhaps to contact them or verify details.
def get_own_details(own_name):

    data_file = pandas.read_csv(data_file_path, encoding="ISO-8859-1")
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
Details of < {} >:
    Room number: < {} >
    Likes: < {} >
    Dislikes: < {} >
    Indicated prank level: < {} >
    Prank vetoes (if any): < {} >
      '''.format(full_name, room_number, likes, dislikes, prank_level, prank_vetoes)

def copy_mortal_details_to_clipboard(angel_name):
    mortal_name = get_mortal_from_angel(angel_name)
    formatted_message = create_formatted_message(mortal_name, angel_name)
    pyperclip.copy(formatted_message)
    print("Copied formatted message containing mortal's details to clipboard.\n")

def copy_angel_details_to_clipboard(angel_name):
    angel_details = get_own_details(angel_name)
    pyperclip.copy(angel_details)
    print("Copied angel's own details to clipboard.\n")

def execute_data_retrieval(angel_name):
    while True:
        if is_producing_formatted_message:
            copy_mortal_details_to_clipboard(angel_name)
        else:
            copy_angel_details_to_clipboard(angel_name)

def set_formatted_message_boolean():
    global is_producing_formatted_message
    print("Do you want to use the formatted message for this use of the script? Enter 'yes' or 'no'. If you want to change mode, you will have to restart the script.")
    while True:
        answer = input()
        if answer == 'yes':
            is_producing_formatted_message = True
            break
        elif answer == 'no':
            is_producing_formatted_message = False
            break
        else:
            print("Please enter a valid instruction!")

def main():
    print("Input the name of the Angel you want to search for.")
    angel_name = input()
    #print("The Angel's telegram handle is " + get_angel_telegram(angel_name))
    execute_data_retrieval(angel_name)

is_producing_formatted_message = True

print(help)
set_formatted_message_boolean()
while True:
    main()
