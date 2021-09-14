<template>
  <div>
    <div class="container">
      <!-- 使用元件顯示搜尋結果 -->
      <Result 
        :tableData="tableData"
        :input="input"
        :totalData="totalData">
      </Result>
      
      <!-- 使用元件顯示資料分頁 -->
      <Pagination
        :prevText="prevText"
        :nextText="nextText"
        :linkClass="linkClass"
        @updatePage="filterByPageNum"
        :pageNum="pageNum"
        :totalPageCount="totalPageCount">
      </Pagination>
    </div>
  </div>
</template>

<style lang="scss" scoped>

</style>

<script>
import Result from '../components/Result.vue';
import Pagination from '../components/Pagination.vue';

  export default {
    name: 'ViewRecords',
    components: { // 使用的元件
      Result,
      Pagination,
    },
    data(){
      return{
        requestUrl: '',
        dataArray:[],
        // Result 元件需要用到的參數
        input:'',
        tableData: [],
        totalData: '',
        //  Pagination 元件需要用到的參數
        prevText: '',
        nextText: '',
        linkClass: '',
        rowsPerPage: 10,
        pageNum: 1,
        totalPageCount: 0,
      }
    },
    mounted(){
      var id = this.$route.params.id
      this.input = id
      
      // 在本地端測試的 url
      // var url = "http://140.120.182.87:6003/api/GetByUserId?user_id=" + id + "&start=none&end=none" //former call api method
      
      // 上線的 url ( 因為架設的位置可能不同，需要根據上線的位置設定 url )
      var url = window.location.href
      url = url.replace("observe/" + id,"")
      url = url + "api/GetByUserId?user_id=" + id + "&start=none&end=none"
      
      // 儲存 url ( 為了在分頁時搜尋某個範圍的資料 )
      this.requestUrl = url

      // 設定資料數量以及從哪筆資料開始取得
      url = url + "&size=" + this.rowsPerPage + "&from=0"
      // console.log(url)
      this.requestSender(url)
    },
    methods: {  
      requestSender(url){
        this.$http.get(url, { headers:{
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "GET, POST, PATCH, PUT, DELETE, OPTIONS",
          "Access-Control-Allow-Headers": "Origin, Content-Type, X-Auth-Token"
        }}).then(r => {
            // console.log(r)
            // 設定搜尋到的資料
            this.dataArray = r.data.hits.map(e => { return e })

            // 設定搜尋資料筆數
            this.totalData = '共 ' + r.data.total.value + ' 筆資料';
            // 設定分頁元件的參數
            this.prevText = 'Prev';
            this.nextText = 'Next';
            this.linkClass = 'page-link';
            this.totalPageCount = Math.ceil(r.data.total.value / this.rowsPerPage);
            this.tableData = this.dataArray.slice(0, this.rowsPerPage);
        }).catch( r => console.log(r) )        
      },  
      // 從分頁元件取得頁碼
      filterByPageNum(num){
        this.pageNum = num;
        // 設定資料數量以及從哪筆資料開始取得
        this.requestSender(this.requestUrl + "&size=" + this.rowsPerPage + "&from=" + this.rowsPerPage * (num - 1))
      },
    }
  }


</script>