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
#from django.urls import path
from django.conf.urls import url
from staging import views as eSearchViews

admin.autodiscover()
urlpatterns = [

    url(r'^admin/', admin.site.urls),
    ####beecell test 
    url('creatIndex/',eSearchViews.creatIndex,name='creatIndex'),
    url('createEsNode/',eSearchViews.createEsNode,name='createEsNode'),
    url('pushtoIndexGeneral/',eSearchViews.pushtoIndexGeneral,name='pushtoIndexGeneral'),        
    url('pushtoBeecellIndex/',eSearchViews.pushtoBeecellIndex,name='pushtoBeecellIndex'),
    url('compressBeecellFileToGzip/',eSearchViews.compressBeecellFileToGzip,name='compressBeecellFileToGzip'),
    url('insertBulkTransactons/',eSearchViews.insertBulkTransactons,name='insertBulkTransactons'),
    url('elasticSearch/',eSearchViews.elasticSearch,name='elasticSearch')


    
]
