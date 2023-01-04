#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 04 14:45:33 2022
@author: Sai Bannur

This is a file processor that allows to generate relevant statistics from F1 data.
"""

import sys
import pandas as pd
import matplotlib.pyplot as plot

def handle_question(question: int, files: str) -> None:
    """
    Takes in the question number and filename and 
    prints formatted contents to .csv file and plots its graph
    """
    if question == 1:
        df: pd.DataFrame = handle_question_one(files)
        print_answer_csv(df)
        plot_answer(question, df)
    if question == 2:
        df: pd.DataFrame = handle_question_two_three(files, "driverId", "nationality", 7)
        print_answer_csv(df)
        plot_answer(question, df)
    if question == 3:
        df: pd.DataFrame = handle_question_two_three(files, "constructorId", "name", 2)
        print_answer_csv(df)
        plot_answer(question, df)
    if question == 4:
        df: pd.DataFrame = handle_question_four(files)
        print_answer_csv(df)
        plot_answer(question, df)
    if question == 5:
        df: pd.DataFrame = handle_question_five(files)
        print_answer_csv(df)
        plot_answer(question, df)

def add_missing(df2: pd.DataFrame, length: int, id: str) -> pd.DataFrame:
    """
    Takes in a Dataframe and adds temporary 
    rows if it is missing any contents
    """

    i: int = 0
    while i < length:
        if i != df2[id][i] - 1:
            if id == "driverId":
                df2.loc[df2.shape[0]] = [i + 1,"N\A","N\A","N\A","N\A","N\A","N\A","N\A","N\A"]
            else:
                df2.loc[df2.shape[0]] = [i + 1, "N\A", "N\A", "N\A", "N\A"]
            df2 = df2.sort_values(id)
            df2 = df2.reset_index(drop=True)
            length = len(df2)
        i = i + 1
    return df2

def handle_question_one(files: str) -> pd.DataFrame:
    """
    Takes in the filename and extracts data to 
    output the top 20 drivers with the most wins
    """

    df: pd.DataFrame = pd.read_csv(files[1], usecols=["driverId", "positionOrder"]) # reads in two specific columns of the .csv file
    df2: pd.DataFrame = pd.read_csv(files[0]) 
    df2 = df2.sort_values("driverId").reset_index(drop=True) # sorts contents of file according to specific column and resets index
    df3: pd.DataFrame = df.loc[df["positionOrder"] == 1] # locates all the first place winner in any race
    df2 = add_missing(df2, len(df2), "driverId") # adds placeholder information to dataframe missing any rows
    trackWins: list[list[int]] = [[0 for i in range(2)] for j in range(len(df2))]

    # counts the number of wins a particular person has using the driverId
    y: int = 0
    for x in df3.positionOrder:
        trackWins[df3.values[y][0]][1] += 1
        trackWins[df3.values[y][0]][0] = df3.values[y][0]
        y = y + 1

    # switches the driverId with the racer's firstname/lastname
    p: int = 0
    for k in trackWins:

        trackWins[p][0] = df2.values[k[0] - 1][4] + " " + df2.values[k[0] - 1][5]
        p = p + 1
    
    trackWins = sorted(trackWins, key=lambda x: (-x[1], x[0]), reverse=False) # sorts by most wins then lexicographically 
    trackWins = trackWins[:20] # only store the top 20

    df4: pd.DataFrame = pd.DataFrame(trackWins, columns=["subject", "statistic"]) # converts 2D array back to dataframe

    return df4

def handle_question_two_three(files: str, id: str, value: str, index: int) -> pd.DataFrame:
    """
    Takes in the filename and extracts data to 
    output the top  10 countries with most race-winners or
    top 10 constructors with most wins depending on the 
    id passed to the method
    """

    df: pd.DataFrame = pd.read_csv(files[1], usecols=[id, "positionOrder"]) # reads in  specific columns of the .csv file
    df = df.loc[df["positionOrder"] == 1] # locates all the first place winner in any race
    df_nationality: pd.DataFrame = pd.read_csv(files[0])
    df_nationality2: pd.DataFrame = df_nationality.sort_values(id).reset_index(drop=True) # sorts contents of file according to specific column and resets index
    df_nationality2 = add_missing(df_nationality2, len(df_nationality2), id) # adds placeholder information to dataframe missing any rows
    df_n: pd.DataFrame = df_nationality2[value].T.drop_duplicates().T.reset_index(drop=True) # contains all the countries, no duplicates

    arr_of_n = [[0 for i in range(2)] for j in range(len(df_n))]
    trackWins = [[0 for i in range(3)] for j in range(len(df))]
    
    # counts the number of wins a particular person has using the driverId
    y: int = 0
    for x in df.positionOrder:
        trackWins[df.values[y][0]][1] += 1
        trackWins[df.values[y][0]][0] = df.values[y][0]
        y = y + 1

    trackWins = sorted(trackWins, key=lambda x: (x[1], -x[0]), reverse=True) 

    # finds a winners nationality, and increments number wins of specific nationality to find the countries with most wins
    z: int = 0
    for y in trackWins:
        r: int = 0
        if y[0] == 0:
            break
        for l in df_n:
            if l == df_nationality2.values[y[0] - 1][index]:
                arr_of_n[r][0] = l
                arr_of_n[r][1] += trackWins[z][1]
            r = r + 1
        z = z + 1

    arr_of_n = sorted(arr_of_n, key=lambda x: (-x[1], x[0])) # sorts by most wins then lexicographically 
    df4: pd.DataFrame = pd.DataFrame(arr_of_n[:10], columns=["subject", "statistic"]) # converts array back to dataframe

    return df4

def handle_question_four(files: str) -> pd.DataFrame:
    """
    Takes in the filename and extracts data to 
    output the top 20 countries with most hosted F1 races
    """

    df: pd.DataFrame = pd.read_csv(files[0], usecols=["circuitId", "country"]) # reads in  specific columns of the .csv file
    df_n: pd.DataFrame = (df["country"].T.drop_duplicates().T.reset_index(drop=True))  # contains all the countries
    df_races: pd.DataFrame = pd.read_csv(files[1])
    df_races = df_races["circuitId"] # tracks all circuitId 
    circuit_arr: pd.DataFrame = [[0 for i in range(2)] for j in range(len(df))]
    country_arr: pd.DataFrame = [[0 for i in range(2)] for j in range(len(df_n))]

    r: int = 0
    # finds all the circuit id of a particular race and its hosted country
    for x in df.circuitId:
        circuit_arr[r][0] = df.values[r][0]
        circuit_arr[r][1] = df.values[r][1]
        r = r + 1
   
    r = 0
    # a 2D array with all the countries in the first index, second element empty for now
    for d in df_n:
        country_arr[r][0] = d
        r = r + 1

    # fills second element of 2D array with total number hosted by country
    for k in df_races:
        for j in circuit_arr:
            if k == j[0]:
                for l in country_arr:
                    if l[0] == j[1]:
                        l[1] += 1
    
    country_arr = sorted(country_arr, key=lambda x: (-x[1], x[0]), reverse=False) # organzies numerically then lexiographically
    country_arr = country_arr[:20] # finds top 20 countries
    df4: pd.DataFrame = pd.DataFrame(country_arr, columns=["subject", "statistic"]) # converts array to dataframe

    return df4

def handle_question_five(files: str) -> pd.DataFrame:
    """
    Takes in the filename and extracts data to 
    output the top 5 drivers with most wins in 
    F1 history who started a race not being on pole
    position
    """

    df: pd.DataFrame = pd.read_csv(files[1], usecols=["driverId", "positionOrder", "grid"])  # reads in  specific columns of the .csv file
    df2: pd.DataFrame = pd.read_csv(files[0])
    df2 = df2.sort_values("driverId").reset_index(drop=True)  # sorts contents of file according to specific column and resets index
    df3: pd.DataFrame = df.loc[df["positionOrder"] == 1] # locates all the first place winner in any race
    df3 = df3.loc[df["grid"] != 1] # sorts players who did not begin in pole posiiton
    df2 = add_missing(df2, len(df2), "driverId") # adds temporary dumby information if file contains missing rows
    trackWins = [[0 for i in range(2)] for j in range(len(df2))]

    y: int = 0
    # sorts number of total wins of players without starting on pole posiiton
    for x in df3.positionOrder:
        trackWins[df3.values[y][0]][1] += 1
        trackWins[df3.values[y][0]][0] = df3.values[y][0]
        y = y + 1

    trackWins = sorted(trackWins, key=lambda x: (-x[1], x[0]), reverse=False)
    trackWins = trackWins[:5] # finds the top 5

    p: int = 0
    # changes driverId with players name
    for k in trackWins:
        trackWins[p][0] = df2.values[k[0] - 1][4] + " " + df2.values[k[0] - 1][5]
        p = p + 1
    df4: pd.DataFrame = pd.DataFrame(trackWins, columns=["subject", "statistic"]) # converts array to dataframe
    return df4

def print_answer_csv(df: pd.DataFrame) -> None:
    """
    Prints the DataFrame to .csv file
    """
    df.to_csv("output.csv", index=False)

def plot_answer(question: int, df: pd.DataFrame) -> None:
    """
    Plots the DataFrame to different type of graphs
    """
    if question == 1:
        # plots a horizontal bar graph
        df.plot.barh(x="subject", y="statistic",figsize=(15, 10), title="Top 20 Drivers With Most Wins in F1 History", color="green")
        plot.savefig("output_graph_q1.png")
    elif question == 2:
        # plots a pie char
        df.plot.pie(labels=df["subject"].values, x="subject", y="statistic", figsize=(6, 6), legend=None, autopct="%1.1f%%")
        plot.title("Top 10 Countries with Most Race-Winners in F1 History")
        plot.savefig("output_graph_q2.png")
    elif question == 3:
        # plots a horizaontal bar chart
        df.plot.barh( x="subject", y="statistic", figsize=(9, 5), title="The Top 10 Constructors With Most Wins in F1" )
        plot.savefig("output_graph_q3.png")
    elif question == 4:
        # plot a pie chart
        df.plot.pie(labels=df["subject"].values, x="subject", y="statistic", figsize=(8, 8), legend=None, autopct="%1.1f%%")
        plot.title("Top 20 Countries With Most Hosted F1 Races")
        plot.savefig("output_graph_q4.png")
    elif question == 5:
        #  plots a vertical bar graph
        plot.rc("font", size=6)
        plot.rc("axes", titlesize=11)
        df.plot.bar(x="subject", y="statistic", figsize=(7, 7), title="The Top 5 Drivers with most Wins in\n F1 History Who Started a Race not being on Pole Position", color="pink")
        plot.xticks(rotation=40)
        plot.savefig("output_graph_q5.png")

def main():
    """The main entry of the program."""
    arg1: str = sys.argv[1] # gets 2nd argument - the question and its number
    arg2: str = sys.argv[2] # gets 3rd argument - the file names

    files_separated: str = arg2[8:] # contains both files names with comma between
    question_number: int = int(arg1[11:]) # the number of the question separated
    letter_list: list[str] = files_separated.split(",") # separates filename by comma in list
    
    handle_question(question_number, letter_list) # begins the construction of the statistical data

if __name__ == "__main__":
    main()
