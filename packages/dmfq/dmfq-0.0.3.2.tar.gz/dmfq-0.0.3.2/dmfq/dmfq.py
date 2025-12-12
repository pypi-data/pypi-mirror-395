import numpy as np
import torch
import os
import glob
from os.path import join,basename,dirname,abspath,expanduser,isdir,isfile
import logging
import inspect
import socket
import pandas as pd


'''
https://www.barwe.cc/2022/06/24/dist-my-pkg-to-pypi

'''
# import logging
# logger = logging.getLogger('base')



from datetime import datetime
def get_timestamp():
    '''
    from datetime import datetime
    '''
    return datetime.now().strftime('%Y%m%d_%H%M%S')  # str: '20240418-221535'
# print(f"==>> get_timestamp(): {get_timestamp()}")

def seconds_to_hms(seconds):
    '''
    # print(seconds_to_hms(86400))  # 输出: 24:00:00
    # print(seconds_to_hms(150000)) # 输出: 41:40:00
    # print(seconds_to_hms(4000))   # 输出: 1:06:40
    '''
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:d}:{minutes:0>2d}:{seconds:0>2d}" 
# print(f"==>> get_timestamp(): {get_timestamp(100.5)}")


DELIMITER_INFO=None

def get_info_numpy(varNp):

    # print("".center(50, "-"))
    print(f"np shape: {varNp.shape} , min ~ max: {varNp.min():.4f} ~ {varNp.max():.4f} , dtype: {varNp.dtype}, mean:{varNp.mean():.8f}")
    
    # a = 10.0001
    # print(f'{a:.4g}')   # g:  https://www.cnblogs.com/fat39/p/7159881.html
    # print('%.7g' % 1111.1111) 

    # print(f"==>> varNp: {varNp}")
    # plt.hist(arrayNp.ravel(), bins='auto')
    # plt.ylim(10000)
    # plt.hist(arrayNp.ravel(), bins=255)
    # plt.show()
    # plt.close()

def get_info_tensor(varTorch):

    # print("".center(50, "-"))
    print(f"{varTorch.shape} , min~max: {varTorch.min():.4f} ~ {varTorch.max():.4f} , device: {varTorch.device} , dtype is :{varTorch.dtype} , mean: {varTorch.float().mean():.8f}")
    # tensor shape: 

    # plt.hist(arrayNp.ravel(), bins='auto')
    # plt.ylim(10000)
    # plt.hist(arrayNp.ravel(), bins=255)
    # plt.show()
    # plt.close()


def get_info_tuple(a_tuple=None):
    print(f"==>> type: tuple;    len(a_tuple): {len(a_tuple)}")
    if len(a_tuple)>0:
        # print(f"==>> a_list[0]: {a_list[0]}")
        if isinstance(a_tuple[0], np.ndarray):
            get_info_numpy(a_tuple[0])
        elif isinstance(a_tuple[0], torch.Tensor):
            get_info_tensor(a_tuple[0])


def get_info_list(a_list=None):
    print(f"==>> type: list;    len(a_list): {len(a_list)}")
    if len(a_list)>0:
        # print(f"==>> a_list[0]: {a_list[0]}")
        if isinstance(a_list[0], np.ndarray):
            get_info_numpy(a_list[0])
        elif isinstance(a_list[0], torch.Tensor):
            get_info_tensor(a_list[0])


def get_info_dict(a_dict=None):
    # a_dict = {'a':1,'b':np.array([1,2]),'c':[4,2]}
    count = 0
    for k, v in a_dict.items():
        print("".center(25, "="),f"keys num = {count}:",f" {k}: {type(v)} ","".center(25, "="))
        # print(f"key, type(value) is : {k}: {type(v)}")

        if type(v) in (int,float,complex):
            # print("".center(50, "-"))
            print(f"{k}: {v}")
        
        if isinstance(v, np.ndarray):
            get_info_numpy(v)
        
        if isinstance(v, torch.Tensor):
            get_info_tensor(v)

        if isinstance(v, tuple):
            # print("".center(50, "-"))
            print(f"len of tuple is: {len(v)}")
            for i in range(len(v)):
                print(f"==>> type(v[i]): {type(v[i])}")

        if isinstance(v, list):
            # print("".center(50, "-"))
            # print(f"len of list is: {len(v)}")
            # print(f"value is: {v}")
            get_info_list(v)

        if isinstance(v, dict):
            print(f"{k}:{v.keys()}")
        count+=1

def get_info(v):
    if isinstance(v, np.ndarray):
        get_info_numpy(v)
    elif isinstance(v, torch.Tensor):
        get_info_tensor(v)
    elif isinstance(v, list):
        get_info_list(v)
    elif isinstance(v, tuple):
        get_info_tuple(v)
    elif isinstance(v, dict):
        get_info_dict(v)
    else:
        print("Func get_info get unknown type!")





# get_dict_info(a_dict=None)
def get_dict_content(a_dict):
    for k, v in a_dict.items():
        print('## dict content:')
        print(f'  {k}:{v}')
        # print(f'  {a_dict.get(key)}')
# a = {'abc':1, 'e':np.array([1,2])}
# prt_dict_content(a)
        
def get_info_npz_file(npzPath):
    npzFile = np.load(npzPath)
    # print(npzFile.files)
    for k in npzFile.files:
        print(f'key: {k}')
        print(f"   {k}'s shape: {npzFile[k].shape}")
        print(f"   {k}'s dtype: {npzFile[k].dtype}")
        print(f"   {k}'s max  num: {npzFile[k].max()}")
        print(f"   {k}'s mean num: {npzFile[k].mean()}")
        print(f"   {k}'s min  num: {npzFile[k].min()}")

# get_info_npz_file('/home/hjy/workspace/interp_photo/04_inr/data/ERF/train_mini_ev_voxel_fp16/0001/1_4_events/04/00000_0t.npz')


def get_info_npy_file(npyPath):
    arrayNp = np.load(npyPath)
    get_info_numpy(arrayNp)


DELIMITER_WRITER_LOG=None


import os
from datetime import datetime
class txtWriter:
    def __init__(self, txt_path=None):    
        # a: 追加         w: 覆盖 
        self.txt_path = txt_path
        if os.path.exists(txt_path):
            archived_path = txt_path[:-4] + '_archived_' + datetime.now().strftime('%y%m%d-%H%M%S'+'.txt')
            print(f'## will rename {txt_path} to {archived_path}')
            os.rename(txt_path, archived_path)

            # print(f'## will remove {txt_path}')
            # os.remove(txt_path)
    
    def __call__(self, *args, **kwargs):
        output_str = ''.join(map(str, args))           # 将输出内容转换为字符串

        if self.txt_path:                               # 如果指定了输出文件名，则将输出内容写入文件
            with open(self.txt_path, 'a') as f:
                f.write(output_str + '\n')     

# txt_writer = txtWriter(txt_path='aaa.csv')     # 创建一个实例，指定输出文件路径
# txt_writer(123)
# txt_writer('abc')
# txt_writer(123,',',789)


import os
from datetime import datetime
import pandas as pd
class csvWriter_y:
    '''
    csv_writer = csvWriter_y(file_path="output_without_header.csv")
    for i in range(6):
        new_data = [i, i*10, i*20, i*30]
        csv_writer.write(new_data)
    '''
    def __init__(self, file_path):
        self.file_path = file_path
        self.current_row = 0
        self._initialize_csv()

    def _initialize_csv(self):
        csvWriter_y.rename_if_file_exists(self.file_path)
        os.makedirs(os.path.dirname(self.file_path),exist_ok=True)
        open(self.file_path, 'w').close()   # 创建空文件或清空现有文件
        self.current_row = 0                # 初始化时不包含header行

    def write(self, new_data):
        new_data_df = pd.DataFrame([new_data])          # 将新数据转换为 DataFrame
        new_data_df.to_csv(self.file_path, index=False, mode='a', header=False)  # 动态写入 CSV 文件
        self.current_row += len(new_data_df)            # 更新当前行数
        print("数据写入完成")

    def get_row_count(self):
        return self.current_row

    @staticmethod
    def rename_if_file_exists(file_path):
        if os.path.isfile(file_path):                   # 如果存在， 且为文件路径
            _, suffix = os.path.splitext(file_path)     # eg.  '.csv'
            backup_file_path = f"{file_path.rsplit('.', 1)[0]}-archived_{datetime.now().strftime('%Y%m%d_%H%M%S')}"+ suffix
            os.rename(file_path, backup_file_path)
            print(f"文件已存在，重命名为: {backup_file_path}")
        else:
            print(f'文件不存在: {file_path}')

# csv_writer = csvWriter_y(file_path="output_without_header.csv")
# for i in range(6):
#     new_data = [i, i*10, i*20, 'a'*i]
#     csv_writer.write(new_data)

import os
from datetime import datetime
import pandas as pd
# rename_if_file_exists('/home/hjy/ws/EvINR/utils_git/utils_print_log_excel/aaa/1111.txt')
# rename_if_folder_exists('/home/hjy/ws/EvINR/utils_git/utils_print_log_excel/aaa')

class xlsxWriter_y:
    '''
    powered by chatGPT and hjy
    example:
        # 定义第一行的说明字符串
        header = ["ID", "Value1", "Value2", "Value3"]
        out_excel_path = "output_with_header.xlsx"

        # 创建 ExcelWriter 实例
        excel_writer = ExcelWriter(out_excel_path, header)

        # 模拟循环体逐行获取数据并写入
        for i in range(6):  # 示例循环次数
            # 获取一行数据（这里用示例数据）
            new_data = [i, i*10, i*20, i*30]
            excel_writer.write(new_data)
    '''
    def __init__(self, file_path, header):
        self.file_path = file_path
        self.header = header
        self.current_row = 0
        self._initialize_excel()


    def _initialize_excel(self):
        xlsxWriter_y.rename_if_file_exists(self.file_path)

        # 初始化一个空的 DataFrame 并写入 header
        df = pd.DataFrame(columns=self.header)
        df.to_excel(self.file_path, index=False, engine='openpyxl')
        self.current_row = 1  # 初始化时包含header行

    def write(self, new_data):
        # 将新数据列表转换为字典
        new_data_dict = {self.header[i]: new_data[i] for i in range(len(new_data))}

        # 将新数据转换为 DataFrame
        new_data_df = pd.DataFrame([new_data_dict])
        # 动态写入 Excel 文件
        with pd.ExcelWriter(self.file_path, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:  #  overlay
            # 获取当前 Sheet 的最大行数，用于确定新数据的起始写入位置
            writer.sheets = {ws.title: ws for ws in writer.book.worksheets}
            startrow = self.current_row
            new_data_df.to_excel(writer, index=False, header=False, startrow=startrow)

        # 更新当前行数
        self.current_row += len(new_data_df)
        print("数据写入完成")

    def get_row_count(self):
        return self.current_row

    
    @staticmethod
    def rename_if_file_exists(file_path):
        if os.path.isfile(file_path):   # 如果存在， 且为文件路径
            _, suffix = os.path.splitext(file_path)   # eg.  '.csv'
            backup_file_path = f"{file_path.rsplit('.', 1)[0]}-archived_{datetime.now().strftime('%Y%m%d_%H%M%S')}"+ suffix
            os.rename(file_path, backup_file_path)
            print(f"文件已存在，重命名为: {backup_file_path}")
        else:
            print(f'文件不存在: {file_path}')

# # 定义第一行的说明字符串
# header = ["ID", "Value1", "Value2", "Value3"]
# out_excel_path = "output_with_header.xlsx"

# # 创建 ExcelWriter 实例
# excel_writer = xlsxWriter_y(out_excel_path, header)

# # 模拟循环体逐行获取数据并写入
# for i in range(6):  # 示例循环次数
#     # 获取一行数据（这里用示例数据）
#     new_data = [i, i*10, i*20, i*30]
#     excel_writer.write(new_data)


def setup_logger(logger_name:str, level=logging.INFO, toscreen=True, tofile=False, file_root:str=None, prefix:str=None):
    ''' set up logger
    example:
        setup_logger('base',
            level=logging.INFO,
            toscreen=True, 
            tofile=True,
            file_root='./', 
            prefix='test'
            )
        logger = logging.getLogger('base')
    '''

    logger = logging.getLogger(logger_name)
    formatter = logging.Formatter(f'%(asctime)s.%(msecs)03d - %(levelname)s {logger_name}: %(message)s',datefmt='%y-%m-%d %H:%M:%S')
    logger.setLevel(level)
    if toscreen:
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        logger.addHandler(sh)
    if tofile:
        log_file = os.path.join(file_root, prefix + '_{}.log'.format(get_timestamp()))
        os.makedirs(os.path.dirname(log_file),exist_ok=True)
        fh = logging.FileHandler(log_file, mode='w')
        fh.setFormatter(formatter)
        logger.addHandler(fh)





DELIMITER_PRINT=None

def print_list(a_list):
    frame = inspect.currentframe().f_back
    name_a_list=None
    for name, value in frame.f_locals.items():
        if value is a_list:
            name_a_list = name
    if name_a_list is not None:
        print(f'== {name_a_list} ==')
    for i, v in enumerate(a_list):
        if i<3 or i > len(a_list)-3:
            print(f"    {i}: {v}")
        elif i==3:
            print(f"    ...")

def print_list_all(a_list):
    frame = inspect.currentframe().f_back
    name_a_list=None
    for name, value in frame.f_locals.items():
        if value is a_list:
            name_a_list = name
    if name_a_list is not None:
        print(f'== {name_a_list} ==')
    for i, v in enumerate(a_list):
        print(f"        {i}: {v}")


def dict2str(opt, indent_l=1):
    '''dict to string for logger'''
    msg = ''
    for k, v in opt.items():
        if isinstance(v, dict):
            msg += ' ' * (indent_l * 2) + k + ':[\n'
            msg += dict2str(v, indent_l + 1)
            msg += ' ' * (indent_l * 2) + ']\n'
        else:
            msg += ' ' * (indent_l * 2) + k + ': ' + str(v) + '\n'
    return msg

def print_opt(opt):
    print('will print opt dict:')
    print(dict2str(opt))

DELIMITER_PATH=None


def get_host_name():
    hostname_str = socket.gethostname()
    return hostname_str

# print(f"==>> get_host_name(): {get_host_name()}")


def get_home_dir():
    '''
    from utils import getHomeDir
    '''
    home = os.path.expanduser("~")
    print(f'home path is {home}')
    return home



#%%
import glob
def get_folder_path_list(root, verbose=False):
    # folders_path_l = [join(data_root,f) for f in os.listdir(data_root) if isdir(join(data_root,f))]
    folders_path_l = [p for p in sorted(glob.glob(f'{os.path.expanduser(root)}/*')) if os.path.isdir(p)]
    if verbose:
        print(f"==>> folders_path_l: {folders_path_l}")
    return folders_path_l

def get_folder_name_list(root, verbose=False):
    folders_path_l = get_folder_path_list(root,verbose)
    folders_name_l = [os.path.basename(p) for p in folders_path_l]
    return folders_name_l


def get_file_path_list(root, suffix='.png', verbose=False):
    '''
    root='/home/hjy/data/ERF/test/0000/processed_images'
    suffix='.png'
    '''
    # files_path_l = [join(data_root,f) for f in os.listdir(data_root) if isfile(join(data_root,f))]
    files_path_l = [p for p in sorted(glob.glob(f'{os.path.expanduser(root)}/*{suffix}')) if os.path.isfile(p)]
    if verbose:
        # print(f"==>> files_path_l: {files_path_l}")
        print_list_all(files_path_l)
    return files_path_l

def get_file_name_list(root, suffix='.png', verbose=False):
    '''
    from dmfq
    '''
    files_path_l = get_file_path_list(root, suffix, verbose)
    files_name_l = [basename(p) for p in files_path_l]
    if verbose:
        print_list_all(files_name_l)
    return files_name_l


def get_file_path_list_intname(root, suffix='.png', prefix='', verbose=False):
    '''
    get_file_path_list_intname(in_root, suffix='.npz',prefix='r_')
    root='/home/hjy/data/Adobe240/frame/train/720p_240fps_1'
    suffix='.png'
    '''
    files_path_l = [p for p in sorted(glob.glob(f'{os.path.expanduser(root)}/*{suffix}')) if os.path.isfile(p)]
    files_path_l.sort(key=lambda x: int(  os.path.splitext(os.path.basename(x))[0].replace(prefix,'')))
    if verbose:
        # print(f"==>> imgs_path_list: {files_path_l}")
        print_list_all(files_path_l)
    return files_path_l
# get_file_path_list_intname(root='/home/hjy/workspace/interp_photo/04_inr/data/Adobe240/frame/train/720p_240fps_1', suffix='.png', verbose=True)
# get_file_path_list_intname(root='/home/hjy/workspace/interp_photo/04_inr/data/ERF/test/0000/processed_images', suffix='.png', verbose=True)

def get_file_name_list_intname(root, suffix='.png', prefix='', verbose=False):
    files_path_l = get_file_path_list_intname(root, suffix, prefix, verbose)
    files_name_l = [os.path.basename(p) for p in files_path_l]
    return files_name_l


# def get_suffix(path):
#     if os.path.isdir(path):
#         print('Warning: Folder path has no suffix.')
#         return None  # 文件夹没有后缀名
#     elif os.path.isfile(path):
#         print('Folder path has no suffix.')
#         _, suffix = os.path.splitext(path)   # 
#         return suffix

def get_suffix(path):
    '''
    in:
        "/fake/path/image.JPG"
    out:
        ".JPG"
    
    root, ext = os.path.splitext(path)
    # root = "/fake/path/image"
    # ext = ".txt"
    命名规范:
        ext 也即 suffix
    '''
    root, ext = os.path.splitext(path)

    if ext:  # 有后缀的情况
        return ext
    else:       # 无后缀或输入是目录形式（如以/结尾）
        return None
# print(get_suffix("/fake/path/image.JPG"))      # .JPG 


# def mkdirs(paths):
#     if isinstance(paths, str):
#         mkdir_if_folder_not_exist(paths)
#     else:
#         for path in paths:
#             mkdir_if_folder_not_exist(path)





DELIMITER_RENAMEPATH=None

def rename_files_to_04d(root,suffix = '.png', prefix='',  n=4, just_print = False):  
    '''
    要求所有文件名 具有相同后缀
    '''
    if os.path.isdir(root):   # 如果存在， 且为文件夹路径

        files_name_l = get_file_name_list(root, suffix, verbose=False)
        # print_list(files_name_l)
        i = 0
        for file in files_name_l:
            file_path = os.path.join(root, file)
            dirname = os.path.dirname(file_path)
            basename = os.path.basename(file_path)

            file_name , suffix = os.path.splitext(basename)  # eg.  '.csv'
            new_file_path =  join(dirname, f'{i:0>{n}d}'+ suffix) 
            if just_print:
                print(f'will rename {file_path} -> {new_file_path}')
            else:
                os.rename(file_path, new_file_path)
                print(f'done renamed {file_path} -> {new_file_path}')
            i +=1
    else:
        print(f'Folder does not exist: {root}')



def mkdir_rename_if_folder_exists(folder_path):
    '''
    path: folder path
    if path exists,     rename it, and mkdir
    if path not exists, mkdir
    '''
    if os.path.exists(folder_path):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # _20240817_223521
        new_name = folder_path + "_" + timestamp
        # print('Path already exists. Rename it to [{:s}]'.format(new_name))
        logger = logging.getLogger('base')
        logger.info('Path already exists. Rename it to [{:s}]'.format(new_name))
        os.rename(folder_path, new_name)
        os.makedirs(folder_path)      
    else:
        os.makedirs(folder_path)


def rename_if_folder_exists(folder_path):
    if os.path.isfile(folder_path):   # 如果存在， 且为文件路径
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # _20240817_223521
        _, suffix = os.path.splitext(folder_path)   # eg.  '.csv'
        backup_folder_path = f"{folder_path.rsplit('.', 1)[0]}_{timestamp}"+ suffix
        os.rename(folder_path, backup_folder_path)
        print(f"Folder already exist, renamed to: {backup_folder_path}")
    else:
        print(f'Folder does not exist: {folder_path}')


def rename_if_file_exists(file_path):
    if os.path.isfile(file_path):   # 如果存在， 且为文件路径
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # _20240817_223521
        _, suffix = os.path.splitext(file_path)   # eg.  '.csv'
        backup_file_path = f"{file_path.rsplit('.', 1)[0]}_{timestamp}"+ suffix
        os.rename(file_path, backup_file_path)
        print(f"File already exist, renamed to: {backup_file_path}")
    else:
        print(f'File does not exist: {file_path}')

# def mkdir_y(path):
#     '''
#     path: folder path
#     if path exists,     rename it, and mkdir
#     if path not exists, mkdir
#     '''
#     if os.path.exists(path):
#         new_name = path + '_archived_' + get_timestamp()
#         print('Path already exists. Rename it to [{:s}]'.format(new_name))
#         logger = logging.getLogger('base')
#         logger.info('Path already exists. Rename it to [{:s}]'.format(new_name))
#         os.rename(path, new_name)
#         os.makedirs(path)
#     else:
#         os.makedirs(path)


# def mkdir_if_folder_not_exist(path):
#     '''
#     mkdir is deprecated.
#     '''
#     if not os.path.exists(path):
#         os.makedirs(path)
#     # os.makedirs(path,exist_ok=True)

# def mkdir_if_folder_exist_rename(path):
#     '''
#     name mkdir_and_rename is deprecated.
#     '''
#     if os.path.exists(path):
#         new_name = path + '_archived_' + get_timestamp()
#         print('Path already exists. Rename it to [{:s}]'.format(new_name))
#         logger = logging.getLogger('base')
#         logger.info('Path already exists. Rename it to [{:s}]'.format(new_name))
#         os.rename(path, new_name)
        
#         os.makedirs(path)




# def rename_if_folder_exists(folder_path):
#     if os.path.isdir(folder_path):   # 如果存在， 且为文件夹路径
#         new_name = folder_path + '-archived_' + get_timestamp()
#         print(f'文件夹已存在，重命名为: [{new_name:s}]')
#         os.rename(folder_path, new_name)
#     else:
#         print(f'文件夹不存在: {folder_path}')

