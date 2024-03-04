<script setup lang="ts">
//表单响应式数据
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { reactive, ref } from 'vue'
import { login } from '@/api/user'
import { useTokenStore } from '@/stores/token'
import { useRouter, useRoute } from 'vue-router'

const tokenStore = useTokenStore()

const isLoading = ref(false)

const router = useRouter()

const route = useRoute()

const form = reactive({
  username: 'admin',
  password: '123456'
})

//定义表单校验规则，传入的泛型是Elementui已经定义好的类型
//参数解释：trigger:"blur"表示在失去光标的时候触发校验
//可以定义多个校验{pattern:正则，message:"不符合规则",trigger:"blur"}
const rules = reactive<FormRules>({
  username: [{ required: true, message: '用户名不能为空', trigger: 'blur' }],
  password: [
    { required: true, message: '密码不能为空', trigger: 'blur' },
    { min: 6, message: '密码最小6位', trigger: 'blur' }
  ]
})

//获取表单元素,定义的泛型是ELementUI为我们封装好的表单实例类型
const formRef = ref<FormInstance>()

//首先对表单的内容做二次校验，校验失败要做错误捕获,捕获完毕仍要thorw抛出错误停止代码运行
//登录成功后跳转到 / 页面，或者触发路由守卫前的页面
async function onSubmit() {
  await formRef.value?.validate().catch((err) => {
    ElMessage.error('表单校验失败')
    throw err
  })
  login(form)
    .then((res) => {
      const userToken: string = res.access_token
      tokenStore.token = userToken
      tokenStore.saveToken(userToken)
      isLoading.value = false
      router.push((route.query.redirect as string) || '/')
    })
    .catch((error) => {
      if (error.response.status === 401) ElMessage.error('登录失败账号或密码错误')
      else ElMessage.error('出错了，登录失败，请稍后再试')
      isLoading.value = false
    })
}
</script>

<template>
  <div class="login">
    <el-form
      :model="form"
      :rules="rules"
      ref="formRef"
      label-width="120px"
      label-position="top"
      size="large"
    >
      <h2>登录</h2>
      <!-- prop参数用于分配表单规则 -->
      <el-form-item label="账号" prop="username">
        <el-input v-model="form.username" />
      </el-form-item>

      <el-form-item label="密码" prop="password">
        <el-input v-model="form.password" />
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="onSubmit" :loading="isLoading">登录</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<style scoped lang="scss">
.login {
  background-color: #ccc;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}
.el-form {
  width: 300px;
  background-color: #fff;
  padding: 30px;
  border-radius: 10px;

  .el-form-item {
    margin-top: 20px;
  }
  .el-button {
    width: 100%;
    margin-top: 30px;
  }
}
</style>
