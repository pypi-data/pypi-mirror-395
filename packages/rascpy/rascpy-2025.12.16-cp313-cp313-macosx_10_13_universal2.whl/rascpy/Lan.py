# -*- coding: utf-8 -*-
from .Lan_CHN import CHN
from .Lan_EN import EN
import locale

'''
通过改变lan的值，就可以实现语言的切换
例：加入德语的方法
from Lan_GER import GER
lan = GER

'''

if locale.getdefaultlocale()[0] == 'zh_CN':
    lan = CHN
else:
    lan = EN
    
# lan = your_lang