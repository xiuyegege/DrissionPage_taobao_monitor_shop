import os
import csv
import time
from config import project_root

class LogNewData:
    """日志记录类，用于管理CSV文件的创建和数据写入"""
    
    def __init__(self):
        self.log_dir = os.path.join(project_root, 'log')
        self.csv_path = os.path.join(self.log_dir, 'new_data_log.csv')
        self.headers = ['csv文件名', '商品id','记录日期']
    
    def create_log_csv(self):
        """创建一个csv文件到log目录下,文件名是new_data_log.csv
        表头是['csv文件名','记录日期']
        """
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        with open(self.csv_path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(self.headers)
        print(f'CSV文件已创建: {self.csv_path}')
    
    def write_log_csv(self, csv_file_name,pro_id):
        """将参数'csv文件名'和'记录日期'写入csv文件
        
        Args:
            csv_file_name (str): 要记录的CSV文件名
        """
        if not os.path.exists(self.csv_path):
            self.create_log_csv()
        record_date = time.strftime("%Y-%m-%d")
        with open(self.csv_path, 'a', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow([csv_file_name,pro_id, record_date])
        print(f'已将{csv_file_name}写入CSV文件')

if __name__ == '__main__':
    log = LogNewData()
    log.create_log_csv()