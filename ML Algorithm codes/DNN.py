import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.neural_network import MLPClassifier
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
X_word_freq = pd.DataFrame(data['Word Frequencies'].apply(eval).tolist())
X_char_ngrams = pd.DataFrame(data['Character N-grams'].apply(eval).tolist())

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

# Convert the features to tensors
X = torch.tensor(normalized_features, dtype=torch.float32)

# Convert the labels to tensors
label_encoder = LabelEncoder()
y = torch.tensor(label_encoder.fit_transform(data['Folder']), dtype=torch.long)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define the DNN model
class DNNModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(DNNModel, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, num_classes)
    
    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        # out = self.fc2(out)
        # return out
        logits = self.fc2(out)
        probabilities = nn.functional.softmax(logits, dim=1)  # Apply softmax
        return probabilities

# Set the hyperparameters
input_size = X_train.shape[1]
hidden_size = 128
num_classes = len(np.unique(y_train))
num_epochs = 10
learning_rate = 0.001

# Initialize the model
model = DNNModel(input_size, hidden_size, num_classes)

# Define the loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# Training loop
for epoch in range(num_epochs):
    model.train()
    optimizer.zero_grad()
    outputs = model(X_train)
    loss = criterion(outputs, y_train)
    loss.backward()
    optimizer.step()

    # Print the loss every few epochs
    if (epoch + 1) % 5 == 0:
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

# Evaluation
model.eval()
with torch.no_grad():
    outputs = model(X_test)
    _, predicted = torch.max(outputs, 1)
    accuracy = accuracy_score(y_test, predicted)

print(f'Test Accuracy: {accuracy:.4f}')

# Define the parameter grid
param_grid = {
    'hidden_layer_sizes': [(64,), (128,), (256,)],
    'activation': ['relu', 'tanh'],
    'learning_rate': ['constant', 'adaptive']
}

# Create the DNN model
model = MLPClassifier()

# Perform grid search
grid_search = GridSearchCV(model, param_grid, cv=5)
grid_search.fit(X_train, y_train)

# Get the best hyperparameters and model
best_params = grid_search.best_params_
best_model = grid_search.best_estimator_

# Evaluate the best model
accuracy = best_model.score(X_test, y_test)
print("Best Parameters:", best_params)
print("Accuracy:", accuracy)
