import Vue from 'vue'
import App from './Test1.vue'
import App2 from './Test2.vue'
Vue.config.productionTip = false


import Vuex from 'vuex'

Vue.use(Vuex)


new Vue({
    store:window.store,
    
    
    render: h => h(App),
}).$mount('#app')


