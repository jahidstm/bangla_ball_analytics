from fastapi import APIRouter, Query, HTTPException
from typing import List

from app.core.config import get_settings
from app.services.mock_data import search_mock_players, get_mock_player, get_mock_team
from app.models.schemas import PlayerSearchResult, PlayerStatsResponse

settings = get_settings()
router = APIRouter(prefix="/search", tags=["Search"])


@router.get("/players", response_model=List[PlayerSearchResult])
async def search_players(q: str = Query(..., min_length=2, description="Player name")):
    """
    Player নাম দিয়ে search করো।
    Phase 1-2: Mock data থেকে।
    Phase 3+: Real API।
    """
    if settings.USE_MOCK_DATA:
        results = search_mock_players(q)
        return results

    # Phase 3 এ soccerdata API call আসবে এখানে
    raise HTTPException(status_code=503, detail="Real API integration Phase 3 এ আসবে।")


@router.get("/players/{player_id}", response_model=PlayerStatsResponse)
async def get_player_stats(player_id: str):
    """নির্দিষ্ট player এর full stats।"""
    if settings.USE_MOCK_DATA:
        player = get_mock_player(player_id)
        if not player:
            raise HTTPException(status_code=404, detail=f"'{player_id}' নামে কোনো player পাওয়া যায়নি।")
        return player

    raise HTTPException(status_code=503, detail="Real API integration Phase 3 এ আসবে।")


@router.get("/teams/{team_id}")
async def get_team_stats(team_id: str):
    """নির্দিষ্ট team এর stats।"""
    if settings.USE_MOCK_DATA:
        team = get_mock_team(team_id)
        if not team:
            raise HTTPException(status_code=404, detail=f"'{team_id}' নামে কোনো team পাওয়া যায়নি।")
        return team

    raise HTTPException(status_code=503, detail="Real API integration Phase 3 এ আসবে।")
