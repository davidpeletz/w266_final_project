import pandas as pd


def ingest_data():
    first_name_df = pd.read_csv("../../data/interim/first_name_df.csv")
    last_name_df = pd.read_csv("../../data/interim/whole_last_name_df.csv")
    rt_last_name_df = pd.read_csv("../../data/interim/retrain_ln_df.csv", index_col=0)
    first_name_df = first_name_df.drop(columns=["Unnamed: 0"])
    last_name_df = last_name_df.drop(columns=["Unnamed: 0"])
    first_name_df["firstname"] = first_name_df["firstname"].apply(lambda x: str(x).title())

    return first_name_df, last_name_df, rt_last_name_df


def get_retrain_data(input_df):
    hispanic_fn = input_df.sort_values(by=["pcthispanic", "obs"], ascending=False).loc[input_df["pctwhite"] < 40]
    black_fn = input_df.sort_values(by=["pctblack", "obs"], ascending=False).loc[
        input_df["pctwhite"] < 40]
    api_fn = input_df.sort_values(by=["pctapi", "obs"], ascending=False).loc[
        input_df["pctwhite"] < 40]

    api_fn_list = list(api_fn["firstname"])
    hispanic_fn_list = list(hispanic_fn["firstname"])
    black_fn_list = list(black_fn["firstname"])

    return hispanic_fn_list, api_fn_list, black_fn_list


def get_first_names(input_df):
    white_fn = input_df.sort_values(by=["pctwhite", "obs"], ascending=False).loc[input_df["obs"] > 10000][:20]
    hispanic_fn = input_df.sort_values(by=["pcthispanic", "obs"], ascending=False).loc[
                      input_df["obs"] > 1000][
                  :20]

    api_fn = input_df.sort_values(by=["pctapi", "obs"], ascending=False).loc[
                 input_df["obs"] > 200][:20]
    black_fn = input_df.sort_values(by=["pctblack", "obs"], ascending=False).loc[
                   input_df["obs"] > 25][:20]
    api_fn_list = list(api_fn["firstname"])
    hispanic_fn_list = list(hispanic_fn["firstname"])
    black_fn_list = list(black_fn["firstname"])
    white_fn_list = list(white_fn["firstname"])
    return hispanic_fn_list, api_fn_list, black_fn_list, white_fn_list


def get_last_names(input_df):
    white_ln_list = input_df.loc[input_df["Given Race"] == "White"].reset_index(drop=True)[
        "Last name / Surname"]
    black_ln_list = input_df.loc[input_df["Given Race"] == "Black"].reset_index(drop=True)[
        "Last name / Surname"]
    api_ln_list = input_df.loc[input_df["Given Race"] == "Asian & Pacific Islander"].reset_index(drop=True)[
        "Last name / Surname"]
    hispanic_ln_list = input_df.loc[input_df["Given Race"] == "Hispanic"].reset_index(drop=True)[
        "Last name / Surname"]

    return hispanic_ln_list, api_ln_list, white_ln_list, black_ln_list


def generate_full_names(first_names, last_names):
    full_names = [i + " " + j for i in first_names for j in last_names]
    return full_names


def form_df(first_name_list, last_name_list, input_full_names, race_name):
    first_name_df = pd.DataFrame(first_name_list, columns=["Name"])
    last_name_df = pd.DataFrame(list(last_name_list), columns=["Name"])
    combined_name_df = pd.DataFrame(input_full_names, columns=["Name"])
    total_df = pd.concat([first_name_df, last_name_df, combined_name_df]).reset_index(drop=True)
    total_df["Race"] = race_name
    return total_df


def form_whole_df():
    first_name_df, last_name_df, rt_last_name_df = ingest_data()

    rt_threshold = 50
    hispanic_ln_list, api_ln_list, white_ln_list, black_ln_list = get_last_names(last_name_df)
    rt_hispanic_ln_list, rt_api_ln_list, rt_white_ln_list, rt_black_ln_list = get_last_names(rt_last_name_df)
    rt_hispanic_ln_list, rt_api_ln_list, rt_black_ln_list = rt_hispanic_ln_list[
                                                            :rt_threshold], rt_api_ln_list[
                                                                            :rt_threshold], rt_black_ln_list[
                                                                                            :rt_threshold]

    hispanic_fn_list, api_fn_list, black_fn_list, white_fn_list = get_first_names(first_name_df)

    rt_hispanic_fn_list, rt_api_fn_list, rt_black_fn_list = get_retrain_data(first_name_df)
    rt_hispanic_fn_list, rt_api_fn_list, rt_black_fn_list = rt_hispanic_fn_list[:rt_threshold], rt_api_fn_list[
                                                                                                :rt_threshold], rt_black_fn_list[
                                                                                                                :rt_threshold]

    rt_hispanic_fn_list = [i for i in rt_hispanic_fn_list if i not in hispanic_fn_list]
    rt_api_fn_list = [i for i in rt_api_fn_list if i not in api_fn_list]
    rt_black_fn_list = [i for i in rt_black_fn_list if i not in black_fn_list]

    rt_api_full_names = generate_full_names(rt_api_fn_list, rt_api_ln_list)
    rt_black_full_names = generate_full_names(rt_black_fn_list, rt_black_ln_list)
    rt_hispanic_full_names = generate_full_names(rt_hispanic_fn_list, rt_hispanic_ln_list)

    api_full_names = generate_full_names(api_fn_list, api_ln_list)
    hispanic_full_names = generate_full_names(hispanic_fn_list, hispanic_ln_list)
    black_full_names = generate_full_names(black_fn_list, black_ln_list)
    white_full_names = generate_full_names(white_fn_list, white_ln_list)

    rt_total_hispanic_df = form_df(rt_hispanic_fn_list, rt_hispanic_ln_list, rt_hispanic_full_names, "Hispanic")
    rt_total_black_df = form_df(rt_black_fn_list, rt_black_ln_list, rt_black_full_names, "Black")
    rt_total_api_df = form_df(rt_api_fn_list, rt_api_ln_list, rt_api_full_names, "API")
    rt_whole_df = pd.concat([rt_total_hispanic_df,
                             rt_total_black_df,
                             rt_total_api_df]).reset_index(drop=True)
    rt_copy_df = rt_whole_df.copy()

    rt_copy_df["Name"] = rt_copy_df["Name"].apply(lambda x: str(x).lower())
    rt_total_df = pd.concat([rt_whole_df, rt_copy_df]).drop_duplicates().reset_index(drop=True)

    updated_rt_df = rt_copy_df.copy()
    updated_rt_df["Name"] = updated_rt_df["Name"].apply(
        lambda x: "I went to pick " + str(x) + " up at the train station.")

    rt_fabricated_df = rt_copy_df.copy()
    rt_fabricated_df["Name"] = rt_fabricated_df["Name"].apply(lambda x: str(x) + " went to the store.")

    rt_final_df = pd.concat([rt_total_df, rt_fabricated_df]).drop_duplicates().reset_index(drop=True)
    print(rt_final_df.shape)
    print(rt_final_df["Race"].value_counts())
    rt_final_df.to_csv("../../data/interim/retrain_processed.csv")

    total_name_list = list(rt_whole_df["Name"])

    total_hispanic_df = form_df(hispanic_fn_list, hispanic_ln_list, hispanic_full_names, "Hispanic")
    total_api_df = form_df(api_fn_list, api_ln_list, api_full_names, "API")
    total_white_df = form_df(white_fn_list, white_ln_list, white_full_names, "White")
    total_black_df = form_df(black_fn_list, black_ln_list, black_full_names, "Black")

    whole_df = pd.concat([total_white_df,
                          total_black_df,
                          total_api_df,
                          total_hispanic_df]).reset_index(drop=True)
    whole_df = whole_df.loc[~whole_df["Name"].isin(total_name_list)]
    another_df = whole_df.copy()

    another_df["Name"] = another_df["Name"].apply(lambda x: str(x).lower())
    total_df = pd.concat([whole_df, another_df]).drop_duplicates().reset_index(drop=True)
    fabricated_df = total_df.copy()
    fabricated_df["Name"] = fabricated_df["Name"].apply(lambda x: str(x) + " went to the store.")
    final_df = pd.concat([total_df, fabricated_df]).drop_duplicates().reset_index(drop=True)
    print(final_df.shape)
    print(final_df["Race"].value_counts())
    final_df.to_csv("../../data/interim/processed_df.csv")


form_whole_df()
