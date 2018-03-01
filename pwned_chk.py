#!/usr/bin/env python3
"""
Check if passwords in a file are compromised according to pwnedpasswords.com
"""

import requests
import hashlib
import sys
import getopt
from colorama import init, Fore, Back, Style
init()

__author__ = "eyetyrant@protonmail.com"
__copyright__ = "2018"
__license__ = "MIT"
__version__ = "1.0.0"
__status__ = "Prototype"


def check_password(pw):
    URL = "https://api.pwnedpasswords.com/range/"
    pwned_times = 0
    pw_hash = hashlib.sha1(pw).hexdigest()
    prefixe = pw_hash[:5].upper()
    suffixe = pw_hash[5:].upper()
    response = requests.get(URL + prefixe).text
    response = response.split("\r\n")

    for line in response:
        potential_suffixe, count = line.split(":")
        if suffixe.strip() == potential_suffixe.strip():
            pwned_times = count
    return int(pwned_times)


def check_password_file(input_file, output_file):
    passwords = {}
    try:
        with open(input_file, 'r') as f:
            for row in f:
                pw = row.strip()
                passwords[pw] = check_password(pw.encode())
    except IOError:
        print("Could not read file:", input_file)
    return passwords


def print_passwords(pw_dictionary, color=False):
    print("\nPassword" + " "*32 + "Pwned count")
    for password in sorted(pw_dictionary):
        spacing = " "
        if len(password) < 39:
            spacing *= (40-len(password))

        pw_text = password + spacing + str(pw_dictionary[password])
        if color:
            if pw_dictionary[password] == 0:
                print(Fore.GREEN + pw_text)
            else:
                print(Fore.RED + pw_text)
        else:
            print(pw_text)
    print(Style.RESET_ALL)


def write2file(pw_dictionary, file):
    try:
        with open(file, 'w') as f:
            [f.write('{0},{1}\n'.format(pw, count)) for pw, count in
                pw_dictionary.items()]
    except IOError as e:
        print("Could not write file:", file)
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
    except:
        print("Unexpected error:", sys.exc_info()[0])


def usage():
    print("Usage:")
    print("python pwned_chk.py -p <password>")
    print("python pwned_chk.py -i <input_password_file>"
          "[-o <output_password_file>]")
    print("\nArguments:")
    print("-i <input_password_file>   --input=<input_password_file>       "
          "Text file containing one password per line")
    print("-o <ouput_password_file>   --output=<input_password_file>      "
          "Output file for pwned passwords")
    print("-p                         --password=<password>               "
          "Single passowd test")
    print("-c                         --color                             "
          "Color output")
    print("-h                         --help                              "
          "HELP!")


def main(argv):
    input_file = ""
    output_file = ""
    single_password = ""
    color = False
    try:
        options, args = getopt.getopt(argv, "hcp:i:o:", ["input=", "output="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for option, arg in options:
        if option in ("-h", "--help"):
            usage()
            sys.exit()
        elif option in ("-i", "--ifile"):
            input_file = arg
        elif option in ("-o", "--ofile"):
            output_file = arg
        elif option in ("-c", "--color"):
            color = True
        elif option in ("-p", "--password"):
            single_password = arg

    if output_file == "" or output_file == input_file:
        output_file = "pwned_" + input_file

    if single_password != "":
        pw_count = check_password(single_password.encode())
        pw_text = "The password " + single_password
        if pw_count == 0:
            pw_text += " has not been pwned according to haveibeenpwned.com."
        else:
            pw_text += " has been pwned " + str(pw_count) + " times."
        print(pw_text)
    elif input_file != "":
        passwords_found = check_password_file(input_file, output_file)
        print_passwords(passwords_found, color)
        write2file(passwords_found, output_file)
    else:
        usage()
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])
