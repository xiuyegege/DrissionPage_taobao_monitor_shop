import streamlit as st
from get_datas import GetHotSellingDatas
import os
import pandas as pd
from config import project_root

ghsd = GetHotSellingDatas()


st.title("竞店爆款数据监控采集")



with st.sidebar:

    # 按键登录淘宝
    st.subheader('登录淘宝')
    if st.button("打开登录淘宝"):
        ghsd.login_tb()
        st.success("打开成功")
        st.write("浏览器打开之后手动完成登录")

    # 分割线
    st.markdown("---")

    # 按键打开csv_file文件夹
    st.subheader('打开csv_file文件夹')
    if st.button("打开csv_file文件夹"):
        os.system("start " + os.path.join(project_root, 'csv_file'))
        st.success("打开成功")

    # 分割线
    st.markdown("---")

    # 按键打开temp文件夹
    st.subheader('打开temp文件夹')
    if st.button("打开temp文件夹"):
        os.system("start " + os.path.join(project_root, 'temp'))
        st.success("打开成功")


# 分割线
st.markdown("---")

st.subheader('店铺数据预览')
# 从下拉选项框从scv_file文件夹中获取所有csv文件
csv_files = [f for f in os.listdir(os.path.join(project_root, 'csv_file')) if f.endswith('.csv')]
# 从下拉选项框中选择一个csv文件
csv_file = st.selectbox('请选择一个店铺文件', csv_files)
# 从csv文件中读取数据
df = pd.read_csv(os.path.join(project_root, 'csv_file', csv_file))
# 显示数据
st.dataframe(df,use_container_width=True)

# 分割线
st.markdown('---')