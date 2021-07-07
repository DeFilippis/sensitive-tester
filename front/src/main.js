import Vue from 'vue'
import App from './App.vue'
import VueNativeSock from 'vue-native-websocket'
import 'material-design-icons-iconfont/dist/material-design-icons.css' // Ensure you are using css-loader
import '@mdi/font/css/materialdesignicons.css'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'
import VueLodash from 'vue-lodash'
import lodash from 'lodash'
import VueResizeText from 'vue-resize-text';
 
Vue.use(VueResizeText)

// name is optional
Vue.use(VueLodash, { name: 'custom' , lodash: lodash })
// index.js or main.js
import 'vuetify/dist/vuetify.min.css' // Ensure you are using css-loader

Vue.use(Vuetify)
Vue.config.productionTip = false
const ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
const ws_path = ws_scheme + '://' + window.location.host + window.socket_path;
Vue.use(VueNativeSock, ws_path, {

    format: 'json',
    reconnection: true, // (Boolean) whether to reconnect automatically (false)
    reconnectionAttempts: 5, // (Number) number of reconnection attempts before giving up (Infinity),
    reconnectionDelay: 3000,
});


window.vueOpinion = new Vue({
    vuetify: new Vuetify(
        {
            defaultAssets: {
                font: true,
                icons: 'mdi'
            },
            icons: {
                iconfont: 'mdi',
            }
        }
    )
    ,
    render: h => h(App),
}).$mount('#app')


