"""
Lightweight Operational Progress Kit (LOPK) v4.0
一个轻量级的操作进度工具包，提供丰富的进度条和终端操作功能

Author: I-love-china
Version: 4.0.0
License: MIT
"""

__version__ = "4.0.0"
__author__ = "I-love-china,douyin:我是小miao~qwq,youtube:BlackNest,bilibili:绿色__帽子"
__email__ = "13709048021@163.com"

# 处理相对导入问题
try:
    from .lopk import (
        ProgressBar,
        Spinner,
        CountdownTimer,
        MultiProgressBar,
        TkProgressBar,
        AK,
        cls,
        clear_line,
        get_terminal_size,
        colored_text,
        format_file_size,
        format_time
    )
except ImportError:
    # 直接运行时使用绝对导入
    from lopk import (
        ProgressBar,
        Spinner,
        CountdownTimer,
        MultiProgressBar,
        TkProgressBar,
        AK,
        cls,
        clear_line,
        get_terminal_size,
        colored_text,
        format_file_size,
        format_time
    )

__all__ = [
    "ProgressBar",
    "Spinner", 
    "CountdownTimer",
    "MultiProgressBar",
    "TkProgressBar",
    "AK",
    "cls",
    "clear_line",
    "get_terminal_size",
    "colored_text",
    "format_file_size",
    "format_time"
]

def main():
    """命令行主函数 - 输出作者、版本和邮箱信息"""
    print("=== Lightweight Operational Progress Kit (LOPK) ===")
    print(f"版本: {__version__}")
    print(f"作者: {__author__}")
    print(f"邮箱: {__email__}")
    print("=" * 50)
    print("这是一个轻量级的操作进度工具包")
    print("包含进度条、旋转指示器、倒计时器等实用功能")
    print("=" * 50)

if __name__ == "__main__":
    main()