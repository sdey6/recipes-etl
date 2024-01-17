import csv
import json
import logging
import warnings
import requests
import pandas as pd
import isodate

pd.options.display.width = None
pd.options.display.max_columns = None
pd.set_option('display.max_rows', 3000)
pd.set_option('display.max_columns', 3000)

url = "https://bnlf-tests.s3.eu-central-1.amazonaws.com/recipes.json"

logging.basicConfig(level=logging.INFO)
warnings.simplefilter(action='ignore', category=FutureWarning)


def convert_to_minutes(time_str):
    """
    Converts a time string to minute
    :param time_str: cooking and prep time string
    :return: values in minutes
    """
    if time_str and time_str.startswith('PT'):
        try:
            duration = isodate.parse_duration(time_str)
            return int(duration.total_seconds() / 60)
        except isodate.isoerror.ISO8601Error as e:
            logging.error(f"Error parsing duration string {time_str}: {e}")
    return None


def get_difficulty(rows):
    """
    The function calculates the difficulty of the meal in terms of time
    :param rows: each row of a dataframe
    :return: the difficulty level as string
    """
    prep_time = rows['prepTime']
    cook_time = rows['cookTime']

    prep_time = convert_to_minutes(prep_time)
    cook_time = convert_to_minutes(cook_time)

    # handling nan values
    if prep_time is None or cook_time is None:
        return "Unknown"

    total = prep_time + cook_time

    if total > 60:
        return "Hard"
    elif 30 <= total <= 60:
        return "Medium"
    elif total < 30:
        return "Easy"
    else:
        return "Unknown"


def get_output_csv_from_json(url_link):
    """
    Function to convert the raw data from a URL to a CSV format by filtering out recipes with chilies and time difficulties

    :param url_link: Link for raw JSON data
    :return: filtered CSV file, error message if the url is wrong or in case of other exception
    """

    try:
        response = requests.get(url_link)
        response.raise_for_status()

        # Split the response into lines and process each line
        raw_data = response.text.split('\n')

        data_list = []
        for data in raw_data:
            if data.strip():  # Skip empty lines

                dataset = json.loads(data)
                data_list.append(dataset)

        # storing data into a dataframe
        df = pd.DataFrame(data_list)

        # lower casing the ingredients/recipe
        df['ingredients'] = df['ingredients'].str.lower()

        # define search string for 'chilies'
        str_pattern = r'\bchil(?:i|li|ies|es|ie|is)?\b'

        # getting recipes with chilies
        df_chilies = df[df['ingredients'].str.contains(str_pattern, case=False, regex=True)].reset_index(drop=True)

        # getting the difficulty column with values
        df_chilies['difficulty'] = df_chilies.apply(lambda x: get_difficulty(x), axis=1)

        df_chilies.to_csv('./chilies_recipe.csv', encoding='utf-8')


    except requests.exceptions.RequestException as e:
        logging.error(f"Data download failed. {e}")


get_output_csv_from_json(url)
logging.info(f'CSV for chili recipe data generated...')


