# fastapi-vue-template

本项目旨在提供使用vue和fastapi构建前后端分离项目的模板

## backend后端

后端采用fastapi结合tortoise-orm主要内容如下

- 数据库采用mysql使用tortoise-orm进行数据库操作
- 提供RBAC权限控制的表结构以及数据库操作的模板
- 提供JWT登录的模板
- 提供FastAPI异常捕获的实现思路

## frontend前端

前端采用vue结合elementui主要内容如下

- 提供使用vue-router路由守卫配合pinia来实现多角色登录的模板
- 提供使用element-ui来进行表单校验，弹窗，以及数据渲染的模板