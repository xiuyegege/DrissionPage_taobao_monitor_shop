@echo off
echo 正在启动DPTB监控程序...
echo.

REM 激活虚拟环境
echo 激活虚拟环境...
call venv\Scripts\activate.bat

REM 检查虚拟环境是否激活成功
if errorlevel 1 (
    echo 错误：无法激活虚拟环境
    pause
    exit /b 1
)

echo 虚拟环境激活成功！
echo.

REM 启动Streamlit应用
echo 启动Streamlit应用...
streamlit run main.py

REM 如果Streamlit退出，暂停以查看任何错误信息
if errorlevel 1 (
    echo.
    echo Streamlit应用已退出
    pause
)