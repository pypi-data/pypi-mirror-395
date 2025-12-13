import zipfile
import shutil
import tempfile
from pathlib import Path
from typing import Optional, Callable
import logging
from contextlib import contextmanager

from .models import PluginConfig

logger = logging.getLogger("PluginManager.ArchiveHandler")


class ArchiveHandler:
    def __init__(self):
        pass

    def extract_archive(self, archive_path: Path, extract_dir: Path) -> bool:
        """解压归档文件"""
        try:
            if archive_path.suffix.lower() == '.zip':
                with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                    # 首先验证zip文件
                    bad_file = zip_ref.testzip()
                    if bad_file:
                        raise zipfile.BadZipFile(f"ZIP文件损坏: {bad_file}")

                    zip_ref.extractall(extract_dir)
                logger.info(f"ZIP解压完成: {extract_dir}")
                return True
            else:
                logger.error(f"不支持的压缩格式: {archive_path.suffix}")
                return False
        except zipfile.BadZipFile as e:
            logger.error(f"ZIP文件损坏: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"解压失败: {str(e)}")
            return False

    def package_plugin(self, plugin_name: str, plugin_dir: Path, output_dir: Path,
                       plugin_config: PluginConfig = None,
                       progress_callback: Optional[Callable[[float, str], None]] = None) -> Optional[Path]:
        """
        打包插件为zip文件

        Args:
            plugin_name: 插件名称
            plugin_dir: 插件目录路径
            output_dir: 输出目录路径
            plugin_config: 插件配置对象
            progress_callback: 进度回调函数，参数为(当前进度, 当前文件)

        Returns:
            打包后的zip文件路径，失败返回None
        """
        if not plugin_dir.exists():
            logger.error(f"插件目录不存在: {plugin_dir}")
            return None

        # 确保输出目录存在
        if not output_dir.exists():
            output_dir.mkdir(parents=True, exist_ok=True)

        # 获取插件配置的版本信息
        version = plugin_config.current_version if plugin_config else "1.0.0"
        zip_filename = f"{plugin_name}-{version}.zip"
        zip_path = output_dir / zip_filename

        try:
            # 首先获取所有要打包的文件列表，用于计算总进度
            file_list = []
            for file_path in plugin_dir.rglob('*'):
                if file_path.is_file():
                    file_list.append(file_path)

            total_files = len(file_list)
            current_file = 0

            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # 遍历插件目录中的所有文件和子目录
                for file_path in file_list:
                    current_file += 1

                    # 计算在zip文件中的相对路径
                    arcname = file_path.relative_to(plugin_dir)
                    zipf.write(file_path, arcname)

                    # 调用进度回调
                    if progress_callback:
                        progress_callback(current_file * 100 / total_files, str(arcname))

                    logger.debug(f"添加文件: {arcname}")

            logger.info(f"插件打包成功: {zip_path}")

            # 最后调用一次回调表示完成
            if progress_callback:
                progress_callback(total_files * 100 / total_files, "完成")

            return zip_path

        except Exception as e:
            logger.error(f"打包插件失败: {str(e)}")

            # 出错时也调用回调
            if progress_callback:
                progress_callback(-1, total_files if 'total_files' in locals() else 0, f"错误: {str(e)}")

            return None

    @contextmanager
    def temp_directory(self, temp_plugin_dir: Optional[Path] = None):
        """临时目录上下文管理器"""
        temp_dir = None
        try:
            if temp_plugin_dir is None:
                temp_dir = Path(tempfile.mkdtemp())
            else:
                temp_dir = temp_plugin_dir
            yield temp_dir
        finally:
            if temp_dir and temp_dir.exists():
                try:
                    shutil.rmtree(temp_dir)
                except Exception as e:
                    logger.warning(f"清理临时目录失败 {temp_dir}: {str(e)}")
