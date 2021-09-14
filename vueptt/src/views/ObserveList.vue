<template>
  <div>
    <div class="container">

      <p class="mt-5">新增觀察ID (範例: alonelykid stinger5009)</p>

      <!-- 使用元件取得輸入的 ID -->
      <GetInput class="mb-5" @getInput="getInput" ></GetInput>

      <!-- 觀察清單列表 -->
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
              <!-- 配置動態路由，並根據 params 的不同來顯示不同使用者資訊 -->
              <router-link type="button" class="btn btn-primary" :to="{ name: 'ViewRecords', params: { id: id } }">查看紀錄</router-link>
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
  import GetInput from "../components/GetInput.vue"

  export default {
    name: 'ObserveList',
    components: { // 使用的元件
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
      // 取出在 localStorage 的資料
      getLocalStorageArray(){
        // 把存進去的字串用 key 名取出來
        var rawData = localStorage.getItem("ObservedList")
        var arr = JSON.parse(rawData) 
        return arr
      },
      // 把字串存進 localStorage
      setLocalStorageArray(array){  
        this.datalist = array
        var target = JSON.stringify(array)
        localStorage.setItem('ObservedList',target)
      },
      // 使用者移除觀察 ID
      deleteLocalStorageArray(id) {
        // 確認是否刪除的通知
        var yes = confirm('確定移除 '+ id +' 嗎？');
        if(yes){
          // 取出 localStorage 的資料刪除 ID 後再存進去
          var arr = this.getLocalStorageArray()
          arr.splice(arr.indexOf(id),1)
          this.setLocalStorageArray(arr)
        }
      },
      // 從元件取得使用者輸入的觀察ID
      getInput(input) {
        // 如果在 localStorage 沒有發現資料的話，先設定 localStorage
        if(this.getLocalStorageArray("ObservedList") === null){
          var a = []
          this.setLocalStorageArray(a)
        }

        // 取出 localStorage 的資料
        var tempArray = this.getLocalStorageArray("ObservedList")

        // 判斷使用者輸入的 ID 是否已在觀察名單內
        if( tempArray.find(e => e==input) ) {
          alert('此 ID 已在觀察名單內')
        }
        else{
          
          // 在本地端測試的 url
          // var url = "http://140.120.182.87:6003/api/GetByUserId?user_id=" + input + "&start=none&end=none"
          
          // 上線的 url ( 因為架設的位置可能不同，需要根據上線的位置設定 url )
          var url = window.location.href
          url = url.replace("observe","")
          url = url + "api/GetByUserId?user_id=" + input + "&start=none&end=none"
          

          this.$http.get(url, { headers:{
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PATCH, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "Origin, Content-Type, X-Auth-Token"
          }}).then(r =>{
            // console.log(r)

            // 判斷資料庫中使否有輸入的 ID (資料庫搜尋 ID 的結果長度是否為 0)
            if(r.data.hits.length === 0) {
              alert('此 ID 不存在')
            }
            else {
              // 將輸入的 ID 加到 array 中，並且設定 localStorage
              tempArray.push(input) 
              this.setLocalStorageArray(tempArray)
            }
          }).catch(r => console.log(r))
        }
      },
    }
  }

</script>
