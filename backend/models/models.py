from tortoise.models import Model
from tortoise import fields


class TimestampMixin(Model):
    create_time = fields.DatetimeField(auto_now_add=True, description='创建时间')
    update_time = fields.DatetimeField(auto_now=True, description="更新时间")

    class Meta:
        abstract = True


class User(TimestampMixin):
    user_name = fields.CharField(max_length=20,unique=True)
    role: fields.ManyToManyRelation["Role"] = \
        fields.ManyToManyField("models.Role", related_name="user", on_delete=fields.CASCADE)
    password = fields.CharField(max_length=255)
    user_status = fields.IntField(default=0, description='0未激活 1正常 2禁用')
    super_admin = fields.BooleanField(default=False, description="用户类型 True:超级管理员 False:普通用户")


class Role(TimestampMixin):
    role_name = fields.CharField(max_length=20,unique=True)
    user: fields.ManyToManyRelation[User]
    permission: fields.ManyToManyRelation["Permission"] = \
        fields.ManyToManyField("models.Permission", related_name="role", on_delete=fields.CASCADE)


class Permission(TimestampMixin):
    scope = fields.CharField(max_length=30,unique=True)
    role: fields.ManyToManyRelation[Role]

