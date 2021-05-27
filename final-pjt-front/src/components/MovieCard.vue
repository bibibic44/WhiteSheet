<template>
  <!-- <div class="col mb-4">
    <div class="card" @click="userLikeMovie">
      <router-link :to="{ name: 'MovieCardDetail' }">
        <img v-if=movie.poster_path class="img-fluid" :src="`https://image.tmdb.org/t/p/w500` + movie.poster_path">
      </router-link>
      <div class="card-body">
        <h5 class="card-title">{{ movie.title }}</h5>
      </div>
    </div>
  </div> -->
  <li :id="`id-${movie.id}`" @mouseover="onMouseOver" @mouseout="onMouseOut">
    <router-link :to="{ name: 'MovieCardDetail' }">
      <p class="mb-1">#{{ movie.id }}</p>
      <h3 @click="userLikeMovie" class="pt-1 py-3 ps-4 pb-5 d-flex justify-content-start text-wrap">
        {{ movie.title }}
      </h3>
    </router-link>
  </li>
</template>
<script>
export default {
  name: 'MovieCard',
  props: {
    movie: {
      type: Object,
    },
  },
  methods: {
    onMouseOver: function () {
      let movieId = this.movie.id
      let hSelectTag = document.querySelector(`#id-${movieId} h3`)
      hSelectTag.classList.add('movie-text-hover')
      let pSelectTag = document.querySelector(`#id-${movieId} p`)
      pSelectTag.classList.add('movie-text-hover')
      this.onDetailAdd(this.movie)
    },
    onMouseOut: function () {
      let movieId = this.movie.id
      let hSelectTag = document.querySelector(`#id-${movieId} h3`)
      hSelectTag.classList.remove('movie-text-hover')
      let pSelectTag = document.querySelector(`#id-${movieId} p`)
      pSelectTag.classList.remove('movie-text-hover')
      this.onDetailRemove(this.movie)
    },
    onDetailAdd: function (movie) {
      let parentBox = document.querySelector('.box-movie')
      parentBox.classList.add('col')
      let childDiv = document.createElement('div')
      let childId = `tmp-id-${movie.id}`
      let childPoster = document.createElement('img')
      let childOverview = document.createElement('p')
      let childHorizon = document.createElement('hr')
      // let childDate = document.createElement('p')
      // childDate.classList.add('d-flex', 'justify-content-start')
      // childDate.innerText = movie.release_date
      if (movie.poster_path) {
        childPoster.setAttribute('src', `https://image.tmdb.org/t/p/w300${movie.poster_path}`)
        childDiv.append(childPoster)
      }
      if (movie.overview) {
        childOverview.innerText = movie.overview
      }
      else {
        childOverview.innerText = '등록된 줄거리가 없습니다.'
      }
      childDiv.append(childPoster, childHorizon, childOverview)
      childDiv.setAttribute('id', childId)
      childDiv.setAttribute('style', 'color: #eeeeee;')

      parentBox.append(childDiv)
    },
    onDetailRemove: function (movie) {
      let childId = `#tmp-id-${movie.id}`
      let childDiv = document.querySelector(`${childId}`)
      childDiv.remove()
    },
    setToken: function () {
      const token = localStorage.getItem('jwt')
      const config = {
        Authorization: `JWT ${token}`
      }
      return config
    },
    userLikeMovie: function () {
      const context = {
        movie: this.movie,
        setToken: this.setToken()
      }
      this.$store.dispatch('userLikeMovie', context)
    },
  }
}
</script>

<style>
  .movie-text-hover {
    transition-property: color;
    transition-duration: 1s;
    transition-timing-function: ease-out;
    opacity: 1;
    color: #fea82f;
  }
</style>