# DPTB 监控程序

这是一个用于监控淘宝店铺数据的程序，使用 DrissionPage 库来自动化浏览器操作并监听网络请求。

## 文件说明

- `get_datas.py` - 原始程序（已修复异常处理）
- `get_datas_improved.py` - 改进版程序（推荐使用）
- `config.py` - 配置文件
- `README.md` - 说明文档

## 问题分析

### 原始问题
程序在 `page.listen.wait(5)` 处等待很长时间没有监听到数据，可能的原因：

1. **API接口变更** - 淘宝可能更改了API接口名称
2. **反爬虫机制** - 网站检测到自动化行为
3. **页面结构变化** - 页面元素选择器失效
4. **网络请求时机** - 请求触发条件不满足
5. **等待时间不足** - 网络请求需要更长时间

### 解决方案

#### 1. 多API监听
```python
api_patterns = [
    'mtop.taobao.shop.simple.fetch',
    'mtop.taobao.shop.item.list',
    'mtop.relationrecommend.wirelessrecommend.recommend',
    'mtop.taobao.detail.getdetail',
    'shop.simple.fetch'
]
```

#### 2. 增强异常处理
- 添加 KeyboardInterrupt 处理
- 详细的错误日志
- 程序优雅退出

#### 3. 调试功能
- 带时间戳的日志
- 响应数据预览
- 监听器状态检查

#### 4. 备用方案
- 监听所有网络请求
- 多种元素选择器
- 自动重试机制

## 使用方法

### 运行原始程序（已修复）
```bash
python get_datas.py
```

### 运行改进版程序（推荐）
```bash
python get_datas_improved.py
```

## 配置说明

在 `config.py` 中可以调整以下参数：

### API监听配置
```python
API_PATTERNS = [
    'mtop.taobao.shop.simple.fetch',  # 主要API
    'mtop.taobao.shop.item.list',     # 商品列表API
    # ... 更多API模式
]
```

### 等待时间配置
```python
WAIT_CONFIG = {
    'page_load': 3,        # 页面加载等待时间
    'request_timeout': 10, # 网络请求超时时间
    'between_attempts': (2, 5)  # 尝试间隔时间
}
```

### 调试配置
```python
DEBUG_CONFIG = {
    'verbose': True,           # 显示详细日志
    'save_responses': False,   # 保存响应数据
    'response_preview_length': 500  # 响应预览长度
}
```

## 故障排除

### 1. 仍然无法监听到数据

**可能原因：**
- 网站使用了新的反爬虫机制
- API接口完全变更
- 需要登录才能访问数据

**解决方法：**
1. 手动登录后再运行程序
2. 使用开发者工具查看实际的网络请求
3. 更新API监听模式

### 2. 程序运行缓慢

**解决方法：**
1. 减少等待时间配置
2. 关闭详细日志 (`verbose: False`)
3. 减少重试次数

### 3. 浏览器无法启动

**解决方法：**
1. 检查 Chrome 浏览器是否正确安装
2. 更新 DrissionPage 库
3. 检查系统权限

## 开发者工具使用

### 查看网络请求
1. 打开浏览器开发者工具 (F12)
2. 切换到 Network 标签
3. 刷新页面或执行操作
4. 查看实际的API请求URL
5. 更新 `config.py` 中的 `API_PATTERNS`

### 查看页面元素
1. 右键点击页面元素
2. 选择"检查元素"
3. 查看元素的class、id等属性
4. 更新元素选择器

## 注意事项

1. **遵守网站条款** - 请确保使用符合网站服务条款
2. **适度使用** - 避免过于频繁的请求
3. **数据用途** - 仅用于学习和研究目的
4. **及时更新** - 网站结构变化时需要更新代码

## 依赖库

```bash
pip install DrissionPage
```

## 版本历史

- v1.0 - 原始版本
- v1.1 - 添加异常处理和调试信息
- v2.0 - 重构代码，添加配置文件和改进的监听策略