# coding=utf-8
# -*- coding: utf-8 -*-
# logger
import logging
import logging.config
import os
import platform
import sys


class Logger:
    if sys.platform.startswith('win'):
        all_log_dir_path = r"D:\log_dir"  # 所有日志存储目录路径
    elif sys.platform.startswith('linux'):
        all_log_dir_path = "/tmp/log_dir"  # 所有日志存储目录路径

    def __init__(self,log_name="default",log_dir_path=None):
        """
            Logger初始化
        """
        self.log_name = log_name or "default"
        # 目录参数
        self.log_dir = log_dir_path or Logger.all_log_dir_path
        self.current_logger_dir_path = os.path.join(self.log_dir, self.log_name)  # 当前logger的目录路径
        self.root_logger_dir_path = os.path.join(self.log_dir,'root')
        os.makedirs(self.current_logger_dir_path, exist_ok=True)
        os.makedirs(self.root_logger_dir_path, exist_ok=True)
        # 配置
        logging.config.dictConfig(self.get_log_setting())  # load 配置文件
        self.logger = logging.getLogger(log_name)

    def logger_check(self):
        # ---- 新增以下检查代码 ----
        print(f"当前 logger 名称: {self.logger.name}")
        if self.logger.handlers:
            print("这个 logger 已配置的处理器 (Handlers):")
            for handler in self.logger.handlers:
                print(f"  - Handler 类型: {type(handler).__name__}")
                if hasattr(handler, 'formatter') and handler.formatter:
                    print(f"    使用的格式器: {handler.formatter._fmt}")
        else:
            print("警告：这个 logger 没有找到任何处理器，可能正在使用上级 logger 的配置!")
        # ---- 检查代码结束 ----

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warn(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def cri(self, message):
        self.logger.critical(message)

    def get_log_setting(self):
        setting_map = {
            'version': 1,  # 保留字
            'disable_existing_loggers': False,  # 禁用已经存在的logger实例,也就是如果为true且有两个logger只会保留最后一个
            # 过滤器
            'filters': {},
            # 日志文件的格式
            'formatters': {
                # 详细的日志格式
                'standard': {
                    'format': "[%(asctime)s][%(levelname)s][%(threadName)s:%(thread)d][logger_id:%(name)s][%(filename)s:%(lineno)d] %(message)s"
                },
                # 简单的日志格式
                'simple': {
                    'format': '[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d] %(message)s'
                },
                # 定义一个特殊的日志格式
                'specific': {
                    'format': '[%(asctime)s][%(levelname)s][%(message)s]'
                }
            },

            # 处理器
            'handlers': {

                # logger的handlers
                # 终端
                'console': {
                    'level': 'INFO',
                    'class': 'logging.StreamHandler',
                    'formatter': 'standard'
                },
                # INFO
                'info': {
                    'level': 'INFO',
                    'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
                    'filename': os.path.join(self.current_logger_dir_path,
                                             "{}_INFO.log".format(self.log_name)),
                    'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
                    'backupCount': 5,  # 最多备份几个
                    'formatter': 'standard',
                    'encoding': 'utf-8',
                },
                # ERROR
                'error': {
                    'level': 'ERROR',
                    'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
                    'filename': os.path.join(self.current_logger_dir_path,
                                             "{}_ERROR.log".format(self.log_name)),
                    'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
                    'backupCount': 5,
                    'formatter': 'standard',
                    'encoding': 'utf-8',
                },
                # DEBUG
                'debug': {
                    'level': 'DEBUG',
                    'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
                    'filename': os.path.join(self.current_logger_dir_path,
                                             "{}_DEBUG.log".format(self.log_name)),
                    'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
                    'backupCount': 5,
                    'formatter': 'standard',
                    'encoding': "utf-8"
                },

                # root handlers
                # root-终端
                'root_console': {
                    'level': 'INFO',
                    'class': 'logging.StreamHandler',
                    'formatter': 'standard'
                },
                # root-INFO
                'root_info': {
                    'level': 'INFO',
                    'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
                    'filename': os.path.join(self.root_logger_dir_path,"ROOT_INFO.log"),

                    'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
                    'backupCount': 5,  # 最多备份几个
                    'formatter': 'standard',
                    'encoding': 'utf-8',
                },
                # root-ERROR
                'root_error': {
                    'level': 'ERROR',
                    'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
                    'filename': os.path.join(self.root_logger_dir_path,"ROOT_ERROR.log"),

                    'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
                    'backupCount': 5,
                    'formatter': 'standard',
                    'encoding': 'utf-8',
                },
                # root-DEBUG
                'root_debug': {
                    'level': 'DEBUG',
                    'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
                    'filename': os.path.join(self.root_logger_dir_path,"ROOT_DEBUG.log"),
                    'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
                    'backupCount': 5,
                    'formatter': 'standard',
                    'encoding': "utf-8"
                }
            },
            'loggers': {
                # 默认的logger应用如下配置
                self.log_name: {
                    'handlers': ['console', 'info', 'error', 'debug'],
                    'level': 'DEBUG',
                    'propagate': True,  # 向不向更高级别的logger传递,也就是所有logger会向根日志器传递
                },

            },
            # 新增对根日志器的配置
            'root': {
                'level': 'INFO',    # 设置根日志器级别为INFO或更低
                'handlers': ['root_console', 'root_info', 'root_error', 'root_debug'],  # 为根日志器添加处理器，例如控制台处理器
            }
        }
        return setting_map

