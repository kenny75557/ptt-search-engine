<template>
  <div id="app">
    <Index/>
  </div>
</template>

<style lang="scss">
@import '@/assets/all.scss';
</style>

<script>
import Index from '@/views/Index.vue'

export default {
  name: 'App',
  components: {
    Index,
  }
}
</script>

