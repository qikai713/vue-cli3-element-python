<template>
    <div>
        <div style="float: left; width: 6% ;font-size: 15px;color: #3e3e3e">资产类型:</div>
        <el-checkbox-group v-model="search.checkList" style="margin-bottom: 10px; float: left; width: 94%">
            <el-checkbox @change="checkinlist" label="硬件"></el-checkbox>
            <!--<el-checkbox label="软件" disabled></el-checkbox>-->
            <el-checkbox @change="checkinlist" label="服务"></el-checkbox>
        </el-checkbox-group>
        <div style="margin-bottom: 10px;font-size: 15px; color: #3e3e3e">告警原因:</div>
        <div v-for="(item,index) in deterrentList"
             v-if="item.alert_label_a || item.alert_label_b || item.alert_label_c || item.alert_label_d || item.alert_label_e || item.alert_label_f"
             class="ben_border">
            <span class="s_border">威胁</span>
            <el-button :class="search.activeClass == '恶意代码' ? 'active_c':'active_h'" @click="yy_click('恶意代码')"
                       v-if="item.alert_label_a !== 0" plain>恶意代码({{item.alert_label_a}})
            </el-button>
            <el-button :class="search.activeClass == 'C&C' ? 'active_c':'active_h'" @click="yy_click('C&C')"
                       v-if="item.alert_label_b !== 0" plain>C&C({{item.alert_label_b}})
            </el-button>
            <el-button :class="search.activeClass == '网络入侵' ? 'active_c':'active_h'" @click="yy_click('网络入侵')"
                       v-if="item.alert_label_c !== 0" plain>网络入侵({{item.alert_label_c}})
            </el-button>
            <el-button :class="search.activeClass == '挂马' ? 'active_c':'active_h'" @click="yy_click('挂马')"
                       v-if="item.alert_label_d !== 0" plain>挂马({{item.alert_label_d}})
            </el-button>
            <el-button :class="search.activeClass == '钓鱼' ? 'active_c':'active_h'" @click="yy_click('钓鱼')"
                       v-if="item.alert_label_e !== 0" plain>钓鱼({{item.alert_label_e}})
            </el-button>
            <el-button :class="search.activeClass == '暗链' ? 'active_c':'active_h'" @click="yy_click('暗链')"
                       v-if="item.alert_label_f !== 0" plain>暗链({{item.alert_label_f}})
            </el-button>
        </div>
        <div v-for="(item,index) in deterrentList"
             v-if="item.alert_label_g || item.alert_label_h || item.alert_label_i || item.alert_label_j"
             class="ben_border">
            <span class="s_border">脆弱性</span>
            <el-button :class="search.activeClass == 'WEB漏洞' ? 'active_c':'active_h'" @click="yy_click('WEB漏洞')"
                       v-if="item.alert_label_g !== 0" plain>WEB漏洞({{item.alert_label_g}})
            </el-button>
            <el-button :class="search.activeClass == '漏洞' ? 'active_c':'active_h'" @click="yy_click('漏洞')"
                       v-if="item.alert_label_h !== 0" plain>漏洞({{item.alert_label_h}})
            </el-button>
            <el-button :class="search.activeClass == '系统漏洞' ? 'active_c':'active_h'" @click="yy_click('系统漏洞')"
                       v-if="item.alert_label_i !== 0" plain>系统漏洞({{item.alert_label_i}})
            </el-button>
            <el-button :class="search.activeClass == '弱口令' ? 'active_c':'active_h'" @click="yy_click('弱口令')"
                       v-if="item.alert_label_j !== 0" plain>弱口令({{item.alert_label_j}})
            </el-button>

        </div>
        <div v-for="(item,index) in deterrentList" v-if="item.alert_label_k || item.alert_label_l || item.alert_label_m"
             class="ben_border">
            <span class="s_border">可用性</span>
            <el-button :class="search.activeClass == 'HTTP未响应' ? 'active_c':'active_h'" @click="yy_click('HTTP未响应')"
                       v-if="item.alert_label_k !== 0" plain>
                HTTP未响应({{item.alert_label_k}})
            </el-button>
            <el-button :class="search.activeClass == 'DNS未响应' ? 'active_c':'active_h'" @click="yy_click('DNS未响应')"
                       v-if="item.alert_label_l !== 0" plain>
                DNS未响应({{item.alert_label_l}})
            </el-button>
            <el-button :class="search.activeClass == 'PING未响应' ? 'active_c':'active_h'" @click="yy_click('PING未响应')"
                       v-if="item.alert_label_m !== 0" plain>
                PING未响应({{item.alert_label_m}})
            </el-button>
        </div>
        <div v-for="(item,index) in deterrentList" v-if="item.alert_label_n || item.alert_label_o" class="ben_border">
            <span class="s_border">内容</span>
            <el-button :class="search.activeClass == '篡改' ? 'active_c':'active_h'" @click="yy_click('篡改')"
                       v-if="item.alert_label_n !== 0" plain>篡改({{item.alert_label_n}})
            </el-button>
            <el-button :class="search.activeClass == '敏感词' ? 'active_c':'active_h'" @click="yy_click('敏感词')"
                       v-if="item.alert_label_o !== 0" plain>敏感词({{item.alert_label_o}})
            </el-button>
        </div>
        <div v-for="(item,index) in deterrentList" v-if="item.alert_label_q || item.alert_label_p" class="ben_border_b">
            <span class="s_border">异常</span>
            <el-button :class="search.activeClass == '违规接入' ? 'active_c':'active_h'" @click="yy_click('违规接入')"
                       v-if="item.alert_label_p !== 0" plain>违规接入({{item.alert_label_p}})
            </el-button>
            <el-button :class="search.activeClass == '违规外联' ? 'active_c':'active_h'" @click="yy_click('违规外联')"
                       v-if="item.alert_label_q !== 0" plain>违规外联({{item.alert_label_q}})
            </el-button>
        </div>
        <el-card class="box-card" style="margin-top: 10px">
            <div>
                <el-button size="small" @click="commitClick" plain>提交通报</el-button>
                <el-button size="small" @click="endClick" plain>结束告警</el-button>
                <el-input
                        style="width: 20%; float: right"
                        v-model="search.inputSearch"
                        placeholder="请输入内容">
                    <i
                            class="el-icon-search
 el-input__icon"
                            slot="suffix"
                            @click="querySearch()">
                    </i>
                </el-input>
            </div>
            <el-table
                    stripe
                    @row-click="rowClick"
                    @filter-change="filterlevel"
                    v-loading="loading"
                    ref="filterTable"
                    :data="tableData.data"
                    @selection-change="handleSelectionChange"
                    @sort-change="timesort"
                    style="width: 100%">
                <el-table-column
                        type="selection"
                        width="40"
                        column-key="alert_id"
                >
                </el-table-column>
                <el-table-column
                        prop="new_time"
                        label="最后一次告警时间"
                        sortable="custom"
                        width="180"
                        column-key="alert_id"
                >
                </el-table-column>
                <el-table-column
                        prop="resource"
                        label="名称"
                        column-key="alert_id"
                        show-overflow-tooltip
                        width="180">
                </el-table-column>
                <el-table-column
                        prop="asset_name"
                        label="所属单位"
                        column-key="alert_id"
                        show-overflow-tooltip
                        width="180">
                </el-table-column>
                <el-table-column
                        column-key="alert_level"
                        prop="alert_level_pd"
                        label="告警等级"
                        width="180"
                        show-overflow-tooltip
                        :filters="[{ text: '轻危', value: '1' }, { text: '低危', value: '2' }, { text: '中危', value: '3' }, { text: '高危', value: '4' }, { text: '严重', value: '5' }]"
                        filter-placement="bottom-end">
                    @filter-change="filterlevel"
                </el-table-column>
                <el-table-column
                        column-key="alert_id"
                        prop="alert_label"
                        label="原因"
                        show-overflow-tooltip
                        width="180">
                </el-table-column>
                <el-table-column
                        column-key="res_state"
                        prop="res_state_pd"
                        label="处理状态"
                        width="180"
                        :filters="[{ text: '未处理', value: '1' }, { text: '已处理', value: '2' }, { text: '已完成', value: '3' }]"
                        filter-placement="bottom-end">
                    @filter-change="filterStuta"
                </el-table-column>
                <el-table-column
                        label="处理进度"
                        width="180">
                    <template slot-scope="scope">
                        <span>{{scope.row.fw_fz === null ? 0 : scope.row.fw_fz}}</span>/<span>{{scope.row.fw_fz === null ? 0 : scope.row.fw_fm}}</span>
                    </template>
                </el-table-column>
                <el-table-column
                        label="通报状态">
                    <template slot-scope="scope">
                        <span>{{scope.row.fw_fz === scope.row.fw_fm ? '已提交' : ( scope.row.fw_fz < scope.row.fw_fm ? '部分提交': '未提交')}}</span>
                    </template>
                </el-table-column>
            </el-table>
            <el-pagination
                    @size-change="handleSizeChange"
                    @current-change="handleCurrentChange"
                    :current-page="1"
                    :page-sizes="[20, 50, 100, 200]"
                    :page-size="20"
                    layout="total, sizes, prev, pager, next, jumper"
                    :total="total">
            </el-pagination>
        </el-card>
        <div v-if="$store.state.emergency.showPrise" class="operTable"
             style="width: 100%; height: 100%; background: #bdc1ca5e">
            <oper-table v-bind:style="$store.state.emergency.operStyle" :showData="operTableData"></oper-table>
        </div>
        <div v-if="$store.state.emergency.showPar" class="parTable"
             style="width: 100%; height: 100%; background: #bdc1ca5e">
            <par-table v-bind:style="$store.state.emergency.parStyle" :imageData="operTableData"></par-table>
        </div>
    </div>
</template>

<script>
    import {tableList, reasons, endelarm} from './service/getData'

    export default {
        data() {
            return {

                tableData: {},  // 列表信息
                total: 0,  // 列表信息
                deterrentList: [],  // 威胁
                fragilityList: [],  // 脆弱
                practicalList: [],  // 可用性
                contentList: [],  // 内容
                abnormalList: [],  // 异常
                loading: true,  //
                selectList: [],   // 多选数据
                operTableData: '',  // 传子组件
                search: {
                    level: [], // 等级筛选
                    status: [], // 状态筛选
                    activeClass: '全部',   // 按钮选择
                    sort: 'descending',  //  降序
                    inputSearch: '',  //  降序
                    dispose: [],  //  降序
                    checkList: ['硬件', '服务'],
                    page: {
                        pageSize: 20,
                        pageNumber: 1
                    }
                },  // 搜索条件
            }
        },
        mounted() {
            // 获取主列表信息
            tableList(this.search).then(res => {
                console.log(this.search.checkList, '=========================================================')
                this.tableData = res
                this.total = res.total
                console.log(res)
                this.loading = false
            })
            // 获取主列表信息
            reasons().then(res => {
                this.deterrentList = res.data
                this.loading = false
            })
        },
        methods: {
            querySearch() {
                console.log(this.search.inputSearch)
                tableList(this.search).then(res => {
                    if (res.error = 'false') {
                        this.$message({
                            showClose: true,
                            message: '查询成功',
                            type: 'success'
                        });
                        this.tableData = res
                        this.total = res.total
                        console.log(res)
                        this.loading = false
                        this.search.inputSearch = []
                    }
                })
            },
            checkinlist() {
                console.log(this.search)
                tableList(this.search).then(res => {
                    this.tableData = res
                    this.total = res.total
                    console.log(res)
                    this.loading = false
                })

                // let restaurants = this.restaurants;
                // let results = queryString ? restaurants.filter(this.createFilter(queryString)) : restaurants;
                // // 调用 callback 返回建议列表的数据
                // cb(results);l
            },
            yy_click(index) {
                let that = this
                console.log(this.search.activeClass)
                console.log(index)
                if (that.search.activeClass == index) {
                    this.search.activeClass = "全部"
                    tableList(this.search).then(res => {
                        this.tableData = res
                        this.total = res.total
                        this.loading = false
                    })
                } else {
                    this.search.activeClass = index;
                    tableList(this.search).then(res => {
                        this.tableData = res
                        this.total = res.total
                        this.loading = false
                    })
                }
            },
            handleSizeChange(val) {
                this.search.page.pageSize = val
                tableList(this.search).then(res => {
                    console.log(res)
                    this.tableData = res
                    this.total = res.total
                    this.loading = false
                })
                console.log(`每页 ${val} 条`);
            },

            commitClick() {
                if (this.$store.state.emergency.search.alert_id.length === 0) {
                    this.$message({
                        showClose: true,
                        message: '请选择提交信息',
                        type: 'warning'
                    });
                } else {
                    this.$store.dispatch('par_list')
                }
            },
            endClick() {
                if (this.$store.state.emergency.search.alert_id.length === 0) {
                    this.$message({
                        showClose: true,
                        message: '请选择提交信息',
                        type: 'warning'
                    });

                } else {
                    endelarm(this.$store.state.emergency.search.alert_id).then(res => {
                        console.log(res)
                        if (res.error === 'false') {
                            this.$message({
                                showClose: true,
                                message: '查询成功',
                                type: 'success'
                            });
                            tableList(this.search).then(res => {
                                this.tableData = res
                                this.total = res.total
                                this.loading = false
                            })
                        } else {
                            this.$message.error('错误信息：', res.warn);
                        }
                    })
                }
            },

            handleCurrentChange(val) {
                this.search.page.pageNumber = val
                console.log(val)
                tableList(this.search).then(res => {
                    console.log(res)
                    this.tableData = res
                    this.total = res.total
                    this.loading = false
                })
                console.log(`当前页: ${val}`);
            },

            // 告警等级帅选
            filterlevel(filters) {
                this.search.level = []
                console.log(filters.alert_level)
                if (filters.alert_level.length === 0) {
                    this.search.level = 0
                } else {
                    this.search.level = filters.alert_level
                    tableList(this.search).then(res => {
                        this.tableData = res
                        this.total = res.total
                        this.loading = false
                    })
                }
            },
            // 告警状态帅选
            filterStuta(filters) {
                console.log(filters.res_state)
                if (filters.res_state.length === 0) {
                    this.search.res_state = 0
                } else {
                    this.search.res_state = filters.res_state
                    tableList(this.search).then(res => {
                        this.tableData = res
                        this.total = res.total
                        this.loading = false
                    })
                }
            },

            // table 行点击
            rowClick(row, event, column) {
                console.log(row)
                console.log(event)
                console.log(column)
                this.operTableData = row
                if (row.class_name === '硬件') {
                    console.log(row.alert_label, '2222222222')
                    this.$store.state.emergency.search.type = '0'
                    if (row.alert_label === 'C&C通讯') {
                        this.$store.state.emergency.search.type_yj = 'CC'
                    } else {
                        this.$store.state.emergency.search.type_yj = row.alert_label
                    }
                } else {
                    this.$store.state.emergency.search.type = '1'
                }

                this.$store.state.emergency.search.id = row.alert_id
                this.$store.state.emergency.visable = true
                console.log(this.$store.state.emergency.search.id, '22132123123123')
                this.$store.dispatch('emergency_list')
            },
            handleSelectionChange(val) {
                this.$store.state.emergency.search.alert_id = []
                for (let i = 0; i < val.length; i++) {
                    this.$store.state.emergency.search.alert_id.push(val[i].alert_id)
                }
                console.log(this.$store.state.emergency.search.alert_id)
            },
            timesort(val) {
                this.search.sort = val.order
                tableList(this.search).then(res => {
                    this.tableData = res
                    this.loading = false
                })
            },
            handleSelect(item) {
                console.log(item);
            },
            handleIconClick(ev) {
                console.log(ev);
            }
        }
    }
</script>
<style>
    .active_c {
        background: #fff !important;
        border-color: #409EFF !important;
        color: #409EFF !important;
    }

    .active_h {
        background: #fff !important;
        border-color: #409EFF !important;
        color: #606266 !important;
    }

    .ben_border {
        overflow: hidden;
        border: 1px solid #dcdfe6;
        border-bottom: none
    }

    .s_border {
        display: inline-block;
        width: 80px;
        text-align: center;
        border-right: 1px solid #dcdfe6;
        padding: 10px;
        font-size: 14px;
    }

    .ben_border_b {
        border: 1px solid #dcdfe6;
        border-top: none
    }

    .ben_border button, .ben_border_b button {
        border: none !important;
    }

    .operTable {
        position: fixed;
        overflow: auto;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
        z-index: 100;
        -webkit-overflow-scrolling: touch;
        outline: 0;
        display: block;
    }

    .parTable {
        position: fixed;
        overflow: auto;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
        z-index: 200;
        -webkit-overflow-scrolling: touch;
        outline: 0;
        display: block;
    }

</style>