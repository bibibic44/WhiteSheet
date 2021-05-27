<template>
  <div>
    <div class="d-flex justify-content-end ">
    <button class="mb-4 me-5 btn btn-link reset-btn fs-6">
      <router-link class="nav-link create-color" :to="{ name: 'CreateReview' }" style="padding-right: 100px;">
        <span style="font-size: 10px; color: #bf9f71; margin-left: 20px; opacity: 0.7;">
        <i class="fas fa-pen fa-2x"></i>
        </span> Review
      </router-link>
    </button>
    </div>
    <div v-if="reviewList && reviewList.length">
      <div class="container">
        <section class="row row-cols-2">
          <ul>
            <li :id="`id-${review.id}`" v-for="(review, idx) in reviewList" :key="idx" 
            @mouseover="onMouseOverAll" @mouseout="onMouseOutAll"
            >
              <router-link :to="{ name: 'ReviewListDetail' }">
                <div @mouseover="onMouseOverElement(review)" @mouseout="onMouseOutElement(review)">
                  <p>#{{ review.id }}</p>
                  <h2 class="py-3 ps-4 d-flex justify-content-start text-wrap" @click="getReviews(review)">
                    {{ review.title }}
                  </h2>
                </div>
              </router-link>
            </li>
          </ul>
          <div class="row d-flex justify-content-center">
            <div class="box-text ms-5 mt-3"></div>
          </div>
        </section>
      </div>  
    </div>
    <div v-else>
      <p>리뷰가 없습니다.</p>
    </div>
  </div>
</template>

<script>
// import axios from 'axios'

export default {
  name: 'ReviewList',
  data: function () {
    return {
      reviews: null,
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
    getReviews: function (review) {
      const context = {
        review: review,
        setToken: this.setToken()
      }
      this.$store.dispatch('getReviews', context)
    },
    onMouseOverAll: function () {
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
      }
    },
    onMouseOutAll: function () {
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
      }
    },
    onMouseOverElement: function (review) {
      let reviewId = review.id
      let hSselectTag = document.querySelector(`#id-${reviewId} h2`)
      hSselectTag.classList.add('review-text-hover')
      let pSselectTag = document.querySelector(`#id-${reviewId} p`)
      pSselectTag.classList.add('review-text-hover')
      // 작성자를 받아온다.
      const context = {
        userPk: review.user,
        setToken: this.setToken()
      }
      this.$store.dispatch('getUsername', context)

      this.onDetailAdd(review)
    },
    onMouseOutElement: function (review) {
      let reviewId = review.id
      let hSselectTag = document.querySelector(`#id-${reviewId} h2`)
      hSselectTag.classList.remove('review-text-hover')
      let pSselectTag = document.querySelector(`#id-${reviewId} p`)
      pSselectTag.classList.remove('review-text-hover')
      this.onDetailRemove(review)
    },
    onDetailAdd: function (review) {
      let parentBox = document.querySelector('.box-text')
      let childDiv = document.createElement('div')
      let childId = `tmp-id-${review.id}`
      let childUsername = document.createElement('h3')
      childUsername.innerText = '작성자: ' + this.nowUsername
      let childContent = document.createElement('h4')
      childContent.innerText = review.content
      let childHorizon = document.createElement('hr')
      let childBr = document.createElement('br')
      let childDate = document.createElement('p')
      childDate.innerText = review.created_at
      childDate.classList.add('d-flex', 'justify-content-start')

      childDiv.append(childDate, childUsername, childHorizon, childBr, childContent)
      childDiv.setAttribute('id', childId)
      childDiv.setAttribute('style', 'color: #eeeeee;')

      parentBox.append(childDiv)
    },
    onDetailRemove: function (review) {
      let childId = `#tmp-id-${review.id}`
      let childDiv = document.querySelector(`${childId}`)
      childDiv.remove()
    },
  },
  computed: {
    reviewList: function () {
      return this.$store.state.reviews
    },
    nowUsername: function () {
      return this.$store.state.nowUsername
    },
  },
  created: function () {
    if (localStorage.getItem('jwt')) {
      this.getReviews()
    }
    else {
      this.$router.push({ name: 'Login' })
    }
    this.onMouseOutAll()
  },
  destroyed: function() {
    removeEventListener('scroll', this.infinteScroll)
    this.onMouseOutAll()
  },
}
</script>

<style scoped>
  .review-btn {
    margin-left: 10px;
  }
  ul {
    list-style: none;
  }
  .review-text-hover {
    transition-property: color;
    transition-duration: 1s;
    transition-timing-function: ease-out;
    opacity: 1;
    color: #fea82f;
  }
  .box-text {
    width: 30%;
    /* height: 600px; */
    border-width: 0px;
    position: fixed;
  }
  .create-color {
    font-size: 22px; 
    color: #bf9f71; 
  }
</style>