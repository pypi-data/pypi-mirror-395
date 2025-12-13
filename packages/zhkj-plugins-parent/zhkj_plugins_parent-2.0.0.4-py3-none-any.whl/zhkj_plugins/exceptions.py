'''
Author: yasin l1y0l20@qq.com
Date: 2025-10-28 14:04:31
LastEditors: yasin l1y0l20@qq.com
LastEditTime: 2025-11-07 18:38:38
FilePath: /zhkj-plugins/zhkj_plugins/exceptions.py
Description: 

Copyright (c) 2021-2025 by yasin, All Rights Reserved. 
'''

# 自定义异常类
class PluginManagerError(Exception):
    """插件管理器基础异常"""
    pass


class PluginNotFoundError(PluginManagerError):
    """插件未找到异常"""
    pass


class PluginInstallError(PluginManagerError):
    """插件安装异常"""
    pass


class PluginUpdateError(PluginManagerError):
    """插件更新异常"""
    pass


class PluginStartError(PluginManagerError):
    """插件启动异常"""
    pass


class NetworkError(PluginManagerError):
    """网络异常"""
    pass


class SecurityError(PluginManagerError):
    """安全相关异常"""
    pass
