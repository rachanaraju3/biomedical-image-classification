import csv
import os

"""Code for aggregating the relevant data images and labeling them."""


"""Prepare a CSV subset of the release-midas csv file based on midas_distance.

Assumes that data has already been downloaded from https://stanfordaimi.azurewebsites.net/datasets/f4c2020f-801a-42dd-a477-a1a8357ef2a5 and that the xlsx file was converted to a csv file and stored in "data/" in the root directory.

Args:
    csv_path            (str): Path to the metadata CSV file. Defaults to `../data/release_midas.csv`
    midas_distance      (list of str): The distance at which the images were taken at. Options are {"1ft", "6in", "dscope", "n/a - virtual"}
    midas_path_shorten  (bool): If true filter down the midas_path to just malignant, benign, other or control. Defaults to false.
    output_path         (str): Path to write the filtered subset to. Defaults to `../data/filtered_midas.csv`
"""
def subset(csv_path=None,midas_distance=None, midas_path_shorten=False,output_path=None):
    if csv_path is None:
        csv_path = os.path.join("data", "release_midas.csv")
    if midas_distance is None:
        midas_distance = ["1ft", "6in", "dscope", "n/a - virtual"]
    if output_path is None:
        output_path = os.path.join("data","filtered_midas.csv")
    filtered_rows = []
    with open(csv_path, "r", encoding='utf-8') as file:
        reader = csv.DictReader(file)
        field_names = reader.fieldnames

        for row in reader:
            if row["midas_distance"] in midas_distance:
                if row["midas_path"] == "" and row["midas_iscontrol"] == "yes":
                    row["midas_path"] = "control"
                if midas_path_shorten:
                    path = row["midas_path"].split("-")
                    row["midas_path"] = path[0]
                filtered_rows.append(row)
        
    with open(output_path, 'w', encoding='utf-8', newline='') as subset:
        writer = csv.DictWriter(subset, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(filtered_rows)

    print(f"\nSaved to {output_path}")
    print(f"Total columns: {len(field_names)}")
    print(f"Total rows: {len(filtered_rows)}")

subset(midas_distance=["6in"], midas_path_shorten=True)