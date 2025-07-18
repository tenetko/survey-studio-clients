import sys
from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

import requests
from bs4 import BeautifulSoup


class DailyCountersPageScraper:
    MONTH_TO_STRING = {
        1: "января",
        2: "февраля",
        3: "марта",
        4: "апреля",
        5: "мая",
        6: "июня",
        7: "июля",
        8: "августа",
        9: "сентября",
        10: "октября",
        11: "ноября",
        12: "декабря",
    }

    def __init__(self, url: str) -> None:
        self.url = url

    def get_value_by_counter_name(self, counter_name_to_find: str) -> int | None:
        res = requests.get(self.url)
        if res.status_code != HTTPStatus.OK:
            raise requests.HTTPError

        rows = BeautifulSoup(res.text, "lxml").find_all("tr")
        for row in rows:
            cells = row.find_all("td")
            if len(cells) != 4:
                continue

            counter_name = cells[0].get_text(strip=True)
            if counter_name != counter_name_to_find:
                continue

            return int(cells[2].get_text(strip=True))

        return None


if __name__ == "__main__":
    parser = DailyCountersPageScraper(sys.argv[1])
    counter_name = parser.get_daily_counter_name(datetime(2025, 6, 30))
    print(counter_name)
    value = parser.get_value_by_counter_name(counter_name)
    print(value)
