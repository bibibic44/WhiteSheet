<template>
  <div>
    <h1 class="pb-4 my-3">Signup</h1>
    <div class="signup_id">
      <!-- <label for="username">사용자 이름: </label> -->
      <input type="text" id="username" v-model="credentials.username" placeholder="아이디 입력">
    </div>
    <div class="signup_pw1">
      <!-- <label for="password">비밀번호: </label> -->
      <input type="password" id="password" v-model="credentials.password" placeholder="비밀번호 입력">
    </div>
    <div class="signup_pw2">
      <!-- <label for="passwordConfirmation">비밀번호 확인: </label> -->
      <input type="password" id="passwordConfirmation" v-model="credentials.passwordConfirmation" placeholder="비밀번호 확인">
    </div>
    <div class="signup_button my-3">
      <button @click="signup(credentials)">회원가입</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

// const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'Signup',
  data: function () {
    return {
      credentials: {
        username: null,
        password: null,
        passwordConfirmation: null,
      }
    }
  },
  methods: {
    signup: function () {
      // console.log(credientials)
      axios({
        method: 'post',
        url: 'http://127.0.0.1:8000/accounts/signup/',
        data: this.credentials,
      })
        .then(res => {
          console.log(res)
          this.$router.push({ name: 'Login'})
        })
        .catch(err => {
          alert("회원가입에 실패했습니다.")
          console.log(err)
        })
    }
  }
}
</script>

<style>
.logo{
  width:100px;
}
.signup_id input {
  width: 300px;
  height: 40px;
  padding-left: 20px;
  display: block;
  margin-bottom: 10px;
  margin-right: auto;
  margin-left: auto;
  border: 0px solid #845460;
  border-radius: 10px;
}

.signup_pw1 input {
  width: 300px;
  height: 40px;
  padding-left: 20px;
  display: block;
  margin-bottom: 10px;
  margin-right: auto;
  margin-left: auto;
  border: 0px solid #845460;
  border-radius: 10px;
}

.signup_pw2 input {
  width: 300px;
  height: 40px;
  padding-left: 20px;
  display: block;
  margin-bottom: 15px;
  margin-right: auto;
  margin-left: auto;
  border: 0px solid #845460;
  border-radius: 10px;
}

.signup_button button{
  width: 320px;
  height: 40px;
  /* border: 1px solid skyblue;
  background: skyblue; */
  border: 0px solid #845460;
  background: #faf3f3;
  /* color: #fff; */
  cursor: pointer;
}

</style>