# -*- encoding: utf-8 -*-
"""
@File    :   demo_structured_lines.py
@Time    :   2025年12月07日
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   liumou.site@qq.com
@Homepage : https://liumou.site
@Desc    :   演示结构化日志如何改进 demo.py 的 16-19 行
"""
from ColorInfo_liumou_Stable import ColorLogger, sugar


def demonstrate_improved_logging():
    """演示如何改进 demo.py 的 16-19 行日志记录"""
    
    # 原来的方式（demo.py 16-19 行）
    print("=== 原来的日志记录方式 ===")
    log = ColorLogger(txt=True, fileinfo=True, basename=False)
    log.info(msg='1', x="23")  # 第16行
    log.error('2', '22', '222')  # 第17行
    log.debug('3', '21')  # 第18行
    log.warning('4', '20', 22)  # 第19行
    
    print("\n=== 改进后的结构化日志记录方式 ===")
    # 使用结构化日志改进这些调用
    structured_log = sugar(ColorLogger(txt=True, fileinfo=True, basename=False))
    
    # 第16行改进：更清晰的字段表达
    structured_log.info('1', x="23")
    
    # 第17行改进：为参数添加明确的字段名
    structured_log.error('2', code='22', message='222')
    
    # 第18行改进：为调试信息添加上下文
    structured_log.debug('3', value='21')
    
    # 第19行改进：为警告参数添加描述性字段名
    structured_log.warning('4', min_value='20', max_value=22)
    
    print("\n=== 更高级的结构化日志示例 ===")
    # 展示结构化日志的真正威力
    structured_log.info('用户操作',
                     user_id=12345,
                     action='login',
                     ip='192.168.1.100',
                     user_agent='Mozilla/5.0')
    
    structured_log.error('业务处理失败',
                        error_type='database',
                        error_code='DB_CONNECTION_LOST',
                        retry_count=3,
                        affected_records=150)


if __name__ == "__main__":
    demonstrate_improved_logging()