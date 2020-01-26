## Author: Samuel Lim (GitHub: Sam-limyr)

help = r'''
This Python script was designed to streamline individual message-sending
to participants of tAngels 2019. This script relies on two main .csv files:
an Angel File, which contains a loop or loops of angel-mortal pairings,
and a Data File, which contains data of each participant.

To use, create and place both .csv files in the same directory as this script,
and follow the instructions below. The formatted messages below may also be
modified as is necessary.

IMPORTANT:
*** The file names ('angel_file_path' and 'data_file_path') listed below must 
be changed!!

Note:
* Format for Angel File - all names in one column; separate with spaces 
if multiple loops exist. The first entry of each loop must appear both
at the top and bottom of each section.
* Format for Data File - rows are participants, columns are fields. The
required fields are 'Full Name', 'Floor Number', 'Room Number',
'Telegram Handle', 'Likes', 'Dislikes', 'Prank Level', and 'Prank Vetoes'.
These are reflected in the global constants below. The constant names may
be changed if desired.
* When inputting names, you do not need to input the full name. Inputting
any portion of the name is sufficient. Inputting the name in uppercase or
lowercase is also not important. An error will be shown if there are
no names in the data file containing the inputted name, or if there are
multiple names that contain the inputted name.
* If one name is contained entirely within another, this script will 
prioritize exact name matches. For example, comparing "testtesttest" and
"testtest": Typing "test" will ambiguously match both; however, typing 
"testtest" is an exact match for the second name, and therefore the 
second name will be returned.
* Press Ctrl-C in the console to quit the program at any time.
'''

import pandas, math, pyperclip

## IMPORTANT: Edit these two variables to reflect desired name changes to the angel and data files. -----------------------------

angel_file_path = 'C://Users//Exact//Path//To//Your//File//Angel File.csv'
data_file_path = 'C://Users//Exact//Path//To//Your//File//Data File.csv'

## Edit these two message formats to reflect desired format changes to the messages: --------------------------------------------

mortal_details_message_format = r'''
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
    '''

angel_details_message_format = r'''
Printing Angel's own details:
For your own reference. Do NOT send this to any Angels accidentally.
Details of < {} >:
    Room number: < {} >
    Likes: < {} >
    Dislikes: < {} >
    Indicated prank level: < {} >
    Prank vetoes (if any): < {} >
'''

## Constants for column headers: ------------------------------------------------------------------------------------------------

CONSTANT_full_name = 'Full Name'
CONSTANT_floor_number = 'Floor Number'
CONSTANT_room_number = 'Room Number'
CONSTANT_telegram_handle = 'Telegram Handle'
CONSTANT_likes = 'Likes'
CONSTANT_dislikes = 'Dislikes'
CONSTANT_prank_level = 'Prank Level'
CONSTANT_prank_vetoes = 'Prank Vetoes'

## Pandas file reader utility functions: ----------------------------------------------------------------------------------------

def read_dataframe_from_file(file_path):
    return pandas.read_csv(file_path, encoding="ISO-8859-1")

def read_pandas_row_series_from_file(row_name_to_search, file_path):
    raw_dataframe = read_dataframe_from_file(file_path)
    caseless_row_name_to_search = row_name_to_search.casefold()
    for index, row in raw_dataframe.iterrows():
        if caseless_row_name_to_search in row.loc[CONSTANT_full_name].casefold():
            return row

def read_pandas_column_dataframe_from_file(column_name_to_search, file_path):
    raw_dataframe = read_dataframe_from_file(file_path)
    column = raw_dataframe[[column_name_to_search]]
    return column

def read_specific_full_name_from_file(name_to_search, file_path):
    row_containing_name_to_search = read_pandas_row_series_from_file(name_to_search, file_path)
    required_full_name = row_containing_name_to_search.loc[CONSTANT_full_name]
    return required_full_name

## Exception Checkers for names and number of name occurrences: -----------------------------------------------------------------

def no_naming_exceptions_exist(angel_name):
    name_is_all_whitespace_error = "Please enter a non-empty name!"
    full_name_does_not_exist_in_file_error = "No Angel with a name containing the input exists in the Data File!"
    multiple_full_names_exist_in_file_error = "Multiple Angels whose names contain the input exist in the Data File!"
    multiple_full_names_exist_in_file_explanation = "Please specify unambiguously which name it is.\nGive the exact full " \
    "name if one name is contained within the other and hence cannot be disambiguated."
    
    if name_is_all_whitespace(angel_name):
        print(name_is_all_whitespace_error)
        return False
    elif full_name_does_not_exist_in_file(angel_name, data_file_path):
        print(full_name_does_not_exist_in_file_error)
        return False
    elif multiple_full_names_exist_in_file(angel_name, data_file_path):
        print(multiple_full_names_exist_in_file_error)
        print_occurrences_of_name_in_file(angel_name, data_file_path)
        print(multiple_full_names_exist_in_file_explanation)
        return False
    else:
        return True

def name_is_all_whitespace(name_to_search):
    return name_to_search.isspace() or not name_to_search

def full_name_does_not_exist_in_file(name_to_search, file_path):
    return count_occurrences_of_name_in_file(name_to_search, file_path) == 0

def multiple_full_names_exist_in_file(name_to_search, file_path):
    return count_occurrences_of_name_in_file(name_to_search, file_path) > 1

def count_occurrences_of_name_in_file(name_to_search, file_path):
    name_dataframe = read_pandas_column_dataframe_from_file(CONSTANT_full_name, file_path)
    caseless_name_to_search = name_to_search.casefold()
    
    if more_than_one_exact_match_is_found(caseless_name_to_search, name_dataframe):
        return count_exact_matches_of_name_in_dataframe(caseless_name_to_search, name_dataframe)
    elif one_exact_match_is_found(caseless_name_to_search, name_dataframe):
        return 1
    else:
        return count_partial_matches_of_name_in_dataframe(caseless_name_to_search, name_dataframe)

def count_exact_matches_of_name_in_dataframe(name_to_search, name_dataframe):
    number_of_name_occurrences = 0
    for header, series in name_dataframe.items():
        for index, name in series.items():
            if name_to_search == name.casefold():
                number_of_name_occurrences += 1
    return number_of_name_occurrences

def one_exact_match_is_found(name_to_search, name_dataframe):
    return count_exact_matches_of_name_in_dataframe(name_to_search, name_dataframe) == 1

def more_than_one_exact_match_is_found(name_to_search, name_dataframe):
    return count_exact_matches_of_name_in_dataframe(name_to_search, name_dataframe) > 1

def count_partial_matches_of_name_in_dataframe(name_to_search, name_dataframe):
    number_of_name_occurrences = 0
    for header, series in name_dataframe.items():
        for index, name in series.items():
            if name_to_search in name.casefold():
                number_of_name_occurrences += 1
    return number_of_name_occurrences

def print_occurrences_of_name_in_file(name_to_search, file_path):
    name_dataframe = read_pandas_column_dataframe_from_file(CONSTANT_full_name, file_path)
    caseless_name_to_search = name_to_search.casefold()

    for header, series in name_dataframe.items():
        for index, name in series.items():
            if caseless_name_to_search in name.casefold():
                print(name)

## Deriving Mortal name from Angel name: ----------------------------------------------------------------------------------------

def get_mortal_from_angel(angel_name):
    raw_dataframe = read_dataframe_from_file(angel_file_path)
    caseless_angel_name = angel_name.casefold()
    angel_has_been_found = False

    for index, row in raw_dataframe.iterrows():
        name = replace_empty_value_with_nil_string(row.loc[CONSTANT_full_name])
        if angel_has_been_found:
            return name
        elif caseless_angel_name in name.casefold():
            angel_has_been_found = True

## Telegram-handle-parsing utilities: -------------------------------------------------------------------------------------------

def get_telegram_handle_from_name(angel_name):    
    name_series = read_pandas_row_series_from_file(angel_name, data_file_path)
    telegram_handle = name_series.loc[CONSTANT_telegram_handle]
    return clean_up_telegram_handle_formatting(telegram_handle)

def clean_up_telegram_handle_formatting(raw_telegram_handle):
    telegram_handle = raw_telegram_handle
    if telegram_handle.startswith("'"):
        telegram_handle = telegram_handle.lstrip("'")
    if not telegram_handle.startswith("@"):
        telegram_handle = "@" + telegram_handle
    return telegram_handle

## Message-parsing and message-formatting utilities: ----------------------------------------------------------------------------

# Edit mortal_details_message_format to change the format of this message
def create_formatted_message_containing_mortal_details(mortal_name, angel_name):
    angel_full_name = read_specific_full_name_from_file(angel_name, data_file_path)
    name_series = read_pandas_row_series_from_file(mortal_name, data_file_path)

    name_to_search = name_series.loc[CONSTANT_full_name]
    room_number = str(name_series.loc[CONSTANT_floor_number]) + "-" + str(name_series.loc[CONSTANT_room_number])
    likes = name_series.loc[CONSTANT_likes]
    dislikes = name_series.loc[CONSTANT_dislikes]
    prank_level = name_series.loc[CONSTANT_prank_level]
    prank_vetoes = replace_empty_value_with_nil_string(name_series.loc[CONSTANT_prank_vetoes])
    
    return mortal_details_message_format.format(angel_full_name, name_to_search, room_number, likes, dislikes, prank_level, prank_vetoes)

# Edit angel_details_message_format to change the format of this message
def create_message_containing_details_of_input_name(input_name):
    name_series = read_pandas_row_series_from_file(input_name, data_file_path)

    name_to_search = name_series.loc[CONSTANT_full_name]
    room_number = str(name_series.loc[CONSTANT_floor_number]) + "-" + str(name_series.loc[CONSTANT_room_number])
    likes = name_series.loc[CONSTANT_likes]
    dislikes = name_series.loc[CONSTANT_dislikes]
    prank_level = name_series.loc[CONSTANT_prank_level]
    prank_vetoes = replace_empty_value_with_nil_string(name_series.loc[CONSTANT_prank_vetoes])
    
    return angel_details_message_format.format(name_to_search, room_number, likes, dislikes, prank_level, prank_vetoes)

def print_full_name_and_telegram_handle_of_angel(angel_name):
    feedback_to_user_of_angel_telegram_handle = r'''You have selected: < {} >.
    Their telegram handle is: < {} >'''

    angel_full_name = read_specific_full_name_from_file(angel_name, data_file_path)
    angel_telegram_handle = get_telegram_handle_from_name(angel_name)
    print(feedback_to_user_of_angel_telegram_handle.format(angel_full_name, angel_telegram_handle))

def replace_empty_value_with_nil_string(input_string):
    if input_string is None:
        return "None."
    elif pandas.isnull(input_string):
        return "None."
    else:
        return input_string

## Pyperclip clipboard-copying function: ----------------------------------------------------------------------------------------

def copy_mortal_details_to_clipboard(mortal_details):
    feedback_to_user_of_copying_to_clipboard = "Copied formatted message containing Mortal's details to clipboard.\n"
    
    pyperclip.copy(mortal_details)
    print(feedback_to_user_of_copying_to_clipboard)

## Toggle which mode this script is in: -----------------------------------------------------------------------------------------

def set_mode_to_get_angel_or_mortal_details():
    instructions_for_setting_mode = r'''
    Do you want to search for the Angel's own details or their Mortal's details?
    Enter 'm' or 'a'.
    'm' signifies that you are looking for the details of the Mortal of the input name.
    'a' signifies that you are looking for the details of the input name.
    If you want to change mode, you will have to restart the script.

    '''
    invalid_instruction_error = "Please enter a valid instruction!"

    global is_in_obtaining_mortal_details_mode
    print(instructions_for_setting_mode)
    while True:
        answer = input()
        if answer == 'm':
            is_in_obtaining_mortal_details_mode = True
            break
        elif answer == 'a':
            is_in_obtaining_mortal_details_mode = False
            break
        else:
            print(invalid_instruction_error)

def format_query_for_angel_or_mortal_name(is_in_obtaining_mortal_details_mode):
    prompt_for_angel_mode = "\nInput the name of the Angel whose own details you are looking for.\n"
    prompt_for_mortal_mode = "\nInput the name of the Angel whose Mortal's details you are looking for.\n"

    if is_in_obtaining_mortal_details_mode:
        return prompt_for_mortal_mode
    else:
        return prompt_for_angel_mode

## Parses and copies the formatted message to clipboard: ------------------------------------------------------------------------

def parse_input_name_and_output_formatted_message(angel_name):
    if is_in_obtaining_mortal_details_mode:
        mortal_name = get_mortal_from_angel(angel_name)
        mortal_details = create_formatted_message_containing_mortal_details(mortal_name, angel_name)
        copy_mortal_details_to_clipboard(mortal_details)
    else:
        angel_details = create_message_containing_details_of_input_name(angel_name)
        print(angel_details)

## Main function: ---------------------------------------------------------------------------------------------------------------

def main():
    print(format_query_for_angel_or_mortal_name(is_in_obtaining_mortal_details_mode))
    name_to_search = input()
    if no_naming_exceptions_exist(name_to_search):
        print_full_name_and_telegram_handle_of_angel(name_to_search)
        parse_input_name_and_output_formatted_message(name_to_search)

## Actual code run: -------------------------------------------------------------------------------------------------------------

is_in_obtaining_mortal_details_mode = True

print(help)
set_mode_to_get_angel_or_mortal_details()
while True:
    main()
