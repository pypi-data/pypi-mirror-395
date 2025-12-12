# 获取目录信息：(文件的总大小,文件个数，子文件夹个数)
#  不存在的目录，返回None
#  存在的目录，返回3个元素的元组
import os
import shutil
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)
@dataclass
class DirInfoRet:
    """目录信息结果对象  来自 dir_info()方法的返回值"""
    all_size: int
    """文件总大小"""
    file_count: int
    """文件总数"""
    subdir_count: int
    """子文件夹数"""
    def format_size(self):
        size1 = self.all_size
        return format_size(size1)

def format_size(size1):
    """返回格式化的文件大小，如 B, KB, MB, GB """
    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    for unit in units:
        if size1 < 1024.0 or unit == units[-1]:
            return f"{size1:.2f} {unit}"
        size1 /= 1024.0
    pass

def dir_info(root_dir: str)->DirInfoRet:
    """
    获取目录信息元组：(文件的总大小,文件个数，子文件夹个数)
    :param root_dir: 根目录
    :return:
    """
    while True:
        # 检查参数 路径是否存在
        if not os.path.exists(root_dir):
            return DirInfoRet(0,0,0)
        # 检查参数 路径是否为文件
        if os.path.isfile(root_dir):
            return DirInfoRet(os.path.getsize(root_dir),1,0)

        size = 0
        file_count = 0
        subdir_count = 0
        for cur_dir,sub_dirs,files in os.walk(root_dir):
            file_count += len(files)
            subdir_count += len(sub_dirs)
            for name in files:
                fullname = os.path.join(cur_dir, name)
                if len(fullname) > 260:
                    logger.warning('文件路径名超长(%s)，%s', len(fullname), fullname)
                else:
                    size += os.path.getsize(fullname)
        return DirInfoRet(size,file_count,subdir_count)
    pass

def insert_path(path, inst_dir):
    """组合新路径 /a/b, c -> /a/c/b """
    absPath = os.path.abspath(path)
    pathTup = os.path.split(absPath)
    return os.path.join(pathTup[0], inst_dir, pathTup[1])

@dataclass
class MoveInsertPathRet:
    """移动到组合成的新路径 /a/b, c -> /a/c/b """
    success: bool
    """移动操作是否成功"""
    new_path: str
    """移动后的新路径"""
def move_insert_path(path,inst_dir):
    newdir = insert_path(path,inst_dir)
    if os.path.exists(path):
        try:
            shutil.move(path,newdir)
        except Exception as e:
            logger.warning('文件夹移动操作异常 %s，'+str(e),path)
            return MoveInsertPathRet(False, newdir)

        return MoveInsertPathRet(True,newdir)
    else:
        return MoveInsertPathRet(False,newdir)
def join(*paths):
    """与os.path.join 类似，担忧以下不同：
        1，遇到/或'\\\\'开头的路径段，会忽略前面参数的路径前缀
        2，遇到\和/混合使用时， 原始版本，原样处理， 本方法：会统一转为平台相关的分隔符
    """
    new_paths = []
    for path in paths:
        path = path.removeprefix("/")
        path = path.removeprefix("\\")
        new_paths.append(os.path.normpath(path))
    # print(new_paths,paths)
    return os.path.join(*new_paths)
def join_slash(*paths):
    """将路径片段组合后，强制按照/作为路径分隔符 """
    return join(*paths).replace("\\","/")


if __name__ == '__main__':
    abc = DirInfoRet(104, 1, 0).format_size()
    print(abc)