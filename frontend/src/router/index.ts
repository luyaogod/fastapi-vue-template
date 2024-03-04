import { createRouter, createWebHistory } from 'vue-router'
import AppLayout from '@/components/layout/AppLayout.vue'
import { useTokenStore } from '@/stores/token'
import { tokenVertify } from '@/utils/jwt'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/login/LoginView.vue')
    },
    {
      path: '/',
      name: 'home',
      meta: { requiersAuth: true },
      component: AppLayout,
      children: [
        {
          path: 'user-manage',
          name: 'userManage',
          component: () => import('@/views/admin/UserVue.vue')
        },
        {
          path: 'role-manage',
          name: 'roleManage',
          component: () => import('@/views/role/RoleVue.vue')
        },
        {
          path: 'permission-manage',
          name: 'permissionManage',
          component: () => import('@/views/admin/PermissionVue.vue')
        },
        {
          path: 'permission-test',
          name: 'permissionTest',
          component: () => import('@/views/PermissionTestVue.vue'),
          meta: { role: ['scope_test_2'] }
        },
        {
          path: '/:xxx(.*)*',
          name: 'errorPage',
          component: () => import('@/views/error/ErrorPage.vue')
        }
      ]
    },
    {
      path: '/error',
      name: 'error',
      component: () => import('@/views/error/ErrorPage.vue')
    }
  ]
})

router.beforeEach((to, from, next) => {
  if (to.meta.requiersAuth) {
    //获取store的时候不能过早，就应该再这里
    const store = useTokenStore()
    const tokenVT: boolean = tokenVertify(store.getToken)
    // console.log(tokenVT)
    // console.log(to.meta.role)

    if (!tokenVT) {
      next({ name: 'login', query: { redirect: to.fullPath } })
    } else if (to.meta.role) {
      // console.log('需要role')
      if (!store.getUserObj) {
        // console.log('有用户信息')
        next({ name: 'error', query: { redirect: to.fullPath } })
      } else {
        const superAdmin = store.getUserObj.super_admin
        // console.log('是否管理员？-', superAdmin)
        const routerRole = to.meta.role as string[]
        const roleVertify: boolean = routerRole.every((role) =>
          store.getUserObj?.role.includes(role)
        )
        // console.log('role是否正确？-', roleVertify)
        if (!superAdmin && !roleVertify) {
          // console.log('校验没通过')
          next({ name: 'error', query: { redirect: to.fullPath } })
        }
        // else console.log('校验通过')
      }
    }
  }
  next()
})

export default router
