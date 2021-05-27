<template>
  <div id="LoginGoogle" class="d-flex justify-content-center m-5">
    <div><GoogleLogin :params="params" :renderParams="renderParams" :onSuccess="onSuccess"></GoogleLogin></div>
  </div>
</template>

<script>
import GoogleLogin from 'vue-google-login';

export default {
  name: 'LoginGoogle',
  data() {
    return {
      // client_id is the only required property but you can add several more params, full list down bellow on the Auth api section
      params: {
        client_id: "477507881845-7fps6lj6rfovbrpmrngigfissin9uekb.apps.googleusercontent.com"
      },
      // only needed if you want to render the button with the google ui
      renderParams: {
        width: 250,
        height: 50,
        longtitle: true
      }
    }
  },
  components: {
    GoogleLogin
  },
  methods: {
        onSuccess(googleUser) {
            // console.log(JSON.stringifty(googleUser));
            console.log(googleUser)
 
            // This only gets the user information: id, name, imageUrl and email
            console.log(JSON.stringifty(googleUser.getBasicProfile()));
        }
    }
}
</script>