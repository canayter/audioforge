import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

class AudioClassifier:
    """Classify audio based on extracted features."""
    
    def __init__(self):
        self.model = None
        
    def prepare_features(self, features_list, labels=None):
        """Convert features to a format suitable for machine learning."""
        # For simplicity, let's use mean of each feature
        X = []
        
        for features in features_list:
            feature_vector = []
            
            # Extract mean of each feature
            for feature_name, feature_value in features.items():
                if isinstance(feature_value, np.ndarray):
                    if feature_value.ndim > 1:
                        feature_vector.extend(np.mean(feature_value, axis=1))
                    else:
                        feature_vector.append(np.mean(feature_value))
            
            X.append(feature_vector)
            
        if labels is not None:
            return np.array(X), np.array(labels)
        else:
            return np.array(X)
    
    def train(self, features_list, labels, test_size=0.2, random_state=42):
        """Train a classifier on the given features."""
        X, y = self.prepare_features(features_list, labels)
        
        # Split into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        
        # Initialize and train the model
        self.model = RandomForestClassifier(n_estimators=100, random_state=random_state)
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)
        
        return accuracy, report
    
    def predict(self, features):
        """Predict the class of new audio based on its features."""
        if self.model is None:
            raise ValueError("Model not trained yet!")
            
        X = self.prepare_features([features])
        prediction = self.model.predict(X)[0]
        
        return prediction