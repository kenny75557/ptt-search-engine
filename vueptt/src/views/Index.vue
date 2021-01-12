<template>
  <div>
    <Header/>
    <router-view></router-view>
    <!-- <Footer/> -->
  </div>
</template>

<style lang="scss" scoped>

</style>

<script>
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'

export default {
  name: "Index",
  data() {
    return {
    }
  },
  components: {
    Header,
    Footer
  }
}
</script>