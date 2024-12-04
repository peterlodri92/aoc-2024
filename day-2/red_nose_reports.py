import argparse
from typing import List

def is_safe(report_levels: List[int]) -> bool:
    if not (report_levels := list(report_levels)) or len(report_levels) < 2:
        # if the report is empty or has only one level -> safe
        return True

    previous_level = report_levels[0]
    direction = None

    for level in report_levels[1:]:
        diff = level - previous_level
        if diff == 0 or diff not in range(-3, 4):
            return False

        match direction:
            case None:
                direction = diff > 0
            case True:  # inc
                if diff < 0:
                    return False
            case False:  # dec
                if diff > 0:
                    return False

        previous_level = level

    return True

def is_safe_with_dampener(report_levels: List[int]) -> bool:
    if is_safe(report_levels):
        return True

    for i in range(len(report_levels)):
        # remove one level at a time and check if the new report is safe
        if is_safe(report_levels[:i] + report_levels[i+1:]):
            return True

    return False

def main():
    parser = argparse.ArgumentParser(description="Analyze reports for safety.")
    parser.add_argument('--dampener', action='store_true', help='Enable the Problem Dampener to allow one bad level to be ignored.')
    args = parser.parse_args()

    safe_count = 0
    unsafe_count = 0
    with open('input.txt', 'r') as file:
        for line_number, line in enumerate(file, start=1):
            report_levels = list(map(int, line.strip().split()))
            if (args.dampener and is_safe_with_dampener(report_levels)) or (not args.dampener and is_safe(report_levels)):
                safe_count += 1
            else:
                # print(f"UNSAFE report on line {line_number}: {report_levels}")
                unsafe_count += 1

    print(f"SAFE: {safe_count}")
    print(f"UNSAFE: {unsafe_count}")
    print(f"Total Reports: {safe_count + unsafe_count}")

if __name__ == "__main__":
    main()
