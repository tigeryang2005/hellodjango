from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from . import models
import time
import os
import traceback
import logging
logger = logging.getLogger('log')


# Create your views here.


def del_book(request, book_id):
    try:
        book = models.Books.objects.get(id=book_id)
        os.remove('.' + book.img_url)
        book.delete()
    except:
        logger.error(traceback.format_exc())
    return redirect('list_book')


def list_book(request):
    data = models.Books.objects.all()
    context = {'data': data}
    return render(request, 'books/list.html', context)


def add_book(request):
    # 判断当前的请求方式，如果是get只返回html 如果是post则添加数据
    if request.method == 'GET':
        return render(request, 'books/add.html')
    else:
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken')

        # 处理上传的文件
        img_url = img_upload(data, request)
        if img_url:
            data['img_url'] = img_url[1:]
        else:
            data.pop('img_url')

        try:
            book = models.Books(**data)
            book.save()
            return redirect(reverse('list_book'))
        except:
            os.remove(img_url)
            logger.error(traceback.format_exc())
            return redirect(reverse('add_book'), {'add_failed': '添加数据失败'})


def img_upload(data, request):
    file = request.FILES.get('img_url', None)
    if file:
        file_path = './static/uploads/' + data.get('name') + str(int(time.time())) + '.' + file.name.split('.').pop()
        try:
            with open(file_path, mode='wb+') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            return file_path
        except:
            logger.error(traceback.format_exc())
            return None
    else:
        return None


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
    return render(request, 'athena_templates/demo.html')


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
