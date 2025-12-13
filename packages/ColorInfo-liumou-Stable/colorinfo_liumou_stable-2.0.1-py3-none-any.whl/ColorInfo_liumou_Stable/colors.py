# -*- encoding: utf-8 -*-
"""
ColorInfo 日志系统的颜色常量和工具。
"""

class ColorConstants:
    """用于终端输出格式化的 ANSI 颜色代码。"""
    
    # Basic colors
    RED = "\033[31m"      # 红色
    GREEN = "\033[32m"    # 绿色  
    YELLOW = '\033[33m'   # 黄色
    BLUE = '\033[34m'    # 蓝色
    RESET_ALL = '\033[0m' # 重置所有格式
    
    # 用于未来扩展的其他颜色
    MAGENTA = "\033[35m"  # 洋红色
    CYAN = "\033[36m"     # 青色
    WHITE = "\033[37m"    # 白色
    BLACK = "\033[30m"    # 黑色
    
    # 明亮变体
    BRIGHT_RED = "\033[91m"     # 明亮红色
    BRIGHT_GREEN = "\033[92m"   # 明亮绿色
    BRIGHT_YELLOW = "\033[93m"  # 明亮黄色
    BRIGHT_BLUE = "\033[94m"    # 明亮蓝色
    BRIGHT_MAGENTA = "\033[95m" # 明亮洋红色
    BRIGHT_CYAN = "\033[96m"    # 明亮青色
    BRIGHT_WHITE = "\033[97m"   # 明亮白色
    
    # 背景颜色
    BG_RED = "\033[41m"     # 红色背景
    BG_GREEN = "\033[42m"   # 绿色背景
    BG_YELLOW = "\033[43m"  # 黄色背景
    BG_BLUE = "\033[44m"   # 蓝色背景
    BG_RESET = "\033[49m"  # 重置背景