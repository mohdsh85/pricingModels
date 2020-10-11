from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect 
import datetime
from django.core.mail import send_mail
import json
from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import make_regression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import secrets
import re
import shutil
from django.contrib.sessions.models import Session
from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore
import joblib
import os.path
from os import path
###https://realpython.com/logistic-regression-python/

client = MongoClient()
db=client.pricingModel##should be dynamic name

#apiPreUrl='http://46.101.239.156/mlProcess'
apiPreUrl='http://127.0.0.1:8000/mlProcess/?'
serverIpAddress=apiPreUrl
#apiDescriptionUrl='http://127.0.0.1:8000/apiDescription/'
apiDescriptionUrl='http://46.101.239.156/apiDescription/'
normalCountryStatusPercentage=1
restrictedCountryStatusPercentage=0.2
growingCountryStatusPercentage=-0.20
"""
default attributres for each org saved to db
"""
def defaultAttributesML():
    return ['Requested_Amount','Emi_Amount','Age','Segment','Ex_Showroom_Price','Cost_Of_Vehicle','Loan_Term','cibil_score','No_Of_Years_At_Residence','No_Of_Years_In_City','application_creation_date','Disbursed','Gender_Desc','IRR']

def defaultAttributesMLEDA():
    return ['Requested_Amount','Emi_Amount','Age','Ex_Showroom_Price','Cost_Of_Vehicle','Loan_Term','cibil_score','No_Of_Years_At_Residence','No_Of_Years_In_City','year','A1','A2','A3','A4','A5','A6','EXTRA1','MUV','SUV','Yes','Male']

def defaultAttributesMLEDARequest():
    return ['Requested_Amount','Emi_Amount','Age','Ex_Showroom_Price','Cost_Of_Vehicle','Loan_Term','cibil_score','No_Of_Years_At_Residence','No_Of_Years_In_City','year','Segment','Gender']

def defaultAttributesMLEDAFinal():
    return ['Requested_Amount','Emi_Amount','Age','Segment','Ex_Showroom_Price','Cost_Of_Vehicle','Loan_Term','cibil_score','No_Of_Years_At_Residence','No_Of_Years_In_City','year','A1','A2','A3','A4','A5','A6','EXTRA1','MUV','SUV','No','Yes','Male','Female']

def returnHashValue(request):
    orgId=request.GET.get('orgId')
    key=(secrets.token_urlsafe(16))
    return HttpResponse(orgId+"" +key)

def authorizeOrg(orgId,token):
    if(orgId==token):
        return True
    return False

##
def checkSeesionOrg(request):
    if request.session['org_name']:
        return request.session['org_name']
    else:
        return False


##
"""
function to manage request dfemo API
function accept 
email, org name 
build db for each organization
"""
def demoRequestProcess(request):
    email=request.GET.get('email')
    org_name=request.GET.get('org_name')
    org_name=re.sub(r"\s+", "", org_name)

    if not re.match(r"[^@]+@[^@]+\.[^@]", email):
        email='Error In Email Format'
    else:
        email=email   
    request.session['org_name'] = org_name##set org value as session
    alreadyExist='Dataset Creation Process....'
    col=org_name
    orgColection='orgnizationInfo'
    l=list(db[col].find())
    if l :
        alreadyExist='Organization Already Existed, Old Dataset will be removed and new default one will be Inserted.....'
        shutil.copyfile('datasets/DataSet.csv', 'datasets/'+org_name+'.csv')
        db[col].drop()
        db[col+'_eda'].drop()
        data=parseCSVFileDirectlt('datasets/'+org_name+'.csv',org_name)
        
    else:
        shutil.copyfile('datasets/DataSet.csv', 'datasets/'+org_name+'.csv')
        data=parseCSVFileDirectlt('datasets/'+org_name+'.csv',org_name)

    totalRecords=(db[col].count())

    ###remove org info if existed and insert new one with key in db
    db[orgColection].remove( { 'email' : email,'org_name':org_name } )
    key=(secrets.token_urlsafe(16))

    d={'email':email,'org_name':org_name,'key':key}
    db[orgColection].insert_one(d)
    return  render(request, "orgCreation.html", {"org_name" : org_name,'email':email,'alreadyExist':alreadyExist,'data':data,'totalRecords':totalRecords})#HttpResponse("Hello, world. You're at the polls index.")
###end request demo API

def parseCSVFileDirectlt(filePath,org_name):
    df = pd.read_csv(filePath)
    data=df.head(50)
    db[org_name].insert_many(df.to_dict('records'))
    edAprocess(df,org_name)
    return data

""""
full eda process with hot encodong preperation for ML
"""

def edAprocess(df,org_name):
    workingDf=df
    s = workingDf.groupby('Requested_Amount')['Emi_Amount'].transform('median')#  
    workingDf['Emi_Amount'].fillna(s, inplace=True)
    ## build working df based on targeted col
    workingDf=workingDf[['Requested_Amount','Emi_Amount','Age','Segment','IRR','Ex_Showroom_Price','Cost_Of_Vehicle','Current Valuation','Loan_Term','cibil_score','No_Of_Years_At_Residence','No_Of_Years_In_City','application_creation_date','Disbursed','Gender_Desc','Average_Bank_Balance']]
    workingDf['year']=pd.DatetimeIndex(workingDf['application_creation_date']).year
    workingDf=workingDf.drop(['Average_Bank_Balance'],axis=1)
    workingDf= workingDf.dropna(axis = 0, how ='any')
    uniuqeSegments=workingDf.Segment.unique()
    workingDf = workingDf[workingDf.Requested_Amount > 10000]
    workingDf = workingDf[workingDf.Age <= 65]
    tmpDf=pd.get_dummies(workingDf.Segment)
    workingDf=workingDf.drop(['Segment','application_creation_date'],axis=1)
    workingDf = pd.concat([workingDf, tmpDf], axis=1)
    tmpDf=pd.get_dummies(workingDf.Disbursed)
    workingDf=workingDf.drop(['Disbursed'],axis=1)
    workingDf = pd.concat([workingDf, tmpDf], axis=1)
    tmpDf=pd.get_dummies(workingDf.Gender_Desc)
    workingDf=workingDf.drop(['Gender_Desc'],axis=1)
    workingDf = pd.concat([workingDf, tmpDf], axis=1)
    workingDf=workingDf.drop(['Female'],axis=1)
    workingDf=workingDf.drop(['No'],axis=1)
    db[org_name+'_eda'].insert_many(workingDf.to_dict('records'))

    return True




def checkOrgData(request):
    org_name=''

    if request.session.get('org_name')!='':
        org_name=request.session['org_name']
    count=countEDA=0
    apiUrl=''
    email=key=''
    t=''
    defaultAttributesMLEDAFinalParam=defaultAttributesMLEDARequest()
    for i in  (defaultAttributesMLEDAFinalParam):
        t=t+'&'+i+'='+i+'_value'
    if org_name:
        data=list(db[org_name].find().limit(10))
        count=db[org_name].count()
        dataEDA=list(db[org_name+'_eda'].find().limit(10))
        countEDA=db[org_name+'_eda'].count()
        apiUrl=list(db['orgnizationInfo'].find({'org_name':org_name}).limit(1))
        finalUrl=apiPreUrl+'email='+(apiUrl[0]['email'])+'&org_name='+(apiUrl[0]['org_name'])+'&key='+(apiUrl[0]['key'])
        finalUrl=finalUrl+t+'&max_loan_term_in_months=pass_it_to_suggest_values_fou_u'
        responseRequest={"disbursed":"yes or no","IRR":"rate value","Suggestions":"what to do next step.."}
        email=apiUrl[0]['email']
        key=apiUrl[0]['key']
    else:
        org_name='Please Request Demo Again to check your Data or keep using your Result From ML API as Below file URL here ....'
        data=dataEDA={}
        finalUrl='Request Demo First....'
        responseRequest={"disbursed":"yes or no","IRR":"rate value","Suggestions":"what to do next step.."}



    #print(t)

    return  render(request, "checkData.html", {'apiDescriptionUrl':apiDescriptionUrl,"responseRequest":responseRequest,"apiPreUrl":apiPreUrl,"apiUrl":finalUrl,"countEDA":countEDA,"dataEDA":dataEDA,"count":count,"org_name" : org_name,'data':data,'defaultAttributesML':defaultAttributesML(),'defaultAttributesMLEDA':defaultAttributesMLEDA(),'email':email,'key':key})#HttpResponse("Hello, world. You're at the polls index.")

def hello(request):
    
    today=datetime.datetime.now().date()
    daysOfWeek = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    dump = json.dumps(daysOfWeek)
    return JsonResponse(dump, content_type='application/json')#render(request, "hello.html", {"today" : today,'daysOfWeek':daysOfWeek})#HttpResponse("Hello, world. You're at the polls index.")

def checkStatus(request):
    l=list(db.pallease.find())
    today=datetime.datetime.now().date()
    daysOfWeek = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sunday']
    return  render(request, "hello.html", {"today" : today,'daysOfWeek':daysOfWeek,'md':l})#HttpResponse("Hello, world. You're at the polls index.")

def testRedirect(request):
    print(request+" test")
    today=datetime.datetime.now().date()
    daysOfWeek = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sunday']
    return  render(request, "hello.html", {"today" : today,'daysOfWeek':daysOfWeek})#HttpResponse("Hello, world. You're at the polls index.")

def send_mail(request):
    res = send_mail("hello paul", "comment tu vas?", "paul@polo.com", "mohdsh85@gmail.com")
    return HttpResponse('%s'%res)

###add trans to be analysied with ML 
def addMongoTrans(request):
    orgId=request.GET.get('orgId')
    token=request.GET.get('token')
    validateRequest=authorizeOrg(orgId,token)
    if(validateRequest==False or orgId is None):
        return  HttpResponse("Not Valid request")
    name=(request.GET.get('name'))
    requested_amount=(request.GET.get('requested_amount'))
    d={'name':name,'requested_amount':requested_amount}
    db.pallease.insert_one(d)
    return  HttpResponse("name:"+name+' Requested Amount '+requested_amount)

def checkSegment(segmentValue):
    print(segmentValue)
    segmant=['A1','A2','A3','A4','A5','A6','EXTRA1','MUV','SUV']
    for i in (segmant):
        if i==segmentValue:
            return True
    
    return False


## cal ML demo 
def mlProcess(request):
    filename_step_1 = 'finalized_model_step_1.sav'
    filename_step_2 = 'finalized_model_step_2.sav'
    org_name=request.GET.get('org_name')
    dataEDA=pd.DataFrame(list(db[org_name+'_eda'].find()))
    requestedSegment=str(request.GET.get('Segment'))
    validateSegmant=checkSegment(requestedSegment)
    country_status=int(request.GET.get('country_status'))
    approvedIRR=str(request.GET.get('approvedIRR'))
    saveToDb=int(request.GET.get('saveToDb'))
    xRandom = dataEDA[['Requested_Amount','Emi_Amount','Age','Loan_Term','Male']]
    if validateSegmant:
        xRandom = dataEDA[['Requested_Amount','Emi_Amount','Age','Loan_Term','Male',requestedSegment]]

   # print(xRandom)
    yRandom = dataEDA['Yes']


    Requested_Amount=float(request.GET.get('Requested_Amount'))
    Emi_Amount=(request.GET.get('Emi_Amount'))
    Age=(request.GET.get('Age'))
    Loan_Term=int(request.GET.get('Loan_Term'))
    Gender=(request.GET.get('Gender'))
    isMale=0
    if Gender=='Male':
        isMale=1

    max_loan_term_in_months=int(request.GET.get('max_loan_term_in_months'))
    x_=createDfFromList(Requested_Amount,Emi_Amount,Age,Loan_Term,isMale,validateSegmant,requestedSegment)##return df 
    if path.exists(filename_step_1):
        loaded_model = joblib.load(filename_step_1)##check if file existed
       # print("we are here")
        yes_test =  loaded_model.predict(x_)[0]##random foreset predection
        #print(yes_test)
    else:##load and save model
        model_random=RandomForestClassifier()
        model_random.fit(xRandom,yRandom)
        # save the model to disk    
        joblib.dump(model_random, filename_step_1)##save ml model to file
        yes_test = model_random.predict(x_)[0]##random foreset predection
    #print("Yes or No Disbursed Test Results "+str(yes_test))
    if yes_test==1:
        ##start IRR value regression
        irrML=dataEDA['IRR']
        x_IRR=createDfFromList(Requested_Amount,Emi_Amount,Age,Loan_Term,isMale,validateSegmant,requestedSegment)

        if path.exists(filename_step_2):##model existed and saved
            loaded_model_2 = joblib.load(filename_step_2)##check if file existed
            irr_regression_value=loaded_model_2.predict(x_IRR)[0] 
        else:
            model_random_regression=RandomForestRegressor()
            model_random_regression.fit(xRandom,irrML)
            joblib.dump(model_random_regression, filename_step_2)##save regression model to file
            irr_regression_value=model_random_regression.predict(x_IRR)[0]
        (irr_regression_value_str)=str(round(irr_regression_value,4))
        ## end IRR value regression
        irr_regression_value_str=irr_regression_value_str
        
        if country_status==1:#normal
            irr_regression_value_country_status=float(irr_regression_value_str)
        if country_status==2:#restricted
            irr_regression_value_country_status=float(irr_regression_value_str)+restrictedCountryStatusPercentage*(float(irr_regression_value_str))
        if country_status==3:#growing
            irr_regression_value_country_status=float(irr_regression_value_str)+growingCountryStatusPercentage*(float(irr_regression_value_str))                    
        

        array={"Disbursed":"Yes :) ","IRR":"Recommended IRR value is "+irr_regression_value_str,"Suggestions":"Check your Paper Work.....","IRR based on country Status":irr_regression_value_country_status}
    else:
        if max_loan_term_in_months>0:
            if int(Loan_Term+12)<=(max_loan_term_in_months):
                newTermIs=(Loan_Term+12)
                Emi_Amount=(Requested_Amount/newTermIs)
                array={"Disbursed":"No :( ","IRR":"0","Suggestions":"Make Loan Term "+str(newTermIs)+" and EMI Amount "+str(Emi_Amount)}
            else:
                array={"Disbursed":"No :( ","IRR":"0","Suggestions":"Stuck nothing to do or Try to lower the requested amount ..."}
        else:
            array={"Disbursed":"No :( ","IRR":"0","Suggestions":"Try To Increase Loan Terms and Reduce EMI or change Max loan terms in month make it more than "+str(Loan_Term)+"..."}
##just add all col.
#return ['Requested_Amount','Emi_Amount','Age','Ex_Showroom_Price','Cost_Of_Vehicle','Loan_Term','cibil_score','No_Of_Years_At_Residence','No_Of_Years_In_City','year','A1','A2','A3','A4','A5','A6','EXTRA1','MUV','SUV','Yes','Male']
    if saveToDb==1:
        if approvedIRR:
            irr=approvedIRR
        else:
            irr=irr_regression_value_str
        d={'IRR':irr,'Requested_Amount':Requested_Amount,'Emi_Amount':Emi_Amount,'Age':Age,'Loan_Term':Loan_Term,'Male':Gender,requestedSegment:1}
        db[org_name+'_eda'].insert_one(d)
        print(d)
        
    return  JsonResponse(array)

##convert list to df processs 
def createDfFromList(Requested_Amount,Emi_Amount,Age,Loan_Term,isMale,validateSegmant,requestedSegment):
    x_ = pd.DataFrame(index=None,columns=None)
    x_['Requested_Amount'] = [Requested_Amount]
    x_['Emi_Amount'] = [Emi_Amount]
    x_['Age'] = [Age]
    x_['Loan_Term'] = [Loan_Term]
    x_['Male']=[isMale]
    if validateSegmant and requestedSegment:
        x_[requestedSegment]=[1]
    x_.head()
    return x_

def mlDemo(request):
    x = np.arange(10).reshape(-1, 1)
    y = np.array([0, 0, 0, 0, 1, 1, 1, 1, 1, 1])
    model = LogisticRegression(solver='liblinear', random_state=0).fit(x, y)
    modelClasses=(model.classes_)
    modelIntercept=( model.intercept_)
    modelCoef=(model.coef_)
    cm = confusion_matrix(y, model.predict(x))

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(cm)
    ax.grid(False)
    ax.xaxis.set(ticks=(0, 1), ticklabels=('Predicted 0s', 'Predicted 1s'))
    ax.yaxis.set(ticks=(0, 1), ticklabels=('Actual 0s', 'Actual 1s'))
    ax.set_ylim(1.5, -0.5)
    for i in range(2):
        for j in range(2):
            ax.text(j, i, cm[i, j], ha='center', va='center', color='red')
    plt.show()
    plt.close()
    return  HttpResponse("modelClasses:"+str(modelClasses)+" modelIntercept:"+str(modelIntercept)+" modelCoef:"+str(modelCoef))

## parse CSV file and insert the transactions into mongo
def parseCSV(request):
    df = pd.read_csv('datasets/DataSet.csv')
    data=df.head(2000)
    #db.pallease.insert_many(df.to_dict('records'))
    return  render(request, "parseCSV.html", {"data" : data,'static':'static'})

## sys landing page
def landing(request):
    org_name=''
    if request.session.get('org_name')!='':
        org_name=request.session['org_name']
    #print( org_name)
    return  render(request, "landing.html",{'org_name':org_name})

def services(request):
    today=datetime.datetime.now().date()
    return  render(request, "services.html",{'year':today.year})

def killRunningSession(request):
    request.session['org_name'] = ''    
    return  render(request, "landing.html",{'org_name':''})

def checkDataDescription(request):
    return  render(request, "checkDataDescription.html")


def simulationProcess(request):
    return render(request, "simulationProcess.html",{'ip_address':serverIpAddress})

def presentation(request):
    return render(request, "presentation.html",{'ip_address':serverIpAddress})


def apiDescription(request):
    return render(request, "apiDescription.html")