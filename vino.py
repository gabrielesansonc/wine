# -*- coding: utf-8 -*-
"""
Spyder Editor
this is the wine calculator file
"""
import pandas as pd
import streamlit as st
from PIL import Image
import statsmodels.api as sm
import altair as alt
import base64
import numpy

image = Image.open ('Screen Shot 2021-07-13 at 9.56.48 PM.png')

st.image (image, use_column_width=True)

st.title('The Wine Calculator App')
st.subheader('This app will predict how much you will like an unknown wine!')

st.write("#")
st.write("#")


st.image ('Screen Shot 2021-07-27 at 9.27.37 PM.png', use_column_width=True)
st.image ('Screen Shot 2021-07-27 at 3.29.19 PM.png', use_column_width=True)


sample = pd.read_excel('WineSampleFile.csv')
samplecsv = sample.to_csv(index=False)

sample.head()

b64 = base64.b64encode(samplecsv.encode()).decode()
href = f'<a href="data:file/csv;base64,{b64}" download="samplefile.csv">Download Sample file </a>'

st.write(href, unsafe_allow_html=True)   

st.write("#")
st.write("#")

try:
    yourFile= st.file_uploader('Upload excel or csv file here')
    
    yourData=0
    
    if yourFile.name.endswith('.csv'):
        yourData = pd.read_csv(yourFile)
    else:
        yourData = pd.read_excel(yourFile)
    

    st.write("#")
    
    
    st.header('Fill in the following variables of your prospective wine')
    
    #Load file
    
    
    
    
    #Assign regression variables
    independentvar = yourData[['Europe', 'VivinoRating', 'ABV','Bold','Tannic','Sweet','Acidic']]
    explanatoryvar = yourData['MyRating']
    
    
    Price = st.number_input('What is the price of this wine?',float(yourData['Bold'].mean()))
    
    st.write("""
             ***
             """)
    
    #create sliders for ABV, tannic, sweetnes and acidity
    ABV = st.slider ('Alcohol percentage:',0.0,100.0,float(yourData['ABV'].mean()),0.1)
    
    st.write("""
             ***
             """)
         
    Rating = st.slider ('Rating according to vivino:',0.0,5.0,float(yourData['VivinoRating'].mean()),0.1)
    
    st.write("""
             ***
             """)
           
    Bold = st.slider ('Boldness level (use Vivino):',1.0,10.0,float(yourData['Bold'].mean()),0.5) 
    Tannic = st.slider ('Tannic level (use Vivino):',1.0,10.0,float(yourData['Tannic'].mean()),0.5)
    Sweet = st.slider ('Sweetness level (use Vivino):',1.0,10.0,float(yourData['Sweet'].mean()),0.5)  
    Acidic = st.slider ('Acidity level (use Vivino):',1.0,10.0,float(yourData['Acidic'].mean()),0.5) 
    
    
    st.write("""
             ***
             """)
             
    #create variable for label in st.radio
    region = ["Europe","Other"]
    
    #make a radio (alows selection between europe or other)
    European = st.radio('Region:',region) 
    EuropeBinary = 0
    
    if European == "Europe":
        EuropeBinary = 1
            
    
    
    
    # Creates Multiple linear regression
    model = sm.OLS(explanatoryvar, independentvar).fit()
    
    # Stores independent variables in a string
    prospectVar = [EuropeBinary, Rating, ABV, Bold, Tannic, Sweet, Acidic]
    
    
    st.write("""
             ***
             """)
             
    st.write("#")
    
    st.header('Your personal rating for this wine:')
    
    predictions = float(model.predict(prospectVar)) # make the predictions by the model
    st.header (round(predictions,1))
    
    st.write("#")
    
    st.write("""
             ***
             """)
    
    
    #create Wine and Raking arrays and covert them to list in order to anex new candidate
    
    colu1 = list(yourData['Wine'])
    colu1.append ('Prospective Candidate')
    
    colu16 = list(yourData['VivinoRating'])
    colu16.append(Rating)
    
    colu17 = list(yourData['ABV'])
    colu17.append(ABV)
    
    colu19 = list(yourData['Tannic'])
    colu19.append(Tannic)
    
    colu20 = list(yourData['Sweet'])
    colu20.append(Sweet)
    
    colu21 = list(yourData['Acidic'])
    colu21.append(Acidic)
    
    colu22 = list(explanatoryvar)
    colu22.append (round(predictions,1))
    
    colu23 = list(yourData['Bold'])
    colu23.append(Bold)
    
    colu24 = list(yourData['Price'])
    colu24.append(Price)
    
    
    #Create both colums with anexed wine into a dataframe
    
    dataForCharts = pd.DataFrame({'Wine' : colu1, 'Previous Rating' : colu22, 'Vivino Rating': colu16, 'Alcohol' : colu17, 'Tannicity' : colu19, 'Sweetness': colu20, 'Acidity': colu21, 'Boldness':colu23, 'Price' : colu24}) 
    print(dataForCharts)
    
    #Create and plot Bar Chart
    
    
    
    st.subheader("This is how the prospect compares to your other wines:")
    
    st.write("#")
    
    ChartRanking = alt.Chart(dataForCharts).mark_bar().encode(
        x=alt.X('Wine', sort='-y'),
        y=alt.Y('Previous Rating',scale=alt.Scale(domain=(min(colu22)-0.5, 10))),
         # The highlight will be set on the result of a conditional statement
        color=alt.condition(
            alt.datum.Wine == 'Prospective Candidate',  # If the year is 1810 this test returns True,
            alt.value('red'),     # which sets the bar orange.
            alt.value('rebeccapurple')   # And if it's not true it sets the bar steelblue.
            ),
            tooltip=['Wine', 'Previous Rating']
        ).interactive()
    
    st.write(ChartRanking)
    
    st.write("""
             ***
             """)
             
    st.subheader('This is how the prospect compares with the other variables:')
    
    st.write("#")
    
    st.write("Vivino Rating vs Your Ratings")
    
    ChartRating= alt.Chart(dataForCharts).mark_circle(size=100).encode(
        x='Vivino Rating',
        y='Previous Rating',
        color=alt.condition(
        alt.datum.Wine == 'Prospective Candidate', 
        alt.value('red'),     
        alt.value('darkturquoise')  
            ),
        tooltip=['Wine', 'Previous Rating', 'Vivino Rating']
    ).interactive()
    
    st.write(ChartRating)
    
    st.write("ABV vs Your Ratings")
    
    ChartABV= alt.Chart(dataForCharts).mark_circle(size=100).encode(
        x='Alcohol',
        y='Previous Rating',
        color=alt.condition(
        alt.datum.Wine == 'Prospective Candidate', 
        alt.value('red'),     
        alt.value('steelblue')  
            ),
        tooltip=['Wine', 'Previous Rating', 'Alcohol']
    ).interactive()
    
    st.write(ChartABV)
    
    
    st.write("Bold Level vs Your Ratings")
    
    ChartBold= alt.Chart(dataForCharts).mark_circle(size=100).encode(
        x='Boldness',
        y='Previous Rating',
        color=alt.condition(
        alt.datum.Wine == 'Prospective Candidate', 
        alt.value('red'),     
        alt.value('darkcyan')  
            ),
        tooltip=['Wine', 'Previous Rating', 'Boldness']
    ).interactive()
    
    st.write(ChartBold)
    
    
    
    st.write("Tannic Level vs Your Ratings")
    
    ChartTannic= alt.Chart(dataForCharts).mark_circle(size=100).encode(
        x='Tannicity',
        y='Previous Rating',
        color=alt.condition(
        alt.datum.Wine == 'Prospective Candidate', 
        alt.value('red'),     
        alt.value('blueviolet')  
            ),
        tooltip=['Wine', 'Previous Rating', 'Tannicity']
    ).interactive()
    
    st.write(ChartTannic)
    
    st.write("Sweetness Level vs Your Ratings")
    
    ChartSweet= alt.Chart(dataForCharts).mark_circle(size=100).encode(
        x='Sweetness',
        y='Previous Rating',
        color=alt.condition(
        alt.datum.Wine == 'Prospective Candidate', 
        alt.value('red'),     
        alt.value('cadetblue')  
            ),
        tooltip=['Wine', 'Previous Rating', 'Sweetness']
    ).interactive()
    
    st.write(ChartSweet)
    
    
    st.write("Acidity Level vs Your Ratings")
    
    ChartAcid= alt.Chart(dataForCharts).mark_circle(size=100).encode(
        x='Acidity',
        y='Previous Rating',
        color=alt.condition(
        alt.datum.Wine == 'Prospective Candidate', 
        alt.value('red'),     
        alt.value('navy')  
            ),
        tooltip=['Wine', 'Previous Rating', 'Acidity']
    ).interactive()
    
    st.write(ChartAcid)
    
    st.subheader('This is how the prospect compares in price:')
    
    st.write("#")
    
    st.write("Price vs Your Ratings")
    
    ChartPrice= alt.Chart(dataForCharts).mark_circle(size=100).encode(
        x='Price',
        y='Previous Rating',
        color=alt.condition(
        alt.datum.Wine == 'Prospective Candidate', 
        alt.value('red'),     
        alt.value('darkolivegreen')  
            ),
        tooltip=['Wine', 'Previous Rating', 'Price']
    ).interactive()
    
    st.write(ChartPrice)
    
    
    st.write("""
             ***
             """)
    
             
    st.subheader('Summary of the multiple linear regression:')
    
    st.write("#")
             
    st.write(model.summary())
    
    st.write("#")
    st.write("#")
    st.write("#")
    st.write("#")
    
    link = '[Check out the Beer Calculator](https://beer-claculator.herokuapp.com)'
    st.markdown(link, unsafe_allow_html=True)
    
    st.write("#")
    
    st.image ('Screen Shot 2021-07-21 at 10.28.01 AM.png', use_column_width=True)
         
except:
    st.write('No Excel or CSV file uploaded yet')
