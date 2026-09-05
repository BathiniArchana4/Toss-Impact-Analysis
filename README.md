# 🏏 IPL Toss Impact Analysis

An interactive data analytics and machine learning dashboard that
investigates whether winning the toss gives a team an advantage in
Indian Premier League (IPL) matches.

The project uses **Python, Pandas, Plotly, Scikit-learn, and Streamlit**
to clean IPL match data, calculate toss-related statistics, visualize
patterns, and build a machine-learning model.

------------------------------------------------------------------------

## 📌 Project Overview

In cricket, winning the toss allows a team to choose whether to bat or
field first. This project explores an important question:

> **Does winning the toss actually increase the probability of winning
> the match?**

The dashboard analyzes IPL match data from multiple perspectives,
including overall toss impact, toss decision, team performance, seasons,
venues, and machine-learning predictions.

------------------------------------------------------------------------

## 🎯 Objectives

-   Analyze the relationship between toss results and match results.
-   Calculate the percentage of toss winners who also won the match.
-   Compare **bat first** and **field first** decisions.
-   Analyze team-wise toss performance.
-   Study toss impact across IPL seasons.
-   Identify venues where toss winners have performed better.
-   Build a machine-learning model to predict whether the toss winner
    will win the match.
-   Present the results through an interactive Streamlit dashboard.

------------------------------------------------------------------------

## 🛠️ Technologies Used

  Technology     Purpose
  -------------- ----------------------------
  Python         Core programming
  Pandas         Data cleaning and analysis
  NumPy          Numerical processing
  Plotly         Interactive visualizations
  Scikit-learn   Machine learning
  Streamlit      Interactive web dashboard

------------------------------------------------------------------------

## 📊 Dashboard Features

### 1. 📊 Overall Toss Impact

Shows: - Total matches - Toss winners who won the match - Toss winners
who lost the match - Toss-to-match win percentage - Pie chart and bar
chart

### 2. 🪙 Toss Decision Analysis

Compares: - Bat first - Field first - Number of matches - Toss winner
success percentage

### 3. 👥 Team-wise Analysis

Provides: - Toss wins by team - Matches won after winning the toss -
Toss-to-match win percentage - Overall match win percentage

### 4. 📅 Season Analysis

Shows how toss impact changes across IPL seasons.

### 5. 🏟️ Venue Analysis

Analyzes toss success at different venues and allows filtering based on
the minimum number of matches played at a venue.

### 6. 🤖 Machine Learning

A Random Forest classification model is used to predict whether the toss
winner will also win the match.

Model features can include: - Toss decision - Venue - Season

The dashboard displays the model accuracy and actual-vs-predicted
results.

------------------------------------------------------------------------

## 📁 Project Structure

``` text
TOSS IMPACT/
│
├── data/
│   └── matches.csv
│
├── screenshots/
│   ├── overview.png
│   ├── toss_decision.png
│   ├── team_analysis.png
│   ├── season_analysis.png
│   ├── venue_analysis.png
│   └── machine_learning.png
│
├── app.py
├── analysis.py
├── model.py
└── requirements.txt
```

------------------------------------------------------------------------

## 📦 Dataset

The project uses an IPL match-level CSV dataset containing information
such as:

-   Season
-   Teams
-   Venue
-   Toss winner
-   Toss decision
-   Match winner

The dataset is stored in:

``` text
data/matches.csv
```

------------------------------------------------------------------------

## ⚙️ Installation

### 1. Clone the repository

``` bash
git clone https://github.com/BathiniArchana4/Toss-Impact-Analysis.git
```

### 2. Open the project folder

``` bash
cd Toss-Impact-Analysis
```

### 3. Install dependencies

``` bash
python -m pip install -r requirements.txt
```

If you do not have `requirements.txt`, the main packages are:

``` bash
python -m pip install pandas numpy plotly scikit-learn streamlit
```

------------------------------------------------------------------------

## ▶️ Run the Dashboard

Start the Streamlit application with:

``` bash
python -m streamlit run app.py
```

The dashboard will open in your browser.

------------------------------------------------------------------------

## 🔬 Analysis Workflow

``` text
IPL Match Dataset
        ↓
Data Cleaning
        ↓
Exploratory Analysis
        ↓
Toss Impact Calculations
        ↓
Interactive Visualizations
        ↓
Machine Learning Model
        ↓
Streamlit Dashboard
```

------------------------------------------------------------------------

## 🤖 Machine Learning Approach

The project creates a binary target:

``` text
1 → Toss winner also won the match
0 → Toss winner lost the match
```

A **Random Forest Classifier** is trained using available features such
as:

-   Toss decision
-   Venue
-   Season

The dataset is divided into training and testing sets, and model
accuracy is calculated using the test data.

> **Note:** Model accuracy should be interpreted carefully. A prediction
> model built from historical match data does not guarantee future match
> outcomes.

------------------------------------------------------------------------

## 💡 Key Insights

This project helps answer questions such as:

-   How often does the toss winner win the match?
-   Is batting first or fielding first associated with better
    toss-winner success?
-   Which teams have converted toss wins into match wins most
    effectively?
-   Does toss impact change from season to season?
-   Which venues show higher toss-winner success?
-   How accurately can historical features predict the toss winner's
    match result?

------------------------------------------------------------------------

## 📸 Dashboard Screenshots

Screenshots of the Streamlit dashboard are available in the
`screenshots/` folder.

Example:

``` text
screenshots/
├── overview.png
├── toss_decision.png
├── team_analysis.png
├── season_analysis.png
├── venue_analysis.png
└── machine_learning.png
```

------------------------------------------------------------------------

## 🚀 Future Improvements

-   Add player-level analysis.
-   Add team comparison filters.
-   Include additional match statistics.
-   Add more machine-learning algorithms.
-   Compare model performance using multiple evaluation metrics.
-   Add real-time or regularly updated datasets.
-   Deploy the Streamlit dashboard online.

------------------------------------------------------------------------

## 👩‍💻 Author

**Archana Bathini**

GitHub: [BathiniArchana4](https://github.com/BathiniArchana4)

------------------------------------------------------------------------

## ⭐ If You Like This Project

If you find this project useful or interesting, consider giving the
repository a ⭐ on GitHub.

------------------------------------------------------------------------

## 📄 License

This project is intended for educational and portfolio purposes.
