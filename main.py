import os

import datetime
import random
import time
import holidays
from git import Repo

# Path to the local GitHub repository
REPO_PATH = "/home/ubuntu/github-faker"
# Path to the file to update
FILE_PATH = os.path.join(REPO_PATH, "daily_update.txt")

# German holidays
german_holidays = holidays.Germany()


def is_commit_day():
    """Determine if today is a valid commit day."""
    today = datetime.date.today()
    # Check if today is a holiday
    if today in german_holidays:
        return False
    # Always commit on weekdays (Monday to Friday)
    if today.weekday() < 5:  # Monday to Friday (0 to 4)
        return True
    # 20% chance to commit on Saturday (5) or Sunday (6)
    return random.random() < 0.2  # 20% chance for weekends


def random_time_delay():
    """Introduce random delay between commits to simulate realistic activity."""
    time.sleep(random.randint(1, 1800))  # Delay between 1 second and 30 minutes
    

def update_file():
    """Update a file in the repository."""
    with open(FILE_PATH, "a") as file:
        file.write(f"Updated on: {datetime.datetime.now()}\n")


def commit_and_push(repo_path, num_commits):
    """Create multiple commits and push them to GitHub."""
    repo = Repo(repo_path)
    for _ in range(num_commits):
        update_file()
        repo.git.add(FILE_PATH)
        repo.index.commit(f"Commit: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        random_time_delay()
    origin = repo.remote(name="origin")
    origin.push(refspec="main:main")


if __name__ == "__main__":
    if is_commit_day():
        # Generate a random number of commits (1 to 10)
        num_commits = random.randint(1, 10)
        print(f"Committing {num_commits} times to {REPO_PATH}...")
        try:
            commit_and_push(REPO_PATH, num_commits)
            print("Changes pushed successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("Today is not a commit day. No commits will be made.")
