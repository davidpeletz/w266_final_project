import pandas as pd
import progressbar
from time import sleep


def convert_csv_to_text():
    retrain_df = pd.read_csv("../../data/interim/retrain_processed.csv")
    f = open("../../data/interim/retrain_processed.txt", "w+")
    f.write("-DOCSTART- O\n\n")
    bar = progressbar.ProgressBar(maxval=len(retrain_df), \
                                  widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    for i, row in retrain_df.iterrows():
        current_name = row["Name"]
        multiple_words = False
        bar.update(i + 1)

        if current_name.count(" ") > 0:
            multiple_words = True

        for index, split_name in enumerate(current_name.split(" ")):

            if index == 0:
                f.write(split_name + " " + "B-PER\n")
            else:
                f.write(split_name + " " + "I-PER\n")

        f.write("\n")
    f.close()
    bar.finish()


convert_csv_to_text()
