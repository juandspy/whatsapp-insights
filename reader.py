import io
import pandas as pd
import re
from tqdm import tqdm

DATE_REGEX = "^[0-9]{1,2}\/[0-9]{1,2}\/[0-9]{2}\s[0-9]{1,2}:[0-9]{1,2}"

def check_contains(input: str, pattern: str) -> bool:
    """Return true if the input string contains the RegEx pattern"""
    return re.search(pattern, input) is not None

def chat_to_df(input_io: io.BytesIO) -> pd.DataFrame:
    """
    Parses a Whatsapp exported chat into a Pandas Dataframr
    containing `date, user, message` columns.
    """
    lines = input_io.readlines()
    # Each line has the format:
    # DD/MM/YY HH:mm - USER: MESSAGE

    if not check_contains(lines[0], DATE_REGEX):
        print("The first line of the file doesn't contain a valid format")
        exit()

    parsed_lines = []

    print("Reading the file:")
    for line in tqdm(lines):
        # Check if the line starts with a date, if not append it to previous message
        if not check_contains(line, DATE_REGEX):
            parsed_lines[-1][2] += "\n" + line.rstrip()
            continue
        # Parse the line and append it to `parsed_lines`
        try:
            date = line.split("-")[0]
            user = line.split("-")[1].split(":")[0]
            message = line.split(":")[2].rstrip()
            parsed_lines.append([date, user, message])
        except IndexError:
            tqdm.write(f"Cannot split the line correctly: {line}")

    df = pd.DataFrame(parsed_lines,
        columns =['date', 'user', 'message'])
    df["date"] = pd.to_datetime(df["date"])
    return df

if __name__ == "__main__":
    INPUT_FILE =  "input.txt"
    with open(INPUT_FILE, "r", encoding="utf8") as f:
        df = chat_to_df(f)
    print(df)