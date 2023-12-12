import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from keras.models import Sequential
from keras.layers import LSTM, Dense
from keras.optimizers import Adam
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
import tensorflow as tf
# Load the CSV data
data = pd.read_csv("C:\\Users\\vamshi krishna\\Desktop\\INTERNSHIP\\codes\\allfeatures.csv")

# Separate features and labels
X = data.drop(columns=["Folder"])
y = data["Folder"]

# Preprocess numeric features
numeric_features = X.select_dtypes(include=[np.number])

# Impute missing values with median
imputer = SimpleImputer(strategy='median')
numeric_features_imputed = imputer.fit_transform(numeric_features)

# Convert imputed features to DataFrame
numeric_features_imputed_df = pd.DataFrame(numeric_features_imputed, columns=numeric_features.columns)

# Standardize numeric features
scaler = StandardScaler()
numeric_features_scaled = scaler.fit_transform(numeric_features_imputed_df)

# Preprocess non-numeric features
non_numeric_features = X.select_dtypes(include=[np.object])
non_numeric_features.fillna("missing", inplace=True)  # Fill NaN values with "missing" or other appropriate value
non_numeric_features_encoded = pd.get_dummies(non_numeric_features, columns=non_numeric_features.columns)

# Combine preprocessed features
X_final = pd.concat([pd.DataFrame(numeric_features_scaled, columns=numeric_features.columns), non_numeric_features_encoded], axis=1)


# Encode labels
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Convert features and labels to tensors
X_train_tensor = tf.convert_to_tensor(X_final.values, dtype=tf.float32)
y_train_tensor = tf.convert_to_tensor(y_encoded, dtype=tf.int32)

# Split the data into training and testing sets
X_train, X_test, y_train_encoded, y_test_encoded = train_test_split(X_final, y_encoded, test_size=0.2, random_state=69)

# Reshape data for LSTM input (samples, time steps, features)
X_train_lstm = X_train.values.reshape(X_train.shape[0], 1, X_train.shape[1])

# Define hyperparameters
lstm_units = 128
dense_units = len(np.unique(y_encoded))
epochs = 10
batch_size = 32
learning_rate = 0.01

# Define LSTM model
model = Sequential()
model.add(LSTM(units=lstm_units, input_shape=(X_train_lstm.shape[1], X_train_lstm.shape[2])))
model.add(Dense(units=dense_units, activation='softmax'))

optimizer = Adam(learning_rate=learning_rate)
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train_lstm, y_train_encoded, epochs=epochs, batch_size=batch_size, validation_split=0.1)

# Evaluate the model
X_test_lstm = X_test.values.reshape(X_test.shape[0], 1, X_test.shape[1])
score = model.evaluate(X_test_lstm, y_test_encoded, batch_size=batch_size)
print("Test loss:", score[0])
print("Test accuracy:", score[1])

# # Define the parameter grid for grid search
# param_grid = {
#     'lstm_units': [64, 128, 256],
#     'dense_units': [len(np.unique(y_encoded))],
#     'epochs': [10, 20],
#     'batch_size': [32, 64],
#     'learning_rate': [0.001, 0.01, 0.1]
# }

# # Define LSTM model
# def create_model(lstm_units, dense_units, learning_rate):
#     model = Sequential()
#     model.add(LSTM(units=lstm_units, input_shape=(X_train_lstm.shape[1], X_train_lstm.shape[2])))
#     model.add(Dense(units=dense_units, activation='softmax'))
    
#     optimizer = Adam(learning_rate=learning_rate)
#     model.compile(optimizer=optimizer, loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    
#     return model

# # Create the KerasClassifier wrapper for scikit-learn
# from keras.wrappers.scikit_learn import KerasClassifier
# model = KerasClassifier(build_fn=create_model)

# # Perform grid search
# grid = GridSearchCV(estimator=model, param_grid=param_grid, scoring='accuracy', cv=3)
# grid_result = grid.fit(X_train_lstm, y_train_encoded)

# # Print the results
# print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
# Evaluate the model on the test data
y_pred = model.predict(X_test_lstm)
y_pred_classes = np.argmax(y_pred, axis=1)
print("Classification Report:")
print(classification_report(y_test_encoded, y_pred_classes))