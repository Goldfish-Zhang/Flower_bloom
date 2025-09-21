"""
月季花动画 - 优化版
==================

性能优化的季节循环月季花绽放动画

特色功能：
- 立即盛开：打开即可看到花朵绽放
- 季节循环：春→夏→秋→冬的完整循环  
- 优化性能：84个花瓣，流畅60FPS
- 粒子效果：适量的发光和飘落效果
- 快速循环：8秒完成一个生命周期

控制说明：
- 空格键：快速跳转到下一阶段
- ESC键：退出动画

"""

import subprocess
import sys
import os

def main():
    """启动优化版月季花动画"""
    print(__doc__)
    
    input("按回车键启动动画...")
    
    try:
        # 运行优化版动画
        subprocess.run([sys.executable, "rose_animation.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ 动画运行出错: {e}")
    except FileNotFoundError:
        print("❌ 找不到动画文件 rose_animation.py")
    except KeyboardInterrupt:
        print("\n👋 动画已退出")

if __name__ == "__main__":
    main()