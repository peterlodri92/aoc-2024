import re
import sys

def read_input(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def parse_and_sum_mul_instructions(memory, handle_conditions=False):
    mul_pattern = r'mul\((\d{1,3}),(\d{1,3})\)'
    do_pattern = r'do\(\)'
    dont_pattern = r'don\'t\(\)'

    mul_matches = re.finditer(mul_pattern, memory)
    do_matches = re.finditer(do_pattern, memory)
    dont_matches = re.finditer(dont_pattern, memory)

    total_sum = 0
    is_enabled = True  # start with mul enabled

    # iterators for do() and don't()
    do_iter = iter(do_matches)
    dont_iter = iter(dont_matches)

    # get first do() and don't()
    next_do = next(do_iter, None)
    next_dont = next(dont_iter, None)

    for match in mul_matches:
        x_str, y_str = match.groups()
        x, y = int(x_str), int(y_str)
        product = x * y

        # is current matchbetween a do() and a don't()
        if handle_conditions:
            mul_start = match.start()
            while next_do and mul_start > next_do.start():
                is_enabled = True
                next_do = next(do_iter, None)
            while next_dont and mul_start > next_dont.start():
                is_enabled = False
                next_dont = next(dont_iter, None)

        if is_enabled:
            total_sum += product
            # debugging
            #print(f"Valid mul instruction found: mul({x},{y}) => {product}")

    return total_sum

if __name__ == "__main__":
    memory = read_input('input.txt')

    handle_conditions = '--conditions' in sys.argv

    result = parse_and_sum_mul_instructions(memory, handle_conditions)
    print(f"The total sum of all valid mul instructions is: {result}")
