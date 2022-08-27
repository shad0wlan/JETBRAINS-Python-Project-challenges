# write your code here

comparison = input().split("|")
first = comparison[0]
second = comparison[1]
is_a_match = False  # Keep track of lengths in order to continue the Iterations from the different lengths function if b is bigger
match_start = False  # Keep track of ^
match_end = False  # Keep track of $
appeared_more = False  # Tracking the appearances of ? and *
is_escaped = False  # We keep track of the escaping

def single_character_strings(a, b):
    if a == "." or a == b or not a:
        return True
    else:
        return False


# Main function for equalities
def equal_length_strings(a, b, n=0):
    global match_start
    global is_a_match
    global match_end
    global appeared_more
    global is_escaped
    is_escaped = False

    if n == len(a):
        return True

    # Checking if current char of regex is escaped
    try:
        if a[n] == "\\".strip():
            is_escaped = True
            if a[n + 1] == b[n]:
                return equal_length_strings(a[n + 1:], b[n:], n + 1)
            else:
                return equal_length_strings(a[n:], b, n + 1)

    # If a > b we assist it with the exception to continue the equality tests without moving to other function
    except IndexError:
        if not single_character_strings(a[n + 1], b[n]):
            return False
        else:
            return equal_length_strings(a[n + 1], b[n:], n + 1)

    if not b:
        return False

    # Ensuring our regex is matching the end of string
    if a[n] == "$" and is_a_match and n == len(b):
        match_end = True
        return True

    if n > len(b):
        return False

    # Ensuring our string starts according to the regex
    if a[n] == "^":
        match_start = True
        return equal_length_strings(a[n + 1:], b)

    # Handling ? and + and "." if it is preceding those characters if we already have a match and they are not escaped
    if a[n] == "?" or a[n] == "+" and not is_escaped:
        if a[n] == "?":
            appeared_more = True
        if a[n] == "+":
            indexes_jumped = 0
            current_b = b[n]
            counters = 0

            for i in b[n:]:
                if a[n - 1] == ".":
                    if i == current_b:
                        counters += 1
                        continue
                    else:
                        return equal_length_strings(a[n:], b[counters + 1:], n - 1)

                if i == a[n - 1]:
                    indexes_jumped += 1
                    continue

                if indexes_jumped > 1:
                    return equal_length_strings(a[n:], b[indexes_jumped + 1:], n - 1)

                else:
                    try:
                        if i == a[n + 1]:
                            return equal_length_strings(a[n + 1:], b[n:], 0)
                    except IndexError:
                        pass

                return equal_length_strings(a[n:], b[indexes_jumped + 1:], n - 1)

        return equal_length_strings(a[:n-1] + a[n:], b[: n] + b[n:], n)


    # Handling * and + and "+" if it is preceding those characters if we already have a match and they are not escaped

    if a[n] == "*" or a[n] == "+" and not is_escaped:
        get_index = n

        try:
            while single_character_strings(a[n - 1], b[get_index - 1]):
                if a[n - 1] == b[get_index - 1]:
                    get_index += 1
                    continue

                if a[n - 1] == ".":
                    if b[get_index - 1] != b[n - 1]:
                        return equal_length_strings(a[n + 1], b[get_index:])

                    else:
                        get_index += 1
                        continue
        except IndexError:
            return True
        return equal_length_strings(a[n + 1:], b[get_index - 1:])

    if single_character_strings(a[n], b[n]):

        is_a_match = True

        return equal_length_strings(a, b, n + 1)

    else:
        # Handling escapes that without switching functions
        try:
            if a[n + 1] == "\\".strip():
                is_escaped = True
                if a[n + 1] == b[n]:
                    return equal_length_strings(a[n + 1:], b[n:], n + 1)
                else:
                    return False
        except IndexError:
            return False

        # Handling ? and * that are one index ahead from string
        for i in a[n:]:
            if i == "?" or i == "*" and not is_escaped:
                if a[n] != b[n]:
                    return equal_length_strings(a[:n] + a[n + 2:], b, 0)

        is_a_match = False

        return False


# Assistive function to manage b > a
def different_lengths(a, b, n=0):
    global is_a_match

    if not a and not b or not a:
        return True

    if n > len(b) - 1:
        return False

    check_for_equal_first = equal_length_strings(a, b[n:])
    if check_for_equal_first:
        return True
    if not check_for_equal_first and not match_start and not appeared_more:  #We increase index of string and not of regex
        return different_lengths(a, b, n + 1)
    else:
        return False


print(different_lengths(first, second))

