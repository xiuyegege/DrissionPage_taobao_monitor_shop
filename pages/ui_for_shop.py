import streamlit as st
import pandas as pd
import sys
import os

st.set_page_config(layout="wide")

# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from config import project_root
from control_shop_info import ControlShopInfo
from get_datas import GetHotSellingDatas
from monitor_shop import MonitorShop


ctsp = ControlShopInfo()
ghsd = GetHotSellingDatas()
ms = MonitorShop()

with st.sidebar:
    st.subheader('启动店铺监控')
    if st.button('一键启动'):
        ms.scan_shop_by_weekday()
        st.success('启动成功')



st.title('店铺信息管理')

# 输入店铺名称，店铺url，翻页次数获取数据
st.subheader('获取数据')
shop_name = st.text_input('请输入店铺名称')
shop_url = st.text_input('请输入店铺URL')
scoll_num = st.number_input('请输入翻页次数', min_value=1, max_value=100, value=4)

if st.button('获取数据'):
    ghsd.get_shop_info(shop_name, shop_url, scoll_num)
    st.success('数据获取成功')


# 分割线
st.markdown('---')
# 获取店铺信息（返回三个列表的元组）
shop_name_list, shop_url_list, scan_weekday_list = ctsp.get_all_shop_info()
# 将列表数据转换为DataFrame格式
if shop_name_list:
    # 创建DataFrame
    df = pd.DataFrame({
        '店铺名称': shop_name_list,
        '店铺URL': shop_url_list,
        '扫描星期': scan_weekday_list
    })
    
    # 显示表格
    st.subheader('店铺信息预览')
    st.dataframe(df, use_container_width=True)
    
    # 显示统计信息
    st.info(f'共有 {len(shop_name_list)} 个店铺')
else:
    st.warning('暂无店铺信息')

col1, col2 ,col3 ,col4= st.columns([2,2,2,1])
with col1:
        # 添加店铺信息
    st.subheader('添加店铺信息')
    shop_name = st.text_input('店铺名称', key='add_shop_name')
    shop_url = st.text_input('店铺URL', key='add_shop_url')
    scan_weekday = st.text_input('扫描时间（整数1~7）', key='add_scan_weekday')

    if st.button('添加', key='add_button'):
        result = ctsp.add_shop_info(shop_name, shop_url, scan_weekday)
        st.success(result)


with col2:
    #显示店铺信息
    st.subheader('查看店铺信息')
    shop_name = st.text_input('请输入店铺名称', key='view_shop_name')
    if st.button('查看', key='view_button'):
        result = ctsp.chekc_shop_info(shop_name)
        if result:
            st.write('店铺url')
            st.success(f'{result["shop_url"]}')
            st.success(f'扫描时间: {result["scan_weekday"]}')
        else:
            st.error('店铺不存在')
        
    

with col3:
    # 修改店铺信息
    st.subheader('修改店铺信息')
    shop_name = st.text_input('请输入店铺名称', key='update_shop_name')
    shop_url = st.text_input('请输入店铺URL', key='update_shop_url')
    scan_weekday = st.text_input('请输入扫描时间（整数1~7）', key='update_scan_weekday')

    if st.button('修改', key='update_button'):
        result = ctsp.update_shop_info(shop_name, shop_url, scan_weekday)
        st.success(result)

with col4:
    # 删除店铺信息
    st.subheader('删除店铺信息')
    shop_name = st.text_input('请输入店铺名称', key='del_shop_name')
    if st.button('删除', key='del_button'):
        result = ctsp.del_shop_info(shop_name)
        st.success(result)

# 分割线
st.markdown('---')

# 从log目录下读取new_data_log.csv文件，并显示在页面上
log_dir = os.path.join(project_root, 'log')
log_file = os.path.join(log_dir, 'new_data_log.csv')

if os.path.exists(log_file):
    st.subheader('最新数据日志')
    df = pd.read_csv(log_file)
    st.dataframe(df, use_container_width=True)
else:
    st.warning('暂无日志数据')