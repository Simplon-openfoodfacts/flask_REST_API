import pandas as pd
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from lightgbm import LGBMClassifier
import unittest
from memory_profiler import memory_usage
import time

#Test for the first model

def train_lgbm_model(X_train, y_train, num_leaves=31, max_depth=-1, learning_rate=0.1, n_estimators=100, boosting_type='gbdt'):
    model = LGBMClassifier(
        num_leaves=num_leaves,
        max_depth=max_depth,
        learning_rate=learning_rate,
        n_estimators=n_estimators,
        boosting_type=boosting_type,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    return model

class TestLightGBMModel(unittest.TestCase):

    results = []

    def setUp(self):
        self.X, self.y = make_classification(n_samples=100, n_features=20, n_classes=2, random_state=42)
        self.X_train, self.X_val, self.y_train, self.y_val = train_test_split(self.X, self.y, test_size=0.2, random_state=42)

    def test_model_training(self):
        model = train_lgbm_model(self.X_train, self.y_train)
        self.assertIsNotNone(model)
        self.results.append(('Model Training', True, None))

    def test_model_predict(self):
        model = train_lgbm_model(self.X_train, self.y_train)
        y_pred = model.predict(self.X_val)
        self.assertEqual(y_pred.shape, self.y_val.shape)
        self.results.append(('Model Predict', True, None))

    def test_feature_importance(self):
        model = train_lgbm_model(self.X_train, self.y_train)
        importances = model.feature_importances_
        self.assertEqual(len(importances), self.X.shape[1])
        self.results.append(('Feature Importance', True, None))

    def test_memory_usage(self):
        mem_usage = memory_usage((train_lgbm_model, (self.X_train, self.y_train)), interval=0.1)
        max_memory = max(mem_usage) - min(mem_usage)
        if max_memory >= 100:
            self.results.append(('Memory Usage', False, f"Exceeded: {max_memory} MB"))
            self.fail(f"Memory usage exceeded: {max_memory} MB")
        else:
            self.results.append(('Memory Usage', True, f"{max_memory:.2f} MB"))

    def test_time_usage(self):
        start_time = time.time()
        train_lgbm_model(self.X_train, self.y_train)
        elapsed_time = time.time() - start_time
        
        if elapsed_time >= 5:
            self.results.append(('Time Usage', False, f"Too long: {elapsed_time:.2f} seconds"))
            self.fail(f"Model training took too long: {elapsed_time:.2f} seconds")
        else:
            self.results.append(('Time Usage', True, f"{elapsed_time:.2f} seconds"))

    @classmethod
    def tearDownClass(cls):
        # Create a DataFrame from the results and display it
        df_results = pd.DataFrame(cls.results, columns=['Test', 'Passed', 'Details'])
        print("\nTest Results:")
        print(df_results)

if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
