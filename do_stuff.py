import csv
import regex
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)


# TO-DO: TENSORFLOW TOMORROW. DATA ENGINEERING SEEMS TO BE COMPLETE.
titanic_path = "train.csv"
age_list = []
status_list = []
age_dictionary = {}

# Two loops, first loop to clean the data and extract whatever is there in the
# column so that the second loop can fill in the blanks.
# Third loop is to remove the feature columns not needed for now...


def extract_data(file_path: str):

    title_pattern = ",\s(.*\.)"
    title_compile = regex.compile(title_pattern)
    # Now, how do you initialize a numpy array?
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        next(csv_reader)  # Skip first row
        passenger_data = []

        # May have to completely remove PassengerID and some other variables categories to avoid unnecessary noise.
        for row in csv_reader:
            arr_row = row
            # Extract only the title of the name, and put it in the place of the original full name.
            if result := regex.search(pattern=title_compile, string=arr_row[3]):
                # print(result.group(1))
                arr_row[3] = result.group(1)
                passenger_data.append(arr_row)
                line_count += 1
            age = arr_row[5]
            status = arr_row[1]
            embarked = arr_row[-1]
            gender = arr_row[4]
            status_list.append(float(status))
            if age != "":
                age_extracted_to_list(float(age))
            if gender == "male":
                arr_row[4] = "1"
            elif gender == "female":
                arr_row[4] = "0"
            # Remove the columns as the final step in feature extraction.
            # Remove the passengerID columns
            # eliminate_columns(arr_row, 0)

        # After eliminating all columns, turn the whole data into an array.
        fill_blanks_with_means(passenger_data)
        passenger_data = np.asarray(passenger_data)
        return passenger_data


def eliminate_columns(data, *cols):
    # Note: eliminate columns should be the last step in feature engineering I think.
    """TO-DO: Might use this to work with the whole ndarray instead of just each row in the nested list."""
    cols = sorted(cols)
    data = np.delete(data, cols[0], axis=1)
    for i in range(1, len(cols)):
        data = np.delete(data, cols[i] - i, axis=1)
    return data


# This is a not good function
def age_extracted_to_list(age: float):
    age_list.append(age)
    #print(age_list)
    #print(len(age_list))


def fill_blanks_with_means(passenger_data: list):
    """This is the second loop to fill in the blanks of necessary stuff
    In the future, might make it more general."""
    mean = round(sum(age_list) / len(age_list), 3)
    age_list.clear()
    for passenger in passenger_data:
        age = passenger[5]
        if age == "":
            passenger[5] = mean
        age_list.append(float(passenger[5]))
        #print(passenger)
        #print(len(age_list))


def missing_data(col: int):
    missing = 0
    for passenger in data:
        if passenger[col] == "":
            missing += 1
            print(passenger)
    return f" Total number of entries: {data.shape[0]}. Missing data in column {col}: {missing}"


def frequency_dict(col: int):
    """Generate a frequency dictionary of a column of each passenger"""
    result = {}
    for passenger in data:
        if passenger[col] != "":
            result[passenger[col]] = result.get(passenger[col], 0) + 1
    return result


def fill_blanks_with_means(passenger_data: list):
    """This is the second loop to fill in the blanks of necessary stuff"""
    mean = round(sum(age_list) / len(age_list), 3)
    age_list.clear()
    for passenger in passenger_data:
        age = passenger[5]
        if age == "":
            passenger[5] = mean
        age_list.append(float(passenger[5]))
        #print(passenger)
        #print(len(age_list))


def fill_blanks_with_modes(col: int):
    freq_dict = frequency_dict(col)
    #print(freq_dict)
    most_common = list(freq_dict.keys())[list(freq_dict.values()).index(max(freq_dict.values()))]
    for passenger in data:
        if passenger[col] == "":
            passenger[col] = most_common
            #print(passenger)


def change_categorical_data_into_index_of_that_data_key_in_the_freq_dict(col: int):
    freq_dict = frequency_dict(col)
    for passenger in data:
        passenger[col] = list(freq_dict.keys()).index(passenger[col])


for i in range(len(age_list)):
    print(age_list[i], status_list[i])

if __name__ == "__main__":
    data = extract_data(file_path=titanic_path)
    print(data.shape)

    # Remember, there is no automatic algorithm to categorize the bins limits, for your knowledge level anyways, Huy.
    # The function lies in Tensorflow library, but you don't have to know that.
    # This is trial-and-error, tho with some brute-force solution to find the maximum differences possible
    # among the bins, you can kinda do it.
    bins = {
        9: [0, 0],
        17: [0, 0],
        30: [0, 0],
        38: [0, 0],
        65: [0, 0],
        max(age_list): [0, 0]
    }
    for i in range(len(age_list)):
        for upper_limits in bins.keys():
            if age_list[i] <= upper_limits:
                bins[upper_limits][0] += status_list[i]
                bins[upper_limits][1] += 1
                # Do sth to the numpy array data. Replace the age value of each of the row in the numpy array
                # into a binary representation of the bin the age value is in.
                # age group is currently in index 5.
                # print(data[i])
                data[i][5] = str(list(bins.keys()).index(upper_limits))
                # print(data[i])
                break

    for [interval, total] in bins.items():
        bins[interval] = total[0] / total[1]
        # bins[interval] = bins[list(bins.keys()).index(interval)]

    # Check for missing data in certain columns
    missing_embarked = missing_data(-1)
    missing_gender = missing_data(4)
    missing_survived = missing_data(1)
    print(f"Missing embarked: {missing_embarked}")
    print(f"Missing gender: {missing_gender}")
    print(f"Missing survived: {missing_survived}")
    print(bins)

    # Fill the data for the missing embarked value.
    fill_blanks_with_modes(-1)

    # Change values to a numerical version: Embarked!
    change_categorical_data_into_index_of_that_data_key_in_the_freq_dict(-1)
    # Last step: Delete the columns
    data = eliminate_columns(data, 0, 3, 6, 7, 8, 9, 10)
    # Drop the PassengerID, Name, SibSp, Parch, Ticket, Fare, Cabin
    print(data.shape)
    print(data[0])
    # First one should be 0, 3 (p_class), 1 (male sex), 2 (age_bin), 0 (Embarked Value)

    # Efficiency may be horrible, but at least we're done for now. Tensorflow tomorrow.