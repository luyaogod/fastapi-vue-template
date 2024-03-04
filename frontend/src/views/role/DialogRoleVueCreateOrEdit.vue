<script setup lang="ts">
import { ref, reactive, watch } from 'vue'
import { type CheckboxValueType, ElMessage } from 'element-plus'
import { getAllPermissionForSelect, type permission, createRoleWithPermission } from '@/api/role'

const dialogFormVisible = ref(false)
const formLabelWidth = '140px'
const isCreate = ref(true)
const MgsText = ref('')
const form = reactive({
  role_name: ''
})
const allPermission = ref([] as permission[])
const checkAll = ref(false)
const indeterminate = ref(false)
const value = ref<CheckboxValueType[]>([])
let targetDataId: number
const { getAllRoleFunction } = defineProps(['getAllRoleFunction'])
//表单规则

//权限下拉框数据获取
getAllPermissionForSelect()
  .then((rep) => {
    allPermission.value = rep
    // console.log(allPermission.value)
  })
  .catch((error) => {
    console.log('出错了', error)
  })

//对话框开关函数
function initAndShow(data: any = 0) {
  //打开表单对话框初始化时清空表单
  dialogFormVisible.value = true
  targetDataId = data.id || ''
  if (data) {
    MgsText.value = '更新'
    form.role_name = data.role_name
    const permissionIdArray = []
    const targerArray = data.permission as Array<permission>
    for (const item of targerArray) {
      permissionIdArray.push(item.id)
    }
    value.value = permissionIdArray
    isCreate.value = true
  } else {
    form.role_name = ''
    value.value = []
    isCreate.value = false
    MgsText.value = '创建'
  }
}

//导出对话框开关函数
defineExpose({
  initAndShow
})

//表单提交事件
async function onSubmit() {
  const selectedValues = value.value
  console.log('用户选择的选项值：', selectedValues)
  const role_name = form.role_name
  console.log('用户填写的role_name', role_name)
  const postData = {
    role_name: role_name as string,
    permission_id: selectedValues as Array<number>
  }
  console.log('检查表单数据', postData)
  console.log('检查ID', targetDataId)

  createRoleWithPermission(postData, targetDataId)
    .then(() => {
      ElMessage.success('创建/更新成功')
    })
    .catch((error) => {
      ElMessage.error(`创建/更新失败：${error}`)
    })
    .finally(() => {
      getAllRoleFunction()
      dialogFormVisible.value = false
    })
}

//全选和半选状态更新
watch(value, (val) => {
  if (val.length === 0) {
    checkAll.value = false
    indeterminate.value = false
  } else if (val.length === allPermission.value.length) {
    checkAll.value = true
    indeterminate.value = false
  } else {
    indeterminate.value = true
  }
})

//全选工具
const handleCheckAll = (val: CheckboxValueType) => {
  indeterminate.value = false
  if (val) {
    value.value = allPermission.value.map((_) => _.id)
  } else {
    value.value = []
  }
}
</script>

<template>
  <el-dialog v-model="dialogFormVisible" :title="MgsText + '角色'" width="500">
    <el-form :model="form">
      <el-form-item label="角色名称" :label-width="formLabelWidth">
        <el-input v-model="form.role_name" autocomplete="off" />
      </el-form-item>
      <el-form-item label="权限选择" :label-width="formLabelWidth">
        <el-select
          v-model="value"
          multiple
          clearable
          collapse-tags
          placeholder="Select"
          popper-class="custom-header"
          :max-collapse-tags="1"
          style="width: 240px"
        >
          <template #header>
            <el-checkbox v-model="checkAll" :indeterminate="indeterminate" @change="handleCheckAll">
              All
            </el-checkbox>
          </template>
          <el-option
            v-for="item in allPermission"
            :key="item.id"
            :label="item.scope"
            :value="item.id"
          />
        </el-select>
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取消</el-button>
        <el-button type="primary" @click="onSubmit"> 确定 </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<style scoped lang="scss">
.custom-header {
  .el-checkbox {
    display: flex;
    height: unset;
  }
}
</style>
