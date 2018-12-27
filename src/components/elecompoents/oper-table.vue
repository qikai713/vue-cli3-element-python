<template>
    <el-container class="oper-table">
        <el-header class="operHeader">
            <el-card class="box-card operHeader">
                <div slot="header" class="cardBorder">
                    <span>{{showData.resource}}告警详情</span>
                    <el-button @click="$store.commit('emergency_visible')"
                               style="float: right; padding: 3px 0; color: aliceblue" type="text"><i
                            class="el-icon-close"></i>
                    </el-button>
                    <el-button v-if="$store.state.emergency.visable === true" @click="$store.commit('big_visible')"
                               style="float: right; padding: 3px 0; color: aliceblue" type="text"><i
                            class="el-icon-plus"></i>
                    </el-button>
                    <el-button v-if="$store.state.emergency.visable === false" @click="$store.commit('small_visible')"
                               style="float: right; padding: 3px 0; color: aliceblue" type="text"><i
                            class="el-icon-minus"></i>
                    </el-button>

                </div>
                <div style="font-size: 12px;" class="">
                    <span>最后一次告警时间:&nbsp;&nbsp;&nbsp;{{showData.new_time}}</span>&nbsp;&nbsp&nbsp;&nbsp;<span>等级: {{showData.alert_level_pd}}</span>&nbsp;&nbsp;&nbsp;&nbsp;<span>处理状态:&nbsp;&nbsp;{{showData.res_state_pd}}</span>
                    <button @click="getPdf('#pdfDom')" style="float: right">导出</button>
                </div>
            </el-card>
        </el-header>
        <el-main id="pdfDom">
            <el-row class="elrow" style="font-size: 14px;">
                <el-col style="border-bottom: 1px solid #ccc;padding-bottom: 10px;margin-bottom: 10px;">告警资产</el-col>
                <el-col class="elcol" :span="7">
                    <div>资产标识： {{showData.uuid}}</div>
                </el-col>
                <el-col class="elcol" :span="5">
                    <div class="">保护等级：{{showData.asset_level }}</div>
                </el-col>
                <el-col class="elcol" :span="6">
                    <div class="">所属单位：{{showData.asset_name}}</div>
                </el-col>
                <el-col class="elcol" :span="6">
                    <div class="">责任人：{{showData.in_charge}}</div>
                </el-col>
                <el-col class="elcol" :span="7">
                    <div>网站标题： {{showData.resource}}</div>
                </el-col>
                <el-col class="elcol" :span="5">
                    <div class="">URL：{{showData.uuid}}</div>
                </el-col>
                <el-col class="elcol" :span="6">
                    <div class="">域名：{{showData.domain}}</div>
                </el-col>
                <el-col class="elcol" :span="6">
                    <div class="">资产类型：{{showData.class_name}}</div>
                </el-col>
            </el-row>
            <el-tabs v-if="showData.class_name == '服务'" type="card" @tab-click="handleClick">
                <el-tab-pane v-if="$store.state.emergency.gmlist.length > 0" label="挂马">
                    <el-select v-model="selectvalue" placeholder="标记为" @change="selectChange">
                        <el-option
                                key="1"
                                label="已提交"
                                value='1'>
                        </el-option>
                        <el-option
                                key="2"
                                label="未提交"
                                value='2'>
                        </el-option>
                    </el-select>
                    <el-button @click="handNotification" style=" margin-left: 10px">提交通报</el-button>
                    <el-table
                            @selection-change="handleSelectionChange"
                            @select="selectionChange"
                            @select-all="selectall"
                            :data="$store.state.emergency.gmlist"
                            ref="filterTable"
                            @row-click="rowClick"
                            style="width: 100%"
                            max-height="250">
                        <el-table-column
                                type="selection"
                                width="40"
                                column-key="alert_merge_id">
                        </el-table-column>
                        <el-table-column
                                column-key="alert_merge_id"
                                prop="new_time"
                                label="最后一次发现时间"
                                width="150">
                        </el-table-column>
                        <el-table-column
                                column-key="alert_merge_id"
                                prop="website"
                                label="问题页面"
                                width="120">
                        </el-table-column>
                        <el-table-column
                                prop="website"
                                label="持续时间"
                                width="120">
                        </el-table-column>
                        <el-table-column
                                prop="is_notice_flag_db"
                                label="通报状态"
                                width="150">
                        </el-table-column>
                        <el-table-column
                                prop="sign_result"
                                label="标记结果"
                                width="120">
                        </el-table-column>
                        <el-table-column
                                fixed="right"
                                label="操作"
                                width="120">
                            <template slot-scope="scope">
                                <el-button @click="verificationClick(scope.row)" type="text" size="small">验证</el-button>
                                <el-dropdown style="float: right" :hide-on-click="false">
                                    <el-button type="text" size="small">标记为</el-button>
                                    <el-dropdown-menu slot="dropdown">
                                        <el-dropdown-item @click.native="submitClick(scope.row,1)">已提交</el-dropdown-item>
                                        <el-dropdown-item @click.native="submitClick(scope.row,2)">未提交</el-dropdown-item>
                                    </el-dropdown-menu>
                                </el-dropdown>
                            </template>
                        </el-table-column>
                    </el-table>
                </el-tab-pane>
                <el-tab-pane v-if="$store.state.emergency.xtlist.length > 0" label="系統漏洞">
                    <el-select v-model="selectvalue" placeholder="标记为" @change="selectChange">
                        <el-option
                                key="1"
                                label="已提交"
                                value="1">
                        </el-option>
                        <el-option
                                key="2"
                                label="未提交"
                                value="2">
                        </el-option>
                    </el-select>
                    <el-button @click="handNotification" style=" margin-left: 10px">提交通报</el-button>
                    <el-table
                            @selection-change="handleSelectionChange"
                            @select="selectionChange"
                            :data="$store.state.emergency.xtlist"
                            ref="filterTable"
                            @row-click="rowClick"
                            style="width: 100%"
                            max-height="250">
                        <el-table-column
                                type="selection"
                                width="40"
                                column-key="alert_merge_id">
                        </el-table-column>
                        <el-table-column
                                column-key="alert_merge_id"
                                prop="new_time"
                                label="最后一次发现时间"
                                width="150">
                        </el-table-column>
                        <el-table-column
                                column-key="alert_merge_id"
                                prop="website"
                                label="问题页面"
                                width="120">
                        </el-table-column>
                        <el-table-column
                                prop="loop_name"
                                label="漏洞编号"
                                width="120">
                        </el-table-column>
                        <el-table-column
                                prop="loop_level"
                                label="漏洞级别"
                                width="120">
                        </el-table-column>
                        <el-table-column
                                prop="is_notice_flag_db"
                                label="通报状态"
                                width="150">
                        </el-table-column>
                        <el-table-column
                                prop="sign_result"
                                label="标记结果"
                                width="120">
                        </el-table-column>
                        <el-table-column
                                fixed="right"
                                label="操作"
                                width="120">
                            <template slot-scope="scope">
                                <el-button @click="verificationClick(scope.row)" type="text" size="small">验证</el-button>
                                <el-dropdown style="float: right" :hide-on-click="false">
                                    <el-button type="text" size="small">标记为</el-button>
                                    <el-dropdown-menu slot="dropdown">
                                        <el-dropdown-item @click.native="submitClick(scope.row,1)">已提交</el-dropdown-item>
                                        <el-dropdown-item @click.native="submitClick(scope.row,2)">未提交</el-dropdown-item>
                                    </el-dropdown-menu>
                                </el-dropdown>
                            </template>
                        </el-table-column>
                    </el-table>
                </el-tab-pane>
                <el-tab-pane v-if="$store.state.emergency.dylist.length > 0" label="钓鱼">
                    <el-select v-model="selectvalue" placeholder="标记为" @change="selectChange">
                        <el-option
                                key="1"
                                label="已提交"
                                value="1">
                        </el-option>
                        <el-option
                                key="2"
                                label="未提交"
                                value="2">
                        </el-option>
                    </el-select>
                    <el-button @click="handNotification" style=" margin-left: 10px">提交通报</el-button>
                    <el-table
                            @selection-change="handleSelectionChange"
                            @select="selectionChange"
                            :data="$store.state.emergency.dylist"
                            ref="filterTable"
                            @row-click="rowClick"
                            style="width: 100%"
                            max-height="250">
                        <el-table-column
                                type="selection"
                                width="40"
                                column-key="alert_merge_id">
                        </el-table-column>
                        <el-table-column
                                column-key="alert_merge_id"
                                prop="new_time"
                                label="最后一次发现时间"
                                width="150">
                        </el-table-column>
                        <el-table-column
                                column-key="alert_merge_id"
                                prop="website"
                                label="问题页面"
                                width="120">
                        </el-table-column>
                        <el-table-column
                                prop="website"
                                label="持续时间"
                                width="120">
                        </el-table-column>
                        <el-table-column
                                prop="virus_url"
                                label="钓鱼网站"
                                width="120">
                        </el-table-column>
                        <el-table-column
                                prop="is_notice_flag_db"
                                label="通报状态"
                                :filters="[{ text: '已处理', value: '3' }, { text: '未处理', value: '1' }]"
                                :filter-method="filterTag"
                                filter-placement="bottom-end">
                            width="150">
                        </el-table-column>
                        <el-table-column
                                prop="sign_result"
                                label="标记结果"
                                width="120">
                        </el-table-column>
                        <el-table-column
                                fixed="right"
                                label="操作"
                                width="120">
                            <template slot-scope="scope">
                                <el-button @click="verificationClick(scope.row)" type="text" size="small">验证</el-button>
                                <el-dropdown style="float: right" :hide-on-click="false">
                                    <el-button type="text" size="small">标记为</el-button>
                                    <el-dropdown-menu slot="dropdown">
                                        <el-dropdown-item @click.native="submitClick(scope.row,1)">已提交</el-dropdown-item>
                                        <el-dropdown-item @click.native="submitClick(scope.row,2)">未提交</el-dropdown-item>
                                    </el-dropdown-menu>
                                </el-dropdown>
                            </template>
                        </el-table-column>
                    </el-table>
                </el-tab-pane>
                <el-tab-pane v-if="$store.state.emergency.allist.length > 0" label="暗链">
                    <el-select v-model="selectvalue" placeholder="标记为" @change="selectChange">
                        <el-option
                                key="1"
                                label="已提交"
                                value="1">
                        </el-option>
                        <el-option
                                key="2"
                                label="未提交"
                                value="2">
                        </el-option>
                    </el-select>
                    <el-button @click="handNotification" style=" margin-left: 10px">提交通报</el-button>
                    <el-table
                            @selection-change="handleSelectionChange"
                            @select="selectionChange"
                            :data="$store.state.emergency.allist"
                            ref="filterTable"
                            @row-click="rowClick"
                            style="width: 100%"
                            max-height="250">
                        <el-table-column
                                type="selection"
                                width="40"
                                column-key="alert_merge_id">
                        </el-table-column>
                        <el-table-column
                                column-key="alert_merge_id"
                                prop="new_time"
                                label="最后一次发现时间"
                                width="150">
                        </el-table-column>
                        <el-table-column
                                column-key="alert_merge_id"
                                prop="website"
                                label="问题页面"
                                width="120">
                        </el-table-column>
                        <el-table-column
                                prop="website"
                                label="持续时间"
                                width="120">
                        </el-table-column>
                        <el-table-column
                                prop="virus_url"
                                label="暗链网站"
                                width="120">
                        </el-table-column>
                        <el-table-column
                                prop="is_notice_flag_db"
                                label="通报状态"
                                width="120">
                        </el-table-column>
                        <el-table-column
                                prop="sign_result"
                                label="标记结果"
                                width="120">
                        </el-table-column>
                        <el-table-column
                                fixed="right"
                                label="操作"
                                width="120">
                            <template slot-scope="scope">
                                <el-button @click="verificationClick(scope.row)" type="text" size="small">验证</el-button>
                                <el-dropdown style="float: right" :hide-on-click="false">
                                    <el-button type="text" size="small">标记为</el-button>
                                    <el-dropdown-menu slot="dropdown">
                                        <el-dropdown-item @click.native="submitClick(scope.row,1)">已提交</el-dropdown-item>
                                        <el-dropdown-item @click.native="submitClick(scope.row,2)">未提交</el-dropdown-item>
                                    </el-dropdown-menu>
                                </el-dropdown>
                            </template>
                        </el-table-column>
                    </el-table>
                </el-tab-pane>
                <el-tab-pane v-if="$store.state.emergency.weblist.length > 0" label="WEB漏洞">
                    <el-select v-model="selectvalue" placeholder="标记为" @change="selectChange">
                        <el-option
                                key="1"
                                label="已提交"
                                value="1">
                        </el-option>
                        <el-option
                                key="2"
                                label="未提交"
                                value="2">
                        </el-option>
                    </el-select>
                    <el-button @click="handNotification" style=" margin-left: 10px">提交通报</el-button>
                    <el-table
                            @selection-change="handleSelectionChange"
                            @select="selectionChange"
                            :data="$store.state.emergency.weblist"
                            ref="filterTable"
                            @row-click="rowClick"
                            style="width: 100%"
                            max-height="250">
                        <el-table-column
                                type="selection"
                                width="40"
                                column-key="alert_merge_id">
                        </el-table-column>
                        <el-table-column
                                column-key="alert_merge_id"
                                prop="new_time"
                                label="最后一次发现时间"
                                width="150">
                        </el-table-column>
                        <el-table-column
                                column-key="alert_merge_id"
                                prop="website"
                                label="问题页面"
                                width="120">
                        </el-table-column>
                        <el-table-column
                                prop="website"
                                label="持续时间"
                                width="120">
                        </el-table-column>
                        <el-table-column
                                prop="loop_name"
                                label="漏洞名称"
                                width="120">
                        </el-table-column>
                        <el-table-column
                                prop="loop_level"
                                label="漏洞级别"
                                width="120">
                        </el-table-column>
                        <el-table-column
                                prop="is_notice_flag_db"
                                label="通报状态"
                                :filters="[{ text: '已处理', value: '3' }, { text: '未处理', value: '1' }]"
                                :filter-method="filterTag"
                                filter-placement="bottom-end">
                            width="150">
                        </el-table-column>
                        <el-table-column
                                prop="sign_result"
                                label="标记结果"
                                width="120">
                        </el-table-column>
                        <el-table-column
                                fixed="right"
                                label="操作"
                                width="120">
                            <template slot-scope="scope">
                                <el-button @click="verificationClick(scope.row)" type="text" size="small">验证</el-button>
                                <el-dropdown style="float: right" :hide-on-click="false">
                                    <el-button type="text" size="small">标记为</el-button>
                                    <el-dropdown-menu slot="dropdown">
                                        <el-dropdown-item @click="submitClick(scope.row)">已提交</el-dropdown-item>
                                        <el-dropdown-item>未提交</el-dropdown-item>
                                    </el-dropdown-menu>
                                </el-dropdown>

                            </template>
                        </el-table-column>
                    </el-table>
                </el-tab-pane>
                <el-tab-pane v-if="$store.state.emergency.rkllist.length > 0" label="弱口令">
                    <el-select v-model="selectvalue" placeholder="标记为" @change="selectChange">
                        <el-option
                                key="1"
                                label="已提交"
                                value="1">
                        </el-option>
                        <el-option
                                key="2"
                                label="未提交"
                                value="2">
                        </el-option>
                    </el-select>
                    <el-button @click="handNotification" style=" margin-left: 10px">提交通报</el-button>
                    <el-table
                            @selection-change="handleSelectionChange"
                            @select="selectionChange"
                            :data="$store.state.emergency.rkllist"
                            ref="filterTable"
                            @row-click="rowClick"
                            style="width: 100%"
                            max-height="250">
                        <el-table-column
                                type="selection"
                                width="40"
                                column-key="alert_merge_id">
                        </el-table-column>
                        <el-table-column
                                column-key="alert_merge_id"
                                prop="new_time"
                                label="最后一次发现时间"
                                width="150">
                        </el-table-column>
                        <el-table-column
                                column-key="crack_host_ip"
                                prop="website"
                                label="主机"
                                width="120">
                        </el-table-column>
                        <el-table-column
                                prop="service"
                                label="服务"
                                width="120">
                        </el-table-column>
                        <el-table-column
                                prop="port"
                                label="端口"
                                width="120">
                        </el-table-column>
                        <el-table-column
                                prop="is_notice_flag_db"
                                label="通报状态"
                                :filters="[{ text: '已处理', value: '3' }, { text: '未处理', value: '1' }]"
                                :filter-method="filterTag"
                                filter-placement="bottom-end">
                            width="150">
                        </el-table-column>
                        <el-table-column
                                prop="sign_result"
                                label="标记结果"
                                width="120">
                        </el-table-column>
                        <el-table-column
                                fixed="right"
                                label="操作"
                                width="120">
                            <template slot-scope="scope">
                                <el-button @click="verificationClick(scope.row)" type="text" size="small">验证</el-button>
                                <el-dropdown style="float: right" :hide-on-click="false">
                                    <el-button type="text" size="small">标记为</el-button>
                                    <el-dropdown-menu slot="dropdown">
                                        <el-dropdown-item @click.native="submitClick(scope.row,1)">已提交</el-dropdown-item>
                                        <el-dropdown-item @click.native="submitClick(scope.row,2)">未提交</el-dropdown-item>
                                    </el-dropdown-menu>
                                </el-dropdown>
                            </template>
                        </el-table-column>
                    </el-table>
                </el-tab-pane>
                <el-tab-pane v-if="$store.state.emergency.httplist.length > 0" label="HTTP未响应">
                    <el-select v-model="selectvalue" placeholder="标记为" @change="selectChange">
                        <el-option
                                key="1"
                                label="已提交"
                                value="1">
                        </el-option>
                        <el-option
                                key="2"
                                label="未提交"
                                value="2">
                        </el-option>
                    </el-select>
                    <el-button @click="handNotification" style=" margin-left: 10px">提交通报</el-button>
                    <el-table
                            @selection-change="handleSelectionChange"
                            @select="selectionChange"
                            :data="$store.state.emergency.httplist"
                            ref="filterTable"
                            @row-click="rowClick"
                            style="width: 100%"
                            max-height="250">
                        <el-table-column
                                type="selection"
                                width="40"
                                column-key="alert_merge_id">
                        </el-table-column>
                        <el-table-column
                                column-key="alert_merge_id"
                                prop="new_time"
                                label="最后一次发现时间"
                                width="150">
                        </el-table-column>
                        <el-table-column
                                prop="website"
                                label="持续时间"
                                width="120">
                        </el-table-column>
                        <el-table-column
                                prop="is_notice_flag_db"
                                label="通报状态"
                                :filters="[{ text: '已处理', value: '3' }, { text: '未处理', value: '1' }]"
                                :filter-method="filterTag"
                                filter-placement="bottom-end">
                            width="150">
                        </el-table-column>
                        <el-table-column
                                prop="sign_result"
                                label="标记结果"
                                width="120">
                        </el-table-column>
                        <el-table-column
                                fixed="right"
                                label="操作"
                                width="120">
                            <template slot-scope="scope">
                                <el-button @click="verificationClick(scope.row)" type="text" size="small">验证</el-button>
                                <el-dropdown style="float: right" :hide-on-click="false">
                                    <el-button type="text" size="small">标记为</el-button>
                                    <el-dropdown-menu slot="dropdown">
                                        <el-dropdown-item @click.native="submitClick(scope.row,1)">已提交</el-dropdown-item>
                                        <el-dropdown-item @click.native="submitClick(scope.row,2)">未提交</el-dropdown-item>
                                    </el-dropdown-menu>
                                </el-dropdown>
                            </template>
                        </el-table-column>
                    </el-table>
                </el-tab-pane>
                <el-tab-pane v-if="$store.state.emergency.dnslist.length > 0" label="DNS未响应">
                    <el-select v-model="selectvalue" placeholder="标记为" @change="selectChange">
                        <el-option
                                key="1"
                                label="已提交"
                                value="1">
                        </el-option>
                        <el-option
                                key="2"
                                label="未提交"
                                value="2">
                        </el-option>
                    </el-select>
                    <el-button @click="handNotification" style=" margin-left: 10px">提交通报</el-button>
                    <el-table
                            @selection-change="handleSelectionChange"
                            @select="selectionChange"
                            :data="$store.state.emergency.dnslist"
                            ref="filterTable"
                            @row-click="rowClick"
                            style="width: 100%"
                            max-height="250">
                        <el-table-column
                                type="selection"
                                width="40"
                                column-key="alert_merge_id">
                        </el-table-column>
                        <el-table-column
                                column-key="alert_merge_id"
                                prop="new_time"
                                label="最后一次发现时间"
                                width="150">
                        </el-table-column>
                        <el-table-column
                                prop="website"
                                label="持续时间"
                                width="120">
                        </el-table-column>
                        <el-table-column
                                prop="is_notice_flag_db"
                                label="通报状态"
                                :filters="[{ text: '已处理', value: '3' }, { text: '未处理', value: '1' }]"
                                :filter-method="filterTag"
                                filter-placement="bottom-end">
                            width="150">
                        </el-table-column>
                        <el-table-column
                                prop="sign_result"
                                label="标记结果"
                                width="120">
                        </el-table-column>
                        <el-table-column
                                fixed="right"
                                label="操作"
                                width="120">
                            <template slot-scope="scope">
                                <el-button @click="verificationClick(scope.row)" type="text" size="small">验证</el-button>
                                <el-dropdown style="float: right" :hide-on-click="false">
                                    <el-button type="text" size="small">标记为</el-button>
                                    <el-dropdown-menu slot="dropdown">
                                        <el-dropdown-item @click.native="submitClick(scope.row,1)">已提交</el-dropdown-item>
                                        <el-dropdown-item @click.native="submitClick(scope.row,2)">未提交</el-dropdown-item>
                                    </el-dropdown-menu>
                                </el-dropdown>
                            </template>
                        </el-table-column>
                    </el-table>
                </el-tab-pane>
                <el-tab-pane v-if="$store.state.emergency.cglist.length > 0" label="篡改">
                    <el-select v-model="selectvalue" placeholder="标记为" @change="selectChange">
                        <el-option
                                key="1"
                                label="已提交"
                                value="1">
                        </el-option>
                        <el-option
                                key="2"
                                label="未提交"
                                value="2">
                        </el-option>
                    </el-select>
                    <el-button @click="handNotification" style=" margin-left: 10px">提交通报</el-button>
                    <el-table
                            @selection-change="handleSelectionChange"
                            @select="selectionChange"
                            :data="$store.state.emergency.cglist"
                            ref="filterTable"
                            @row-click="rowClick"
                            style="width: 100%"
                            max-height="250">
                        <el-table-column
                                type="selection"
                                width="40"
                                column-key="alert_merge_id">
                        </el-table-column>
                        <el-table-column
                                column-key="alert_merge_id"
                                prop="new_time"
                                label="最后一次发现时间"
                                width="150">
                        </el-table-column>
                        <el-table-column
                                column-key="alert_merge_id"
                                prop="website"
                                label="问题页面"
                                width="120">
                        </el-table-column>
                        <el-table-column
                                prop="website"
                                label="持续时间"
                                width="120">
                        </el-table-column>
                        <el-table-column
                                prop="is_notice_flag_db"
                                label="通报状态"
                                :filters="[{ text: '已处理', value: '3' }, { text: '未处理', value: '1' }]"
                                :filter-method="filterTag"
                                filter-placement="bottom-end">
                            width="150">
                        </el-table-column>
                        <el-table-column
                                prop="sign_result"
                                label="标记结果"
                                width="120">
                        </el-table-column>
                        <el-table-column
                                fixed="right"
                                label="操作"
                                width="120">
                            <template slot-scope="scope">
                                <el-button @click="verificationClick(scope.row)" type="text" size="small">验证</el-button>
                                <el-dropdown style="float: right" :hide-on-click="false">
                                    <el-button type="text" size="small">标记为</el-button>
                                    <el-dropdown-menu slot="dropdown">
                                        <el-dropdown-item @click.native="submitClick(scope.row,1)">已提交</el-dropdown-item>
                                        <el-dropdown-item @click.native="submitClick(scope.row,2)">未提交</el-dropdown-item>
                                    </el-dropdown-menu>
                                </el-dropdown>
                            </template>
                        </el-table-column>
                    </el-table>
                </el-tab-pane>
                <el-tab-pane v-if="$store.state.emergency.mgclist.length > 0" label="敏感词">
                    <!--<el-checkbox-group v-model="markselectList">-->
                    <!--<el-checkbox @change="flage(markselectList,'敏感词')" label="false">已处理</el-checkbox>-->
                    <!--<el-checkbox @change="flage(markselectList,'敏感词')" label="true">未处理</el-checkbox>-->
                    <!--</el-checkbox-group>-->
                    <el-select v-model="selectvalue" placeholder="标记为" @change="selectChange">
                        <el-option
                                key="1"
                                label="已提交"
                                value="1">
                        </el-option>
                        <el-option
                                key="2"
                                label="未提交"
                                value="2">
                        </el-option>
                    </el-select>
                    <el-button @click="handNotification" style=" margin-left: 10px">提交通报</el-button>
                    <el-table
                            @selection-change="handleSelectionChange"
                            @select-all="selectall"
                            :data="$store.state.emergency.mgclist"
                            ref="filterTable"
                            @row-click="rowClick"
                            style="width: 100%"
                            @select="selectionChange"
                            max-height="250">
                        <el-table-column
                                type="selection"
                                width="40">
                        </el-table-column>
                        <el-table-column
                                prop="new_time"
                                label="最后一次发现时间"
                                width="150">
                        </el-table-column>
                        <el-table-column
                                prop="website"
                                label="问题页面"
                                width="120">
                        </el-table-column>
                        <el-table-column
                                prop="sensitive_words"
                                label="敏感词"
                                width="120">
                        </el-table-column>
                        <el-table-column
                                prop="website"
                                label="持续时间"
                                width="120">
                        </el-table-column>
                        <el-table-column
                                prop="is_notice_flag_db"
                                label="通报状态"
                                :filters="[{ text: '已处理', value: '3' }, { text: '未处理', value: '1' }]"
                                :filter-method="filterTag"
                                filter-placement="bottom-end">
                            width="150">
                        </el-table-column>
                        <el-table-column
                                prop="sign_result"
                                label="标记结果"
                                width="120">
                        </el-table-column>
                        <el-table-column
                                fixed="right"
                                label="操作"
                                width="120">
                            <template slot-scope="scope">
                                <el-button @click="verificationClick(scope.row)" type="text" size="small">验证</el-button>
                                <el-dropdown style="float: right" :hide-on-click="false">
                                    <el-button type="text" size="small">标记为</el-button>
                                    <el-dropdown-menu slot="dropdown">
                                        <el-dropdown-item @click.native="submitClick(scope.row,1)">已提交</el-dropdown-item>
                                        <el-dropdown-item @click.native="submitClick(scope.row,2)">未提交</el-dropdown-item>
                                    </el-dropdown-menu>
                                </el-dropdown>
                            </template>
                        </el-table-column>
                    </el-table>
                </el-tab-pane>
            </el-tabs>
            <el-tabs v-if="showData.class_name == '硬件'" type="card" @tab-click="handleClick">
                <el-tab-pane v-if="$store.state.emergency.eylist.length > 0" label="恶意代码网络传输">
                    <el-select v-model="selectvalue" placeholder="标记为" @change="selectChange">
                        <el-option
                                key="1"
                                label="已提交"
                                value="1">
                        </el-option>
                        <el-option
                                key="2"
                                label="未提交"
                                value="2">
                        </el-option>
                    </el-select>
                    <el-button @click="handNotification" style=" margin-left: 10px">提交通报</el-button>
                    <el-table
                            @selection-change="handleSelectionChange"
                            @select="selectionChange"
                            @select-all="selectall"
                            :data="$store.state.emergency.eylist"
                            ref="filterTable"
                            @row-click="rowClick"
                            style="width: 100%"
                            max-height="250">
                        <el-table-column
                                type="selection"
                                width="40">
                        </el-table-column>
                        <el-table-column
                                prop="md5"
                                label="文件MD5"
                                width="150">
                        </el-table-column>
                        <el-table-column
                                prop="virus_family"
                                label="恶意代码名称"
                                width="120">
                        </el-table-column>
                        <el-table-column
                                prop="virus_family"
                                label="病毒家族"
                                width="120">
                        </el-table-column>
                        <el-table-column
                                label="通报状态"
                                :filters="[{ text: '已处理', value: 'true' }, { text: '未处理', value: 'false' }]"
                                :filter-method="filterTag"
                                filter-placement="bottom-end"
                                width="150">
                            <template slot-scope="scope">
                                <span>{{scope.row.is_notice_flag ? '已处理':'未处理'}}</span>
                            </template>
                        </el-table-column>
                        <el-table-column
                                prop="deal_result"
                                label="标记结果"
                                width="120">
                        </el-table-column>
                        <el-table-column
                                fixed="right"
                                label="操作"
                                width="120">
                            <template slot-scope="scope">
                                <el-button @click="verificationClick(scope.row)" type="text" size="small">验证</el-button>
                                <el-dropdown style="float: right" :hide-on-click="false">
                                    <el-button type="text" size="small">标记为</el-button>
                                    <el-dropdown-menu slot="dropdown">
                                        <el-dropdown-item @click.native="submitClick(scope.row,1)">已提交</el-dropdown-item>
                                        <el-dropdown-item @click.native="submitClick(scope.row,2)">未提交</el-dropdown-item>
                                    </el-dropdown-menu>
                                </el-dropdown>
                            </template>
                        </el-table-column>
                    </el-table>
                </el-tab-pane>
                <el-tab-pane v-if="$store.state.emergency.cclist.length > 0" label="C&C通讯">
                    <el-select v-model="selectvalue" placeholder="标记为" @change="selectChange">
                        <el-option
                                key="1"
                                label="已提交"
                                value="1">
                        </el-option>
                        <el-option
                                key="2"
                                label="未提交"
                                value="2">
                        </el-option>
                    </el-select>
                    <el-button @click="handNotification" style=" margin-left: 10px">提交通报</el-button>
                    <el-table
                            @selection-change="handleSelectionChange"
                            @select-all="selectall"
                            :data="$store.state.emergency.cclist"
                            ref="filterTable"
                            @row-click="rowClick"
                            style="width: 100%"
                            @select="selectionChange"
                            max-height="250">
                        <el-table-column
                                type="selection"
                                width="40">
                        </el-table-column>
                        <el-table-column
                                prop="cc_ip"
                                label="域名"
                                width="150">
                        </el-table-column>
                        <el-table-column
                                prop="asset_ip"
                                label="ip"
                                width="120">
                        </el-table-column>
                        <el-table-column
                                prop="connect_time"
                                label="连接持续时间"
                                width="120">
                        </el-table-column>
                        <el-table-column
                                label="通报状态"
                                :filters="[{ text: '已处理', value: '3' }, { text: '未处理', value: '1' }]"
                                :filter-method="filterTag"
                                filter-placement="bottom-end"
                                width="150">
                            <template slot-scope="scope">
                                <span>{{scope.row.sign_result ? '已处理':'未处理'}}</span>
                            </template>
                        </el-table-column>
                        <el-table-column
                                prop="sign_result"
                                label="标记结果"
                                width="120">
                        </el-table-column>
                        <el-table-column
                                fixed="right"
                                label="操作"
                                width="120">
                            <template slot-scope="scope">
                                <el-button @click="verificationClick(scope.row)" type="text" size="small">验证</el-button>
                                <el-dropdown style="float: right" :hide-on-click="false">
                                    <el-button type="text" size="small">标记为</el-button>
                                    <el-dropdown-menu slot="dropdown">
                                        <el-dropdown-item @click.native="submitClick(scope.row,1)">已提交</el-dropdown-item>
                                        <el-dropdown-item @click.native="submitClick(scope.row,2)">未提交</el-dropdown-item>
                                    </el-dropdown-menu>
                                </el-dropdown>
                            </template>
                        </el-table-column>
                    </el-table>
                </el-tab-pane>
            </el-tabs>
        </el-main>
        <div v-if="$store.state.emergency.showVer" class="verTable"

             style="width: 100%; height: 100%; background: #bdc1ca5e">
            <par-verify v-bind:style="$store.state.emergency.verStyle"></par-verify>
        </div>
    </el-container>
</template>
<script>
    import { mapState } from 'vuex'
    import { getMark, notification } from '../../service/getData'

    export default {
        props: {
            showData: {}
        },
        data() {
            return {
                selectList: [],// 多选
                mergeidList: [],//
                htmlTitle: '页面导出PDF文件名',
                markselectList: ['false', 'true'],
                selectvalue: [],
            }
        },
        mounted() {
        },
        watch: {},
        beforeUpdate() {

        },
        computed() {
        // ...mapState()
        },

        updated() {

        },
        methods: {
            handleSelectionChange(val, cherk) {
                // console.log(val)

            },
            handleClick() {
            },
            handNotification() {
                if (this.selectList.length === 0) {
                    return this.$message.error('请选择告警信息');
                }
                notification(this.selectList).then(res => {
                    this.selectList = []

                    if (res.error === 'false') {
                        this.$message({
                            showClose: true,
                            message: '提交成功',
                            type: 'success'
                        });
                    } else {
                        this.$message.error('错误信息：', res.warn);
                    }
                    this.$store.dispatch('emergency_lists')
                })

            },
            selectChange() {
                if (this.selectList.length === 0) {
                    this.selectvalue = []
                    return this.$message.error('请选择告警信息');
                }
                getMark(this.selectList, this.selectvalue).then(res => {
                    if (res.error === 'false') {
                        this.$message({
                            showClose: true,
                            message: '修改成功',
                            type: 'success'
                        });
                        this.selectList.length = []
                        this.$store.dispatch('emergency_lists')
                    } else {
                        this.$message.error('错误信息：', res.warn);
                    }
                    this.selectvalue = []
                })
            },

            selectionChange(row, selected) {
                if (this.showData.class_name == '服务') {
                    let flag = 0
                    for (let i in row) {
                        if (selected.alert_merge_id === row[i].alert_merge_id) {
                            flag = 1
                            break
                        }
                    }
                    if (flag === 1) {
                        this.selectList.push(selected.alert_merge_id)
                    } else {
                        for (let i in this.selectList) {
                            if (this.selectList[i] === selected.alert_merge_id) {
                                this.selectList.splice(i, 1)
                            }
                        }
                    }
                } else {
                    let flag = 0
                    for (let i in row) {
                        if (selected.id === row[i].id) {
                            flag = 1
                            break
                        }
                    }
                    if (flag === 1) {
                        this.selectList.push(selected.id)
                    } else {
                        for (let i in this.selectList) {
                            if (this.selectList[i] === selected.id) {
                                this.selectList.splice(i, 1)
                            }
                        }
                    }
                }
            },
            selectall(selection) {
                if (this.showData.class_name == '服务') {
                    this.selectList = []
                    for (let i in selection) {
                        this.selectList.push(selection[i].alert_merge_id)
                    }
                } else {
                    this.selectList = []
                    for (let i in selection) {
                        this.selectList.push(selection[i].id)
                    }
                }

            },
            filterTag(value, row) {
                return row.res_state === value;
            },

            handleClick(tab, event) {
                this.selectList = []
            },
            rowClick(row) {
            },
            verificationClick(row) {
                this.$store.commit('ver_visible')
                this.$store.state.emergency.alert_merge_id = row.alert_merge_id
            },
            submitClick(row, val) {
                console.log(row)
                console.log(val)
                if (this.showData.class_name === '服务') {
                    this.mergeidList = []
                    this.mergeidList.push(row.alert_merge_id)
                    getMark(this.mergeidList, val).then(res => {
                        if (res.error === 'false') {
                            this.$message({
                                showClose: true,
                                message: '修改成功',
                                type: 'success'
                            });
                            this.$store.dispatch('emergency_lists')
                        } else {
                            this.$message.error('错误信息：', res.warn);
                        }
                        // this.deterrentList = res.data
                        // this.loading = false
                    })
                } else {
                    this.mergeidList = []
                    this.mergeidList.push(row.id)
                    getMark(this.mergeidList, val).then(res => {
                        if (res.error === 'false') {
                            this.$message({
                                showClose: true,
                                message: '修改成功',
                                type: 'success'
                            });
                            this.$store.dispatch('emergency_lists')
                        } else {
                            this.$message.error('错误信息：', res.warn);
                        }
                        // this.deterrentList = res.data
                        // this.loading = false
                    })
                }
            },
        },
    }
</script>
<style>
    .el-card {
        border: none !important;
    }

    . el-card__header {
        border: none !important;
        border-bottom: 1px solid #f0f8ff !important;

    }

    .operHeader {
        color: aliceblue;
        background-color: rgb(51 63 93);
        height: 120px !important;
    }

    .el-main {
        background: #fff !important;
    }

    .elcol {
        margin-bottom: 10px;
    }

    .verTable {
        position: fixed;
        overflow: auto;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
        z-index: 300;
        -webkit-overflow-scrolling: touch;
        outline: 0;
        display: block;
    }
</style>