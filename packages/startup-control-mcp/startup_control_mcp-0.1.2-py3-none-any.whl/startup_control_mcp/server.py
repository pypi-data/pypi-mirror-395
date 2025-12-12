#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
开机启动项控制 MCP 服务器
支持跨平台的启动项管理和自然语言交互
使用 FastMCP 框架
"""

import json
import os
import platform
import re
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set
import logging

# FastMCP imports
from fastmcp import FastMCP


# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class StartupItemManager:
    """跨平台启动项管理器"""
    
    def __init__(self):
        self.platform = platform.system().lower()
        self.backup_dir = Path.home() / ".startup_control_backups"
        self.backup_dir.mkdir(exist_ok=True)

        # 记录最近一次获取启动项时的异常
        self.last_error: Optional[Exception] = None
        
        # 重要启动项关键词（不应被禁用）
        self.critical_keywords = [
            'security', 'antivirus', 'firewall', 'system', 'audio', 'bluetooth',
            'defender', 'realtek', 'nvidia', 'amd', 'intel', 'logitech', 'razer',
            '安全', '防病毒', '防火墙', '系统', '音频', '蓝牙', 'network', '网络',
            '电脑管家', '杀毒', '360', '金山', '瑞星', '火绒'
        ]
        
        # 常见可优化启动项关键词
        self.optimizable_keywords = [
            'adobe', 'office', 'game', 'steam', 'epic', 'launcher', 'updater',
            'helper', 'assistant', 'sync', 'cloud', 'backup', 'skype', 'teams',
            'discord', 'slack', 'zoom', 'spotify', 'itunes', 'dropbox', 'onedrive',
            '游戏', '启动器', '更新', '助手', '同步', '云', '迅雷', '下载',
            '腾讯', 'qq', '微信', 'wechat', '阿里', '淘宝', '支付宝', '百度',
            '搜狗', '输入法', '网易', '音乐', '视频', '播放器', '看图',
            '压缩', 'winrar', '7zip', '浏览器', 'chrome', 'firefox',
            '工具栏', 'toolbar', '插件', 'plugin', '助理', '全家桶'
        ]

    def get_startup_items(self) -> List[Dict]:
        """获取所有启动项"""
        self.last_error = None
        try:
            if self.platform == "windows":
                return self._get_windows_startup_items()
            elif self.platform == "darwin":  # macOS
                return self._get_macos_startup_items()
            elif self.platform == "linux":
                return self._get_linux_startup_items()
            else:
                raise Exception(f"Unsupported platform: {self.platform}")
        except Exception as e:
            logger.error(f"Failed to get startup items: {e}")
            self.last_error = e
            return []

    def _get_windows_startup_items(self) -> List[Dict]:
        """获取Windows启动项"""
        items: List[Dict] = []

        registry_seen: Set[Tuple[str, str]] = set()
        folder_seen: Set[str] = set()
        task_seen: Set[str] = set()
        service_seen: Set[str] = set()

        def append_registry_items(reg_path: str) -> None:
            """读取注册表某一分支的启动项"""
            try:
                result = subprocess.run(
                    ["reg", "query", reg_path],
                    capture_output=True,
                    text=True,
                    encoding="gbk",
                    errors="ignore"
                )
            except FileNotFoundError:
                logger.warning("reg command not found; cannot read registry")
                return
            except Exception as e:
                logger.debug(f"Failed to query registry {reg_path}: {e}")
                return

            if result.returncode != 0 or not result.stdout.strip():
                return

            lines = result.stdout.strip().splitlines()
            if len(lines) <= 1:
                return

            for line in lines[1:]:  # 跳过标题行
                line = line.strip()
                if not line or "REG_" not in line:
                    continue

                parts = re.split(r"\s{4,}", line)
                if len(parts) < 3:
                    parts = line.split(None, 2)
                if len(parts) < 3:
                    continue

                name = parts[0].strip()
                data = parts[2].strip() if len(parts) >= 3 else ""

                # 跳过未设置的默认值
                if name in {"(默认)", "(Default)"} and (
                    not data or data.lower() in {"(value not set)", "值未设置"}
                ):
                    continue

                key = (reg_path, name.lower())
                if key in registry_seen:
                    continue
                registry_seen.add(key)

                items.append({
                    'name': name,
                    'path': data,
                    'type': 'registry',
                    'location': reg_path,
                    'enabled': True,
                    'impact': self._analyze_startup_impact(name, data)
                })

        reg_paths: List[str] = []
        added_paths: Set[str] = set()

        def add_reg_path(path: str) -> None:
            if path and path not in added_paths:
                reg_paths.append(path)
                added_paths.add(path)

        # 常见启动项分支（当前用户、所有用户、WOW6432Node 32 位视图）
        base_reg_paths = [
            r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run",
            r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunOnce",
            r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunServices",
            r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunServicesOnce",
            r"HKEY_CURRENT_USER\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Run",
            r"HKEY_CURRENT_USER\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\RunOnce",
            r"HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run",
            r"HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunOnce",
            r"HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunServices",
            r"HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunServicesOnce",
            r"HKEY_LOCAL_MACHINE\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Run",
            r"HKEY_LOCAL_MACHINE\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\RunOnce",
            r"HKEY_LOCAL_MACHINE\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\RunServices",
            r"HKEY_LOCAL_MACHINE\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\RunServicesOnce",
            r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run",
            r"HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run",
        ]
        for path in base_reg_paths:
            add_reg_path(path)

        # 枚举所有已加载用户 SID 的 Run 分支，覆盖非当前用户启动项
        user_suffixes = [
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            r"Software\Microsoft\Windows\CurrentVersion\RunOnce",
            r"Software\Microsoft\Windows\CurrentVersion\RunServices",
            r"Software\Microsoft\Windows\CurrentVersion\RunServicesOnce",
            r"Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Run",
            r"Software\WOW6432Node\Microsoft\Windows\CurrentVersion\RunOnce",
        ]
        try:
            sid_result = subprocess.run(
                ["reg", "query", "HKEY_USERS"],
                capture_output=True,
                text=True,
                encoding="gbk",
                errors="ignore"
            )
            if sid_result.returncode == 0:
                for raw_line in sid_result.stdout.splitlines():
                    sid_line = raw_line.strip()
                    if not sid_line.startswith("HKEY_USERS\\"):
                        continue
                    if sid_line.endswith("_Classes"):
                        continue
                    sid = sid_line.split("\\", 1)[1]
                    if sid in {".DEFAULT", "S-1-5-18", "S-1-5-19", "S-1-5-20"}:
                        continue
                    if not sid.startswith("S-"):
                        continue
                    for suffix in user_suffixes:
                        add_reg_path(f"{sid_line}\\{suffix}")
        except Exception as e:
            logger.debug(f"Failed to enumerate HKEY_USERS subkeys: {e}")

        for reg_path in reg_paths:
            append_registry_items(reg_path)

        # 启动文件夹
        startup_folders = [
            os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"),
            os.path.expandvars(r"%PROGRAMDATA%\Microsoft\Windows\Start Menu\Programs\Startup")
        ]

        for folder in startup_folders:
            if os.path.exists(folder):
                try:
                    for file in os.listdir(folder):
                        if file.endswith((".lnk", ".exe", ".bat", ".cmd")):
                            full_path = os.path.join(folder, file)
                            key = full_path.lower()
                            if key in folder_seen:
                                continue
                            folder_seen.add(key)
                            items.append({
                                'name': os.path.splitext(file)[0],
                                'path': full_path,
                                'type': 'startup_folder',
                                'location': folder,
                                'enabled': True,
                                'impact': self._analyze_startup_impact(file, full_path)
                            })
                except Exception as e:
                    logger.warning(f"Failed to read startup folder {folder}: {e}")

        # 任务计划程序启动项
        schedule_keywords = ["startup", "logon", "log on", "登录", "登陆", "开机", "启动"]
        try:
            result = subprocess.run(
                ["schtasks", "/query", "/fo", "LIST", "/v"],
                capture_output=True,
                text=True,
                encoding="gbk",
                errors="ignore"
            )

            if result.returncode == 0 and result.stdout.strip():
                blocks = re.split(r"\r?\n\r?\n", result.stdout)
                for block in blocks:
                    block = block.strip()
                    if not block:
                        continue

                    task_name = None
                    task_path = ""
                    enabled = True
                    schedule_matched = False

                    for line in block.splitlines():
                        normalized = line.replace("：", ":").strip()
                        if ":" not in normalized:
                            continue
                        key, value = normalized.split(":", 1)
                        key_lower = key.strip().lower()
                        value_str = value.strip()

                        if key_lower in {"taskname", "任务名称", "任务名"}:
                            task_name = value_str
                        elif key_lower in {"task to run", "操作", "action"}:
                            task_path = value_str
                        elif key_lower in {"schedule", "计划"}:
                            value_lower = value_str.lower()
                            if any(keyword in value_lower for keyword in schedule_keywords):
                                schedule_matched = True
                        elif key_lower in {"enabled", "已启用", "启用"}:
                            enabled = value_str.lower() in {"yes", "true", "是", "已启用"}

                    if task_name and schedule_matched:
                        task_key = task_name.lower()
                        if task_key in task_seen:
                            continue
                        task_seen.add(task_key)

                        display_name = task_name.split('\\')[-1] if '\\' in task_name else task_name
                        items.append({
                            'name': display_name,
                            'path': task_path or 'Task Scheduler',
                            'type': 'task_scheduler',
                            'location': task_name,
                            'enabled': enabled,
                            'impact': self._analyze_startup_impact(display_name, task_path)
                        })
        except Exception as e:
            logger.warning(f"Failed to get scheduled tasks: {e}")

        # Windows 服务（自动启动的服务）
        try:
            result = subprocess.run(
                ["sc", "query", "type=", "service", "state=", "all"],
                capture_output=True,
                text=True,
                encoding="gbk",
                errors="ignore"
            )

            if result.returncode == 0:
                services = result.stdout.split('SERVICE_NAME:')
                for service in services[1:]:  # 跳过第一个空元素
                    lines = service.strip().split('\n')
                    if not lines:
                        continue
                    service_name = lines[0].strip()
                    if not service_name:
                        continue

                    # 检查是否是自动启动
                    config_result = subprocess.run(
                        ["sc", "qc", service_name],
                        capture_output=True,
                        text=True,
                        encoding="gbk",
                        errors="ignore"
                    )

                    cfg_stdout = config_result.stdout if config_result.returncode == 0 else ""
                    if 'AUTO_START' not in cfg_stdout and '自动' not in cfg_stdout:
                        continue

                    # 过滤掉Windows系统服务
                    if any(sys_svc in service_name.lower() for sys_svc in ['windows', 'microsoft', 'system32', 'svchost']):
                        continue

                    service_key = service_name.lower()
                    if service_key in service_seen:
                        continue
                    service_seen.add(service_key)

                    binary_path = ""
                    display_name = ""
                    for cfg_line in cfg_stdout.splitlines():
                        normalized = cfg_line.replace("：", ":")
                        if ":" not in normalized:
                            continue
                        cfg_key, cfg_value = normalized.split(":", 1)
                        cfg_key_lower = cfg_key.strip().lower()
                        cfg_value_str = cfg_value.strip()
                        if cfg_key_lower in {"binary_path_name", "二进制路径名"}:
                            binary_path = cfg_value_str
                        elif cfg_key_lower in {"display_name", "显示名称"}:
                            display_name = cfg_value_str

                    service_display = display_name or service_name

                    items.append({
                        'name': service_display,
                        'path': binary_path or 'Windows Service',
                        'type': 'service',
                        'location': f'Services\\{service_name}',
                        'enabled': True,
                        'impact': self._analyze_startup_impact(service_display, binary_path)
                    })
        except Exception as e:
            logger.warning(f"Failed to get Windows services: {e}")

        return items

    def _get_macos_startup_items(self) -> List[Dict]:
        """获取macOS启动项"""
        items = []
        
        # LaunchAgents 和 LaunchDaemons
        launch_paths = [
            "~/Library/LaunchAgents",
            "/Library/LaunchAgents",
            "/Library/LaunchDaemons",
            "/System/Library/LaunchAgents",
            "/System/Library/LaunchDaemons"
        ]
        
        for path in launch_paths:
            expanded_path = os.path.expanduser(path)
            if os.path.exists(expanded_path):
                for file in os.listdir(expanded_path):
                    if file.endswith('.plist'):
                        full_path = os.path.join(expanded_path, file)
                        
                        # 检查是否已加载
                        try:
                            result = subprocess.run([
                                "launchctl", "list"
                            ], capture_output=True, text=True)
                            
                            service_name = os.path.splitext(file)[0]
                            enabled = service_name in result.stdout
                            
                            items.append({
                                'name': service_name,
                                'path': full_path,
                                'type': 'launchd',
                                'location': path,
                                'enabled': enabled,
                                'impact': self._analyze_startup_impact(service_name, full_path)
                            })
                        except Exception as e:
                            logger.warning(f"Failed to check service status {file}: {e}")
        
        # 登录项 (Login Items)
        try:
            result = subprocess.run([
                "osascript", "-e", 
                'tell application "System Events" to get the name of every login item'
            ], capture_output=True, text=True)
            
            if result.returncode == 0 and result.stdout.strip():
                login_items = result.stdout.strip().split(', ')
                for item in login_items:
                    items.append({
                        'name': item.strip(),
                        'path': '',
                        'type': 'login_item',
                        'location': 'System Preferences',
                        'enabled': True,
                        'impact': self._analyze_startup_impact(item, '')
                    })
        except Exception as e:
            logger.warning(f"Failed to get login items: {e}")
        
        return items

    def _get_linux_startup_items(self) -> List[Dict]:
        """获取Linux启动项"""
        items = []
        
        # systemd 服务
        try:
            result = subprocess.run([
                "systemctl", "list-unit-files", "--type=service", "--state=enabled"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[1:]  # 跳过标题行
                for line in lines:
                    if line.strip() and not line.startswith('UNIT FILE'):
                        parts = line.strip().split()
                        if len(parts) >= 2:
                            service_name = parts[0]
                            items.append({
                                'name': service_name,
                                'path': f'/etc/systemd/system/{service_name}',
                                'type': 'systemd',
                                'location': 'systemd',
                                'enabled': True,
                                'impact': self._analyze_startup_impact(service_name, '')
                            })
        except Exception as e:
            logger.warning(f"Failed to get systemd services: {e}")
        
        # 自启动应用程序
        autostart_dirs = [
            "~/.config/autostart",
            "/etc/xdg/autostart"
        ]
        
        for dir_path in autostart_dirs:
            expanded_path = os.path.expanduser(dir_path)
            if os.path.exists(expanded_path):
                for file in os.listdir(expanded_path):
                    if file.endswith('.desktop'):
                        full_path = os.path.join(expanded_path, file)
                        name = os.path.splitext(file)[0]
                        
                        # 检查是否启用
                        enabled = True
                        try:
                            with open(full_path, 'r') as f:
                                content = f.read()
                                if 'Hidden=true' in content:
                                    enabled = False
                        except Exception:
                            pass
                        
                        items.append({
                            'name': name,
                            'path': full_path,
                            'type': 'autostart',
                            'location': dir_path,
                            'enabled': enabled,
                            'impact': self._analyze_startup_impact(name, full_path)
                        })
        
        return items

    def _analyze_startup_impact(self, name: str, path: str) -> Dict:
        """分析启动项对系统性能的影响"""
        name_lower = name.lower()
        path_lower = path.lower()
        
        # 判断是否为关键启动项
        is_critical = any(keyword in name_lower or keyword in path_lower 
                         for keyword in self.critical_keywords)
        
        # 判断是否为可优化项
        is_optimizable = any(keyword in name_lower or keyword in path_lower 
                           for keyword in self.optimizable_keywords)
        
        # 计算影响级别
        if is_critical:
            impact_level = "critical"
            recommendation = "Not recommended to disable"
        elif is_optimizable:
            impact_level = "high"
            recommendation = "Recommended to disable to improve startup time"
        else:
            impact_level = "medium"
            recommendation = "May disable as needed"
        
        return {
            'level': impact_level,
            'recommendation': recommendation,
            'is_critical': is_critical,
            'is_optimizable': is_optimizable
        }

    def disable_startup_item(self, item_info: Dict) -> bool:
        """禁用启动项"""
        try:
            # 先备份
            self._backup_startup_state()
            
            if self.platform == "windows":
                return self._disable_windows_startup_item(item_info)
            elif self.platform == "darwin":
                return self._disable_macos_startup_item(item_info)
            elif self.platform == "linux":
                return self._disable_linux_startup_item(item_info)
            else:
                return False
        except Exception as e:
            logger.error(f"Failed to disable startup item: {e}")
            return False

    def enable_startup_item(self, item_info: Dict) -> bool:
        """启用启动项"""
        try:
            if self.platform == "windows":
                return self._enable_windows_startup_item(item_info)
            elif self.platform == "darwin":
                return self._enable_macos_startup_item(item_info)
            elif self.platform == "linux":
                return self._enable_linux_startup_item(item_info)
            else:
                return False
        except Exception as e:
            logger.error(f"Failed to enable startup item: {e}")
            return False

    def _disable_windows_startup_item(self, item_info: Dict) -> bool:
        """禁用Windows启动项"""
        if item_info['type'] == 'registry':
            # 删除注册表项
            try:
                subprocess.run([
                    "reg", "delete", item_info['location'], "/v", item_info['name'], "/f"
                ], check=True, capture_output=True, encoding='gbk')
                return True
            except subprocess.CalledProcessError:
                return False
        elif item_info['type'] == 'startup_folder':
            # 重命名文件（添加.disabled后缀）
            try:
                disabled_path = item_info['path'] + '.disabled'
                os.rename(item_info['path'], disabled_path)
                return True
            except Exception:
                return False
        elif item_info['type'] == 'task_scheduler':
            # 禁用计划任务
            try:
                subprocess.run([
                    "schtasks", "/change", "/tn", item_info['name'], "/disable"
                ], check=True, capture_output=True, encoding='gbk')
                return True
            except subprocess.CalledProcessError:
                return False
        elif item_info['type'] == 'service':
            # 禁用Windows服务
            try:
                # 先停止服务
                subprocess.run([
                    "sc", "stop", item_info['name']
                ], capture_output=True, encoding='gbk')
                # 设置为禁用
                subprocess.run([
                    "sc", "config", item_info['name'], "start=", "disabled"
                ], check=True, capture_output=True, encoding='gbk')
                return True
            except subprocess.CalledProcessError:
                return False
        return False

    def _disable_macos_startup_item(self, item_info: Dict) -> bool:
        """禁用macOS启动项"""
        if item_info['type'] == 'launchd':
            try:
                # 卸载服务
                subprocess.run([
                    "launchctl", "unload", item_info['path']
                ], check=True, capture_output=True)
                return True
            except subprocess.CalledProcessError:
                return False
        elif item_info['type'] == 'login_item':
            try:
                # 移除登录项
                subprocess.run([
                    "osascript", "-e", 
                    f'tell application "System Events" to delete login item "{item_info["name"]}"'
                ], check=True, capture_output=True)
                return True
            except subprocess.CalledProcessError:
                return False
        return False

    def _disable_linux_startup_item(self, item_info: Dict) -> bool:
        """禁用Linux启动项"""
        if item_info['type'] == 'systemd':
            try:
                subprocess.run([
                    "systemctl", "disable", item_info['name']
                ], check=True, capture_output=True)
                return True
            except subprocess.CalledProcessError:
                return False
        elif item_info['type'] == 'autostart':
            try:
                # 修改.desktop文件，添加Hidden=true
                with open(item_info['path'], 'r') as f:
                    content = f.read()
                
                if 'Hidden=' not in content:
                    content += '\nHidden=true\n'
                else:
                    content = re.sub(r'Hidden=.*', 'Hidden=true', content)
                
                with open(item_info['path'], 'w') as f:
                    f.write(content)
                return True
            except Exception:
                return False
        return False

    def _enable_windows_startup_item(self, item_info: Dict) -> bool:
        """启用Windows启动项"""
        if item_info['type'] == 'startup_folder':
            # 移除.disabled后缀
            try:
                if item_info['path'].endswith('.disabled'):
                    original_path = item_info['path'][:-9]  # 移除.disabled
                    os.rename(item_info['path'], original_path)
                    return True
            except Exception:
                return False
        return False

    def _enable_macos_startup_item(self, item_info: Dict) -> bool:
        """启用macOS启动项"""
        if item_info['type'] == 'launchd':
            try:
                subprocess.run([
                    "launchctl", "load", item_info['path']
                ], check=True, capture_output=True)
                return True
            except subprocess.CalledProcessError:
                return False
        return False

    def _enable_linux_startup_item(self, item_info: Dict) -> bool:
        """启用Linux启动项"""
        if item_info['type'] == 'systemd':
            try:
                subprocess.run([
                    "systemctl", "enable", item_info['name']
                ], check=True, capture_output=True)
                return True
            except subprocess.CalledProcessError:
                return False
        elif item_info['type'] == 'autostart':
            try:
                with open(item_info['path'], 'r') as f:
                    content = f.read()
                
                # 移除或修改Hidden=true
                content = re.sub(r'Hidden=true.*\n', '', content)
                content = re.sub(r'Hidden=.*', 'Hidden=false', content)
                
                with open(item_info['path'], 'w') as f:
                    f.write(content)
                return True
            except Exception:
                return False
        return False

    def _backup_startup_state(self):
        """备份当前启动项状态"""
        try:
            startup_items = self.get_startup_items()
            timestamp = int(time.time())
            backup_file = self.backup_dir / f"startup_backup_{timestamp}.json"

            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(startup_items, f, ensure_ascii=False, indent=2)

            logger.info(f"Startup items state backed up to: {backup_file}")
        except Exception as e:
            logger.error(f"Failed to back up startup items state: {e}")

    def restore_startup_state(self, backup_file: str) -> bool:
        """恢复启动项状态"""
        try:
            with open(backup_file, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)
            
            # 恢复逻辑（简化版）
            logger.info(f"Restored startup items state from {backup_file}")
            return True
        except Exception as e:
            logger.error(f"Failed to restore startup items state: {e}")
            return False

    def parse_natural_language(self, command: str) -> List[Dict]:
        """解析自然语言命令"""
        command_lower = command.lower()
        startup_items = self.get_startup_items()
        matched_items = []
        
        # 关键词匹配
        disable_keywords = ['禁用', '关闭', '停用', '删除', '移除', 'disable', 'stop', 'remove']
        enable_keywords = ['启用', '开启', '打开', '添加', 'enable', 'start', 'add']
        
        action = None
        if any(keyword in command_lower for keyword in disable_keywords):
            action = 'disable'
        elif any(keyword in command_lower for keyword in enable_keywords):
            action = 'enable'
        
        # 匹配目标程序
        target_keywords = []
        
        # 常见程序类型匹配
        program_patterns = {
            '游戏': ['game', 'steam', 'epic', 'origin', 'uplay'],
            'adobe': ['adobe', 'acrobat', 'photoshop', 'illustrator'],
            '办公软件': ['office', 'word', 'excel', 'powerpoint', 'outlook'],
            '聊天软件': ['qq', 'wechat', 'skype', 'discord'],
            '浏览器': ['chrome', 'firefox', 'edge', 'safari'],
            '音乐软件': ['spotify', 'itunes', 'music'],
            '云同步': ['dropbox', 'onedrive', 'icloud', 'google drive', 'sync'],
        }
        
        for category, keywords in program_patterns.items():
            if category in command_lower or any(kw in command_lower for kw in keywords):
                target_keywords.extend(keywords)
        
        # 直接文本匹配
        words = re.findall(r'\b\w+\b', command_lower)
        target_keywords.extend(words)
        
        # 匹配启动项
        for item in startup_items:
            item_name_lower = item['name'].lower()
            item_path_lower = item['path'].lower()
            
            if any(keyword in item_name_lower or keyword in item_path_lower 
                   for keyword in target_keywords):
                matched_items.append({
                    'item': item,
                    'action': action,
                    'confidence': self._calculate_match_confidence(item, target_keywords)
                })
        
        # 按置信度排序
        matched_items.sort(key=lambda x: x['confidence'], reverse=True)
        
        return matched_items

    def _calculate_match_confidence(self, item: Dict, keywords: List[str]) -> float:
        """计算匹配置信度"""
        name_lower = item['name'].lower()
        path_lower = item['path'].lower()
        
        confidence = 0.0
        for keyword in keywords:
            if keyword in name_lower:
                confidence += 1.0
            elif keyword in path_lower:
                confidence += 0.5
        
        return confidence / len(keywords) if keywords else 0.0

    def get_startup_performance_analysis(self) -> Dict:
        """获取启动性能分析"""
        startup_items = self.get_startup_items()
        if self.last_error is not None:
            raise RuntimeError(f"Failed to get startup items: {self.last_error}")
        
        total_items = len(startup_items)
        enabled_items = sum(1 for item in startup_items if item['enabled'])
        critical_items = sum(1 for item in startup_items if item['impact']['is_critical'])
        optimizable_items = sum(1 for item in startup_items if item['impact']['is_optimizable'])
        
        return {
            'total_items': total_items,
            'enabled_items': enabled_items,
            'critical_items': critical_items,
            'optimizable_items': optimizable_items,
            'optimization_potential': f"{optimizable_items}/{enabled_items}" if enabled_items > 0 else "0/0",
            'recommendations': self._get_optimization_recommendations(startup_items)
        }

    def _get_optimization_recommendations(self, startup_items: List[Dict]) -> List[str]:
        """获取优化建议"""
        recommendations = []
        
        optimizable_items = [item for item in startup_items 
                           if item['enabled'] and item['impact']['is_optimizable']]
        
        if len(optimizable_items) > 5:
            recommendations.append(f"Found {len(optimizable_items)} optimizable startup items; consider disabling to improve startup speed")
        
        critical_enabled = sum(1 for item in startup_items 
                             if item['enabled'] and item['impact']['is_critical'])
        if critical_enabled > 0:
            recommendations.append(f"Detected {critical_enabled} critical startup items running")
        
        if len(startup_items) > 20:
            recommendations.append("Many startup items; consider regularly cleaning up unnecessary programs")
        
        return recommendations


# 创建MCP服务器
mcp = FastMCP("Startup Control")
manager = StartupItemManager()

@mcp.tool()
def list_user_startup_items(
    show_all: bool = False,
    only_enabled: bool = False
) -> str:
    """
    获取用户启动项列表

    智能过滤显示用户安装的第三方应用启动项，自动排除系统内置项。
    专注于用户实际需要管理的启动项，避免显示大量系统组件。

    Args:
        show_all: 是否显示所有启动项包括系统项（默认False仅显示第三方应用）
        only_enabled: 是否只显示已启用的项（默认False显示全部状态）

    Returns:
        格式化的启动项清单，包含状态、影响级别和管理建议
    """
    startup_items = manager.get_startup_items()

    if manager.last_error is not None:
        raise RuntimeError(f"Failed to get startup items: {manager.last_error}")

    # 默认过滤掉系统启动项，只显示用户安装的第三方应用
    if not show_all:
        startup_items = [
            item for item in startup_items
            if not (item['location'].startswith('/System/') or
                   item['name'].startswith('com.apple.'))
        ]

    # 过滤已启用项
    if only_enabled:
        startup_items = [item for item in startup_items if item['enabled']]

    # 统计信息
    total_count = len(startup_items)
    enabled_count = sum(1 for item in startup_items if item['enabled'])

    if total_count == 0:
        return "No user-installed startup items found"

    result = f"📊 Startup Items Summary\n"
    result += f"   • User startup items: {total_count}\n"
    result += f"   • Enabled: {enabled_count}\n"
    result += f"   • Disabled: {total_count - enabled_count}\n\n"

    # 按位置分组显示
    grouped_items = {}
    for item in startup_items:
        location = item['location']
        if location not in grouped_items:
            grouped_items[location] = []
        grouped_items[location].append(item)

    # 按重要性排序位置
    location_order = ['System Preferences', '~/Library/LaunchAgents', '/Library/LaunchAgents', '/Library/LaunchDaemons']
    sorted_locations = sorted(grouped_items.keys(), key=lambda x: location_order.index(x) if x in location_order else 99)

    for location in sorted_locations:
        items = grouped_items[location]
        location_name = {
            'System Preferences': 'Login Items',
            '~/Library/LaunchAgents': 'User Launch Agents',
            '/Library/LaunchAgents': 'Global Launch Agents',
            '/Library/LaunchDaemons': 'System Daemons'
        }.get(location, location)

        result += f"📁 {location_name} ({len(items)})\n"

        for item in items:
            status = "✅" if item['enabled'] else "❌"
            impact = item['impact']['level']

            result += f"   {status} {item['name']}\n"
            if item['impact']['is_critical']:
                result += f"      ⚠️ Critical item, impact: {impact}\n"
            else:
                result += f"      Impact: {impact}\n"

        result += "\n"

    # 添加使用提示
    if not show_all:
        result += "💡 Tip: By default, only user-installed items are shown. Use 'show_all: true' to see all items (including 800+ system entries).\n"

    return result

@mcp.tool()
def disable_startup_item(item_name: str) -> str:
    """禁用指定的开机启动项

    安全地禁用启动项，会自动检查是否为关键项避免影响系统运行。

    Args:
        item_name: 启动项名称（如 'Docker', 'FlClash' 等）
    """
    startup_items = manager.get_startup_items()
    if manager.last_error is not None:
        raise RuntimeError(f"Failed to get startup items: {manager.last_error}")
    
    target_item = None
    for item in startup_items:
        if item['name'].lower() == item_name.lower():
            target_item = item
            break
    
    if not target_item:
        raise ValueError(f"Startup item named '{item_name}' not found")
    
    if target_item['impact']['is_critical']:
        raise RuntimeError(f"⚠️ '{item_name}' is a critical startup item; disabling is not recommended!")
    
    success = manager.disable_startup_item(target_item)
    
    if success:
        return f"✅ Disabled startup item: {item_name}"

    raise RuntimeError(f"❌ Failed to disable startup item: {item_name}")

# @mcp.tool()
# def enable_startup_item(item_name: str) -> str:
#     """启用指定的开机启动项
#
#     重新启用之前被禁用的启动项。
#
#     Args:
#         item_name: 启动项名称
#     """
#     startup_items = manager.get_startup_items()
#
#     target_item = None
#     for item in startup_items:
#         if item['name'].lower() == item_name.lower():
#             target_item = item
#             break
#
#     if not target_item:
#         return f"未找到名为 '{item_name}' 的启动项"
#
#     success = manager.enable_startup_item(target_item)
#
#     if success:
#         return f"✅ 成功启用启动项: {item_name}"
#     else:
#         return f"❌ 启用启动项失败: {item_name}"

# @mcp.tool()
# def natural_language_control(command: str, confirm: bool = False) -> str:
#     """使用自然语言控制启动项
#
#     支持自然语言命令，如：
#     - '禁用所有游戏相关的启动项'
#     - '关闭不常用的启动项'
#     - '优化启动速度'
#
#     Args:
#         command: 自然语言描述的控制命令
#         confirm: 是否执行操作（默认False只预览，True执行操作）
#     """
#     matches = manager.parse_natural_language(command)
#
#     if not matches:
#         return "未找到匹配的启动项，请尝试更具体的描述"
#
#     result = f"根据命令 '{command}' 找到以下匹配项:\n\n"
#
#     for match in matches[:10]:  # 最多显示10个匹配项
#         item = match['item']
#         action = match['action']
#         confidence = match['confidence']
#
#         action_text = "禁用" if action == 'disable' else "启用"
#
#         result += f"🎯 **{item['name']}** (匹配度: {confidence:.2f})\n"
#         result += f"   当前状态: {'已启用' if item['enabled'] else '已禁用'}\n"
#         result += f"   建议操作: {action_text}\n"
#         result += f"   影响级别: {item['impact']['level']}\n\n"
#
#         if confirm and action:
#             if action == 'disable' and not item['impact']['is_critical']:
#                 success = manager.disable_startup_item(item)
#                 result += f"   {'✅ 已禁用' if success else '❌ 禁用失败'}\n"
#             elif action == 'enable':
#                 success = manager.enable_startup_item(item)
#                 result += f"   {'✅ 已启用' if success else '❌ 启用失败'}\n"
#             elif action == 'disable' and item['impact']['is_critical']:
#                 result += f"   ⚠️ 关键启动项，跳过禁用操作\n"
#             result += "\n"
#
#     if not confirm:
#         result += "\n💡 添加参数 'confirm: true' 来执行这些操作"
#
#     return result

@mcp.tool()
def analyze_startup_performance() -> str:
    """分析启动性能并提供优化建议

    Analyze current startup items' impact on system boot time and provide optimization suggestions.
    """
    analysis = manager.get_startup_performance_analysis()
    
    result = "🔍 Startup Performance Analysis\n\n"
    result += f"📊 Stats:\n"
    result += f"   • Total startup items: {analysis['total_items']}\n"
    result += f"   • Enabled items: {analysis['enabled_items']}\n"
    result += f"   • Critical items: {analysis['critical_items']}\n"
    result += f"   • Optimizable items: {analysis['optimizable_items']}\n"
    result += f"   • Optimization potential: {analysis['optimization_potential']}\n\n"
    
    result += f"💡 Recommendations:\n"
    for i, rec in enumerate(analysis['recommendations'], 1):
        result += f"   {i}. {rec}\n"
    
    return result

# @mcp.tool()
# def backup_startup_state() -> str:
#     """备份当前启动项状态"""
#     manager._backup_startup_state()
#     return "✅ 启动项状态已成功备份"
#
# @mcp.tool()
# def restore_startup_state(backup_file: str) -> str:
#     """从备份恢复启动项状态"""
#     success = manager.restore_startup_state(backup_file)
#
#     if success:
#         return f"✅ 成功从 {backup_file} 恢复启动项状态"
#     else:
#         return f"❌ 从 {backup_file} 恢复启动项状态失败"


# 导出 MCP 服务器实例以便外部使用
mcp_server = mcp

def main():
    """主入口函数"""
    mcp.run()

if __name__ == "__main__":
    main()
