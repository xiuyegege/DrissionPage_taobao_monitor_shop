from DrissionPage import ChromiumPage
import time
import random
import json
from config import shop_dict , project_root
import os
import csv
from control_shop_info import ControlShopInfo
from log import LogNewData



class GetHotSellingDatas:
    """获取热销商品数据的类"""
    
    def __init__(self):
        """初始化类"""
        self.shop_dict = shop_dict
        self.project_root = project_root
        self.csv_dir = os.path.join(self.project_root, 'csv_file')
        self.page = None
        self.log = LogNewData()
        
    def login_tb(self):
        """登录淘宝"""
        page = ChromiumPage()
        page.get('https://www.taobao.com')
        ele = page.ele('@taxt()=亲，请登录')
        if ele:
            ele.click()
            # go_on = input('登录完成后回车继续')
        else:
            ele2 = page.ele('@taxt()=立即登录')
            if ele2:
                ele2.click()
                # go_on = input('登录完成后回车继续')
            else:
                print('登录失败')
                return
                
    def create_shop_csv(self, shop_name):
        """创建店铺CSV文件"""
        # 确保csv_file目录存在
        if not os.path.exists(self.csv_dir):
            os.makedirs(self.csv_dir)
        
        csv_path = os.path.join(self.csv_dir, f'{shop_name}.csv')
        
        # 检查文件是否被占用
        try:
            # 表头
            headers = ['店铺名','商品ID','商品名称','图片url',  '商品url', '销量','记录日期']
            # 写入CSV文件
            with open(csv_path, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f) 
                writer.writerow(headers)
            
            print(f'CSV文件已创建: {csv_path}')
        except PermissionError as e:
            print(f'文件权限错误: {e}')
            print(f'请检查文件 {csv_path} 是否被其他程序占用（如Excel）')
            print('请关闭相关程序后重试')
            raise
        except Exception as e:
            print(f'创建CSV文件时发生错误: {e}')
            raise

    def get_shop_info(self, shop_name, shop_url, scroll_down_num=8):
        """获取店铺信息"""
        self.page = ChromiumPage()
        self.page.get(shop_url)
        time.sleep(random.randint(2,4))
        self.page.listen.start("mtop.taobao.shop.")
        ele = self.page.ele('xpath://div[@class="tags--ziaPbLe4"][1]')
        ele.click()
        time.sleep(random.randint(2,4))
        response = self.page.listen.wait(timeout=15)
        
        mtop_dict = response.response.body
        time.sleep(random.randint(2,4))
        self.save_to_csv(shop_name, mtop_dict)
        
        for i in range(scroll_down_num):
            self.page.scroll.down(500)
            time.sleep(random.randint(2,4))
            self.page.scroll.down(500)
            time.sleep(random.randint(2,4))
            self.page.scroll.down(500)
            time.sleep(random.randint(2,4))
            response = self.page.listen.wait(timeout=15)
            try:
                mtop_dict = response.response.body
                self.save_to_csv(shop_name, mtop_dict)
            except Exception as e:
                print(f'解析商品数据时发生错误: {e}')
                continue
                
        self.page.listen.stop()
        print('数据获取完成')
        
        # # 关闭浏览器
        # try:
        #     if self.page:
        #         self.page.quit()
        # except Exception as e:
        #     print(f'关闭浏览器时发生错误: {e}')

    def save_to_csv(self, shop_name, mtop_dict):
        """保存数据到CSV文件"""
        csv_path = os.path.join(self.csv_dir, f'{shop_name}.csv')
        if not os.path.exists(csv_path):
            self.create_shop_csv(shop_name)
        
        # 检查数据结构
        if not isinstance(mtop_dict, dict) or 'data' not in mtop_dict:
            print('响应数据格式不正确，跳过保存')
            return   

        try:
            product_list = mtop_dict['data']['data']

            for product in product_list:
                try:
                    product_id = product.get('itemId', '')
                    product_name = product.get('title', '')
                    product_url = product.get('itemUrl', '')
                    product_img = product.get('image', '')
                    product_sold = product.get('vagueSold365', '')
                    record_day = time.strftime('%Y-%m-%d')
                    
                    # 判断商品是否已经存在product_id
                    product_exists = False
                    try:
                        with open(csv_path, 'r', newline='', encoding='utf-8-sig') as f:
                            reader = csv.reader(f)
                            next(reader, None)  # 跳过表头
                            for row in reader:
                                if len(row) > 1 and str(row[1]).strip() == str(product_id).strip():
                                    print(f'商品{product_name}已经存在')
                                    product_exists = True
                                    break
                    except FileNotFoundError:
                        print(f'CSV文件不存在，重新创建: {csv_path}')
                        self.create_shop_csv(shop_name)
                        # 文件刚创建，商品肯定不存在，保持 product_exists = False
                    except PermissionError as e:
                        print(f'读取CSV文件权限错误: {e}')
                        print(f'请检查文件 {csv_path} 是否被其他程序占用')
                        continue
                    
                    if not product_exists:
                        # 写入CSV文件
                        try:
                            with open(csv_path, 'a', newline='', encoding='utf-8-sig') as f:
                                writer = csv.writer(f)
                                writer.writerow([shop_name,product_id,product_name,product_img, product_url, product_sold, record_day])
                                self.log.write_log_csv(shop_name,product_id)
                            print(f'商品 {product_name} 已保存到CSV')
                        except PermissionError as e:
                            print(f'写入CSV文件权限错误: {e}')
                            print(f'请检查文件 {csv_path} 是否被其他程序占用（如Excel）')
                            print('请关闭相关程序后重试')
                            break
                            
                except Exception as e:
                    print(f'处理商品数据时发生错误: {e}')
                    continue
                    
        except Exception as e:
            print(f'解析商品数据时发生错误: {e}')
            return

    def check_shop_name(self):
        """查看所有店铺名称"""
        for shop_name in self.shop_dict:
            print(shop_name)
        print("---------------------------------------")

    def choose_shop(self, shop_name):
        """选择店铺"""
        if shop_name in self.shop_dict:
            shop_url = self.shop_dict[shop_name]['shop_url']
            return shop_name, shop_url
        else:
            return None, '输入有误，请重新输入'
    



    def main(self):
        """主程序入口"""
        csi = ControlShopInfo()
        while True:
            print('1.登录淘宝')
            print('2.查看店铺名称')
            print('3.获取店铺信息')
            print('4.处理店铺信息')
            print('5.退出')
            choice = input('请输入你的选择：')
            if choice == '1':
                self.login_tb()
                print("---------------------------------------")
            elif choice == '2':
                self.check_shop_name()
                print("---------------------------------------")
            elif choice == '3':
                shop_name = input('请输入店铺名称：')
                scroll_down_num = int(input('请输入滚动次数：'))
                shop_name, shop_url = self.choose_shop(shop_name)
                if shop_name is not None:
                    self.get_shop_info(shop_name, shop_url, scroll_down_num)
                else:
                    print(shop_url)  # 这里shop_url实际是错误信息
                print("---------------------------------------")
            elif choice == '4':
                csi.main()
                print("---------------------------------------")
            elif choice == '5':
                break
            else:
                print('输入有误，请重新输入')
                print("---------------------------------------")


if __name__ == '__main__':
    hot_selling_data = GetHotSellingDatas()
    hot_selling_data.main()