from typing import Type
from pydantic import BaseModel


def util_list_queryset_validate_dump(data:list,schemas:Type[BaseModel]) -> list:
    """
    解析被list包裹的queryset，并使用pydantic进行校验和反序列化
    :param schemas:
    :param data:
    :return:
    """
    data_list = []
    for i in data:
        instance = schemas(**i)
        model_dump = getattr(instance, "model_dump", None)
        if callable(model_dump):
            data_list.append(model_dump())
        else:
            pass
    return data_list



