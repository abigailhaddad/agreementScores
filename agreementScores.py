# -*- coding: utf-8 -*-
"""
This calculates agreement scores between every 'Name' in a file 
where each row represents how they voted in particular match-ups

"""
import os
import pandas as pd

def clean(df):
    #gets the set of names
    uniqueNames=df['Name'].unique()
    #reshapes it so each row is a Name/Matchup
    dfLong=pd.melt(df,id_vars=['Name'],var_name='Matchup', value_name='Pick')
    #drops blanks
    dfNonBlank=dfLong.dropna()
    #creates blank df that will be our final outcomes
    colNames=['Person A', 'Person B', 'Number of Matchups', 'Number of Agreements']
    aggDF=pd.DataFrame(columns=colNames)
    #we're interested in each combination of people
    for personA in uniqueNames:
        for personB in uniqueNames:
            #but we don't need to calculate A vs A 
            if (personA!=personB):
                #keep all matchups judged by A or B
                keepDF=dfNonBlank.loc[dfNonBlank['Name'].isin([personA, personB])]
                #just keep the ones that we have two verdicts on (they both judged)
                allpicks=keepDF.groupby('Matchup').count()
                #and then get the matchup names
                overlap=allpicks.loc[allpicks['Name']==2].index
                #get all the results from the overlap group (where they both judged)
                toKeep=keepDF.loc[keepDF['Matchup'].isin(overlap)]
                #get total unique number of picks
                nonDupes=toKeep[['Matchup', 'Pick']].drop_duplicates()
                #if they agree on all, the nonduplicate # will be the same as the total votes/2
                Disagree=len(nonDupes)-len(toKeep)/2
                #number of agreements is total matchups/2 minus disagreements
                Agree=len(toKeep)/2-Disagree
                #put that info into a series
                newRow=pd.Series([personA, personB, len(toKeep)/2, Agree], index=colNames)
                #append it to the DF
                aggDF=aggDF.append(newRow, ignore_index=True)
    return(aggDF)

def main():
    #change directory
    os.chdir(os.getcwd().replace("code","data"))
    #read the data
    df=pd.read_excel('Greatest Cartoon Ever Data.xlsx')
    #call function that cleans the data
    results=clean(df)
    #calculate percentage agreement
    results['percentAgree']=results['Number of Agreements']/results['Number of Matchups']
    #sort and output to a file
    results.sort_values(['percentAgree']).to_excel("Results.xlsx", index=False)
    
main()


            
            
        