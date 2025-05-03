# Import the necessary components from CleanFusion
from cleanfusion.core.data_preprocessor import DataPreprocessor
import pandas as pd

# Create a DataPreprocessor instance with desired cleaning options
preprocessor = DataPreprocessor(
    numerical_strategy='median',  # Options: 'mean', 'median', 'knn'
    categorical_strategy='most_frequent',
    outlier_threshold=3.0,
    text_vectorizer='tfidf',
    # round_decimals=2  # Optional: round numerical values to 2 decimal places
)

# Option 1: Clean a CSV file directly
input_file = "sample_data.csv"
output_file = "cleaned_data.csv"
cleaned_df = preprocessor.clean_file(input_file, output_file)
print(f"File cleaned and saved to {output_file}")

# Option 2: More control over the process
# Read the CSV file
df = pd.read_csv("sample_data.csv")

# Examine the data before cleaning
print("Original data shape:", df.shape)
print("Missing values before cleaning:", df.isnull().sum().sum())

# Apply the cleaning transformations
cleaned_df = preprocessor.transform(df)

# Examine the cleaned data
print("Cleaned data shape:", cleaned_df.shape)
print("Missing values after cleaning:", cleaned_df.isnull().sum().sum())

# Save the cleaned data
cleaned_df.to_csv("cleaned_data.csv", index=False)
