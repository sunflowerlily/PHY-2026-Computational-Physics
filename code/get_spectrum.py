import numpy as np
import matplotlib.pyplot as plt
from urllib.request import urlretrieve
import os

def download_sdss_spectrum(plate, mjd, fiberid, save_path='galaxy_spectrum.txt'):
    """
    从 SDSS DR16 服务器下载光谱数据 (FITS)，提取波长和流量，保存为 txt。
    
    参数:
    plate (int): 观测板号
    mjd (int): 观测日期 (Modified Julian Date)
    fiberid (int): 光纤号
    """
    # SDSS 数据服务器 URL (SAS)
    # 示例 URL: https://dr16.sdss.org/optical/spectrum/view/data/format=csv/spec=lite?plateid=273&mjd=51957&fiberid=350
    # 我们直接使用 CSV 接口，避免依赖 astropy 读取 FITS (虽然 astropy 很强大，但为了教学环境简化，先用 CSV)
    
    url = f"https://dr16.sdss.org/optical/spectrum/view/data/format=csv/spec=lite?plateid={plate}&mjd={mjd}&fiberid={fiberid}"
    
    print(f"Downloading from: {url}")
    
    try:
        # 下载 CSV 文件
        csv_filename = "temp_spectrum.csv"
        urlretrieve(url, csv_filename)
        
        # 读取 CSV (跳过头部注释)
        # SDSS CSV 格式: wavelength, flux, best_fit, sky_flux, noise, ...
        data = np.genfromtxt(csv_filename, delimiter=',', skip_header=1)
        
        # 提取波长 (Angstrom) 和流量 (10^-17 erg/s/cm^2/Angstrom)
        wavelength = data[:, 0]
        flux = data[:, 1]
        
        # 保存为教学用的简单 txt 格式
        header = "Wavelength(A)  Flux(10^-17 erg/s/cm^2/A)"
        np.savetxt(save_path, np.column_stack((wavelength, flux)), header=header, fmt='%.4f  %.4f')
        
        print(f"Success! Spectrum saved to {save_path}")
        print(f"Data points: {len(wavelength)}")
        
        # 简单的预览图
        plt.figure(figsize=(10, 5))
        plt.plot(wavelength, flux, 'k-', lw=0.5)
        plt.title(f"SDSS Spectrum (Plate={plate}, MJD={mjd}, Fiber={fiberid})")
        plt.xlabel("Wavelength ($\AA$)")
        plt.ylabel("Flux")
        plt.grid(True, alpha=0.3)
        plt.savefig(save_path.replace('.txt', '.png'))
        print(f"Preview image saved to {save_path.replace('.txt', '.png')}")
        
        # 清理临时文件
        os.remove(csv_filename)
        
    except Exception as e:
        print(f"Error downloading or processing data: {e}")

if __name__ == "__main__":
    # 这是一个经典的类星体 3C 273 (实际上是一个非常明亮的 AGN) 或者其他典型星系
    # 这里选一个 SDSS 的经典星系样本
    # Plate: 0400, MJD: 51820, Fiber: 0350 (Spectral Class: GALAXY, Redshift z ~ 0.05)
    
    download_sdss_spectrum(plate=400, mjd=51820, fiberid=350, save_path='galaxy_spectrum.txt')
