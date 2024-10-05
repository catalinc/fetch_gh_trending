#!/usr/bin/env python3

import sqlite3
from gtrending import fetch_repos
import argparse


# Connect to SQLite database (or create it if it doesn't exist)
def setup_database():
    conn = sqlite3.connect("trending_repos.db")
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS trending_repos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        url TEXT UNIQUE,
        description TEXT,
        language TEXT,
        stars INTEGER,
        forks INTEGER,
        date DATE DEFAULT (date('now'))
    )
    """
    )
    return conn, cursor


def save_repos_to_db(repos, cursor):
    # Insert or update repository data into the table
    for repo in repos:
        cursor.execute(
            """
        INSERT INTO trending_repos (name, url, description, language, stars, forks)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(url) DO UPDATE SET
            name=excluded.name,
            description=excluded.description,
            language=excluded.language,
            stars=excluded.stars,
            forks=excluded.forks,
            date=excluded.date
        WHERE date('now') - date(trending_repos.date) < 1
        """,
            (
                repo["name"],
                repo["url"],
                repo["description"],
                repo["language"],
                repo["stars"],
                repo["forks"],
            ),
        )


# Main function to fetch GitHub trending repositories and save them to a SQLite database.
# This function uses argparse to handle command-line arguments for specifying the spoken language code,
# programming language, and time range for fetching trending repositories. It then fetches the repositories
# using the gtrending library, sets up the SQLite database, saves the repositories to the database, and
# commits the changes.
# Command-line arguments:
# --spoken_language_code: The spoken language code (default: 'en').
# --language: The programming language (default: empty for all languages).
# --since: The time range for trending repositories (default: 'daily').
# Example usage:
# python fetch_gh_trending.py --spoken_language_code en --language python --since weekly
def main():
    parser = argparse.ArgumentParser(description="Fetch GitHub trending repositories.")
    parser.add_argument(
        "--spoken_language_code",
        type=str,
        default="en",
        help="Spoken language code (default: en)",
    )
    parser.add_argument(
        "--language",
        type=str,
        default="",
        help="Programming language (default: empty for all languages)",
    )
    parser.add_argument(
        "--since", type=str, default="daily", help="Time range (default: daily)"
    )
    args = parser.parse_args()

    repos = fetch_repos(
        spoken_language_code=args.spoken_language_code,
        language=args.language,
        since=args.since,
    )
    print(f"Fetching trending repositories for the time range: {args.since}")
    conn, cursor = setup_database()
    save_repos_to_db(repos, cursor)
    conn.commit()
    conn.close()
    print("Trending repositories have been saved to the database")


if __name__ == "__main__":
    main()
