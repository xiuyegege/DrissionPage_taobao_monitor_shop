from config import shop_dict
from get_datas import GetHotSellingDatas
import time


class MonitorShop:
    def __init__(self):
        self.gsd = GetHotSellingDatas()
        self.shop_dict = shop_dict
    
    def longin(self):
        """登录淘宝"""
        self.gsd.login_tb()
    
    def scan_shop_by_weekday(self):
        """按照weekday，扫描所有店铺，将新增的商品写入csv文件"""
        for shop_name in self.shop_dict:
            shop_url = self.shop_dict[shop_name]['shop_url']
            weekday = self.shop_dict[shop_name]['scan_weekday']
            today = time.strftime("%w")
            if today == weekday:
                print(f'开始扫描店铺{shop_name}')
                self.gsd.get_shop_info(shop_name, shop_url, 8)
        print('扫描完成')


if __name__ == '__main__':
    monitor = MonitorShop()
    # monitor.longin()
    monitor.scan_shop_by_weekday()