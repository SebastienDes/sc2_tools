# sc2_tools
## Breakdown of the Structure
- **data/:** This directory holds all the datasets we will use, such as player information, current standings, and winning probabilities. Using JSON for qualitative data and CSV for quantitative data like standings and probabilities makes accessing and processing these data types efficient.
- **docs/:** Documentation to explain the purpose of this project, its structure, and how to use it.
- **src/:** Contains all our Python code.
    - **`__init__.py`:** Marks the directory as a Python package, allowing us to import between files.
    - **`main.py`:** The entry point of our program, which calls functions from other files.
    - **`analysis.py`:** Contains functions and classes that implement the qualification scenarios and outcome calculations.
    - **`data_loader.py`:** Handles loading and preprocessing data from the data directory.
    - **`visualization.py`:** Functions to visualize data and results, useful for making the impact of each match clear.
- **tests/:** Contains tests for our application, ensuring our analysis functions work as expected under various scenarios.
    - **`__init__.py`:** Marks the directory as a Python package.
    - **`test_analysis.py`** and **`test_data_loader.py`:** These scripts are used to test our logic and data handling, respectively.
- **requirements.txt:** Lists the project’s dependencies. This makes setting up the project on a new machine straightforward using **`pip install -r requirements.txt`.**
- **README.md:** Provides an introduction to our project, setup instructions, and how to run the code, along with any other necessary information for users or contributors to get started.
- **CHANGELOG.md** and **VERSION:** Respectively describes what was changed, added, or fixed in the repository, and contains the current version of the project.
