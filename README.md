# PTTSearchEngine_web
## 使用Flask及Vuejs建立Web application
使用vue前端框架開發一個單頁應用程式(SPA)，再將建置好的前端界面交由Flask作為服務端，處理Request以及對Elasticsearch下搜尋指令之API。此筆記將會分為Vue.js以及Flask兩部分。
### 架構圖
![](https://i.imgur.com/JFfRHzW.png)


網頁應用及路由基本觀念可以參考:
[SPA & Router](https://blog.huli.tw/2019/09/18/spa-common-problem-about-router/)




## Vue.js
### 啟用
前置:

`npm install -g @vue/cli`

專案建置流程:
```
$ vue create <project_name>
$ npm install axios vue-axios bootstrap jquery popper.js -save
```
建置完成後進入專案目錄:

```
// 在 app.vue
<style>
@import './assets/all';
</style>

// 然後到 指定資料夾內 新增 all.scss 後
@import "~bootstrap/scss/functions";
@import "./helpers/_variables";
@import "~bootstrap/scss/bootstrap";

// 在 assets 裡新增 helpers 資料夾並且放入 _variables.scss 
// 來自 node_moudles/bootstrap/scss/_variables.scss

// 執行 eslint init, 選擇有框架的
// 將上面裝的套件匯入
// main.js
import axios from 'axios'
import VueAxios from 'vue-axios'
import 'bootstrap'

Vue.use(VueAxios, axios)

```
### Compiles and hot-reloads for development
開發時在專案目錄下可用來刷新修改後的網頁(在瀏覽器查看)。
```
yarn serve
```

### Compiles and minifies for production
修改程式後使用指令建立出新的Dist資料夾，更新到後端目錄中。
```
yarn build
```

### 頁面架構
```
.
├── package.json
├── public
│   ├── favicon.ico
│   └── index.html  // 入口文件，系統進入之後先進入index.html
└── src
    ├── App.vue  // 專案中的主要組件，所有頁面都在App.vue下進行切換
    ├── assets
    │   ├── all.scss
    │   ├── helpers
    │   │   ├── AQI.scss
    │   │   ├── reset.css
    │   │   └── _variables.scss
    │   └── logo.png
    ├── bus.js
    ├── components  // 將常用的功能寫成元件方便在不同頁面使用
    │   ├── Footer.vue  // 網頁頁尾
    │   ├── GetInput.vue  // 新增觀察ID的輸入欄位，可以得到使用者輸入的ID
    │   ├── Header.vue  // 網頁標頭:放置網站標題、三個功能頁面的切換
    │   ├── Pagination.vue  // 設定vuejs-paginate分頁套件
    │   ├── Result.vue  // 帳號和關鍵字的搜尋結果
    │   └── SearchingBar.vue  // 搜尋帳號和關鍵字的搜尋列，包括日期區間以及重設日期
    ├── main.js  // 建立 Vue 的實例、使用額外套件主要import的地方
    ├── router.js  // 路由檔案的配置及管理
    └── views  // 顯示的頁面
        ├── Index.vue  // 首頁:包括header和配置的路由元件
        ├── ObserveList.vue  // 觀察帳號清單的頁面
        ├── Search.vue  // 搜尋帳號和關鍵字的頁面
        └── ViewRecords.vu  // 查看觀察清單紀錄的頁面
```

### Components使用
#### Header.vue - 網頁標題以及三個功能頁面(帳號搜尋、關鍵字搜尋、觀察帳號清單)的切換
In Vue Template - Basic Usage
```html
<Header><Header>
```

#### SearchingBar.vue - 搜尋帳號和關鍵字的搜尋列，包括日期區間以及重設日期
In Vue Template - Basic Usage
```html
<SearchingBar @3param="functionName">
</SearchingBar>
```
Example
```html
<template>
  <SearchingBar @3param="urlMaker">
  </SearchingBar>
</template>

<script>
export default {
  methods: {
    urlMaker(input, d1, d2) {
      console.log(input, d1, d2)
    }
  }
}
</script>
```
Props
|Name&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | Type | Description |
| ----------------- | :--- | :--- |
| `@3param` | `Function` | 這個方法使用在使用者搜尋帳號或關鍵字時，可以得到輸入以及選擇的日期。|

#### Result.vue - 顯示帳號和關鍵字的搜尋結果
In Vue Template - Basic Usage
```html
<Result 
  :tableData='[
    {
      "_source": {
        "article_id": "M.1604988654.A.8B3",
        "user_id": "stinger5009",
        "board": "C_Chat",
        "date": 1605017522,
        "article_url": "https://www.ptt.cc/bbs/C_Chat/M.1604988654.A.8B3.html",
        "article_title": "[閒聊] 有沒有人跟我一樣對holo很失望= =",
        "content": "超級喜歡~郭顏文~~",
        "comment_tag": "推",
      }
    },
    {
      "_source": {
        "article_id": "M.1604989190.A.632",
        "user_id": "stinger5009",
        "board": "C_Chat",
        "date": 1605018120,
        "article_url": "https://www.ptt.cc/bbs/C_Chat/M.1604989190.A.632.html",
        "article_title": "[閒聊] 令狐沖打得過宋青書嗎？",
        "content": "沖哥應該完全看不懂九陰白骨爪XD",
        "comment_tag": "推",
      }
    },
  ]'
  :input="'stinger5009'"
  :totalData="'共 720 筆資料'">
</Result>
```
Value Binding
```html
<template>
  <Result 
    :tableData="tableData"
    :input="input"
    :totalData="totalData">
  </Result>
</template>

<script>
export default {
  data() {
    return {
      tableData:[
        {
          "_source": {
            "article_id": "M.1604988654.A.8B3",
            "user_id": "stinger5009",
            "board": "C_Chat",
            "date": 1605017522,
            "article_url": "https://www.ptt.cc/bbs/C_Chat/M.1604988654.A.8B3.html",
            "article_title": "[閒聊] 有沒有人跟我一樣對holo很失望= =",
            "content": "超級喜歡~郭顏文~~",
            "comment_tag": "推",
          }
        },
        {
          "_source": {
            "article_id": "M.1604989190.A.632",
            "user_id": "stinger5009",
            "board": "C_Chat",
            "date": 1605018120,
            "article_url": "https://www.ptt.cc/bbs/C_Chat/M.1604989190.A.632.html",
            "article_title": "[閒聊] 令狐沖打得過宋青書嗎？",
            "content": "沖哥應該完全看不懂九陰白骨爪XD",
            "comment_tag": "推",
          }
        },
      ]
      input: 'stinger5009',
      totalData: '共 720 筆資料',
    }
  }
}
</script>
```
Props
|Name&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | Type | Description |
| ----------------- | :--- | :--- |
| `tableData`       | `Array`  | 要顯示在表格上的搜尋資料，需要有<br>article_id(文章ID)、<br>user_id(使用者ID)、<br>board(版名)、<br>date(以timestamp顯示日期)、<br>article_url(文章連結)、<br>article_title(文章標題)、<br>content(文章或留言內容)、<br>comment_tag(留言標籤推/噓/->)<br>並且在"_source"這個dictionary中。 |
| `input`           | `String` | 使用者輸入的搜尋。 |
| `totalData`       | `String` | 顯示搜尋的總筆數。 |


#### Pagination.vue - 將搜尋的結果做分頁顯示
In Vue Template - Basic Usage
```html
<Pagination
  :prevText="'Prev'"
  :nextText="'Next'"
  :linkClass="'page-link'"
  @updatePage="functionName"
  :pageNum="1"
  :totalPageCount="721">
</Pagination>
```
Example
```html
<template>
  <Pagination
    :prevText="'Prev'"
    :nextText="'Next'"
    :linkClass="'page-link'"
    @updatePage="filterByPageNum"
    :pageNum="1"
    :totalPageCount="721">
  </Pagination>
</template>

<script>
export default {
  methods: {
    filterByPageNum(num) {
      console.log(num)
    }
  }
}
</script>
```
Value Binding
```html
<template>
  <Pagination
    :prevText="prevText"
    :nextText="nextText"
    :linkClass="linkClass"
    @updatePage="filterByPageNum"
    :pageNum="pageNum"
    :totalPageCount="totalPageCount">
  </Pagination>
</template>

<script>
export default {
  data() {
    return {
      prevText: 'Prev',
      nextText: 'Next',
      linkClass: 'page-link',
      pageNum: 3,
      totalPageCount: 0,
    }
  }
}
</script>
```
Props
|Name&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | Type | Description |
| ----------------- | :--- | :--- |
| `prevText`       | `String` | 顯示在上一頁按鈕上的文字。 |
| `nextText`       | `String` | 顯示在下一頁按鈕上的文字。 |
| `linkClass`      | `String` | 分頁的樣式Class。 |
| `@updatePage`    | `Function` | 這個方法使用在使用者在點選分頁按鈕時，可以得到目前的分頁頁數。 |
| `pageNum`        | `Number` | 分頁現在指向的頁數。 |
| `totalPageCount` | `Number` | 資料頁數的總數。 |

#### GetInput.vue - 新增觀察ID的輸入欄位，可以得到使用者的輸入
In Vue Template - Basic Usage
```html
<GetInput @getInput="getInput">
</GetInput>
```
Example
```html
<template>
  <GetInput @getInput="getInput">
  </GetInput>
</template>

<script>
export default {
  methods: {
    getInput(input) {
      console.log(input)
    }
  }
}
</script>
```
Props
|Name&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | Type | Description |
| ----------------- | :--- | :--- |
| `@getInput` | `Function` | 這個方法使用在使用者新增觀察ID時，可以得到使用者輸入的ID。|

## Flask
### 安裝flask

安裝Flask和Flask-CORS擴充套件

`(env)$ pip install Flask Flask-Cors `

背景處理下(保存Session，可使用[Tmux](https://larrylu.blog/tmux-33a24e595fbc))，執行main.py即可將服務開啟在server。
```
//在Flask目錄下 
tmux
<Ctrl+b> + s//選擇Session 
python app.py

```

### Query API
處理如何將前端發送的搜尋條件處理成Query並發送到ElasticSearch。

在main.py中引入Elasticsearch套件，對資料庫發request可回傳資料。

這邊使用環境參數是為了資料庫網域及密碼更動上有更多彈性，在部屬時由Docker指令帶入，也可以直接把輸入你ES服務的連接格式(如下方註解)。


連結ES設定:

```python=
from elasticsearch import Elasticsearch, RequestsHttpConnection
es = Elasticsearch(os.environ['ES'],connection_class=RequestsHttpConnection, use_ssl=True,verify_certs=False,send_get_body_as='POST' )
//ES帶換成['http://elastic:<key>@<Domain>']
```


#### 搜尋處理範例(由id檢索)
API格式如下，"?"符號之後為用於設定DSL語法搜尋之參數，Elastisearch如何Query請參照:[連結1](https://godleon.github.io/blog/Elasticsearch/Elasticsearch-advanced-search/) ，[連結2](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html)

```javascript=
<yourDomain>/api/GetByUserId?user_id=String&start=timeStamp&end=timeStamp?size=25?from=1
 //
<yourDomain>/api/GetByContent?Content=String&start=timeStamp&end=timeStamp?size=25?from=1
```

以下為使用到的變數:
1. user_id:作者id
1. content:內文搜尋(關鍵字)
1. start:日期起始點(以Timestamp格式)
1. end:日期結束點(以Timestamp格式)
1. size:顯示幾筆資料
1. from:從第幾筆資料開始

把資料處理好後包成DSL，使用ES的search function將送到DB，最後再以JSON格式回傳前端:
 ```python=
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
註:其餘細節請參見程式碼註解

### 將整套前後端包成Docker image
#### Dockerfile
[官方文檔](https://docs.docker.com/engine/reference/builder/)
寫一個Dockerfile將Build好的前端專案及Flask包成一個image。

**Dockerfile**
```dockerfile=
FROM python:3.6.9 #Base Image環境版本

WORKDIR /PTTapp #欲建立的工作目錄

ADD . /PTTapp  #複製檔案及資料夾加入到指定位置

RUN pip install -r requirements.txt
# 每一個 RUN 指令會在現有映像檔之上加入新的一層，是在建立 (build) 映像檔的過程中會執行的指令。
CMD python main.py #在Container中運行時所執行的指令
```
**requirements.txt**:所使用套件的版本

完成後，使用指令Build出一個docker image，在Flask資料夾下，Terminal輸入
```
docker image build -t <帳號>/<Image名稱>:<版本Tag> .
//docker帳號可以省略，除非你有需要推到DockerHub上
```
![](https://i.imgur.com/Wo2qYbU.png)

完成後可以在Terminal輸入`docker images`或是在應用程式上看到剛剛創建的檔案。
![](https://i.imgur.com/jpmcV7G.png)

#### 執行
使用docker run指令，把服務on在Container上。
```lua=

docker run -d -e"ES=http://elastic:密碼@140.120.DB的對外port" -p 80:9527 --name newcontainer kenny2330/pttwebapp:ver_1.0
```
指令參數:
-e 參數設定，前面提到的ES用來設置資料庫的Domain及密碼
-p 將主機的Port與Container的port綁定
-name 替你的Container命名