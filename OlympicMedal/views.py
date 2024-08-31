from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib import messages
import pandas as pd
from .models import Data
from .tests import *
# Create your views here.

def medal(request, dataObj):
    medalListb = ['Gold','Silver','Bronze']
    valueList = []
    for m in medalListb:
        obj = Data.objects.filter(country = dataObj.country,medal = m)
        if dataObj.isMale and dataObj.isFemale:
            #apply no filter
            pass
        else:
            obj = obj.filter(isMale = dataObj.isMale,isFemale = dataObj.isFemale)
        
        if dataObj.season != 'Both':
            obj = obj.filter(season = dataObj.season)
        
        if dataObj.year != 0:
            obj = obj.filter(year = dataObj.year)

        if dataObj.sports != "All sports":
            obj = obj.filter(sports = dataObj.sports)
        print(obj.count())
        valueList.append(obj.count())
    return render(request,'Medal.html',context={'country':dataObj.country ,'Gmedal':valueList[0],'Smedal':valueList[1],'Bmedal':valueList[2]})

def FormPage(request):
    cData = countryReader()
    sData = sportsReader()
    context = {'countrydata':cData,'sportdata':sData}
    dataobj = None
    if request.method == "POST":
        data = request.POST
        year:int
        yearStr = data.get("Year")
        gender = data.get("Gender")
     #assume both to be false
        isFemale = False
        isMale = False
        if gender == "Male":
            isMale = True
        elif gender == "Female":
            isFemale = True
        else:
            isMale = True
            isFemale = True
        dataobj = Data.objects.create(
            country = data.get("Country"),
            isFemale = isFemale,
            isMale = isMale,
            year = 0,
            sports = data.get("Sport"),
            season = data.get("Season")
        )
              
        if len(yearStr) != 0:
            try:
              year = int(yearStr)
              if year > 2016 or year  < 1960:
                  messages.add_message(request,messages.INFO,"Please enter between 1960 and 2016")
                  return render(request,"Olympic.html",context=context)     


              #delete all messages
              if 'messages' in request.session:
                  del request.session['messages']
              dataobj.year = year
            except ValueError as ve:
                messages.add_message(request,messages.INFO,"Invalid year entered")
                print("Invalid year")
        
        return medal(request,dataobj)
    return render(request,"Olympic.html",context=context)



def countryReader():
    d = pd.read_csv("OlympicMedal/athlete_events.csv")
    dataSet = d[d['Year'] > 1960] 
    return sorted(dataSet['Team'].unique())


def sportsReader():
    d = pd.read_csv("OlympicMedal/athlete_events.csv")
    dataSet = d[d['Year'] > 1960]
    return sorted(dataSet['Sport'].unique())

def ModelMaker():
    d = pd.read_csv("OlympicMedal/athlete_events.csv")
    dataSet = d[d['Year'] > 1960]
    dataObj = []
    for index,row in dataSet.iterrows():
        isMale = False
        isFemale = False
        if row['Sex'] == 'M':
            isMale = True
        else:
            isFemale = True
        dataObj.append(
            Data(
                isMale = isMale,
                isFemale = isFemale,
                country = row['Team'],
                sports = row['Sport'],
                year = row['Year'],
                medal = row['Medal'],
                season = row['Season']            
            )
        )

    Data.objects.bulk_create(dataObj)

    