<template>
  <div>
    <h1 class="pb-4 my-3">Login</h1>
    <div class="login_id">
      <!-- <img class="logo" src="../assets/ssafy_logo.png"> -->
      <!-- <label for="username">사용자 이름: </label> -->
      <input type="text" id="username" v-model="credentials.username" @keyup.enter="login" placeholder="아이디 입력">
    </div>
    <div class="login_pw">
      <!-- <label for="password">비밀번호: </label> -->
      <input type="password" id="password" v-model="credentials.password" @keyup.enter="login" placeholder="비밀번호 입력">
    </div>
    <div class="login_button">
      <button @click="login">로그인 </button>
    </div>
    <p class="social_login my-3">
      <router-link :to="{ name: 'LoginGoogle' }">소셜로그인</router-link>
    </p>
  </div>
</template>

<script>
import axios from 'axios'

// const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'Login',
  data: function () {
    return {
      credentials: {
        username: null,
        password: null,
      }
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
    login: function () {
      axios({
        method: 'post',
        url: 'http://127.0.0.1:8000/accounts/api-token-auth/',
        data: this.credentials
      })
        .then(res => {
          // console.log(res)
          localStorage.setItem('jwt', res.data.token)
          // 유저 이름 받아오기
          this.$store.dispatch('accessUser', this.credentials.username)
          this.$emit('login')
          this.$router.push({ name: 'Home' })
        })
        .catch(err => {
          alert("로그인에 실패했습니다.")
          console.log(err)
        })
    }
  }
}
</script>

<style>
.logo{
  width:100px
}
.login_id input {
  width: 300px;
  height: 40px;
  padding-left: 20px;
  display: block;
  margin-bottom: 10px;
  margin-right: auto;
  margin-left: auto;
  border: 0px solid #fea82f;
  border-radius: 10px;
}

.login_pw input {
  width: 300px;
  height: 40px;
  padding-left: 20px;
  display: block;
  margin-bottom: 15px;
  margin-right: auto;
  margin-left: auto;
  border: 0px solid #fea82f;
  border-radius: 10px;
}

.login_button button{
  width: 320px;
  height: 40px;
  /* border: 1px solid skyblue;
  background: skyblue; */
  border: 0px solid #fea82f;
  background: #faf3f3;
  /* color: #fea82f; */
  cursor: pointer;
  border-radius: 10px;
}
/* .login_button:hover {
    color: #fea82f;
  } */

</style>