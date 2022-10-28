import csv
import regex
import numpy as np

titanic_path = "train.csv"


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
            # Extract only the title of the name.
            if result := regex.search(pattern=title_compile, string=arr_row[3]):
                # print(result.group(1))
                arr_row[3] = result.group(1)
                passenger_data.append(arr_row)
                line_count += 1
        passenger_data = np.asarray(passenger_data)
        print(passenger_data.shape)


if __name__ == "__main__":
    extract_data(file_path=titanic_path)