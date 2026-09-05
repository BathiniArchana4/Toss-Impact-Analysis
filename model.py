import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


# ==========================================
# PREPARE DATA
# ==========================================

def prepare_model_data(df):

    data = df.copy()

    # 1 = toss winner also won the match
    # 0 = toss winner lost the match

    data["toss_winner_match_winner"] = (
        data["toss_winner"] == data["winner"]
    ).astype(int)

    # Select features that exist in the dataset
    features = []

    if "toss_decision" in data.columns:
        features.append("toss_decision")

    if "venue" in data.columns:
        features.append("venue")

    if "season" in data.columns:
        features.append("season")

    if len(features) == 0:
        raise ValueError(
            "No suitable columns found for the model."
        )

    X = data[features]
    y = data["toss_winner_match_winner"]

    return X, y


# ==========================================
# TRAIN MACHINE LEARNING MODEL
# ==========================================

def train_model(df):

    X, y = prepare_model_data(df)

    # Identify text columns
    categorical_features = [
        column
        for column in X.columns
        if X[column].dtype == "object"
    ]

    # Identify numerical columns
    numerical_features = [
        column
        for column in X.columns
        if X[column].dtype != "object"
    ]

    # Convert text data into numbers
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(
                    handle_unknown="ignore"
                ),
                categorical_features
            ),
            (
                "numerical",
                "passthrough",
                numerical_features
            )
        ]
    )

    # Random Forest model
    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42
    )

    # Complete pipeline
    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model)
        ]
    )

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    # Train
    pipeline.fit(X_train, y_train)

    # Predict
    predictions = pipeline.predict(X_test)

    # Calculate accuracy
    accuracy = accuracy_score(
        y_test,
        predictions
    )

    return (
        pipeline,
        accuracy,
        y_test,
        predictions
    )


# ==========================================
# TEST MODEL
# ==========================================

if __name__ == "__main__":

    print("Toss Impact Machine Learning Model")
    print("-----------------------------------")

    try:

        # Load dataset
        df = pd.read_csv(
            "data/matches.csv"
        )

        # Clean column names
        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )

        # Remove missing values
        df = df.dropna(
            subset=[
                "toss_winner",
                "winner"
            ]
        )

        # Train model
        model, accuracy, y_test, predictions = train_model(df)

        print("\nModel trained successfully!")

        print(
            "\nModel Accuracy:",
            round(accuracy * 100, 2),
            "%"
        )

        print(
            "\nTesting completed successfully!"

        )

    except FileNotFoundError:

        print(
            "\nERROR: matches.csv not found."
        )

        print(
            "Make sure the file is here:"
        )

        print(
            "data/matches.csv"
        )

    except Exception as e:

        print(
            "\nERROR:",
            e
        )
