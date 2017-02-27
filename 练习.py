from functools import wraps

def deco(func):
    def sub_deco(a,b):
        print('before func')
        s=func(a,b)
        print('after func')
        return s
    return sub_deco

@deco
def f(a,b):
    print('i am func,%d,%d' % (a,b))
    return a+b

s=f(2,3)
print(s)

print('-'*20)
# 带参数
def deco2(f):
    def sub_deco2(*args,**kwargs):
        print('before f')
        res=f(*args,**kwargs)
        print('after f %s' % (f.__name__))
        print('after f %s' % (f.__dict__))
        return res
    return sub_deco2

@deco2
def zdy(a,b,c):
    print(str(a+b+c)+', i am f')
    return a+b+c
r=zdy(a=1,b=1,c=1)
print(r)

print('-'*20)
# 让装饰器带参数
def deco3(arg):
    def sub_deco3(f):
        def thd_deco3(*args,**kwargs):
            print('before 让装饰器带参数')
            print(arg)
            res = f(*args,**kwargs)
            print('after f')
            return res
        return thd_deco3
    return sub_deco3

@deco3('zz')
def f(a='xx',b='aa'):
    print(a+b)
    return a+b

res=f()
print(res)
print(type(res))


print('-'*20)
# 让装饰器带 类
class locker():
    def __init__(self):
        print('这是我的__init__方法被调用')
    @staticmethod
    def acquire():
        print('上锁')
    @staticmethod
    def release():
        print('解锁')

def deco4(cls):
    def sub_deco(f):
        def thd_deco():
            print('before %s called %s' % (f.__name__,cls))
            cls.acquire()
            try:
                return f()
            finally:
                cls.release()
        return thd_deco
    return sub_deco

@deco4(locker)
def f():
    print('我是f')
# f()
print('-'*20)

def my_decorator(f):
    @wraps(f)
    def wraper(*args,**kwargs):
        print('Calling decorator')
        return f(*args,**kwargs)
    return wraper

@my_decorator
def example():
    '''这是文档'''
    print('Called example function')

example()
print(example.__name__)
print(example.__doc__)

print('-'*20)

def my_decirator2(f):
    def wraper(*args,**kwargs):
        print('Calling decorator')
        return f(*args,**kwargs)
    return wraper
@my_decirator2
def example2():
    '''这是文档2'''
    print('Calling example2 function')
example2()
print(example2.__name__)
print(example2.__doc__)
