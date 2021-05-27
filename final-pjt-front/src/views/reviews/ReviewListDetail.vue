<template>
  <div v-if="nowReview" class="container text-start px-5" style="color: #393e46;">
    <!-- <p>{{ nowReview }}</p> -->
    <div id="review-head">
      <div class="d-flex justify-content-between pe-3">
        <div>
          <span style="font-size: 48px; color: #c9c6bd; margin-left: 20px;">
            <i @click="backReviewList" class="fas fa-chevron-left"></i>
          </span>
        </div>
        <div class="pt-4">
          <span v-show="isReviewMe" @click="updateReview" style="font-size: 25px; color: #c9c6bd; margin-left: 20px;">
            <i class="far fa-edit"></i>
          </span>
          <span v-show="isReviewMe" @click="deleteReview(nowReview)" style="font-size: 25px; color: #c9c6bd; margin-left: 20px;">
            <i class="far fa-trash-alt"></i>
          </span>
        </div>
      </div>
      <br>
      <div class="d-flex justify-content-between pe-3 ps-2">
        <div class="me-5">
          <b>[{{ nowReview.movie_title }}] </b>
          <h2 class="mt-2"> {{ nowReview.title }}</h2>
        </div>
        <div class="ms-5 mb-0 d-flex justify-content-end align-items-end">
          <p> <span class="my-text-bold">평점</span> {{ nowReview.rank }}/10 </p>
        </div>
        <!-- <div class="my-box d-flex justify-content-center align-items-center">
          <div style="text-align: center;">
            점수
            <br>
            {{ nowReview.rank }} / 10
          </div>
        </div> -->
      </div>
      <hr class="my-hr3">
    </div>
    <div id="review-neck">
      <div class="d-flex justify-content-between px-3">
        <div>
          |  <span class="my-text-bold">작성자</span>  {{ nowUsername }}    | 
        </div>
        <div>
          |  <span class="my-text-bold">작성일</span> {{ nowReview.created_at | moment("from", "now") }} | 
          <span v-if="nowReview.created_at !== nowReview.updated_at ">
            <span class="my-text-bold">마지막 수정일</span> {{ nowReview.updated_at | moment("from", "now") }} |
          </span>
          <span class="my-text-bold">게시글 번호</span> {{ nowReview.id }}  | 
        </div>
      </div>
      <hr class="my-hr2">
    </div>
      <!-- <p class="text-start">
        {{ nowUsername }}님의 평점 : {{ nowReview.rank }}점 | 댓글 수 : <span v-if="nowReview">{{ review.comment_count }}개</span>
      </p> -->
    <div id="review-body" class="container p-3">
      <p>{{ nowReview.content }}</p>
      <br><br><br>
    </div>
    <hr class="my-hr1">
    <p class="ps-4 mb-0"> 
      <span class="my-text-bold">댓글 수</span> {{ review.comment_count }}
      <span v-if="review.comment_count" class="badge bg-secondary">New</span>
    </p>
    <div id="comment" class="container p-3">
      
      <div>
        <ul class="p-0">
          <li id="comment-body" v-for="(comment, idx) in comments" :key="idx" class="border border-0 rounded-3 mb-2 px-3 py-2" style="border-color: coral;">
            <div class="py-1">
              <p> | <span class="my-text-bold">작성자</span> {{ comment.username }} |</p>
            </div>
            <div>
              <p>{{ comment.content }}</p>
            </div>
            <div class="d-flex justify-content-between align-items-center pe-3">
              <span> {{ comment.created_at | moment('YYYY.MM.DD HH:mm:ss') }}</span>
              <span v-if="isCommentMe" @click="deletedComment(comment)" style="font-size: 20px; color: #c9c6bd; margin-left: 20px;">
                <i class="far fa-trash-alt"></i>
              </span>
            </div>
          </li>
        </ul>
      </div>
      <div id="comment-input" class="input-group mb-3 pt-3">
        <textarea type="text" style="border: 0; height: 100px; padding: 15px" class="form-control" placeholder="댓글을 작성해보세요 :D" aria-label="Recipient's username" aria-describedby="button-addon2" v-model.trim="comment_content">
        </textarea>
        <button @click="createComment" style="border: 0;" class="btn btn-outline-secondary border border-1" type="button" id="button-addon2">Comment</button>
      </div>
    </div>
    <br><br><br>
  </div>
  
</template>

<script>
import axios from 'axios'

export default {
  name: 'ReviewListDetail',
  data: function () {
    return {
      review: null,
      comments: null,
      comment_content: null,
      isReviewMe: false,
      isCommentMe: true,
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
    getReviewDetail: function () {
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/movies/reviews/detail/${this.nowReview.id}/`,
        headers: this.setToken()
      })
        .then((res) => {
          console.log(res)
          this.review = res.data
        })
        .catch((err) => {
          alert("리뷰가 없습니다.")
          console.log(err)
        })
    },

    deleteReview: function () {
      if (confirm('정말 삭제하시겠습니까?') == true) {
        axios({
          method: 'delete',
          url: `http://127.0.0.1:8000/movies/reviews/${this.nowReview.id}/`,
          headers: this.setToken()
        })
          .then((res) => {
            console.log(res)
            this.$router.push({ name: 'ReviewList' })
          })
          .catch((err) => {
            console.log(err)
            alert('타인의 작성글을 보호해주세요 :-)')
          })
      } else {
        return        
      }
    },

    updateReview: function () {
      axios({
          method: 'get',
          url: `http://127.0.0.1:8000/movies/reviews/${this.nowReview.id}`,
          headers: this.setToken()
        })
          .then((res) => {
            console.log(res)
            this.$router.push({ name: 'CreateReview', params: { review_id: this.nowReview.id } })
          })
          .catch((err) => {
            console.log(err)
            alert('타인의 작성글을 보호해주세요 :-)')
          })
      
    },

    backReviewList: function () {
      this.$router.push({ name: 'ReviewList' })
    },

    getComments: function () {
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/movies/reviews/detail/${this.nowReview.id}/comments/`,
        headers: this.setToken()
      })
        .then((res) => {
          console.log(res)
          this.comments = res.data
        })
        .catch((err) => {
          console.log(err)
        })
    },
    createComment: function () {
      const commentItem = {
        content: this.comment_content,
      }
      if (commentItem.content) {
        axios({
          method: 'post',
          url: `http://127.0.0.1:8000/movies/reviews/detail/${this.nowReview.id}/comments/`,
          data: commentItem,
          headers: this.setToken()
        })
          .then((res) => {
            console.log(res)
            this.getComments()
            this.getReviewDetail()
          })
          .catch((err) => {
            console.log(err)
          })
      }
      this.clearInput()
    },
    clearInput: function () {
      this.comment_content = ''
    },
    deletedComment: function (comment) {
      if (confirm('정말 삭제하시겠습니까?') == true) {
        axios({
          method: 'delete',
          url: `http://127.0.0.1:8000/movies/reviews/detail/${this.nowReview.id}/comments/${comment.id}`,
          headers: this.setToken()
        })
          .then((res) => {
            console.log(res)
            this.getComments()
            this.getReviewDetail()
          })
          .catch((err) => {
            console.log(err)
            alert('타인의 작성글을 보호해주세요 :-)')
          })
      } else {
        return;
      }
    },
    getUsername: function () {
      const userPk = this.nowReview.user
      // const userPk = this.comments.user
      const context = {
        userPk: userPk,
        setToken: this.setToken()
      }
      this.$store.dispatch('getUsername', context)
    },
    isReviewWriter: function () {
    // 리뷰 작성자가 자신인지 확인, updatedReview에 겹치는 코드 있음, 주의
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/movies/reviews/${this.nowReview.id}`,
        headers: this.setToken()
      })
        .then((res) => {
          console.log(res)
          this.isReviewMe = true
        })
        .catch((err) => {
          console.log(err)
          this.isReviewMe = false
        })
    },
    isCommentWriter: function (comment) {
      // 코멘트 작성자가 자신인지 확인
    axios({
      method: 'get',
      url: `http://127.0.0.1:8000/movies/reviews/detail/${this.nowReview.id}/comments/${comment.id}`,
      headers: this.setToken()
    })
      .then((res) => {
        console.log(res)
        this.isCommentMe = true
      })
      .catch((err) => {
        console.log(err)
        this.isCommentMe = false
      })
    }
  },
  computed: {
    nowReview: function () {
      return this.$store.state.nowReview
    },
    nowUsername: function () {
      return this.$store.state.nowUsername
    }
  },
  created: function () {
    if (localStorage.getItem('jwt')) {
      this.getReviewDetail()
      this.getComments()
      this.getUsername()
    } else {
      this.$router.push({name: 'Login'})
    }
    this.isReviewWriter()
  }
}
</script>

<style scoped>
  .comment-btn {
    margin-left: 10px;
  }
  .my-box { 
    border:1px solid; 
    border-radius: 20%;
    padding:10px; 
  }
  /* #comment{
    background-color: #FAF3F3;
  } */
  #comment-body{
    /* #E8E1E1 #EDE6E6 #F7F0F0*/
    background-color:#F0E9E9;
    opacity: 0.9;
  }
  /* #comment-input{
    background-color: whitesmoke;
  } */
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
    opacity: 0.2;
  }
  .my-text-bold {
    font-weight: bold;
  }
</style>