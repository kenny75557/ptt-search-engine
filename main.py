from flask import Flask, jsonify,render_template
from flask import Flask, request, send_from_directory, send_file, jsonify, Response
from elasticsearch import Elasticsearch, RequestsHttpConnection
import os
import json
from flask_cors import CORS
import requests.packages.urllib3
es = Elasticsearch(os.environ['ES'],connection_class=RequestsHttpConnection, use_ssl=True,verify_certs=False,max_retries=5,retry_on_timeout=True,send_get_body_as='POST' )


requests.packages.urllib3.disable_warnings()
# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)

app.config.from_object(__name__)
CORS(app)
static_dir = './dist'
# enable CORS
@app.route('/')
def index():  # pylint: disable=unused-variable
    if static_dir is not None:
        return send_file(os.path.join(static_dir, 'index.html'))

@app.route('/<path:path>')
def static_proxy(path: str):
    if static_dir is not None:
        return send_from_directory(static_dir, path)
    else:
        return send_file(os.path.join(static_dir, 'index.html'))
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return send_file(os.path.join(static_dir, 'index.html'))

def get_list(query):
    q_list=[]
    token_li = query.split(' ')
    for token in token_li:
        dic_in = {"content":token}
        dic_out = {"match_phrase":dic_in}
        q_list.append(dic_out)

    return q_list

#id搜尋 query: ?user_id=String&start=timeStamp&end=timsSamp
#http://140.120.182.87:6003/api/GetByUserId?user_id=stinger5009
@app.route("/api/GetByUserId")
def GetByUserId():
    query_id =request.args.get("user_id")
    query_startTimestamp =request.args.get("start")
    query_endTimestamp =request.args.get("end")

    if request.args.get("size"):
      query_size = request.args.get("size")
    else:
        query_size = 30
    if request.args.get("from"):
      query_page = request.args.get("from")
    else:
        query_page = 0
    # query_size =request.args.get("size")
    # query_page =request.args.get("from")
    if    query_startTimestamp =='none': #無時間範圍
        dsl = {
           "size": query_size, 
           "from": query_page,
           "query": {
                'match': {'user_id': query_id }
            },
            "sort": [
                      {"date": {"order": "desc"}}
                    ]
          }

    else:
        dsl = {
           "size": query_size, 
           "from": query_page,
           "query":
              { 
            "bool": { 
              "must": [ 
                        { "match": {"user_id": query_id}},
                        { "range": { "date": { "gt": query_startTimestamp,"lt":query_endTimestamp}}
                         }
                      ]
             
                 }
              },
               "sort": [
                       {"date": {"order": "desc"} }
                    ]
          }  #有下時間範圍
   
    res=es.search(index="article2", body= dsl)
    return json.dumps(res['hits'], indent=2, ensure_ascii=False)
    

#關鍵字搜尋
#http://140.120.182.87:6003/api/GetByContent?content=鬼滅?start=none?end=none?size=25?from=1
@app.route("/api/GetByContent")
def GetByContent():

    query_content =request.args.get("content")
    query_startTimestamp =request.args.get("start")
    query_endTimestamp =request.args.get("end")
    if request.args.get("size"):
      query_size = request.args.get("size")
    else:
        query_size = 30
    if request.args.get("from"):
      query_page = request.args.get("from")
    else:
        query_page = 0
    print(query_content)
    qmatch_list = get_list(query_content)
    print(qmatch_list)



    if    query_startTimestamp =='none': 
        dsl = {
           "size": query_size,
           "from": query_page,
           "query": {
               "bool": {
                 "should": [
                  {"bool": {
                    "must": qmatch_list
                        }
                    },
                  {"bool": {
                      "must":qmatch_list,
                      "must_not": {   "exists": {"field": "comment_tag"}}
                    }
                  }
                 ],
                 "minimum_should_match": 1
                 }
  }
            }

    else:
         dsl = {
            "size": query_size,
            "from": query_page,
            "query": {
              "bool": {
                  "should": [
                      {"bool": {
                                "must": qmatch_list
                              }
                       },
                    {"bool": {
                              "must":qmatch_list
                              ,
                              "must_not": {
                                "exists": {"field": "comment_tag"}
                              }
                            }
                            }
                     ],
      "must": [
        {"range": { "date": { "gt": query_startTimestamp,"lt": query_endTimestamp}}}
      ], 
      "minimum_should_match": 1
    }
  }

          
  
          }  #有下時間範圍
    res=es.search(index="article2", body= dsl)
    return json.dumps(res['hits'], indent=2, ensure_ascii=False)
#BoardSearch API
@app.route("/api/GetByBoard")
def GetByBoard():
  query_board =request.args.get("board")
  query_startTimestamp =request.args.get("start")
  query_endTimestamp =request.args.get("end")
  
  if request.args.get("size"):
    query_size = request.args.get("size")
  else:
      query_size = 30
  if request.args.get("from"):
    query_page = request.args.get("from")
  else:
      query_page = 0
  print(query_board)
  print(query_startTimestamp)
  if query_startTimestamp == None: 
    print("notime")
    dsl = {
           "size": query_size, 
           "from": query_page,
           "query": {
                "match": {"board": query_board }
            },
            "sort": [
                      {"date": {"order": "desc"}}
                    ]
          }


  else:
    print("haveTime")
    dsl = {
           "size": query_size, 
           "from": query_page,
           "query":
              { 
            "bool": { 
              "must": [ 
                        { "match": {"board": query_board}},
                        { "range": { "date": { "gt": query_startTimestamp,"lt":query_endTimestamp}}
                         }
                      ],
              
                 }
              },
              "sort": [
                       {"date": {"order": "desc"} }
                    ]
          }  #有下時間範圍
  res=es.search(index="article2", body= dsl)
  return json.dumps(res['hits'], indent=2, ensure_ascii=False)




if __name__ == '__main__':
    app.run(host ='0.0.0.0',port ='8000',debug ='True')
    #140.120.182.87:6003
    #8001