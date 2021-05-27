<template>
  <div id="app">
    <div id="nav" class="pt-2 pb-2 px-5">
      <span v-if="isLogin">
        <nav class="navbar navbar-expand navbar-light px-2">
          <span class="navbar-brand ps-4" id="navbar-brand">Hello, {{ accessUsername }}</span>
          <div class="container-fluid">
            <div class="collapse navbar-collapse d-flex justify-content-end" id="navbarNavAltMarkup">
              <div class="navbar-nav">
                <router-link class="nav-link pe-4" :to="{ name: 'Home' }">Home</router-link>
                <!-- 추천영화 드랍 다운 -->
                <button class="nav-link btn btn-link pe-3" @mouseover="recommenderToggle()">Movie Recommender</button>
                <router-link class="nav-link pe-4" :to="{ name: 'ReviewList' }">Review List</router-link>
                <!-- <router-link class="nav-link pe-4" :to="{ name: 'CreateReview' }">Create Review</router-link> -->
                <router-link class="nav-link pe-4" @click.native="logout" to="#">Logout</router-link>
              </div>
            </div>
          </div>
        </nav>
        <!-- 추천 영화 드랍다운 -->
        <div v-if="isBtnToggle" @mouseleave="recommenderToggleOut">
          <div v-if="recommendedMovies">
            <!-- <h3 class="pb-4 fw-bold">당신을 위한 추천 영화!</h3> -->
            <div class="row-cols-6 pt-4">
              <div v-for="(movie, idx) in recommendedMovies" :key="idx" class="row me-1 d-inline-flex">
                <div v-if=movie.poster_path>
                  <router-link :to="{ name: 'MovieCardDetail' }">
                    <img @click="userLikeMovie(movie)" class="img-fluid" :src="`https://image.tmdb.org/t/p/w500` + movie.poster_path">
                  </router-link>
                </div>
                <div v-else>
                  <p>{{ movie.title }}</p>
                </div>
              </div>
            </div>
            <div class="d-flex justify-content-end">
              <button class="mt-4 btn btn-link reset-btn fs-6 pe-5" @click="recommendClear" style="color: #bf9f71;">Reset</button>
            </div>
          </div>
            <span v-else class="pb-4 fw-bold">관심있는 영화를 눌러보세요</span>
          </div>
        <div v-else></div>

      </span>
      <span v-else>
        <router-link :to="{ name: 'Signup' }">Signup</router-link> |
        <router-link :to="{ name: 'Login' }">Login</router-link> 
      </span>
    </div>
    <router-view @login="isLogin=true"/>

  </div>
</template>


<script>
export default {
  name: 'App',
  data: function () {
    return {
      isLogin: false,
    }
  },
  methods: {
    setToken: function () {
      const token = localStorage.getItem('jwt')
      const config = {
        Authorization: `JWT ${token}`
      }
      return config
    },
    logout: function () {
      this.isLogin = false
      localStorage.removeItem('jwt')
      this.$router.push({ name: 'Login' })
      this.$store.dispatch('logoutRecommend')
      this.$store.state.isBtnToggle = false
    },
    userLikeMovie: function (movie) {
      const context = {
        movie: movie,
        setToken: this.setToken()
      }
      this.$store.dispatch('userLikeMovie', context)
    },
    recommenderToggle: function () {
      this.$store.dispatch('recommenderToggle')
      let btnTrue = document.querySelector('#nav button')
      if (this.isBtnToggle) {
        btnTrue.style.fontWeight = 'bold'
      }
      else {
        btnTrue.style.fontWeight = 'normal'
      }
    },
    recommenderToggleOut: function () {
      this.$store.dispatch('recommenderToggle')
      let btnTrue = document.querySelector('#nav button')
      if (!this.isBtnToggle) {
        btnTrue.style.fontWeight = 'normal'
      }
    },
    recommendClear: function () {
      const context = {
        setToken: this.setToken()
      }
      this.$store.dispatch('recommendClear', context)
    },
    // onMouseOver: function (num) {
    //   if (num == 1){
    //     let routerSselectTag = document.querySelector(`.review-list`)
    //     routerSselectTag.classList.add('route-hover')
    //   }
    //   else if (num == 2){
    //     let routerSselectTag = document.querySelector(`.create-review`)
    //     routerSselectTag.classList.add('route-hover')
    //   }
    //   else if (num == 3){
    //     let routerSselectTag = document.querySelector(`.logout-btn`)
    //     routerSselectTag.classList.add('route-hover')
    //   }
    //   else{
    //     let routerSselectTag = document.querySelector(`.home-btn`)
    //     routerSselectTag.classList.add('route-hover')
    //   }
        
    // },
    // onMouseOut: function (num) {
    //   if (num == 1){
    //     let routerSselectTag = document.querySelector(`.review-list`)
    //     routerSselectTag.classList.remove('route-hover')
    //   }
    //   else if (num == 2){
    //     let routerSselectTag = document.querySelector(`.create-review`)
    //     routerSselectTag.classList.remove('route-hover')
    //   }
    //   else if (num == 3){
    //     let routerSselectTag = document.querySelector(`.logout-btn`)
    //     routerSselectTag.classList.remove('route-hover')
    //   }
    //   else{
    //     let routerSselectTag = document.querySelector(`.home-btn`)
    //     routerSselectTag.classList.remove('route-hover')
    //   }
    // }
  },
  created: function () {
    const token = localStorage.getItem('jwt')
    if (token) {
      this.isLogin = true
    }
    // 추천 영화 받아오기
    const context = {
      movie: null,
      setToken: this.setToken()
    }
    this.$store.dispatch('userLikeMovie', context)
  },
  computed: {
    recommendedMovies: function () {
      return this.$store.state.recommendedMovies
    },
    isBtnToggle: function () {
      return this.$store.state.isBtnToggle
    },
    accessUsername: function () {
      return this.$store.state.accessUsername
    },
  },
}
</script>

<style>
#app {
  font-family: 'Noto Serif KR', serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: 393e46;
}

#nav {
  padding: 30px;
}

#nav a {
  /* font-weight: bold; */
  color: #2c3e50;
} 

#nav a:hover {
  /* color: #867ae9; */
  font-size: 103%;
  font-weight: bold;
}

#nav button:hover {
  font-size: 103%;
  font-weight: bold;
}

#nav a.router-link-exact-active {
  /* color: #7868e6;
  color: #fea82f; */
  /* color: #867ae9; */
  color: #2c3e50;
  font-size: 103%;
  font-weight: bold;
}
img {
  border-radius: 40px;
}

a {
  text-decoration: none;
  color: #393e46;
  text-align: left;
}
/* .route-hover {
  color: #867ae9;
  font-size: 103%;
} */
.reset-btn {
  text-decoration: none;
  color: #845460;
}
.reset-btn:hover {
  color: #766161;
  font-weight: bold;
}
#navbar-brand {
  color: whitesmoke;
  font-size: 20px;
}

</style>
