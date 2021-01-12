<template>

  <form>
    <div class="row mt-5">
      <div class="col-10 pr-0">
       
        <input type="text" class="form-control" placeholder="請輸入" v-model="input">
      </div>
      <div class="col-2">
        <button type="button" class="btn btn-primary" @click="setSearch">Search</button>
      </div>

      <div class="col-10 pr-0">
        <p class="mt-5">選擇日期區間</p>
        <input type="date" v-model="startDate"> 
        <input type="date" v-model="endDate">
        
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
  //  // Import component
  //   import Loading from 'vue-loading-overlay';
  //   // Import stylesheet
  //   import 'vue-loading-overlay/dist/vue-loading.css';
  export default {
    name: "Searchbar",
    data(){
      return {
        input: '',
        startDate: '',
        endDate: '',
        d1: 0,
        d2: 0,
        input_clean:''
      }
    },
    props: {
      // inputPlaceholder: String,
      // buttonText: String,
    },
    computed: {
    },
    methods: {
      dateToTimestamp(date){  // timestamp 單位為秒
        return Date.parse(date+'T00:00:00') / 1000;
      },
      //TODO: prevent SQL injection if needed
      checkSearch(){
        this.d1 = this.dateToTimestamp(this.startDate)
        this.d2 = this.dateToTimestamp(this.endDate)

        if(!this.input || this.input.trim().length === 0) return "請確實輸入"
        else{
          if(isNaN(this.d1) && isNaN(this.d2)){
            return true // Valid Input with Both NaN
          }
          else if(isNaN(this.d1) || isNaN(this.d2)) return "請輸入完整的日期"
          else{
            if(this.d1 > this.d2){
              this.d1 = [this.d2, this.d2=this.d1][0]; // Swap d1 and d2
              return true // Valid Input with Both Num
            } 
            else {
              return true // Valid Input with Both Num
            }
          }
        }
      },
      setSearch() {
        if(this.checkSearch() === true){
          this.input_clean = this.input.trim();
          this.$emit('3param', this.input_clean, this.d1, this.d2);
        } else{
          alert(this.checkSearch())}
      }
    
    }

  }
</script>