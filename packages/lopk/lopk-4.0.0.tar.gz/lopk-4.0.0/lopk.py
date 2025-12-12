"""
Lightweight Operational Progress Kit (LOPK) v3.0
高级进度条和终端操作工具包

Features:
- 彩色进度条
- 旋转指示器
- 多进度条管理
- 倒计时器
- 终端工具函数
- 跨平台支持
- ETA（预计剩余时间）
- 性能优化

Author: I-love-china
Version: 3.0.0
"""

import os
import sys
import time
import threading
from typing import Optional, Union, List, Callable

# 检查是否支持彩色输出
try:
    import colorama
    colorama.init()
    HAS_COLORAMA = True
except ImportError:
    HAS_COLORAMA = False

# 全局颜色映射，避免重复创建
COLORS = {
    'green': '\033[92m',
    'blue': '\033[94m', 
    'red': '\033[91m',
    'yellow': '\033[93m',
    'cyan': '\033[96m',
    'magenta': '\033[95m',
    'reset': '\033[0m'
}

class ProgressBar:
    """高级进度条类"""
    
    def __init__(self, total: int, prefix: str = '', suffix: str = '', 
                 length: int = 50, fill: str = '█', print_end: str = "\r",
                 color: str = 'green', show_time: bool = True, show_eta: bool = True):
        """
        初始化进度条
        
        Args:
            total: 总进度
            prefix: 前缀字符串
            suffix: 后缀字符串  
            length: 进度条长度
            fill: 进度条填充字符
            print_end: 每次打印结束的字符
            color: 进度条颜色 (green, blue, red, yellow, cyan, magenta)
            show_time: 是否显示耗时
            show_eta: 是否显示预计剩余时间
        """
        self.total = total
        self.prefix = prefix
        self.suffix = suffix
        self.length = length
        self.fill = fill
        self.print_end = print_end
        self.color = color
        self.show_time = show_time
        self.show_eta = show_eta
        self.progress = 0
        self.start_time = time.time()
        self.last_update = 0
        self.last_progress = -1
        # 缓存颜色代码
        self.color_code = COLORS.get(color, '') if HAS_COLORAMA else ''
        self.reset_code = COLORS['reset'] if HAS_COLORAMA else ''

    def update(self, progress: Optional[int] = None, suffix: Optional[str] = None):
        """
        更新进度条
        
        Args:
            progress: 当前进度，如果为None则自动加1
            suffix: 临时后缀，如果提供则覆盖原后缀
        """
        if progress is not None:
            self.progress = progress
        else:
            self.progress += 1

        # 限制进度范围
        self.progress = min(max(self.progress, 0), self.total)
        
        # 只有当进度变化或超过0.1秒时才更新，减少终端IO
        current_time = time.time()
        if self.progress == self.last_progress and (current_time - self.last_update) < 0.1:
            return
        self.last_progress = self.progress
        self.last_update = current_time
        
        # 计算百分比和填充长度
        percent = ("{0:.1f}").format(100 * (self.progress / float(self.total)))
        filled_length = int(self.length * self.progress // self.total)
        bar = self.fill * filled_length + '-' * (self.length - filled_length)
        
        # 计算耗时和ETA
        elapsed_time = current_time - self.start_time
        time_str = f" [{elapsed_time:.1f}s]" if self.show_time else ""
        
        # 计算ETA
        eta_str = ""
        if self.show_eta and self.progress > 0:
            eta = (elapsed_time / self.progress) * (self.total - self.progress)
            eta_str = f" [ETA: {eta:.1f}s]" if eta > 0 else " [ETA: 0.0s]"
        
        # 使用临时后缀或原后缀
        current_suffix = suffix if suffix is not None else self.suffix
        
        # 构建输出字符串
        output = f'\r{self.prefix} |{self.color_code}{bar}{self.reset_code}| {percent}% {self.progress}/{self.total} {current_suffix}{time_str}{eta_str}'
        print(output, end=self.print_end)
        sys.stdout.flush()

        # 完成时换行
        if self.progress == self.total:
            print()

    def reset(self):
        """重置进度条"""
        self.progress = 0
        self.start_time = time.time()
        self.last_update = 0
        self.last_progress = -1

    def finish(self):
        """强制完成进度条"""
        self.progress = self.total
        self.update()
        self.last_progress = -1


class Spinner:
    """旋转指示器类"""
    
    # 静态变量，避免重复创建
    _spinner_chars = ['|', '/', '-', '\\']
    
    def __init__(self, message: str = "处理中...", delay: float = 0.1):
        self.message = message
        self.delay = delay
        self.running = False
        self.thread = None
        # 缓存消息长度
        self.msg_length = len(message) + 2

    def _spin(self):
        """旋转动画线程"""
        i = 0
        chars = self._spinner_chars
        msg = self.message
        while self.running:
            sys.stdout.write(f'\r{msg} {chars[i]}')
            sys.stdout.flush()
            i = (i + 1) % len(chars)
            time.sleep(self.delay)

    def start(self):
        """开始旋转"""
        self.running = True
        self.thread = threading.Thread(target=self._spin, daemon=True)
        self.thread.start()

    def stop(self):
        """停止旋转"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=0.1)  # 添加超时，避免阻塞
        # 使用缓存的消息长度，减少计算
        sys.stdout.write('\r' + ' ' * self.msg_length + '\r')
        sys.stdout.flush()

    def __enter__(self):
        """上下文管理器入口"""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.stop()


class CountdownTimer:
    """倒计时器类"""
    
    def __init__(self, seconds: int, message: str = "倒计时"):
        self.seconds = seconds
        self.message = message
        self.remaining = seconds

    def start(self):
        """开始倒计时"""
        for i in range(self.seconds, 0, -1):
            self.remaining = i
            sys.stdout.write(f'\r{self.message}: {i:2d}秒')
            sys.stdout.flush()
            time.sleep(1)
        sys.stdout.write('\r' + ' ' * 20 + '\r')
        sys.stdout.flush()

    def __enter__(self):
        """上下文管理器入口"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        pass


class MultiProgressBar:
    """多进度条管理器"""
    
    def __init__(self):
        self.bars = []
        self.lock = threading.Lock()
        self.initialized = False

    def add_bar(self, total: int, prefix: str = '', **kwargs):
        """添加进度条"""
        bar = ProgressBar(total, prefix, **kwargs)
        self.bars.append(bar)
        return len(self.bars) - 1

    def update(self, bar_index: int, progress: Optional[int] = None):
        """更新指定进度条"""
        with self.lock:
            if 0 <= bar_index < len(self.bars):
                # 简化实现，避免复杂的光标移动
                # 清空当前输出并重新打印所有进度条
                # 这种方式在进度条数量不多时更可靠
                sys.stdout.write('\033[F' * len(self.bars))  # 上移n行
                sys.stdout.flush()
                
                for i, bar in enumerate(self.bars):
                    if i == bar_index:
                        bar.update(progress)
                    else:
                        # 直接打印其他进度条，不更新
                        current_time = time.time()
                        elapsed_time = current_time - bar.start_time
                        percent = ("{0:.1f}").format(100 * (bar.progress / float(bar.total)))
                        filled_length = int(bar.length * bar.progress // bar.total)
                        bar_str = bar.fill * filled_length + '-' * (bar.length - filled_length)
                        time_str = f" [{elapsed_time:.1f}s]" if bar.show_time else ""
                        eta_str = ""
                        if bar.show_eta and bar.progress > 0:
                            eta = (elapsed_time / bar.progress) * (bar.total - bar.progress)
                            eta_str = f" [ETA: {eta:.1f}s]" if eta > 0 else " [ETA: 0.0s]"
                        output = f'\r{bar.prefix} |{bar.color_code}{bar_str}{bar.reset_code}| {percent}% {bar.progress}/{bar.total} {bar.suffix}{time_str}{eta_str}'
                        print(output)
                sys.stdout.flush()

    def finish_all(self):
        """完成所有进度条"""
        for bar in self.bars:
            bar.finish()


# 工具函数
def AK():
    """等待用户按下回车继续"""
    input("按下回车继续...")


def cls():
    """清屏函数（跨平台）"""
    os.system("cls" if os.name == "nt" else "clear")


def clear_line():
    """清除当前行"""
    sys.stdout.write('\r' + ' ' * 100 + '\r')
    sys.stdout.flush()


def get_terminal_size() -> tuple:
    """获取终端尺寸"""
    try:
        size = os.get_terminal_size()
        return size.columns, size.lines
    except:
        return 80, 24


def colored_text(text: str, color: str) -> str:
    """彩色文本输出"""
    # 使用全局COLORS字典，避免重复创建
    if HAS_COLORAMA and color in COLORS:
        return f"{COLORS[color]}{text}{COLORS['reset']}"
    return text


def format_file_size(size_bytes: int) -> str:
    """格式化文件大小为人类可读格式"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


def format_time(seconds: float) -> str:
    """格式化时间为人类可读格式"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes, seconds = divmod(seconds, 60)
        return f"{int(minutes)}m {int(seconds)}s"
    else:
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"


# 基于tkinter的进度条类
try:
    import tkinter as tk
    from tkinter import ttk
    import threading
    
    class TkProgressBar:
        """基于tkinter的图形化进度条类"""
        
        def __init__(self, total: int, title: str = "进度", prefix: str = "进度", suffix: str = "", 
                     length: int = 300, show_time: bool = True, show_eta: bool = True):
            """
            初始化tkinter进度条
            
            Args:
                total: 总进度
                title: 窗口标题
                prefix: 前缀文本
                suffix: 后缀文本
                length: 进度条长度（像素）
                show_time: 是否显示耗时
                show_eta: 是否显示预计剩余时间
            """
            self.total = total
            self.title = title
            self.prefix = prefix
            self.suffix = suffix
            self.length = length
            self.show_time = show_time
            self.show_eta = show_eta
            self.progress = 0
            self.start_time = time.time()
            self.running = True
            self.last_update = 0
            self.update_interval = 0.1  # 限制更新频率，避免未响应
            
            # 使用线程安全的方式更新进度
            self._progress_queue = []
            self._lock = threading.Lock()
            
            # 初始化进度值和文本
            percent = "0.0"
            text = f"{self.prefix}: {percent}% {self.progress}/{self.total} {self.suffix}"
            
            # 创建tkinter窗口 - 主线程中创建
            self.root = tk.Tk()
            self.root.title(title)
            self.root.geometry(f"{length + 100}x100")
            self.root.resizable(False, False)
            
            # 设置窗口关闭事件
            self.root.protocol("WM_DELETE_WINDOW", self._close)
            
            # 设置窗口置顶，确保用户能看到
            self.root.attributes("-topmost", True)
            
            # 创建框架
            self.frame = ttk.Frame(self.root, padding="10")
            self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            
            # 创建进度条
            self.progress_var = tk.DoubleVar(value=0)
            self.progress_bar = ttk.Progressbar(
                self.frame, 
                variable=self.progress_var, 
                maximum=total, 
                length=length,
                mode="determinate"
            )
            self.progress_bar.grid(row=1, column=0, columnspan=2, pady=(10, 0), sticky=(tk.W, tk.E))
            
            # 创建标签
            self.text_var = tk.StringVar(value=text)
            self.label = ttk.Label(self.frame, textvariable=self.text_var, font=('Arial', 10))
            self.label.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky=tk.W)
            
            # 创建关闭按钮
            self.close_btn = ttk.Button(self.frame, text="关闭", command=self._close)
            self.close_btn.grid(row=2, column=1, pady=10, sticky=tk.E)
            
            # 配置列权重
            self.frame.columnconfigure(0, weight=1)
            self.root.columnconfigure(0, weight=1)
            self.root.rowconfigure(0, weight=1)
            
            # 立即显示窗口
            self.root.update()
            self.root.deiconify()
            
            # 使用after方法定期检查更新，避免线程问题
            self.root.after(100, self._check_update)
        
        def _update_text(self):
            """更新文本显示"""
            current_time = time.time()
            elapsed_time = current_time - self.start_time
            percent = ("{0:.1f}").format(100 * (self.progress / float(self.total)))
            time_str = f" [{elapsed_time:.1f}s]" if self.show_time else ""
            
            eta_str = ""
            if self.show_eta and self.progress > 0:
                eta = (elapsed_time / self.progress) * (self.total - self.progress)
                eta_str = f" [ETA: {eta:.1f}s]" if eta > 0 else " [ETA: 0.0s]"
            
            text = f"{self.prefix}: {percent}% {self.progress}/{self.total} {self.suffix}{time_str}{eta_str}"
            self.text_var.set(text)
        
        def _check_update(self):
            """定期检查是否需要更新进度条"""
            if not self.running:
                return
            
            # 检查是否有新的进度更新
            with self._lock:
                if self._progress_queue:
                    progress, suffix = self._progress_queue.pop(0)
                    self._do_update(progress, suffix)
            
            # 继续检查
            self.root.after(100, self._check_update)
        
        def _do_update(self, progress: int, suffix: str):
            """实际更新进度条的函数（在tkinter主线程中调用）"""
            if not self.running:
                return
            
            self.progress = progress
            
            # 限制进度范围
            self.progress = min(max(self.progress, 0), self.total)
            
            # 更新进度值
            self.progress_var.set(self.progress)
            
            # 更新文本
            if suffix is not None:
                self.suffix = suffix
            self._update_text()
            
            # 完成时自动关闭
            if self.progress == self.total:
                self.root.after(1000, self._close)
        
        def _close(self):
            """安全关闭窗口"""
            if not self.running:
                return
            
            try:
                self.running = False
                # 安全关闭tkinter窗口
                if self.root.winfo_exists():
                    self.root.destroy()
            except Exception as e:
                pass
        
        def update(self, progress: Optional[int] = None, suffix: Optional[str] = None):
            """
            更新进度条，线程安全
            
            Args:
                progress: 当前进度，如果为None则自动加1
                suffix: 临时后缀，如果提供则覆盖原后缀
            """
            if not self.running:
                return
            
            # 计算新进度
            new_progress = progress if progress is not None else self.progress + 1
            
            # 确保进度可以达到100%
            if new_progress >= self.total:
                new_progress = self.total
            
            # 将更新请求放入队列（不限制频率，确保最终进度能更新）
            with self._lock:
                self._progress_queue.append((new_progress, suffix))
            
            # 触发tkinter事件循环更新
            self.root.event_generate("<<ProgressUpdate>>", when="tail")
        
        def reset(self):
            """重置进度条"""
            if not self.running:
                return
            
            with self._lock:
                self.progress = 0
                self.start_time = time.time()
                self.last_update = 0
                self._progress_queue.append((0, None))
            
            # 触发tkinter事件循环更新
            self.root.event_generate("<<ProgressUpdate>>", when="tail")
        
        def finish(self):
            """强制完成进度条"""
            if not self.running:
                return
            
            self.update(self.total)
        
        def show(self):
            """显示窗口并运行主循环"""
            try:
                self.root.mainloop()
            except Exception as e:
                pass
            finally:
                self.running = False
except ImportError:
    # 如果tkinter不可用，提供一个占位类
    class TkProgressBar:
        """基于tkinter的图形化进度条类（占位）"""
        
        def __init__(self, *args, **kwargs):
            raise ImportError("tkinter is not available")


# 演示函数
def demo():
    """演示函数"""
    print("=== LOPK v3.0 演示 ===")
    
    # 演示进度条
    print("\n1. 彩色进度条演示:")
    bar = ProgressBar(100, "下载", color="cyan", show_time=True)
    for i in range(101):
        bar.update(i)
        time.sleep(0.02)
    
    # 演示旋转指示器
    print("\n2. 旋转指示器演示:")
    with Spinner("正在处理数据"):
        time.sleep(3)
    print("处理完成!")
    
    # 演示倒计时
    print("\n3. 倒计时演示:")
    with CountdownTimer(5, "准备开始"):
        pass
    print("开始!")
    
    print("\n演示完成!")


def demo_tk():
    """基于tkinter的进度条演示函数"""
    print("=== LOPK v3.0 基于tkinter的进度条演示 ===")
    
    try:
        # 创建进度条
        tk_bar = TkProgressBar(100, title="LOPK 进度演示", prefix="下载进度")
        
        # 使用线程更新进度，避免阻塞tkinter主循环
        def update_progress():
            for i in range(101):
                tk_bar.update(i, suffix="MB")
                time.sleep(0.05)
        
        # 启动进度更新线程
        update_thread = threading.Thread(target=update_progress, daemon=True)
        update_thread.start()
        
        # 运行tkinter主循环
        tk_bar.show()
        
        print("\ntkinter进度条演示完成!")
    except Exception as e:
        print(f"tkinter进度条演示失败: {e}")


if __name__ == "__main__":
    demo()
    AK()