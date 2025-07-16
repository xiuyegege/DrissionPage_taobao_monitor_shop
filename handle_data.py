
import csv
import os
from config import project_root

class HandleDatas:
    """处理CSV数据的类"""
    
    def __init__(self):
        """初始化类"""
        self.project_root = project_root
        self.csv_folder = os.path.join(self.project_root, 'csv_file')
        self.temp_folder = os.path.join(self.project_root, 'temp')
    
    def change_sales(self, csv_file):
        """
        将CSV文件中的销量数据转换为整数类型
        处理规则：
        - 去掉"+"符号
        - 将"万"替换为"0000"
        - 转换为整数类型
        """
        csv_path = os.path.join(self.csv_folder, csv_file)
        
        if not os.path.exists(csv_path):
            print(f'CSV文件不存在: {csv_path}')
            return
        
        # 读取原始数据
        rows = []
        try:
            with open(csv_path, 'r', newline='', encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                headers = next(reader)  # 读取表头
                
                # 找到销量列的索引
                sales_index = -1
                for i, header in enumerate(headers):
                    if '销量' in header:
                        sales_index = i
                        break
                
                if sales_index == -1:
                    print('未找到销量列')
                    return
                
                # 处理每一行数据
                for row in reader:
                    if len(row) > sales_index:
                        original_sales = row[sales_index]
                        converted_sales = self.convert_sales_to_int(original_sales)
                        row[sales_index] = str(converted_sales)
                    rows.append(row)
        
        except Exception as e:
            print(f'读取CSV文件时发生错误: {e}')
            return
    
        # 写回文件
        try:
            with open(csv_path, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow(headers)  # 写入表头
                writer.writerows(rows)    # 写入数据行
            
            print(f'销量数据转换完成: {csv_path}')
        
        except Exception as e:
            print(f'写入CSV文件时发生错误: {e}')

    def convert_sales_to_int(self, sales_str):
        """
        将销量字符串转换为整数
        例如: "1万+" -> 10000, "9000+" -> 9000
        """
        if not sales_str or sales_str.strip() == '':
            return 0
        
        # 去掉空格
        sales_str = sales_str.strip()
        
        # 去掉"+"符号
        sales_str = sales_str.replace('+', '')
        
        # 处理"万"字
        if '万' in sales_str:
            # 提取万前面的数字
            number_part = sales_str.replace('万', '')
            try:
                base_number = float(number_part)
                return int(base_number * 10000)
            except ValueError:
                print(f'无法解析销量数据: {sales_str}')
                return 0
        else:
            # 直接转换为整数
            try:
                return int(sales_str)
            except ValueError:
                print(f'无法解析销量数据: {sales_str}')
                return 0

    def handle_all_csv(self):
        """
        处理csv_file文件夹下的所有CSV文件
        将所有CSV文件中的销量数据转换为整数类型
        """
        if not os.path.exists(self.csv_folder):
            print(f'文件夹不存在: {self.csv_folder}')
            return

        for filename in os.listdir(self.csv_folder):
            if filename.endswith('.csv'):
                self.change_sales(filename)

    def select_pro_by_csv(self, csv_file, sals_volume=500):
        """
        根据销量筛选商品
        将筛选后的商品保存到新的CSV文件中，并保存在temp文件夹下
        """
        csv_path = os.path.join(self.csv_folder, csv_file)
        if not os.path.exists(csv_path):
            print(f'CSV文件不存在: {csv_path}')
            return

        # 读取原始数据
        rows = []
        try:
            with open(csv_path, 'r', newline='', encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                headers = next(reader)  # 读取表头

                # 找到销量列的索引
                sales_index = -1
                for i, header in enumerate(headers):
                    if '销量' in header:
                        sales_index = i
                        break

                if sales_index == -1:
                    print('未找到销量列')
                    return

                # 处理每一行数据
                for row in reader:
                    if len(row) > sales_index:
                        sales_str = row[sales_index]
                        if sales_str.strip() != '':
                            try:
                                sales = int(sales_str)
                                if sales >= sals_volume:
                                    rows.append(row)
                            except ValueError:
                                print(f'无法解析销量数据: {sales_str}')
                    else:
                        print(f'行数据不完整: {row}')

        except Exception as e:
            print(f'读取CSV文件时发生错误: {e}')
            return

        # 保存筛选后的数据到新的CSV文件
        try:
            if not os.path.exists(self.temp_folder):
                os.makedirs(self.temp_folder)

            new_csv_path = os.path.join(self.temp_folder, csv_file)
            with open(new_csv_path, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow(headers)  # 写入表头
                writer.writerows(rows)    # 写入数据行

            print(f'筛选后的数据已保存到: {new_csv_path}')

        except Exception as e:
            print(f'写入CSV文件时发生错误: {e}')

    def select_all_csv_by_sales(self, sals_volume=500):
        """
        筛选所有CSV文件中销量大于等于sals_volume的商品
        """
        if not os.path.exists(self.csv_folder):
            print(f'文件夹不存在: {self.csv_folder}')
            return

        for filename in os.listdir(self.csv_folder):
            if filename.endswith('.csv') and filename not in os.listdir(self.temp_folder):
                self.select_pro_by_csv(filename, sals_volume)

    def delete_csv_file(self, csv_file):
        """
        删除csv_file文件夹下的文件
        """
        csv_path = os.path.join(self.csv_folder, csv_file)
        if not os.path.exists(csv_path):
            print(f'CSV文件不存在: {csv_path}')
            return

        try:
            os.remove(csv_path)
            print(f'CSV文件已删除: {csv_path}')

        except Exception as e:
            print(f'删除CSV文件时发生错误: {e}')

    def clear_temp_folder(self):
        """
        清空temp文件夹下的所有文件
        """
        if not os.path.exists(self.temp_folder):
            print(f'文件夹不存在: {self.temp_folder}')
            return

        for filename in os.listdir(self.temp_folder):
            file_path = os.path.join(self.temp_folder, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f'文件已删除: {file_path}')
            except Exception as e:
                print(f'删除文件时发生错误: {e}')

    def get_pro_info(self, csv_file, pro_id):
        """
        根据商品ID获取商品信息
        """
        csv_path = os.path.join(self.csv_folder, csv_file)
        if not os.path.exists(csv_path):
            print(f'CSV文件不存在: {csv_path}')
            return

        try:
            with open(csv_path, 'r', newline='', encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                headers = next(reader)  # 读取表头

                # 找到商品ID列的索引
                id_index = -1
                for i, header in enumerate(headers):
                    if '商品ID' in header:
                        id_index = i
                        break

                if id_index == -1:
                    print('未找到商品ID列')
                    return

                # 处理每一行数据
                for row in reader:
                    if len(row) > id_index:
                        if row[id_index] == pro_id:
                            return row
                    else:
                        print(f'行数据不完整: {row}')

        except Exception as e:
            print(f'读取CSV文件时发生错误: {e}')
            return

    # 传入文件名和日期，筛选数据并保存新的csv文件到temp文件夹下
    def select_pro_by_date(self, csv_file, date):
        """
        根据日期筛选商品
        将筛选后的商品保存到新的CSV文件中，并保存在temp文件夹下
        """
        csv_path = os.path.join(self.csv_folder, csv_file)
        if not os.path.exists(csv_path):
            print(f'CSV文件不存在: {csv_path}')
            return

        # 读取原始数据
        rows = []
        try:
            with open(csv_path, 'r', newline='', encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                headers = next(reader)  # 读取表头

                # 找到日期列的索引
                date_index = -1
                for i, header in enumerate(headers):
                    if '日期' in header:
                        date_index = i
                        break

                if date_index == -1:
                    print('未找到日期列')
                    return

                # 处理每一行数据
                for row in reader:
                    if len(row) > date_index:
                        if date in row[date_index]:
                            rows.append(row)
                    else:
                        print(f'行数据不完整: {row}')

        except Exception as e:
            print(f'读取CSV文件时发生错误: {e}')
            return

        # 保存筛选后的数据到新的CSV文件
        try:
            if not os.path.exists(self.temp_folder):
                os.makedirs(self.temp_folder)

            new_csv_path = os.path.join(self.temp_folder, csv_file)
            with open(new_csv_path, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow(headers)  # 写入表头
                writer.writerows(rows)    # 写入数据行

            print(f'筛选后的数据已保存到: {new_csv_path}')

        except Exception as e:
            print(f'写入CSV文件时发生错误: {e}')



    def main(self):
        """
        创建循环，让用户选择操作
        1. 处理所有CSV文件，将所有CSV文件中的销量数据转换为整数类型
        2. 筛选所有CSV文件中销量大于等于500的商品
        3. 输入csv文件名，删除csv_file文件夹下的文件
        4. 情况temp文件夹下的所有文件
        5. 输入csv文件名，输入商品ID，返回商品信息
        6. 退出
        """
        while True:
            print('请选择操作：')
            print('1. 处理所有CSV文件，将所有CSV文件中的销量数据转换为整数类型')
            print('2. 筛选所有CSV文件中销量大于等于500的商品')
            print('3. 输入csv文件名，删除csv_file文件夹下的文件')
            print('4. 情况temp文件夹下的所有文件')
            print('5. 输入csv文件名，输入商品ID，返回商品信息')
            print('6. 退出')
            choice = input('请输入操作编号：')

            if choice == '1':
                self.handle_all_csv()
            elif choice == '2':
                self.select_all_csv_by_sales()
            elif choice == '3':
                csv_file = input('请输入csv文件名：')
                self.delete_csv_file(csv_file)
            elif choice == '4':
                self.clear_temp_folder()
            elif choice == '5':
                csv_file = input('请输入csv文件名：')
                pro_id = input('请输入商品ID：')
                pro_info = self.get_pro_info(csv_file, pro_id)
                print(pro_info)
            elif choice == '6':
                break
            else:
                print('无效的操作编号，请重新输入')



if __name__ == '__main__':
    handler = HandleDatas()
    csv_file = input('请输入csv文件名：')
    date = input('请输入日期：')
    handler.select_pro_by_date(csv_file, date)




    