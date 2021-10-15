from django.shortcuts import render
from django.http import HttpResponse
from . import models
# Create your views here.


def add_book(request):
    return render(request, 'books/add.html')


def demo(request):
    # 添加数据的一种方式
    # student = models.Student()
    # student.name = '张三'
    # student.age = 24
    # student.sex = '1'
    # student.address = '天津'
    # s = student.save()
    # print(s, type(s))
    # 添加数据的另一种方式
    # data = {'name': '李四', 'age': 21, 'sex': '0', 'address': '天津'}
    # student = models.Student(**data)
    # student.save()
    # 查询数据
    data = models.Student.objects.all()
    print(data)
    for s in data:
        print(s.name)
    data = models.Student.objects.get(pk=1)
    print(data.name)
    data = models.Student.objects.filter(sex='0')
    for s in data:
        print(s.sex)
    return HttpResponse('模型类的测试')


# 字符串返回
def hello_world(request):
    return HttpResponse('hello world!')


# 模板返回
def index(request):
    return render(request, 'athena_templates/index.html', {'welcome': 'hello'})


# 接收url中的一部分参数
def index_year(request, year):
    return render(request, 'athena_templates/index.html', {'year': year})


def index_year_month(request, year, month):
    return render(request, 'athena_templates/index.html', {'year': year, 'month': month})
