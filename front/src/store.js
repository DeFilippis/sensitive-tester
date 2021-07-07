import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

window.store = new Vuex.Store({
    state: {
        count: 11
    },
    mutations: {
        increment(state) {
            console.debug('smthin happens at increemant')
            state.count++
        }
    }
})
export default store;