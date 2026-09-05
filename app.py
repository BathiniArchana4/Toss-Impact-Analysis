import streamlit as st
import pandas as pd
import plotly.express as px

from analysis import (
    clean_data,
    toss_match_statistics,
    toss_decision_analysis,
    team_toss_analysis,
    season_analysis,
    venue_analysis
)

from model import train_model


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="IPL Toss Impact Analysis",
    page_icon="🏏",
    layout="wide"
)


# =========================================================
# TITLE
# =========================================================

st.title("🏏 IPL Toss Impact Analysis")

st.write(
    "This dashboard analyzes whether winning the toss "
    "provides an advantage in IPL matches."
)


# =========================================================
# LOAD DATA
# =========================================================

try:

    df = pd.read_csv("data/matches.csv")

except FileNotFoundError:

    st.error(
        "matches.csv not found!"
    )

    st.write(
        "Please make sure your file is located at:"
    )

    st.code(
        "Toss_Impact_Analysis/data/matches.csv"
    )

    st.stop()


# =========================================================
# CLEAN COLUMN NAMES
# =========================================================

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)


# =========================================================
# CLEAN DATA
# =========================================================

df = clean_data(df)


# =========================================================
# CHECK REQUIRED COLUMNS
# =========================================================

required_columns = [
    "toss_winner",
    "winner"
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:

    st.error(
        f"Missing columns: {missing_columns}"
    )

    st.write(
        "Your CSV must contain toss_winner and winner."
    )

    st.stop()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("⚙️ Dashboard Controls")


# =========================================================
# SEASON FILTER
# =========================================================

if "season" in df.columns:

    seasons = sorted(
        df["season"].dropna().unique()
    )

    selected_seasons = st.sidebar.multiselect(
        "Select Season",
        seasons,
        default=seasons
    )

    filtered_df = df[
        df["season"].isin(selected_seasons)
    ]

else:

    filtered_df = df.copy()


# =========================================================
# MAIN STATISTICS
# =========================================================

stats = toss_match_statistics(
    filtered_df
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "🏏 Total Matches",
        stats["total_matches"]
    )


with col2:

    st.metric(
        "🪙 Toss Winner Won",
        stats["toss_winner_won"]
    )


with col3:

    st.metric(
        "❌ Toss Winner Lost",
        stats["toss_winner_lost"]
    )


with col4:

    st.metric(
        "📈 Toss → Match Win %",
        f"{stats['win_percentage']:.2f}%"
    )


st.divider()


# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    [
        "📊 Overview",
        "🪙 Toss Decision",
        "👥 Team Analysis",
        "📅 Season Analysis",
        "🏟️ Venue Analysis",
        "🤖 Machine Learning"
    ]
)


# =========================================================
# TAB 1 - OVERVIEW
# =========================================================

with tab1:

    st.header("📊 Overall Toss Impact")

    chart_data = pd.DataFrame({
        "Result": [
            "Toss Winner Won Match",
            "Toss Winner Lost Match"
        ],
        "Matches": [
            stats["toss_winner_won"],
            stats["toss_winner_lost"]
        ]
    })


    col1, col2 = st.columns(2)


    # PIE CHART
    with col1:

        fig = px.pie(
            chart_data,
            names="Result",
            values="Matches",
            title="Toss Winner vs Match Result"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # BAR CHART
    with col2:

        fig = px.bar(
            chart_data,
            x="Result",
            y="Matches",
            title="Toss Impact"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # INTERPRETATION
    st.subheader("🔎 Interpretation")


    if stats["win_percentage"] > 50:

        st.success(
            f"Toss winners won "
            f"{stats['win_percentage']:.2f}% "
            f"of the selected matches."
        )

    elif stats["win_percentage"] < 50:

        st.warning(
            f"Toss winners won only "
            f"{stats['win_percentage']:.2f}% "
            f"of the selected matches."
        )

    else:

        st.info(
            "Toss winners and toss losers have "
            "an equal match-win percentage."
        )


# =========================================================
# TAB 2 - TOSS DECISION
# =========================================================

with tab2:

    st.header("🪙 Bat First vs Field First")


    decision_data = toss_decision_analysis(
        filtered_df
    )


    if not decision_data.empty:

        st.dataframe(
            decision_data,
            use_container_width=True
        )


        fig = px.bar(
            decision_data,
            x="toss_decision",
            y="win_percentage",
            text="win_percentage",
            title="Toss Winner Success by Decision"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    else:

        st.warning(
            "toss_decision column not found."
        )


# =========================================================
# TAB 3 - TEAM ANALYSIS
# =========================================================

with tab3:

    st.header("👥 Team-wise Toss Analysis")


    team_data = team_toss_analysis(
        filtered_df
    )


    if not team_data.empty:

        st.dataframe(
            team_data,
            use_container_width=True
        )


        sorted_team_data = team_data.sort_values(
            "toss_to_match_win_percentage",
            ascending=False
        )


        fig = px.bar(
            sorted_team_data,
            x="team",
            y="toss_to_match_win_percentage",
            title="Team Toss-to-Match Win Percentage"
        )


        fig.update_layout(
            xaxis_tickangle=-45
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =========================================================
# TAB 4 - SEASON ANALYSIS
# =========================================================

with tab4:

    st.header("📅 Season-wise Toss Impact")


    season_data = season_analysis(
        filtered_df
    )


    if not season_data.empty:

        st.dataframe(
            season_data,
            use_container_width=True
        )


        fig = px.line(
            season_data,
            x="season",
            y="toss_impact_percentage",
            markers=True,
            title="Toss Impact Across IPL Seasons"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    else:

        st.warning(
            "Season column not found."
        )


# =========================================================
# TAB 5 - VENUE ANALYSIS
# =========================================================

with tab5:

    st.header("🏟️ Venue-wise Toss Impact")


    venue_data = venue_analysis(
        filtered_df
    )


    if not venue_data.empty:

        # Minimum matches filter
        max_matches = int(
            venue_data["matches"].max()
        )


        minimum_matches = st.slider(
            "Minimum Matches at Venue",
            min_value=1,
            max_value=max_matches,
            value=min(5, max_matches)
        )


        filtered_venues = venue_data[
            venue_data["matches"] >= minimum_matches
        ]


        st.dataframe(
            filtered_venues,
            use_container_width=True
        )


        fig = px.bar(
            filtered_venues.head(20),
            x="venue",
            y="toss_win_percentage",
            title="Venue-wise Toss Success"
        )


        fig.update_layout(
            xaxis_tickangle=-45
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    else:

        st.warning(
            "Venue column not found."
        )


# =========================================================
# TAB 6 - MACHINE LEARNING
# =========================================================

with tab6:

    st.header("🤖 Machine Learning Prediction")


    st.write(
        """
        The machine-learning model attempts to predict whether
        the toss winner will also win the match.

        Features may include:

        • Toss decision
        • Venue
        • Season
        """
    )


    try:

        model, accuracy, y_test, predictions = train_model(
            filtered_df
        )


        st.metric(
            "🎯 Model Accuracy",
            f"{accuracy * 100:.2f}%"
        )


        comparison = pd.DataFrame({
            "Actual Result": y_test.values,
            "Predicted Result": predictions
        })


        st.subheader(
            "Actual vs Predicted Results"
        )


        st.dataframe(
            comparison,
            use_container_width=True
        )


        st.success(
            "Machine-learning model trained successfully!"
        )


    except Exception as error:

        st.error(
            f"Model training error: {error}"
        )


# =========================================================
# RAW DATA
# =========================================================

st.divider()


with st.expander("📄 View Dataset"):

    st.dataframe(
        filtered_df,
        use_container_width=True
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🏏 IPL Toss Impact Analysis | "
    "Python + Pandas + Plotly + Scikit-learn + Streamlit"
)
