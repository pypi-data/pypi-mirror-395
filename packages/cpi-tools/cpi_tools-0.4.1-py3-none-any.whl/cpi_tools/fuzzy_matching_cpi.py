# Import packages
from io import StringIO
import pandas as pd
import numpy as np
import string
from unidecode import unidecode
import warnings
import time
import s3fs
import boto3
import jaro  # pip install jaro-winkler

# ------------------------------------
# -- Define cleaning function
# ------------------------------------


def clean_entity_name(original_entity: str, stop_words: list):

    clean_entity_name = str(original_entity)
    clean_entity_name = clean_entity_name.lower()
    clean_entity_name = clean_entity_name.split(" (")[0]
    translator = str.maketrans("", "", string.punctuation)
    clean_entity_name = clean_entity_name.translate(translator)
    clean_entity_name = unidecode(clean_entity_name)

    if stop_words == stop_words:
        # Remove stop words
        clean_entity_name = " ".join(
            word for word in clean_entity_name.split() if word.lower() not in stop_words
        )

    return clean_entity_name


# ------------------------------------
# -- Define threshold function
# ------------------------------------


def dynamic_threshold(matching_scores: list, lower_threshold: float) -> float:

    # Sort the pairs based on the scores in descending order
    sorted_scores = sorted(matching_scores, reverse=True)
    # Remove scores below the lower threshold set in the main function
    sorted_scores = [x for x in sorted_scores if x >= lower_threshold]
    # Compute the ratio between any two consecutive pairs of scores
    score_ratios = [
        sorted_scores[i] / sorted_scores[i + 1] for i in range(len(sorted_scores) - 1)
    ]

    return sorted_scores[(score_ratios.index(max(score_ratios)))]


# ------------------------------------
# -- Define manual input of
# -- threshold function
# ------------------------------------


def threshold_check(
    matched_scores: list, matched_entities: list, current_threshold: float
) -> float:

    # Zip the two lists together
    combined_list = list(zip(matched_scores, matched_entities))
    # Sort the pairs based on the scores in descending order
    sorted_pairs = sorted(combined_list, reverse=True)
    # Separate the sorted pairs back into two lists
    sorted_scores, sorted_matches = zip(*sorted_pairs)

    # Keep only those entities above the threshold
    new_threshold = current_threshold
    while new_threshold != "":
        new_threshold = float(new_threshold)
        scores_to_keep = [x for x in sorted_scores if x >= new_threshold]
        matches_to_keep = sorted_matches[: len(scores_to_keep) + 1]
        first_three_discared_matches = sorted_matches[
            len(scores_to_keep) + 1 : len(scores_to_keep) + 4
        ]
        # matched_entities = [entity for entity, score in zip(matched_entities, matched_scores) if score > fixed_value]
        new_threshold = input(
            f"With a threshold of {calculated_threshold}, \
			the last three retained matches are {matches_to_keep[-3:]}, \
			while the first three discared ones are {first_three_discared_matches}. \
			Please input the new desired threshold (leave blank if current one is acceptable)"
        )

    return new_threshold


# ------------------------------------
# -- Define fuzzy matching function
# ------------------------------------


def run_fuzzy_match(
    entity_to_match: str,
    search_list: list,
    stop_words: list,
    clean_names: bool,
    multiple_matches: bool,
    set_threshold_dynamically: bool,
    lower_threshold: bool
    ) -> list:

    if clean_names == True:  # perform round of cleaning of names
        entity_to_match_clean = clean_entity_name(entity_to_match, stop_words)
        search_list_clean = [clean_entity_name(x, stop_words) for x in search_list]
    else:
        entity_to_match_clean = entity_to_match
        search_list_clean = search_list

    # Initialize empty lists
    matched_entities = []
    matched_scores = []

    # Compute a Jaro-Winkler score for each combination of entities
    for i, s in enumerate(search_list_clean):
        score = jaro.jaro_winkler_metric(entity_to_match_clean, s)
        matched_entities.append(search_list[i])
        matched_scores.append(score)

    # Extract matches of interest on the basis of the various parameters
    if multiple_matches == False:
        # Retain highest score only
        max_score = max(matched_scores)
        if max_score >= lower_threshold:
            matched_entities = matched_entities[
                matched_scores.index(max(matched_scores))
            ]
            matched_scores = max_score
        else:
            matched_scores = []
            matched_entities = []

    elif (multiple_matches == True) & (set_threshold_dynamically == False):
        matched_entities = [
            entity
            for entity, score in zip(matched_entities, matched_scores)
            if score >= lower_threshold
        ]
        matched_scores = [x for x in matched_scores if x >= lower_threshold]

    elif (multiple_matches == True) & (set_threshold_dynamically == True):
        # Calculate the dynamic threshold
        calculated_threshold = float(dynamic_threshold(matched_scores, lower_threshold))
        # Zip the two lists together
        combined_list = list(zip(matched_scores, matched_entities))
        # Sort the pairs based on the scores in descending order
        sorted_pairs = sorted(combined_list, reverse=True)
        # Separate the sorted pairs back into two lists
        sorted_scores, sorted_matches = zip(*sorted_pairs)
        # Retain all scores above or equal to the calculated threshold
        matched_scores = [x for x in sorted_scores if x >= calculated_threshold]
        matched_entities = sorted_matches[: len(matched_scores)]

    return matched_scores, matched_entities


# ------------------------------------
# -- Define master function
# ------------------------------------


def fm_dataset(
    dataframe_to_match: pd.DataFrame,
    original_column: str,
    search_list: list,
    stop_words: list,
    clean_names: bool = True,
    multiple_matches: bool = False,
    set_threshold_dynamically: bool = False,
    lower_threshold: float = 0.8,
) -> pd.DataFrame:

    """
    fm_dateset performs a fuzzy match for all lines appear in the original dataframe passed as input. For each pair of strings, the Jaro-Winkler metric is calculated and, depending on the arguments specified, the combination will be either treated as a match and the matched string retained and stored in a new column, or discared.

    *Arguments*
    dataframe_to_match: a pd.DataFrame object that contains the column that needs to be matched to one or more elements of another list.
    
    original_column: a string, specifying the name of the column in "dataframe_to_match" that needs to be used as base for the fuzzy match. For each item in this column, the algorithm will try and find a match in the list passed in the following argument.
    
    search_list: a list of strings, containing all the potential matches to the "original_column" items. The algorithm will iterate over each of the elements in this list and calculate the distance score between it and the item to be matched. 
    
    stop_words: a list of strings, containing stop words to be removed from both the base strings to be matched and the strings of potential matches.
    
    clean_names: a boolean indicating whether to perform the names' cleaning (removal of stop words, lower case, removal of punctuation). Defaulted to True. 
    
    multiple_matches: a boolean indicating whether multiple matches are to be allowed by the algorithm. If False (as per default), each base string to matched will be matched with at most one string from the "search_list" list (the match with the higher score will be retained); otheriwse, an indefinite amount of matches will be returned. 
    
    set_threshold_dynamically: a boolean, defaulted to False, specifying whether the lower threshoold (after which pair of matches will be discared) should  be set dynamically (contact the author of this function for more details) or whether it should be fixed to a constant (see next argument).
    
    lower_threshold: a float between 0 and 1 that indicates the lower bound for matches to be considered as such. The higher the threshold, the lower the  probability of finding a match, but also the lower the probability of a  false positive. Defaulted to 0.8.


    *Output*
    dataframe_to_match: pd.DataFrame object similar to the inputted one, with the addition of two extra columns: "Matched score" and "Matched string", each in a list format.

    *Example* 

    *Author*
    Nikita Marini - nikita.marini@cpiglobal.org

    Last updated on November 15th, 2023.
    """

    # Apply function
    results = dataframe_to_match[original_column].apply(
        run_fuzzy_match,
        args=(
            search_list,
            stop_words,
            clean_names,
            multiple_matches,
            set_threshold_dynamically,
            lower_threshold,
        ),
    )

    # Create two new columns to store the results
    dataframe_to_match["Matched score"] = results.apply(lambda x: x[0])
    dataframe_to_match["Matched string"] = results.apply(lambda x: x[1])

    return dataframe_to_match


# Test
# importpath = '/Users/nikitamarini/Desktop/CPI'
# df = pd.read_csv(f'{importpath}/gfanz_entities.csv')
# search_list_test = ['Ageas', 'ABN AMRO', 'Intesa San Paolo']

# df = run_fuzzy_match(df, 'Entity', search_list_test)
# print(df[df['Matched entity'].apply(len) > 0])
