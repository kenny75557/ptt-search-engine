<template>
  <paginate
    :value="pageNum"
    :page-count="totalPageCount"
    :click-handler="changePage"
    :page-range="3"
    :margin-pages="1"
    :prev-text="prevText"
    :next-text="nextText"
    :container-class="'pagination'"
    :page-class="'page-item'"
    :page-link-class="'page-link'"
    :prev-class="'page-item'"
    :next-class="'page-item'"
    :prev-link-class="linkClass"
    :next-link-class="linkClass"
    :activate-class="'active'">
  </paginate>
</template>

<style lang="scss" scoped>

</style>

<script>
  import Paginate from 'vuejs-paginate';
  export default {
    name: "pagination",    
    components: {
      Paginate,
    },
    props: {
      prevText: String,
      nextText: String,
      linkClass: String,
      pageNum: Number,
      totalPageCount: Number,
    },
    methods: {
      changePage(num) {
        this.$emit('updatePage', num);
      }
    }
  }
</script>