# BiliHome

一个用于获取B站用户信息的Python包

## 功能特性

- 获取B站用户的粉丝数量
- 获取B站用户的关注数量  
- 获取B站用户的用户名
- 简单易用的API接口
- 自动处理网络请求异常

## 安装

### 使用pip安装（推荐）

```bash
pip install BiliHome
```

### 从源码安装

```bash
git clone https://github.com/Moxin1044/BiliHome.git
cd BiliHome
pip install .
```


## 快速开始

### 基本用法

```python
from BiliHome import Bili

# 创建Bili实例（使用用户的vmid）
bili_user = Bili("8047632")

# 获取粉丝数量
fans_count = bili_user.fans()
print(f"粉丝数量: {fans_count}")

# 获取关注数量
follows_count = bili_user.follows()
print(f"关注数量: {follows_count}")

# 获取用户名
username = bili_user.name()
print(f"用户名: {username}")
```

### 完整示例

```python
#!/usr/bin/env python3
"""
BiliHome使用示例
"""

import sys
import os

# 添加当前目录到Python路径，以便导入BiliHome包
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from BiliHome import Bili

def main():
    """主函数"""
    print("BiliHome示例程序")
    
    # 使用示例中的vmid
    vmid = "8047632"
    
    # 创建Bili实例
    bili_user = Bili(vmid)
    
    # 获取粉丝数量
    fans_count = bili_user.fans()
    
    if fans_count is not None:
        print(f"用户 {vmid} 的粉丝数量: {fans_count}")
    else:
        print("获取粉丝数量失败，请检查网络连接或vmid是否正确")
    
    # 获取关注数量
    follows_count = bili_user.follows()
    if follows_count is not None:
        print(f"用户 {vmid} 的关注数量: {follows_count}")
    else:
        print("获取关注数量失败，请检查网络连接或vmid是否正确")

    # 获取用户名
    username = bili_user.name()
    if username is not None:
        print(f"用户 {vmid} 的用户名: {username}")
    else:
        print("获取用户名失败，请检查网络连接或vmid是否正确")

if __name__ == "__main__":
    main()
```

## API文档

### Bili类

#### 构造函数

```python
Bili(vmid)
```

**参数:**
- `vmid` (str): B站用户的唯一标识符（个人主页ID）

#### 方法

##### `fans()`

获取用户的粉丝数量

**返回值:**
- `int`: 用户的粉丝数量，如果请求失败返回`None`

##### `follows()`

获取用户的关注数量

**返回值:**
- `int`: 用户的关注数量，如果请求失败返回`None`

##### `name()`

获取用户的用户名

**返回值:**
- `str`: 用户名称，如果获取失败返回`None`

## 运行测试

项目包含一个测试文件，可以验证包的功能：

```bash
python test_bili.py
```

## 依赖

- Python 3.6+
- requests >= 2.25.0

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request来改进这个项目。

## 支持

如果您在使用过程中遇到问题，请通过以下方式联系：
- 提交Issue: [GitHub Issues](https://github.com/Moxin1044/BiliHome/issues)
- 查看源码: [GitHub Repository](https://github.com/Moxin1044/BiliHome)

## 版本历史

- v0.1.0 (当前版本)
  - 初始版本发布
  - 支持获取粉丝数量、关注数量和用户名

## 注意事项

1. 请确保网络连接正常，因为所有数据都通过B站API获取
2. 请遵守B站的使用条款和API调用频率限制
3. 如果遇到请求失败，请检查网络连接和vmid是否正确
4. 本工具仅用于学习和开发目的，请勿用于商业用途