from mcp.server.fastmcp import FastMCP

import httpx

from typing import Any

mcp = FastMCP("Fantasy Baseball")

HITTER_RANKING_ENDPOINT = "http://localhost:9292/api/v2/players/hitting/stats"

async def makeHitterRankingsRequest(url: str) -> dict[str, Any] | None:
    """ Make a request to the fantasy baseball API to obtain hitter projections with proper error handling"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=30.0)

            response.raise_for_status()

            return response.json()
        except Exception:
            return None

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
async def getHitterRankings(season: str, position: str = "", startDate: str = "", endDate: str = "") -> str:
    """Get hitter rankings for a season.

    Args:
        season: The season to get rankings for (e.g. 2025, 2024)
        position: The position to filter by (e.g. 1B, OF)
        startDate: The start date to filter hitter ranks by with format YYYY-MM-DD
        endDate: The end date to filter hitter ranks by with format YYYY-MM-DD
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

    data = await makeHitterRankingsRequest(url)

    if not data or len(data) == 0:
        return "Unable to fetch hitter rankings for given season"

    rankings = [formatHitterRanking(hitter) for hitter in data]

    return "\n---\n".join(rankings)

def main():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
