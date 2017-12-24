from django.shortcuts import render,HttpResponse,redirect
from app01 import models
from app01.form import SignForm,Loginform
from django.db.models import Count
import json

def index(request,*args,**kwargs):#取url中的typeid
    if request.method=='GET':
        type_id = int(kwargs.get('type_id')) if kwargs.get('type_id') else None
        #后台都是get传参
        if type_id:
            # article_list = models.Article.objects.filter(article_type_id=type_id).values('blog__user__username','title','summary','read_count','comment_count','create_time')
            article_list = models.Article.objects.filter(article_type_id=type_id).extra(select={'c': "strftime('%%Y-%%m',create_time)"})
        else:
            article_list = models.Article.objects.all().extra(select={'c': "strftime('%%Y-%%m',create_time)"})
        type_choice_list = models.Article.type_choices#分类的
        # print(type_choice_list)#[(1, 'Python'), (2, 'Linux'), (3, 'OpenStack'), (4, 'GoLang')]
        count=article_list.count()#分页
        from utils.page import PageInfo
        # 获取当前URL
        # print(request.path_info)
        page_info = PageInfo(request.GET.get('page'), count, 5, request.path_info, 11)
        rel_article_list=article_list[page_info.start():page_info.end()]
        return render(request,'index.html',{'type_choice_list':type_choice_list,'type_id':type_id,'article_list':rel_article_list,
                                            'page_info':page_info})
    else:
        import json
        ret = {'status': True}
        try:
            del request.session['username']
        except:
            ret['status']=False
        return HttpResponse(json.dumps(ret))

# from django.core.exceptions import NON_FIELD_ERRORS
def login(request):
    if request.session.get('username'):
        print(request.session)
        return redirect('/' + request.session.get('username'))
    else:
        if request.method == "GET":
            obj=Loginform(request)
            return render(request,'login.html',{'obj':obj})
        else:
            obj=Loginform(request,request.POST)
            if obj.is_valid():
                user_mes=models.UserInfo.objects.filter(**obj.cleaned_data).first()
                # print(user_mes.nid)
                if user_mes:
                    request.session['username']=request.POST.get('username')
                    request.session['user_id']=user_mes.nid
                    return redirect('/'+request.POST.get('username'))
                else:
                    return render(request, 'login.html', {'obj': obj,'msg':'用户名或密码错误'})
            # print(obj.errors[NON_FIELD_ERRORS])
            return render(request, 'login.html', {'obj': obj})
            # print(obj.cleaned_data.get('password'))

def check_code(request):
    from io import BytesIO
    from utils.random_check_code import rd_check_code
    img,code = rd_check_code()
    stream = BytesIO()#开辟一个内存空间，类似于文件句柄
    print(stream)#io空间，<_io.BytesIO object at 0x06D6EAE0>
    print(img)#pillow生成的图片对象
    img.save(stream,'png')
    print(stream)
    print(stream.getvalue())#bytes类型的图片信息，返回前端生成图片
    print(img)
    request.session['code'] = code#将生成的随机字符串存到session用于验证
    return HttpResponse(stream.getvalue())

import os
def signup(request):
    if request.method =='GET':
        obj=SignForm(request)
        return render(request,'signup.html',{'obj':obj})
    else:
        obj=SignForm(request,request.POST,request.FILES)
        if obj.is_valid():
            obj.cleaned_data.pop('password2')

            print(obj.cleaned_data.get('avatar'))
            with open(os.path.join('/static/imgs/', obj.cleaned_data.get('avatar').name), 'wb') as file:
                all = obj.cleaned_data.get('avatar').chunks()  # 拿到整个文件
                for trunk in all:
                    file.write(trunk)
                file.close()
            obj.cleaned_data['avatar'] = os.path.join('/static/imgs/', obj.cleaned_data.get('avatar').name)
            models.UserInfo.objects.create(**obj.cleaned_data)
            return redirect('/')
        else:
            return render(request,'signup.html',{'obj':obj})

def home(request,site):
    if request.session.get('username'):#只有登陆的人可以看主页
        blog = models.Blog.objects.filter(site=site).first()
        if blog:
            cate_list = models.Article.objects.filter(blog=blog).values('category__nid', 'category__title',
                                                                        'blog__site').annotate(c=Count('nid'))
            tag_list = models.Article2Tag.objects.filter(article__blog=blog).values('tag__nid','tag__title','tag__blog__site').annotate(co=Count('id'))
            date_list = models.Article.objects.filter(blog=blog).extra(select={'c': "strftime('%%Y-%%m',create_time)"}).values('c','blog__site').annotate(ct=Count('nid'))
            article_list=models.Article.objects.filter(blog=blog)
            return render(request,'home.html',{'cate_list':cate_list,'article_list':article_list,'blog':blog,'tag_list':tag_list,'date_list':date_list})
        return redirect('/')
    else:
        return HttpResponse('登陆已过期，请重新登陆')

def category(request,site,num):
    '''
    随笔分类
    :param request:
    :param site:
    :param num:
    :return:
    '''
    print(num)
    blog = models.Blog.objects.filter(site=site).first()
    cate_list=models.Article.objects.filter(blog=blog).values('category__nid','category__title','blog__site').annotate(c=Count('nid'))
    tag_list = models.Article2Tag.objects.filter(article__blog=blog).values('tag__nid', 'tag__title',
                                                                            'tag__blog__site').annotate(co=Count('id'))
    article_list = models.Article.objects.filter(category_id=num,blog=blog).all()
    return render(request,'home.html',{'cate_list':cate_list,'article_list':article_list,'blog':blog,'tag_list':tag_list})


def tag(request,site,num):
    '''
    标签分类
    :param request:
    :param site:
    :param num:
    :return:
    '''
    print(num)
    blog = models.Blog.objects.filter(site=site).first()
    cate_list = models.Article.objects.filter(blog=blog).values('category__nid', 'category__title',
                                                                'blog__site').annotate(c=Count('nid'))
    tag_list = models.Article2Tag.objects.filter(article__blog=blog).values('tag__nid', 'tag__title',
                                                                            'tag__blog__site').annotate(co=Count('id'))
    article_list = models.Article.objects.filter(blog=blog,article2tag__tag_id=num).all()
    return render(request,'home.html',{'tag_list':tag_list,'article_list':article_list,'blog':blog,'cate_list':cate_list})

# date_list = models.Article.objects.filter(blog=blog).extra(select={'c': "strftime('%%Y-%%m',create_time)"}).values('c').annotate(ct=Count('nid'))

def filter(request,site,key,val):
    # print(site)
    # print(key)
    # print(val)
    '''
    随笔，标签和时间分类
    :param request:
    :param site:
    :param key:
    :param val:
    :return:
    '''
    blog = models.Blog.objects.filter(site=site).first()
    date_list = models.Article.objects.filter(blog=blog).extra(select={'c': "strftime('%%Y-%%m',create_time)"}).values(
        'c', 'blog__site').annotate(ct=Count('nid'))
    cate_list = models.Article.objects.filter(blog=blog).values('category__nid', 'category__title',
                                                                'blog__site').annotate(c=Count('nid'))
    tag_list = models.Article2Tag.objects.filter(article__blog=blog).values('tag__nid', 'tag__title',
                                                                            'tag__blog__site').annotate(
        co=Count('id'))
    if key == 'category':
        article_list = models.Article.objects.filter(category_id=val, blog=blog).all()
    elif key=='tag':
        article_list = models.Article.objects.filter(blog=blog, article2tag__tag_id=val).all()
    elif key=='date':
        article_list = models.Article.objects.filter(blog=blog).extra(where=["strftime('%%Y-%%m',create_time)=%s"],params=[val,]).all()
        print(article_list.query)
    return render(request, 'home.html',
                  {'cate_list': cate_list, 'article_list': article_list, 'blog': blog, 'tag_list': tag_list,
                   'date_list': date_list})

def article(request,site,nid):
    blog = models.Blog.objects.filter(site=site).first()
    date_list = models.Article.objects.filter(blog=blog).extra(select={'c': "strftime('%%Y-%%m',create_time)"}).values(
        'c', 'blog__site').annotate(ct=Count('nid'))
    cate_list = models.Article.objects.filter(blog=blog).values('category__nid', 'category__title',
                                                                'blog__site').annotate(c=Count('nid'))
    tag_list = models.Article2Tag.objects.filter(article__blog=blog).values('tag__nid', 'tag__title',
                                                                            'tag__blog__site').annotate(
        co=Count('id'))
    content=models.Article.objects.filter(blog=blog,nid=nid).values('articledetail__content','up_count','down_count',
                                                                    'nid','comment__content','comment__reply__user__username','comment__user__username',
                                                                    'comment__create_time')
    print(content)
    return render(request, 'article.html',
                  {'cate_list': cate_list, 'blog': blog, 'tag_list': tag_list,'content':content.first(),
                   'date_list': date_list,'reply':content})

def updown(request):
    # 是谁？文章?赞或踩 1赞，0踩
    # 是谁？当前登录用户，session中获取
    # 文章？
    response = {'status':True,'msg':None}
    try:
        user_id = request.session.get('user_id')
        article_id = request.POST.get('nid')
        val = int(request.POST.get('val'))#val代表踩或者赞
        obj = models.UpDown.objects.filter(article_id=article_id,user_id=user_id).first()
        if obj:
            # 已经赞或踩过
            pass
        else:
            # print(obj)
            # print(article_id)
            # print(val)
            from django.db import transaction#支持原子性事务
            from django.db.models import F
            with transaction.atomic():
                if val:
                    models.UpDown.objects.create(user_id=user_id,article_id=article_id,up=True)
                    models.Article.objects.filter(nid=article_id).update(up_count=F('up_count')+1)
                else:
                    models.UpDown.objects.create(user_id=user_id,article_id=article_id,up=False)
                    models.Article.objects.filter(nid=article_id).update(down_count=F('down_count')+1)
    except Exception as e:
        response['status'] = False
        response['msg'] = str(e)

    return HttpResponse(json.dumps(response))