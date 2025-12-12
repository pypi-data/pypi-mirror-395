from os import walk, listdir
from os.path import splitext, basename, abspath, join, isdir, isfile
from natsort import natsorted, ns

class FileFolderPath:
    def __init__(self, 路径):
        self.路径 = 路径
        self.名称 = basename(路径)
        self.后缀 = splitext(self.路径)[1]
        self.名称不含后缀 = splitext(basename(路径))[0]
        self.路径不含后缀 = splitext(路径)[0]
        self.绝对路径 = abspath(self.路径)
        self.是文件 = isfile(self.路径)
        self.是文件夹 = isdir(self.路径)

    def 所有文件(self,筛选后缀 = None):
        """
        :param 筛选后缀: 如'xlsx'
        """
        # 遍历目录，并获取所有文件的绝对路径
        所有文件列表 = []
        for root, dirs, files in walk(self.路径):
            for file in files:
                if file.startswith('~$'): continue
                if 筛选后缀 and not file.endswith(筛选后缀):
                    continue
                所有文件列表.append(join(root, file))
        所有文件列表 = natsorted(所有文件列表, alg=ns.PATH)
        return [FileFolderPath(x) for x in 所有文件列表]

    def 所有文件夹(self):
        # 遍历目录，并获取所有文件夹的绝对路径
        所有文件夹列表 = []
        for root, dirs, files in walk(self.路径):
            for dir_name in dirs:
                所有文件夹列表.append(join(root, dir_name))
        所有文件夹列表 = natsorted(所有文件夹列表, alg=ns.PATH)
        return [FileFolderPath(x) for x in 所有文件夹列表]

    def 文件(self,筛选后缀 = None):
        """
        :param 筛选后缀: 如'.xlsx'
        :return: 当前目录所有文件
        """
        # 遍历当前目录，找出所有文件
        当前目录所有文件列表 = []
        for dir_name in listdir(self.路径):
            if dir_name.startswith('~$'):continue
            dir_path = join(self.路径, dir_name)
            if isfile(dir_path):
                if 筛选后缀 and not dir_path.endswith(筛选后缀):
                    continue
                当前目录所有文件列表.append(abspath(dir_path))
        当前目录所有文件列表 = natsorted(当前目录所有文件列表, alg=ns.PATH)
        return [FileFolderPath(x) for x in 当前目录所有文件列表]

    def 文件夹(self):
        """
        :return: 当前目录所有文件夹
        """
        # 遍历当前目录，找出所有文件夹
        当前目录所有文件夹列表 = []
        for dir_name in listdir(self.路径):
            dir_path = join(self.路径, dir_name)
            if isdir(dir_path):
                当前目录所有文件夹列表.append(abspath(dir_path))
        当前目录所有文件夹列表 = natsorted(当前目录所有文件夹列表, alg=ns.PATH)
        return [FileFolderPath(x) for x in 当前目录所有文件夹列表]

    def __call__(self,文件后缀 = None):
        """
        :param 文件后缀: 如'xlsx'；传入True，则返回所有文件和文件夹路径
        :return: 当前目录所有文件路径；传入True，则返回所有文件和文件夹路径
        """
        if 文件后缀 == True:
            return [x.绝对路径 for x in self.文件()] + [x.绝对路径 for x in self.文件夹()]
        return [x.绝对路径 for x in self.文件(文件后缀)]

    def __str__(self):
        return self.路径
