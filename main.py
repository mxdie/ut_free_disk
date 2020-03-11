import ctypes
import os
import platform
import sys
import shutil
import json
import time
class ut_free_disk:
    #初始化 初始化后 ->free_disk() -> insert_file()
    def __init__(self, path:str, disk:str ,min_size:int, target_size:int):
        '''
        path: 文件路径 例如：'C:\\xxx'
        disk: 盘符 例如 'D'
        min_size: 磁盘清理阈值 GB
        target_size: 磁盘清理目标值 GB
        '''
        self.path = path 
        self.disk = disk+':\\'
        self.min_size = min_size*1024*1024*1024
        self.target_size = target_size*1024*1024*1024
        self.free_disk()
        self.insert_file()

    # 判断空间是否低于阈值，低于阈值就从小到大清理之前的文件,直到达到目标
    def free_disk(self):
        cur_free = self.get_free_space()
        if cur_free > self.min_size:
            return
        with open('data.json','r') as f:
            curDict = json.load(f)
        target_free = self.target_size - cur_free
        file_list = sorted([int(x) for x in curDict])
        ready_free = []
        ready_free_size = 0
        for file_size in file_list:
            ready_free.append(str(file_size))
            ready_free_size += file_size
            if(ready_free_size>=target_free):
                break
        for del_file in ready_free:
            if self.delete_file(curDict[del_file]):
                del curDict[del_file]
                time.sleep(10)
        with open('data.json','w') as f:
            json.dump(curDict,f)

    #获取磁盘可用空间
    def get_free_space(self)->int:
        '''
        return:剩余空间大小 kb
        '''
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(self.disk), None, None, ctypes.pointer(free_bytes))
        return int(free_bytes.value)

    #删除文件或目录
    def delete_file(self, path: str)->bool:
        '''
        path:待删除的文件或文件夹路径 如'C:\\'
        return:是否已删除
        '''
        if os.path.exists(path):
            try:
                if os.path.isfile(path):
                    os.remove(path)
                else:
                    shutil.rmtree(path)
            except:
                return False
        return True
    
    #获取文件或目录大小
    def get_size(self, path: str)->int:
        '''
        path:文件或文件夹路径 如'C:\\'
        return:文件或文件夹大小 kb
        '''
        total_size = 0
        if not os.path.exists(path):
            return total_size
        if os.path.isfile(path):
            total_size = os.path.getsize(path)
        else:
            with os.scandir(path) as dir_list:
                for cur_dir in dir_list:
                    cur_dir_path = os.path.join(path, cur_dir.name)
                    if cur_dir.is_dir():
                        total_size += self.get_size(cur_dir_path)
                    else:
                        total_size += os.path.getsize(cur_dir_path)
        return int(total_size)
    
    #将文件插入data.json中
    def insert_file(self):
        cur_size = self.get_size(self.path)
        with open('data.json','r') as f:
            curDict = json.load(f)
        while(str(cur_size) in curDict):
            cur_size += 1
        curDict[str(cur_size)] = self.path
        with open('data.json','w') as f:
            json.dump(curDict,f)

if __name__ == "__main__":
    path =   sys.argv[1].replace('&','\\')
    ut_free_disk(path,'d',200,500)
