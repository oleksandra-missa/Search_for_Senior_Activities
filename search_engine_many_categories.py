import pandas as pd
from Activity import Activity
from datetime import datetime, timedelta

from Cas import Cas

#Loading of excel files
xls = pd.ExcelFile("CAS_data.xlsx")
sheets = {sheet_name: xls.parse(sheet_name) for sheet_name in xls.sheet_names}
df_zajecia = sheets["Classes"]
df_casy = sheets["CAS_OpenData"]




def LoadDataFromCas(df_casy):
    # Loading CAS centers
    for index, row in df_casy.iterrows():
        VariablesInCas = [row[column] for column in df_casy.columns]

        temporaryCas = Cas(
            VariablesInCas[0],
            VariablesInCas[1],
            VariablesInCas[2],
            VariablesInCas[3],
            VariablesInCas[4],
            VariablesInCas[5],
            VariablesInCas[6],
            VariablesInCas[7],
            VariablesInCas[8],
            VariablesInCas[9],
            VariablesInCas[10],
            VariablesInCas[11],
            VariablesInCas[12],
            VariablesInCas[13],
            VariablesInCas[14],
            VariablesInCas[15],
            VariablesInCas[16],
        )
        temporaryCas.addCas()

    # Loading activities
    for index, row in df_zajecia.iterrows():
        VariablesInZajecia = [row[column] for column in df_zajecia.columns]

        temporaryZajecia = Activity(
            VariablesInZajecia[0],
            VariablesInZajecia[1],
            VariablesInZajecia[2],
            VariablesInZajecia[3],
            VariablesInZajecia[4],
            VariablesInZajecia[5],
            VariablesInZajecia[6],
            VariablesInZajecia[7],
            VariablesInZajecia[8],
        )
        temporaryZajecia.addZajecia()

        temporaryZajecia.addCas(Cas.Casy[-1])

CategorieList = ["Zajęcia edukacyjne","Aktywność fizyczna","Twórczość i hobby","Integracja i wycieczki"]

def SearchZajeciaByManyParameters(CategoriesSelected,MinPrice,MaxPrice,SelectedDay,SelectedHour,TypesSelected):
    searched_activities = []

    for zajecia in Activity.Activitivity_list:
        got_requirments = 1

        global CategorieList
        i = 0

        Correct = 0
        n_cols = min(len(CategoriesSelected[0]), len(CategoriesSelected[1]))
        for i in range(n_cols):
            name = CategoriesSelected[0][i]
            flag = CategoriesSelected[1][i]
            if name == zajecia.Kategoria and flag == 1:
                Correct = 1
        if Correct == 0:
            got_requirments = 0

        #Sorting by minimal price
        if zajecia.Price<float(MinPrice):
            got_requirments = 0

        #Sorting by maximal price
        if zajecia.Price>float(MaxPrice):
            got_requirments = 0

        #Sorting by minimal day and hour
        if zajecia.Start.date() <= SelectedDay +timedelta(hours=SelectedHour):
            got_requirments = 0

        #Sort by online/offline
        Correct = 0
        if TypesSelected[1][0] == 1 and zajecia.On_offline == "Stacjonarny":
            Correct = 1
        if TypesSelected[1][1] == 1 and zajecia.On_offline == "Online":
            Correct = 1

        if Correct == 0:
            got_requirments = 0

        if got_requirments == 1:
            searched_activities.append(zajecia)


    return searched_activities
data_initalised = 0

def initalizeData():
    global data_initalised
    if data_initalised == 0:
        Cas.Casy.clear()
        Activity.Activitivity_list.clear()
        LoadDataFromCas(df_casy)


        data_initalised = 1

initalizeData()

