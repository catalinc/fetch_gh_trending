# GitHub Trending Repositories Fetcher

This Python script fetches the latest trending repositories from GitHub using the `gtrending` library and saves them to a SQLite database.

## Features

- Fetches trending repositories from GitHub.
- Saves repository details to a SQLite database.
- Creates the database and table if they do not exist.

## Requirements

- Python 3.x
- `gtrending` library
- `sqlite3` library (comes with Python standard library)

## Installation

1. Clone the repository.

2. Install the required libraries:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

1. Run the script
   ```sh
   python3 fetch_gh_trending.py
   ```

2. Open `show_trending_repos.ipynb` and click on "Run All" cells to view statistics.