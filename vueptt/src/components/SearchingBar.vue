<template>

  <form>
    <div class="row mt-5">

      <div class="col-10 pr-0">
        <input type="text" class="form-control" placeholder="請輸入" v-model="input" @keydown.enter.prevent="setSearch">
      </div>

      <div class="col-2">
        <button type="button" class="btn btn-primary" @click="setSearch">Search</button>
      </div>

      <div class="col-10 pr-0">
        <p class="mt-5">選擇日期區間(預設搜尋最近一年之文章，清空可查詢所有歷史紀錄)</p>
        <input type="date" v-model="startDate" value-format="yyyy-MM-dd"> 
        <input type="date" v-model="endDate" value-format="yyyy-MM-dd">

        <div class="col-10 pr-0">
          <button type="button" class="btn btn-danger row mt-3" v-on:click= "startDate='' ,endDate=''">Reset Date</button>
        </div>
      </div>

    </div>
  </form>

</template>



<style lang="scss" scoped>

</style>



<script>
  import Loading from 'vue-loading-overlay';
  import 'vue-loading-overlay/dist/vue-loading.css';
  export default {
    name: "Searchbar",
    data(){
    let nowDate = new Date();
    let date = {
    year: nowDate.getFullYear(),
    month: nowDate.getMonth()+1,
    date: nowDate.getDate(),};
    let systemDate = date.year + "-"+(date.month<10?'0':'') + date.month + "-"+(date.date<10?'0':'') + date.date;//這裡
    console.log(systemDate)
    //一年前日期
    var beforedate = new Date(nowDate);
    beforedate.setDate(nowDate.getDate() - 1);
    let systemDateBegin = `${beforedate.getFullYear()}-${beforedate.getMonth() + 1<10?`0${beforedate.getMonth() + 1}`:beforedate.getMonth() + 1}-${beforedate.getDate()<10?'0'+beforedate.getDate():beforedate.getDate()}`;
    console.log(systemDateBegin)
    


    return {
        input: '',
        startDate: systemDateBegin,
        endDate: systemDate,
        d1: 0,
        d2: 0,
        input_clean:'',
        
      }
    },
    props: {
      // inputPlaceholder: String,
      // buttonText: String,
    },
    computed: {
    },
    methods: {
      // 將時間轉換為 timestamp
      dateToTimestamp(date){  // timestamp 單位為秒
        return Date.parse(date+'T00:00:00') / 1000;
      },
      //TODO: prevent SQL injection if needed
      // 檢查是否為合法的搜尋
      checkSearch(){
        this.d1 = this.dateToTimestamp(this.startDate)
        this.d2 = this.dateToTimestamp(this.endDate)

        // 判斷輸入是否為空
        if(!this.input || this.input.trim().length === 0) { 
          return "請確實輸入"
        }
        else{
          // 兩個日期皆為 NaN 時為合法的輸入
          if(isNaN(this.d1) && isNaN(this.d2)){
            return true // Valid Input with Both NaN
          }
          // 一個有日期一個沒日期為不合法的輸入
          else if(isNaN(this.d1) || isNaN(this.d2)) {
            return "請輸入完整的日期"
          }
          // 兩個日期皆不是 NaN 為合法輸入
          else{
            // 判斷日期順序是否相反
            if(this.d1 > this.d2){
              // 交換日期
              this.d1 = [this.d2, this.d2=this.d1][0]; // Swap d1 and d2
              return true // Valid Input with Both Num
            } 
            else {
              return true // Valid Input with Both Num
            }
          }
        }
      },
      // 回傳搜尋資訊
      setSearch() {
        // 判斷是否為合法的搜尋
        if(this.checkSearch() === true){
          this.input_clean = this.input.trim();
          // 將搜尋資訊傳遞到父元件
          this.$emit('3param', this.input_clean, this.d1, this.d2);
        } else{
          alert(this.checkSearch())
        }
      },
    
    }
  }
</script>