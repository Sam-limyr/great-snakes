## Author: Samuel Lim (GitHub: Sam-limyr)

help = """
This is a Python script written to encrypt a credit amount stored as an integer. It is meant to be decrypted
by the companion script "Credit Decrypt". This script is intended for use by an administrator with control of all the
credit amounts. Inputs required to encrypt a credit amount are: the student's full name, their matriculation A-number,
their NUSNET E-number, and their Tembusu room number. The script will return a dictionary pair of full names and encrypted
credit amount.

The process of encryption involves summing up the numbers of the A-number, E-number, and room number. This is added to
13x the value of the credit amount.
"""

import re

def parse_A_number():
	a_number_pattern = re.compile("A\\d{7}[A-Z]")
	print("Enter the student's matric A-number (format: A0123456A)")
	while True:
		result = a_number_pattern.fullmatch(input())
		if result is not None:
			return int(result.string[1:8])
		else:
			print("Please type the A-number in the correct format (e.g. A0123456A)")

def parse_E_number():
	e_number_pattern = re.compile("E\\d{7}")
	print("Enter the student's NUSNET E-number (format: E0654321)")
	while True:
		result = e_number_pattern.fullmatch(input())
		if result is not None:
			return int(result.string[1:])
		else:
			print("Please type the E-number in the correct format (e.g. E0654321)")

def parse_room_number():
	room_number_pattern = re.compile("\\d{2}-\\d{3}[A-F]?")
	print("Enter the student's room number (format: 04-162A OR 13-151)")
	while True:
		result = room_number_pattern.fullmatch(input())
		if result is not None:
			return int(result.string[0:2] + result.string[3:6])
		else:
			print("Please type the room number in the correct format (e.g. 04-162A OR 13-151).")

def encrypt_credit_value(credit_value):
	encryption_key = parse_A_number() + parse_E_number() + parse_room_number()
	encrypted_credit_value = (credit_value * 13) + encryption_key
	return encrypted_credit_value

def parse_full_name():
	print("Enter the student's full name.")
	while True:
		full_name = input()
		if full_name.isalpha():
			return full_name
		else:
			print("Please input a non-empty alphabetical entry! Only alphabetical characters are allowed.")

def parse_credit_value():
	print("Enter the student's credit value. It must be an integer.")
	while True:
		credit_value = input()
		if credit_value.isdigit():
			return int(credit_value)
		else:
			print("Please enter an integer for the credit value!")

def print_output_to_format(full_name, credit_value, encrypted_credit_value):
	print(f"""The student with name: < {full_name} > and credit value: < {str(credit_value)} > has been encoded in the string:
        <      "{full_name} : {str(encrypted_credit_value)}",      >
Please manually put this without the brackets in the dictionary called 'credit_dictionary' at the top of the 'Credit Decrypt' Python script.\n""")

def main():
	full_name = parse_full_name()
	credit_value = parse_credit_value()
	encrypted_credit_value = encrypt_credit_value(credit_value)
	print_output_to_format(full_name, credit_value, encrypted_credit_value)

print(help)
while True:
	print("We are starting a new student. Start entering the details of the student. Press Ctrl-C to exit.")
	main()
