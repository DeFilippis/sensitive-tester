import Vue from "vue";
import App from "./DistributionApp.vue";
import HighchartsVue from "highcharts-vue";
import VueNativeSock from 'vue-native-websocket'
Vue.config.productionTip = false;
Vue.use(HighchartsVue);

import Vuetify from "vuetify";

Vue.use(Vuetify);

import "vuetify/dist/vuetify.min.css";
const ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
const ws_path = ws_scheme + '://' + window.location.host + window.socket_path;
console.debug("WHAT", ws_path)
Vue.use(VueNativeSock, ws_path, {

    format: 'json',
    reconnection: true, // (Boolean) whether to reconnect automatically (false)
    reconnectionAttempts: 5, // (Number) number of reconnection attempts before giving up (Infinity),
    reconnectionDelay: 3000,
});


new Vue({
  vuetify: new Vuetify({ icons: { iconfont: "mdi" } }),

  render: (h) => h(App)
}).$mount("#app");
