## Author: Samuel Lim (GitHub: Sam-limyr)

help = """
This is a Python script written to decrypt a credit amount encrypted by the companion script "Credit Encrypt".
It is meant for use by all participants of an event. Inputs required by the user are: their full name,
their matriculation A-number, their NUSNET E-number, and their Tembusu room number.
The script will return their credit amount.

Note: The administrator must first input all the encoded strings as below, before disseminating this script.
"""

import re

## Input the encoded strings directly here, above this "Example" string.
credit_dictionary = {

	"Example of a name" : 784929
}

def name_exists_in_dictionary(full_name):
	return full_name in credit_dictionary

def parse_full_name():
	while True:
		print("Enter your full name (the one you registered on the form with)")
		full_name = input()
		if name_exists_in_dictionary(full_name):
			return full_name
		else:
			print("This full name was not submitted!")

def find_encrypted_value_from_name(full_name):
	return credit_dictionary.get(full_name)

def parse_A_number():
	a_number_pattern = re.compile("A\\d{7}[A-Z]")
	print("Enter your matric A-number (e.g. A0123456A)")
	while True:
		result = a_number_pattern.fullmatch(input())
		if result is not None:
			return int(result.string[1:8])
		else:
			print("Please type your A-number in the correct format (e.g. A0123456A)")

def parse_E_number():
	e_number_pattern = re.compile("E\\d{7}")
	print("Enter your NUSNET E-number (e.g. E0654321)")
	while True:
		result = e_number_pattern.fullmatch(input())
		if result is not None:
			return int(result.string[1:])
		else:
			print("Please type your E-number in the correct format (e.g. E0654321)")

def parse_room_number():
	room_number_pattern = re.compile("\\d{2}-\\d{3}[A-F]?")
	print("Enter your room number (e.g. 04-162A)")
	while True:
		result = room_number_pattern.fullmatch(input())
		if result is not None:
			return int(result.string[0:2] + result.string[3:6])
		else:
			print("Please type your room number in the correct format (e.g. 04-162A OR 13-151).")

def decrypt_encrypted_value(encrypted_credit_value):
	decryption_key = parse_A_number() + parse_E_number() + parse_room_number()
	decrypted_credit_value = (encrypted_credit_value - decryption_key) / 13
	return decrypted_credit_value

def main():
	user_full_name = parse_full_name()
	user_credit_value = find_encrypted_value_from_name(user_full_name)
	decrypted_credit_value = decrypt_encrypted_value(user_credit_value)
	print("Your credit amount is: " + str(decrypted_credit_value))

print(help)
while True:
	print("\nStarting a new iteration: ")
	main()
