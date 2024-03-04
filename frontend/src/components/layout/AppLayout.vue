<script setup lang="ts">
import LayoutAside from '@/components/layout/LayoutAside.vue'
import LayoutHeader from '@/components/layout/LayoutHeader.vue'
import { RouterView } from 'vue-router'
</script>

<template>
  <div class="common-layout">
    <el-container>
      <el-header>
        <LayoutHeader></LayoutHeader>
      </el-header>
      <el-container>
        <el-aside width="200px">
          <LayoutAside></LayoutAside>
        </el-aside>
        <el-main>
          <RouterView></RouterView>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<style scoped lang="scss"></style>
