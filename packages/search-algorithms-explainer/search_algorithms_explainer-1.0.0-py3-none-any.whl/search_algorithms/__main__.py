#!/usr/bin/env python3
"""
Search Algorithms Explainer - Main Entry Point

A comprehensive command-line application for learning and comparing search algorithms.
Supports Linear Search, Binary Search, and performance comparisons.

Usage:
    python -m search_algorithms [command]
    search-algorithms [command]

Commands:
    /start        - Start the interactive program (default)
    /end          - Exit the program
    /history      - Show search history
    /clearresult  - Clear the last search result
    -h, --help    - Show help message
    -v, --version - Show version
"""

import sys
import argparse
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from search_algorithms.utils import load_questions, show_history, clear_last_result
from search_algorithms.cli.commands import process_main_menu
from search_algorithms import __version__


def main():
    """Entry point with argparse for CLI commands."""
    
    parser = argparse.ArgumentParser(
        prog="search-algorithms",
        description="Search Algorithms Explainer - Interactive CLI Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Start interactive mode
  %(prog)s /start             # Start interactive mode
  %(prog)s /history           # Show search history
  %(prog)s /clearresult       # Clear last search result
  %(prog)s -v                 # Show version
        """
    )
    
    parser.add_argument(
        'command',
        nargs='?',
        default='/start',
        help='Command: /start (default), /end, /history, /clearresult'
    )
    
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )
    
    args = parser.parse_args()
    command = args.command.lower()
    
    # Handle commands
    if command == '/start':
        print("\n" + "="*60)
        print(" SEARCH ALGORITHMS EXPLAINER")
        print(f" Version {__version__}")
        print(" Interactive Mode Started")
        print("="*60)
        
        # Load questions from data directory
        questions_file = Path(__file__).parent.parent / "data" / "questions.json"
        questions = load_questions(str(questions_file))
        
        if not questions:
            print("\n❌ Error: Could not load questions.json")
            print(f"   Expected file at: {questions_file}")
            sys.exit(1)
        
        process_main_menu(questions)
        
    elif command == '/end':
        print("\n" + "="*60)
        print(" Program terminated")
        print("="*60)
        sys.exit(0)
        
    elif command == '/history':
        show_history()
        
    elif command == '/clearresult':
        clear_last_result()
        
    else:
        print(f"\n❌ Unknown command: {command}")
        print("\nAvailable commands:")
        print("  /start        - Start the interactive program")
        print("  /end          - Exit the program")
        print("  /history      - Show search history")
        print("  /clearresult  - Clear the last search result")
        print("\nUse -h or --help for more information")
        sys.exit(1)


if __name__ == "__main__":
    main()