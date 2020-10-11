from django.http import HttpResponse, JsonResponse
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from prettytable import PrettyTable
import gzip
import json
import csv
import requests
from django.views.decorators.csrf import csrf_exempt

es = Elasticsearch([{'host': '127.0.0.1', 'port': 9200,'timeout':30}])
index_name = "tweets"
index_name_beecell="transaction"
index_mobibees_beecell="mobibees"

esUrl='http://127.0.0.1:9200/'
##starting human readable code fro work
aNodes=['tweets','transaction','mobi']

#close all nodes 
def closeAllNodes():
    for i in aNodes:
        print(i)
        es.indices.delete(index=i) 
        closeIndex(i)

def createEsNode(request):
    closeAllNodes()##hit close all nodes before create any new node
    #openIndex('mobi')
    if es.indices.exists('mobibees'):
        es.indices.delete(index='mobibees')    
    
# index settings
    settings = {
        "settings": {
        "analysis": {
        "filter": {
        "trigrams_filter": {
        "type": "ngram",
        "min_gram": 3,
        "max_gram": 4
        }
    },
    "analyzer": {
        "text_processing": {
        "type": "custom",
        "tokenizer": "standard",
        "filter": [
            "lowercase",
            "trigrams_filter",
            
        ]
        }
    }
    }
}
,"mappings": {
        "properties": {

        "flag": {
        "type": "text",
        "fields": {
            "keyword": {
            "type": "keyword",
            "ignore_above": 256
            }
        }
        },
        "id": {
        "type": "text",
        "fields": {
            "keyword": {
            "type": "keyword",
            "ignore_above": 256
            }
        }
        },
        "msisdn": {
        "type": "text",
        "fields": {
            "keyword": {
            "type": "keyword",
            "ignore_above": 256
            }
        }
        },
        "url": {
        "type": "text",
        "fields": {
            "keyword": {
            "type": "keyword",
            "ignore_above": 1024
            }
        }
        },
        "action": {
        "type": "text",
        "fields": {
            "keyword": {
            "type": "keyword",
            "ignore_above": 256
            }
        }
        },
        "op_name": {
        "type": "text",
        "fields": {
            "keyword": {
            "type": "keyword",
            "ignore_above": 256
            }
        }
        },
        "date": {
        "type": "text",
        "fields": {
            "keyword": {
            "type": "keyword",
            "ignore_above": 256
            }
        }
        }, 
        "response": {
        "type": "text",
        "fields": {
            "keyword": {
            "type": "keyword",
            "ignore_above": 256
            }
        }
        }, 
        "message": {
        "type": "text",
        "fields": {
            "keyword": {
            "type": "keyword",
            "ignore_above": 256
            }
        }
        },                        

        }

    }

    }
#    create index
    s=es.indices.create(index='mobibees', ignore=400, body=settings)
    return  HttpResponse(s)    

#open index before search and write
def openIndex(indexName):
    url=esUrl+indexName+'/_open'
    print(url)
    headers = {"content-type": "application/json", "Accept-Charset": "UTF-8"}
    r = requests.post(url, data={"sample":"data"}, headers=headers)
    print(r)

#close any open index
def closeIndex(indexName):
    url=esUrl+indexName+'/_close'
    print(url)
    headers = {"content-type": "application/json", "Accept-Charset": "UTF-8"}
    r = requests.post(url, data={"sample":"data"}, headers=headers)
    print(r)

def checkNode(indexName):
    for i in (aNodes):
        if i==indexName:
            return True
    
    return False

##general API to push into node
@csrf_exempt
def pushtoIndexGeneral(request):
    indexName=request.POST.get('node_name')
    print(indexName)
    if checkNode(indexName):
            openIndex(indexName)
            if indexName=='mobibees':
                handelMobibeesNode(request,indexName)
            else:
                print('need to build node details')
            closeIndex(indexName)
    else:
        print('not supported node')

    return  HttpResponse("Check Server Logs")

@csrf_exempt
def handelMobibeesNode(request,indexName):
    #print("hello")
    #print(request)
    #print("end")
    msisdn=request.POST.get('msisdn')    
    url=request.POST.get('url')
    action=request.POST.get('action')
    op_name=request.POST.get('op_name')
    date=request.POST.get('date')
    response=request.POST.get('response')
    message=request.POST.get('message')
    uid=request.POST.get('id')
    #print(transaction_id)

    transaction = {
            
            "msisdn": msisdn,
            "url": url,
            "action": action,
            "op_name": op_name,
            "date": date,
            "response":response,
            "message":message,
            "id":uid
            }

    print(transaction)
    res = es.index(index=indexName, id=transaction['id'], body=transaction)
    if res:
        return True
    else:
        return False

#########################################
def eSearch(request):    
    if es.indices.exists(index_mobibees_beecell):
        es.indices.delete(index=index_mobibees_beecell)
    
# index settings
    settings = {
        "settings": {
        "analysis": {
        "filter": {
        "trigrams_filter": {
        "type": "ngram",
        "min_gram": 3,
        "max_gram": 4
        }
    },
    "analyzer": {
        "text_processing": {
        "type": "custom",
        "tokenizer": "standard",
        "filter": [
            "lowercase",
            "trigrams_filter"
        ]
        }
    }
    }
}
,"mappings": {
        "properties": {
        "date": {
        "type": "text",
        "fields": {
            "keyword": {
            "type": "keyword",
            "ignore_above": 256
            }
        }
        },
        "flag": {
        "type": "text",
        "fields": {
            "keyword": {
            "type": "keyword",
            "ignore_above": 256
            }
        }
        },
        "id": {
        "type": "text",
        "fields": {
            "keyword": {
            "type": "keyword",
            "ignore_above": 256
            }
        }
        },
        "target": {
        "type": "text",
        "fields": {
            "keyword": {
            "type": "keyword",
            "ignore_above": 256
            }
        }
        },
        "text": {
        "type": "text",
        "fields": {
            "keyword": {
            "type": "keyword",
            "ignore_above": 256
            }
        }
        },
        "user": {
        "type": "text",
        "fields": {
            "keyword": {
            "type": "keyword",
            "ignore_above": 256
            }
        }
        }
        }

    }

    }
#    create index
    s=es.indices.create(index='demo', ignore=400, body=settings)
    return  HttpResponse(s)

def pushtoIndex(request):
    tweet = {
            "target": "4",
            "id": "2193602063",
            "date": "Tue Jun 16 08:40:49 PDT 2009",
            "flag": "NO_QUERY",
            "user": "tinydiamondz",
            "text": "Happy 38th Birthday to my boo of alll time!!! Tupac Amaru Shakur"
            }
    res = es.index(index=index_name, id=tweet['id'], body=tweet)
    print(res)
    return  HttpResponse("Check Server Logs")


def compressFileToGzip(request):
    fp = open("E:\\softwares\\elasticsearh_binary\\twteerData\\tweetsBulk.csv","rb")
    data = fp.read()
    bindata = bytearray(data)
    with gzip.open("E:\\softwares\\elasticsearh_binary\\twteerData\\tweetsBulk.csv.gz", "wb") as f:
        f.write(bindata)
    return  HttpResponse("Check Folder path and server  Logs")

def insertBulkTweets(request):
    i = 1
    actions = []
    with gzip.open('E:\\softwares\\elasticsearh_binary\\twteerData\\tweetsBulk.csv.gz','rt') as f:
        #print(i, len(actions))
        for line in f:
            
            if i>100:
                break
            currentLine=createTweetObj(line,i)##general funstion to build json tweets
           
            #res = es.index(index=index_name, id=currentLine['id'], body=currentLine)
            #print(res)
           # print(currentLine)
            try:
                if i%10000!=0:
                    #print('got line', i)
                    #line = line.replace("\'", "\"")
                    actions.append(currentLine)##append tweets to array 
                    #print(i)

                else:
                    print(i)
                    print("batch start")
                    bulkResult=bulkInsertEsSerach(actions)
                    actions=[]##truncate array
                    #print(bulkResult)
                    print("batch end")
            except:
                None
            i=i+1
        
    #print(actions)
    return HttpResponse("Check Srever Logs")
            
def createTweetObj(dataLine,indexV):
    cLine=list(csv.reader([dataLine]))[0]
    tweet = {
        "_index":indexV,
        "_id":index_name,
        "target": "4",
        "id": cLine[1],
        "date": cLine[2],
        "flag": cLine[3],
        "user": cLine[4],
        "text": cLine[5]
        }
    
    return tweet

def bulkInsertEsSerach(actionsList):    
    return helpers.bulk(es, actionsList)




###beecell area
#1.0
def creatIndex(request):
    #if es.indices.exists(index_mobibees_beecell):
     #   es.indices.delete(index=index_mobibees_beecell)
    settings = {
        "settings": {
        "analysis": {
        "filter": {
        "trigrams_filter": {
        "type": "ngram",
        "min_gram": 3,
        "max_gram": 4
        }
    },
    "analyzer": {
        "text_processing": {
        "type": "custom",
        "tokenizer": "standard",
        "filter": [
            "lowercase",
            "trigrams_filter"
        ]
        }
    }
    }
}
,"mappings": {
        "properties": {
        "date": {
        "type": "text",
        "fields": {
            "keyword": {
            "type": "keyword",
            "ignore_above": 256
            }
        }
        },
        "flag": {
        "type": "text",
        "fields": {
            "keyword": {
            "type": "keyword",
            "ignore_above": 256
            }
        }
        },
        "id": {
        "type": "text",
        "fields": {
            "keyword": {
            "type": "keyword",
            "ignore_above": 256
            }
        }
        },
        "target": {
        "type": "text",
        "fields": {
            "keyword": {
            "type": "keyword",
            "ignore_above": 256
            }
        }
        },
        "text": {
        "type": "text",
        "fields": {
            "keyword": {
            "type": "keyword",
            "ignore_above": 256
            }
        }
        },
        "user": {
        "type": "text",
        "fields": {
            "keyword": {
            "type": "keyword",
            "ignore_above": 256
            }
        }
        }
        }

    }

    }
    try:
        s=es.indices.create(index="demo", ignore=400)
    except Exception as ex:
            print(str(ex))
    return  HttpResponse(s)

#1.1
def compressBeecellFileToGzip(request):
    fp = open("E:\\softwares\\elasticsearh_binary\\beecell\\apr.csv","rb")
    data = fp.read()
    bindata = bytearray(data)
    with gzip.open("E:\\softwares\\elasticsearh_binary\\beecell\\apr.gz", "wb") as f:
        f.write(bindata)
    return  HttpResponse("Check Folder path and server  Logs")


#1.2 first push
def pushtoBeecellIndex(request):
    transaction_id=request.GET.get('transaction_id')
    transaction_feature=request.GET.get('transaction_feature')
    transaction_operator=request.GET.get('transaction_operator')
    transaction_uid=request.GET.get('transaction_uid')
    transaction_type=request.GET.get('transaction_type')
    transaction_status=request.GET.get('transaction_status')
    transaction_msisdn=request.GET.get('transaction_msisdn')
    transaction_date=request.GET.get('transaction_date')
    

    transaction = {
            
            "transaction_id": transaction_id,
            "transaction_feature": transaction_feature,
            "transaction_operator": transaction_operator,
            "transaction_uid": transaction_uid,
            "transaction_type": transaction_type,
            "transaction_status":transaction_status,
            "transaction_msisdn":transaction_msisdn,
            "transaction_date":transaction_date
            }
    openIndex('mobibees')
    res = es.index(index='mobibees', id=transaction['transaction_id'], body=transaction)
    closeIndex('mobibees')
    print(res)
    return  HttpResponse("Check Server Logs")
#1.2
def insertBulkTransactons(request):
    i = 1
    actions = []
    with gzip.open('E:\\softwares\\elasticsearh_binary\\beecell\\apr.gz','rt') as f:
        #print(i, len(actions))
        for line in f:
            if i<100001:
                i=i+1
                continue

            
            
           



           
            currentLine=createTransObj(line,i)##general funstion to build json tweets
            print(currentLine)

            try:
                if i%10000!=0:
                    #print('got line', i)
                    #line = line.replace("\'", "\"")
                    actions.append(currentLine)##append tweets to array 
                    #print(i)

                else:
                    print(i)
                    print("batch start")
                    bulkResult=bulkInsertEsSerach(actions)
                    actions=[]##truncate array
                    #print(bulkResult)
                    print("batch end")
            except:
                None
            i=i+1
        
   # print(actions)
    return HttpResponse("Check Srever Logs")

def createTransObj(dataLine,indexV):
    cLine=list(csv.reader([dataLine]))[0]
    #68,53,2,972569185199,6,id,date
    trans = {
        "_index":index_name_beecell,
        "_id":cLine[5],
        "transaction_operator": cLine[0],
        "transaction_feature": cLine[1],
        "transaction_type": cLine[2],
        "transaction_msisdn": cLine[3],
        "transaction_status": cLine[4],
        "transaction_id": cLine[5],
        "transaction_date": cLine[6],        
        "transaction_uid":""
        }

    
    return trans



def elasticSearch(request):
    transaction_msisdn=request.GET.get('transaction_msisdn')
    response = es.search(
    index=index_name_beecell,
    body={
      "query": {
        "bool": {
          #"must": [{"match": {"transaction_msisdn":transaction_msisdn}}],
          "must_not": [{"match": {"transaction_status": 6}}],
          #"filter": [{"term": {"transaction_type": 2}}]
          "match":[{'all'}]
        }
 
      },
        } 
        
    )

    x = PrettyTable()

    x.field_names = ["Transaction Msisdn", "Date","status","type"]

   
    
    for hit in response['hits']['hits']:
        x.add_row([hit['_source']['transaction_msisdn'],hit['_source']['transaction_date'],hit['_source']['transaction_status'],hit['_source']['transaction_type']])
        #
        #print(hit['_score'], hit['_source']['transaction_msisdn'])

    print(x)
    return HttpResponse("ss")

