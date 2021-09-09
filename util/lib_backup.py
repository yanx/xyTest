
import os
from os.path import join, splitext, split, exists
import shutil
from shutil import copyfile
import time

# THIS_LIB = ["/Users/yanxin/eclipse-workspace/vicuna_base/vicuna_root", "/Users/yanxin/eclipse-workspace/dev_base"]
THIS_LIB = ["/Users/yanxin/eclipse-workspace/vicuna_base/vicuna_root", "/Users/yanxin/eclipse-workspace/vicuna_base/view_root"]
THIS_BACKUP = "/Users/yanxin/Downloads/yan_doc/lib_backup"

def backup_lib():

#     name_folder = "lib_" + time.strftime("%Y%m%d_%H%M%S", time.localtime(time.time()))
    name_folder = "lib_" + time.strftime("%Y%m%d", time.localtime(time.time()))

    path_folder = join(THIS_BACKUP, name_folder )
    print ("backup to " + path_folder)
    
    if os.path.isdir(path_folder):
        shutil.rmtree(path_folder)
    
    time.sleep(5)
    for item in THIS_LIB:
        copy_directory(item, path_folder)


def copy_directory(source, target):
    if not os.path.exists(target):
        os.mkdir(target)

    for root, dirs, files in os.walk(source):
        for di in ['.svn' , '.git', '__pycache__']:
            if di in dirs:
                dirs.remove(di)

        for file in files:
            if splitext(file)[-1] in ('.pyc', '.pyo', '.fs', '.log'):
                continue

            from_ = join(root, file)
            to_ = from_.replace(source, target, 1)
            to_directory = split(to_)[0]
            if not exists(to_directory):
                os.makedirs(to_directory)
            copyfile(from_, to_)
            

if __name__ in '__main__':
    backup_lib()
