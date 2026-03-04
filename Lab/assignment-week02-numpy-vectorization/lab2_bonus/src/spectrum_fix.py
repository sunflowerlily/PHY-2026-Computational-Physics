import numpy as np
from scipy.interpolate import interp1d, CubicSpline

class GalaxySpectrum:
    def __init__(self, filepath):
        """
        读取光谱文件。
        格式: Wavelength(A)  Flux
        """
        try:
            data = np.loadtxt(filepath)
            self.wave = data[:, 0]
            self.flux = data[:, 1]
        except Exception as e:
            print(f"Error loading file: {e}")
            self.wave = np.array([])
            self.flux = np.array([])

    def rest_frame_linear(self, redshift, target_wave):
        """
        TODO: 使用线性插值 (Linear Interpolation) 将红移光谱还原到静止系。
        
        参数:
        redshift (float): 红移值 z
        target_wave (array): 目标静止系波长网格
        
        返回:
        flux_restored (array): 在 target_wave 处的流量
        """
        # 1. 计算观测到的波长对应的静止波长: lambda_rest = lambda_obs / (1 + z)
        #    这里的 self.wave 是 lambda_obs
        wave_rest_reconstructed = self.wave / (1 + redshift)
        
        # 2. 构建线性插值函数 f(lambda)
        #    注意处理边界情况 (fill_value="extrapolate")
        
        # [STUDENT_CODE_HERE]
        # f = interp1d(...)
        # return f(target_wave)
        
        raise NotImplementedError("请实现线性插值")

    def rest_frame_cubic(self, redshift, target_wave):
        """
        TODO: 使用三次样条插值 (Cubic Spline) 将红移光谱还原到静止系。
        
        参数:
        redshift (float): 红移值 z
        target_wave (array): 目标静止系波长网格
        
        返回:
        flux_restored (array): 在 target_wave 处的流量
        """
        # 1. 计算观测到的波长对应的静止波长
        wave_rest_reconstructed = self.wave / (1 + redshift)
        
        # 2. 构建 CubicSpline 插值函数
        #    CubicSpline 默认处理边界条件较好，且保证二阶导连续
        
        # [STUDENT_CODE_HERE]
        # cs = CubicSpline(...)
        # return cs(target_wave)
        
        raise NotImplementedError("请实现三次样条插值")
