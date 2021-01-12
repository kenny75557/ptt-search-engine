<template>
  <div>
    <div class="container">
      <p class="mt-5" v-if="route=='Account'">帳號查詢 (範例: alonelykid stinger5009) </p>
      <p class="mt-5" v-else-if="route=='Keyword'">關鍵字查詢 (範例: 跨年)</p>
      <div>
        <loading :active.sync="isLoading" 
        :can-cancel="true" 
        :is-full-page="fullPage"></loading>
        <SearchingBar @3param="urlMaker"></SearchingBar>
        <Result 
          :tableData="tableData"
          :input="input"
          :totalData="totalData">
        </Result>
         
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
import SearchingBar from '@/components/SearchingBar.vue'
import Result from '../components/Result.vue'
import Pagination from '../components/Pagination.vue';
// Import component
import Loading from 'vue-loading-overlay';
    // Import stylesheet
import 'vue-loading-overlay/dist/vue-loading.css';

export default {
  name: "Account",
  components: { 
    SearchingBar,
    Result,
    Pagination,
    Loading,
  },
  data() {
    return {
      input: '',
      requestUrl: '',
      tableData: [],
      totalData: '',
      //  分頁需要用到的參數
      prevText: '',
      nextText: '',
      linkClass: '',
      rowsPerPage: 10,
      pageNum: 3,
      totalPageCount: 0,
      isLoading: false,
      fullPage: true
    }
  },
  computed: {
    route: function(){ return this.$route.name }
  },
  methods:{
    requestSender(url){
      this.isLoading = true;
      this.$http.get(url, { headers:{
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, PATCH, PUT, DELETE, OPTIONS",
        "Access-Control-Allow-Headers": "Origin, Content-Type, X-Auth-Token"
      }}).then(r => {
          // console.log(r)
          this.tableData = r.data.hits.map(e => { return e })
          this.isLoading = false //Loading overlay
          if(this.route === "Account"){
            if(this.tableData.length == 0){
              alert('此帳號不存在');
            }
            else{
              // 搜尋資料筆數
              this.totalData = '共 ' + r.data.total.value + ' 筆資料';
              // 分頁顯示
              this.prevText = 'Prev';
              this.nextText = 'Next';
              this.linkClass = 'page-link';
              this.totalPageCount = Math.ceil(r.data.total.value / this.rowsPerPage);
            }
          }
          else if(this.route === "Keyword"){
            if(this.tableData.length == 0){
              alert('此關鍵字不存在');
            }
            else{
              // 搜尋資料筆數
              this.totalData = '共 ' + r.data.total.value + ' 筆資料';
              // 分頁顯示
              this.prevText = 'Prev';
              this.nextText = 'Next';
              this.linkClass = 'page-link';
              this.totalPageCount = Math.ceil(r.data.total.value / this.rowsPerPage);
            }
          }
          
      }).catch( r => console.log(r) )
     
    },

    urlMaker(input,d1, d2){
      this.isLoading = true;
      this.input = input
       var url = "http://140.120.182.87:6003/"
      //var url = top.location.href  - "page/"...
      console.log(url)
      if(this.route === "Keyword") url = url + "api/GetByContent?content="
      else if(this.route === "Account") url = url  + "api/GetByUserId?user_id="
      console.log(url)
      url = url + input
      if(isNaN(d1) && isNaN(d2)) url = url + "&start=none&end=none"
      else url = url + "&start=" + d1 + "&end=" + d2
      this.requestUrl = url
      url = url + "&size=" + this.rowsPerPage + "&from=0"
      this.pageNum = 1
      this.requestSender(url)
    },
    filterByPageNum(num){
      this.pageNum = num
      this.requestSender(this.requestUrl + "&size=" + this.rowsPerPage + "&from=" + this.rowsPerPage * (num - 1))
    },
  },
}

</script>