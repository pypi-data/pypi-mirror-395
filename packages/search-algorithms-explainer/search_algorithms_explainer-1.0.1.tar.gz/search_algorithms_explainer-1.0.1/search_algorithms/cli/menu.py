"""
Menu display functions for the CLI interface.
"""


def show_main_q_menu(keys):
    """
    Display the main menu where user chooses a question key from JSON.
    
    Args:
        keys (list): List of available question keys.
    """
    print("\n--------------------------------------")
    print(" Choose question key from JSON (e.g. Q1)")
    print("--------------------------------------")

    if len(keys) > 0:
        print("Available keys:")
        line = ""
        count = 0

        for i, key in enumerate(keys):
            line += key + "  "
            count += 1
            if count == 10:
                print(line)
                line = ""
                count = 0

        if line != "":
            print(line)
    else:
        print("No keys loaded from JSON.")

    print("--------------------------------------")
    print("You may type: Q1  OR  manual  OR  numbers directly (e.g. 1 2 3 4)")
    print("Type 'exit' to quit.")
    print("--------------------------------------")


def show_algo_menu():
    """Display the algorithm selection menu."""
    
    print("\n--------------------------------------")
    print(" Choose algorithm:")
    print(" 1 - Linear Search")
    print(" 2 - Binary Search (on sorted list)")
    print(" 3 - Compare Linear vs Binary")
    print(" b - Back to choose Q-key")
    print(" exit - Quit program")
    print("--------------------------------------")