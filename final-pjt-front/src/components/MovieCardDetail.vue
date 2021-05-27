<template>
  <div v-if="nowMovie" class="container px-5 mt-3 text-start" style="color: #393e46;">
    <span style="font-size: 48px; color: #c9c6bd; margin-left: 20px;">
      <i @click="backMovieList" class="fas fa-chevron-left mb-4"></i>
    </span>
    <!-- <button  class="btn btn-secondary m-1">뒤로</button> -->
    <div class="row">
      <section id="movie-side" class="col-4">
        <!-- {{ nowMovie }} -->
        <br>
        <img id="movie-poster" class="img-fluid mt-4" :src="`https://image.tmdb.org/t/p/w500` + nowMovie.poster_path">
      </section>
      <div id="movie-content" class="col-8 px-4">
        <hr class="my-hr3 mt-5">
        <div id="movie-content-head" class="mt-3">
          <span>#{{ nowMovie.id }}</span>
          <h2>{{ nowMovie.title }} ({{ nowMovie.release_date | moment('YYYY') }})</h2>
          <div class="d-flex justify-content-between px-1 mt-3 mb-0">
            <p>
              | <span class="my-text-bold">{{ nowMovie.adult !== false ? '성인' : '전체'}}</span> | 
              <span class="my-text-bold">{{ nowMovie.release_date | moment('YYYY.MM.DD') }}</span> |
            </p>
            <p><span class="my-text-bold">{{ nowMovie.release_date | moment("from", "now") }}</span> 개봉</p>
          </div>
        </div>
        <div id="movie-content-body">
          <p class="ps-3 py-3">{{ nowMovie.overview }}</p>
          <hr class="my-hr2">
        </div>
        <div id="movie-content-footer" class="row m-3">
          <div class="col d-flex justify-content-center mt-3">
            <vue-ellipse-progress size=70 color="#fea82f" :progress="`${nowMovie.vote_average * 10}`" :legend-value="`${nowMovie.vote_average}`" />
          </div>
          <div class="col mt-3">
            <p><span class="my-text-bold">평점</span> : {{ nowMovie.vote_average }}</p>
            <p><span class="my-text-bold">참여수</span> : {{ nowMovie.vote_count }}</p>
          </div>
          <div class="col mt-3">
            <p><span class="my-text-bold">총점</span> : {{ Math.ceil(nowMovie.vote_average * nowMovie.vote_count) }}</p>
            <p><span class="my-text-bold">인기도</span> : {{ Math.ceil(nowMovie.popularity) }}</p>
          </div>
        </div>
        <hr class="my-hr1">
      </div>
    </div>
    <br><br><br><br><br><br>
  </div>
</template>

<script>

export default {
  name: 'MovieCardDetail',
  methods: {
    backMovieList: function () {
      this.$router.push({ name: 'Home' })
    },
  },
  computed: {
    nowMovie: function () {
      return this.$store.state.nowMovie
    },
    recommendedMovies: function () {
      return this.$store.state.recommendedMovies
    },
  },
}
</script>

<style scoped>
  #movie-poster {
    width: 100%;
    height: auto;
    border-radius: 40px;
    transition: transform .3s; 
    cursor: pointer;
  }
  #movie-poster:hover {
    filter: grayscale(0);
    transform: scale(1.1);
    /* opacity: 0.8; */
  }
  i:hover {
    cursor: pointer;
  }
  .my-hr1 {
    border: 0;
    height: 1px;
    background: #787474;
    opacity: 0.7;
  }
  .my-hr2 {
    border: 0;
    height: 1px;
    background: #787474;
    opacity: 0.4;
  }
  .my-hr3 {
    border: 0;
    height: 0.5px;
    background: #787474;
    opacity: 0.1;
  }
  .my-text-bold {
    font-weight: bold;
  }


</style>