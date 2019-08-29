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
    
