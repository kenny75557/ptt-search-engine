

# Ptt_SearchEngineWeb

## Introduction

Build a search engine include all articles and commands crawl from Ptt(web forum), Searching content by keyword or by user’s id observe what articles they replied or post. This Repo only conclude Wep UI part.
ptt: https://en.wikipedia.org/wiki/PTT_Bulletin_Board_System
[Demo-Link](https://ptt-search.nlpnchu.org/)
## Build a Web application using Flask and Vuejs
Use the vue front-end framework to develop a single-page application (SPA), and then hand over the built front-end interface to Flask as the server to process Request and the API for search commands under Elasticsearch. This note will be divided into two parts: Vue.js and Flask.

see VueJS README in ```vueptt``` directory.
### Architecture diagram
![](https://i.imgur.com/JFfRHzW.png)


For basic concepts of web application and routing, please refer to:
[SPA & Router](https://blog.huli.tw/2019/09/18/spa-common-problem-about-router/)






## Flask
### Installing

Install Flask and the Flask-CORS extension

`(env)$ pip install Flask Flask-Cors `

Under background processing (save Session, you can use[Tmux](https://larrylu.blog/tmux-33a24e595fbc))，Execute main.py to start the service on the server.
```
//Flask directory
tmux
<Ctrl+b> + s//select Session 
python app.py

```

### Query API
Handle how to process the search conditions sent by the front end into Query and send it to ElasticSearch.

Introduce the Elasticsearch suite in main.py, and send a request to the database to return the data.

The environment parameters are used here to have more flexibility in changing the database domain and password. It is brought in by the Docker command when deploying, or you can directly enter the connection format of your ES service (as noted below).

Link to ES(database) settings:

```python
from elasticsearch import Elasticsearch, RequestsHttpConnection
es = Elasticsearch(os.environ['ES'],connection_class=RequestsHttpConnection, use_ssl=True,verify_certs=False,send_get_body_as='POST' )
//ES is the variabe of ['http://elastic:<key>@<Domain>']
```


#### Search processing example (retrieved by id)
The API format is as follows. After the "?" symbol is the parameter used to set the DSL syntax search. For how to query in Elastisearch, please refer to:[Link1](https://godleon.github.io/blog/Elasticsearch/Elasticsearch-advanced-search/) ，[Link2](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html)

```javascript
<yourDomain>/api/GetByUserId?user_id=String&start=timeStamp&end=timeStamp?size=25?from=1
 //
<yourDomain>/api/GetByContent?Content=String&start=timeStamp&end=timeStamp?size=25?from=1
```

The following variables are used:
1. user_id:author id
1. content:In-text search (keywords)
1. start:Date start point (in Timestamp format)
1. end:Date end point (in Timestamp format)
1. size:Show several data
1. from:From the first few data

After the data is processed and packaged into a DSL, the search function of ES will be used to send it to the DB, and finally it will be sent back to the front end in JSON format:
 ```python
dsl = {
  "size": size,
  "from": page,
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "content": content
          }
        },
        {
          "match": {
            "article_title": content
          }
        },
        {
          "range": {
            "date": {
              "gt": start,
              "lt": end
            }
          }
        }
      ],
      "must_not": [],
      "should": []
    }
  },
  "sort": [
    {
      "date": {
        "order": "desc"
      }
    }
  ]
}
    res=es.search(index="article2", body= dsl)
    return json.dumps(res['hits'], indent=2, ensure_ascii=False)
```
See the code comments for the rest of the details

### Wrap the whole set of front and back into Docker image
#### Dockerfile
Write a Dockerfile to package the built front-end project and Flask into an image.

[official documentation](https://docs.docker.com/engine/reference/builder/)


**Dockerfile**
```dockerfile
FROM python:3.6.9 #Base Image Environment version

WORKDIR /PTTapp #The working directory to be created

ADD . /PTTapp  #Copy files and folders to the specified location

RUN pip install -r requirements.txt
# Each RUN command adds a new layer on top of the existing image and is the command that is executed during the build process of the image.
CMD python main.py # instructions executed at runtime in container
```
**requirements.txt**:The version of the kit used.

After completion, use the command Build to generate a docker image, under the Flask folder, Terminal input
```
docker image build -t <Account>/<Image Name>:<Version Tag> .
//docker Account can be omitted unless you need to push to DockerHub
```
![](https://i.imgur.com/Wo2qYbU.png)

When finished, you can type `docker images` in Terminal or see the file you just created on the application.
![](https://i.imgur.com/jpmcV7G.png)

#### Execute
Use the docker run command to put the service on the Container.
```lua

docker run -d -e"ES=http://elastic:PASSWARD@140.120.Forward port of DB" -p 80:9527 --name newcontainer kenny2330/pttwebapp:ver_1.0
```
Instruction parameters:<br>
-e Parameter setting, the ES mentioned earlier is used to set the Domain and password of the database <br> 
-p Bind the host's port to the container's port <br> 
-name Name your Container <br> 

