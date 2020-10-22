import Vue from 'vue'
import App from './RelImp.vue'
import VueNativeSock from 'vue-native-websocket'
import 'material-design-icons-iconfont/dist/material-design-icons.css' // Ensure you are using css-loader
import '@mdi/font/css/materialdesignicons.css'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'
import VueLodash from 'vue-lodash'
import lodash from 'lodash'
 
// name is optional
Vue.use(VueLodash, { name: 'custom' , lodash: lodash })
// index.js or main.js
import 'vuetify/dist/vuetify.min.css' // Ensure you are using css-loader

Vue.use(Vuetify)
Vue.config.productionTip = false

Vue.config.ignoredElements = [/^ion-/]
Vue.prototype.originalList = window.originalList;
Vue.prototype.error = window.error;

new Vue({
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


