# moneycounter 💸

A Python-based desktop application designed for efficiently counting cash by guiding the user through each denomination.

## Badges 🛡️

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Description 📝

The `moneycounter` project is a user-friendly desktop application built with Python and Tkinter. It simplifies the process of counting cash by providing a guided, step-by-step interface for each denomination of coins and bills. The application features a clean, dark-themed UI, tracks running totals, and allows users to save their count history to a local SQLite database.

## Table of Contents 📋

- [Project Title & Badges](#moneycounter-%F0%9F%92%B5)
- [Description](#description-%F0%9F%97%92%EF%B8%8F)
- [Table of Contents](#table-of-contents-%F0%9F%97%92%EF%B8%8F)
- [Features](#features-%E2%9C%A8)
- [Tech Stack](#tech-stack-%F0%9F%AA%A7)
- [Installation](#installation-%E2%9A%99%EF%B8%8F)
- [Usage](#usage-%E2%9A%A1%EF%B8%8F)
- [How to Use](#how-to-use-%E2%9A%A1%EF%B8%8F)
- [Project Structure](#project-structure-%F0%9F%93%81)
- [Contributing](#contributing-%F0%9F%94%8D)
- [License](#license-%F0%9F%93%9C)
- [Important Links](#important-links-%F2%9C%8B)
- [Footer](#footer-%F0%9F%97%91%EF%B8%8F)

## Features ✨

- **Guided Denomination Entry**: Step-by-step input for each coin and bill denomination.
- **Loose & Roll Counting**: Supports counting loose coins and rolls of coins.
- **Real-time Totals**: Displays a running total of the cash counted.
- **Dark Theme UI**: A modern and comfortable dark interface.
- **SQLite Database Integration**: Saves count history to a local `money_counter.db` file.
- **Review & Save**: Allows users to review their final count before saving.
- **Count History**: View past cash counts stored in the database.
- **Reset Functionality**: Option to clear current count and start over.

## Tech Stack 💻

- **Language**: Python
- **GUI Toolkit**: Tkinter
- **Database**: SQLite

## Installation 🛠️

This project is a standalone Python script and does not have external dependencies beyond the standard Python library.

1.  **Clone the repository (if applicable):**
    ```bash
    git clone https://github.com/mrjohndowe/moneycounter.git
    cd moneycounter
    ```
2.  **Ensure Python is installed:**
    Make sure you have Python 3.9 or later installed on your system.

## Usage 🚀

This application is designed to help users quickly and accurately count cash by prompting them for the quantity of each denomination. It's ideal for cashiers, small businesses, or anyone needing to reconcile physical currency.

## How to Use 💡

1.  **Run the application:**
    Navigate to the project directory in your terminal and run the Python script:
    ```bash
    python money_counter.py
    ```
2.  **Enter Denominations:**
    - The application will present each denomination (e.g., Penny, Nickel, $1 Bill) one by one.
    - For coins, you will input the number of **loose coins** and the number of **rolls** (with the count per roll specified).
    - For bills, you will input the **quantity** of each bill.
    - Use the input fields and press Enter or click 'SAVE & NEXT' to proceed.
    - Use the '‹ PREVIOUS' button to go back to a previous denomination.
3.  **Review and Save:**
    - Once all denominations are entered, click 'REVIEW FINAL COUNT'.
    - A summary table will display the breakdown of your count.
    - Click 'SAVE FINAL COUNT' to store the result in the `money_counter.db` SQLite database.
4.  **View History:**
    - From the main screen, access the 'Cash Count History' to view previous saved counts.
5.  **Reset:**
    - Click 'RESET ALL' to clear the current count and start a new one.

## Project Structure 📁

```
moneycounter/
├── README.md
├── money_counter.db
└── money_counter.py
```

-   `README.md`: This file containing project information.
-   `money_counter.db`: SQLite database file to store count history.
-   `money_counter.py`: The main Python script containing the application logic and UI.

## Contributing 🤝

Contributions are welcome! If you have suggestions for improvements or find bugs, please feel free to:

-   Fork the repository.
-   Create a new branch (`git checkout -b feature/your-feature-name`).
-   Make your changes.
-   Commit your changes (`git commit -m 'Add some feature'`).
-   Push to the branch (`git push origin feature/your-feature-name`).
-   Open a Pull Request.

Please ensure your code adheres to Python best practices.

## License 📄

This project is licensed under the MIT License - see the [LICENSE](https://opensource.org/licenses/MIT) file for details.

## Important Links 🔗

-   [Repository URL](https://github.com/mrjohndowe/moneycounter)

## Footer 📝

© 2023 moneycounter. All rights reserved.

This project is maintained by [mrjohndowe](https://github.com/mrjohndowe).

--- 

**Like this project?** Star it ⭐ | Fork it 🍴 | Report Issues 🐞


---
**<p align="center">Generated by [ReadmeCodeGen](https://www.readmecodegen.com/)</p>**