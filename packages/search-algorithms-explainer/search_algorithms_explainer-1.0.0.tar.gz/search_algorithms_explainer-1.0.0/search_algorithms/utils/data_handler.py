"""
Data handling utilities for file I/O and result logging.
"""

import json
import os
from pathlib import Path

# Default paths
RESULTS_FILE = "results.json"
QUESTIONS_FILE = "data/questions.json"


def load_questions(filename):
    """
    Load questions from a JSON file and return as a dictionary.
    
    Args:
        filename (str): Path to the JSON file containing questions.
        
    Returns:
        dict: Dictionary of questions, or empty dict if load fails.
    """
    if not os.path.exists(filename):
        print(f"Warning: {filename} not found.")
        return {}
    
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except Exception as e:
        print(f"Error: Unable to read '{filename}': {e}")
        return {}
    
    if not isinstance(data, dict):
        print("Error: JSON must contain key-value pairs.")
        return {}

    return data


def save_result(question, method, steps, time_complexity, space_complexity, found):
    """
    Save one result entry into results.json as a list of records.
    
    Args:
        question (str): Question identifier (e.g., "Q1", "manual", "inline: 1 2 3")
        method (str): Search method used ("Linear Search", "Binary Search", etc.)
        steps (int): Number of steps taken during search.
        time_complexity (str): Time complexity (e.g., "O(n)", "O(log n)")
        space_complexity (str): Space complexity (e.g., "O(1)")
        found (bool): Whether the target was found.
    """
    entry = {
        "question": question,
        "method": method,
        "time_complexity": time_complexity,
        "space_complexity": space_complexity,
        "steps": steps,
        "found": "Found" if found else "Not Found"
    }

    # Load existing data (if any)
    data = []
    if os.path.exists(RESULTS_FILE):
        try:
            with open(RESULTS_FILE, "r", encoding="utf-8") as f:
                old = json.load(f)
                if isinstance(old, list):
                    data = old
        except Exception:
            data = []

    data.append(entry)

    # Save back to file
    try:
        with open(RESULTS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Warning: Could not write to results.json: {e}")


def show_history():
    """Display the history of all searches from results.json"""
    
    print("\n" + "="*60)
    print(" SEARCH HISTORY")
    print("="*60)
    
    if not os.path.exists(RESULTS_FILE):
        print("No history found. The results file doesn't exist yet.")
        print("="*60)
        return
    
    try:
        with open(RESULTS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            
            if not isinstance(data, list) or len(data) == 0:
                print("No search results found in history.")
                print("="*60)
                return
            
            for idx, entry in enumerate(data, 1):
                print(f"\n[{idx}] Question: {entry.get('question', 'N/A')}")
                print(f"    Method: {entry.get('method', 'N/A')}")
                print(f"    Result: {entry.get('found', 'N/A')}")
                print(f"    Steps: {entry.get('steps', 'N/A')}")
                print(f"    Time Complexity: {entry.get('time_complexity', 'N/A')}")
                print(f"    Space Complexity: {entry.get('space_complexity', 'N/A')}")
            
            print("\n" + "="*60)
            print(f"Total entries: {len(data)}")
            print("="*60)
            
    except Exception as e:
        print(f"Error reading history: {e}")
        print("="*60)


def clear_last_result():
    """Remove the last entry from results.json"""
    
    if not os.path.exists(RESULTS_FILE):
        print("\n❌ No results file found. Nothing to clear.")
        return
    
    try:
        with open(RESULTS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            
            if not isinstance(data, list) or len(data) == 0:
                print("\n❌ No results found in history. Nothing to clear.")
                return
            
            # Get the last entry before removing
            last_entry = data[-1]
            
            # Remove the last entry
            data = data[:-1]
            
            # Save back
            with open(RESULTS_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            
            print("\n✓ Last result cleared successfully!")
            print(f"  Removed: Question '{last_entry.get('question', 'N/A')}' - Method '{last_entry.get('method', 'N/A')}'")
            print(f"  Remaining entries: {len(data)}")
            
    except Exception as e:
        print(f"\n❌ Error clearing last result: {e}")