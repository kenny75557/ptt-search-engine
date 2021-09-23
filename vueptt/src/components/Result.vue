<template>
    
  <div>
    <!-- <div class="spinner-border text-primary" role="status">
      <span class="sr-only">Loading...</span>
    </div> -->
    <p class="mt-5" v-if="route=='Account' || route=='ViewRecords'">{{ input }} 之發文紀錄</p>
    <p class="mt-5" v-else-if="route=='Keyword'">{{ input }} 的相關推文</p>
    <p class="text-muted"> {{ totalData }} {{ searchTime }}</p>

    <table id="result" class="table table-striped">
      <thead>
        <tr v-if="route=='Account' || route=='ViewRecords'">
          <th v-for="i in accountHead" :key="i"> {{ i }} </th>
        </tr>
        <tr v-else-if="route=='Keyword'">
          <th v-for="i in keywordHead" :key="i"> {{ i }} </th>
        </tr>
      </thead>
  

      <tbody v-if="route=='Account' || route=='ViewRecords'">
        <tr v-for="item in tableData" :key="item._id">
          <td>{{ item._source.board }}</td>

          <!-- handle scapy-data loss -->
          <!-- 因為時區的關係，需要加 8 小時 -->
          <td v-if="item._source.date">{{ new Date((Number(item._source.date)+28800) * 1000).toISOString().split("T")[0] }}</td>
          <td v-else >無法顯示</td>
          <td v-if="item._source.article_title"><a target="_blank" :href="item._source.article_url">{{ item._source.article_title }}</a> </td>
          <td v-else><a target="_blank" :href="item._source.article_url">來源格式錯誤，點擊以查看原文網址</a> </td>
          <td v-if="item._source.content.length <= 25">{{ item._source.comment_tag }} : {{ item._source.content }}</td>
          <td v-if="item._source.content.length > 25">{{ item._source.comment_tag }} : {{ item._source.content.substr(0, 25) + ' . . .' }}</td>
        </tr>
      </tbody>

      <tbody v-else-if="route=='Keyword'">
        <tr v-for="item in tableData" :key="item._id">
          <td>{{ item._source.user_id }}</td>
          <td>{{ item._source.board }}</td>
          <td v-if="item._source.date">{{ new Date((Number(item._source.date)+28800) * 1000).toISOString().split("T")[0] }}</td>
          <td v-else >無法顯示</td>
          <td><a target="_blank" :href="item._source.article_url">{{ item._source.article_title }}</a> </td>
          <td v-if="item._source.content.length <= 20">{{ item._source.comment_tag }} : {{ item._source.content }}</td>
          <td v-if="item._source.content.length > 20">{{ item._source.comment_tag }} : {{ item._source.content.substr(0, 20) + ' . . .' }}</td>
        </tr>
      </tbody>

    </table>
  </div>

</template>

<style lang="scss" scoped>

</style>

<script>
  export default {
    name: "Result",
    data(){
      return {
        accountHead: ['看板', '日期', '標題', '類型'],
        keywordHead: ['作者帳號', '看板', '日期', '標題', '類型']
      }
    },
    computed: {
      route: function(){ return this.$route.name },
    },
    props: {
      tableData: Array,
      input: String,
      totalData: String,
      searchTime: String,
    },
  }
  
</script>