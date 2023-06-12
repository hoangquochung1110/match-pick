import re
from collections import namedtuple

GoalEvent = namedtuple("GoalEvent", "player minute label")


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
        "Gabriel Jesus 35' (pen), 55' label.penalty.scored"

    """
    def strip_whitespace_and_single_quote(text: str):
        mapping = {
            "'": "",
        }
        trans_table = str.maketrans(mapping)
        return text.translate(trans_table).strip()

    goal_events = []

    cleaned_text = text.replace("label.penalty.scored", "Goal")
    player_pattern = r"^[A-Za-z\s-]+"
    # minute_pattern = r"\b[\d\s\+]+'"
    minute_pattern = r"[\d\s+]*'\s*(?:\(pen\))?|\d+'"

    label_pattern = r"Goal"
    is_goal = re.search(label_pattern, cleaned_text)
    if not is_goal:
        raise ValueError("Not goal: ",cleaned_text)

    player = re.match(player_pattern, cleaned_text)

    minutes = re.findall(minute_pattern, cleaned_text)

    for idx in range(len(minutes)):
        minutes[idx] = strip_whitespace_and_single_quote(minutes[idx])
        try:
            minute, label = minutes[idx].split(" ")
        except ValueError:
            minute, label = minutes[idx], ""
        finally:
            goal_events.append(GoalEvent(player[0], minute, label))
    return goal_events


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


def parse_assist_event_string(text: str) -> tuple[str, str]:
    """Parse assist string.
    
    For example: Bukayo Saka 28 -> return ('Bukayo Saka', 28)

    Armel Bella-Kotchap 66' -> return (Armel Bella-Kotchap, 66)
    """
    match = re.match(r"([-A-Za-zÀ-ÿ\s]+)(\d+)", text)
    return match.group(1).strip(), match.group(2)
