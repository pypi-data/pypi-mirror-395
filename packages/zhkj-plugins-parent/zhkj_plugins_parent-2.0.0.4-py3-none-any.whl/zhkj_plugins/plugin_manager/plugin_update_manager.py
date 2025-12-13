import time
import threading
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any
import logging

from .progresses import InstallDownloadBridge, SubProgress
from .models import PluginConfig, VersionInfo
from .plugin_loader import PluginLoader
from .config_manager import ConfigManager
from .version_manager import VersionManager
from .download_manager import DownloadManager
from .archive_handler import ArchiveHandler
from .plugin_runtime_manager import PluginRuntimeManager
from ..task_progress_manager import NestedProgressCallback

logger = logging.getLogger("PluginManager.Update")


class PluginUpdateManager:
    def __init__(self, plugin_loader: PluginLoader, config_manager: ConfigManager, version_manager: VersionManager,
                 download_manager: DownloadManager, archive_handler: ArchiveHandler,
                 plugin_install_dir: Path, runtime_manager: PluginRuntimeManager,
                 dependency_manager=None, install_manager=None):
        self.plugin_loader = plugin_loader
        self.config_manager = config_manager
        self.version_manager = version_manager
        self.download_manager = download_manager
        self.archive_handler = archive_handler
        self.plugin_install_dir = plugin_install_dir
        self.runtime_manager = runtime_manager
        self.dependency_manager = dependency_manager
        self.install_manager = install_manager

    def _start_auto_update_check(self, plugins: List[PluginConfig]) -> None:
        """启动自动更新检查后台线程"""

        def check_updates_background():
            while True:
                try:
                    # 每6小时检查一次更新
                    time.sleep(6 * 3600)
                    self.check_all_updates(plugins, background=True)
                except Exception as e:
                    logger.error(f"后台更新检查失败: {str(e)}")
                    time.sleep(300)  # 出错后等待5分钟再重试

        thread = threading.Thread(target=check_updates_background, daemon=True)
        thread.start()
        logger.info("自动更新检查线程已启动")

    def check_plugin_update(self, plugin_name: str, plugins: List[PluginConfig]) -> Tuple[bool, Optional[VersionInfo]]:
        """检查插件是否有更新"""
        plugin = self._get_plugin_info(plugin_name, plugins)
        if not plugin:
            logger.warning(f"插件不存在: {plugin_name}")
            return False, None

        # 从远程获取版本检查信息
        remote_info = self.version_manager.get_version_info(plugin_name)

        if not remote_info:
            logger.info(f"插件 {plugin_name} 未配置版本检查URL")
            return False, None

        try:
            remote_version = remote_info.version
            remote_url = remote_info.download_url

            if not remote_version or not remote_url:
                logger.warning(f"远程版本信息不完整: {plugin_name}")
                return False, None

            # 比较版本
            current_version = plugin.current_version
            version_comparison = self.version_manager._compare_versions(remote_version, current_version)

            if version_comparison > 0:
                # 有新版本
                version_info = remote_info
                logger.info(f"发现插件 {plugin_name} 新版本: {current_version} -> {remote_version}")
                return True, version_info
            else:
                logger.info(f"插件 {plugin_name} 已是最新版本: {current_version}")
                return False, None

        except Exception as e:
            logger.error(f"检查插件 {plugin_name} 更新失败: {str(e)}")
            return False, None

    def check_all_updates(self, plugins: List[PluginConfig], background: bool = False) -> Dict[str, VersionInfo]:
        """检查所有插件的更新"""
        updates = {}

        if not background:
            logger.info("开始检查所有插件更新...")

        for plugin in plugins:
            try:
                has_update, version_info = self.check_plugin_update(plugin.name, plugins)
                if has_update and version_info:
                    updates[plugin.name] = version_info
                    if not background:
                        logger.info(
                            f"🔔 插件 {plugin.name} 有新版本: {plugin.current_version} -> {version_info.version}")
            except Exception as e:
                logger.error(f"检查插件 {plugin.name} 更新时出错: {str(e)}")

        # 更新缓存
        self.version_manager.version_cache['last_update_check'] = datetime.now().isoformat()
        self.version_manager.version_cache['available_updates'] = {
            plugin_name: {
                'version': info.version,
                'release_date': info.release_date
            } for plugin_name, info in updates.items()
        }
        self.version_manager.save_version_cache()

        if not background:
            if updates:
                logger.info(f"发现 {len(updates)} 个插件有更新")
            else:
                logger.info("所有插件都是最新版本")

        return updates

    def update_plugin(
            self,
            plugin: PluginConfig,
            version_info: VersionInfo,
            progress_callback: Optional[NestedProgressCallback] = None
    ) -> bool:
        """更新指定插件（带连续子阶段进度）"""
        if not plugin:
            raise Exception(f"插件不存在: {plugin.name}")
        plugin_name = plugin.name
        logger.info(f"开始更新插件 {plugin_name}: {plugin.current_version} -> {version_info.version}")

        plugins = self.plugin_loader.load_all_plugins()

        # ----------  零改动：停运行、失败直接 return False ----------
        if self.runtime_manager.is_plugin_running(plugin):
            logger.info(f"停止运行中的插件: {plugin_name}")
            if not self.runtime_manager.stop_plugin(plugin):
                raise Exception("停止插件失败，无法更新")

        # ====================  仅这里新增进度划分  ====================
        # 总进度 0~100% 切成 6 段：下载→校验→解压→依赖→备份→移动/清理
        stages = SubProgress(progress_callback or NestedProgressCallback(lambda p, s: None, 0, 100),
                             0, 100, "整体更新", segments=6)
        # ============================================================

        temp_plugin_dir = self.plugin_install_dir / f"_temp"
        with self.archive_handler.temp_directory(temp_plugin_dir) as temp_dir:
            temp_archive = temp_dir / f"{plugin.name}_update.zip"

            # 1. 下载（0~16%）
            stages.update(0, "开始下载新版本")
            down_bridge = InstallDownloadBridge(
                stages.parent.create_sub_callback(0, 16, "下载")
            )
            version_file_name = f"{plugin_name}-{version_info.version}.zip"
            if not self.download_manager.download_with_progress(
                    version_info.download_url + "/" + version_file_name,
                    str(temp_archive), down_bridge):
                raise Exception(f"下载新版本失败: {plugin_name}")
            stages.next_segment()

            # 2. 校验（16~33%）
            if version_info.md5_hash:
                stages.update(0, "校验文件MD5")
                downloaded_md5 = self.download_manager.calculate_file_md5(temp_archive)
                if downloaded_md5 != version_info.md5_hash.lower():
                    raise Exception("文件校验失败: MD5不匹配")
            stages.next_segment()

            # 3. 解压（33~50%）
            stages.update(0, "解压新版本")
            extract_temp_dir = temp_dir / "extracted"
            if not self.archive_handler.extract_archive(temp_archive, extract_temp_dir):
                raise Exception(f"解压新版本失败: {plugin_name}")

            stages.next_segment()

            # 下载配置文件
            config_file_name = f"{plugin_name}-{version_info.version}.yaml"
            plugin_config_path = self.download_manager.download(self.config_manager.config_url + "/" + config_file_name,
                                                                str(extract_temp_dir / config_file_name))
            if not plugin_config_path:
                raise Exception(f"下载新版本配置失败: {plugin_name}")

            # 加载新版本插件配置
            new_plugin_config = self.plugin_loader.load_plugin_config_from_file(Path(plugin_config_path))
            if not new_plugin_config:
                raise Exception(f"加载新版本配置失败: {plugin_name}")

            # 4. 依赖处理（50~66%）
            stages.update(0, "处理依赖关系")
            dependency_install_success = True
            if self.dependency_manager:
                dependency_install_success = self._handle_dependencies_during_update(
                    plugin, new_plugin_config, plugins)
                if not dependency_install_success:
                    raise Exception(f"依赖处理失败，取消更新: {plugin_name}")
            stages.next_segment()

            # 5. 备份旧版本（66~83%）
            stages.update(0, "备份旧版本")
            plugin_dir = self.plugin_install_dir / plugin.extract_folder
            backup_success = False
            backup_dir = None
            if plugin_dir.exists():
                try:
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    backup_dir = self.plugin_install_dir / f"{plugin.extract_folder}_backup_{timestamp}"
                    shutil.copytree(plugin_dir, backup_dir)
                    backup_success = True
                    logger.info(f"已创建备份: {backup_dir}")
                except Exception as e:
                    logger.warning(f"备份失败: {str(e)}")
            stages.next_segment()

            # 6. 移动新版本 + 清理（83~100%）
            stages.update(0, "替换新版本")
            try:
                if plugin_dir.exists():
                    shutil.rmtree(plugin_dir)
                shutil.move(str(extract_temp_dir), str(plugin_dir))

                plugin.current_version = version_info.version
                plugin.dependencies = new_plugin_config.dependencies
                if not self.plugin_loader.save_plugin_config(plugin):
                    logger.warning(f"保存插件配置失败，但文件已更新: {plugin_name}")

                if self.dependency_manager:
                    self.dependency_manager.unregister_plugin_dependencies(plugin_name)
                    self.dependency_manager.register_plugin_dependencies(plugin)

                if backup_success and backup_dir and backup_dir.exists():
                    shutil.rmtree(backup_dir)

                stages.update(100, "更新完成")
                logger.info(f"插件 {plugin_name} 更新完成: {version_info.version}")
                return True

            except Exception as e:
                if backup_success and backup_dir and backup_dir.exists():
                    try:
                        if plugin_dir.exists():
                            shutil.rmtree(plugin_dir)
                        shutil.move(str(backup_dir), str(plugin_dir))
                        logger.info(f"已从备份恢复插件: {plugin_name}")
                    except Exception as restore_error:
                        logger.error(f"恢复备份失败: {str(restore_error)}")
                raise Exception(f"更新过程出错: {str(e)}")

    def rollback_plugin_version(
            self,
            plugin: PluginConfig,
            version_info: VersionInfo,
            progress_callback: Optional[NestedProgressCallback] = None
    ) -> bool:
        """
        将插件回滚到指定的历史版本（通过下载对应版本的安装包实现）。

        :param plugin: 要回滚的插件配置对象。
        :param version_info: 目标回滚版本的版本信息，必须包含 `version` 和 `download_url`。
        :param progress_callback: 用于报告进度的回调函数。
        :return: 如果回滚成功则返回 True，否则返回 False。
        """
        if not plugin or not version_info:
            raise Exception("插件配置对象或版本信息不能为空。")

        if not version_info.version or not version_info.download_url:
            raise Exception("VersionInfo 必须包含 'version' 和 'download_url'。")

        plugin_name = plugin.name
        target_version = version_info.version
        logger.info(f"开始将插件 {plugin_name} 回滚到版本: {target_version}")

        # ----------  零改动：停运行、失败直接 return False ----------
        if self.runtime_manager.is_plugin_running(plugin):
            logger.info(f"停止运行中的插件: {plugin_name}")
            if not self.runtime_manager.stop_plugin(plugin):
                raise Exception("停止插件失败，无法回滚。")

        # ====================  仅这里新增进度划分  ====================
        # 总进度 0~100% 切成 5 段：下载→校验→解压→备份→移动/清理
        stages = SubProgress(progress_callback or NestedProgressCallback(lambda p, s: None, 0, 100),
                             0, 100, "版本回滚", segments=5)
        # ============================================================
        temp_plugin_dir = self.plugin_install_dir / f"_temp"
        with self.archive_handler.temp_directory(temp_plugin_dir) as temp_dir:
            temp_archive = temp_dir / f"{plugin.name}_rollback.zip"

            # 1. 下载目标版本（0~20%）
            stages.update(0, "开始下载目标版本")
            down_bridge = InstallDownloadBridge(
                stages.parent.create_sub_callback(0, 20, "下载")
            )
            # 假设下载URL已经是完整的，或者需要像更新一样拼接
            download_url = version_info.download_url
            if not self.download_manager.download_with_progress(
                    download_url + f"/{plugin_name}-{target_version}.zip",
                    str(temp_archive), down_bridge):
                raise Exception(f"下载目标版本失败: {plugin_name}")
            stages.next_segment()

            # 2. 校验（20~40%）
            if version_info.md5_hash:
                stages.update(0, "校验文件MD5")
                downloaded_md5 = self.download_manager.calculate_file_md5(temp_archive)
                if downloaded_md5 != version_info.md5_hash.lower():
                    raise Exception("文件校验失败: MD5不匹配")
            stages.next_segment()

            # 3. 解压（40~60%）
            stages.update(0, "解压目标版本")
            extract_temp_dir = temp_dir / "extracted"
            if not self.archive_handler.extract_archive(temp_archive, extract_temp_dir):
                raise Exception(f"解压目标版本失败: {plugin_name}")
            stages.next_segment()

            # 4. 备份当前版本（60~80%）
            stages.update(0, "备份当前版本")
            plugin_dir = self.plugin_install_dir / plugin.extract_folder
            backup_success = False
            backup_dir = None
            if plugin_dir.exists():
                try:
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    backup_dir = self.plugin_install_dir / f"{plugin.extract_folder}_pre_rollback_{timestamp}"
                    shutil.copytree(plugin_dir, backup_dir)
                    backup_success = True
                    logger.info(f"已创建回滚前备份: {backup_dir}")
                except Exception as e:
                    logger.warning(f"备份当前版本失败: {str(e)}。回滚仍将继续，但如果出现问题将无法恢复。")
            stages.next_segment()

            # 5. 移动新版本 + 清理（80~100%）
            stages.update(0, "替换为目标版本")
            try:
                if plugin_dir.exists():
                    shutil.rmtree(plugin_dir)
                shutil.move(str(extract_temp_dir), str(plugin_dir))

                # 更新插件配置中的版本号
                plugin.current_version = target_version
                # 注意：这里我们没有处理 dependencies 的回滚，如果需要，逻辑会更复杂
                # plugin.dependencies = ...
                if not self.plugin_loader.save_plugin_config(plugin):
                    logger.warning(f"保存插件配置失败，但文件已更新: {plugin_name}")

                # 清理备份（如果需要）
                # if backup_success and backup_dir and backup_dir.exists():
                #     shutil.rmtree(backup_dir)

                stages.update(100, "回滚完成")
                logger.info(f"插件 {plugin_name} 回滚到版本 {target_version} 成功。")
                return True

            except Exception as e:
                # 如果有备份，尝试恢复
                if backup_success and backup_dir and backup_dir.exists():
                    try:
                        if plugin_dir.exists():
                            shutil.rmtree(plugin_dir)
                        shutil.move(str(backup_dir), str(plugin_dir))
                        logger.info(f"已从备份恢复插件到回滚前的状态: {plugin_name}")
                    except Exception as restore_error:
                        raise Exception(f"恢复备份失败: {str(restore_error)}")
                raise Exception(f"回滚过程出错: {str(e)}")

    def auto_update_plugins(self, plugins: List[PluginConfig]) -> Dict[str, bool]:
        """自动更新所有有更新的插件"""
        updates = self.check_all_updates(plugins, background=True)
        results = {}

        for plugin_name, version_info in updates.items():
            try:
                plugin = self._get_plugin_info(plugin_name, plugins)
                version_check_info = self.version_manager.get_version_check_info(plugin_name)
                auto_update = version_check_info.get('auto_update', False)

                if plugin and auto_update:
                    logger.info(f"自动更新插件: {plugin_name}")
                    success = False
                    try:
                        success = self.update_plugin(plugin, version_info)
                    except Exception as e:
                        logger.error(e, exc_info=True)
                    results[plugin_name] = success
                else:
                    logger.info(f"插件 {plugin_name} 有更新但未启用自动更新")
                    results[plugin_name] = False
            except Exception as e:
                logger.error(f"自动更新插件 {plugin_name} 失败: {str(e)}")
                results[plugin_name] = False

        return results

    def _get_plugin_info(self, plugin_name: str, plugins: List[PluginConfig]) -> Optional[PluginConfig]:
        """获取插件信息"""
        if plugins is None:
            return None
        return next((p for p in plugins if p.name == plugin_name), None)

    def _handle_dependencies_during_update(
            self,
            old_plugin: PluginConfig,
            new_plugin: PluginConfig,
            plugins: List[PluginConfig]
    ) -> bool:
        """处理插件更新过程中的依赖关系"""
        logger.info(f"检查插件 {old_plugin.name} 的依赖关系变化")

        # 获取已安装插件的版本信息
        installed_plugins = {p.name: p.current_version for p in plugins}

        # 比较新旧版本的依赖
        old_dependencies = old_plugin.dependencies or {}
        new_dependencies = new_plugin.dependencies or {}

        # 找出新增的依赖
        new_dependency_names = set(new_dependencies.keys()) - set(old_dependencies.keys())

        # 找出版本变更的依赖
        changed_dependencies = []
        for dep_name in set(old_dependencies.keys()) & set(new_dependencies.keys()):
            if old_dependencies[dep_name] != new_dependencies[dep_name]:
                changed_dependencies.append(dep_name)

        logger.info(f"依赖变化分析 - 新增: {list(new_dependency_names)}, 变更: {changed_dependencies}")

        # 如果没有依赖变化，直接返回成功
        if not new_dependency_names and not changed_dependencies:
            logger.info("没有依赖关系变化")
            return True

        # 处理新增的依赖
        for dep_name in new_dependency_names:
            logger.info(f"处理新增依赖: {dep_name}")

            # 检查依赖是否已安装
            if dep_name in installed_plugins:
                # 检查已安装版本是否满足新要求
                if not self.dependency_manager.validate_plugin_dependencies(dep_name, installed_plugins):
                    logger.warning(f"依赖 {dep_name} 已安装但版本不满足新要求")
                    # 这里不能阻止，因为一个插件只能安装一个版本,只能提示出来
                else:
                    logger.info(f"依赖 {dep_name} 已安装且版本满足要求")
            else:
                # 依赖未安装，尝试自动安装
                if self.install_manager:
                    logger.info(f"开始自动安装新增依赖: {dep_name}")
                    try:
                        # 使用安装管理器安装依赖
                        install_success = self.install_manager.install_plugin(
                            dep_name,
                            progress_callback=None,
                            plugins=plugins,
                            lock=None,  # 在更新过程中，我们可能不需要锁
                            auto_install_dependencies=True
                        )
                        if install_success:
                            logger.info(f"成功安装新增依赖: {dep_name}")
                            # 更新已安装插件列表
                            installed_plugins[dep_name] = "unknown"  # 版本将在后续验证中检查
                        else:
                            logger.error(f"自动安装新增依赖 {dep_name} 失败")
                            return False
                    except Exception as e:
                        logger.error(f"安装新增依赖 {dep_name} 时出错: {str(e)}")
                        return False
                else:
                    logger.error(f"无法自动安装新增依赖 {dep_name}，安装管理器不可用")
                    return False

        # 处理版本变更的依赖
        for dep_name in changed_dependencies:
            logger.info(f"检查依赖版本变更: {dep_name} ({old_dependencies[dep_name]} -> {new_dependencies[dep_name]})")

            if dep_name in installed_plugins:
                # 检查已安装版本是否满足新要求
                if not self.dependency_manager.validate_plugin_dependencies(dep_name, installed_plugins):
                    logger.error(f"依赖 {dep_name} 版本不满足新要求")
                    return False
                else:
                    logger.info(f"依赖 {dep_name} 版本满足新要求")
            else:
                logger.error(f"依赖 {dep_name} 未安装但新版本要求该依赖")
                return False

        # 最终验证所有依赖关系
        logger.info("进行最终依赖关系验证")
        if not self.dependency_manager.validate_plugin_dependencies(new_plugin.name, installed_plugins):
            logger.error("最终依赖关系验证失败")
            return False

        logger.info("依赖关系检查通过")
        return True
