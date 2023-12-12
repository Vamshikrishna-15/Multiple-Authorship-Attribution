import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV

# Load the data from CSV
data = pd.read_csv("C:\\Users\\vamshi krishna\\Desktop\\INTERNSHIP\\codes\\allfeatures.csv", encoding='latin1')

# Process numeric features
numeric_features = ['Code Complexity', 'Cyclomatic Complexity', 'Lines of Code', 'Comment Density',
                    'Has Loops', 'Has Conditionals', 'Has Functions', 'Has Classes']
X_numeric = data[numeric_features].values

# Process non-numeric features
non_numeric_features = ['Lexical Features', 'Syntactic Features', 'Semantic Features', 'Layout Features']
X_non_numeric = pd.get_dummies(data[non_numeric_features])

# Process 'Word Frequencies' and 'Character N-grams'
X_word_freq = pd.DataFrame(data['Word Frequencies'].apply(eval).apply(lambda x: sum(x.values())).tolist())
X_char_ngrams = pd.DataFrame(data['Character N-grams'].apply(eval).apply(lambda x: sum(x.values())).tolist())

# Combine the features
X = pd.concat([pd.DataFrame(X_numeric), X_non_numeric, X_word_freq, X_char_ngrams], axis=1)


# Convert all column names to strings
X.columns = X.columns.astype(str)

# Impute NaN values with mean
from sklearn.impute import SimpleImputer
imputer = SimpleImputer(strategy='mean')
X = pd.DataFrame(imputer.fit_transform(X), columns=X.columns)

# Normalize the features
scaler = StandardScaler()
normalized_features = scaler.fit_transform(X)

# Convert the features to numpy array
X = np.array(normalized_features)

# Convert the labels to numpy array
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(data['Folder'])

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define the parameter grid for SVM
param_grid = {
    'C': [0.1, 1, 10],
    'kernel': ['linear', 'rbf'],
}

# Create the SVM model
model = SVC()

# Perform grid search for hyperparameters
grid_search = GridSearchCV(model, param_grid, cv=5)
grid_search.fit(X_train, y_train)

# Get the best hyperparameters and model
best_params = grid_search.best_params_
best_model = grid_search.best_estimator_

# Evaluate the best model
y_pred = best_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("Best Parameters:", best_params)
print("Test Accuracy:", accuracy)