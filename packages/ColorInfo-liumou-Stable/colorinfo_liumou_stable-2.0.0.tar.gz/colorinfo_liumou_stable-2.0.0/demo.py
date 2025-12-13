# -*- encoding: utf-8 -*-
"""
@File    :   demo.py
@Time    :   2025年3月27日00:33:56
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   liumou.site@qq.com
@Homepage : https://liumou.site
@Desc    :   演示
"""
from ColorInfo_liumou_Stable import ColorLogger, logger, sugar, JSONStructuredLogger


def demos():
    # 传统日志记录方式
    log = ColorLogger(txt=True, fileinfo=True, basename=False)
    log.info(msg='1', x="23")
    log.error('2', '22', '222')
    log.debug('3', '21')
    log.warning('4', '20', 22)
    
    # 结构化日志记录方式（类似 Zap）
    print("\n=== 结构化日志演示 ===")
    structured_log = sugar(ColorLogger(txt=True, fileinfo=True, basename=False))
    
    # 使用字段式日志记录
    structured_log.info('用户登录', user_id=12345, username='admin', ip='192.168.1.1')
    structured_log.error('数据库连接失败', error='ConnectionRefused', host='localhost', port=3306)
    structured_log.debug('API 调用', endpoint='/api/users', method='GET', status=200, duration=45.2)
    structured_log.warning('内存使用率高', usage_percent=85.3, threshold=80, service='web-server')
    
    # JSON 格式的结构化日志
    print("\n=== JSON 结构化日志演示 ===")
    json_log = JSONStructuredLogger(ColorLogger(txt=True, fileinfo=True, basename=False))
    json_log.info('订单处理', order_id='ORD-2024-001', amount=99.99, customer='张三')
    json_log.error('支付失败', error_code='PAY_001', transaction_id='TXN-123456')


class Demo:
    def __init__(self):
        self.logger = logger
        self.logger.info("初始化")

    def de(self):
        self.logger.debug("de1")
        logger.info("de2")
        logger.warning("de3")
        logger.error("de4")


if __name__ == "__main__":
    d = Demo()
    d.de()
    demos()
