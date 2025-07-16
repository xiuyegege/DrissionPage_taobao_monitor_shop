from config import project_root
from DrissionPage import SessionPage, ChromiumPage
import os
import csv
import time
import random
import re
from datetime import datetime
from urllib.parse import urlparse, parse_qs


class GetImages:
    """图片下载管理类"""
    
    def __init__(self, project_root_path=None):
        """
        初始化GetImages类
        
        Args:
            project_root_path (str, optional): 项目根目录路径，默认使用config中的project_root
        """
        self.project_root = project_root_path or project_root
        self.session = None
        self.page = None
    
    def _ensure_directory(self, directory_path):
        """确保目录存在，如果不存在则创建"""
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            print(f'创建文件夹: {directory_path}')
    
    def _get_file_extension(self, content_type, img_url):
        """根据content-type和URL确定文件扩展名"""
        if 'jpeg' in content_type or 'jpg' in content_type:
            return '.jpg'
        elif 'png' in content_type:
            return '.png'
        elif 'gif' in content_type:
            return '.gif'
        elif 'webp' in content_type:
            return '.webp'
        else:
            # 如果无法从content-type判断，尝试从URL判断
            if img_url.lower().endswith('.png'):
                return '.png'
            elif img_url.lower().endswith('.gif'):
                return '.gif'
            elif img_url.lower().endswith('.webp'):
                return '.webp'
            else:
                return '.jpg'  # 默认为jpg
    
    def get_img_from_csv(self, csv_file):
        """
        从temp文件夹中的csv文件中的图片url列中，依次获取商品图片链接，并下载保存到imgs文件夹中
        保存图片的名称以对应的'商品ID'列中的值命名
        
        Args:
            csv_file (str): CSV文件名
        """
        csv_path = os.path.join(self.project_root, 'temp', csv_file)
        if not os.path.exists(csv_path):
            print(f'CSV文件不存在: {csv_path}')
            return
        
        # 创建imgs主文件夹
        img_folder = os.path.join(self.project_root, 'imgs')
        self._ensure_directory(img_folder)
        
        # 根据csv文件名创建子文件夹
        csv_name = os.path.splitext(csv_file)[0]  # 去掉.csv后缀
        sub_img_folder = os.path.join(img_folder, csv_name)
        self._ensure_directory(sub_img_folder)
        
        # 创建SessionPage对象用于下载图片
        if not self.session:
            self.session = SessionPage()
        
        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            next(reader)  # 跳过表头
            
            for row in reader:
                if len(row) < 4:  # 确保行数据完整
                    continue
                    
                img_url = row[3]  # 图片URL列
                product_id = row[1]  # 商品ID列
                
                if img_url and product_id:
                    try:
                        # 检查是否已存在该商品ID的图片
                        existing_files = [f for f in os.listdir(sub_img_folder) 
                                        if f.startswith(product_id + '.')]
                        
                        if existing_files:
                            print(f'商品ID {product_id} 的图片已存在，跳过下载')
                            continue
                        
                        # 下载图片
                        print(f'正在下载商品ID {product_id} 的图片...')
                        
                        # 使用DrissionPage的正确方式访问页面
                        self.session.get(img_url)
                        
                        # 检查页面是否成功加载
                        if self.session.response and self.session.response.status_code == 200:
                            # 获取图片内容
                            img_content = self.session.response.content
                            
                            # 获取图片内容类型
                            content_type = self.session.response.headers.get('content-type', '')
                            
                            # 根据content-type确定文件扩展名
                            ext = self._get_file_extension(content_type, img_url)
                            
                            # 构建完整的文件路径
                            # 获取当前日期（年月日格式）
                            current_date = datetime.now().strftime('%Y%m%d')
                            img_name = product_id + '_' + current_date + ext
                            img_path = os.path.join(sub_img_folder, img_name)
                            
                            # 保存图片
                            with open(img_path, 'wb') as img_file:
                                img_file.write(img_content)
                            
                            print(f'图片已保存: {img_path}')
                            
                            # 添加随机延时，避免请求过于频繁
                            time.sleep(random.uniform(0.5, 1.5))
                        else:
                            status_code = self.session.response.status_code if self.session.response else 'Unknown'
                            print(f'下载失败，状态码: {status_code}, URL: {img_url}')
                            
                    except Exception as e:
                        print(f'下载图片时发生错误: {e}, URL: {img_url}')
                        continue
        
        print(f'图片下载完成，保存在文件夹: {sub_img_folder}')

    def get_all_imgs(self):
        """
        遍历temp文件夹中的所有csv文件，并获取其中的图片链接
        """
        temp_folder = os.path.join(self.project_root, 'temp')
        if not os.path.exists(temp_folder):
            print(f'文件夹不存在: {temp_folder}')
            return

        csv_files = [f for f in os.listdir(temp_folder) if f.endswith('.csv')]
        if not csv_files:
            print('文件夹中没有CSV文件')
            return

        for csv_file in csv_files:
            print(f'正在处理文件: {csv_file}')
            self.get_img_from_csv(csv_file)


    def get_img_from_product_page(self, product_url):
        """
        从商品页面获取商品图片,并保存到imgs文件夹下的single_pro_imgs文件夹中
        
        Args:
            product_url (str): 商品页面URL
        """
        # 确保single_pro_imgs文件夹存在
        single_pro_imgs_folder = os.path.join(self.project_root, 'imgs', 'single_pro_imgs')
        self._ensure_directory(single_pro_imgs_folder)
        
        if not self.page:
            self.page = ChromiumPage()
        
        self.page.get(product_url)
        time.sleep(random.randint(2, 4))
        eles = self.page.eles('xpath://ul[@class="xM6AVLCbLn--thumbnails--_45f4c28"]//img')

        for ele in eles:
            img_url = ele.link
            if not self.session:
                self.session = SessionPage()
            
            self.session.get(img_url)

            if self.session.response and self.session.response.status_code == 200:
                # 获取图片内容
                img_content = self.session.response.content
                
                # 获取图片内容类型
                content_type = self.session.response.headers.get('content-type', '')
                
                # 根据content-type确定文件扩展名
                ext = self._get_file_extension(content_type, img_url)
                
                # 构建完整的文件路径
                # 从URL中提取商品ID，如果无法提取则使用时间戳
                # 尝试从URL中提取商品ID
                parsed_url = urlparse(product_url)
                query_params = parse_qs(parsed_url.query)
                
                if 'id' in query_params:
                    product_id = query_params['id'][0]
                    # 获取当前日期（年月日格式）
                    current_date = datetime.now().strftime('%Y%m%d')
                    img_name = f"{product_id}_{current_date}_{int(time.time())}{ext}"
                else:
                    # 如果无法提取ID，使用时间戳
                    current_date = datetime.now().strftime('%Y%m%d')
                    img_name = f"product_{current_date}_{int(time.time())}{ext}"
                
                img_path = os.path.join(single_pro_imgs_folder, img_name)

                # 保存图片
                with open(img_path, 'wb') as img_file:
                    img_file.write(img_content)

                print(f'图片已保存: {img_path}')

                # 添加随机延时，避免请求过于频繁
                time.sleep(random.uniform(0.5, 1.5))
            else:
                status_code = self.session.response.status_code if self.session.response else 'Unknown'
                print(f'下载失败，状态码: {status_code}, URL: {img_url}')

        print(f'图片下载完成，保存在文件夹: {single_pro_imgs_folder}')

    def get_img_from_csv_by_id(self, csv_file, product_id):
        """
        从csv文件中获取商品图片；
        从商品页面获取商品图片,并保存到imgs文件夹下的single_pro_imgs文件夹中
        
        Args:
            csv_file (str): CSV文件名
            product_id (str): 商品ID
        """
        csv_path = os.path.join(self.project_root, 'csv_file', csv_file)
        if not os.path.exists(csv_path):
            print(f'CSV文件不存在: {csv_path}')
            return

        # 创建imgs主文件夹
        img_folder = os.path.join(self.project_root, 'imgs')
        self._ensure_directory(img_folder)
        single_pro_imgs_folder = os.path.join(img_folder, 'single_pro_imgs')
        self._ensure_directory(single_pro_imgs_folder)

        # 在csv文件中查找指定的商品ID，获取对应的商品url，然后传递给get_img_from_product_page函数
        found = False
        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            next(reader)  # 跳过表头

            for row in reader:
                if len(row) < 5:  # 确保行数据完整（需要至少5列：包含商品ID和图片URL）
                    continue

                current_product_id = row[1]  # 商品ID列
                img_url = row[4]  # 图片URL列
                
                # 只处理匹配的商品ID
                if current_product_id == str(product_id) and img_url:
                    found = True
                    try:
                        # 检查是否已存在该商品ID的图片
                        existing_files = [f for f in os.listdir(single_pro_imgs_folder)
                                        if f.startswith(str(product_id) + '_')]

                        if existing_files:
                            print(f'商品ID {product_id} 的图片已存在，跳过下载')
                            break

                        # 下载图片
                        print(f'正在下载商品ID {product_id} 的图片...')

                        # 传递商品url给get_img_from_product_page函数
                        self.get_img_from_product_page(img_url)
                        break  # 找到并处理后退出循环

                    except Exception as e:
                        print(f'下载图片时发生错误: {e}, URL: {img_url}')
                        break
        
        if not found:
            print(f'在CSV文件中未找到商品ID: {product_id}')
        else:
            print(f'商品ID {product_id} 的图片下载完成，保存在文件夹: {single_pro_imgs_folder}')

    
    def close(self):
        """
        关闭浏览器页面和会话，释放资源
        """
        if self.page:
            self.page.quit()
            self.page = None
        if self.session:
            self.session.close()
            self.session = None
    
    def __enter__(self):
        """支持with语句的上下文管理器"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出时自动清理资源"""
        self.close()


if __name__ == '__main__':
    # 使用示例
    with GetImages() as img_downloader:
        # 示例1: 下载所有CSV文件中的图片
        # img_downloader.get_all_imgs()
        
        # 示例2: 从商品页面直接下载图片
        # url = input('请输入商品链接:')
        # img_downloader.get_img_from_product_page(url)
        
        # 示例3: 根据CSV文件和商品ID下载图片
        csv_name = input('请输入csv文件名:')
        product_id = input('请输入商品ID:')
        img_downloader.get_img_from_csv_by_id(csv_name, product_id)