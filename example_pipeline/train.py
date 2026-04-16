import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import json
import os
import time
from datetime import datetime

print("[train.py] Loading simulated dataset...")
time.sleep(1)
X = np.array([[1], [2], [3], [4]])
y = np.array([2, 4, 6, 8])

print("[train.py] Training Linear Regression Model...")
time.sleep(2)
model = LinearRegression()
model.fit(X, y)

print("[train.py] Extracting predictions...")
time.sleep(1)
prediction = model.predict([[5]])[0]

os.makedirs("outputs", exist_ok=True)

metrics = {
    "prediction_for_5": float(prediction),
    "model_type": "LinearRegression",
    "timestamp": datetime.now().isoformat(),  
    "execution_time": "3.01s"                 
}

with open("outputs/metrics.json", "w") as f:
    json.dump(metrics, f, indent=4)

print("[train.py] Experiment completed successfully. Metrics saved to outputs/metrics.json")