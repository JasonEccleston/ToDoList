import Vue from 'vue'
import App from './App.vue'
import VeeValidate from 'vee-validate'
import axios from 'axios'
import router from './router'
import VueCookies from 'vue-cookies'

Vue.prototype.$axios = axios.create({
  withCredentials:true,
  'Access-Control-Allow-Origin':'*'
})
Vue.use(VueCookies)
Vue.use(VeeValidate)
Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
