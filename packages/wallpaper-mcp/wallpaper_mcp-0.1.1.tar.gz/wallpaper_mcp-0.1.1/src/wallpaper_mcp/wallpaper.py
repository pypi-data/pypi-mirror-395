"""壁纸设置核心功能模块"""

import os
import platform
import subprocess
import shutil
import tempfile
from pathlib import Path
from typing import Optional, Tuple
from PIL import Image
import requests
from io import BytesIO
import logging

logger = logging.getLogger(__name__)


class WallpaperManager:
    """跨平台壁纸管理器"""

    def __init__(self):
        self.system = platform.system()
        self.wallpaper_dir = Path.home() / ".wallpapers"
        self.wallpaper_dir.mkdir(exist_ok=True)

    def download_image(self, url: str) -> Path:
        """下载网络图片到本地"""
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            # 保存到临时文件
            img = Image.open(BytesIO(response.content))

            # 确定文件格式
            format_ext = img.format.lower() if img.format else 'jpg'
            temp_path = self.wallpaper_dir / f"wallpaper_{os.getpid()}.{format_ext}"

            # 保存图片
            img.save(temp_path, format=img.format or 'JPEG')
            logger.info(f"图片已下载到: {temp_path}")
            return temp_path

        except Exception as e:
            logger.error(f"下载图片失败: {e}")
            raise Exception(f"下载图片失败: {e}")

    def process_image(self, image_path: Path, target_resolution: Optional[Tuple[int, int]] = None) -> Path:
        """处理图片（验证、调整分辨率等）"""
        try:
            img = Image.open(image_path)

            # 获取图片信息
            width, height = img.size
            logger.info(f"原始图片分辨率: {width}x{height}")

            # 如果指定了目标分辨率，进行调整
            if target_resolution:
                target_w, target_h = target_resolution

                # 计算缩放比例，保持宽高比
                scale = max(target_w / width, target_h / height)
                new_width = int(width * scale)
                new_height = int(height * scale)

                # 缩放图片
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

                # 裁剪到目标尺寸
                left = (new_width - target_w) // 2
                top = (new_height - target_h) // 2
                right = left + target_w
                bottom = top + target_h
                img = img.crop((left, top, right, bottom))

                logger.info(f"图片已调整到: {target_w}x{target_h}")

            # 保存处理后的图片
            processed_path = self.wallpaper_dir / f"wallpaper_processed.jpg"
            img.convert("RGB").save(processed_path, "JPEG", quality=95)

            return processed_path

        except Exception as e:
            logger.error(f"处理图片失败: {e}")
            raise Exception(f"处理图片失败: {e}")

    def get_screen_resolution(self) -> Tuple[int, int]:
        """获取当前屏幕分辨率"""
        if self.system == "Darwin":  # macOS
            try:
                result = subprocess.run(
                    ["system_profiler", "SPDisplaysDataType"],
                    capture_output=True,
                    text=True
                )
                # 解析输出获取分辨率
                for line in result.stdout.split('\n'):
                    if 'Resolution:' in line:
                        # 提取分辨率，格式如: "2560 x 1440"
                        parts = line.split(':')[1].strip().split(' x ')
                        if len(parts) == 2:
                            width = int(parts[0].split()[0])
                            height = int(parts[1].split()[0])
                            return (width, height)
            except Exception as e:
                logger.warning(f"获取屏幕分辨率失败: {e}")

        # 默认16:9高清分辨率
        return (1920, 1080)

    def set_wallpaper(self, image_path: Path) -> bool:
        """设置壁纸（跨平台）"""
        image_path = image_path.absolute()

        if not image_path.exists():
            raise FileNotFoundError(f"图片文件不存在: {image_path}")

        try:
            if self.system == "Darwin":  # macOS
                return self._set_wallpaper_macos(image_path)
            elif self.system == "Windows":
                return self._set_wallpaper_windows(image_path)
            elif self.system == "Linux":
                return self._set_wallpaper_linux(image_path)
            else:
                raise NotImplementedError(f"不支持的操作系统: {self.system}")

        except Exception as e:
            logger.error(f"设置壁纸失败: {e}")
            raise

    def _set_wallpaper_macos(self, image_path: Path) -> bool:
        """macOS 设置壁纸"""
        script = f'''
        tell application "System Events"
            tell every desktop
                set picture to "{image_path}"
            end tell
        end tell
        '''

        try:
            subprocess.run(
                ["osascript", "-e", script],
                check=True,
                capture_output=True
            )
            logger.info(f"macOS 壁纸已设置: {image_path}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"macOS 设置壁纸失败: {e}")
            return False

    def _set_wallpaper_windows(self, image_path: Path) -> bool:
        """Windows 设置壁纸"""
        try:
            import ctypes

            # 转换路径为Windows格式
            image_path_str = str(image_path)

            # 调用Windows API
            SPI_SETDESKWALLPAPER = 20
            ctypes.windll.user32.SystemParametersInfoW(
                SPI_SETDESKWALLPAPER, 0, image_path_str, 3
            )
            logger.info(f"Windows 壁纸已设置: {image_path}")
            return True

        except Exception as e:
            logger.error(f"Windows 设置壁纸失败: {e}")
            return False

    def _set_wallpaper_linux(self, image_path: Path) -> bool:
        """Linux 设置壁纸（支持多种桌面环境）"""
        desktop = os.environ.get("DESKTOP_SESSION", "").lower()
        image_path_str = str(image_path)

        try:
            if "gnome" in desktop or "ubuntu" in desktop:
                # GNOME / Ubuntu (Unity)
                subprocess.run([
                    "gsettings", "set",
                    "org.gnome.desktop.background", "picture-uri",
                    f"file://{image_path_str}"
                ], check=True)

            elif "kde" in desktop or "plasma" in desktop:
                # KDE Plasma
                script = f"""
                qdbus org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript '
                    var allDesktops = desktops();
                    for (i=0; i<allDesktops.length; i++) {{
                        d = allDesktops[i];
                        d.wallpaperPlugin = "org.kde.image";
                        d.currentConfigGroup = Array("Wallpaper", "org.kde.image", "General");
                        d.writeConfig("Image", "file://{image_path_str}")
                    }}
                '
                """
                subprocess.run(["bash", "-c", script], check=True)

            elif "xfce" in desktop:
                # XFCE
                subprocess.run([
                    "xfconf-query", "-c", "xfce4-desktop",
                    "-p", "/backdrop/screen0/monitor0/workspace0/last-image",
                    "-s", image_path_str
                ], check=True)

            elif "mate" in desktop:
                # MATE
                subprocess.run([
                    "gsettings", "set",
                    "org.mate.background", "picture-filename",
                    image_path_str
                ], check=True)

            else:
                # 尝试通用的 feh 命令
                subprocess.run(["feh", "--bg-fill", image_path_str], check=True)

            logger.info(f"Linux 壁纸已设置: {image_path}")
            return True

        except Exception as e:
            logger.error(f"Linux 设置壁纸失败: {e}")
            return False

    def set_wallpaper_from_url(self, url: str, resolution: Optional[Tuple[int, int]] = None) -> bool:
        """从URL下载并设置壁纸"""
        try:
            # 下载图片
            logger.info(f"正在下载图片: {url}")
            local_path = self.download_image(url)

            # 如果没有指定分辨率，使用屏幕分辨率
            if not resolution:
                resolution = self.get_screen_resolution()
                logger.info(f"使用屏幕分辨率: {resolution[0]}x{resolution[1]}")

            # 处理图片
            processed_path = self.process_image(local_path, resolution)

            # 设置壁纸
            success = self.set_wallpaper(processed_path)

            # 清理临时文件
            if local_path != processed_path and local_path.exists():
                local_path.unlink()

            return success

        except Exception as e:
            logger.error(f"从URL设置壁纸失败: {e}")
            raise

    def set_wallpaper_from_file(self, file_path: str, resolution: Optional[Tuple[int, int]] = None) -> bool:
        """从本地文件设置壁纸"""
        try:
            file_path = Path(file_path).expanduser().absolute()

            if not file_path.exists():
                raise FileNotFoundError(f"文件不存在: {file_path}")

            # 如果没有指定分辨率，使用屏幕分辨率
            if not resolution:
                resolution = self.get_screen_resolution()
                logger.info(f"使用屏幕分辨率: {resolution[0]}x{resolution[1]}")

            # 处理图片
            processed_path = self.process_image(file_path, resolution)

            # 设置壁纸
            return self.set_wallpaper(processed_path)

        except Exception as e:
            logger.error(f"从文件设置壁纸失败: {e}")
            raise
