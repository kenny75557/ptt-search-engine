import Vue from 'vue'
import App from './App.vue'
import router from '@/router.js'
import axios from 'axios'
import VueAxios from 'vue-axios'
import 'bootstrap'
import './bus.js'

Vue.use(VueAxios, axios)
Vue.config.productionTip = false

new Vue({
  router,
  render: function (h) { return h(App) }
}).$mount('#app')
