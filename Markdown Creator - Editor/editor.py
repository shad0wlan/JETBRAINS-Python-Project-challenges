# write your code here
formatters = "plain bold italic header link inline-code new-line unordered-list ordered-list".split(" ")

def plain():
    input_text = input("Text:")
    return input_text.strip()


def bold():
    input_text = input("Text:")
    return f'**{input_text}**'.strip()


def italic():
    input_text = input("Text:")
    return f'*{input_text}*'.strip()


def header():
    while True:
        input_level = input("Level:")
        if int(input_level) < 1 or int(input_level) > 6:
            print("The level should be within the range of 1 to 6")
            continue
        else:
            break

    input_text = input("Text:")

    return f'{"#" * int(input_level)} {input_text}\n'


def inline_code():
    input_text = input("Text:")
    return f"`{input_text}`".strip()


def new_line():
    return f'\n'


def link():
    input_label = input("Label:")
    input_text = input("URL:")
    return f'[{input_label}]({input_text})'


def rows_checker():
    while True:
        input_rows = int(input("Number of rows:"))
        if input_rows <= 0:
            print("The number of rows should be greater than zero")
            continue
        return input_rows


def ordered_list():
    list_array = []
    rows = rows_checker()
    for i in range(1, rows + 1):
        row = input(f'Row #{i}:')
        list_array.append(f'{i}. {row}\n')
    return list_array


def unordered_list():
    list_array = []
    rows = rows_checker()
    for i in range(1, rows + 1):
        row = input(f'Row #{i}:')
        list_array.append(f'* {row}\n')
    return list_array


function_formatter = [plain,  bold, italic, header, link, inline_code, new_line, unordered_list, ordered_list]


def main():
    string_saver = []
    while True:
        x = input("Choose a formatter: ")
        if x == "!help":
            print(f'Available formatters: {" ".join(formatters)}\nSpecial commands: !help !done')
            continue
        if x == "!done":
            with open("output.md", "w") as f:
                f.write("".join(string_saver))
            break
        if x not in formatters:
            print("Unknown formatting type or command")
            continue
        answer = function_formatter[formatters.index(x)]()
        string_saver += answer
        print("".join(string_saver))


if __name__ == "__main__":
    main()