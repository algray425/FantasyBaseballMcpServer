from mcp.server.fastmcp import FastMCP

import httpx

from typing import Any
from enum import Enum

mcp = FastMCP("Fantasy Baseball")

HITTER_PROJECTIONS_ENDPOINT = "http://localhost:9292/api/v2/players/hitting/projections"
HITTER_RANKING_ENDPOINT     = "http://localhost:9292/api/v2/players/hitting/stats"

class HittingStat(Enum):
    PERCENTILE_OVERALL  = 1
    RUNS                = 2
    HOME_RUNS           = 3
    RBIS                = 4
    STOLEN_BASES        = 5
    OBP                 = 6
    NONE                = 7

async def makeHitterRequest(url: str) -> dict[str, Any] | None:
    """ Make a request to the fantasy baseball API with proper error handling"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=30.0)

            response.raise_for_status()

            return response.json()
        except Exception:
            return None

def formatHitterProjections(hitterProjection: dict) -> str:
    return f"""
    Name: {hitterProjection.get("firstName", "Unknown")} {hitterProjection.get("lastName", "Unknown")}
    Team: {hitterProjection.get("team", "Unknown")}
    Position: {hitterProjection.get("position", "Unknown")}
    Runs: {hitterProjection.get("runs", "Unknown")}
    Home Runs: {hitterProjection.get("homeRuns", "Unknown")}
    Rbis: {hitterProjection.get("rbis", "Unknown")}
    Stolen Bases: {hitterProjection.get("stolenBases", "Unknown")}
    Overall Percentile Runs: {hitterProjection.get("overallPercentileRuns", "Unknown")}
    Overall Percentile Home Runs: {hitterProjection.get("overallPercentileHomeRuns", "Unknown")}
    Overall Percentile Rbis: {hitterProjection.get("overallPercentileRbis", "Unknown")}
    Overall Percentile Stolen Bases: {hitterProjection.get("overallPercentileStolenBases", "Unknown")}
    Overall Percentile OBP: {hitterProjection.get("overallPercentileOnBasePercentage", "Unknown")}
    Overall Grade Percentile: {hitterProjection.get("overallPercentileGrade", "Unknown")}
    Qualified Percentile Runs: {hitterProjection.get("qualifiedPercentileRuns", "Unknown")}
    Qualified Percentile Home Runs: {hitterProjection.get("qualifiedPercentileHomeRuns", "Unknown")}
    Qualified Percentile Rbis: {hitterProjection.get("qualifiedPercentileRbis", "Unknown")}
    Qualified Percentile Stolen Bases: {hitterProjection.get("qualifiedPercentileStolenBases", "Unknown")}
    Qualified Percentile OBP: {hitterProjection.get("qualifiedPercentileOnBasePercentage", "Unknown")}
    Qualified Grade Percentile: {hitterProjection.get("qualifiedPercentileGrade", "Unknown")}
    """

def formatHitterRanking(hitterProjection: dict) -> str:
    return f"""
    Name: {hitterProjection.get("firstName", "Unknown")} {hitterProjection.get("lastName", "Unknown")}
    Team: {hitterProjection.get("team", "Unknown")}
    Position: {hitterProjection.get("position", "Unknown")}
    Runs: {hitterProjection.get("runs", "Unknown")}
    Home Runs: {hitterProjection.get("homeRuns", "Unknown")}
    Rbis: {hitterProjection.get("rbis", "Unknown")}
    Stolen Bases: {hitterProjection.get("stolenBases", "Unknown")}
    OBP: {hitterProjection.get("onBasePercentage", "Unknown")}
    """

@mcp.tool()
async def getHitterProjections(position: str = "", qualified: bool = False, sortBy: HittingStat = HittingStat.NONE) -> str:
    """Get hitter projections for the upcoming season

    Args:
        position: The position to filter by (e.g. 1B, OF)
        qualified: Flag to determine if we should filter by qualified hitters or not
        sortBy: The hitting stat to sort results by (e.g. runs, home runs)
    """

    url = f"{HITTER_PROJECTIONS_ENDPOINT}?qualified={qualified}"

    if len(position) != 0:
        url = url + f"&position={position}"

    if sortBy != HittingStat.NONE:
        url = url + f"&sortBy={sortBy.name}"

    data = await makeHitterRequest(url)

    projections = [formatHitterProjections(hitter) for hitter in data]

    return "\n---\n".join(projections)

@mcp.tool()
async def getHitterRankings(season: str, position: str = "", startDate: str = "", endDate: str = "", leagueTypeFilter: str = "", leagueIdFilter: str = "") -> str:
    """Get hitter rankings for a season.

    Args:
        season: The season to get rankings for (e.g. 2025, 2024)
        position: The position to filter by (e.g. 1B, OF)
        startDate: The start date to filter hitter ranks by with format YYYY-MM-DD
        endDate: The end date to filter hitter ranks by with format YYYY-MM-DD
        leagueTypeFilter: The type of league to filter by (e.g. ESPN)
        leagueIdFilter: The id of the league to filter by
    """

    url = f"{HITTER_RANKING_ENDPOINT}/{season}"

    if len(position) != 0 or len(startDate) != 0 or len(endDate) != 0:
        url = url + f"?"

    if len(position) != 0:
        url = url + f"position={position}&"

    if len(startDate) != 0:
        url = url + f"startDate={startDate}&"

    if len(endDate) != 0:
        url = url + f"endDate={endDate}&"

    if len(leagueTypeFilter) != 0:
        url = url + f"leagueTypeFilter={leagueTypeFilter}&"

    if len(leagueIdFilter) != 0:
        url = url + f"leagueIdFilter={leagueIdFilter}&"

    data = await makeHitterRequest(url)

    if not data or len(data) == 0:
        return "Unable to fetch hitter rankings for given season"

    rankings = [formatHitterRanking(hitter) for hitter in data]

    return "\n---\n".join(rankings)

def main():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
