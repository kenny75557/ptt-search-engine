<template>
  <div>
    <div class="container">
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
</template>

<style lang="scss" scoped>

</style>

<script>
import Result from '@/components/Result.vue';
import Pagination from '@/components/Pagination.vue';

  export default {
    name: 'ViewRecords',
    components: { 
      Result,
      Pagination,
    },
    data(){
      return{
        dataArray:[],
        input:'',
        tableData: [],
        requestUrl: '',
        totalData: '',
        //  分頁需要用到的參數
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
      var url = "http://140.120.182.87:6003/api/GetByUserId?user_id="+ id +"&start=none&end=none"

      
      //console.log(url)
      this.requestUrl = url

      url = url + "&size=" + this.rowsPerPage + "&from=0"

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
            this.dataArray = r.data.hits.map(e => { return e })

            this.tableHead = ['看板', '日期', '標題', '類型']
            this.tableTitle = this.input + ' 之發文紀錄'

            // 搜尋資料筆數
            this.totalData = '共 ' + r.data.total.value + ' 筆資料';
            // 分頁顯示
            this.prevText = 'Prev';
            this.nextText = 'Next';
            this.linkClass = 'page-link';
            this.totalPageCount = Math.ceil(r.data.total.value / this.rowsPerPage);
            this.tableData = this.dataArray.slice(0, this.rowsPerPage);
        }).catch( r => console.log(r) )        
      },  
      filterByPageNum(num){
        this.pageNum = num;
        this.requestSender(this.requestUrl + "&size=" + this.rowsPerPage + "&from=" + this.rowsPerPage * (num - 1))
      },
    }
  }


</script>