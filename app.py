import streamlit as st
import os
import numpy as np
import pandas as pd
from apyori import apriori
import matplotlib.pyplot as plt

def process_file(filename):
    df = pd.read_csv(filename)    
    df1 = df['Description']
    df2 = df1.str.split(",", expand=True)
    #df2.fillna("", inplace = True) 
    #df2.dropna()
    df2.replace('1 x', '', regex=True, inplace=True)
    df2.replace('2 x', '', regex=True, inplace=True)
    df2.replace('3 x', '', regex=True, inplace=True)
    df2.replace('4 x', '', regex=True, inplace=True)
    df2.replace('5 x', '', regex=True, inplace=True)

    #st.write("Preview file : ")
    st.dataframe(df)

    #st.write("Processed file : ")
    st.dataframe(df2)
    return df2

def arm_model(support, confidence, lift):
    input = np.array([[support, confidence, lift]]).astype(np.float64)
    #prediction = model.predict_proba(input)
    return float(support)

def modelling(df, support, confidence, lift):
    df1 = df.copy()
    records = []

    for i in range(0, len(df1)):
        records.append([str(df1.values[i,j]) for j in range(0, 20)])

    #association_rules = apriori(records, min_support=0.0045, min_confidence=0.2, min_lift=3, min_length=2)
    association_rules = apriori(records, min_support=support, min_confidence=confidence, min_lift=int(lift), min_length=2)
    association_results = list(association_rules)

    return association_results


def getLength(association_results):
    return len(association_results)


def print_result(association_results):

    count = 0    

    for item in association_results:
    
        count += 1
        # first index of the inner list
        # Contains base item and add item
        pair = item[0] 
        items = [x for x in pair]
        print("(Rule " + str(count) + ") " + items[0] + " -> " + items[1])
        
        #second index of the inner list
        print("Support: " + str(round(item[1],3)))

        #third index of the list located at 0th
        #of the third index of the inner list

        print("Confidence: " + str(round(item[2][0][2],4)))
        print("Lift: " + str(round(item[2][0][3],4)))
        print("=====================================")

    #return print_item

def print_result2(association_results):

    count = 0    
    print_item = []

    for item in association_results:
    
        count += 1
        # first index of the inner list
        # Contains base item and add item
        pair = item[0] 
        items = [x for x in pair]
        line1 = "(Rule " + str(count) + ") " + items[0] + " -> " + items[1]
        
        #second index of the inner list
        line2 = "Support: " + str(round(item[1],3))

        #third index of the list located at 0th
        #of the third index of the inner list
        line3 = "Confidence: " + str(round(item[2][0][2],4))
        line4 = "Lift: " + str(round(item[2][0][3],4))

        #print("=====================================")
        print_item.append(line1+"\n"+line2+"\n"+line3+"\n"+line4)

    return print_item

def main():
    st.beta_container()
    st.beta_columns(2)
    #st.set_page_config(layout="centered")
    st.title("Association Rule Mining")
    html_temp = """
    <div style="background-color:#025246 ;padding:10px">
    <h2 style="color:white;text-align:center;">Association Rule Generator </h2>
    </div>
    </br>
    """

    st.markdown(html_temp, unsafe_allow_html=True)
    file = st.file_uploader('Select a dataset file.')
    if file is None:
        return None,None,None,None,None,None

    df = process_file(file)

    support     = st.number_input("Support", 0.01)
    confidence  = st.number_input("Confidence", 0.01)
    lift        = st.number_input("Lift", 2)

    if st.button("Generate Rule"):

        output = modelling(df, support, confidence, lift)
        sizeResult = getLength(output)
        printOutput = print_result2(output)

        st.success('Number of rules generated : {} rules'.format(sizeResult))
        st.table(printOutput)

if __name__=='__main__':
    main()
