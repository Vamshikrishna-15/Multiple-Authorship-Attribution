import ast
from collections import Counter
import os
import pandas as pd
import radon.complexity as cc
from difflib import SequenceMatcher

def calculate_comment_density(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        code_content = file.read()

    # Parse the code into an Abstract Syntax Tree (AST)
    tree = ast.parse(code_content)

    # Count the number of lines in the code
    lines_of_code = len(code_content.split('\n'))

    # Count the number of comment lines in the code
    comments = sum(isinstance(node, ast.Expr) and isinstance(node.value, ast.Str)
                   for node in ast.walk(tree))

    # Calculate the comment density as the ratio of comment lines to total lines
    comment_density = comments / lines_of_code if lines_of_code > 0 else 0.0
    return comment_density

def detect_duplicate_code(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:  # Specify 'utf-8' encoding here
        code_content = file.read()

    # Parse the code into an Abstract Syntax Tree (AST)
    tree = ast.parse(code_content)

    # Extract all code snippets from the AST
    code_snippets = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            code_snippets.append(ast.unparse(node))

    # Calculate the similarity of each code snippet with others
    duplicate_code = 0.0
    for i, snippet1 in enumerate(code_snippets):
        for snippet2 in code_snippets[i+1:]:
            similarity = SequenceMatcher(None, snippet1, snippet2).ratio()
            if similarity >= 0.9:  # Adjust the similarity threshold as needed
                duplicate_code = 1.0  # Mark as duplicate if similarity is above the threshold
                break
        if duplicate_code == 1.0:
            break

    return duplicate_code


def count_library_calls(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        code_content = file.read()

    tree = ast.parse(code_content)
    library_calls = [node.func.attr for node in ast.walk(tree) if isinstance(node, ast.Call) and hasattr(node.func, 'attr')]

    return Counter(library_calls)


def process_directory_and_store_features(directory_path):
    features_data = []

    for root, _, files in os.walk(directory_path):
        folder_name = os.path.basename(root)  # Get the folder name from the current directory path

        for file_name in files:
            if file_name.endswith('.py'):
                file_path = os.path.join(root, file_name)

                comment_density = calculate_comment_density(file_path)
                duplicate_code = detect_duplicate_code(file_path)
                library_calls = count_library_calls(file_path)

                features_data.append({
                    'Folder': folder_name,  # Use the folder name as a feature
                    'Comment Density': comment_density,
                    'Duplicate Code': duplicate_code,
                    'Library Calls': library_calls
                })

    df = pd.DataFrame(features_data)
    print(df)  # Debug: Print the DataFrame to check if data is present
    df.to_csv("code_features.csv", index=False)


# Replace 'path_to_directory' with the path of the directory containing the Python files
process_directory_and_store_features("C:\\Users\\vamshi krishna\\Desktop\\INTERNSHIP\\github")