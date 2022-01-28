## Vue.js
### Enable
Env install:

`npm install -g @vue/cli`

Install the JS pakage management tool[yarn](https://yarnpkg.com/getting-started/install)
```
npm install -g yarn
```

### Compiles and hot-reloads for development
It can be used to refresh the modified web page in the project directory during development (view it directly in the browser).
```
yarn serve
```

### Compiles and minifies for production
After modifying the program, execute build, and update the built dist folder to the backend directory.
```
yarn build
```

### Directory structure
```
.
├── package.json
├── public
│   ├── favicon.ico
│   └── index.html  //Entry file, enter first after system entryindex.html
└── src
    ├── App.vue  // The main components in the project, all pages are switched under App.vue
    ├── assets
    │   ├── all.scss
    │   ├── helpers
    │   │   ├── AQI.scss
    │   │   ├── reset.css
    │   │   └── _variables.scss
    │   └── logo.png
    ├── bus.js
    ├── components  // Write commonly used functions as components for easy use on different pages
    │   ├── Footer.vue  //page footer
    │   ├── GetInput.vue  // Added the input field of observation ID, you can get the ID input by the user
    │   ├── Header.vue  // Web page header: place website title, switch between three functional pages
    │   ├── Pagination.vue  // Set up vuejs-paginate pagination suite
    │   ├── Result.vue  // Search results for accounts and keywords
    │   └── SearchingBar.vue  // Search bar for accounts and keywords, including date ranges and reset dates
    ├── main.js  //Where to create an instance of Vue, where to use the main import of the extra kit
    ├── router.js  // Configuration and management of routing files
    └── views  //displayed page
        ├── Index.vue  //Home: Routing elements including header and configuration
        ├── ObserveList.vue  // Watch the account list page
        ├── Search.vue  // Search page for accounts and keywords
        └── ViewRecords.vu  // View the Watch List Records page
```
![](https://i.imgur.com/M2wL9fu.jpg)


### Components
#### Header.vue - The page title and the switching of three functional pages (account search, keyword search, watch account list)
In Vue Template - Basic Usage
```html
<Header><Header>
```

#### SearchingBar.vue - Search bar for accounts and keywords, including date ranges and reset dates
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
| `@3param` | `Function` | This method is used when a user searches for an account or keyword to get the date entered and selected.|

#### Result.vue - Displays search results for account numbers and keywords
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


#### Pagination.vue - Paginate the search results
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
| `prevText`       | `String` |  The text to display on the previous page button. |
| `nextText`       | `String` | The text to display on the next page button. |
| `linkClass`      | `String` | Pagination style Class. |
| `@updatePage`    | `Function` | This method is used when the user clicks the paging button to get the current number of paging pages. |
| `pageNum`        | `Number` | The number of pages the pagination now points to. |
| `totalPageCount` | `Number` | The total number of data pages |

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
| `@getInput` | `Function` | This method is used to get the ID entered by the user when the user adds an observation ID.|