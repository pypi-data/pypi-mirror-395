import tempfile
import time
from pathlib import Path
import subprocess
import sys
import os

import keyboard
from PIL import ImageGrab
import tkinter as tk
import pyclip


def get_real_user_env():
    """
    获取 sudo 之前的真实用户信息
    """
    # 当使用 sudo 运行脚本时，环境变量中会保留 SUDO_USER 和 SUDO_UID
    user = os.environ.get('SUDO_USER')
    uid = os.environ.get('SUDO_UID')
    
    if not user or not uid:
        # 如果是 Linux 环境且必须依赖 sudo 获取用户信息，则报错
        # 对于 Windows/Mac 或非必须 sudo 的场景，可能需要调整，但根据 provided snippet 逻辑保留
        print("❌ 错误: 请使用 sudo 运行此脚本 (例如: sudo python3 script.py)")
        sys.exit(1)
        
    return user, uid


class RegionSelector:
    def __init__(self) -> None:
        self._start_x = 0
        self._start_y = 0
        self._rect = None
        self._glow_rects = []
        self._bbox = None
        self._root = None
        self._canvas = None

    def select(self):
        self._root = tk.Tk()
        self._root.attributes("-fullscreen", True)
        self._root.attributes("-alpha", 0.3)
        self._root.attributes("-topmost", True)
        self._root.configure(bg="black")

        self._canvas = tk.Canvas(self._root, cursor="cross", bg="gray", highlightthickness=0)
        self._canvas.pack(fill=tk.BOTH, expand=True)

        self._canvas.bind("<ButtonPress-1>", self._on_button_press)
        self._canvas.bind("<B1-Motion>", self._on_move_press)
        self._canvas.bind("<ButtonRelease-1>", self._on_button_release)
        self._root.bind("<Escape>", self._cancel)

        self._root.focus_force()
        self._root.grab_set()

        self._root.mainloop()
        return self._bbox

    def _on_button_press(self, event):
        self._start_x = event.x
        self._start_y = event.y
        if self._rect:
            self._canvas.delete(self._rect)
        if self._glow_rects:
            for glow in self._glow_rects:
                self._canvas.delete(glow)
        self._glow_rects = []

        glow_styles = (("#5bb0ff", 2), ("#2f80ed", 1))
        for color, width in glow_styles:
            glow_rect = self._canvas.create_rectangle(
                self._start_x,
                self._start_y,
                event.x,
                event.y,
                outline=color,
                width=width,
            )
            self._glow_rects.append(glow_rect)

        self._rect = self._canvas.create_rectangle(
            self._start_x,
            self._start_y,
            event.x,
            event.y,
            outline="#02e16e",
            width=1,
        )

    def _on_move_press(self, event):
        if not self._rect:
            return
        self._canvas.coords(self._rect, self._start_x, self._start_y, event.x, event.y)
        for glow in self._glow_rects:
            self._canvas.coords(glow, self._start_x, self._start_y, event.x, event.y)

    def _on_button_release(self, event):
        if not self._rect:
            return
        x0, y0 = self._start_x, self._start_y
        x1, y1 = event.x, event.y
        left, right = sorted([x0, x1])
        top, bottom = sorted([y0, y1])
        if left != right and top != bottom:
            self._bbox = (left, top, right, bottom)
        for glow in self._glow_rects:
            self._canvas.delete(glow)
        self._glow_rects.clear()
        self._rect = None
        self._root.destroy()

    def _cancel(self, _event):
        if self._root is None:
            return
        self._bbox = None
        for glow in self._glow_rects:
            self._canvas.delete(glow)
        self._glow_rects.clear()
        self._rect = None
        try:
            self._root.destroy()
        except tk.TclError:
            pass
        self._root = None

    def cancel(self):
        if self._root is not None:
            self._cancel(None)

    def _take_screenshot_linux(self):
        """
        Linux 下使用 gdbus 调用系统截图
        """
        user, uid = get_real_user_env()
        
        # 构造 DBus 地址 (Ubuntu 默认规则: /run/user/<UID>/bus)
        # 这是 root 能找到用户桌面会话的关键
        dbus_address = f"unix:path=/run/user/{uid}/bus"
        
        print(f"[{time.strftime('%H:%M:%S')}] 检测到按键，正在以用户 [{user}] 身份请求截图...")

        # 构造命令：
        # 1. sudo -u <user>: 切换回普通用户身份
        # 2. env DBUS_...:  手动注入 DBus 环境变量
        # 3. gdbus ...:     执行原始截图命令
        cmd = [
            "sudo", "-u", user,
            "env", f"DBUS_SESSION_BUS_ADDRESS={dbus_address}",
            "gdbus", "call", "--session",
            "--dest", "org.freedesktop.portal.Desktop",
            "--object-path", "/org/freedesktop/portal/desktop",
            "--method", "org.freedesktop.portal.Screenshot.Screenshot",
            "",
            "{'interactive': <true>}"
        ]

        try:

            # 清空剪贴板
            pyclip.copy('')

            # 运行命令
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print(f"✅ 截图界面已呼出")
                while True:
                    if keyboard.is_pressed('esc'):
                        print("取消截图")
                        return None
                    elif keyboard.is_pressed('enter'):
                        print("截图成功，返回剪切板图片数据")
                        waittime = 60
                        start_time = time.time()
                        while time.time() -  start_time < waittime:
                            try:
                                content = pyclip.paste()
                                if content:
                                   return content
                            except Exception as e:
                                break
                            time.sleep(0.1)
                        return None
                    time.sleep(0.05)                  

            else:
                print(f"❌ 调用失败 (Code {result.returncode})")
                print(f"   错误信息: {result.stderr.strip()}")
                return None
                
        except Exception as e:
            print(f"❌ 发生异常: {str(e)}")
        
        return None

    def screenshot(self):
        # 判断是否为 Linux 系统
        if sys.platform == 'linux':
            return self._take_screenshot_linux()

        bbox = self.select()
        if not bbox:
            print("[Screenshot] 操作被取消。")
            return
        image = ImageGrab.grab(bbox=bbox)
        # temp_path = Path(tempfile.gettempdir()) / f"screenshot_{int(time.time() * 1000)}.png"
        # image.save(temp_path)
        # print(f"[Screenshot] 已保存至: {temp_path}")

        return image

def main():
    selector = RegionSelector()
    
    HOTKEY = 'f8+8' 
    
    def on_activate():
        selector.screenshot()

    # Linux 下检查是否以 root 运行
    if sys.platform == 'linux':
        if os.geteuid() != 0:
            print("⚠️  错误: 此脚本需要 root 权限才能监听键盘。")
            print(f"👉 请使用: sudo {sys.executable} {sys.argv[0]}")
            sys.exit(1)
        
        print(f"🎧 [Root模式] 截图服务已启动")
        print(f"👤 目标用户: {os.environ.get('SUDO_USER') or os.environ.get('USER')}")
    else:
        print(f"🎧 截图服务已启动")

    print(f"👉 请按下快捷键 [{HOTKEY}] 调用截图 UI")
    print(f"⌨️  按 ESC 键退出脚本")

    # suppress=True: 拦截按键，防止 '8' 被输入到终端或编辑器中
    keyboard.add_hotkey(HOTKEY, on_activate, suppress=True)

    keyboard.wait('esc')

if __name__ == "__main__":
    
    main()