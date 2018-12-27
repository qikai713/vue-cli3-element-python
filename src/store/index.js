import Vue from 'vue'
import Vuex from 'vuex'

import emergency_store from './emergency_store'

Vue.use(Vuex)

export default new Vuex.Store({
    modules: {
        emergency: emergency_store
    }
})

