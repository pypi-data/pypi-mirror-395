from sportsdatabase import SportsDatabaseClient


def main() -> None:
    client = SportsDatabaseClient(api_key="")

    leagues = client.leagues.list(sport_slug="soccer")
    print("[smoke] leagues:", len(leagues["data"]))

    if leagues["data"]:
        league_id = leagues["data"][0]["id"]
        teams = client.teams.list(league_id=league_id, limit=5)
        print(f"[smoke] teams for {league_id}:", len(teams["data"]))

        schedule = client.schedules.league_next(league_id=league_id, limit=3)
        for entry in schedule["data"]:
            print("[smoke] upcoming event", entry.get("eventId"), entry.get("status"))


if __name__ == "__main__":
    main()
