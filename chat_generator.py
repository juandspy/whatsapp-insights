"""This file is used to generate a sample conversation
It can be run as 
    python chat_generator.py > input.txt
"""

from datetime import datetime, timedelta
import random

NUM_MESSAGES = 1000
NUM_USERS = 3
users = [f"User_{i}" for i in range(NUM_USERS)]
WORDS = ["Hello", "there", "How", "are", "you", "I'm", "fine", "thank", "you"]
WORDS_PER_MESSAGE = 4

START_DATE = datetime(2021, 1, 1)
END_DATE = datetime(2022, 1, 1)
time_between_dates = END_DATE - START_DATE
days_between_dates = time_between_dates.days

def get_random_date():
    random_number_of_days = random.randrange(days_between_dates)
    random_date = START_DATE + timedelta(
        days=random_number_of_days,
        hours=random.randint(0, 24), 
        minutes=random.randint(0, 60)
    )
    return random_date

lines = []
for i in range(NUM_MESSAGES):
    date = get_random_date()
    date_str = date.strftime("%-d/%-m/%-y %-H:%M")
    user = random.choice(users)
    message = " ".join(random.sample(WORDS, WORDS_PER_MESSAGE))
    line = f"{date_str} - {user}: {message}"
    print(line)
