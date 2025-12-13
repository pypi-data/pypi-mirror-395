"""
BiliHome - B站用户信息获取模块
"""

import requests
import json
import re


class Bili:
    """
    B站用户信息类
    
    Args:
        vmid (str): B站用户的唯一标识符（个人主页ID）
    """
    
    def __init__(self, vmid):
        """
        初始化Bili类
        
        Args:
            vmid (str): B站用户的唯一标识符
        """
        self.vmid = vmid
        self.base_url = "https://api.bilibili.com/x/relation/stat"
    
    def fans(self):
        """
        获取用户的粉丝数量
        
        Returns:
            int: 用户的粉丝数量，如果请求失败返回None
        """
        try:
            # 构建API请求URL
            url = f"{self.base_url}?vmid={self.vmid}"
            
            # 添加必要的请求头
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Referer": "https://www.bilibili.com/",
                "Accept": "application/json, text/plain, */*"
            }
            
            # 发送GET请求
            response = requests.get(url, headers=headers)
            
            # 检查请求是否成功
            if response.status_code == 200:
                data = response.json()
                
                # 检查API返回状态
                if data.get("code") == 0:
                    # 返回粉丝数量
                    return data["data"]["follower"]
                else:
                    print(f"API返回错误: {data.get('message', '未知错误')}")
                    return None
            else:
                print(f"HTTP请求失败，状态码: {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"网络请求异常: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
            return None
        except KeyError as e:
            print(f"数据格式错误，缺少必要字段: {e}")
            return None
    
    def follows(self):
        """
        获取用户的关注数量
        
        Returns:
            int: 用户的关注数量，如果请求失败返回None
        """
        try:
            # 构建API请求URL
            url = f"{self.base_url}?vmid={self.vmid}"
            
            # 添加必要的请求头
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Referer": "https://www.bilibili.com/",
                "Accept": "application/json, text/plain, */*"
            }
            
            # 发送GET请求
            response = requests.get(url, headers=headers)
            
            # 检查请求是否成功
            if response.status_code == 200:
                data = response.json()
                
                # 检查API返回状态
                if data.get("code") == 0:
                    # 返回粉丝数量
                    return data["data"]["following"]
                else:
                    print(f"API返回错误: {data.get('message', '未知错误')}")
                    return None
            else:
                print(f"HTTP请求失败，状态码: {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"网络请求异常: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
            return None
        except KeyError as e:
            print(f"数据格式错误，缺少必要字段: {e}")
            return None

    def name(self):
        """
        获取用户名称
        
        Returns:
            str: 用户名称，如果获取失败返回None
        """
        url = f"https://m.bilibili.com/space/{self.vmid}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'https://www.bilibili.com/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-site',
            'Cache-Control': 'max-age=0'
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            html_content = response.text
            
            # 方法1：从页面标题中提取用户名
            title_match = re.search(r'<title>([^<]+)</title>', html_content)
            if title_match:
                title = title_match.group(1)
                
                # 尝试从标题中提取用户名
                if '的个人空间' in title:
                    user_name = title.split('的个人空间')[0]
                    return user_name
                elif '的个人主页' in title:
                    user_name = title.split('的个人主页')[0]
                    return user_name
            
            # 方法2：从meta关键词中提取
            meta_keywords_match = re.search(r'<meta[^>]*name="keywords"[^>]*content="([^"]+)"', html_content)
            if meta_keywords_match:
                keywords = meta_keywords_match.group(1)
                if '的个人空间' in keywords:
                    user_name = keywords.split('的个人空间')[0]
                    return user_name
            
            # 方法3：尝试原始的正则表达式模式（兼容旧版本页面结构）
            patterns = [
                r'<div[^>]*data-v-2497e204[^>]*class="name"[^>]*>([^<]+)</div>',
                r'<div[^>]*class="name"[^>]*data-v-2497e204[^>]*>([^<]+)</div>',
                r'<div[^>]*class="name"[^>]*>([^<]+)</div>',
                r'<h1[^>]*class="name"[^>]*>([^<]+)</h1>'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, html_content)
                if match:
                    user_name = match.group(1).strip()
                    return user_name
            
            # 如果所有方法都不匹配，返回None
            return None
            
        except requests.RequestException as e:
            print(f"网络请求错误: {e}")
            return None
        except re.error as e:
            print(f"正则表达式错误: {e}")
            return None
        except Exception as e:
            print(f"其他错误: {e}")
            return None