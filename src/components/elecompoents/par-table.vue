<template>
    <el-container class="oper-table">
        <el-header class="operHeaderD">
            <span>确认通报内容</span>
            <span @click="$store.commit('par_visible')" style="float: right; padding: 3px 0; color: aliceblue"
                  type="text"><i class="el-icon-close"></i></span>
            <span  v-if="$store.state.emergency.visable === true" @click="$store.commit('big_parvisible')" style="float: right; padding: 3px 0; color: aliceblue"
                  type="text"><i class="el-icon-plus"></i></span>
            <span  v-if="$store.state.emergency.visable === false" @click="$store.commit('small_parvisible')" style="float: right; padding: 3px 0; color: aliceblue"
                  type="text"><i class="el-icon-minus"></i></span>

        </el-header>
        <el-main>
            <el-form ref="form" :model="form" label-width="80px">
                <el-form-item label="处理状态">
                    <el-checkbox-group v-model="form.select" style="margin-bottom: 0px">
                        <el-checkbox label="已处理" ></el-checkbox>
                        <el-checkbox label="未处理" ></el-checkbox>
                    </el-checkbox-group>
                </el-form-item>
                <el-form-item label="通报状态">
                    <el-checkbox-group v-model="form.select">
                        <el-checkbox label="已提交" ></el-checkbox>
                        <el-checkbox label="未提交" ></el-checkbox>
                    </el-checkbox-group>
                </el-form-item>
                <el-tree
                        :data="this.$store.state.emergency.data4"
                        show-checkbox
                        @check="checkchange"
                        node-key="alert_merge_id"
                        default-expand-all
                        :expand-on-click-node="false"
                        :render-content="renderContent">
                </el-tree>
                <!--<el-collapse v-for="(dataarea,index1) in this.$store.state.emergency.partableList"-->
                             <!--:key="index1">-->
                <!--</el-collapse>-->

            </el-form>
            <div class="btn">
                <el-button @click="handNotification" type="primary" >确定</el-button>
                <el-button @click="$store.commit('par_visible');">取消</el-button>
            </div>
        </el-main>
    </el-container>
</template>
<script>
    import {notification} from '../../service/getData'
    export default {

        props: {
            imageData: {}
        },
        data() {
            return {
                selectlists: [],
                setTree: '',
                form: {
                    select:['已处理','未处理','已提交','未提交']
                },

            }
        },
        created() {
        },
        methods: {
            handNotification() {
                if(this.selectlists.length === 0){
                    return this.$message.error('请选择告警信息');
                }
                notification(this.selectlists).then(res => {
                    console.log(res,'===============================================')
                    this.selectlists = []
                    if(res.error === 'false'){
                        this.$message({
                            showClose: true,
                            message: '提交成功',
                            type: 'success'
                        });
                    }else {
                        this.$message.error('错误信息：', res.warn);
                    }
                    this.$store.dispatch('emergency_lists')
                    this.$store.commit('par_visible')


                })
                console.log(this.selectList,'=-=-=-=======================')
            },

            renderContent(h, { node, data, store }) {
                // console.log(node)
                // console.log(data)
                // console.log(store)
                return (
                    <span class="custom-tree-node">
                        <span style={{marginLeft : '20px'}}>{node.data.id}</span>
                        <span style={{marginLeft : '20px'}}>{data.new_time}</span>
                        <span style={{marginLeft : '20px'}}>{data.alert_reson}</span>
                        <span style={{marginLeft : '20px'}}>{data.is_notice_flag_db}</span>
                {node.data.id ? '' : (data.sign_result === '1' ? <span style={{marginLeft : '20px'}}> 未提交</span>: <span style={{marginLeft : '20px'}}> 已提交</span>)}
                    </span>);
            },
            checkchange(val,row,al) {
             console.log(val)
             console.log(row.checkedKeys)
                let b = [];
                for(var i=0;i<row.checkedKeys.length;i++){
                    if(typeof(row.checkedKeys[i])!='undefined'){
                        b.push(row.checkedKeys[i]);
                    }
                }
                console.log(b)
                this.selectlists = b
            },
        },
    }
</script>
<style scoped>
    .el-card {
        border: none !important;
    }

    . el-card__header {
        border: none !important;
        border-bottom: 9px solid #f0f8ff !important;

    }

    .operHeaderD {
        color: aliceblue;
        background-color: rgb(51 63 93);
        height: 80px !important;
        line-height: 80px !important;

    }

    .btn {
        text-align: center;
        padding: 12px 40px;
    }

    .el-main {
        background: #fff !important;
    }
</style>