# conding=utf-8
import time
import calendar

ticks = time.time()
print('当前时间戳为：', ticks)

localtime = time.localtime()

print("本地时间为：", localtime)

asctime = time.asctime(time.localtime(time.time()))

print(asctime)

print(">>>>>>>>>>>>>>>>>>>>")

print(time.strftime("%Y-%m-%d %H:%M:%S"))

print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

a = "Sat Mar 28 22:24:24 2016"
print (time.mktime(time.strptime(a,"%a %b %d %H:%M:%S %Y")))

cal = calendar.month(2019,5)
print(cal)


