from page_object import Component
import datetime as dt
from zoneinfo import ZoneInfo

class Matchbar(Component):
    """Represents `matchBar` container."""

    def get_referee(self) -> str:
        """Return main referee's fullname."""
        return self.component.find_class("referee")[0].text_content().strip()

    def get_kickoff(self) -> dt:
        timestamp_as_str = self.component.find_class(
            "matchDate"
        )[0].attrib["data-kickoff"]
        return dt.datetime.fromtimestamp(
            int(timestamp_as_str)/1000,
            tz=ZoneInfo("Asia/Ho_Chi_Minh"),
        )

    def get_attendance(self) -> str:
        return self.component.find_class("attendance")[0].text.split(" ")[1]
