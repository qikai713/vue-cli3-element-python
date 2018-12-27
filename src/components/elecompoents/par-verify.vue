<template>
    <el-container class="oper-table">
        <el-header class="operHeaderD">
            <span>确认通报内容</span>
            <span @click="$store.commit('ver_visible')" style="float: right; padding: 3px 0; color: aliceblue"
                  type="text"><i class="el-icon-minus"></i></span>
            <span v-if="$store.state.emergency.visable === true" @click="$store.commit('big_vervisible')"
                  style="float: right; padding: 3px 0; color: aliceblue" type="text"><i class="el-icon-plus"></i></span>
            <span v-if="$store.state.emergency.visable === false" @click="$store.commit('small_vervisible')"
                  style="float: right; padding: 3px 0; color: aliceblue" type="text"><i
                    class="el-icon-minus"></i></span>
        </el-header>
        <el-main>
            <el-form ref="form" :model="form" label-width="80px">
                <el-form-item label="验证结论">
                    <el-upload
                            class="upload-demo"
                            action="http://127.0.0.1:5000/addFlies"
                            :on-progress='fileProgress'
                            :on-success='fileSuccess'
                            :on-preview="handlePreview"
                            :on-remove="handleRemove"
                            :limit="1"
                            :auto-upload="true">
                        <el-button size="small" type="primary">点击上传</el-button>
                        <div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过500kb</div>
                    </el-upload>
                </el-form-item>
                <el-form-item label="验证结论">
                    <el-radio-group v-model="form.resource">
                        <el-radio label="1">属实</el-radio>
                        <el-radio label="2">误报</el-radio>
                    </el-radio-group>
                </el-form-item>
                <el-form-item label="描述">
                    <el-input type="textarea" v-model="form.desc"></el-input>
                </el-form-item>
            </el-form>
            <div class="btn">
                <el-button type="primary" @click="onSubmit">确定</el-button>
                <el-button @click="$store.commit('ver_visible')">取消</el-button>
            </div>
        </el-main>
    </el-container>
</template>
<script>
    import {verification} from '../../service/getData'

    export default {
        props: {
            imageData: {}
        },
        data() {
            return {
                form: {
                    id: '',
                    desc: '',
                    resource: '',
                    image: '',
                }
            }
        },
        methods: {
            handleRemove(file, fileList) {
                console.log(file, fileList);
            },
            handlePreview(file) {
                console.log(file);
            },
            fileProgress(file) {
                console.log(file);

            },
            fileSuccess(file) {
                console.log(file);
                this.form.image = []
                this.form.image = file.data

            },
            onSubmit(file) {
                this.form.id = this.$store.state.emergency.alert_merge_id
                console.log(this.form);
                verification(this.form).then(res => {
                    if (res.error === 'false') {
                        this.$message({
                            showClose: true,
                            message: '提交成功',
                            type: 'success'
                        });
                        this.$store.commit('ver_visible')
                    } else {
                        this.$message.error('错误信息：', res.warn);
                    }
                    console.log(res, '=========================================================')
                })
            },
        },
        mounted() {

        }

    }
</script>
<style>
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