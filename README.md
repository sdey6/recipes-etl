# Hello Fresh Recipe Case Study

This task is about extracting "HOT" recipes from a Recipe dataset as it filters out recipes with "Chilies" as an ingredient, and then adds a field named difficulty based on the sum of preparation time and cooking time of the meal. The output is a CSV file.

## Instructions

1. **Downloading the Dataset:**
   - Download the Open Recipes data from [https://bnlf-tests.s3.eu-central-1.amazonaws.com/recipes.json]


2 **Running the Script:**
   - The python version used for the script is 3.9.4.
   - To run the Python script:
     ```bash
     cd directory_name
     venv\Scripts\activate (windows)
     source venv/bin/activate (Linux)
     pip install -r requirements.txt
     python case_study.py
     ```


3. **The Output:**
   - The resulting CSV file, named `chilies_recipe.csv`, will be saved in the same directory.

## Script Details

  - The script performs an ETL operation on the Open Recipes data.
  - It Filters out recipes containing "Chilies" and also considers the misspellings and singular form of the word.
  - Adds a difficulty column based on the sum of prepTime and cookTime of a recipe.


