"""
Mock Data Service — Phase 1 ও Phase 2 এ real API ছাড়াই কাজ করার জন্য।

USE_MOCK_DATA=true থাকলে এই data ব্যবহার হবে।
Phase 3 এ USE_MOCK_DATA=false করলে soccerdata এ switch হয়ে যাবে।
"""

from typing import Optional


# ══════════════════════════════════════════════════════════════════════
# PLAYER DATA
# ══════════════════════════════════════════════════════════════════════

MOCK_PLAYERS: dict = {
    "messi": {
        "id": "mock_messi",
        "name": "Lionel Messi",
        "team": "Inter Miami CF",
        "position": "Forward / Right Wing",
        "nationality": "Argentina",
        "age": 37,
        "stats": {
            "season": "2024-25",
            "goals": 14,
            "assists": 12,
            "matches_played": 22,
            "minutes_played": 1680,
            "xG": 11.3,
            "xA": 10.8,
            "shots_per_90": 3.2,
            "key_passes_per_90": 2.7,
            "progressive_passes": 87,
            "progressive_carries": 65,
            "dribbles_completed": 48,
            "pressures": 124,
            "tackles_won": 18,
            "rating_avg": 8.4,
            "last_10_games": [
                {"match": "Miami vs LA Galaxy", "date": "2025-05-28", "goals": 2, "assists": 1, "xG": 1.8, "rating": 9.2, "result": "W"},
                {"match": "Miami vs NYCFC",     "date": "2025-05-22", "goals": 0, "assists": 2, "xG": 0.6, "rating": 8.1, "result": "W"},
                {"match": "Miami vs Columbus",  "date": "2025-05-17", "goals": 1, "assists": 0, "xG": 0.9, "rating": 7.8, "result": "D"},
                {"match": "Miami vs Portland",  "date": "2025-05-10", "goals": 1, "assists": 1, "xG": 1.1, "rating": 8.5, "result": "W"},
                {"match": "Miami vs Seattle",   "date": "2025-05-03", "goals": 0, "assists": 1, "xG": 0.4, "rating": 7.6, "result": "L"},
                {"match": "Miami vs Dallas",    "date": "2025-04-26", "goals": 2, "assists": 0, "xG": 1.4, "rating": 8.9, "result": "W"},
                {"match": "Miami vs Atlanta",   "date": "2025-04-19", "goals": 1, "assists": 2, "xG": 0.7, "rating": 8.7, "result": "W"},
                {"match": "Miami vs Houston",   "date": "2025-04-13", "goals": 0, "assists": 0, "xG": 0.3, "rating": 6.8, "result": "L"},
                {"match": "Miami vs Orlando",   "date": "2025-04-05", "goals": 3, "assists": 1, "xG": 2.1, "rating": 9.8, "result": "W"},
                {"match": "Miami vs Toronto",   "date": "2025-03-29", "goals": 1, "assists": 1, "xG": 1.2, "rating": 8.3, "result": "W"},
            ],
        },
    },
    "ronaldo": {
        "id": "mock_ronaldo",
        "name": "Cristiano Ronaldo",
        "team": "Al-Nassr FC",
        "position": "Forward / Striker",
        "nationality": "Portugal",
        "age": 40,
        "stats": {
            "season": "2024-25",
            "goals": 19,
            "assists": 5,
            "matches_played": 24,
            "minutes_played": 1950,
            "xG": 15.2,
            "xA": 4.1,
            "shots_per_90": 4.8,
            "key_passes_per_90": 1.2,
            "progressive_passes": 42,
            "progressive_carries": 38,
            "dribbles_completed": 29,
            "pressures": 98,
            "tackles_won": 12,
            "rating_avg": 7.9,
            "last_10_games": [
                {"match": "Al-Nassr vs Al-Hilal",   "date": "2025-05-25", "goals": 1, "assists": 0, "xG": 1.1, "rating": 7.5, "result": "D"},
                {"match": "Al-Nassr vs Al-Ittihad", "date": "2025-05-18", "goals": 2, "assists": 1, "xG": 1.6, "rating": 8.4, "result": "W"},
                {"match": "Al-Nassr vs Al-Qadsiah", "date": "2025-05-11", "goals": 3, "assists": 0, "xG": 2.2, "rating": 9.1, "result": "W"},
                {"match": "Al-Nassr vs Al-Wehda",   "date": "2025-05-04", "goals": 0, "assists": 1, "xG": 0.8, "rating": 7.2, "result": "W"},
                {"match": "Al-Nassr vs Al-Shabab",  "date": "2025-04-27", "goals": 1, "assists": 0, "xG": 1.0, "rating": 7.6, "result": "W"},
                {"match": "Al-Nassr vs Al-Fayha",   "date": "2025-04-20", "goals": 2, "assists": 0, "xG": 1.3, "rating": 8.2, "result": "W"},
                {"match": "Al-Nassr vs Al-Khaleej", "date": "2025-04-13", "goals": 0, "assists": 0, "xG": 0.5, "rating": 6.5, "result": "L"},
                {"match": "Al-Nassr vs Al-Riyadh",  "date": "2025-04-06", "goals": 3, "assists": 1, "xG": 1.9, "rating": 9.3, "result": "W"},
                {"match": "Al-Nassr vs Al-Hazem",   "date": "2025-03-30", "goals": 1, "assists": 0, "xG": 0.9, "rating": 7.8, "result": "W"},
                {"match": "Al-Nassr vs Al-Taawoun", "date": "2025-03-23", "goals": 2, "assists": 1, "xG": 1.5, "rating": 8.6, "result": "W"},
            ],
        },
    },
    "mbappe": {
        "id": "mock_mbappe",
        "name": "Kylian Mbappé",
        "team": "Real Madrid",
        "position": "Forward / Left Wing",
        "nationality": "France",
        "age": 26,
        "stats": {
            "season": "2024-25",
            "goals": 22,
            "assists": 8,
            "matches_played": 30,
            "minutes_played": 2490,
            "xG": 18.4,
            "xA": 7.2,
            "shots_per_90": 3.9,
            "key_passes_per_90": 2.1,
            "progressive_passes": 98,
            "progressive_carries": 112,
            "dribbles_completed": 87,
            "pressures": 201,
            "tackles_won": 25,
            "rating_avg": 8.1,
            "last_10_games": [
                {"match": "Real Madrid vs Barcelona",  "date": "2025-05-30", "goals": 2, "assists": 1, "xG": 1.7, "rating": 9.0, "result": "W"},
                {"match": "Real Madrid vs Atletico",   "date": "2025-05-24", "goals": 1, "assists": 0, "xG": 0.9, "rating": 7.9, "result": "D"},
                {"match": "Real Madrid vs Sevilla",    "date": "2025-05-17", "goals": 0, "assists": 2, "xG": 0.6, "rating": 7.5, "result": "W"},
                {"match": "Real Madrid vs Valencia",   "date": "2025-05-10", "goals": 3, "assists": 0, "xG": 2.3, "rating": 9.4, "result": "W"},
                {"match": "Real Madrid vs Villarreal", "date": "2025-05-03", "goals": 1, "assists": 1, "xG": 1.1, "rating": 8.3, "result": "W"},
                {"match": "Real Madrid vs Osasuna",    "date": "2025-04-26", "goals": 0, "assists": 0, "xG": 0.4, "rating": 6.7, "result": "L"},
                {"match": "Real Madrid vs Betis",      "date": "2025-04-19", "goals": 2, "assists": 1, "xG": 1.5, "rating": 8.8, "result": "W"},
                {"match": "Real Madrid vs Getafe",     "date": "2025-04-12", "goals": 1, "assists": 0, "xG": 0.8, "rating": 7.7, "result": "W"},
                {"match": "Real Madrid vs Rayo",       "date": "2025-04-05", "goals": 2, "assists": 2, "xG": 1.6, "rating": 9.2, "result": "W"},
                {"match": "Real Madrid vs Celta",      "date": "2025-03-29", "goals": 1, "assists": 0, "xG": 1.0, "rating": 7.9, "result": "W"},
            ],
        },
    },
}


# ══════════════════════════════════════════════════════════════════════
# TEAM DATA
# ══════════════════════════════════════════════════════════════════════

MOCK_TEAMS: dict = {
    "argentina": {
        "id": "mock_arg",
        "name": "Argentina",
        "type": "national",
        "fifa_ranking": 1,
        "manager": "Lionel Scaloni",
        "formation": "4-3-3",
        "stats": {
            "matches_played": 15,
            "wins": 11, "draws": 3, "losses": 1,
            "goals_scored": 34, "goals_conceded": 12,
            "xG_for": 29.4, "xG_against": 14.1,
            "possession_avg": 58.2,
            "pass_accuracy": 87.3,
            "shots_per_game": 14.2,
        },
    },
    "brazil": {
        "id": "mock_bra",
        "name": "Brazil",
        "type": "national",
        "fifa_ranking": 5,
        "manager": "Carlo Ancelotti",
        "formation": "4-2-3-1",
        "stats": {
            "matches_played": 14,
            "wins": 9, "draws": 2, "losses": 3,
            "goals_scored": 28, "goals_conceded": 14,
            "xG_for": 24.8, "xG_against": 16.2,
            "possession_avg": 61.5,
            "pass_accuracy": 89.1,
            "shots_per_game": 13.8,
        },
    },
    "real_madrid": {
        "id": "mock_rm",
        "name": "Real Madrid",
        "type": "club",
        "league": "La Liga",
        "manager": "Carlo Ancelotti",
        "formation": "4-3-3",
        "stats": {
            "matches_played": 36,
            "wins": 24, "draws": 6, "losses": 6,
            "goals_scored": 78, "goals_conceded": 41,
            "xG_for": 72.3, "xG_against": 45.8,
            "possession_avg": 56.4,
            "pass_accuracy": 88.6,
            "shots_per_game": 16.1,
        },
    },
}


# ══════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════════════════

def search_mock_players(query: str) -> list:
    """Player নাম দিয়ে mock data search করে।"""
    query_lower = query.lower()
    results = []
    for key, player in MOCK_PLAYERS.items():
        if query_lower in player["name"].lower() or query_lower in key:
            results.append({
                "id": player["id"],
                "name": player["name"],
                "team": player["team"],
                "position": player["position"],
                "nationality": player["nationality"],
            })
    return results


def get_mock_player(identifier: str) -> Optional[dict]:
    """ID বা নামের slug দিয়ে player data আনো।"""
    # Direct key match
    if identifier in MOCK_PLAYERS:
        return MOCK_PLAYERS[identifier]
    # ID match
    for player in MOCK_PLAYERS.values():
        if player["id"] == identifier:
            return player
    return None


def get_mock_team(identifier: str) -> Optional[dict]:
    """ID বা slug দিয়ে team data আনো।"""
    if identifier in MOCK_TEAMS:
        return MOCK_TEAMS[identifier]
    for team in MOCK_TEAMS.values():
        if team["id"] == identifier:
            return team
    return None
