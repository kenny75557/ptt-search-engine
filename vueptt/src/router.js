import Vue from 'vue'
import VueRouter from 'vue-router'

// import Account from '@/views/Account.vue'
// import Keyword from '@/views/Keyword.vue'
import ObserveList from '@/views/ObserveList.vue'
import ViewRecords from '@/views/ViewRecords.vue'
import Search from '@/views/Search.vue'

Vue.use(VueRouter)

  const routes = [
  {
    path: '*',
    redirect: 'Account'
  },
  {
    path: '/',
    name: 'Account',
    component: Search
  },
  {
    path: '/keyword',
    name: 'Keyword',
    component: Search
  },
  {
    path: '/observe',
    name: 'ObserveList',
    component: ObserveList 
  },
  {
    path: '/observe/:id',
    name: 'ViewRecords',
    component: ViewRecords 
  }
]

const router = new VueRouter({
  routes,
  mode:'history',
})

export default router
