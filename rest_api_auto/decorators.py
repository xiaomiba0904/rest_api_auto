from rest_api_auto import _api_globals, CRUD
from rest_api_auto.base import APIManager


def register_model(name=None, actions=CRUD):
    """
    model 装饰器
    """
    if actions not in CRUD:
        raise ValueError("操作方法错误，只能使用CRUD内")

    if name and name in _api_globals:
        raise ValueError("API 名称重复")

    def wrapper(model_class):
        api_name = name or model_class._meta.label
        if api_name in _api_globals:
            return model_class

        api_manager = APIManager(api_name, model_class, actions=actions)
        _api_globals[api_name] = api_manager
        return model_class

    return wrapper
