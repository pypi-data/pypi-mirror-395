from typing import Optional
import os
import sys
import subprocess
import shutil
from tellit import Notify

def desktop_notification(message="", title="picfly", timeout=5, icon_path: Optional[str] = None):
    """
    桌面气泡通知。

    Args:
        title (str): 通知的标题。
        message (str): 通知的内容。
        timeout (int): 通知在屏幕上显示的时间（秒）。默认为 5。
    """
    # 截断超长字符串（避免超限）
    title = title[:20]  # 标题最多20字符
    message = message[:64]  # 内容最多64字符
    app_icon = icon_path or ""

    # Linux 平台下优先使用 notify-send 避免 sudo 下的 DBus 问题
    if sys.platform == 'linux':
        # 尝试查找 notify-send
        notify_send = shutil.which('notify-send')
        if notify_send:
            try:
                cmd = []
                
                # 检查是否在 sudo 环境下
                sudo_user = os.environ.get('SUDO_USER')
                sudo_uid = os.environ.get('SUDO_UID')
                
                if sudo_user and sudo_uid:
                    # 如果是 sudo 运行，切换回原用户发送通知
                    dbus_address = f"unix:path=/run/user/{sudo_uid}/bus"
                    cmd.extend([
                        'sudo', '-u', sudo_user,
                        'env', f'DBUS_SESSION_BUS_ADDRESS={dbus_address}'
                    ])
                
                cmd.append(notify_send)
                cmd.append(title)
                cmd.append(message)
                cmd.extend(['-t', str(timeout * 1000)]) # 毫秒
                
                if app_icon:
                    cmd.extend(['-i', app_icon])
                else:
                    # 默认图标
                    cmd.extend(['-i', 'dialog-information'])
                print(cmd)
                subprocess.run(cmd, check=False, capture_output=True)
                return
            except Exception as e:
                print(f"notify-send failed: {e}, falling back to plyer")

    # 其他平台或 notify-send 失败时回退到 plyer
    try:
        notification = Notify()
        notification.title = title
        notification.message = message
        notification.icon = app_icon
        notification.send()
    except Exception as e:
        print(f"Notification failed: {e}")

    # # 等待通知显示完成（避免脚本提前退出导致通知不显示）
    # time.sleep(timeout)

# 调用示例
if __name__ == "__main__":
    desktop_notification(
        message="这是一条桌面气泡通知～\n支持多行文本显示",
    )