<template>
  <div>
    <nav class="navbar navbar-expand-sm navbar-dark bg-primary">
        <div class="navbar-nav">
          <span class="nav-item active text-white">PPT搜尋引擎</span>
        </div>
    </nav>

    <nav class="navbar navbar-expand-sm navbar-dark bg-secondary">
        <div class="navbar-nav">
          <router-link to="/" class="nav-item nav-link">帳號搜尋</router-link>
          <router-link to="/keyword" class="nav-item nav-link">關鍵字搜尋</router-link>
          <router-link to="/observe" class="nav-item nav-link">觀察帳號清單</router-link>
        </div>
    </nav>
  </div>
</template>

<style lang="scss" scoped>
.bgColor {
  background-color: #563d7c;
}
</style>
<script>
export default {
  name: "Header",
}
</script>