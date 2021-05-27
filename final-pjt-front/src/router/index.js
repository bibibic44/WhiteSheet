import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '@/views/movies/Home'
import ReviewList from '@/views/reviews/ReviewList'
import CreateReview from '@/views/reviews/CreateReview'
import Signup from '@/views/accounts/Signup'
import Login from '@/views/accounts/Login'
import LoginGoogle from '@/views/accounts/LoginGoogle'
import MovieCardDetail from '@/components/MovieCardDetail'
import ReviewListDetail from '@/views/reviews/ReviewListDetail'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/reviews',
    name: 'ReviewList',
    component: ReviewList,
  },
  {
    path: '/reviews/detail',
    name: 'ReviewListDetail',
    component: ReviewListDetail,
    props: true,
  },
  {
    path: '/reviews/create/',
    name: 'CreateReview',
    component: CreateReview,
    props: true,
  },
  {
    path: '/accounts/signup',
    name: 'Signup',
    component: Signup,
  },
  {
    path: '/accounts/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/accounts/LoginGoogle',
    name: 'LoginGoogle',
    component: LoginGoogle,
  },
  {
    path: '/MovieCardDetail',
    name: 'MovieCardDetail',
    component: MovieCardDetail,
    props: true,
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
