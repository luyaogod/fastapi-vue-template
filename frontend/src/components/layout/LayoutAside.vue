<script setup lang="ts">
import { useTokenStore } from '@/stores/token'
import { ref } from 'vue'

const store = useTokenStore()

const allMenusControl = ref(false)

if (store.getUserObj !== null) {
  allMenusControl.value = true
}
</script>

<template>
  <el-menu class="layoutMenu" router>
    <el-menu-item index="1">
      <el-icon><IEpClock /></el-icon>
      <span>主要业务</span>
    </el-menu-item>

    <el-menu-item index="/user-manage">
      <el-icon><IEpUser /></el-icon>
      <span>用户管理</span>
    </el-menu-item>

    <el-menu-item index="/role-manage">
      <el-icon><IEpLocation /></el-icon>
      <span>角色管理</span>
    </el-menu-item>

    <el-menu-item index="/permission-manage">
      <el-icon><IEpLock /></el-icon>
      <span>权限管理</span>
    </el-menu-item>

    <el-menu-item
      index="/permission-test"
      v-if="
        store.getUserObj?.super_admin ||
        (allMenusControl && store.getUserObj?.role.includes('test_role'))
      "
    >
      <el-icon><IEpdocument /></el-icon>
      <span>权限测试</span>
    </el-menu-item>
  </el-menu>
</template>

<style scoped lang="scss">
.layoutMenu {
  height: calc(100vh - 60px);
}
.el-menu-item {
  font-size: 17px;
}
</style>
