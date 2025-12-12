import numpy as np
import os
import cv2
import torch
import glob


#yhj 转移自 utils_git/utils_imgs/utils_imgs.py
img_np_01to8b = lambda x : (255*np.clip(x,0,1)).astype(np.uint8)
img_tsr_01to8b = lambda x : (255*torch.clip(x,0,1)).to(torch.uint8)

img_np_255to8b = lambda x : (np.clip(x,0,255)).astype(np.uint8)
img_tsr_255to8b = lambda x : (torch.clip(x,0,255)).astype(torch.uint8)





def get_err_map(img1_BGR_01,img2_BGR_01,vmin=0.0, vmax=0.4, colormap='COLORMAP_VIRIDIS'):
    '''
    '''
    # print(f"==>> img2_BGR_01.shape: {img2_BGR_01.shape}")
    # print(f"==>> img1_BGR_01.shape: {img1_BGR_01.shape}")
    error_hw3 = np.abs(img1_BGR_01 - img2_BGR_01)
    error_hw = np.mean(error_hw3, axis=2)
    errmap_hw3_BGR255  = get_err_map_func(error_hw,vmin=vmin, vmax=vmax, colormap=colormap)
    return errmap_hw3_BGR255

def get_err_map_func(error_hw_01,vmin=0.0, vmax=1.0, colormap='COLORMAP_VIRIDIS'): # vmin, vmax 有用
    '''
    old name: get_color_map
    y 20240712 经过测试，这种方法, 速度不受影响
    param:
        error_hw: h,w      0.-1. float32
    return:
        errmap_hw3_BGR255: h,w,3    0-255 uint8   BGR
    
    example:
        real255=cv2.imread(pngs_path_list_gt[i])
        fake255=cv2.imread(pngs_path_list_pre1[i])
        error_hw3 = np.abs(real255 / 255.0 - fake255 / 255.0)
        error_hw = np.mean(error_hw3, axis=2)
        erro255  = get_color_map(error_hw,vmin=vmin, vmax=vmax, colormap=colormap)
    '''
    assert vmax>vmin
    error_hw_01 = np.clip(error_hw_01, vmin, vmax)  # 将错误矩阵限制在 [vmin, vmax] 区间
    error_hw_01 = (error_hw_01-vmin)/(vmax-vmin)  # 将错误矩阵归一化到 [0, 1] 区间
    error_hw_255 = np.clip(error_hw_01*255,0,255).astype(np.uint8)   # 生成一个线性的错误矩阵
    # print(f"==>> error_hw.shape: {error_hw.shape}")

    # 将灰度图像转换为Jet样式的伪彩色图像
    if colormap=='COLORMAP_VIRIDIS':
        error_hw_virids = cv2.applyColorMap(error_hw_255, cv2.COLORMAP_VIRIDIS)  # 颜色映射
    elif colormap=='COLORMAP_JET':
        error_hw_virids = cv2.applyColorMap(error_hw_255, cv2.COLORMAP_JET)
    elif colormap=='COLORMAP_HOT':
        error_hw_virids = cv2.applyColorMap(error_hw_255, cv2.COLORMAP_HOT)
    errmap_hw3_BGR255 = error_hw_virids
    # print(f"==>> errmap_hw3_BGR255.shape: {errmap_hw3_BGR255.shape}")
    # print(f"==>> errmap_hw3_BGR255.dtype: {errmap_hw3_BGR255.dtype}")
    return errmap_hw3_BGR255 # hw3 255 BGR



def get_err_colorbar(colorbar_h, colorbar_w=80, bar_inner_w=20, bar_inner_h_ratio=0.8, 
                 bar_x_offset=None, bar_x_offset_ratio=0.2, vmin=0.0, vmax=1.0, num_ticks=5, colormap='COLORMAP_VIRIDIS'):
    """
    生成颜色条（可单独使用）
    
    :param colorbar_h: 颜色条高度（应与误差图 h 一致）
    :param colorbar_w: 整个颜色条区域的宽度（包括白色背景 & 数值标注）
    :param bar_inner_w: 仅颜色条本身的宽度
    :param bar_inner_height_ratio: 颜色条本身的高度比例（相对于 h ，默认 0.8）
    :param bar_x_offset: 颜色条距离左侧的偏移量（若 None，则默认居中）
    :param bar_x_offset_ratio: 颜色条距离左侧的偏移量。bar_x_offset为None时，根据ratio设置。 如果ratio也为 None ，则默认居中）
    :param vmin: 颜色条最小值
    :param vmax: 颜色条最大值
    :param num_ticks: 颜色条上的刻度数量
    :return: (colorbar_h, colorbar_w, 3) 颜色条（BGR 格式）
    """
    assert bar_inner_w < colorbar_w, "bar_inner_w 应小于 colorbar_w"
    assert 0 < bar_inner_h_ratio <= 1, "bar_inner_height_ratio 应在 (0,1] 之间"

    colorbar_w = colorbar_w  # 颜色条总宽度
    # 计算颜色条的高度
    bar_inner_h = int(colorbar_h * bar_inner_h_ratio)
    bar_inner_w = bar_inner_w  # 仅颜色条的宽度

    # 创建白色背景
    colorbar_hw3_BGR = np.ones((colorbar_h, colorbar_w, 3), dtype=np.uint8) * 255  # 全白背景

    # 颜色条的垂直起始位置（确保在图像中居中）
    y_offset = (colorbar_h - bar_inner_h) // 2  


    # 颜色条的水平起始位置（根据 bar_x_offset 调整）
    if bar_x_offset is None:
        if bar_x_offset_ratio:
            x_offset = int(colorbar_w * bar_x_offset_ratio)
        else:
            x_offset = (colorbar_w - bar_inner_w) // 2  # 默认让bar 中轴线 居中
    else:
        x_offset = min(max(0, bar_x_offset), colorbar_w - bar_inner_w)  # 限制范围，防止超出边界

    # 生成颜色条的渐变
    gradient = np.linspace(1, 0, bar_inner_h).reshape(bar_inner_h, 1)
    gradient = (gradient * 255).astype(np.uint8)

    colormap_dict = {
        'COLORMAP_VIRIDIS': cv2.COLORMAP_VIRIDIS,
        'COLORMAP_JET': cv2.COLORMAP_JET,
        'COLORMAP_HOT': cv2.COLORMAP_HOT
    }
    gradient_color = cv2.applyColorMap(gradient, colormap_dict.get(colormap, cv2.COLORMAP_VIRIDIS))

    # 将颜色条插入白色背景
    colorbar_hw3_BGR[y_offset:y_offset + bar_inner_h, x_offset:x_offset + bar_inner_w] = gradient_color

    # ========== 添加刻度标注 ==========
    tick_positions = np.linspace(y_offset, y_offset + bar_inner_h - 1, num_ticks).astype(int)  # 刻度位置
    tick_values = np.linspace(vmax, vmin, num_ticks)  # 误差数值

    for i, (pos, val) in enumerate(zip(tick_positions, tick_values)):
        text = f"{val:.2f}"  # 格式化数值
        text_position = (x_offset + bar_inner_w + 5, pos + 5)  # 数值放在颜色条右侧
        cv2.putText(colorbar_hw3_BGR, text, text_position, cv2.FONT_HERSHEY_SIMPLEX, 
                    0.4, (0, 0, 0), 1, cv2.LINE_AA)

    return colorbar_hw3_BGR  # colorbar: [colorbar_h,colorbar_w,3]  255 BGR




# def get_err_map(img1_BGR_01,img2_BGR_01,vmin=0.0, vmax=0.4, colormap='COLORMAP_VIRIDIS'):
#     '''
#     '''
#     error_hw3 = np.abs(img1_BGR_01 - img2_BGR_01)
#     error_hw = np.mean(error_hw3, axis=2)
#     errmap_hw3_BGR255  = get_err_map_func(error_hw,vmin=vmin, vmax=vmax, colormap=colormap)
#     return errmap_hw3_BGR255

# def get_err_map_func(error_hw,vmin=0.0, vmax=1.0, colormap='COLORMAP_VIRIDIS'): # vmin, vmax 有用
#     '''
#     old name: get_color_map
#     y 20240712 经过测试，这种方法, 速度不受影响
#     param:
#         error_hw: h,w      0.-1. float32
#     return:
#         errmap_hw3_BGR255: h,w,3    0-255 uint8   BGR
    
#     example:
#         real255=cv2.imread(pngs_path_list_gt[i])
#         fake255=cv2.imread(pngs_path_list_pre1[i])
#         error_hw3 = np.abs(real255 / 255.0 - fake255 / 255.0)
#         error_hw = np.mean(error_hw3, axis=2)
#         erro255  = get_color_map(error_hw,vmin=vmin, vmax=vmax, colormap=colormap)
#     '''
#     assert vmax>vmin
#     error_hw = np.clip(error_hw, vmin, vmax)  # 将错误矩阵限制在 [vmin, vmax] 区间
#     error_hw = (error_hw-vmin)/(vmax-vmin)  # 将错误矩阵归一化到 [0, 1] 区间
#     error_hw = np.clip(error_hw*255,0,255).astype(np.uint8)   # 生成一个线性的错误矩阵
#     # print(f"==>> error_hw.shape: {error_hw.shape}")

#     # 将灰度图像转换为Jet样式的伪彩色图像
#     if colormap=='COLORMAP_VIRIDIS':
#         error_hw_virids = cv2.applyColorMap(error_hw, cv2.COLORMAP_VIRIDIS)  # 颜色映射
#     elif colormap=='COLORMAP_JET':
#         error_hw_virids = cv2.applyColorMap(error_hw, cv2.COLORMAP_JET)
#     elif colormap=='COLORMAP_HOT':
#         error_hw_virids = cv2.applyColorMap(error_hw, cv2.COLORMAP_HOT)
#     errmap_hw3_BGR255 = error_hw_virids
#     # print(f"==>> errmap_hw3_BGR255.shape: {errmap_hw3_BGR255.shape}")
#     # print(f"==>> errmap_hw3_BGR255.dtype: {errmap_hw3_BGR255.dtype}")
#     return errmap_hw3_BGR255 # hw3 255 BGR


# def get_err_colorbar(colorbar_h, colorbar_w=80, bar_inner_w=20, bar_inner_h_ratio=0.8, 
#                  bar_x_offset=None, bar_x_offset_ratio=0.2, vmin=0.0, vmax=1.0, num_ticks=5, colormap='COLORMAP_VIRIDIS'):
#     """
#     生成颜色条（可单独使用）
    
#     :param colorbar_h: 颜色条高度（应与误差图 h 一致）
#     :param colorbar_w: 整个颜色条区域的宽度（包括白色背景 & 数值标注）
#     :param bar_inner_w: 仅颜色条本身的宽度
#     :param bar_inner_height_ratio: 颜色条本身的高度比例（相对于 h ，默认 0.8）
#     :param bar_x_offset: 颜色条距离左侧的偏移量（若 None，则默认居中）
#     :param bar_x_offset_ratio: 颜色条距离左侧的偏移量。bar_x_offset为None时，根据ratio设置。 如果ratio也为 None ，则默认居中）
#     :param vmin: 颜色条最小值
#     :param vmax: 颜色条最大值
#     :param num_ticks: 颜色条上的刻度数量
#     :return: (colorbar_h, colorbar_w, 3) 颜色条（BGR 格式）
#     """
#     assert bar_inner_w < colorbar_w, "bar_inner_w 应小于 colorbar_w"
#     assert 0 < bar_inner_h_ratio <= 1, "bar_inner_height_ratio 应在 (0,1] 之间"

#     colorbar_w = colorbar_w  # 颜色条总宽度
#     # 计算颜色条的高度
#     bar_inner_h = int(colorbar_h * bar_inner_h_ratio)
#     bar_inner_w = bar_inner_w  # 仅颜色条的宽度

#     # 创建白色背景
#     colorbar = np.ones((colorbar_h, colorbar_w, 3), dtype=np.uint8) * 255  # 全白背景

#     # 颜色条的垂直起始位置（确保在图像中居中）
#     y_offset = (colorbar_h - bar_inner_h) // 2  


#     # 颜色条的水平起始位置（根据 bar_x_offset 调整）
#     if bar_x_offset is None:
#         if bar_x_offset_ratio:
#             x_offset = int(colorbar_w * bar_x_offset_ratio)
#         else:
#             x_offset = (colorbar_w - bar_inner_w) // 2  # 默认让bar 中轴线 居中
#     else:
#         x_offset = min(max(0, bar_x_offset), colorbar_w - bar_inner_w)  # 限制范围，防止超出边界

#     # 生成颜色条的渐变
#     gradient = np.linspace(1, 0, bar_inner_h).reshape(bar_inner_h, 1)
#     gradient = (gradient * 255).astype(np.uint8)

#     colormap_dict = {
#         'COLORMAP_VIRIDIS': cv2.COLORMAP_VIRIDIS,
#         'COLORMAP_JET': cv2.COLORMAP_JET,
#         'COLORMAP_HOT': cv2.COLORMAP_HOT
#     }
#     gradient_color = cv2.applyColorMap(gradient, colormap_dict.get(colormap, cv2.COLORMAP_VIRIDIS))

#     # 将颜色条插入白色背景
#     colorbar[y_offset:y_offset + bar_inner_h, x_offset:x_offset + bar_inner_w] = gradient_color

#     # ========== 添加刻度标注 ==========
#     tick_positions = np.linspace(y_offset, y_offset + bar_inner_h - 1, num_ticks).astype(int)  # 刻度位置
#     tick_values = np.linspace(vmax, vmin, num_ticks)  # 误差数值

#     for i, (pos, val) in enumerate(zip(tick_positions, tick_values)):
#         text = f"{val:.2f}"  # 格式化数值
#         text_position = (x_offset + bar_inner_w + 5, pos + 5)  # 数值放在颜色条右侧
#         cv2.putText(colorbar, text, text_position, cv2.FONT_HERSHEY_SIMPLEX, 
#                     0.4, (0, 0, 0), 1, cv2.LINE_AA)

#     return colorbar  # colorbar: [colorbar_h,colorbar_w,3]  255 BGR




def crop_center(img, center_crop_height, center_crop_width):
    """
    ChatGPT
    对输入图像进行中心裁剪

    Args:
        img (numpy.ndarray): 读取的图像 (H, W, C)
        center_crop_height (int): 目标裁剪高度
        center_crop_width (int): 目标裁剪宽度

    Returns:
        numpy.ndarray: 裁剪后的图像
    """
    h, w, c = img.shape  # 获取原始图像尺寸

    # 计算中心点
    center_y, center_x = h // 2, w // 2

    # 计算裁剪区域的起始和结束坐标
    start_x = max(center_x - center_crop_width // 2, 0)
    end_x = min(center_x + center_crop_width // 2, w)
    start_y = max(center_y - center_crop_height // 2, 0)
    end_y = min(center_y + center_crop_height // 2, h)

    # 进行裁剪
    cropped_img = img[start_y:end_y, start_x:end_x, :]

    return cropped_img


#! --------------------- folder images function ----------------------------
def folder_imgs_crop_center(inRoot,otRoot=None,suffix='.png', center_crop_height=512, center_crop_width=512):
    '''
    曾用名 crop_imgs
    example:
        crop_yxhw = (56,0,512,512) 
        otRoot = crop_imgs('crop_resize', '.png', crop_yxhw )
    '''
    imagesPathLst = sorted([i for i in glob.glob(f"{inRoot}/*{suffix}")])

    # It creates a folder called ltl if does't exist
    if otRoot is None:
        otRoot = inRoot+"_crop_center"
    os.makedirs(otRoot,exist_ok=True)

    # ic(imagesPathLst)

    for imgPath in imagesPathLst:
        # img = Image.open(i)
        img = cv2.imread(imgPath,-1)
        cropped_img = crop_center(img, center_crop_height, center_crop_width)

        # img = np.array(Image.open(imgPath)).astype("uint16")
        # img = Image.fromarray(img)
        # print("Image mode: ", img.mode)
        # print(img.getextrema())
        # crop = img.crop(area)

        savePath = os.path.join(otRoot,os.path.basename(imgPath))
        cv2.imwrite(savePath,cropped_img)
        # img.save(savePath)
        print(f'done save img to:{savePath}, save dtype is {cropped_img.dtype}')

    print("Done")
    # subprocess.call(["open", otRoot])   # "xdg-open"
    return otRoot



def folder_imgs_crop_yxhw(inRoot,otRoot=None,suffix='.png',crop_yxhw=(100,100,512,512) ):
    '''
    曾用名 crop_imgs
    example:
        crop_yxhw = (56,0,512,512) 
        otRoot = crop_imgs('crop_resize', '.png', crop_yxhw )
    '''
    imagesPathLst = sorted([i for i in glob.glob(f"{inRoot}/*{suffix}")])

    # It creates a folder called ltl if does't exist
    if otRoot is None:
        otRoot = inRoot+"_crop_yxhw"
    os.makedirs(otRoot,exist_ok=True)

    # ic(imagesPathLst)

    for imgPath in imagesPathLst:
        # img = Image.open(i)
        img = cv2.imread(imgPath,-1)
        cropped_img = img[crop_yxhw[0]:crop_yxhw[0]+crop_yxhw[2], crop_yxhw[1]:crop_yxhw[1]+crop_yxhw[3]] 


        # img = np.array(Image.open(imgPath)).astype("uint16")
        # img = Image.fromarray(img)
        # print("Image mode: ", img.mode)
        # print(img.getextrema())
        # crop = img.crop(area)

        savePath = os.path.join(otRoot,os.path.basename(imgPath))
        cv2.imwrite(savePath,cropped_img)
        # img.save(savePath)
        print(f'done save img to:{savePath}, save dtype is {cropped_img.dtype}')

    print("Done")
    # subprocess.call(["open", otRoot])   # "xdg-open"
    return otRoot



def folder_imgs_resize(inRoot,otRoot=None,suffix='.png',newW=128,newH=64):
    '''
    曾用名 resize_imgs
    example:
        crop_yxhw = (56,0,512,512) 
        otRoot = crop_imgs('crop_resize', '.png', crop_yxhw )
    newW = 640
    newH = 480
    suffix = '.png'
    '''
    if otRoot is None:
        otRoot = inRoot+'_rsz'
    # otRoot = inRoot+'_resized'
    os.makedirs(otRoot,exist_ok=True)
    imagesPathLst = sorted(glob.glob(f'{inRoot}/*{suffix}'))

    for imgPath in imagesPathLst:
        #* read and resize
        img = cv2.imread(imgPath,-1)
        rsz = cv2.resize(img,(newW,newH))

        #* save
        imgBaseName = os.path.basename(imgPath)
        savePath = os.path.join(otRoot,imgBaseName)
        cv2.imwrite(savePath, rsz)
        print(f'done save img to:{savePath}, save dtype is {rsz.dtype}')
    return otRoot


def folder_imgs_crop_yxhw_and_resize(inRoot,suffix='.png',crop_yxhw=(56,0,512,512) ,newW=256,newH=256):
    '''
    
    '''
    
    # area = (0+159, 0+118, 1730+159, 1300+118)  #x1,y1,x2,y2
    # crop_yxhw = (0,190,100,100)   # y_left_up, x_left_up, h_new, w_new  # 512 256
    # crop_yxhw = (56,0,512,512) 
    otRoot = folder_imgs_crop_yxhw(inRoot,suffix, crop_yxhw )

    # newH=256
    # newW = 256
    otRoot = folder_imgs_resize(inRoot= otRoot, suffix= suffix,newW= newW ,newH = newH )
    print(f"##  After crop and resize, otRoot: {otRoot}")



def main():
    
    pass

if __name__=='__main__':
    main()

