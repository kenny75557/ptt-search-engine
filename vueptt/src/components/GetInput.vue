<template>

  <form>
    <div class="row mt-5">
      <div class="col-10 pr-0">
        <input type="text" class="form-control" placeholder="輸入ID" v-model="input">
      </div>
      <div class="col-2">
        <button type="button" class="btn btn-primary" @click="setInput">新增觀察</button>
      </div>
      
    </div>
  </form>

</template>



<style lang="scss" scoped>

</style>



<script>
  export default {
    name: "GetInput",
    data() {
      return {
        input: ''
      }
    },
    methods: {
      setInput() {
        this.$emit('getInput', this.input);
      }
    }
  }
</script>