<template>
  <div class="container" style="padding: 30px 100px">
    <h2 class="text-start mb-5" style="color: #393e46;">{{ reviewId !== undefined ? 'Update Review' : 'Create Review'}}</h2>
    <div v-if="reviewId === undefined" class="input-group my-0">
      <div class="input-group">
        <span class="input-group-text non-border">영화</span>
        <input @click="selectedToggle" id="inputId" type="text" placeholder="영화제목을 입력하세요" @input="searchMovie" class="form-control m-0 non-border" autofocus>
        <div class="input-group d-flex justify-content-center" id="movieSelect-body">
          <div v-if="search_movies" id="movieSelect" class="mt-0">
            <div v-show="is_selected" v-for="(search_movie, idx) in search_movies" :key="idx" @click="selectMovie(search_movie)" :value="search_movie.title" class="mb-2 pe-5">
              {{ search_movie.title }}
            </div>
          </div>
          <div v-else class="d-flex align-items-center pe-5" style="color: #6c757d;">
            <p>해당하는 영화 제목이 없습니다</p>
          </div>
        </div>  
      </div>
    </div>
    <div class="input-group mb-3">
      <span class="input-group-text non-border">제목</span>
      <input type="text" placeholder="제목을 입력하세요" v-model.trim="title" class="form-control non-border"><br>
      <div></div>
    </div>
    <div class="input-group mt-3">
      <span class="input-group-text non-border">평점</span>
      <select class="form-select non-border" id="rankSelect" aria-label="Example select with button addon">
        <option selected>Choose...</option>
        <option value="10">10</option>
        <option value="9">9</option>
        <option value="8">8</option>
        <option value="7">7</option>
        <option value="6">6</option>
        <option value="5">5</option>
        <option value="4">4</option>
        <option value="3">3</option>
        <option value="2">2</option>
        <option value="1">1</option>
      </select>
    </div>
    <div class="input-group mt-3">
      <span class="input-group-text non-border">내용</span>
      <textarea  type="text" placeholder="내용을 입력하세요" v-model.trim="content" class="form-control p-3 non-border" style="height: 200px"></textarea>
    </div>
    <div class="mt-3">
    <button @click="reviewId !== undefined ? updateReview(reviewObject) : createReview()" class="btn btn-outline-secondary m-2">{{ reviewId !== undefined ? '수정' : '작성'}}</button> 
    <button @click="reviewId !== undefined ? updateCancel() : cancel()" class="btn btn-outline-secondary m-2">취소</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'CreateReview',
  props: {
    review_id: {
      type: Number,
    }
  },
  data: function () {
    return {
      reviewId: this.review_id,
      title: null,
      content: null,
      rank: null,
      movie: null,
      reviewObject: null,
      q: '',
      search_movies: null,
      is_selected: true,
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
    selectedToggle: function () {
      this.is_selected = true
    },
    cancel: function () {
      this.$router.push({ name: 'ReviewList' })
    },
    updateCancel: function () {
      this.$router.push({ name: 'ReviewListDetail' })
    },
    selectMovie: function (search_movie) {
      // select 옵션의 vlaue를 movie로 저장, 로컬 스토리지 저장 필요 X (수정 못하니까.)
      const movieSelect = document.querySelector('#movieSelect')
      if (movieSelect !== undefined) {
        this.movie = search_movie['title']
        console.log(this.movie)
      }
      const inputId = document.querySelector('#inputId')
      inputId.value = this.movie
      this.is_selected = false
    },
    createReview: function () {
      // select 옵션의 value를 rank로 저장
      const rankSelect = document.querySelector('#rankSelect')
      this.rank = rankSelect.options[rankSelect.selectedIndex].value
      // console.log(this.rank)
      // select 옵션을 로컬 스토리지에 저장해서 수정 시 바로 불러올 수 있도록 한다.
      localStorage.setItem(this.rank, this.rank)

      const reviewItem = {
        title: this.title,
        content: this.content,
        rank: this.rank,
        movie: this.movie,
      }
      if (reviewItem.title && reviewItem.content && reviewItem.rank && reviewItem.movie) {
        axios({
          method: 'post',
          url: 'http://127.0.0.1:8000/movies/reviews/',
          data: reviewItem,
          headers: this.setToken()
        })
          .then((res) => {
            console.log(res)
            const context = {
              review: res.data,
              userPk: res.data.user,
              setToken: this.setToken()
            }
            this.$store.dispatch('getReviews', context)
            this.$store.dispatch('getUsername', context)
            this.$router.push({ name: 'ReviewListDetail' })
            // this.$router.push({ name: 'ReviewList' })
          })
          .catch((err) => {
            console.log(err)
            alert('선택한 영화 정보가 없습니다.')
          })
      }
    },
    updateReview: function () {
      // select 옵션의 value를 rank로 저장
      const select = document.querySelector('#rankSelect')
      this.rank = select.options[select.selectedIndex].value
      // select 옵션을 로컬 스토리지에 저장해서 수정 시 바로 불러올 수 있도록 한다.
      localStorage.setItem(this.rank, this.rank)
      // console.log(localStorage.getItem(this.rank), this.rank)

      const reviewItem = {
        ...this.reviewObject,
        title: this.title,
        content: this.content,
        rank: this.rank,
      }
      console.log(reviewItem)
      axios({
        method: 'put',
        url: `http://127.0.0.1:8000/movies/reviews/${this.reviewId}/`,
        headers: this.setToken(),
        data: reviewItem,
      })
        .then((res) => {
          console.log(res)
          const context = {
            review: res.data,
            setToken: this.setToken()
          }
          this.$store.dispatch('getReviews', context)
          this.$router.push({ name: 'ReviewListDetail' })
      })
        .catch((err) => {
          console.log(err)
          alert('타인의 작성글을 보호해주세요 :-)')
          this.$router.push({ name: 'ReviewListDetail' })
        })
    },
    searchMovie: function (event) {
      this.q = event.target.value
      // console.log(this.movie)
      const query = {
        movie: this.q,
      }
      console.log(query)
      axios({
        method: 'post',
        url: 'http://127.0.0.1:8000/movies/movie_search/',
        data: query,
        headers: this.setToken(),
      })
        .then((res) => {
          console.log(res)
          this.search_movies = res.data
        })
    },
  },
  created: function () {
    if (localStorage.getItem('jwt')) {
      if (this.reviewId !== undefined) {
        axios({
          method: 'get',
          url: `http://127.0.0.1:8000/movies/reviews/detail/${this.reviewId}/`,
          headers: this.setToken()
        })
        .then((res) => {
          console.log(res)
          this.reviewObject = res.data
          this.title = res.data.title
          this.content = res.data.content
          this.movie = res.data.movie_title
          this.rank = res.data.rank
          // 이전에 선택한 rank를 localStorage에서 불러온다.
          console.log(localStorage.getItem(this.rank))
          const select = document.querySelector('#rankSelect')
          select.value = localStorage.getItem(this.rank)
        })
        .catch((err) => {
          console.log(err)
        })
      }
    } else {
      this.$router.push({name: 'Login'})
    }
  }
}
</script>

<style>
  #movieSelect-body {
    background-color: #faf3f3;
    padding: 10px;
    margin-left: 58px;
    margin-right: 1px;
  }
  .non-border {
    border: 0;
    border-radius: 5px;
  }
</style>