import pandas as pd


# ==========================================
# LOAD DATA
# ==========================================

def load_data(file_path):
    """
    Load the IPL matches CSV file.
    """

    df = pd.read_csv(file_path)

    # Clean column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    return df


# ==========================================
# CLEAN DATA
# ==========================================

def clean_data(df):
    """
    Clean the dataset before analysis.
    """

    df = df.copy()

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Remove rows without toss winner
    if "toss_winner" in df.columns:
        df = df.dropna(subset=["toss_winner"])

    # Remove rows without match winner
    if "winner" in df.columns:
        df = df.dropna(subset=["winner"])

    return df


# ==========================================
# TOSS IMPACT ANALYSIS
# ==========================================

def toss_match_statistics(df):
    """
    Calculate how often the toss winner
    also won the match.
    """

    total_matches = len(df)

    if total_matches == 0:
        return {
            "total_matches": 0,
            "toss_winner_won": 0,
            "toss_winner_lost": 0,
            "win_percentage": 0
        }

    # Compare toss winner with match winner
    toss_winner_won = (
        df["toss_winner"] == df["winner"]
    ).sum()

    toss_winner_lost = (
        total_matches - toss_winner_won
    )

    win_percentage = (
        toss_winner_won / total_matches
    ) * 100

    return {
        "total_matches": total_matches,
        "toss_winner_won": int(toss_winner_won),
        "toss_winner_lost": int(toss_winner_lost),
        "win_percentage": round(win_percentage, 2)
    }


# ==========================================
# TOSS DECISION ANALYSIS
# ==========================================

def toss_decision_analysis(df):
    """
    Compare batting first and fielding first.
    """

    if "toss_decision" not in df.columns:
        return pd.DataFrame()

    data = df.copy()

    # Create a new column
    data["toss_winner_won_match"] = (
        data["toss_winner"] == data["winner"]
    )

    result = (
        data.groupby("toss_decision")
        .agg(
            matches=("winner", "count"),
            toss_winner_wins=(
                "toss_winner_won_match",
                "sum"
            )
        )
        .reset_index()
    )

    result["win_percentage"] = (
        result["toss_winner_wins"]
        / result["matches"]
    ) * 100

    result["win_percentage"] = result[
        "win_percentage"
    ].round(2)

    return result


# ==========================================
# TEAM-WISE ANALYSIS
# ==========================================

def team_toss_analysis(df):
    """
    Calculate toss impact for every team.
    """

    teams = set()

    if "team1" in df.columns:
        teams.update(
            df["team1"].dropna().unique()
        )

    if "team2" in df.columns:
        teams.update(
            df["team2"].dropna().unique()
        )

    records = []

    for team in sorted(teams):

        # Number of tosses won
        toss_wins = (
            df["toss_winner"] == team
        ).sum()

        # Number of times team won match
        # after winning toss
        matches_won_after_toss = (
            (df["toss_winner"] == team)
            &
            (df["winner"] == team)
        ).sum()

        # Matches played
        matches_played = (
            (df["team1"] == team)
            |
            (df["team2"] == team)
        ).sum()

        # Total match wins
        match_wins = (
            df["winner"] == team
        ).sum()

        # Toss-to-match win percentage
        if toss_wins > 0:
            toss_to_match_win_percentage = (
                matches_won_after_toss
                / toss_wins
            ) * 100
        else:
            toss_to_match_win_percentage = 0

        # Overall win percentage
        if matches_played > 0:
            overall_win_percentage = (
                match_wins
                / matches_played
            ) * 100
        else:
            overall_win_percentage = 0

        records.append({
            "team": team,
            "toss_wins": int(toss_wins),
            "matches_won_after_toss": int(
                matches_won_after_toss
            ),
            "toss_to_match_win_percentage":
                round(
                    toss_to_match_win_percentage,
                    2
                ),
            "matches_played": int(
                matches_played
            ),
            "match_wins": int(
                match_wins
            ),
            "overall_win_percentage":
                round(
                    overall_win_percentage,
                    2
                )
        })

    return pd.DataFrame(records)


# ==========================================
# SEASON ANALYSIS
# ==========================================

def season_analysis(df):
    """
    Analyze toss impact for each IPL season.
    """

    if "season" not in df.columns:
        return pd.DataFrame()

    data = df.copy()

    data["toss_winner_won_match"] = (
        data["toss_winner"] == data["winner"]
    )

    result = (
        data.groupby("season")
        .agg(
            matches=("winner", "count"),
            toss_winner_wins=(
                "toss_winner_won_match",
                "sum"
            )
        )
        .reset_index()
    )

    result["toss_impact_percentage"] = (
        result["toss_winner_wins"]
        / result["matches"]
    ) * 100

    result["toss_impact_percentage"] = result[
        "toss_impact_percentage"
    ].round(2)

    return result


# ==========================================
# VENUE ANALYSIS
# ==========================================

def venue_analysis(df):
    """
    Analyze toss impact at different venues.
    """

    if "venue" not in df.columns:
        return pd.DataFrame()

    data = df.copy()

    data["toss_winner_won_match"] = (
        data["toss_winner"] == data["winner"]
    )

    result = (
        data.groupby("venue")
        .agg(
            matches=("winner", "count"),
            toss_winner_wins=(
                "toss_winner_won_match",
                "sum"
            )
        )
        .reset_index()
    )

    result["toss_win_percentage"] = (
        result["toss_winner_wins"]
        / result["matches"]
    ) * 100

    result["toss_win_percentage"] = result[
        "toss_win_percentage"
    ].round(2)

    return result.sort_values(
        "toss_win_percentage",
        ascending=False
    )


# ==========================================
# TEST FUNCTION
# ==========================================

if __name__ == "__main__":

    print("Toss Impact Analysis")
    print("--------------------")

    file_path = "data/matches.csv"

    try:

        df = load_data(file_path)

        print("\nDataset loaded successfully!")

        print("\nColumns:")
        print(df.columns.tolist())

        df = clean_data(df)

        print(
            f"\nTotal records: {len(df)}"
        )

        # Overall statistics
        if (
            "toss_winner" in df.columns
            and
            "winner" in df.columns
        ):

            stats = toss_match_statistics(df)

            print("\nTOSS IMPACT")
            print("--------------------")
            print(
                "Total Matches:",
                stats["total_matches"]
            )
            print(
                "Toss Winner Won:",
                stats["toss_winner_won"]
            )
            print(
                "Toss Winner Lost:",
                stats["toss_winner_lost"]
            )
            print(
                "Toss → Match Win %:",
                stats["win_percentage"],
                "%"
            )

        print("\nAnalysis completed!")

    except FileNotFoundError:

        print(
            "\nERROR: matches.csv was not found."
        )

        print(
            "Make sure your file is located at:"
        )

        print(
            "Toss_Impact_Analysis/data/matches.csv"
        )
