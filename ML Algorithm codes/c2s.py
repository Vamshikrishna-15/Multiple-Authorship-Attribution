import ast
import os
import torch
import torch.nn as nn
import torch.optim as optim
import csv
import pandas as pd
import re

class Code2Seq(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, feature_size):
        super(Code2Seq, self).__init__()
        self.embedding = nn.Embedding(input_size, hidden_size)
        self.gru = nn.GRU(hidden_size, hidden_size)
        self.fc = nn.Linear(hidden_size, output_size)
        self.lexical_fc = nn.Linear(hidden_size, feature_size)
        self.syntactic_fc = nn.Linear(hidden_size, feature_size)
        self.semantic_fc = nn.Linear(hidden_size, feature_size)
        self.layout_fc = nn.Linear(hidden_size, feature_size)
        self.relu = nn.ReLU()  # ReLU activation function
        self.tanh = nn.Tanh()  # Tanh activation function for output layer

    def forward(self, input_seq):
        embedded = self.embedding(input_seq)
        _, hidden = self.gru(embedded)
        hidden = hidden.squeeze(0)
        output = self.tanh(self.fc(hidden))  # Apply Tanh activation to output
        lexical_features = self.relu(self.lexical_fc(hidden))
        syntactic_features = self.relu(self.syntactic_fc(hidden))
        semantic_features = self.relu(self.semantic_fc(hidden))
        layout_features = self.relu(self.layout_fc(hidden))
        return output, lexical_features, syntactic_features, semantic_features, layout_features


# Step 1: Generate AST path from Python code snippet
def generate_ast_path(code):
    parsed_ast = ast.parse(code)
    ast_path = []

    def traverse(node):
        ast_path.append(node.__class__.__name__)
        for child in ast.iter_child_nodes(node):
            traverse(child)

    traverse(parsed_ast)
    return ast_path


# Step 2: Preprocess the AST path and convert it to code2seq format
def preprocess_ast_path(ast_path):
    # Step 4: Preprocess the sequence if needed
    # Example preprocessing: Convert sequence to lowercase
    preprocessed_sequence = [node_type.lower() for node_type in ast_path]

    # Example code2seq-specific preprocessing: Add special tokens
    special_token_start = "<START>"
    special_token_end = "<END>"
    preprocessed_sequence = [special_token_start] + preprocessed_sequence + [special_token_end]

    return preprocessed_sequence


# Function to calculate additional features
def calculate_additional_features(code):
    # Step 7: Calculate additional features from the code

    # Example additional features: Calculate word frequencies
    word_frequencies = {}
    for word in code.split():
        word = word.lower()
        word_frequencies[word] = word_frequencies.get(word, 0) + 1

    # Example additional features: Calculate character n-grams
    character_ngrams = {}
    n = 3
    for i in range(len(code) - n + 1):
        ngram = code[i:i + n]
        character_ngrams[ngram] = character_ngrams.get(ngram, 0) + 1

    # Return all additional features as a dictionary
    return word_frequencies, character_ngrams


# Example usage
input_size = 100  # Size of the vocabulary
hidden_size = 128  # Size of the hidden layer in the GRU
output_size = 20  # Number of output classes
feature_size = 64  # Size of the features

# Create an instance of the code2seq model
model = Code2Seq(input_size, hidden_size, output_size, feature_size)

# Example directory path containing multiple folders with Python code files
directory_path = "C:\\Users\\vamshi krishna\\Desktop\\INTERNSHIP\\github"

# Get the current working directory
output_directory = os.getcwd()

# Output CSV file path
output_csv_path = os.path.join(output_directory, "6features.csv")

# Step 3: Process each folder in the directory
with open(output_csv_path, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Folder", "Filename", "Lexical Features", "Syntactic Features", "Semantic Features", "Layout Features", "Word Frequencies", "Character N-grams"])

    for folder_name in os.listdir(directory_path):
        folder_path = os.path.join(directory_path, folder_name)
        if os.path.isdir(folder_path):
            print(f"Processing folder: {folder_name}")

            # Step 4: Process each file in the folder
            for filename in os.listdir(folder_path):
                if filename.endswith(".py"):
                    file_path = os.path.join(folder_path, filename)

                    # Read the Python code from the file
                    with open(file_path, "r", encoding="latin-1") as file:
                        code = file.read()

                    # Step 1: Generate AST path
                    ast_path = generate_ast_path(code)

                    # Step 2: Preprocess the AST path and convert it to code2seq format
                    preprocessed_sequence = preprocess_ast_path(ast_path)

                    # Create a mapping of unique tokens to indices
                    token_to_index = {token: i for i, token in enumerate(set(preprocessed_sequence))}
                    token_to_index["<UNK>"] = len(token_to_index)  # Add "<UNK>" token for out-of-vocabulary tokens

                    # Step 6: Convert the preprocessed sequence to tensor
                    input_seq = torch.tensor([token_to_index.get(token, token_to_index["<UNK>"]) for token in preprocessed_sequence])

                    # Step 7: Calculate additional features
                    word_frequencies, character_ngrams = calculate_additional_features(code)

                    # Apply the code2seq model to the input sequence
                    with torch.no_grad():
                        output, lexical_features, syntactic_features, semantic_features, layout_features = model(input_seq.unsqueeze(0))  # Add an extra dimension for batch size

                    # Prepare the features for writing to the CSV file
                    features = [
                        folder_name,
                        filename,
                        ", ".join(str(val) for val in lexical_features[0]),
                        ", ".join(str(val) for val in syntactic_features[0]),
                        ", ".join(str(val) for val in semantic_features[0]),
                        ", ".join(str(val) for val in layout_features[0]),
                        str(word_frequencies),
                        str(character_ngrams)
                    ]

                    # Write the features to the CSV file
                    writer.writerow(features)

# Assuming you have a CSV file containing the data
data = pd.read_csv(output_csv_path, encoding="latin-1")

# Preprocessing the data
def preprocess_features(features_str):
    # Convert the features string to a list of floats using regular expression
    return [float(val) for val in re.findall(r'-?\d+\.\d+', features_str)]

data['Lexical Features'] = data['Lexical Features'].apply(preprocess_features)
data['Syntactic Features'] = data['Syntactic Features'].apply(preprocess_features)
data['Semantic Features'] = data['Semantic Features'].apply(preprocess_features)
data['Layout Features'] = data['Layout Features'].apply(preprocess_features)
data['Word Frequencies'] = data['Word Frequencies'].apply(eval)  # Convert string representation of dictionary to dictionary
data['Character N-grams'] = data['Character N-grams'].apply(eval)  # Convert string representation of dictionary to dictionary

# Save the preprocessed data to the same CSV file
data.to_csv(output_csv_path, index=False)