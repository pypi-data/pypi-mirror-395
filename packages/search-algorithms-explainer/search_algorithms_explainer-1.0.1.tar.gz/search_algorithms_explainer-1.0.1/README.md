# 🔍 Search Algorithms Explainer CLI

[![PyPI version](https://badge.fury.io/py/search-algorithms-explainer.svg)](https://pypi.org/project/search-algorithms-explainer/)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A professional, interactive command-line tool for learning and comparing search algorithms. This project demonstrates Linear Search, Binary Search, and their performance characteristics with real-time step-by-step execution.

## ✨ Features

### 🎯 Interactive CLI Interface
- User-friendly menu system
- Real-time step-by-step algorithm execution
- Direct visualization of how algorithms work

### 🔎 Search Algorithms
- **Linear Search**: Sequential search with O(n) time complexity
- **Binary Search**: Efficient sorted search with O(log n) time complexity
- **Comparison Mode**: Run both algorithms side-by-side with the same data

### 📊 Result Tracking
- Automatic logging of all searches
- Performance metrics (steps taken, time complexity, space complexity)
- Search history with detailed results
- Ability to clear individual results

### 🎨 Flexible Input
- Pre-loaded questions from JSON
- Manual list input
- Inline number entry (e.g., `1 2 3 4`)

## 📦 Installation

### From PyPI (Recommended)

```bash
pip install search-algorithms-explainer
```

### From Source

```bash
# Clone or download the project
cd search-algorithms-explainer

# Install in development mode
pip install -e .

# Or just run directly
python -m search_algorithms
```

### Requirements

- Python 3.7 or higher
- No external dependencies (uses only Python standard library)

## 🚀 Quick Start

### Start Interactive Mode (Default)

```bash
search-algo

# or
python -m search_algorithms

# or
search-algo /start
```

## 📖 Usage

### Available Commands

| Command | Description |
|---------|-------------|
| `search-algo /start` | Start interactive program (default) |
| `search-algo /history` | View all search history |
| `search-algo /clearresult` | Remove last search result |
| `search-algo /end` | Exit program |
| `search-algo --version` or `-v` | Show version |
| `search-algo --help` or `-h` | Show help message |

### Quick Start Guide

1. **Start the program**
   ```bash
   search-algo
   ```

2. **Choose a question** (Q1, Q2, etc.) or enter numbers manually
   ```
   Which question (Q1) or command: Q1
   ```

3. **Select an algorithm**
   ```
   1 - Linear Search
   2 - Binary Search (on sorted list)
   3 - Compare Linear vs Binary
   ```

4. **Enter target number** and watch the algorithm execute step-by-step

5. **View history** at any time with `/history`

### Interactive Mode

```bash
$ search-algo /start

======================================================
 SEARCH ALGORITHMS EXPLAINER
 Version 1.0.0
 Interactive Mode Started
======================================================

--------------------------------------
 Choose question key from JSON (e.g. Q1)
--------------------------------------
Available keys:
Q1  Q2  Q3  Q4  Q5
--------------------------------------
You may type: Q1  OR  manual  OR  numbers directly (e.g. 1 2 3 4)
Type 'exit' to quit.
--------------------------------------
```

### Input Options

| Input Type | Example | Description |
|------------|---------|-------------|
| **Predefined Questions** | `Q1`, `Q2`, `Q3` | Use pre-loaded question data |
| **Manual Input** | `manual` | Enter a custom list manually |
| **Inline Numbers** | `1 2 3 4` | Search in inline-entered numbers |

### Algorithm Options

1. **Linear Search**: Sequential search through the list
2. **Binary Search**: Efficient search on sorted list (automatically sorts input)
3. **Compare Both**: Run both algorithms and compare results side-by-side

## 📊 Example Session

```bash
$ search-algo /start

Which question (Q1) or command: 5 10 15 20 25

Loaded list for 5 10 15 20 25:
List contents:
5 10 15 20 25
--------------------------------------

--------------------------------------
 Choose algorithm:
 1 - Linear Search
 2 - Binary Search (on sorted list)
 3 - Compare Linear vs Binary
 b - Back to choose Q-key
 exit - Quit program
--------------------------------------
Enter choice (1/2/3/b/exit): 3

Enter target number to search: 15

===== Comparing Linear Search vs Binary Search =====

[1] Running Linear Search...

--------- LINEAR SEARCH ---------
Step 1 : index = 0 , element = 5 , target = 15
=> Not equal, moving next

Step 2 : index = 1 , element = 10 , target = 15
=> Not equal, moving next

Step 3 : index = 2 , element = 15 , target = 15
=> Match found
=> Element 15 found at index 2
Total steps taken (Linear Search): 3

[2] Running Binary Search...

--------- BINARY SEARCH ---------
Note: Binary Search works on a sorted list.
Sorted list used:
List contents:
5 10 15 20 25
Step 1 : low = 0 , high = 4 , mid = 2 , element = 15 , target = 15
=> Match found
=> Element 15 found at index 2 (in sorted list)
Total steps taken (Binary Search): 1

----------- SUMMARY -----------
Linear Search  : Found (index 2 in original list)
Binary Search  : Found (index 2 in sorted list)

Steps taken:
  Linear Search  -> 3 steps
  Binary Search  -> 1 steps

Time Complexity:
  Linear Search  -> O(n)
  Binary Search  -> O(log n)  (requires sorted list)
-------------------------------
```

## 📈 View History

```bash
$ search-algo /history

============================================================
 SEARCH HISTORY
============================================================

[1] Question: inline: 5 10 15 20 25
    Method: Linear Search (Compare Mode)
    Result: Found
    Steps: 3
    Time Complexity: O(n)
    Space Complexity: O(1)

[2] Question: inline: 5 10 15 20 25
    Method: Binary Search (Compare Mode)
    Result: Found
    Steps: 1
    Time Complexity: O(log n)
    Space Complexity: O(1)

============================================================
Total entries: 2
============================================================
```

## 🎓 How It Works

### Linear Search

Linear Search examines each element sequentially until finding the target or reaching the end.

- **Time Complexity**: O(n) - must check every element in worst case
- **Space Complexity**: O(1) - no extra space needed
- **Use Case**: Works on unsorted lists, good for small datasets

### Binary Search

Binary Search divides the search space in half repeatedly (requires sorted data).

- **Time Complexity**: O(log n) - halves search space each iteration
- **Space Complexity**: O(1) - no extra space needed
- **Use Case**: Very efficient for large sorted datasets
- **Note**: Algorithm automatically sorts the input for demonstration

### Comparison Mode

Run both algorithms with the same target on the same data to see:
- How many steps each algorithm takes
- Which is more efficient for the given dataset
- Real-time visualization of each algorithm's execution

## 🎓 Learning Objectives

This tool helps you understand:

- How Linear Search works sequentially
- How Binary Search divides the search space
- Time complexity differences (O(n) vs O(log n))
- When to use each algorithm
- Performance comparison with real examples

## 📁 Project Structure

```
search-algorithms-explainer/
├── search_algorithms/          # Main package
│   ├── __init__.py
│   ├── __main__.py            # Entry point
│   ├── config.py
│   ├── core/                  # Core algorithms
│   │   ├── __init__.py
│   │   └── search_algorithms.py
│   ├── cli/                   # Command-line interface
│   │   ├── __init__.py
│   │   ├── menu.py
│   │   └── commands.py
│   └── utils/                 # Utility functions
│       ├── __init__.py
│       ├── data_handler.py
│       └── input_handler.py
├── data/                      # Data files
│   └── questions.json         # Pre-loaded questions
├── bin/                       # Executable scripts
├── setup.py                   # Package setup
├── pyproject.toml            # Modern Python packaging
├── requirements.txt          # Dependencies
├── README.md                 # This file
├── LICENSE                   # MIT License
└── .gitignore               # Git ignore rules
```

## 💾 Result Logging

All search results are automatically saved to `results.json` with:

- Question identifier
- Algorithm used
- Number of steps taken
- Time and space complexity
- Whether target was found

### Example `results.json`

```json
[
    {
        "question": "Q1",
        "method": "Linear Search",
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "steps": 5,
        "found": "Found"
    }
]
```

## 📋 Data Files

### questions.json

Pre-loaded with 30 test questions (Q1-Q30) containing various list configurations:

- Sorted lists
- Reversed lists
- Random lists
- Duplicates
- Special patterns

**Location**: `data/questions.json`

## 🛠️ Development

### Running Tests

```bash
pytest tests/
```

### Code Style

This project follows PEP 8 guidelines. Use these tools:

```bash
# Format code
black search_algorithms/

# Check style
flake8 search_algorithms/
pylint search_algorithms/

# Check types
mypy search_algorithms/
```

## 🤝 Contributing

Contributions are welcome! Feel free to:

- Report bugs
- Suggest new features
- Submit pull requests

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

Created with ❤️ for learning and education

## 🔗 Links

- **PyPI Package**: https://pypi.org/project/search-algorithms-explainer/
- **GitHub Repository**: https://github.com/yourusername/search-algorithms-explainer
- **Documentation**: https://github.com/yourusername/search-algorithms-explainer/wiki
- **Issue Tracker**: https://github.com/yourusername/search-algorithms-explainer/issues

## 🆘 Support

For issues, questions, or suggestions:

- Check existing documentation
- Review example usage
- Create an issue on GitHub
- Contact via email

## 📝 Changelog

### Version 1.0.0 (2024-12-04)

- ✅ Initial release
- ✅ Linear Search implementation
- ✅ Binary Search implementation
- ✅ Comparison mode
- ✅ Result history tracking
- ✅ Professional CLI structure
- ✅ Complete documentation
- ✅ Interactive CLI interface
- ✅ Search history tracking
- ✅ Result logging to JSON
- ✅ Compare mode for algorithms

---

**Happy Learning! 🚀**

Made with ❤️ for education and learning
