import os


class PluginUtil:
    @classmethod
    def get_resource_path(cls, relative_path):
        """
        获取资源的绝对路径（兼容PyStand打包/源码环境）
        """
        # 拼接绝对路径（兼容Windows/Linux）
        return os.path.join(cls.get_work_path(), relative_path)

    @classmethod
    def get_work_path(cls):
        """
        获取资源的绝对路径（兼容PyStand打包/源码环境）
        """
        # 判断是否为PyStand打包环境
        if os.environ.get("PYSTAND") is not None:
            base_path = os.environ.get("PYSTAND_HOME")
        else:
            # 源码环境，基于当前脚本所在目录
            base_path = os.getcwd()

        return base_path
