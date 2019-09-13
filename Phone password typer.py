description = '''

===============================================================================

Passwords should be easy to type on phones. This implies that there should not
be a long string of letters within the password that one hand is required to
type. An example of such a string would be 'were', or 'sad', which are both
typed entirely by the left hand.

This password typer checker scans a prospective password and outputs three
details: 1) the similarity list of the password,
         2) the similarity streaks list of the password, and
         3) the length of the longest similarity streak.

IMPORTANT: Numbers and symbols are not yet supported by this password checker!!

Depending on your phone-typing habits, you can alter the arrays 'left_hand' and
'right_hand' below.

Extension 1: Add in-program customizable handedness for each character.
Extension 2: Add support for numbers and symbols.

===============================================================================

'''

help = '''

===============================================================================

Hello and welcome to the phone password typer checker.

Input 'exit' to exit.
Input 'help' to call this help screen again.
Input 'desc' for additional background information.

===============================================================================

Please enter a password, or instruction.

'''

left_hand = ['q', 'w', 'e', 'r', 't', 'a', 's', 'd', 'f', 'g', 'z', 'x', 'c', \
            'Q', 'W', 'E', 'R', 'T', 'A', 'S', 'D', 'F', 'G', 'Z', 'X', 'C']
right_hand = ['y', 'u', 'i', 'o', 'p', 'h', 'j', 'k', 'l', 'v', 'b', 'n', 'm', \
            'Y', 'U', 'I', 'O', 'P', 'H', 'J', 'K', 'L', 'V', 'B', 'N', 'M']

def scan_letter(password_list, index):
    if index == 0:
        return 0
    elif password_list[index] in left_hand:
        if password_list[index - 1] in right_hand:
            return 0
        elif password_list[index - 1] in left_hand:
            return 1
    elif password_list[index] in right_hand:
        if password_list[index - 1] in left_hand:
            return 0
        elif password_list[index - 1] in right_hand:
            return 1

def build_similarity_list(password):
    similarity_list = []
    for i in range(len(password)):
        similarity_list.append(scan_letter(list(password), i))
    return similarity_list

def accumulate_streaks(similarity_list):
    streak_list = []
    current_streak = 0
    for i in range(1, len(similarity_list)):
        if similarity_list[i] == 0 and similarity_list[i-1] == 1:
            streak_list.append(current_streak)
            current_streak = 0
        elif similarity_list[i] == 1:
            current_streak += 1
    if current_streak != 0:
        streak_list.append(current_streak)
    return streak_list

def longest_streak(streak_list):
    current_longest_streak = 0
    for i in streak_list:
        if i > current_longest_streak:
            current_longest_streak = i
    return current_longest_streak

def generate_streaks(password):
    similarity_list = build_similarity_list(password)
    streak_list = accumulate_streaks(similarity_list)
    password_longest_streak = longest_streak(streak_list)
    if streak_list == []:
        streak_list = "No streaks."
    return "For the password '" + password + "':\nSimilarity list: " + str(similarity_list) + \
            "\nStreak list: " + str(streak_list) + "\nLongest streak: " + str(password_longest_streak) + "\n"  

print(help)
while True:
    password = input()
    if password == "exit":
        print("\nThank you! Program exiting now.\n")
        break
    elif password == "help":
        print(help)
    elif password == "desc":
        print(description)
    elif not password.isalpha():
        print("Non-letters are not supported!\n")
    else:
        print(generate_streaks(password))