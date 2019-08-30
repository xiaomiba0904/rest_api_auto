# rest_api_auto
根据django model自动生成对应的REST API接口,减少重复工作

## Installation
```
git clone https://github.com/xiaomiba0904/rest_api_auto

cd rest_api_auto

pip install -r requirements.txt

python setup install
```

## Usage

1. `INSTALLED_APPS`中添加`rest_api_auto`
    ```
    INSTALLED_APPS = [
        ...
        'rest_api_auto',
    ]
    ```

2. model添加注册装饰器`register_model`
    ```python
    from django.db import models
    from rest_api_auto.decorators import register_model
    
    @register_model()
    class MoDemo(models.Model):
        name = models.CharField(max_length=16)
        age = models.IntegerField()
        address = models.CharField(max_length=256)
        is_admin = models.BooleanField(default=False)
    
    ```
3. url.py添加`urls`
    ```python
    from django.contrib import admin
    from django.urls import path, include
    
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('api/', include('rest_api_auto.urls'))
    ]
    ```
    
4. 运行django
    ```
    python manage.py runserver
    ```
    
5. 使用 url
    ```python
    >>> data = {"name": "xiaomiba", "age": 18, "address": "China"}
    >>> post_response = requests.post("http://127.0.0.1:8000/api/app_name/model_name/", data=data)
    >>> post_response
    <Response [201]>
    >>> post_response.json()
    {'id': 1, 'name': 'xiaomiba', 'age': 18, 'address': 'China', 'is_admin': False}
    
    >>> list_response = requests.get("http://127.0.0.1:8000/api/app_name/model_name/")
    >>> list_response.json()
    {'code': 200,
     'count': 1,
     'next': None,
     'previous': None,
     'results': [{'id': 1,
       'name': 'xiaomiba',
       'age': 18,
       'address': 'China',
       'is_admin': False}]}
       
    >>> get_response = requests.get("http://127.0.0.1:8000/api/app_name/model_name/1/")
    >>> get_response.json()
    {'id': 1, 'name': 'xiaomiba', 'age': 18, 'address': 'China', 'is_admin': False}

    >>> del_response = resquest.delete("http://127.0.0.1:8000/api/app_name/model_name/1/")
    >>> del_response
    <Response [204]>
    ```
    url路径参数为： 前缀 / app名称 / model名称 /
   
    如果需要修改路径可以在`register_model`函数的`name`参数指定,如
    `register_model(name="user.info")`，访问的url: `http://127.0.0.1:8000/api/user/info/`
    
    