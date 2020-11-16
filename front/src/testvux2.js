import Vue from 'vue'
import App from './Test2'
Vue.config.productionTip = false
import Vuex from 'vuex'

Vue.use(Vuex)



new Vue({
    store:window.store,
    
    render: h => h(App),
}).$mount('#app2')


