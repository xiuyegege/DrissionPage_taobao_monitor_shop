from config import shop_dict
import os

class ControlShopInfo:
    def __init__(self,shop_dict=shop_dict):
        self.shop_dict = shop_dict
        self.config_file_path = os.path.join(os.path.dirname(__file__), 'config.py')
    
    # 保存店铺信息shop_dict到config.py文件
    def save_to_config(self):
        """将shop_dict保存到config.py文件，保留其他配置内容"""
        try:
            # 读取现有配置文件内容
            config_lines = []
            try:
                with open(self.config_file_path, 'r', encoding='utf-8') as f:
                    config_lines = f.readlines()
            except FileNotFoundError:
                # 如果文件不存在，创建基本结构
                config_lines = []
            
            # 重新构建配置文件内容
            new_config_lines = []
            shop_dict_updated = False
            in_shop_dict = False
            brace_count = 0
            
            for line in config_lines:
                stripped_line = line.strip()
                
                # 检测shop_dict的开始
                if stripped_line.startswith('shop_dict = {') or stripped_line.startswith('shop_dict={'):
                    # 替换shop_dict行
                    new_config_lines.append(f'shop_dict = {repr(self.shop_dict)}\n')
                    shop_dict_updated = True
                    in_shop_dict = True
                    brace_count = stripped_line.count('{') - stripped_line.count('}')
                    # 如果在同一行结束，则不需要继续跳过
                    if brace_count <= 0:
                        in_shop_dict = False
                elif in_shop_dict:
                    # 跳过shop_dict的内容行，直到找到匹配的右括号
                    brace_count += line.count('{') - line.count('}')
                    if brace_count <= 0:
                        in_shop_dict = False
                else:
                    # 保留其他配置行
                    new_config_lines.append(line)
            
            # 如果没有找到shop_dict，则添加到文件末尾
            if not shop_dict_updated:
                if new_config_lines and not new_config_lines[-1].endswith('\n'):
                    new_config_lines.append('\n')
                new_config_lines.append('\n# 店铺信息\n')
                new_config_lines.append(f'shop_dict = {repr(self.shop_dict)}\n')
            
            # 确保包含必要的导入和其他配置
            has_import_os = any('import os' in line for line in new_config_lines)
            has_project_root = any('project_root' in line for line in new_config_lines)
            
            if not has_import_os:
                new_config_lines.insert(0, 'import os\n\n')
            
            if not has_project_root:
                # 在shop_dict之前添加project_root
                for i, line in enumerate(new_config_lines):
                    if 'shop_dict' in line:
                        new_config_lines.insert(i, '\n# 项目根目录\n')
                        new_config_lines.insert(i+1, 'project_root = os.path.dirname(os.path.abspath(__file__))\n')
                        break
                else:
                    # 如果没有找到shop_dict，添加到末尾
                    new_config_lines.append('\n# 项目根目录\n')
                    new_config_lines.append('project_root = os.path.dirname(os.path.abspath(__file__))\n')
            
            # 写入更新后的配置
            with open(self.config_file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_config_lines)
            
            print('配置已保存到config.py，其他配置内容已保留')
        except Exception as e:
            print(f'保存配置失败: {e}')

    # 添加店铺信息
    def add_shop_info(self,shop_name,shop_url,scan_weekday):
        if shop_name in self.shop_dict:
            print('店铺已存在')
            return '店铺已存在'
        else:
            self.shop_dict[shop_name] = {'shop_url':shop_url,'scan_weekday':scan_weekday}
            print('店铺添加成功')
            self.save_to_config()
            return '店铺添加成功'
    
    # 查看单个店铺信息
    def chekc_shop_info(self,shop_name):
        if shop_name in self.shop_dict:
            return self.shop_dict[shop_name]
        else:
            return None
    
    # 查看所有店铺信息
    def get_all_shop_info(self):
        shop_name_list = []
        shop_url_list = []
        scan_weekday_list = []
        for _ in self.shop_dict:
            shop_name = _
            print("店铺名称：",_)
            shop_ur = self.shop_dict[_]['shop_url']
            print("店铺链接：",self.shop_dict[_]['shop_url'])
            scan_weekday = self.shop_dict[_]['scan_weekday']
            print("扫描时间：",self.shop_dict[_]['scan_weekday'])
            print("---------------------------------------")
            shop_name_list.append(shop_name)
            shop_url_list.append(shop_ur)
            scan_weekday_list.append(scan_weekday)
        return shop_name_list, shop_url_list, scan_weekday_list

    
    # 删除店铺信息
    def del_shop_info(self,shop_name):
        if shop_name in self.shop_dict:
            del self.shop_dict[shop_name]
            print('店铺删除成功')
            self.save_to_config()
            return '店铺删除成功'
        else:
            print('店铺不存在')
            return '店铺不存在'

    
    # 更新店铺信息
    def update_shop_info(self,shop_name,shop_url,scan_weekday):
        if shop_name in self.shop_dict:
            self.shop_dict[shop_name]['shop_url'] = shop_url
            self.shop_dict[shop_name]['scan_weekday'] = scan_weekday
            print('店铺更新成功')
            self.save_to_config()
        else:
            print('店铺不存在')
        return None
    
    def main(self):
        while True:
            print('1.添加店铺信息')
            print('2.查看店铺信息')
            print('3.查看所有店铺信息')
            print('4.删除店铺信息')
            print('5.更新店铺信息')
            print('6.退出')
            choice = input('请输入你的选择：')
            if choice == '1':   
                shop_name = input('请输入店铺名称：')
                shop_url = input('请输入店铺链接：')
                scan_weekday = input('请输入扫描时间：')
                self.add_shop_info(shop_name,shop_url,scan_weekday)
                print("---------------------------------------")
            elif choice == '2':
                shop_name = input('请输入店铺名称：')
                shop_info = self.chekc_shop_info(shop_name)
                if shop_info:
                    print('店铺链接：',shop_info['shop_url'])
                    print('扫描时间：',shop_info['scan_weekday'])
                else:
                    print('店铺不存在')
                    print("---------------------------------------")
            elif choice == '3':
                self.get_all_shop_info()
                print("---------------------------------------")
            elif choice == '4':
                shop_name = input('请输入店铺名称：')   
                self.del_shop_info(shop_name)
                print("---------------------------------------")
            elif choice == '5':
                shop_name = input('请输入店铺名称：')
                shop_url = input('请输入店铺链接：')
                scan_weekday = input('请输入扫描时间：')
                self.update_shop_info(shop_name,shop_url,scan_weekday)
                print("---------------------------------------")
            elif choice == '6':
                break
            else:   
                print('输入有误')

if __name__ == '__main__':
    control_shop_info = ControlShopInfo()
    control_shop_info.main()