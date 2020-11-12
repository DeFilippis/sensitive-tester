import Vue from 'vue'
import App from './Progress.vue'


Vue.config.productionTip = false


window.vueProgress = new Vue({
    data() {
        return {
            progressValue: window.progressValue,
            eventListenerValue: '',
        }
    },
    render: function(h) {return h(App,{props: {progressValue:this.progressValue}})},
}).$mount('#progress')


