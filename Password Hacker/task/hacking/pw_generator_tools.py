import itertools
import os

CHARACTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

def generate_short_password(length):
    for i in range(1, length):
        for pw in itertools.product(CHARACTERS, repeat=i):
            yield "".join(pw)

def generate_from_file(file_name):
    with open(os.path.abspath(file_name), 'r') as f:
        for line in f:
            line = line.strip('\n\r').lstrip(" ")
            if line.isnumeric():
                yield line
            else:
                for length in range(0, len(line) + 1):
                    for to_capitalize_indizes in itertools.combinations(range(len(line)), length):
                        pw = "".join([c.upper() if i in to_capitalize_indizes else c for i, c in enumerate(line.lower())])
                        yield pw


def main():
    pass

if '__name__' == '__main__':
    main()
