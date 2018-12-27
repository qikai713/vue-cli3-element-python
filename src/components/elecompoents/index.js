import ParTable from './par-table'
import OperTable from './oper-table'
import parVerify from './par-verify'

export default {
    install: (Vue) => {
        Vue.component('par-table', ParTable),
        Vue.component('oper-table', OperTable)
        Vue.component('par-verify', parVerify)
    }
}