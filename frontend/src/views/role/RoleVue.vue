<script setup lang="ts">
import { ref } from 'vue'
import { getAllRole, type responseDataItem } from '@/api/role'
import DialogRoleVueCreateOrEdit from './DialogRoleVueCreateOrEdit.vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { deleteRole } from '@/api/role'

const roleList = ref([] as responseDataItem[])

function getAllRoleFunction() {
  getAllRole()
    .then((rep) => {
      roleList.value = rep
      console.log('role数据已获取')
    })
    .catch((error) => {
      console.log('出错了', error)
    })
}

getAllRoleFunction()

//这里是为组件模板引用类型标注，具体参考官方文档TS组合式API底部部分
const dlgCreateOrEdit = ref<InstanceType<typeof DialogRoleVueCreateOrEdit>>()

async function handleDelete(id: number) {
  await ElMessageBox.confirm('确定要删除吗？', '危险动作提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).catch(() => {
    ElMessage.info('取消删除')
    return new Promise(() => {})
  })
  deleteRole(id)
    .then(() => {
      ElMessage.success('删除成功')
      getAllRoleFunction()
    })
    .catch((error) => {
      ElMessage.error(`出错了删除失败:${error}`)
    })
}
</script>

<template>
  <el-card class="box-card">
    <template #header>
      <div class="card-header">
        <h3>角色操作</h3>
        <el-button class="button" type="primary" @click="($event) => dlgCreateOrEdit?.initAndShow()"
          >创建角色</el-button
        >
      </div>
    </template>
    <!-- 表格区域 -->
    <el-table :data="roleList" style="width: 100%">
      <el-table-column type="index" label="序号" width="70"> </el-table-column>
      <el-table-column label="角色名称" width="120">
        <template #default="scope">
          <el-tag>{{ scope.row.role_name }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="权限">
        <template #default="scope">
          <template v-for="(item, index) in scope.row.permission" :key="index">
            <el-tag type="info" style="margin-right: 3px">{{ item.scope }}</el-tag>
          </template>
        </template>
      </el-table-column>

      <el-table-column label="操作">
        <template #default="scope">
          <el-button size="small" @click="dlgCreateOrEdit?.initAndShow(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(scope.row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <DialogRoleVueCreateOrEdit ref="dlgCreateOrEdit" :getAllRoleFunction="getAllRoleFunction" />
    <!-- <template #footer> </template> -->
  </el-card>
</template>

<style scoped lang="scss">
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.text {
  font-size: 14px;
}

.item {
  margin-bottom: 18px;
}

.box-card {
  width: auto;
}
</style>
