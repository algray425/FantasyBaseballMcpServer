from mcp.server.fastmcp import FastMCP

import httpx

from typing import Any
from enum import Enum

mcp = FastMCP("Fantasy Baseball")

HITTER_PROJECTIONS_ENDPOINT             = "http://localhost:9292/api/v2/players/hitting/projections"
STARTING_PITCHER_PROJECTIONS_ENDPOINT   = "http://localhost:9292/api/v2/players/startingPitchers/projections"
HITTER_RANKING_ENDPOINT                 = "http://localhost:9292/api/v2/players/hitting/stats"
STARTING_PITCHER_RANKING_ENDPOINT       = "http://localhost:9292/api/v2/players/startingPitching/stats"
RELIEF_PITCHER_RANKING_ENDPOINT         = "http://localhost:9292/api/v2/players/reliefPitchers/stats"

FANTASY_TEAM_SUMMARY_ENDPOINT = "http://localhost:9292/api/v2/users/fantasyTeamSummary"

class HittingStat(Enum):
    PERCENTILE_OVERALL  = 1
    RUNS                = 2
    HOME_RUNS           = 3
    RBIS                = 4
    STOLEN_BASES        = 5
    OBP                 = 6
    NONE                = 7

class PitchingStat(Enum):
    PERCENTILE_OVERALL  = 1
    QUALITY_STARTS      = 2
    ERA                 = 3
    WHIP                = 4
    KS_PER_NINE         = 5
    SAVES               = 6
    HOLDS               = 7

async def makeFantasyBaseballRequest(url: str) -> dict[str, Any] | None:
    """ Make a request to the fantasy baseball API with proper error handling"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=30.0)

            response.raise_for_status()

            return response.json()
        except Exception:
            return None

def formatStartingPitcherProjections(pitcherProjection: dict) -> str:
    return f"""
    Name: {pitcherProjection.get("firstName", "Unknown")} {pitcherProjection.get("lastName", "Unknown")}
    Team: {pitcherProjection.get("team", "Unknown")}
    Quality Starts: {pitcherProjection.get("qualityStarts", "Unknown")}
    ERA: {pitcherProjection.get("era", "Unknown")}
    WHIP: {pitcherProjection.get("whip", "Unknown")}
    Ks/9: {pitcherProjection.get("ksPerNine", "Unknown")}
    Percentile Quality Starts: {pitcherProjection.get("percentileQualityStarts", "Unknown")}
    Percentile ERA: {pitcherProjection.get("percentileEra", "Unknown")}
    Percentile WHIP: {pitcherProjection.get("percentileWhip", "Unknown")}
    Percentile Ks/9: {pitcherProjection.get("percentileKsPerNine", "Unknown")}
    Percentile Grade: {pitcherProjection.get("percentileGrade", "Unknown")}
    """

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

def formatHitterRanking(hitterRanking: dict) -> str:
    return f"""
    Name: {hitterRanking.get("firstName", "Unknown")} {hitterRanking.get("lastName", "Unknown")}
    Team: {hitterRanking.get("team", "Unknown")}
    Position: {hitterRanking.get("position", "Unknown")}
    Overall Percentile: {hitterRanking.get("grade", "Unknown")}
    Runs: {hitterRanking.get("runs", "Unknown")}
    Home Runs: {hitterRanking.get("homeRuns", "Unknown")}
    Rbis: {hitterRanking.get("rbis", "Unknown")}
    Stolen Bases: {hitterRanking.get("stolenBases", "Unknown")}
    OBP: {hitterRanking.get("onBasePercentage", "Unknown")}
    """

def formatStartingPitcherRanking(pitcherRanking: dict) -> str:
    return f"""
    Name: {pitcherRanking.get("firstName", "Unknown")} {pitcherRanking.get("lastName", "Unknown")}
    Team: {pitcherRanking.get("team", "Unknown")}
    Overall Percentile: {pitcherRanking.get("grade", "Unknown")}
    Quality Starts: {pitcherRanking.get("qualityStarts", "Unknown")}
    ERA: {pitcherRanking.get("era", "Unknown")}
    WHIP: {pitcherRanking.get("whip", "Unknown")}
    Ks/9: {pitcherRanking.get("ksPerNine", "Unknown")}
    """

def formatReliefPitcherRanking(pitcherRanking: dict) -> str:
    return f"""
    Name: {pitcherRanking.get("firstName", "Unknown")} {pitcherRanking.get("lastName", "Unknown")}
    Team: {pitcherRanking.get("team", "Unknown")}
    Overall Percentile: {pitcherRanking.get("grade", "Unknown")}
    Saves: {pitcherRanking.get("saves", "Unknown")}
    Holds: {pitcherRanking.get("holds", "Unknown")}
    ERA: {pitcherRanking.get("era", "Unknown")}
    WHIP: {pitcherRanking.get("whip", "Unknown")}
    Ks/9: {pitcherRanking.get("ksPerNine", "Unknown")}
    """

def formatFantasyHitter(fantasyHitter: dict) -> str:
    return f"""
    Name: {fantasyHitter.get("firstName", "Unknown")} {fantasyHitter.get("lastName", "Unknown")}
    Team: {fantasyHitter.get("currentTeam", "Unknown")}
    Position: {fantasyHitter.get("currentPosition", "Unknown")}
    Percentile Overall {fantasyHitter.get("percentileOverall", "Unknown")}
    Percentile Runs {fantasyHitter.get("percentileOverallRuns", "Unknown")}
    Percentile Home Runs {fantasyHitter.get("percentileOverallHomeRuns", "Unknown")}
    Percentile RBIs {fantasyHitter.get("percentileOverallRbis", "Unknown")}
    Percentile Stolen Bases {fantasyHitter.get("percentileOverallStolenBases", "Unknown")}
    Percentile OBP {fantasyHitter.get("percentileOverallOnBasePercentage", "Unknown")}
    Runs: {fantasyHitter.get("runs", "Unknown")}
    Home Runs: {fantasyHitter.get("homeRuns", "Unknown")}
    Rbis: {fantasyHitter.get("rbis", "Unknown")}
    Stolen Bases: {fantasyHitter.get("stolenBases", "Unknown")}
    OBP: {fantasyHitter.get("onBasePercentage", "Unknown")}
    """

def formatFantasyStartingPitcher(fantasyPitcher: dict) -> str:
    return f"""
    Name: {fantasyPitcher.get("firstName", "Unknown")} {fantasyPitcher.get("lastName", "Unknown")}
    Team: {fantasyPitcher.get("currentTeam", "Unknown")}
    Percentile Overall {fantasyPitcher.get("percentileOverall", "Unknown")}
    Percentile Quality Starts {fantasyPitcher.get("percentileOverallQualityStarts", "Unknown")}
    Percentile ERA {fantasyPitcher.get("percentileOverallEra", "Unknown")}
    Percentile WHIP {fantasyPitcher.get("percentileOverallWhip", "Unknown")}
    Percentile Ks/9 {fantasyPitcher.get("percentileOverallKsPerNine", "Unknown")}
    Quality Starts: {fantasyPitcher.get("qualityStarts", "Unknown")}
    ERA: {fantasyPitcher.get("era", "Unknown")}
    WHIP: {fantasyPitcher.get("whip", "Unknown")}
    Ks/9: {fantasyPitcher.get("ksPerNine", "Unknown")}
    """

def formatFantasyReliefPitcher(fantasyPitcher: dict) -> str:
    return f"""
    Name: {fantasyPitcher.get("firstName", "Unknown")} {fantasyPitcher.get("lastName", "Unknown")}
    Team: {fantasyPitcher.get("currentTeam", "Unknown")}
    Percentile Overall {fantasyPitcher.get("percentileOverall", "Unknown")}
    Percentile Saves plus Holds {fantasyPitcher.get("percentileOverallSaveAndHolds", "Unknown")}
    Percentile ERA {fantasyPitcher.get("percentileOverallEra", "Unknown")}
    Percentile WHIP {fantasyPitcher.get("percentileOverallWhip", "Unknown")}
    Percentile Ks/9 {fantasyPitcher.get("percentileOverallKsPerNine", "Unknown")}
    Saves plus Holds: {fantasyPitcher.get("saves", 0) + fantasyPitcher.get("holds", 0)}
    ERA: {fantasyPitcher.get("era", "Unknown")}
    WHIP: {fantasyPitcher.get("whip", "Unknown")}
    Ks/9: {fantasyPitcher.get("ksPerNine", "Unknown")}
    """

def formatCurrentMatchupStatus(teamSummary: dict) -> str:
    return f"""
    Wins: {teamSummary.get("wins", "Unknown")}
    Losses: {teamSummary.get("losses", "Unknown")}
    Ties: {teamSummary.get("ties", "Unknown")}
    Runs: {teamSummary.get("runs", "Unknown")}
    Home Runs: {teamSummary.get("homeRuns", "Unknown")}
    Rbis: {teamSummary.get("rbis", "Unknown")}
    Stolen Bases: {teamSummary.get("stolenBases", "Unknown")}
    OBP: {teamSummary.get("onBasePercentage", "Unknown")}
    Quality Starts: {teamSummary.get("qualityStarts", "Unknown")}
    Saves plus Holds: {teamSummary.get("savesPlusHolds", "Unknown")}
    ERA: {teamSummary.get("era", "Unknown")}
    WHIP: {teamSummary.get("whip", "Unknown")}
    Ks/9: {teamSummary.get("ksPerNine", "Unknown")}
    """

@mcp.tool()
async def getFantasyTeamSummary(userId: str, leagueTypeFilter: str, leagueIdFilter: str, teamId: str) -> str:
    """Get the summary of the users fantasy team including

    rosterGrades: summary of each hitter/starting pitcher/relief pitcher on the users roster
    currentMatchup: Summary of scoring for the current fantasy matchup of the user
    upcomingOpponent: summary of each hitter/starting pitcher/relief pitcher on the upcoming opponents roster

    Args:
        userId: The id of the user for the fantasy baseball app
        leagueTypeFilter: The type of league to filter by (e.g. ESPN)
        leagueIdFilter: The id of the league to filter by
        teamId: The id of the team owned by the user in their league
    """

    url = f"{FANTASY_TEAM_SUMMARY_ENDPOINT}/{userId}/{leagueTypeFilter}/{leagueIdFilter}/{teamId}"

    data = await makeFantasyBaseballRequest(url)

    rosterGradesJson = data.get("rosterGrades", [])

    hitterGrades          = []
    startingPitcherGrades = []
    reliefPitcherGrades   = []

    for grade in rosterGradesJson:
        gradeType = grade.get("type", "Unknown")

        if gradeType == "com.advanced_baseball_stats.v2.model.batters.Fantasy.FantasyPlayerSummaryBatting":
            hitterGrades.append(formatFantasyHitter(grade))
        elif gradeType == "com.advanced_baseball_stats.v2.model.batters.Fantasy.FantasyPlayerSummaryStartingPitching":
            startingPitcherGrades.append(formatFantasyStartingPitcher(grade))
        elif gradeType == "com.advanced_baseball_stats.v2.model.batters.Fantasy.FantasyPlayerSummaryReliefPitching":
            reliefPitcherGrades.append(formatFantasyReliefPitcher(grade))

    currentMatchup = data.get("currentMatchup", {})

    homeTeamSummary = currentMatchup.get("homeTeamSummary", {})
    awayTeamSummary = currentMatchup.get("awayTeamSummary", {})

    homeTeamId = homeTeamSummary.get("teamId", -1)
    awayTeamId = awayTeamSummary.get("teamId", -1)

    userCurrentMatchupSummary     = ""
    opponentCurrentMatchupSummary = ""

    if str(homeTeamId) == teamId:
        userCurrentMatchupSummary     = formatCurrentMatchupStatus(homeTeamSummary)
        opponentCurrentMatchupSummary = formatCurrentMatchupStatus(awayTeamSummary)
    elif str(awayTeamId) == teamId:
        userCurrentMatchupSummary     = formatCurrentMatchupStatus(awayTeamSummary)
        opponentCurrentMatchupSummary = formatCurrentMatchupStatus(homeTeamSummary)

    upcomingOpponentHitterGrades          = []
    upcomingOpponentStartingPitcherGrades = []
    upcomingOpponentReliefPitcherGrades   = []

    upcomingOpponent = data.get("upcomingOpponent", [])

    for grade in upcomingOpponent:
        gradeType = grade.get("type", "Unknown")

        if gradeType == "com.advanced_baseball_stats.v2.model.batters.Fantasy.FantasyPlayerSummaryBatting":
            upcomingOpponentHitterGrades.append(formatFantasyHitter(grade))
        elif gradeType == "com.advanced_baseball_stats.v2.model.batters.Fantasy.FantasyPlayerSummaryStartingPitching":
            upcomingOpponentStartingPitcherGrades.append(formatFantasyStartingPitcher(grade))
        elif gradeType == "com.advanced_baseball_stats.v2.model.batters.Fantasy.FantasyPlayerSummaryReliefPitching":
            upcomingOpponentReliefPitcherGrades.append(formatFantasyReliefPitcher(grade))

    summary  = "Team Summary\n" + "\n---\n".join(hitterGrades) + "\n---\n".join(startingPitcherGrades) + "\n---\n".join(reliefPitcherGrades)
    summary += "Current Matchup\nMy Team\n" + userCurrentMatchupSummary + "\n---\nOpponent Team\n" + opponentCurrentMatchupSummary
    summary += "\nUpcoming Matchup Team Summary\n" + "\n---\n".join(upcomingOpponentHitterGrades) + "\n---\n".join(upcomingOpponentStartingPitcherGrades) + "\n---\n".join(upcomingOpponentReliefPitcherGrades)

    return summary

@mcp.tool()
async def getStartingPitcherProjections(sortBy: PitchingStat = PitchingStat.PERCENTILE_OVERALL) -> str:
    """Get starting pitcher projections for the upcoming season

    Args:
        sortBy: The hitting stat to sort results by (e.g. PERCENTILE_OVERALL, KS_PER_NINE)
    """

    url = f"{STARTING_PITCHER_PROJECTIONS_ENDPOINT}"

    if sortBy != PitchingStat.PERCENTILE_OVERALL:
        url = url + f"?sortBy={sortBy.name}"

    data = await makeFantasyBaseballRequest(url)

    projections = [formatStartingPitcherProjections(pitcher) for pitcher in data]

    return "\n---\n".join(projections)

@mcp.tool()
async def getHitterProjections(position: str = "", qualified: bool = False, sortBy: HittingStat = HittingStat.NONE) -> str:
    """Get hitter projections for the upcoming season

    Args:
        position: The position to filter by (e.g. 1B, OF)
        qualified: Flag to determine if we should filter by qualified hitters or not
        sortBy: The hitting stat to sort results by (e.g. RUNS, HOME_RUNS)
    """

    url = f"{HITTER_PROJECTIONS_ENDPOINT}?qualified={qualified}"

    if len(position) != 0:
        url = url + f"&position={position}"

    if sortBy != HittingStat.NONE:
        url = url + f"&sortBy={sortBy.name}"

    data = await makeFantasyBaseballRequest(url)

    projections = [formatHitterProjections(hitter) for hitter in data]

    return "\n---\n".join(projections)

@mcp.tool()
async def getStartingPitcherRankings(season: str, startDate: str = "", endDate: str = "",  leagueTypeFilter: str = "", leagueIdFilter: str = "") -> str:
    """Get starting pitcher rankings for a season.

Args:
    season: The season to get rankings for (e.g. 2025, 2024)
    startDate: The start date to filter starting pitcher rankings by with format YYYY-MM-DD
    endDate: The end date to filter starting pitcher rankings by with format YYYY-MM-DD
    leagueTypeFilter: The type of league to filter by (e.g. ESPN)
    leagueIdFilter: The id of the league to filter by
"""
    url = f"{STARTING_PITCHER_RANKING_ENDPOINT}/{season}"

    if len(startDate) != 0 or len(endDate) != 0 or len(leagueTypeFilter) != 0 or len(leagueIdFilter) != 0:
        url = url + f"?"

    if len(startDate) != 0:
        url = url + f"startDate={startDate}&"

    if len(endDate) != 0:
        url = url + f"endDate={endDate}&"

    if len(leagueTypeFilter) != 0:
        url = url + f"leagueTypeFilter={leagueTypeFilter}&"

    if len(leagueIdFilter) != 0:
        url = url + f"leagueIdFilter={leagueIdFilter}&"

    data = await makeFantasyBaseballRequest(url)

    rankings = [formatStartingPitcherRanking(pitcher) for pitcher in data]

    return "\n---\n".join(rankings)

@mcp.tool()
async def getReliefPitcherRankings(season: str, startDate: str = "", endDate: str = "",  leagueTypeFilter: str = "", leagueIdFilter: str = "") -> str:
    """Get relief pitcher rankings for a season.

Args:
    season: The season to get rankings for (e.g. 2025, 2024)
    startDate: The start date to filter relief pitcher rankings by with format YYYY-MM-DD
    endDate: The end date to filter relief pitcher rankings by with format YYYY-MM-DD
    leagueTypeFilter: The type of league to filter by (e.g. ESPN)
    leagueIdFilter: The id of the league to filter by
"""
    url = f"{RELIEF_PITCHER_RANKING_ENDPOINT}/{season}"

    if len(startDate) != 0 or len(endDate) != 0 or len(leagueTypeFilter) != 0 or len(leagueIdFilter) != 0:
        url = url + f"?"

    if len(startDate) != 0:
        url = url + f"startDate={startDate}&"

    if len(endDate) != 0:
        url = url + f"endDate={endDate}&"

    if len(leagueTypeFilter) != 0:
        url = url + f"leagueTypeFilter={leagueTypeFilter}&"

    if len(leagueIdFilter) != 0:
        url = url + f"leagueIdFilter={leagueIdFilter}&"

    data = await makeFantasyBaseballRequest(url)

    rankings = [formatReliefPitcherRanking(pitcher) for pitcher in data]

    return "\n---\n".join(rankings)

@mcp.tool()
async def getHitterRankings(season: str, position: str = "", startDate: str = "", endDate: str = "", leagueTypeFilter: str = "", leagueIdFilter: str = "") -> str:
    """Get hitter rankings for a season.

    Args:
        season: The season to get rankings for (e.g. 2025, 2024)
        position: The position to filter by (e.g. 1B, OF)
        startDate: The start date to filter hitter rankings by with format YYYY-MM-DD
        endDate: The end date to filter hitter rankings by with format YYYY-MM-DD
        leagueTypeFilter: The type of league to filter by (e.g. ESPN)
        leagueIdFilter: The id of the league to filter by
    """

    url = f"{HITTER_RANKING_ENDPOINT}/{season}"

    if len(position) != 0 or len(startDate) != 0 or len(endDate) != 0 or len(leagueTypeFilter) != 0 or len(leagueIdFilter) != 0:
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

    data = await makeFantasyBaseballRequest(url)

    if not data or len(data) == 0:
        return "Unable to fetch hitter rankings for given season"

    rankings = [formatHitterRanking(hitter) for hitter in data]

    return "\n---\n".join(rankings)

def main():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
