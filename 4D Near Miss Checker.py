import random

help = '''
This is a Near Miss Checker for 4D. 4D is a gambling game which involves correctly picking the same 4-digit number as is drawn by the
governing body. This script attempts to empirically determine how often a 'near miss' occurs - specifically, how often the guesser will
guess the same number as the drawn number, with exactly one digit being off by one. This script allows for flexibility regarding how 
many digits are in the number, and how many iterations to run the script through.
'''

def generate_number():
    global number_of_digits
    random_string_size = ""
    for i in range(number_of_digits):
        random_string_size = random_string_size + "9"
    return random.randint(0, int(random_string_size))

def pad_number(number):
    global number_of_digits
    number_string = str(number)
    if len(number_string) < number_of_digits:
        difference = number_of_digits - len(number_string)
        pad_string = ""
        for i in range(difference):
            pad_string = "0" + pad_string
        return pad_string + number_string
    else:
        return str(number)

def check_off_by_one(scored_digit, attempted_digit):
    if int(scored_digit) == int(attempted_digit):
        return 0
    elif abs(int(scored_digit) - int(attempted_digit)) == 1:
        return 1
    else:
        return 2

def is_off_by_one(scored, attempt):
    string_scored = str(scored)
    string_attempt = str(attempt)
    counter = 0
    for i in range(len(string_scored)):
        scored_int = pad_number(string_scored)[i]
        attempt_int = pad_number(string_attempt)[i]
        counter += check_off_by_one(scored_int, attempt_int)
    return counter == 1

def one_iteration():
    scored = generate_number()
    attempt = generate_number()
    if is_off_by_one(scored, attempt):
        return True
    else:
        return False

def run_iterations(number_of_iterations):
    counter = 0
    for i in range(number_of_iterations):
        if one_iteration():
            counter += 1
    return counter

def parse_as_int(parameter, string):
    while True:
        try:
            parameter = int(string)
            return parameter
        except ValueError:
            print("Please enter a valid integer.")
            string = input()

def main():
    global number_of_digits, number_of_iterations
    print("\n\nNext simulation:")
    print("What is the desired number of digits?")
    number_of_digits = parse_as_int(number_of_digits, input())
    print("What is the desired number of iterations?")
    number_of_iterations = parse_as_int(number_of_iterations, input())
    print("Number of attempts: " + str(number_of_iterations))
    print("Number of near misses: " + str(run_iterations(number_of_iterations)))

number_of_digits = 0
number_of_iterations = 0

print(help)
while True:
    main()