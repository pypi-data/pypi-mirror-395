# ZHKJ Plugins 插件管理系统

一个功能强大的插件管理系统，支持插件安装、更新、依赖管理和安全的RPC调用。

## 功能特性

### 🔌 插件管理
- 插件安装、卸载、更新
- 自动依赖管理
- 版本控制和更新检查
- 插件运行状态监控

### 🔒 安全RPC调用
- 注解式RPC调用系统
- AES加密数据传输
- 统一响应格式
- 类型安全的接口调用

### 🛡️ 依赖管理
- 自动处理插件依赖关系
- 依赖冲突检测和解决
- 安全卸载检查
- 依赖树分析

## 快速开始

### 安装

```bash
pip install -r requirements.txt
```

### 基本使用

```python
from zhkj_plugins.plugin_manager import PluginManager

# 初始化插件管理器
plugin_manager = PluginManager(config_path="config.yaml")

# 列出所有插件
plugin_manager.print_plugin_list()

# 安装插件
plugin_manager.install_plugin("data_processor")

# 启动插件
plugin_manager.start_plugin("data_processor")

# 检查更新
updates = plugin_manager.check_all_updates()
```

## 插件更新依赖管理

系统现在支持插件更新时的自动依赖管理：

```python
# 更新插件时会自动处理依赖关系
plugin_manager.update_plugin("data_processor", version_info)

# 自动检查和处理：
# - 新增依赖的自动安装
# - 版本变更依赖的验证
# - 依赖不满足时的安全回滚
```

## RPC调用系统

### 加密工具

```python
from zhkj_plugins.secret_util import SecretUtil

# 初始化加密工具
secret_util = SecretUtil("your_secret_key_32bytes")

# 加密数据
encrypted = secret_util.encrypt_data("hello world")

# 解密数据
decrypted = secret_util.decrypt_data(encrypted)
```

### 注解式RPC调用

创建插件调用类：

```python
from zhkj_plugins.plugin_caller import rpc_class, rpc_method, RPCCallerBase

@rpc_class("data_processor")
class DataProcessorCaller(RPCCallerBase):
    
    @rpc_method("process_data", timeout=30)
    def process_data(self, input_data: str, mode: str = "normal"):
        """处理数据 - 只需声明，无需实现"""
        pass
    
    @rpc_method("batch_process", endpoint="/api/batch")
    def batch_process(self, items: list, chunk_size: int = 100):
        """批量处理"""
        pass
```

使用RPC调用：

```python
# 初始化调用器
data_caller = DataProcessorCaller(plugin_manager)

# 调用插件方法
result = data_caller.process_data("test data", mode="fast")

# 处理结果
if result["success"]:
    data = result["data"]
    print(f"调用成功: {data}")
else:
    print(f"调用失败: {result['message']}")
```

### 固定返回格式

所有RPC调用返回统一的格式：

```python
{
    "success": True,           # 调用是否成功
    "data": any,              # 返回数据
    "message": "调用成功",     # 成功/错误信息
    "timestamp": "2024-01-01T10:00:00",  # 时间戳
    "request_id": "uuid",     # 请求ID
    "plugin": "data_processor", # 插件名称
    "method": "process_data"  # 调用方法
}
```

## 配置说明

### 环境变量

```bash
# 加密密钥（必须）
export PLUGIN_SECRET_KEY="your_32byte_secret_key_here"

# 插件安装目录（可选）
export PLUGIN_INSTALL_DIR="./plugins"
```

### 配置文件

创建 `config.yaml`：

```yaml
# 基本配置
plugin_install_dir: "plugins"
auto_check_updates: true

# 版本检查配置
version_check:
  base_url: "https://api.example.com/plugins"
  cache_ttl: 3600

# 插件配置
plugins:
  data_processor:
    auto_update: true
    dependencies:
      - "common_utils"
      - "data_formatter"
```

## 高级功能

### 依赖分析

```python
# 分析插件依赖关系
dependency_report = plugin_manager.analyze_dependencies()

# 获取依赖树
dependency_tree = plugin_manager.get_dependency_tree("data_processor")

# 安全卸载检查
can_uninstall, dependents = plugin_manager.dependency_manager.can_safely_uninstall("plugin_name")
```

### 批量操作

```python
# 安装所有插件
results = plugin_manager.install_all_plugins()

# 自动更新所有插件
update_results = plugin_manager.auto_update_plugins()

# 批量验证依赖
validation_results = plugin_manager.dependency_manager.batch_validate_dependencies(plugins)
```

## 开发指南

### 创建新的插件调用类

1. 继承 `RPCCallerBase` 基类
2. 使用 `@rpc_class` 注解指定插件名称
3. 使用 `@rpc_method` 注解声明方法

```python
@rpc_class("your_plugin_name")
class YourPluginCaller(RPCCallerBase):
    
    @rpc_method("your_method")
    def your_method(self, param1: str, param2: int = 0):
        """方法描述"""
        pass
```

### 错误处理

```python
try:
    result = caller.your_method("param")
    if not result["success"]:
        logger.error(f"RPC调用失败: {result['message']}")
        # 处理错误
except Exception as e:
    logger.error(f"调用异常: {str(e)}")
```

## 示例代码

更多使用示例请参考 `zhkj_plugins/examples/` 目录：

- `data_processor_caller.py` - 数据处理插件调用示例
- 更多示例待添加...

## 注意事项

1. **加密密钥安全**：生产环境务必设置安全的 `PLUGIN_SECRET_KEY` 环境变量
2. **依赖管理**：更新插件时确保网络连接稳定，以便自动安装依赖
3. **错误处理**：所有RPC调用都应检查返回的 `success` 字段
4. **超时设置**：根据插件方法复杂度合理设置超时时间
5. **资源清理**：程序退出时调用 `plugin_manager.cleanup()` 释放资源

## 故障排除

### 常见问题

1. **插件无法启动**
   - 检查端口是否被占用
   - 验证插件依赖是否满足

2. **RPC调用失败**
   - 检查插件是否正在运行
   - 验证加密密钥是否正确
   - 检查网络连接

3. **依赖安装失败**
   - 检查网络连接
   - 验证依赖插件是否存在
   - 查看详细错误日志

### 日志调试

启用详细日志：

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 许可证

本项目采用 MIT 许可证。详细信息请查看 LICENSE 文件。
