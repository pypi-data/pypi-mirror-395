'''
Title: 
Description: 基于函数的波形生成器
Version: 
Company: Casia
Author: hsj
Date: 2022-01-14 11:35:09
LastEditors: hsj
LastEditTime: 2022-07-21 18:00:55
'''

from abc import abstractmethod
import math
import numpy as np
from .waver import Waver

#######################################################################################################
#                                        函数类波形生成器基类                                           #
#######################################################################################################
class FunctionWaver(Waver):
    def __init__(self, name, freq = 125e6, samplerate = 2e9, amplitude=math.pow(2, 15) - 1, phase = 0, bias = 0):
        '''
        波形初始化，包括额定频率，当前工作频率，数字信号放大倍率，信号初相，信号偏移

        :param name: str, 波形命名（别名，需要唯一）
        :parma freq: int | float, 载波频率
        :parma samplerate: int | float, 采样率
        :param amplitude: int16, 振幅（信号放大倍率），默认值为2的15次方
        :param phase: float, 初始相位周期百分比（第phase个周期），默认值为0。如0.25表示从1/4周期处开始
        :param bias: float, 偏移，指波形在y轴的偏移量
            注意：-32768 <= amplitude + bias <= 32767
        默认一个sram地址中存放8个数据点，因此，sram地址数可以如下计算：
            c = samplerate  / (freq * 8)
            一个周期内频点数目 n = samplerate / freq
            因此，要保证一个周期内频点个数正确，需要保证n是8的倍数
        '''
        super().__init__(name)
        self.freq = freq
        self.samplerate = samplerate
        self.amplitude = amplitude
        self.phasePercentage = phase
        self.phase = self.phaseShift(phase)
        self.bias = bias

    def getTicks(self, cycle):
        '''
        实现抽象方法
        计算给定周期包含的频点个数

        :return: int，指定周期内点的个数
        '''
        ticks = cycle * self.samplerate / self.freq
        return int(ticks)
    
    def getContent(self, cycle = 1):
        '''
        获取bytes类型的波形数据

        :param cycle: float, 播放该波形的周期数目        
        :return: bytes, 整个波形的字节流
        '''
        array = self.getArray(cycle)
        content = array.tobytes()
        return content 

    @staticmethod
    @abstractmethod
    def phaseShift(phase):
        '''
        实现相位转换静态抽象方法

        :param phase:float, 初始相位所在周期点
        :return: float, 初始相位值
        '''
        return

#######################################################################################################
#                                       以下实现常用波形生成器                                          #
#######################################################################################################

#################################         三角函数类         ###########################################

class sinWaver(FunctionWaver):
    '''
    sin函数波形生成器
    '''
    def __init__(self, name, freq = 125e6, samplerate = 2e9, amplitude=math.pow(2, 15) - 1, phase = 0, bias = 0):
        super().__init__(name, freq, samplerate, amplitude, phase, bias)

    @staticmethod
    def phaseShift(phase):
        '''
        实现sin函数相位转换静态抽象方法

        :param phase:float, 初始相位所在周期点
        :return: float, 初始相位值
        '''
        return 2 * math.pi * phase
    
    def getArray(self, cycle = 1):
        '''
        获取波形数组

        :param cycle: float, 播放该波形的周期数目
        :return content: bytes, 波形内容
        :return: np.ndarray(dtype=np.int16), 波形数组
        '''
        start = self.phase 
        end = cycle * 2 * np.pi
        x = np.linspace(start, end, self.getTicks(cycle), endpoint=False)
        array = np.sin(x) * self.amplitude + self.bias
        array = array.clip(-32768, 32767).astype(np.int16)
        return array

class cosWaver(FunctionWaver):
    '''
    cos函数波形生成器
    '''
    def __init__(self, name, freq = 125e6, samplerate = 2e9, amplitude=math.pow(2, 15) - 1, phase = 0, bias = 0):
        super().__init__(name, freq, samplerate, amplitude, phase, bias)

    @staticmethod
    def phaseShift(phase):
        '''
        实现cos函数相位转换静态抽象方法

        :param phase:float, 初始相位所在周期点
        :return: float, 初始相位值
        '''
        return 2 * math.pi * phase

    def getArray(self, cycle = 1):
        '''
        获取波形数组

        :param cycle: float, 播放该波形的周期数目
        :return content: bytes, 波形内容
        :return: np.ndarray(dtype=np.int16), 波形数组
        '''
        start = self.phase 
        end = cycle * 2 * np.pi
        x = np.linspace(start, end, self.getTicks(cycle), endpoint=False)
        array = np.cos(x) * self.amplitude + self.bias
        array = array.clip(-32768, 32767).astype(np.int16)
        return array 


#################################         锯齿波类         ###########################################


class sawtoothWaver(FunctionWaver):
    '''
    锯齿波生成器
    '''
    def __init__(self, name, freq = 125e6, samplerate = 2e9, amplitude=math.pow(2, 15) - 1, phase = 0, bias = 0):
        super().__init__(name, freq, samplerate, amplitude, phase, bias)

    @staticmethod
    def phaseShift(phase):
        '''
        实现锯齿波初相转换函数

        :param phase: float, 初始周期数
        :return: float, 初相
        '''

        return np.modf(phase)[0] 

    def getArray(self, cycle = 1):
        '''
        获取波形数组

        :param cycle: float, 播放该波形的周期数目
        :return content: bytes, 波形内容
        :return: np.ndarray(dtype=np.int16), 波形数组
        '''
        start = self.phase
        end = self.phase + cycle
        x = np.linspace(start, end, self.getTicks(cycle), endpoint=False)
        array = np.modf(x)[0] * self.amplitude * 2 - self.amplitude + self.bias
        array = array.clip(-32768, 32767).astype(np.int16)
        return array         


class squareWaver(FunctionWaver):
    '''
    方波生成器
    '''
    def __init__(self, name, freq = 125e6, samplerate = 2e9, amplitude=math.pow(2, 15) - 1, phase = 0, bias = 0):
        super().__init__(name, freq, samplerate, amplitude, phase, bias)

    @staticmethod
    def phaseShift(phase):
        '''
        实现方波初相转换函数

        :param phase: float, 初始周期数
        :return: float, 初相
        '''
        return np.modf(phase)[0]

    def getArray(self, cycle = 1):
        '''
        获取波形数组

        :param cycle: float, 播放该波形的周期数目
        :return content: bytes, 波形内容
        :return: np.ndarray(dtype=np.int16), 波形数组
        '''
        ticks = self.getTicks(cycle)    
        zeros = np.zeros(int(ticks/2))
        ones = np.ones(ticks - int(ticks/2))
        temp = np.append(zeros, ones) * self.amplitude + self.bias
        point = int(self.phase * ticks)
        array = np.append(temp[point:], temp[:point])
        array = array.clip(-32768, 32767).astype(np.int16)
        return array


