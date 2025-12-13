from datetime import date

from sportsdatabase import SportsDatabaseClient


def main() -> None:
    client = SportsDatabaseClient(api_key="")
    today = date.today().isoformat()
    events = client.events.get_by_date(date=today, sport="soccer")
    for event in events["data"]:
        print(event["homeTeamId"], "vs", event["awayTeamId"], event["status"])


if __name__ == "__main__":
    main()
