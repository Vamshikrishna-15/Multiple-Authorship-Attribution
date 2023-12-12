import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import accuracy_score, classification_report
from sklearn.impute import SimpleImputer

# Preprocess the numeric features
def preprocess_numeric_features(data):
    numeric_columns = ['Code Complexity', 'Cyclomatic Complexity','Lines of Code','Comment Density','Has Loops','Has Conditionals','Has Functions','Has Classes']

    for col in numeric_columns:
        data[col] = pd.to_numeric(data[col], errors='coerce')  # Convert the features to numeric

    # Impute missing values with the mean of the respective columns
    imputer = SimpleImputer(strategy='mean')
    data[numeric_columns] = imputer.fit_transform(data[numeric_columns])

    return data[numeric_columns]

# Preprocess the non-numeric features
def preprocess_non_numeric_features(data):
    non_numeric_columns = ['Lexical Features', 'Syntactic Features', 'Semantic Features',
                           'Layout Features', 'Word Frequencies', 'Character N-grams']

    for col in non_numeric_columns:
        data[col] = data[col].apply(lambda x: pd.Series(eval(x)).mean())  # Convert list-like objects to their mean
        
    return data[non_numeric_columns]

# Main preprocessing function
def preprocess_features(data):
    numeric_features = preprocess_numeric_features(data)
    non_numeric_features = preprocess_non_numeric_features(data)
    features = pd.concat([numeric_features, non_numeric_features], axis=1)

    return features

# Load the data from the CSV file
data = pd.read_csv("C:\\Users\\vamshi krishna\\Desktop\\INTERNSHIP\\codes\\allfeatures.csv", encoding='latin1')

# Preprocess the features and target
X = preprocess_features(data)
y = data['Folder']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=50)

# Standardize the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the MDA model
mda_model = LinearDiscriminantAnalysis()
mda_model.fit(X_train_scaled, y_train)

# Make predictions on the test set
y_pred = mda_model.predict(X_test_scaled)

# Calculate accuracy and display classification report
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
print("Classification Report:\n", classification_report(y_test, y_pred))
