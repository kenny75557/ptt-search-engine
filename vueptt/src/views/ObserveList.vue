<template>
  <div>
    <div class="container">alonelykid stinger5009
      <p class="mt-5">新增觀察ID</p>
        <GetInput class="mb-5" @getInput="getInput"></GetInput>

        <table class="table table-striped">
          <thead>
            <tr>
              <th>觀察ID</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="id in list" :key="id">
              <td>{{ id }}</td>
              <td>
                <router-link type="button" class="btn btn-primary" :to="{ name: 'ViewRecords', params: { id: id } }" @click="passValue(id)">查看紀錄</router-link>
                <button type="button" class="btn btn-danger" @click="deleteLocalStorageArray(id)">移除觀察</button>
              </td>
            </tr>
          </tbody>
        </table>
    </div>
  </div>
</template>

<style lang="scss" scoped>

</style>

<script>
  import GetInput from "@/components/GetInput.vue"

  export default {
    name: 'ObserveList',
    components: { 
      GetInput,
    },
    mounted(){
      this.datalist = this.getLocalStorageArray()
    },
    data() {
      return {
        datalist: []
      }
    },
    computed: {
      list: function(){ return this.datalist }
    },
    methods:{
      getLocalStorageArray(){
        var rawData = localStorage.getItem("ObservedList")
        var arr = JSON.parse(rawData)
        return arr
      },
      setLocalStorageArray(array){
        this.datalist = array
        var target = JSON.stringify(array)
        localStorage.setItem('ObservedList',target)
      },
      deleteLocalStorageArray(id) { //  ObserveTable components
        var yes = confirm('確定移除 '+ id +' 嗎？');  //  確認是否刪除
        if(yes){
          var arr = this.getLocalStorageArray()
          arr.splice(arr.indexOf(id),1)
          this.setLocalStorageArray(arr)
        }
      },
      getInput(p) {  // Set Peek and Remove LocalStorage
        if(this.getLocalStorageArray("ObservedList") === null){
          var a = []
          this.setLocalStorageArray(a)
        }
        var tempArray = this.getLocalStorageArray("ObservedList")

        if( tempArray.find(e => e==p) ) alert('此 ID 已在觀察名單內')
        else{
          var url = "http://140.120.182.87:6003/api/GetByUserId?user_id="+ p +"&start=none&end=none"
          this.$http.get(url, { headers:{
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PATCH, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "Origin, Content-Type, X-Auth-Token"
          }}).then(r =>{
            // console.log(r)
            if(r.data.hits.length === 0) alert('此 ID 不存在')
            else {
              tempArray.push(p)
              this.setLocalStorageArray(tempArray)
            }
          }).catch(r => console.log(r))
        }
      },
      passValue(id) { this.$router.push({name:'ViewRecords',params:{id:id}}) },
    }
  }

</script>
