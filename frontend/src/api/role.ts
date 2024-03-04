import axio from '@/utils/request'
//allRoleWithPermission
export interface permission {
  id: number
  scope: string
}

export interface responseDataItem {
  id: number
  role_name: string
  permission: permission[]
}

export async function getAllRole() {
  const response = await axio.get('/user/all_role_permissions')
  const data: responseDataItem[] = response.data
  return data
}

//getAllPermissionForSelect
export async function getAllPermissionForSelect() {
  const response = await axio.get('/permissions')
  const data: permission[] = response.data
  return data
}

//role的创建和更新
interface createRoleWithPermissionPostData {
  role_name: string
  permission_id: Array<number> | null
}

//创建或更新role
export async function createRoleWithPermission(
  data: createRoleWithPermissionPostData,
  role_id?: number
) {
  const response = await axio.post(`/role/role_with_permission/${role_id}`, data)
  return response.data
}

//删除role
export async function deleteRole(id: number) {
  const response = await axio.delete(`/role/${id}`)
  return response.data
}
