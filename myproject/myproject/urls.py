"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views as hello_views
from myproject import views as eSearchViews

admin.autodiscover()
urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello_views.hello,name='hello'),
    path('landing', hello_views.landing,name='landing'),
    path('', hello_views.landing,name='landing'),
    path('checkStatus/',hello_views.checkStatus,name='checkStatus'),
    path('send_mail/',hello_views.send_mail,name='send_mail'),
    path('addMongoTrans/',hello_views.addMongoTrans,name='addMongoTrans'),
    path('mlDemo/',hello_views.mlDemo,name='mlDemo'),
    path('simulationProcess/',hello_views.simulationProcess,name='simulationProcess'),
    path('parseCSV/',hello_views.parseCSV,name='parseCSV'),
    path('services/',hello_views.services,name='services'),
    path('returnHashValue/',hello_views.returnHashValue,name='returnHashValue'),
    path('demoRequestProcess/',hello_views.demoRequestProcess,name='demoRequestProcess'),
    path('checkSeesionOrg/',hello_views.checkSeesionOrg,name='checkSeesionOrg'),
    path('checkOrgData/',hello_views.checkOrgData,name='checkOrgData'),
    path('killRunningSession/',hello_views.killRunningSession,name='killRunningSession'),
    path('checkDataDescription/',hello_views.checkDataDescription,name='checkDataDescription'),
    path('mlProcess/',hello_views.mlProcess,name='mlProcess'),
    path('presentation/',hello_views.presentation,name='presentation'),
    path('apiDescription/',hello_views.apiDescription,name='apiDescription'),
    path('eSearch/',eSearchViews.eSearch,name='eSearch'),
    #path('pushtoIndex/',eSearchViews.pushtoIndex,name='pushtoIndex'),
    #path('compressFileToGzip/',eSearchViews.compressFileToGzip,name='compressFileToGzip'),
    #path('insertBulkTweets/',eSearchViews.insertBulkTweets,name='insertBulkTweets'),

    ####beecell test 
    path('creatIndex/',eSearchViews.creatIndex,name='creatIndex'),
    path('createEsNode/',eSearchViews.createEsNode,name='createEsNode'),
    path('pushtoIndexGeneral/',eSearchViews.pushtoIndexGeneral,name='pushtoIndexGeneral'),        
    path('pushtoBeecellIndex/',eSearchViews.pushtoBeecellIndex,name='pushtoBeecellIndex'),
    path('compressBeecellFileToGzip/',eSearchViews.compressBeecellFileToGzip,name='compressBeecellFileToGzip'),
    path('insertBulkTransactons/',eSearchViews.insertBulkTransactons,name='insertBulkTransactons'),
    path('elasticSearch/',eSearchViews.elasticSearch,name='elasticSearch')


    
]
