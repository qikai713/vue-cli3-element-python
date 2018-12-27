import Vue from 'vue'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import App from './App.vue'
import router from './router'
import store from './store/index'
import axios from './axios'
import elecomopens from './components/elecompoents/index'
import htmlToPdf from './utils/htmlToPdf'

Vue.use(elecomopens)
Vue.use(ElementUI);
Vue.use(htmlToPdf)
Vue.config.productionTip = false
Vue.prototype.$axios = axios;

new Vue({
    router,
    store,
    axios,
    render: h => h(App)
}).$mount('#app')