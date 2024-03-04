<script lang="ts" setup>
import { useTokenStore } from '@/stores/token'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRouter } from 'vue-router'

const router = useRouter()

const toeknStore = useTokenStore()

async function handLogout() {
  ElMessageBox.confirm('确定要退出登录吗?', '退出登录', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
    .then(() => {
      // 执行退出操作清空token
      ElMessage({
        type: 'success',
        message: '已退出登录'
      })
      useTokenStore().saveToken('')
      router.push('/login')
    })
    .catch(() => {
      ElMessage({
        type: 'info',
        message: '取消退出'
      })
      return new Promise(() => {})
    })
}
</script>

<template>
  <el-menu class="el-menu-demo" mode="horizontal" :ellipsis="false">
    <div class="logo-item" style="width: 200px">
      <img
        style="width: 120px"
        src="D:\我的项目\Vue-Demo\src\assets\element-plus-logo.svg"
        alt="Element logo"
      />
    </div>

    <div class="flex-grow" style="margin-right: 200px" />
    <!-- <el-menu-item index="0">Processing Center</el-menu-item> -->
    <el-sub-menu index="1">
      <template #title>{{ toeknStore.getUserObj?.user_name }}</template>
      <el-menu-item @click="handLogout">退出登录</el-menu-item>
    </el-sub-menu>
  </el-menu>
</template>

<style scoped lang="scss">
.flex-grow {
  flex-grow: 1;
}

.logo-item {
  display: flex;
  align-items: center;
  margin-left: 20px;
}
</style>
