#!/usr/bin/env python3
"""
Check if passwords in a file are compromised according to pwnedpasswords.com
"""

import requests
import hashlib
#import colorama
import sys
import getopt


__author__ = "eyetyrant@protonmail.com"
__copyright__ = "2018"
__license__ = "MIT"
__version__ = "1.0.0"
__status__ = "Prototype"


color = False


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
    return pwned_times


def check_password_file(input_file, output_file):
    if output_file == "" or output_file == input_file:
        output_file = "pwned" + input_file
    passwords = []
    try:
        with open(input_file, 'r') as f:
            for row in f:
                pw = row.strip()
                passwords.append((pw, check_password(pw.encode())))
    except IOError:
        print("Could not read file:", input_file)
    return passwords


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
    single_password = None
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
            print(input_file)
        elif option in ("-o", "--ofile"):
            output_file = arg
            print(output_file)
        elif option in ("-c", "--color"):
            output_file = arg
            print(output_file)
        elif option in ("-p", "--password"):
            single_password = arg

    if single_password is not None:
        print(single_password)
        print(check_password(single_password.encode()))
    else:
        print(check_password_file(input_file, output_file))


if __name__ == "__main__":
    main(sys.argv[1:])
    password = "lauragpe"
    # check_password(password)
