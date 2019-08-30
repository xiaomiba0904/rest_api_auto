from rest_api_auto import _api_globals, CRUD
from rest_api_auto.base import APIManager


def register_model(name=None, actions=None):
    """
    model 注册装饰器
    :param name: app.model
      默认为Model._meta.label
    :param actions: 增："C"， 删："D", 改："U", 查："R"
    """
    if actions:
        if not set(actions).issubset(set(CRUD)):
                raise ValueError("操作方法错误，只能使用CRUD内")
    else:
        actions = CRUD

    if name:
        if name in _api_globals:
            raise ValueError("API 名称重复")
        if '.' not in name:
            raise ValueError("name 必须有 . 符号")

    def wrapper(model_class):
        api_name = name or model_class._meta.label
        if api_name not in _api_globals:
            _api_globals[api_name] = APIManager(api_name, model_class, actions=actions)
        return model_class

    return wrapper
