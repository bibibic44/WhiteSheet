<template>
  <div> 
    <div id="nav" class="pt-0 pb-4">
      <nav class="navbar navbar-expand navbar-light pb-0">
        <div class="container">
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse d-flex justify-content-start" id="navbarNavAltMarkup">
            <div class="navbar-nav">
              <button class="nav-link btn btn-link" @click="nowPlayingMovies">상영중</button>
              <button class="nav-link btn btn-link" @click="popularMovies">인기영화</button>
              <button class="nav-link btn btn-link" @click="topRatedMovies">높은 평점</button>
              <button class="nav-link btn btn-link" @click="upcomingMovies">개봉예정</button>
            </div>
          </div>
        </div>
      </nav>
      <div class="container"><hr class="mt-0"></div>
    </div>
    <div class="container">
      <section class="row row-cols-2">
        <ul @mouseover="onMouseOver" @mouseout="onMouseOut">
          <MovieCard v-for="(movie, idx) in movies" :key="idx" :movie="movie"/>
        </ul>
        <div class="row d-flex justify-content-center">
          <div class="box-movie"></div>
        </div>
      </section>
    </div>
    
    <button class="scroll-top" id="js-button" @click="goTop">
        gotop
    </button>
  </div>
</template>

<script>
import axios from 'axios'
import MovieCard from '@/components/MovieCard'

const API_KEY = process.env.VUE_APP_TMDB_API_KEY
const NOW_PLAYING_MOVIE_URL = `https://api.themoviedb.org/3/movie/now_playing?api_key=${API_KEY}&language=ko-KR&page=`
const POPULAR_URL = `https://api.themoviedb.org/3/movie/popular?api_key=${API_KEY}&language=ko-KR&page=`
const TOP_RATED_URL = `https://api.themoviedb.org/3/movie/top_rated?api_key=${API_KEY}&language=ko-KR&page=`
const UPCOMING_URL = `https://api.themoviedb.org/3/movie/upcoming?api_key=${API_KEY}&language=ko-KR&page=`

export default {
  name: 'Home',
  components: {
    MovieCard,
  },
  data: function () {
    return {
      movieList: [],
      movies: [],
      pageIdx: 1,
      category: '',
      maxPageIdx: null,
    }
  },
  methods: {
    // recommenderToggleOut: function () {
    //   this.$store.dispatch('recommenderToggle')
    //   let btnTrue = document.querySelector('#nav button')
    //   if (!this.isBtnToggle) {
    //     btnTrue.style.fontWeight = 'normal'
    //   }
    // },
    goTop: function (event) {
      event.preventDefault()
      window.scrollTo({ top: 0, behavior: 'smooth' })
    },
    // API 요청
    usingAxios: function (category, pageIdx) {
      axios({
        url: category + String(pageIdx),
        method: 'get',
      })
        .then(res => {
          // console.log(res.data)
          console.log(res)
          this.maxPageIdx = res.data.total_pages
          if (pageIdx <= this.maxPageIdx) {
            res.data.results.forEach((obj) => {
              this.movies.push(obj)
            })
          }
        })
        .catch(err => {
          console.log(err)
        })
    },
    nowPlayingMovies: function () {
      this.category = NOW_PLAYING_MOVIE_URL
      // 카테고리가 바뀌면 페이지 번호와 영화 리스트가 초기화
      this.pageIdx = 1
      this.movies = []
      this.usingAxios(this.category, this.pageIdx)
      // 스크롤 이벤트 
      addEventListener('scroll', this.infinteScroll)
    },
    popularMovies: function () {
      this.category = POPULAR_URL
      this.pageIdx = 1
      this.movies = []
      this.usingAxios(this.category, this.pageIdx)
      addEventListener('scroll', this.infinteScroll)
    },
    topRatedMovies: function () {
      this.category = TOP_RATED_URL
      this.pageIdx = 1
      this.movies = []
      this.usingAxios(this.category, this.pageIdx)
      addEventListener('scroll', this.infinteScroll)
    },
    upcomingMovies: function () {
      this.category = UPCOMING_URL
      this.pageIdx = 1
      this.movies = []
      this.usingAxios(this.category, this.pageIdx)
      addEventListener('scroll', this.infinteScroll)
    },
    setToken: function () {
      const token = localStorage.getItem('jwt')
      const config = {
        Authorization: `JWT ${token}`
      }
      return config
    },
    sendMovieList: function () {
      axios({
        method: 'post',
        url: 'http://127.0.0.1:8000/movies/',
        headers: this.setToken()
      })
        .then((res) => {
          console.log(res)
        })
        .catch((err) => {
          console.log(err)
        })
    },
    infinteScroll: function() {
      // 스크롤이 바닥에 닿으면 && 현재 페이지 번호가 최대 페이지 번호보다 적으면 API 요청을 보낸다.
      const {scrollTop, clientHeight, scrollHeight} = document.documentElement
      let scrollY = parseInt(scrollHeight - scrollTop)
      if (scrollY == clientHeight && this.pageIdx < this.maxPageIdx) {
        this.pageIdx += 1
        console.log(this.pageIdx)
        // 현재 카테고리에 해당하는 API URL에 요청을 보낸다. 인자로 새로 보여줄 페이지 번호를 넘겨준다.
        this.usingAxios(this.category, this.pageIdx)
      }
    },
    onMouseOver: function () {
      const backgroundColor = document.querySelector('body')
      backgroundColor.style.backgroundColor = '#393e46'
      backgroundColor.setAttribute('class', 'background-transition')
      const apiBtn = document.querySelectorAll('.btn-link')
      for (let i = 0; i < apiBtn.length; i++) {
        apiBtn[i].style.color = '#eeeeee'
      }
      const aTags = document.querySelectorAll('ul a')
      for (let i = 0; i < aTags.length; i++) {
        aTags[i].style.color = '#eeeeee'
      }
      const routerLinks = document.querySelectorAll('#nav .nav-link')
      for (let i = 0; i < routerLinks.length; i++) {
        routerLinks[i].style.color = '#eeeeee'
        // routerLinks[i].classList.remove('router-dark')
        // routerLinks[i].classList.add('router-light')
      }
    },
    onMouseOut: function () {
      const backgroundColor = document.querySelector('body')
      backgroundColor.style.backgroundColor = '#faf3f3'
      backgroundColor.setAttribute('class', 'background-transition')
      const apiBtn = document.querySelectorAll('.btn-link')
      for (let i = 0; i < apiBtn.length; i++) {
        apiBtn[i].style.color = '#393e46'
      }
      const aTags = document.querySelectorAll('ul a')
      for (let i = 0; i < aTags.length; i++) {
        aTags[i].style.color = '#393e46'
      }
      const routerLinks = document.querySelectorAll('#nav .nav-link')
      for (let i = 0; i < routerLinks.length; i++) {
        routerLinks[i].style.color = '#393e46'
        // routerLinks[i].classList.remove('router-light')
        // routerLinks[i].classList.add('router-dark')
      }
    },
    recommendClear: function () {
      const context = {
        setToken: this.setToken()
      }
      this.$store.dispatch('recommendClear', context)
    },
  },
  computed: {
    recommendedMovies: function () {
      return this.$store.state.recommendedMovies
    },
    isBtnToggle: function () {
      return this.$store.state.isBtnToggle
    },
  },
  // default: 인기 영화 
  created: function () {
    if (localStorage.getItem('jwt')) {
      this.popularMovies()
      this.sendMovieList()
    } else {
      this.$router.push({name: 'Login'})
    }
    // 추천 영화 받아오기
    const context = {
      movie: null,
      setToken: this.setToken()
    }
    this.$store.dispatch('userLikeMovie', context)
    this.onMouseOut()
  },
  destroyed: function() {
    removeEventListener('scroll', this.infinteScroll)
    this.onMouseOut()
  },
}
</script>

<style>
  #columns{
    column-width: 200px;
    column-gap: 7px;
  }
  #columns figure{
    display: inline-block;
    border:1px solid rgba(0,0,0,0.2);
    margin:0;
    margin-bottom: 15px;
    padding:10px;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.5);;
  }
  #columns figure img{
    width:100%;
  }
  #columns figure figcaption{
    border-top:1px solid rgba(0,0,0,0.2);
    padding:10px;
    margin-top:11px;
  }
  .btn-link:focus {
    font-weight: bold;
    box-shadow: none;
  }
  .scroll-top {
    position: fixed;
    right: 20px;
    bottom: 20px;
    z-index: 100;
    background-color: #999;
    opacity: .8;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    border: none;
    color: #fff;
  }
  .scroll-top:hover {
    cursor: pointer;
  }
  ul {
    list-style: none;
  }
  /* a:hover {
    transition-property: color;
    transition-duration: 1s;
    transition-timing-function: ease-out;
    color: #fea82f;
  } */

  .background-transition {
    transition-property: background-color, color;
    transition-duration: 1s;
    transition-timing-function: ease-out;
  }
  /* .router-light {
    color: #eeeeee;
  }
  .router-dark {
    color: #393e46;
  } */
  .box-movie {
    width: 45%;
    /* height: 600px; */
    border-width: 0px;
    position: fixed;
  }
</style>