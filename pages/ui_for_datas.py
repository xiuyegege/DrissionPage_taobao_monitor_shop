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
from handle_data import HandleDatas
from get_img import GetImages

hd = HandleDatas()
gi = GetImages()
st.title("数据处理和图片下载")
with st.sidebar:
    # 一键清洗所有店铺数据
    st.subheader('清洗所有店铺数据')
    if st.button('点击清洗', key='clean_all_button'):
        result = hd.handle_all_csv()
        st.success(result)
    
    # 分割线
    st.markdown('---')
    
    # 一键下载清洗后的所有店铺图片
    st.subheader('下载清洗后的所有店铺图片')
    if st.button('点击下载', key='download_all_csv_button'):
        result = gi.get_all_imgs()
        st.success(result)
    
    # 分割线
    st.markdown('---')

    # 一键情况临时文件夹
    st.subheader('清空临时文件夹')
    st.write('这里是筛选后的店铺数据')
    if st.button('点击清空', key='clear_temp_button'):
        result = hd.clear_temp_folder()
        st.success(result)
    

# scv_file文件夹中获取所有csv文件
csv_files = [f for f in os.listdir(os.path.join(project_root, 'csv_file')) if f.endswith('.csv')]

tab1 , tab2 , tab3 = st.tabs(['单个店铺数据处理', '监控店铺数据处理', '单产品页下载'])

with tab1:

    col11 , col12 ,col13 = st.columns(3)


    with col11:

        st.subheader('单店铺销量数据清洗')
        # 通过下来选项框，选择要清洗销售数据的csv文件,通过button按钮修改销售数据
        csv_file_to_change_sales = st.selectbox('请选择要清洗销售数据的csv文件', csv_files, key='change_sales_csv_selectbox')
        if st.button('修改', key='modify_button'):
            result = hd.change_sales(csv_file_to_change_sales)
            st.success(result)

    with col12:
        # 通过下拉选项框，选择要处理的csv文件，填写输入框选择要筛选的销量，通过button按钮筛选数据
        st.subheader('单店铺销量筛选')
        st.write('筛选后数据保存在temp文件夹下')
        filter_single_csv_file_by_sales = st.selectbox('请选择要处理的csv文件', csv_files, key='filter_csv_by_single_sales_selectbox')
        sals_volume = st.number_input('请输入要筛选的销量', min_value=500, step=100, key='filter_csv_by_single_sales_input')
        if st.button('筛选', key='filter_button'):
            result = hd.select_pro_by_csv(filter_single_csv_file_by_sales, sals_volume)
            st.success(result)
            
    with col13:
        st.subheader('删除店铺文件')
        # 通过下拉选项框选择要删除的csv文件，通过button按钮删除csv文件
        csv_file_to_delete = st.selectbox('请选择要删除的csv文件', csv_files, key='delete_csv_selectbox')
        if st.button('删除', key='del_button'):
            result = hd.delete_csv_file(csv_file_to_delete)
            st.success(result)
    
    # 通过下拉框，选择temp文件夹下的csv文件，通过button按钮下载商品图片
    st.subheader('下载选中店铺商品图')
    st.write('这里是经过销量筛选后保存在temp文件夹下的店铺csv文件')
    image_csv_files = [f for f in os.listdir(os.path.join(project_root, 'temp')) if f.endswith('.csv')]
    image_csv_file = st.selectbox('请选择要下载商品图片的csv文件', image_csv_files, key='download_image_single_csv_selectbox')
    if st.button('下载', key='download_image_button'):
        result = gi.get_img_from_csv(image_csv_file)
        st.success(result)


with tab2:

    # 通过销量筛选所有csv_file下的csv文件
    st.subheader('所有监控店铺销量筛选')
    st.write('筛选后数据保存在temp文件夹下')
    sals_volume = st.number_input('请输入要筛选的销量', min_value=500, step=100, key='filter_csv_by_all_sales_input')
    if st.button('筛选', key='filter_all_button'):
        result = hd.select_all_csv_by_sales(sals_volume)
        st.success(result)

    # 分割线
    st.markdown('---')

    col21 , col22 = st.columns(2)
    with col21:
        # 下拉框选择要处理的csv文件，输入年月日，通过button按钮筛选数据
        st.subheader('单店铺按日期筛选')
        st.write('筛选后数据保存在temp文件夹下')
        filter_single_csv_file_by_date = st.selectbox('请选择要处理的csv文件', csv_files, key='filter_csv_by_single_date_selectbox')
        date = st.text_input('请输入要筛选的年份', key='filter_csv_by_single_date_year_input')
        if st.button('筛选', key='filter_date_button'):
            result = hd.select_pro_by_date(filter_single_csv_file_by_date, date)
            st.success(result)



    with col22:
        # 通过下拉框，选择temp文件夹下的csv文件，通过button按钮下载商品图片
        st.subheader('下载店铺所有商品图')
        st.write('这里是经过销量筛选后保存在temp文件夹下的店铺csv文件')
        image_csv_files = [f for f in os.listdir(os.path.join(project_root, 'temp')) if f.endswith('.csv')]
        image_csv_file = st.selectbox('请选择要下载商品图片的csv文件', image_csv_files, key='download_image_single_csv_by_monitor_selectbox')
        if st.button('下载', key='download_image_by_monitor_button'):
            result = gi.get_img_from_csv(image_csv_file)
            st.success(result)


with tab3:


    # 输入商品url，通过button按钮下载店铺图片
    st.subheader('产品页主图下载')
    shop_url = st.text_input('请输入要下载店铺图片的店铺url', key='download_image_single_shop_url_input')
    if st.button('下载', key='download_image_single_shop_button'):
        result = gi.get_img_from_product_page(shop_url)
        st.success(result)

    # 分割线
    st.markdown('---')

    # 通过下拉框，选择csv_flie文件夹下的csv文件，，输入商品ID，通过button按钮下载商品图片
    st.subheader('通过商品id下载商品页主图')
    csv_file = st.selectbox('请选择要下载商品图片的csv文件', csv_files, key='download_image_by_id_csv_selectbox')
    product_id = st.text_input('请输入要下载商品图片的商品id', key='download_image_by_id_input')
    if st.button('下载', key='download_image_by_id_button'):
        result = gi.get_img_from_csv_by_id(csv_file, product_id)
        st.success(result)