import pytest

from match_picker.extract import parse_goal_event_string


def test_parse_goal_event_string():
    output = parse_goal_event_string(text="Bukayo Saka 43', 74' Goal")

    # unnecessary strip()
    assert output[0].player.strip() == "Bukayo Saka"
    assert output[0].minute == "43"

    assert output[1].player.strip() == "Bukayo Saka"
    assert output[1].minute == "74"
