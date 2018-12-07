import Vue from 'vue'
import Router from 'vue-router'
import Main from './components/Main.vue'
import Signin from './components/Signin.vue'
import Signup from './components/Signup.vue'
import Home from './components/Home.vue'
import Profile from './components/Profile.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [

    {
      path: '/',
      name: 'main',
      component: Main
    },
    {
      path: '/signin',
      name: 'signin',
      component: Signin
    },
    {
      path: '/signup',
      name: 'signup',
      component: Signup
    },
    {
      path: '/home',
      name: 'home',
      component: Home
    },
    {
      path: '/profile',
      name: 'profile',
      component: Profile
    }
  ]
})
