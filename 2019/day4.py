def digits_never_decrease(s: str) -> bool:
    for i in range(len(s)-1):
        if int(s[i]) > int(s[i+1]):
            return False
    return True

def has_matching_adjacent_digits(s: str) -> bool:
    for i in range(len(s)-1):
        if s[i] == s[i+1]:
            return True
    return False

def has_only_two_matching_digits(s: str) -> bool:
    for i in range(len(s)-1):
        if s[i] == s[i+1]:
            if i > 0 and s[i-1] == s[i]:
                # prior digit also matches, throw it out
                pass
            elif i < len(s)-2 and s[i+2] == s[i]:
                # digit after also matches, throw it out
                pass
            else:
                return True
    return False

def is_valid_password(s: str, part_two=False) -> bool:
    if len(s) != 6:
        return False
    if not has_matching_adjacent_digits(s):
        return False
    if not digits_never_decrease(s):
        return False
    if part_two and not has_only_two_matching_digits(s):
        return False

    return True

print("Test inputs:")
test_input = ["111111", "223450", "123789"]
for i in test_input:
    print("Is {} valid? {}".format(i, is_valid_password(i)))

print()

valid_password_count = 0
for i in range(123257,647016):
    if is_valid_password(str(i)):
        valid_password_count = valid_password_count + 1
print("Valid passwords (part1): {}".format(valid_password_count))

valid_password_count = 0
for i in range(123257,647016):
    if is_valid_password(str(i), part_two=True):
        valid_password_count = valid_password_count + 1
print("Valid passwords (part2): {}".format(valid_password_count))
