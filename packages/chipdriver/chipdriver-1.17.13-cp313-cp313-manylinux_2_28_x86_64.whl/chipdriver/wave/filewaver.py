'''
Title: 
Description: 基于文件加载波形的波形生成器类
Version: 
Company: Casia
Author: hsj
Date: 2022-01-14 11:37:35
LastEditors: hsj
LastEditTime: 2022-07-21 20:00:05
'''

from abc import abstractmethod
import numpy as np
from .waver import Waver
#######################################################################################################
#                                        基于加载文件的波形生成器                                       #
#######################################################################################################

class FileWaver(Waver):

    def __init__(self, name, data_file):
        super().__init__(name)
        # 加载数据
        self.data = self.loadFile(data_file)
        self.data_file = data_file
        # 一个周期被定义为输入文件中包含的完整点序列
        # 所以此处，定义波形长度为：文件中包含的所有点的数量
        self.len = len(self.data)

    @staticmethod
    @abstractmethod
    def loadFile(data_file) -> list:
        '''
        抽象方法：需要实现加载数据文件的具体规则，读取整数列表

        :param data_file: str, 数据文件
        :return: list[int], 加载后的数据列表
        '''
        return

    def getTicks(self, cycle):
        '''
        实现抽象方法
        计算给定周期包含的频点个数

        :return: int，指定周期内点的个数
        '''
        ticks = cycle * self.len
        return int(ticks)

    def getArray(self, cycle = 1):
        '''
        获取波形数组

        :param cycle: float, 播放该波形的周期数目
        :return content: bytes, 波形内容
        :return: np.ndarray(dtype=np.int16), 波形数组
        '''
        if cycle == 1:
            array = np.array(self.data)
        else:
            tile_remind = cycle % 1
            if tile_remind != 0:
                tile_count = int(cycle // 1 + 1)
            else:
                tile_count = int(cycle // 1)
            temp: np.ndarray = np.tile(self.data, tile_count)
            ticks = self.getTicks(cycle)
            array = temp[:ticks]
        array = array.clip(-32768, 32767).astype(np.int16)  
        return array

    def getContent(self, cycle = 1):
        '''
        获取bytes类型的波形数据

        :param cycle: float, 播放该波形的周期数目        
        :return: bytes, 整个波形的字节流
        '''
        array = self.getArray(cycle)
        content = array.tobytes()
        return content    
        

#######################################################################################################
#                                              实现类                                                  #
#######################################################################################################

class NumpyTxtWaver(FileWaver):

    def __init__(self, name, data_file):
        super().__init__(name, data_file)
    
    @staticmethod
    def loadFile(data_file) -> list:
        '''
        实现加载txt格式数据的读取规则
        要求每个数据值用`,`隔开，无需换行

        :param data_file: str, 数据文件
        :return: list[int], 加载后的数据列表
        '''
        try:
            data = np.loadtxt(data_file, delimiter=',')
        except Exception :
            # TODO 处理信息
            raise FileNotFoundError("无法打开指定的文件，{}".format(data_file))
        # data = data.tolist()        
        return data 