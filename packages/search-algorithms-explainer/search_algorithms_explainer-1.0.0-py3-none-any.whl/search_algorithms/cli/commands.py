"""
Command processing functions for the CLI interface.
"""

from ..core.search_algorithms import linear_search, binary_search
from ..utils import save_result, take_target_input, print_list_plain


def process_algo_menu(arr, question_label):
    """
    Process user's algorithm selection and run the selected algorithm.
    
    Args:
        arr (list): The list to search in.
        question_label (str): Label for the question (for logging).
        
    Returns:
        bool: True if user wants to go back, False if user wants to exit.
    """
    while True:
        from .menu import show_algo_menu
        show_algo_menu()
        algo = input("Enter choice (1/2/3/b/exit): ").strip().lower()

        if algo == "b":
            return True  # Go back

        elif algo == "exit":
            return False  # Exit program

        elif algo == "1":
            # Linear search
            target = take_target_input()
            index, steps = linear_search(arr, target)
            found = index != -1

            save_result(
                question=question_label,
                method="Linear Search",
                time_complexity="O(n)",
                space_complexity="O(1)",
                steps=steps,
                found=found
            )

            input("Press Enter to continue...")

        elif algo == "2":
            # Binary search
            target = take_target_input()
            index, steps = binary_search(arr, target)
            found = index != -1

            save_result(
                question=question_label,
                method="Binary Search",
                time_complexity="O(log n)",
                space_complexity="O(1)",
                steps=steps,
                found=found
            )

            input("Press Enter to continue...")

        elif algo == "3":
            # Compare Linear vs Binary
            target = take_target_input()
            print("\n===== Comparing Linear Search vs Binary Search =====")
            print("Same list and same target will be used for both.\n")

            print("[1] Running Linear Search...\n")
            index_lin, steps_lin = linear_search(arr, target)
            found_lin = index_lin != -1

            save_result(
                question=question_label,
                method="Linear Search (Compare Mode)",
                time_complexity="O(n)",
                space_complexity="O(1)",
                steps=steps_lin,
                found=found_lin
            )

            print("\n[2] Running Binary Search...\n")
            index_bin, steps_bin = binary_search(arr, target)
            found_bin = index_bin != -1

            save_result(
                question=question_label,
                method="Binary Search (Compare Mode)",
                time_complexity="O(log n)",
                space_complexity="O(1)",
                steps=steps_bin,
                found=found_bin
            )

            print("\n----------- SUMMARY -----------")
            if found_lin:
                print(f"Linear Search  : Found (index {index_lin} in original list)")
            else:
                print("Linear Search  : Not found")

            if found_bin:
                print(f"Binary Search  : Found (index {index_bin} in sorted list)")
            else:
                print("Binary Search  : Not found")

            print("\nSteps taken:")
            print(f"  Linear Search  -> {steps_lin} steps")
            print(f"  Binary Search  -> {steps_bin} steps")

            print("\nTime Complexity:")
            print("  Linear Search  -> O(n)")
            print("  Binary Search  -> O(log n)  (requires sorted list)")
            print("-------------------------------")
            input("Press Enter to go back...")

        else:
            print("Invalid choice. Enter 1, 2, 3, b, or exit.")


def process_main_menu(questions):
    """
    Process the main menu loop for choosing question keys and algorithms.
    
    Args:
        questions (dict): Dictionary of available questions.
        
    Returns:
        bool: True if user exited normally, False otherwise.
    """
    from .menu import show_main_q_menu
    from ..utils import convert_num, take_list_input

    keys = list(questions.keys())

    while True:
        show_main_q_menu(keys)
        raw_choice = input("Which question (Q1) or command: ").strip()

        if raw_choice == "":
            continue

        low = raw_choice.lower()

        if low in ("exit", "quit"):
            print("Goodbye!")
            return True

        # Handle manual / inline / Q1, Q2 etc
        if low == "manual":
            arr = take_list_input()
            question_label = "manual"

        else:
            parsed = convert_num(raw_choice)

            if parsed is not None:
                arr = parsed
                question_label = "inline: " + raw_choice

            elif raw_choice in questions:
                arr = questions[raw_choice]
                question_label = raw_choice

            else:
                print(f"\n❌ Invalid key or input: {raw_choice}")
                continue

        # Print loaded list
        print(f"\nLoaded list for {raw_choice}:")
        print_list_plain(arr)
        print("--------------------------------------")

        # Process algorithm menu
        should_continue = process_algo_menu(arr, question_label)
        if not should_continue:
            return False  # User exited from algo menu