import re


def condense_spaces(s: str, separator=" "):
    """Replaces all occurrences of multiple whitespace characters in a string
    
    with a underscore character.

    Args:
        s (str): The input string.

    Returns:
        str: The input string with multiple whitespace characters replaced by a single whitespace character.
    """
    return re.sub(r'\s{2,}', separator, s)


def parse_goal_event_string(text: str) -> tuple[str, list[str]]:
    """Extract player name, event times from event text.
    
    Example:
        "James Ward-Prowse 90 +3' (pen) label.penalty.scored"
        "Shandon Baptiste 90 +2' Second Yellow Card (Red Card)"
        "Matheus Nunes 90 +10' Red Card"
        "Bukayo Saka 43', 74' Goal"
        "Phil Foden 8', 44', 73' Goal"

    """
    def help_transform(text: str):
        mapping = {
            " ": "",
            "'": "",
        }
        trans_table = str.maketrans(mapping)
        return text.translate(trans_table)

    player_pattern = r"^[A-Za-z\s-]+"
    minute_pattern = r"\b[\d\s\+]+'"
    label_pattern = r"Goal|\(pen\)"
    is_goal = re.search(label_pattern, text)
    if not is_goal:
        raise ValueError("Not goal: ",text)
    
    minutes = re.findall(minute_pattern, text)
    for idx in range(len(minutes)):
        minutes[idx] = help_transform(minutes[idx])
    player = re.match(player_pattern, text)
    return player, minutes


if __name__ == "__main__":
    input = "Bukayo Saka 43', 74' Goal"
    input = "James Ward-Prowse 90 +3' (pen) label.penalty.scored"
    input = "Erling Haaland 34', 37', 64' Goal"

    player_pattern = r"^[A-Za-z\s-]+"
    # minute_pattern = r"(?:\w)\d{1,2}"
    # minute_pattern = r"\d+(?=')|\d+(?=\+)"
    minute_pattern = r"[\d\s\+]+'"
    extra_minute_pattern = r"\+\d{1,2}"

    label_pattern = r"Goal|\(pen\)"

    is_goal = re.search(label_pattern, input)
    if is_goal:
        minutes = re.findall(minute_pattern, input)
        player = re.match(player_pattern, input)
