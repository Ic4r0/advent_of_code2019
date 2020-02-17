"""--- Day 4: Secure Container - Part One ---"""

MIN_RANGE = 245318
MAX_RANGE = 765747

# Check if there are at least 2 adjacent equal digits
def check_repetitions(number: int):
    str_number = str(number)
    for i in range(len(str_number) - 1):
        if str_number[i] == str_number[i + 1]:
            return True
    return False

# Check if each digit of the number is in increasing order
def check_increasing_digits(number: int):
    str_number = str(number)
    for i in range(len(str_number) - 1):
        if str_number[i] > str_number[i + 1]:
            return False
    return True

# Check if the number follows the rules
def check_correctness(number: int):
    return check_repetitions(number) and check_increasing_digits(number)

# Check each number in a given range
correct_passwd = []
for password in range(MIN_RANGE, MAX_RANGE + 1):
    if check_correctness(password):
        correct_passwd.append(password)

# Print the result
print(len(correct_passwd))
