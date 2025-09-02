# models/xgboost_model.py

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
  python models/xgboost_model.py --mode predict

  # Custom paths
  python models/xgboost_model.py --mode train --input data/features/my_features.csv
  python models/xgboost_model.py --mode predict --input data/features/my_latest_features.csv
"""

import os
import json
import argparse
import warnings
from typing import List, Tuple
import numpy as np
import pandas as pd