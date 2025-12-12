"""
Input handling utilities for user interactions.
"""


def take_list_input():
    """
    Take list input from user when user types 'manual'.
    
    Returns:
        list: List of integers entered by the user.
    """
    while True:
        raw = input("\nEnter list of numbers (comma or space separated): ")
        parts = raw.replace(",", " ").split()
        numbers = []
        for part in parts:
            try:
                numbers.append(int(part))
            except Exception:
                print("Please enter only integers. Try again.")
                numbers = []
                break
        if len(numbers) == 0:
            print("List cannot be empty.")
            continue
        return numbers
          

def convert_num(s):
    """
    Try to convert inline input like '1 2 3' or '4,5,6' into list of integers.
    
    Args:
        s (str): Input string to convert.
        
    Returns:
        list or None: List of integers if successful, None otherwise.
    """
    if s.strip() == "":
        return None

    parts = s.replace(",", " ").split()
    nums = []
    for p in parts:
        try:
            nums.append(int(p))
        except Exception:
            return None

    return nums if len(nums) > 0 else None


def take_target_input():
    """
    Ask the user to enter the target number and validate it.
    
    Returns:
        int: The target number to search for.
    """
    while True:
        raw = input("Enter target number to search: ").strip()
        try:
            return int(raw)
        except Exception:
            print("Please enter a valid integer.")


def print_list_plain(arr):
    """
    Print the list in a simple, single-line format.
    
    Args:
        arr (list): List to print.
    """
    output = " ".join(str(x) for x in arr)
    print(f"List contents: {output}")
