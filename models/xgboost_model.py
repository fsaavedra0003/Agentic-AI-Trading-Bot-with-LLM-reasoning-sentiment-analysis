# models/xgboost_model.py

"""
XGBoost model for Buy/Sell/Hold signals

- Trains a multi-class classifier on engineered features.
- If 'label' is missing in the input CSV, derives a weak label from avg_sentiment.
- Saves model, label encoder, and feature metadata.
- Can also run prediction on a features CSV.

Usage:

  # Train (uses data/features/features_dataset.csv by default)
  python models/xgboost_model.py --mode train

    # Predict (reads data/features/features_dataset.csv by default)
