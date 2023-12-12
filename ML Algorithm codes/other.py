import csv
import os
import ast
import radon.complexity as radon_complexity
import radon.metrics as radon_metrics

# Function to extract code metrics features
def extract_code_metrics_features(file_path):
    with open(file_path, 'r', encoding="latin-1") as file:
        code_content = file.read()

    # Calculate code complexity
    complexity_results = radon_complexity.cc_visit(code_content)
    if complexity_results:
        code_complexity = complexity_results[0].complexity
    else:
        code_complexity = 0

    # Calculate cyclomatic complexity
    cyclomatic_results = radon_complexity.cc_visit(code_content)
    if cyclomatic_results:
        cyclomatic_complexity = cyclomatic_results[0].complexity
    else:
        cyclomatic_complexity = 0

    # Calculate number of functions and lines of code
    metrics_results = radon_metrics.mi_visit(code_content, multi=False)
    if isinstance(metrics_results, list) and metrics_results:
        number_of_functions = metrics_results[0].methods
    else:
        number_of_functions = 0

    lines_of_code = len(code_content.split('\n'))

    return [code_complexity, cyclomatic_complexity, number_of_functions, lines_of_code]

# Function to extract language features
def extract_language_features(file_path):
    with open(file_path, 'r', encoding="latin-1") as file:
        code_content = file.read()

    # Parse the code to an Abstract Syntax Tree (AST)
    tree = ast.parse(code_content)

    # Initialize language feature values
    has_loops = 0
    has_conditionals = 0
    has_functions = 0
    has_classes = 0

    # Traverse the AST to identify language features
    for node in ast.walk(tree):
        if isinstance(node, ast.For) or isinstance(node, ast.While):
            has_loops = 1
        elif isinstance(node, ast.If) or isinstance(node, ast.While):
            has_conditionals = 1
        elif isinstance(node, ast.FunctionDef):
            has_functions = 1
        elif isinstance(node, ast.ClassDef):
            has_classes = 1

    return [has_loops, has_conditionals, has_functions, has_classes]

# Function to process files in the directory and store combined features in a CSV file
def process_directory_and_store_combined_features(directory_path):
    output_csv_combined_features_path = os.path.join(directory_path, "other_features.csv")

    with open(output_csv_combined_features_path, "w", newline="") as csvfile_combined:
        writer_combined = csv.writer(csvfile_combined)
        writer_combined.writerow(["Folder", "Filename", "Code Complexity", "Cyclomatic Complexity", "Number of Functions", "Lines of Code",
                                  "Has Loops", "Has Conditionals", "Has Functions", "Has Classes"])

        for folder_name in os.listdir(directory_path):
            folder_path = os.path.join(directory_path, folder_name)
            if os.path.isdir(folder_path):
                print(f"Processing folder: {folder_name}")

                # Step 2: Process each file in the folder
                for filename in os.listdir(folder_path):
                    if filename.endswith(".py"):
                        file_path = os.path.join(folder_path, filename)

                        # Extract language features
                        language_features = extract_language_features(file_path)

                        # Extract code metrics features
                        code_metrics_features = extract_code_metrics_features(file_path)

                        # Prepare the features for writing to the CSV file
                        features_combined = [
                            folder_name,
                            filename,
                            code_metrics_features[0],
                            code_metrics_features[1],
                            code_metrics_features[2],
                            code_metrics_features[3],
                            language_features[0],
                            language_features[1],
                            language_features[2],
                            language_features[3]
                        ]

                        # Write the features to the CSV file
                        writer_combined.writerow(features_combined)

# Call the function with the directory path to process the files and store combined features in a CSV file
directory_path = "C:\\Users\\vamshi krishna\\Desktop\\INTERNSHIP\\github"
process_directory_and_store_combined_features(directory_path)