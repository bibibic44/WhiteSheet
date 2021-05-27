import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import VueMoment from 'vue-moment'
import moment from "moment";
import VueEllipseProgress from 'vue-ellipse-progress';

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')

moment.locale("ko");
Vue.use(VueMoment,  { moment });
Vue.use(VueEllipseProgress);