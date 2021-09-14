<template>
  <div>
    <div class="container">
      <p class="mt-5" v-if="route=='Account'">帳號查詢 (範例: alonelykid stinger5009) </p>
      <p class="mt-5" v-else-if="route=='Keyword'">關鍵字查詢 (範例: 跨年)</p>
      <div>
        <!-- 使用載入中(Loading)遮罩套件 -->
        <loading 
          :active.sync="isLoading" 
          :can-cancel="true" 
          :is-full-page="fullPage">
        </loading>

        <!-- 使用元件取得搜尋資訊 -->
        <SearchingBar @3param="urlMaker"></SearchingBar>

        <!-- 使用元件顯示搜尋結果 -->
        <Result 
          :tableData="tableData"
          :input="input"
          :totalData="totalData"
          :searchTime="searchTime">
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
  </div>
</template>

<style lang="scss" scoped>

</style>

<script>
import SearchingBar from '../components/SearchingBar.vue'
import Result from '../components/Result.vue'
import Pagination from '../components/Pagination.vue';
// Import component
import Loading from 'vue-loading-overlay';
// Import stylesheet
import 'vue-loading-overlay/dist/vue-loading.css';

export default {
  name: "Search",
  components: { // 使用的元件
    SearchingBar,
    Result,
    Pagination,
    Loading,
  },
  data() {
    return {
      requestUrl: '',
      // Result 元件需要用到的參數
      input: '',
      tableData: [],
      totalData: '',
      startTime: 0,
      searchTime: '',
      //  Pagination 元件需要用到的參數
      prevText: '',
      nextText: '',
      linkClass: '',
      rowsPerPage: 10,
      pageNum: 1,
      totalPageCount: 0,
      // loading 元件需要用到的參數
      isLoading: false,
      fullPage: true
    }
  },
  computed: {
    route: function(){ return this.$route.name }
  },
  methods:{
    requestSender(url){
      this.startTime = new Date();
      this.isLoading = true;
      this.$http.get(url, { headers:{
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, PATCH, PUT, DELETE, OPTIONS",
        "Access-Control-Allow-Headers": "Origin, Content-Type, X-Auth-Token"
      }}).then(r => {
          // console.log(r)
          // 設定搜尋到的資料
          this.tableData = r.data.hits.map(e => { return e })
          this.isLoading = false //Loading overlay
          if(this.route === "Account"){
            // 判斷資料庫中使否有輸入的 ID
            if(this.tableData.length == 0){
              this.totalData = '共 0 筆資料'; // 設定搜尋資料筆數
              alert('此帳號不存在');  
            }
            else{
              // 設定搜尋資料筆數
              this.totalData = '共 ' + r.data.total.value + ' 筆資料';
              // 設定搜尋時間(毫秒轉成秒)
              var endTime = new Date();
              var time = (endTime.getTime() - this.startTime.getTime()) / 1000;
              this.searchTime = '(搜尋時間：' + time + ' 秒)';
              // 設定分頁元件的參數
              this.prevText = 'Prev';
              this.nextText = 'Next';
              this.linkClass = 'page-link';
              this.totalPageCount = Math.ceil(r.data.total.value / this.rowsPerPage);
            }
          }
          else if(this.route === "Keyword"){
            // 判斷資料庫中使否有輸入的關鍵字
            if(this.tableData.length == 0){
              this.totalData = '共 0 筆資料'; // 設定搜尋資料筆數
              alert('此關鍵字不存在');
              
            }
            else{
              // 設定搜尋資料筆數
              this.totalData = '共 ' + r.data.total.value + ' 筆資料';
              // 設定搜尋時間(毫秒轉成秒)
              var endTime = new Date();
              var time = (endTime.getTime() - this.startTime.getTime()) / 1000;
              this.searchTime = '(搜尋時間：' + time + ' 秒)';
              // 設定分頁元件的參數
              this.prevText = 'Prev';
              this.nextText = 'Next';
              this.linkClass = 'page-link';
              this.totalPageCount = Math.ceil(r.data.total.value / this.rowsPerPage);
            }
          }
          
      }).catch( r => console.log(r) )
     
    },
    // 取得搜尋資訊並建立 url
    urlMaker(input,d1, d2){
      this.isLoading = true;
      this.input = input
      var url

      // 在本地端測試的 url
      // url = "http://140.120.182.87:6003/api/"
      // if(this.route === "Keyword") url = url + "GetByContent?content="
      // else if(this.route === "Account") url = url + "GetByUserId?user_id="

      // 上線的 url ( 因為架設的位置可能不同，需要根據上線的位置設定 url )
      if(this.route === "Keyword") {
        url = window.location.href
        url = url.replace("keyword","")
        url = url + "api/GetByContent?content="
      }
      else if(this.route === "Account"){
        url = window.location.href + "api/"
        url = url + "GetByUserId?user_id="
      }

      // 將搜尋加到 url 中
      url = url + input
      console.log(url)
      
      // 判斷搜尋的日期是否為空 
      if(isNaN(d1) && isNaN(d2)) {
        url = url + "&start=none&end=none"
      }
      else {
        url = url + "&start=" + d1 + "&end=" + d2
      }

      // 儲存 url ( 為了在分頁時搜尋某個範圍的資料 )
      this.requestUrl = url

      // 設定資料數量以及從哪筆資料開始取得
      url = url + "&size=" + this.rowsPerPage + "&from=0"
      // 設定分頁一開始的頁數
      this.pageNum = 1

      this.requestSender(url)
    },
    // 從分頁元件取得頁碼
    filterByPageNum(num){
      this.pageNum = num
      // 設定資料數量以及從哪筆資料開始取得
      this.requestSender(this.requestUrl + "&size=" + this.rowsPerPage + "&from=" + this.rowsPerPage * (num - 1))
    },
  },
}

</script>