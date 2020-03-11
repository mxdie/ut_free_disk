# ut_free_disk
又来生产辣鸡了o(*￣︶￣*)o在ut刷刷刷时维护磁盘空间  
只会删除使用本脚本注册的文件  
没有log 没有print 无脑递归删除 甚至我自己都没测试完 胆小不要碰 _(:з」∠)_  

## 1 进入main.py
`ut_free_disk(path:str, disk:str ,min_size:int, target_size:int)`  
path:文件路径，由ut传入，不用管  
disk:下载盘符，自行修改  
min_size:磁盘可用空间最小阈值，小于这个值开始从小到大删文件，自行修改，单位GB  
target_size:磁盘可用空间目标值，开始删文件后删到这个大小才会停，自行修改，单位GB  

## 2 进入start.bat
`cd /d %~dp0`  
修改`/d`为本文件所在盘符

## 3 进入ut
设置->高级->运行程序  
将`D:\ut_free_disk\start.bat "%D&%F"`填入下载完成后运行此程序，目录需自行修改

## 执行流程
下载完成  
->(文件路径)->执行start.bat  
->(文件路径)->执行main.py  
->判断磁盘剩余空间　  
->(低于阈值)  
　　->读取data.json中的文件信息  
　　->从小到大删除直到剩余空间大于目标值  
->将文件信息插入data.json  
->结束　　  
  
