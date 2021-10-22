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


def update_book(request):
    data = request.POST.dict()
    data.pop('csrfmiddlewaretoken')
    # 判断是否更新图片
    file = request.FILES.get('img_url', None)
    book = models.Books.objects.get(id=data.get('id'))
    if file:
        file_name = img_upload(data, request)
        if file_name:
            data['img_url'] = file_name[1:]
        else:
            data.pop('img_url')
        os.remove('.' + book.img_url)
    else:
        data['img_url'] = book.img_url
    models.Books.objects.filter(id=data.get('id')).update(**data)

    return HttpResponse('更新')


def edit_book(request):
    id = request.GET.get('id')
    book = models.Books.objects.get(id=id)
    return render(request, 'books/edit.html', {'book': book})


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
    # data = models.Student.objects.all()
    # print(data)
    # for s in data:
    #     print(s.name)
    # data = models.Student.objects.get(pk=1)
    # print(data.name)
    # data = models.Student.objects.filter(sex='0')
    # for s in data:
    #     print(s.sex)
    # student_data = {
    #     'name': '王五',
    #     'age': 18,
    #     'sex': '0',
    #     'address': '山西'
    # }
    # # 一对一模型添加
    # student = models.Student(**student_data)
    # student.save()
    # student = models.Student.objects.get(pk=2)
    # student_info = {
    #     'sid': student,
    #     'xueli': '硕士',
    #     'phone': '13888888888'
    # }
    # student_info_obj = models.StuInfo(**student_info)
    # student_info_obj.save()
    # student = models.Student.objects.first()
    # print(student.name)
    # print(student.stuinfo.phone)
    # student_info = models.StuInfo.objects.first()
    # print(student_info.xueli)
    # print(student_info.sid.name)
    # 一对多关系  存
    # b_obj = models.BanJi(name='二班')
    # b_obj.save()
    #
    # student = models.Student(name='赵六', bid=b_obj)
    # student.save()
    # 一对多关系 查询
    # b_obj = models.BanJi.objects.first()
    # print(b_obj.name)
    # print(b_obj.student_set.all())
    # for s in b_obj.student_set.all():
    #     print(s.name)
    #     print(s.stuinfo.xueli)
    #     print(s.bid.name)
    # 添加多对多关系
    # t1 = models.Teacher(name='王老师')
    # t2 = models.Teacher(name='张老师')
    # t1.save()
    # t2.save()
    # b_objects = models.BanJi.objects.all()
    # t1.bid.set(b_objects)
    # b_object = models.BanJi.objects.last()
    # t2.bid.add(b_object)
    # s_obj = models.Student.objects.first()
    # print(s_obj.bid.name)
    # 多对多查询
    print(models.Teacher.objects.first().bid.all())
    print(models.BanJi.objects.last().teacher_set.all())
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
