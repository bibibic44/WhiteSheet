import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
// import _ from 'lodash'
import createPersistedState from "vuex-persistedstate"

Vue.use(Vuex)

export default new Vuex.Store({
  plugins: [createPersistedState()],

  state: {
    recommendedMovies: null,
    nowMovie: null,
    reviews: null,
    nowReview: null,
    nowUsername: null,
    isBtnToggle: false,
    accessUsername: null,
  },
  mutations: {
    ADD_NOW_MOVIES: function (state, movie) {
      state.nowMovie = movie
    },
    ADD_RECOMMENDED_MOVIES: function (state, recommendedMovies) {
      state.recommendedMovies = recommendedMovies
    },
    ADD_NOW_REVIEW: function (state, review) {
      state.nowReview = review
    },
    GET_REVIEWS: function (state, reviews) {
      state.reviews = reviews
    },
    CLEAR_RECOMMENDATION: function (state) {
      state.recommendedMovies = null
    },
    GET_USERNAME: function (state, username) {
      state.nowUsername = username
    },
    RECOMMEND_RESET: function (state) {
      state.recommendedMovies = null
    },
    BTN_TOGGLE: function (state) {
      state.isBtnToggle = !state.isBtnToggle
    },
    ACCESS_USER: function (state, accessUsername) {
      state.accessUsername = accessUsername
    }
  },
  actions: {
    recommenderToggle: function ({ commit }) {
      commit('BTN_TOGGLE')
    },
    userLikeMovie: function ({ commit }, context) {
      commit('ADD_NOW_MOVIES', context.movie)
      let genreData = null
      if (context.movie) {
        genreData = {
          genres: context.movie.genre_ids
        }
      }
      // if (genreData.genres) {
      axios({
        method: 'post',
        url: 'http://127.0.0.1:8000/movies/recommended_movies/',
        data: genreData,
        headers: context.setToken,
      })
        .then((res) => {
          // console.log(res)
          console.log(res.data)
          commit('ADD_RECOMMENDED_MOVIES', res.data)
        })
      // }
    },
    getReviews: function ({ commit }, context) {
      commit('ADD_NOW_REVIEW', context.review)
      axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/movies/reviews/',
        headers: context.setToken,
      })
        .then((res) => {
          console.log(res)
          commit('GET_REVIEWS', res.data)
        })
    },
    recommendClear: function ({ commit }, context) {
      axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/movies/recommended_movies/clear/',
        headers: context.setToken,
      })
        .then((res) => {
          console.log(res)
          commit('CLEAR_RECOMMENDATION')
        })
        .catch((err) => {
          console.log(err)
        })
    },
    logoutRecommend: function({ commit }) {
      commit('RECOMMEND_RESET')
    },
    getUsername: function ({ commit }, context) {
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/accounts/userinfo/${context.userPk}/`,
        headers: context.setToken,
      })
        .then((res) => {
          console.log(res.data.username)
          commit('GET_USERNAME', res.data.username)
        })
        .catch((err) => {
          console.log(err)
        })
    },
    accessUser: function ({ commit }, accessUsername) {
      commit('ACCESS_USER', accessUsername)
    }
  },
  modules: {
  }
})
