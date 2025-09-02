# models/xgboost_model.py

"""
XGBoost model for Buy/Sell/Hold signals

- Trains a multi-class classifier on engineered features.
- If 'label' is missing in the input CSV, derives a weak label from avg_sentiment.