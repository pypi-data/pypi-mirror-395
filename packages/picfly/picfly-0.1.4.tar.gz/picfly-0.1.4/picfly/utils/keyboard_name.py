import keyboard

def on_key_press(e):
    # 打印按下的键的原始名称
    print(f"按下的键名: {e.name}, 扫描码: {e.scan_code}")


if __name__ == "__main__":
    # 监听所有按键
    keyboard.on_press(on_key_press)
    print("请按下减号键（主键盘/-或小键盘-），查看输出的键名...")
    keyboard.wait('esc')  # 按ESC退出监听