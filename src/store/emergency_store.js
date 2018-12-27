import Vue from 'vue'
import Vuex from 'vuex'

import {operList, parlist} from '../service/getData'

Vue.use(Vuex)

export default {
    state: {
        data4: [],
        alert_merge_id: '',
        visable: true,
        operStyle: {
            float: 'right',
            // height: window.innerHeight + 'px',
            width: 950 + 'px',
            position: 'fixed',
            top: '0',
            bottom: '0',
            right: '0',

        },
        parStyle: {
            float: 'right',
            width: 950 + 'px',
            position: 'fixed',
            top: '0',
            bottom: '0',
            right: '0',

        },
        verStyle: {
            float: 'right',
            width: 950 + 'px',
            position: 'fixed',
            top: '0',
            bottom: '0',
            right: '0',
        },
        show: false,
        showPrise: false, // 詳情展示
        showPar: false, // 提交通报 主table
        showVer: false, // 验证
        showParT: false, // 提交通报 详情提交
        operList: '', // operList
        partableList: '', // partableList
        alert_id: [],
        gmlist: [], // 挂马
        dylist: [], // 钓鱼
        allist: [], // 恶意链接
        weblist: [], // web漏洞
        xtlist: [], // 系统漏洞
        rkllist: [], // 弱口令
        httplist: [], // HTTP未响应
        dnslist: [], // DNS未响应
        cglist: [], // 篡改
        mgclist: [], // 敏感词
        cclist: [], // C&C
        eylist: [], //恶意代码
        search: {
            id: '',
            alert_id: [], // 提交 多选数组
            type: '', //类型
            type_yj: '', //类型
        },
    },
    mutations: {
        emergency_visible(state) {
            state.visable = true
            state.operStyle.width = state.operStyle.width = 900 + 'px'
            state.showPrise = state.showPrise ? false : true;
            state.operList = ''
            state.gmlist = []
            state.cclist = []
            state.alert_id = []
            state.dylist = []
            state.allist = []
            state.weblist = []
            state.xtlist = []
            state.rkllist = []
            state.httplist = []
            state.dnslist = []
            state.cglist = []
            state.mgclist = []
            state.eylist = []

        },
        par_visible(state) {
            state.visable = true
            state.operStyle.width = state.operStyle.width = 900 + 'px'
            state.partableList = [],
                state.showPar = state.showPar ? false : true;
        },
        ver_visible(state) {
            state.visable = true
            state.operStyle.width = state.operStyle.width = 900 + 'px'
            state.showVer = state.showVer ? false : true;
        },
        big_visible(state) {
            state.visable = false
            state.operStyle.width = state.operStyle.width = 100 + '%'
        },
        small_visible(state) {
            state.visable = true
            state.operStyle.width = state.operStyle.width = 900 + 'px'
        },
        big_parvisible(state) {
            state.visable = false
            state.parStyle.width = state.parStyle.width = 100 + '%'
        },
        small_parvisible(state) {
            state.visable = true
            state.parStyle.width = state.parStyle.width = 900 + 'px'
        },
        big_vervisible(state) {
            state.visable = false
            state.parStyle.width = state.parStyle.width = 900 + 'px'
        },
        small_vervisible(state) {
            state.visable = true
            state.verStyle.width = state.verStyle.width = 900 + 'px'
        }
    },
    actions: {
        emergency_list({commit, state}) {//这里的context和我们使用的$store拥有相同的对象和方法
            commit('emergency_visible');
            operList(state.search).then(res => {
                state.operList = res
                if (state.search.type === '0') {
                    for (let i = 0; i < res.length; i++) {
                        if (res[i].alert_label === 'C&C通讯') {
                            state.cclist.push(res[i])
                        } else if (res[i].alert_label === '恶意代码网络传输') {
                            state.eylist.push(res[i])
                        }
                    }
                } else {
                    state.alert_id = res[0].alert_id

                    for (let i = 0; i < res.length; i++) {
                        if (res[i].alert_reson === '系统漏洞') {
                            state.xtlist.push(res[i])
                        } else if (res[i].alert_reson === '挂马') {
                            state.gmlist.push(res[i])
                        } else if (res[i].alert_reson === '钓鱼') {
                            state.dylist.push(res[i])
                        } else if (res[i].alert_reson === '暗链') {
                            state.allist.push(res[i])
                        } else if (res[i].alert_reson === 'WEB漏洞') {
                            state.weblist.push(res[i])
                        } else if (res[i].alert_reson === '弱口令') {
                            state.rkllist.push(res[i])
                        } else if (res[i].alert_reson === 'HTTP未响应') {
                            state.httplist.push(res[i])
                        } else if (res[i].alert_reson === 'DNS未响应') {
                            state.dnslist.push(res[i])
                        } else if (res[i].alert_reson === '篡改') {
                            state.cglist.push(res[i])
                        } else if (res[i].alert_reson === '敏感词') {
                            state.mgclist.push(res[i])
                        }
                    }
                }
            })
        },
        emergency_lists({commit, state}) {//这里的context和我们使用的$store拥有相同的对象和方法
            state.operList = ''
            state.gmlist = []
            state.alert_id = []
            state.dylist = []
            state.allist = []
            state.weblist = []
            state.xtlist = []
            state.rkllist = []
            state.httplist = []
            state.dnslist = []
            state.cglist = []
            state.mgclist = []
            operList(state.search).then(res => {
                state.operList = res
                state.alert_id = res[0].alert_id
                if (state.search.type === '0') {
                    console.log('77777777777777777777')
                } else {
                    for (let i = 0; i < res.length; i++) {
                        if (res[i].alert_reson === '系统漏洞') {
                            state.xtlist.push(res[i])
                        } else if (res[i].alert_reson === '挂马') {
                            state.gmlist.push(res[i])
                        } else if (res[i].alert_reson === '钓鱼') {
                            state.dylist.push(res[i])
                        } else if (res[i].alert_reson === '暗链') {
                            state.allist.push(res[i])
                        } else if (res[i].alert_reson === 'WEB漏洞') {
                            state.weblist.push(res[i])
                        } else if (res[i].alert_reson === '弱口令') {
                            state.rkllist.push(res[i])
                        } else if (res[i].alert_reson === 'HTTP未响应') {
                            state.httplist.push(res[i])
                        } else if (res[i].alert_reson === 'DNS未响应') {
                            state.dnslist.push(res[i])
                        } else if (res[i].alert_reson === '篡改') {
                            state.cglist.push(res[i])
                        } else if (res[i].alert_reson === '敏感词') {
                            state.mgclist.push(res[i])
                        }
                    }
                }
            })
        },

        par_list({commit, state}) {//这里的context和我们使用的$store拥有相同的对象和方法
            commit('par_visible');
            parlist(state.search).then(res => {
                console.log(res, '333333333')
                state.partableList = res
                let list = res
                console.log(list, 'parlistparlistparlist')
                let map = [], dest = [];
                for (let i = 0; i < list.length; i++) {
                    let ai = list[i];
                    if (map.indexOf(ai.asset_name) < 0) {
                        dest.push({
                            id: ai.asset_name,
                            data: [ai]
                        });
                        console.log(map)
                        map.push(ai.asset_name);
                    } else {
                        for (let j = 0; j < dest.length; j++) {
                            let dj = dest[j];
                            if (dj.id == ai.asset_name) {
                                dj.data.push(ai);
                                break;
                            }
                        }
                    }
                }
                console.log(dest)
                for (let i = 0; i < dest.length; i++) {
                    let ai = dest[i];
                    ai.children = []
                    for (let z in  ai.data) {
                        if (ai.children.length === 0) {
                            ai.children.push({
                                id: ai.data[z].website,
                                children: [ai.data[z]]
                            })
                        } else {
                            for (let j in ai.children) {
                                if (ai.children[j].id == ai.data[z].website) {
                                    ai.children[j].children.push(ai.data[z]);
                                    break;
                                } else {
                                    ai.children.push({
                                        id: ai.data[z].website,
                                        children: [ai.data[z]]
                                    })
                                }
                            }
                        }
                    }
                }
                state.data4 = JSON.parse(JSON.stringify(dest))
            })
        },
    }
}
