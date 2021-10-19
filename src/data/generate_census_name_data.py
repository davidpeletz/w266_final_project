import requests
import pandas as pd
import io


def get_black_df():
    global URL, r, df_list, black_df
    URL = "https://namecensus.com/data/black.html"
    r = requests.get(URL)

    df_list = pd.read_html(r.text)  # this parses all the tables in webpages to a list
    black_df = df_list[0]
    black_df.columns = black_df.iloc[0]
    black_df = black_df.drop(black_df.index[0])
    black_df["% of people with surname self-identifying as 'black'"] = black_df[
        "% of people with surname self-identifying as 'black'"].apply(lambda x: float(x[:-1]))
    black_df = black_df.sort_values(
        by=["% of people with surname self-identifying as 'black'", "Surname rank among blacks"],
        ascending=[False, True])
    black_df["Last name / Surname"] = black_df["Last name / Surname"].apply(lambda x: str(x).title())
    black_df["Given Race"] = "Black"
    black_df = black_df.rename(columns={
        "Number of occurrences among people self-identifying as 'black'": 'Number of occurences among people self-identifying as given race',
        'Surname rank among blacks': 'Surname rank among given race',
        "% of people with surname self-identifying as 'black'": "% of people with surname self-identifying as given race"})
    return black_df


def get_white_df():
    global URL, r, df_list, white_dfopenpyxl
    URL = "https://namecensus.com/data/white.html"
    r = requests.get(URL)

    df_list = pd.read_html(r.text)  # this parses all the tables in webpages to a list
    white_df = df_list[0]
    white_df.columns = white_df.iloc[0]
    white_df = white_df.drop(white_df.index[0])
    white_df["Number of occurrences among people self-identifying as \'white\'"] = white_df[
        "Number of occurrences among people self-identifying as \'white\'"].apply(lambda x: float(x))
    white_df["% of people with surname self-identifying as 'white'"] = white_df[
        "% of people with surname self-identifying as 'white'"].apply(lambda x: float(x[:-1]))
    white_df = white_df.sort_values(
        by=["% of people with surname self-identifying as 'white'", "Surname rank among whites"],
        ascending=[False, True])
    white_df["Last name / Surname"] = white_df["Last name / Surname"].apply(lambda x: str(x).title())
    white_df["Given Race"] = "White"
    white_df = white_df.rename(columns={
        "Number of occurrences among people self-identifying as 'white'": 'Number of occurences among people self-identifying as given race',
        'Surname rank among whites': 'Surname rank among given race',
        "% of people with surname self-identifying as 'white'": "% of people with surname self-identifying as given race"})
    return white_df


def get_hispanic_df():
    global URL, r, df_list, hispanic_df
    URL = "https://namecensus.com/data/hispanic.html"
    r = requests.get(URL)

    df_list = pd.read_html(r.text)  # this parses all the tables in webpages to a list
    hispanic_df = df_list[0]
    hispanic_df.columns = hispanic_df.iloc[0]
    hispanic_df = hispanic_df.drop(hispanic_df.index[0])
    hispanic_df["Number of occurrences among people self-identifying as \'Hispanic\'"] = hispanic_df[
        "Number of occurrences among people self-identifying as \'Hispanic\'"].apply(lambda x: float(x))
    hispanic_df["% of people with surname self-identifying as 'hispanic'"] = hispanic_df[
        "% of people with surname self-identifying as 'hispanic'"].apply(lambda x: float(x[:-1]))
    hispanic_df = hispanic_df.sort_values(
        by=["% of people with surname self-identifying as 'hispanic'", "Surname rank among hispanics"],
        ascending=[False, True])
    hispanic_df["Last name / Surname"] = hispanic_df["Last name / Surname"].apply(lambda x: str(x).title())
    hispanic_df["Given Race"] = "Hispanic"
    hispanic_df = hispanic_df.rename(columns={
        "Number of occurrences among people self-identifying as 'Hispanic'": 'Number of occurences among people self-identifying as given race',
        'Surname rank among hispanics': 'Surname rank among given race',
        "% of people with surname self-identifying as 'hispanic'": "% of people with surname self-identifying as given race"})
    return hispanic_df


def get_aapi_df():
    global URL, r, df_list, aapi_df
    URL = "https://namecensus.com/data/asian_pacific_islander.html"
    r = requests.get(URL)

    df_list = pd.read_html(r.text)  # this parses all the tables in webpages to a list
    aapi_df = df_list[0]
    aapi_df.columns = aapi_df.iloc[0]
    aapi_df = aapi_df.drop(aapi_df.index[0])
    aapi_df["Number of occurrences among people self-identifying as Asian & Pacific Islander"] = aapi_df[
        "Number of occurrences among people self-identifying as Asian & Pacific Islander"].apply(lambda x: float(x))
    aapi_df["% of people with surname self-identifying as 'Asian & Pacific Islander'"] = aapi_df[
        "% of people with surname self-identifying as 'Asian & Pacific Islander'"].apply(lambda x: float(x[:-1]))
    aapi_df = aapi_df.sort_values(by=["% of people with surname self-identifying as 'Asian & Pacific Islander'",
                                      "Surname rank among Asians & Pacific Islanders"], ascending=[False, True])
    aapi_df["Last name / Surname"] = aapi_df["Last name / Surname"].apply(lambda x: str(x).title())
    aapi_df["Given Race"] = "Asian & Pacific Islander"
    aapi_df = aapi_df.rename(columns={
        'Number of occurrences among people self-identifying as Asian & Pacific Islander': 'Number of occurences among people self-identifying as given race',
        'Surname rank among Asians & Pacific Islanders': 'Surname rank among given race',
        "% of people with surname self-identifying as 'Asian & Pacific Islander'": "% of people with surname self-identifying as given race"})
    return aapi_df


def get_indian_df():
    global URL, r, df_list, indian_df
    URL = "https://namecensus.com/data/indians.html"
    r = requests.get(URL)

    df_list = pd.read_html(r.text)  # this parses all the tables in webpages to a list
    indian_df = df_list[0]
    indian_df.columns = indian_df.iloc[0]
    indian_df = indian_df.drop(indian_df.index[0])
    indian_df["Number of occurences among people self-identifying as American Indian & Alaskan Native"] = indian_df[
        "Number of occurences among people self-identifying as American Indian & Alaskan Native"].apply(
        lambda x: float(x))
    indian_df["% of people with surname self-identifying as 'American Indian & Alaskan Native'"] = indian_df[
        "% of people with surname self-identifying as 'American Indian & Alaskan Native'"].apply(
        lambda x: float(x[:-1]))
    indian_df = indian_df.sort_values(
        by=["% of people with surname self-identifying as 'American Indian & Alaskan Native'",
            "Surname rank among American Indians & Alaskan Natives"], ascending=[False, True])
    indian_df["Last name / Surname"] = indian_df["Last name / Surname"].apply(lambda x: str(x).title())
    indian_df["Given Race"] = "American Indian & Alaskan Native"
    indian_df = indian_df.rename(columns={
        'Number of occurences among people self-identifying as American Indian & Alaskan Native': 'Number of occurences among people self-identifying as given race',
        'Surname rank among American Indians & Alaskan Natives': 'Surname rank among given race',
        "% of people with surname self-identifying as 'American Indian & Alaskan Native'": "% of people with surname self-identifying as given race"})
    return indian_df


def get_multi_race_df():
    global URL, r, df_list
    URL = "https://namecensus.com/data/two_race.html"
    r = requests.get(URL)

    df_list = pd.read_html(r.text)  # this parses all the tables in webpages to a list
    multi_race_df = df_list[0]
    multi_race_df.columns = multi_race_df.iloc[0]
    multi_race_df = multi_race_df.drop(multi_race_df.index[0])
    multi_race_df["2 or More Races"] = multi_race_df["2 or More Races"].apply(lambda x: float(x))
    multi_race_df["% of people with surname self-identifying as 'two or more races'"] = multi_race_df[
        "% of people with surname self-identifying as 'two or more races'"].apply(lambda x: float(x[:-1]))
    multi_race_df = multi_race_df.sort_values(
        by=["% of people with surname self-identifying as 'two or more races'",
            "Surname rank among 'two or more races'"],
        ascending=[False, True])
    multi_race_df["Last name / Surname"] = multi_race_df["Last name / Surname"].apply(lambda x: str(x).title())
    multi_race_df["Given Race"] = "Multi-Race"
    multi_race_df = multi_race_df.rename(
        columns={'2 or More Races': 'Number of occurences among people self-identifying as given race',
                 "Surname rank among 'two or more races'": 'Surname rank among given race',
                 "% of people with surname self-identifying as 'two or more races'": "% of people with surname self-identifying as given race"})
    return multi_race_df


def aggregate_data(input_df_list, threshold=100):
    return [i[:threshold] for i in input_df_list]


df_list = aggregate_data(
    [get_white_df(), get_black_df(), get_hispanic_df(), get_indian_df(), get_aapi_df(), get_multi_race_df()])

whole_last_name_df = pd.concat(df_list).reset_index(drop=True)

whole_last_name_df.to_csv("../../data/interim/whole_last_name_df.csv")

rt_last_name_list = aggregate_data(
    [get_black_df(), get_hispanic_df(), get_aapi_df()], threshold=-1)
last_names = list(whole_last_name_df["Last name / Surname"])

rt_df = pd.concat(rt_last_name_list).reset_index(drop=True)
rt_df = rt_df.loc[(~rt_df["Last name / Surname"].isin(last_names)) & (
        rt_df["% of people with surname self-identifying as given race"] >= 40)].reset_index(drop=True)
rt_df.to_csv("../../data/interim/retrain_ln_df.csv")

fn_df = pd.read_excel("../../data/raw/firstnames.xlsx", sheet_name="Data")
fn_df = fn_df[:-1]
fn_df.to_csv("../../data/interim/first_name_df.csv")
