# -*- coding:utf-8 -*-
import datetime
import inspect
import json
import logging
import shutil
import time
import urllib.request
import pandas as pd
import WeComMsg
import xlwings as xw
import yagmail
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import HiveClient
from PIL import ImageGrab, Image
from bs4 import BeautifulSoup
import re
import numpy as np
from pypinyin import lazy_pinyin
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import requests
import psutil
import pythoncom
from tenacity import retry, stop_after_attempt, wait_fixed
import os


class DataProcessingAndMessaging:
    def __init__(self, enable_console_log=None):
        # -------------------------- 1. 主类日志初始化 --------------------------
        caller_frame = inspect.stack()[1]
        caller_filename = caller_frame.filename
        caller_filename = os.path.abspath(caller_filename)
        script_dir = os.path.dirname(caller_filename)
        log_filename = os.path.splitext(os.path.basename(caller_filename))[0] + ".log"
        self.main_log_file = os.path.join(script_dir, log_filename)

        self.logger = logging.getLogger("main_logger")
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False  # 防止日志扩散
        if not self.logger.handlers:
            file_handler = logging.FileHandler(self.main_log_file, encoding='utf-8')
            file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(file_handler)
            if enable_console_log:
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
                self.logger.addHandler(console_handler)

        self.logger.info("初始化 DataProcessingAndMessaging 类")

        # -------------------------- 2. 主类核心参数初始化 --------------------------
        self.start_time = None
        self.current_script_name = None
        self.log_filename = None
        self.current_script_names = None
        self.current_path = None
        self.path = None

        # 企业微信消息发送参数（建议通过环境变量加载）
        self.corpid = os.getenv("WECOM_CORPID", "wxd4e113eb4c0136b9")
        self.corpsecret = os.getenv("WECOM_CORPSECRET", "PMfPOv2Qqq0iXZAdWHF7WdaW4kkWUZcwyGE4NZtve3k")
        self.agentid = "1000026"

        # -------------------------- 3. 企业微信文档功能初始化 --------------------------
        self.WECHAT_DOC_CORP_ID = os.getenv("WECOM_DOC_CORPID", "wxd4e113eb4c0136b9")
        self.WECHAT_DOC_SECRET = os.getenv("WECOM_DOC_SECRET", "PMfPOv2Qqq0iXZAdWHF7WdaW4kkWUZcwyGE4NZtve3k")
        self.WECHAT_DOC_SPACE_ID = None
        self.WECHAT_DOC_LOG_FILE = os.path.join(script_dir, "docs_operation.log")
        self.wechat_doc_access_token = None
        self._wechat_doc_logger = None  # 企微文档独立日志器（延迟初始化）


    # -------------------------- 企微文档日志：延迟初始化独立日志器 --------------------------
    def _init_wechat_doc_logger(self):
        """仅在首次使用企微文档功能时初始化日志器"""
        if self._wechat_doc_logger is not None:
            return

        self._wechat_doc_logger = logging.getLogger("wechat_doc_logger")
        self._wechat_doc_logger.setLevel(logging.INFO)
        self._wechat_doc_logger.propagate = False  # 禁止日志扩散到主日志

        # 确保日志目录存在
        log_dir = os.path.dirname(self.WECHAT_DOC_LOG_FILE)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        # 添加文件处理器（首次创建日志文件）
        file_handler = logging.FileHandler(self.WECHAT_DOC_LOG_FILE, encoding='utf-8')
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self._wechat_doc_logger.addHandler(file_handler)

        # 写入日志头部
        self._wechat_doc_logger.info(
            f"企微文档操作日志初始化 - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    def _wechat_doc_log(self, message):
        """企微文档专用日志方法"""
        self._init_wechat_doc_logger()  # 延迟初始化
        self._wechat_doc_logger.info(message)
        self.logger.info(f"[企微文档] {message}")  # 同步到主日志（可选）

    # -------------------------- 初始化Edge驱动 --------------------------
    def init_edge_driver(self, headless=True):
        os.environ['WDM_ARCH'] = 'x86'  # 强制32位驱动
        edge_options = Options()
        edge_options.add_argument('--disable-gpu')
        edge_options.add_argument('--no-sandbox')
        edge_options.add_argument('--ignore-certificate-errors')

        if headless:
            edge_options.add_argument('--headless=new')
            edge_options.add_argument('--window-size=1920,1080')

        service = Service(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=edge_options)
        self.logger.info("Edge浏览器初始化成功")
        return driver

    # -------------------------- 脚本路径和文件名初始化 --------------------------
    def Start_Get_filepath_and_filename(self):
        self.start_time = time.time()
        caller_frame = inspect.stack()[1]
        self.current_script_name = caller_frame.filename
        self.log_filename = os.path.splitext(self.current_script_name)[0] + ".log"
        self.current_script_names = os.path.basename(self.current_script_name)
        self.current_path = os.path.dirname(os.path.abspath(self.current_script_name))
        self.path = self.current_path + os.sep
        print(f"当前时间：{self.get_date_and_time('%Y-%m-%d %H:%M:%S', 0)}")
        print(f"开始执行脚本：{self.current_script_names}")
        self.logger.info(f"开始执行脚本：{self.current_script_names}")

    # -------------------------- 脚本结束处理 --------------------------
    def End_operation(self):
        print(f"脚本：{self.current_script_names} 执行成功")
        self.logger.info(f"脚本：{self.current_script_names} 执行成功")
        end_time = time.time()
        elapsed_time = round(end_time - self.start_time, 0)
        print(f"运行时间：{elapsed_time} 秒")
        self.logger.info(f"运行时间：{elapsed_time} 秒")
        self.logger.info('\n' * 10)

    # -------------------------- 企业微信消息发送 --------------------------
    # 仅展示修改后的 uxin_wx 方法，其余代码不变
    def uxin_wx(self, name, message, mentioned_list=None):
        sender = WeComMsg.WeChatWorkSender(self.corpid, self.corpsecret, self.agentid)
        try:
            if isinstance(name, list):
                target_type = "多个用户"
                self.logger.info(f"开始向{target_type}发送消息，目标数量：{len(name)}")
            else:
                target_type = "群聊（Webhook）" if name.startswith("https://") else "单个用户"
                self.logger.info(f"开始向{target_type}发送消息，目标：{name}")

            # ========== 新增：Markdown消息识别与处理 ==========
            # 识别规则：message以特定标识开头（如「MD:」），或显式传入markdown类型
            is_markdown = False
            md_content = ""
            if isinstance(message, dict) and message.get("type") == "markdown":
                # 支持字典格式传参：{"type": "markdown", "content": "markdown内容"}
                is_markdown = True
                md_content = message.get("content", "")
            elif isinstance(message, str) and message.startswith("MD:"):
                # 支持字符串前缀标识："MD:### 标题\n内容"
                is_markdown = True
                md_content = message[3:].strip()  # 去掉前缀"MD:"

            if is_markdown:
                # 处理Markdown消息
                if isinstance(name, str) and name.startswith("https://"):
                    # 群聊Webhook发送Markdown
                    self.logger.info(f"发送群聊Markdown消息：内容={md_content}")
                    result = sender.send_markdown_to_group(name, md_content)
                else:
                    # 个人/多用户发送Markdown
                    receivers = name if isinstance(name, list) else [name]
                    self.logger.info(f"发送个人Markdown消息：内容={md_content}，接收者：{receivers}")
                    result = sender.send_markdown(receivers, md_content)

                msg_id = result.get('msgid', '未知')
                self.logger.info(
                    f"Markdown消息发送结果：{'成功' if result.get('errcode') == 0 else '失败'}，错误信息：{result.get('errmsg')}，消息ID：{msg_id}")

                if result.get('errcode') == 0:
                    print(f"给 {target_type} 的Markdown消息发送成功，消息ID：{msg_id}")
                else:
                    print(
                        f"给 {target_type} 的Markdown消息发送失败，错误码：{result.get('errcode')}，错误信息：{result.get('errmsg')}，消息ID：{msg_id}")
                return

            # ========== 原有逻辑（文本/文件/图片）保持不变 ==========
            if isinstance(name, str) and name.startswith("https://"):
                if isinstance(message, str) and message.endswith(('.xlsx', '.docx', '.pdf', '.txt')) and os.path.isfile(
                        message):
                    file_name = os.path.basename(message)
                    file_size = os.path.getsize(message) / 1024
                    self.logger.info(f"发送群聊文件消息：文件名={file_name}，大小={file_size:.2f}KB")
                    result = sender.send_file_to_group(name, message)
                    msg_id = result.get('msgid', '未知')
                    self.logger.info(
                        f"群聊文件消息发送结果：{'成功' if result.get('errcode') == 0 else '失败'}，错误信息：{result.get('errmsg')}，消息ID：{msg_id}")

                elif isinstance(message, str) and message.endswith(
                        ('.jpg', '.jpeg', '.png', '.gif')) and os.path.isfile(message):
                    img_name = os.path.basename(message)
                    img_size = os.path.getsize(message) / 1024
                    self.logger.info(f"发送群聊图片消息：图片名={img_name}，大小={img_size:.2f}KB")
                    result = sender.send_image_to_group(name, message)
                    msg_id = result.get('msgid', '未知')
                    self.logger.info(
                        f"群聊图片消息发送结果：{'成功' if result.get('errcode') == 0 else '失败'}，错误信息：{result.get('errmsg')}，消息ID：{msg_id}")

                elif isinstance(message, str):
                    at_info = f"，@对象：{mentioned_list}" if mentioned_list else ""
                    self.logger.info(f"发送群聊文本消息：内容={message}{at_info}")
                    result = sender.send_text_to_group(name, message, mentioned_list=mentioned_list)
                    msg_id = result.get('msgid', '未知')
                    self.logger.info(
                        f"群聊文本消息发送结果：{'成功' if result.get('errcode') == 0 else '失败'}，错误信息：{result.get('errmsg')}，消息ID：{msg_id}")

                else:
                    err_msg = "不支持的群聊消息类型"
                    print(err_msg)
                    self.logger.warning(err_msg)
                    return

            else:
                receivers = name if isinstance(name, list) else [name]

                if isinstance(message, str) and message.endswith(('.jpg', '.jpeg', '.png', '.gif')) and os.path.isfile(
                        message):
                    img_name = os.path.basename(message)
                    img_size = os.path.getsize(message) / 1024
                    self.logger.info(f"发送个人图片消息：图片名={img_name}，大小={img_size:.2f}KB，接收者：{receivers}")
                    result = sender.send_image(receivers, message)
                    msg_id = result.get('msgid', '未知')
                    self.logger.info(
                        f"个人图片消息发送结果：{'成功' if result.get('errcode') == 0 else '失败'}，错误信息：{result.get('errmsg')}，消息ID：{msg_id}")

                elif isinstance(message, str) and message.endswith(
                        ('.xlsx', '.docx', '.pdf', '.txt', 'xls', 'csv')) and os.path.isfile(message):
                    file_name = os.path.basename(message)
                    file_size = os.path.getsize(message) / 1024
                    self.logger.info(f"发送个人文件消息：文件名={file_name}，大小={file_size:.2f}KB，接收者：{receivers}")
                    result = sender.send_file(receivers, message)
                    msg_id = result.get('msgid', '未知')
                    self.logger.info(
                        f"个人文件消息发送结果：{'成功' if result.get('errcode') == 0 else '失败'}，错误信息：{result.get('errmsg')}，消息ID：{msg_id}")

                elif isinstance(message, str):
                    self.logger.info(f"发送个人文本消息：内容={message}，接收者：{receivers}")
                    result = sender.send_text(receivers, message)
                    msg_id = result.get('msgid', '未知')
                    self.logger.info(
                        f"个人文本消息发送结果：{'成功' if result.get('errcode') == 0 else '失败'}，错误信息：{result.get('errmsg')}，消息ID：{msg_id}")

                else:
                    err_msg = "不支持的个人消息类型"
                    print(err_msg)
                    self.logger.warning(err_msg)
                    return

            if result.get('errcode') == 0:
                print(f"给 {target_type} 的消息发送成功，消息ID：{result.get('msgid', '未知')}")
            else:
                print(
                    f"给 {target_type} 的消息发送失败，错误码：{result.get('errcode')}，错误信息：{result.get('errmsg')}，消息ID：{result.get('msgid', '未知')}")

        except Exception as e:
            self.logger.error(f"消息发送失败，报错信息: {e}", exc_info=True)
            print(f"发送失败，报错信息: {e}")

    # -------------------------- 企业微信消息撤回 --------------------------
    def recall_message(self, msgid):
        try:
            self.logger.info(f"开始撤回消息，msgid: {msgid}")
            sender = WeComMsg.WeChatWorkSender(self.corpid, self.corpsecret, self.agentid)
            result = sender.recall_message(msgid)

            if result.get('errcode') == 0:
                self.logger.info(f"消息撤回成功，msgid: {msgid}")
                print(f"消息撤回成功，msgid: {msgid}")
            else:
                err_msg = f"消息撤回失败，错误码: {result.get('errcode')}, 错误信息: {result.get('errmsg')}"
                self.logger.warning(err_msg)
                print(err_msg)

            return result
        except Exception as e:
            err_msg = f"撤回消息时发生错误: {str(e)}"
            self.logger.error(err_msg, exc_info=True)
            print(err_msg)
            return

    # -------------------------- 获取Hive表更新时间 --------------------------
    def Get_update_time(self, data_table):
        url4 = f'http://cptools.xin.com/hive/getLastUpdateTime?table={data_table}'
        res = urllib.request.Request(url4)
        try:
            response = urllib.request.urlopen(res, timeout=10)
            html = response.read()
            soup = BeautifulSoup(html, "lxml")
            someData = soup.select("p")
            json_data = json.loads(someData[0].text)
            d_time = json_data['data']
            d_code = json_data['code']
            d_message = json_data['message']

            utc_time = datetime.datetime.utcfromtimestamp(int(d_time))
            beijing_time = utc_time + datetime.timedelta(hours=8)
            self.logger.info(f'更新时间：{beijing_time}')
            print(f'更新时间：{beijing_time}')
            return beijing_time
        except Exception as e:
            self.logger.error(f"获取更新时间失败: {str(e)}", exc_info=True)
            raise

    # -------------------------- 从SQL提取主表名 --------------------------
    def extract_main_table_from_sql(self, sql_query):
        lines = sql_query.split('\n')
        from_line = None
        for line in lines:
            if line.strip().lower().startswith('from'):
                parts = line.strip().split('from', 1)
                if len(parts) > 1:
                    from_table_info = parts[1].strip()
                    table_name = from_table_info.split(' ')[0]
                    from_line = table_name
                    break
        self.logger.info(f'数据表：{from_line}')
        print(f'数据表：{from_line}')
        return from_line

    # -------------------------- 替换SQL中的日期变量 --------------------------
    def replace_day(self, sqls, day_num):
        today = datetime.date.today()
        oneday = datetime.timedelta(days=day_num)
        yesterday = str(today - oneday)
        yesterday = yesterday.replace('-', '')
        yesterday_m = yesterday[0:6]
        sqls = sqls.replace('$dt_ymd', yesterday)
        sqls = sqls.replace('$dt_ym', yesterday_m)
        return sqls

    # -------------------------- 获取指定格式的日期时间 --------------------------
    def get_date_and_time(self, format_type, days):
        today = datetime.datetime.today()
        target_date = today - datetime.timedelta(days=days)
        result = target_date.strftime(format_type)
        return result

    # -------------------------- 发送邮件（旧版） --------------------------
    def sende_email(self, name, contact_name, title, rec, file=None, cc=None, bcc=None, remarks=None):
        """
        简洁版邮件发送（支持重复调用，自动过滤无效参数）
        :param name: 收件人称呼（如"各位"）
        :param contact_name: 联系人姓名（如"董养"）
        :param title: 邮件主题
        :param rec: 收件人邮箱（单个字符串或列表）
        :param file: 附件路径（单个字符串、列表，或None）
        :param cc: 抄送邮箱（单个字符串、列表，或None）
        :param bcc: 密送邮箱（单个字符串、列表，或None）
        :param remarks: 附加备注（可选，默认None，传入文本字符串时追加到正文）
        """

        # 1. 内部工具：格式化邮箱（转列表+过滤无效值）
        def format_email(emails):
            if not emails:
                return None
            # 单个邮箱转列表，列表直接使用
            email_list = [emails] if isinstance(emails, str) else emails
            # 过滤：非空字符串 + 简单格式校验（含@和.）
            valid_emails = [
                e.strip() for e in email_list
                if isinstance(e, str) and e.strip() and '@' in e.strip() and '.' in e.strip()
            ]
            return valid_emails if valid_emails else None

        # 2. 格式化所有邮箱参数
        to_emails = format_email(rec)
        cc_emails = format_email(cc)
        bcc_emails = format_email(bcc)

        # 3. 核心参数校验（提前报错，避免无效连接）
        if not to_emails:
            err_msg = "邮件发送失败：无有效收件人邮箱"
            self.logger.error(err_msg)
            raise ValueError(err_msg)
        if not title.strip():
            err_msg = "邮件发送失败：邮件主题不能为空"
            self.logger.error(err_msg)
            raise ValueError(err_msg)

        # 4. 附件处理（校验存在性，支持单个/列表）
        attachments = None
        if file:
            file_list = [file] if isinstance(file, str) else file
            attachments = []
            for f in file_list:
                f = f.strip()
                if not os.path.exists(f):
                    err_msg = f"邮件发送失败：附件不存在 -> {f}"
                    self.logger.error(err_msg)
                    raise FileNotFoundError(err_msg)
                attachments.append(f)

        # 5. SMTP固定配置（重复调用无需修改）
        smtp_conf = {
            "user": 'cc_yingxiao@xin.com',
            "password": 'cw46pfeznNQx',
            "host": 'mail.xin.com',
            "port": 587,
            "smtp_ssl": False,
            "smtp_starttls": True
        }

        # 6. 邮件内容（新增remarks逻辑：有值则追加到"请查收！"下方，保持缩进一致）
        email_content = f"{name} 好：\n附件为《{title}》，请查收！"
        if remarks and isinstance(remarks, str) and remarks.strip():
            formatted_remarks = remarks.strip().replace('\n', '\n')  # 处理多行备注
            email_content += f"\n{formatted_remarks}"
        email_content += f"\n\n如有疑问请联系{contact_name}，谢谢~"

        try:
            # 上下文管理器：自动关闭连接，重复调用不泄露资源
            with yagmail.SMTP(**smtp_conf) as yag:
                yag.send(
                    to=to_emails,
                    subject=title.strip(),
                    contents=email_content,
                    attachments=attachments,
                    cc=cc_emails,
                    bcc=bcc_emails
                )
            # 简洁日志：关键信息+统计，便于排查
            log_msg = f"邮件发送成功 | 主题：{title.strip()} | 收件人：{len(to_emails)}人"
            if cc_emails:
                log_msg += f" | 抄送：{len(cc_emails)}人"
            if bcc_emails:
                log_msg += f" | 密送：{len(bcc_emails)}人"
            if attachments:
                log_msg += f" | 附件：{len(attachments)}个"
            if remarks and remarks.strip():
                log_msg += f" | 包含备注：{remarks.strip()[:20]}..."  # 日志显示备注前20字（避免过长）
            self.logger.info(log_msg)
            print(log_msg)

        # 7. 分类异常捕获（易排查问题）
        except yagmail.SMTPAuthenticationError:
            err_msg = "邮件发送失败：SMTP账号/密码/授权码错误"
            self.logger.error(err_msg)
            raise ValueError(err_msg)
        except yagmail.SMTPConnectionError:
            err_msg = "邮件发送失败：SMTP服务器连接失败（检查host/port/防火墙）"
            self.logger.error(err_msg)
            raise ConnectionError(err_msg)
        except FileNotFoundError:
            raise  # 附件错误已提前处理，直接抛出
        except Exception as e:
            err_msg = f"邮件发送失败：{str(e)}"
            self.logger.error(err_msg, exc_info=True)
            raise RuntimeError(err_msg)

    # 新增：提取Hive核心错误信息方法
    def extract_core_hive_error(self, err_msg):
        """提取Hive核心错误信息"""
        if not err_msg:
            return "未知Hive错误"

        # 优先从errorMessage提取
        if 'errorMessage="' in err_msg:
            match = re.search(r'errorMessage="([^"]+)"', err_msg)
            if match:
                return match.group(1)

        # 提取SemanticException核心信息
        if 'SemanticException' in err_msg:
            match = re.search(r'SemanticException \[.*?\]: (.*?)(?=:|\n|")', err_msg)
            if match:
                return match.group(1)

        # 保留原始错误的前500个字符作为 fallback
        return err_msg[:500] + ("..." if len(err_msg) > 500 else "")


    # -------------------------- 执行SQL查询 --------------------------
    # 修改后的run_sql函数（参数统一为小写，与HiveClient方法对应）
    def run_sql(self, path=None, sql_name=None, method=None, sql_content=None):
        # 参数校验：统一使用小写参数名
        if sql_content is not None:
            if path is not None or sql_name is not None or method is not None:
                error_msg = "参数错误：sql_content不能与path、sql_name、method同时存在"
                self.logger.error(error_msg)
                raise ValueError(error_msg)
            # 仅传入sql_content时默认使用dql方法
            method = "dql"
        else:
            if path is None or sql_name is None:
                error_msg = "参数错误：当不传入sql_content时，必须提供path和sql_name"
                self.logger.error(error_msg)
                raise ValueError(error_msg)
            # 未指定方法时默认使用dql
            if method is None:
                method = "dql"
            # 校验方法合法性（统一转为小写处理）
            method = method.lower()
            if method not in ["dml", "dmls", "dql", "dqls"]:
                error_msg = f"参数错误：不支持的方法'{method}'，支持的方法为dml、dmls、dql、dqls"
                self.logger.error(error_msg)
                raise ValueError(error_msg)

        # 读取SQL内容
        if sql_content is not None:
            sql = sql_content
            sql_file_path = "[直接传入的SQL内容]"
            self.logger.info(f"使用直接传入的SQL内容，长度：{len(sql)}字符")
        else:
            sql_file_path = os.path.join(path, sql_name)
            # self.logger.info(f"准备执行SQL文件：{sql_file_path}")
            # print(f"准备执行SQL文件：{sql_file_path}")

            try:
                with open(sql_file_path, encoding='utf-8') as sql_file:
                    sql = sql_file.read()
                self.logger.info(f"SQL文件内容读取成功，长度：{len(sql)}字符")
            except FileNotFoundError:
                error_msg = f"SQL文件不存在：{sql_file_path}"
                self.logger.error(error_msg)
                raise FileNotFoundError(error_msg)
            except Exception as e:
                error_msg = f"读取SQL文件失败：{str(e)}"
                self.logger.error(error_msg)
                raise

        # 清洗SQL（保留换行符用于语法分析）
        def clean_sql(raw_sql):
            # 移除单行注释但保留换行结构，避免破坏语法
            lines = []
            for line in raw_sql.split('\n'):
                comment_idx = line.find('--')
                if comment_idx != -1:
                    line = line[:comment_idx]
                line = line.strip()
                if line:
                    lines.append(line)
            # 用空格替换制表符，合并连续空格，但保留语句间的空格分隔
            cleaned = ' '.join(lines).replace('\t', ' ')
            return re.sub(r'\s+', ' ', cleaned).strip()

        cleaned_sql = clean_sql(sql)
        self.logger.info(f"清洗后SQL长度：{len(cleaned_sql)}字符")

        try:
            # 替换日期变量
            original_sql = cleaned_sql
            cleaned_sql = self.replace_day(cleaned_sql, 0)
            self.logger.info(f"已替换SQL中的日期变量")

            # 分号处理逻辑（精细化处理）
            cleaned_sql = cleaned_sql.strip()
            statements = []

            if method == "dml":
                # 单条DML语句：严格校验只能有一条语句
                statements = [stmt.strip() for stmt in re.split(r';+', cleaned_sql) if stmt.strip()]
                if len(statements) > 1:
                    raise ValueError(f"DML方法只支持单条语句，但检测到{len(statements)}条语句，请检查SQL中的分号")
                cleaned_sql = statements[0] if statements else ''
                # 单条DML可省略分号，Hive会自动处理
                self.logger.info(f"DML分号处理完成，单条语句（长度：{len(cleaned_sql)}）")

            elif method == "dmls":
                # 多条DML语句：确保每条语句正确分隔
                statements = [stmt.strip() for stmt in re.split(r';+', cleaned_sql) if stmt.strip()]
                if not statements:
                    raise ValueError("DMLS方法未检测到有效SQL语句")
                # 用分号连接并在末尾加一个分号
                cleaned_sql = ';'.join(statements) + ';'
                self.logger.info(f"DMLS分号处理完成，共{len(statements)}条语句")

            elif method == "dql":
                # 单条DQL查询：移除所有分号
                cleaned_sql = re.sub(r';+', '', cleaned_sql).strip()
                if not cleaned_sql:
                    raise ValueError("DQL方法未检测到有效查询语句")
                self.logger.info(f"DQL分号处理完成，单条查询语句")

            elif method == "dqls":
                # 多条DML+最后一条DQL：严格控制分号位置
                statements = [stmt.strip() for stmt in re.split(r';+', cleaned_sql) if stmt.strip()]
                if len(statements) < 1:
                    raise ValueError("DQLS方法至少需要包含一条语句")
                # 前N-1条DML加回分号，最后一条DQL不加
                cleaned_sql = ';'.join(statements[:-1]) + (';' if len(statements) > 1 else '') + statements[-1]
                self.logger.info(f"DQLS分号处理完成，共{len(statements)}条语句（前{len(statements) - 1}条DML，最后1条DQL）")

            self.logger.info(f"开始连接Hive服务器（地址：172.20.2.190:10023）")
            hive_client = HiveClient.HiveClient('172.20.2.190', 10023, 'cc_yingxiao', 'e147bbed39c810e32f7842cf5f59b9ae')
            try:
                self.logger.info(f"Hive连接成功，开始执行SQL：{sql_file_path}（方法：{method}）")
                print(f"开始执行 {method} 操作：{sql_file_path}")

                # 方法映射：与HiveClient的小写方法名对应
                if method == "dml":
                    hive_client.dml(cleaned_sql)
                    self.logger.info(f"{method}执行成功：{sql_file_path}")
                    print(f"{method}操作：{sql_file_path} 执行完成")
                    return None

                elif method == "dmls":
                    hive_client.dmls(cleaned_sql)
                    self.logger.info(f"{method}执行成功：{sql_file_path}")
                    print(f"{method}操作：{sql_file_path} 执行完成")
                    return None

                elif method == "dql":
                    data = hive_client.pd_dql(cleaned_sql)
                    row_count = len(data) if isinstance(data, pd.DataFrame) and not data.empty else 0
                    self.logger.info(f"{method}执行成功：{sql_file_path}，返回数据行数：{row_count}")
                    print(f"{method}查询：{sql_file_path} 执行完成，返回数据行数：{row_count}")
                    return data

                elif method == "dqls":
                    data = hive_client.pd_dqls(cleaned_sql)
                    row_count = len(data) if isinstance(data, pd.DataFrame) and not data.empty else 0
                    self.logger.info(f"{method}执行成功：{sql_file_path}，返回数据行数：{row_count}")
                    print(f"{method}操作：{sql_file_path} 执行完成，返回数据行数：{row_count}")
                    return data

            finally:
                hive_client.close()
                self.logger.info("Hive连接已关闭")

        except Exception as e:
            sanitized_sql = cleaned_sql[:500] + "..." if len(cleaned_sql) > 500 else cleaned_sql
            full_error_details = repr(e).replace('e147bbed39c810e32f7842cf5f59b9ae', '******')

            # 提取核心错误信息（复用DataProcessingAndMessaging中的方法）
            core_error = self.extract_core_hive_error(full_error_details)

            # 错误信息展示优化
            print(f"\n===== SQL执行失败 =====")
            print(f"时间：{self.get_date_and_time('%Y-%m-%d %H:%M:%S', 0)}")
            print(f"脚本路径：{sql_file_path}")
            print(f"执行方法：{method}")
            print(f"核心错误：{core_error}")
            print(f"========================\n")

            # 日志记录完整信息
            self.logger.error(f"SQL执行失败（来源：{sql_file_path}，方法：{method}）：{str(e)}")
            self.logger.error(f"Hive原始错误详情：\n{full_error_details}")
            self.logger.error(f"执行的SQL语句（脱敏后）：\n{sanitized_sql}")
            raise

    # -------------------------- 写入Excel数据 --------------------------
    def writer_excel_data(self, path, filename, send_file, sheet_data, headers):
        self.logger.info('开始处理Excel表格')
        print('开始处理Excel表格')
        filename = path + filename
        send_file = send_file
        dfs = []
        sheet_names = []
        clear_ranges = []
        date_ranges = []
        for sheet in sheet_data:
            dfs.append(sheet['data'])
            sheet_names.append(sheet['sheet_name'])
            clear_ranges.append(sheet['clear_range'])
            date_ranges.append(sheet['date_range'])

        # 检查文件是否被占用
        if self.is_file_locked(filename):
            error_msg = f"文件被占用，请关闭后重试：{filename}"
            self.logger.error(error_msg)
            raise Exception(error_msg)

        app = None
        try:
            app = xw.App(visible=False, add_book=False)
            app.display_alerts = False
            app.screen_updating = False
            wb = app.books.open(filename)

            for i in range(0, len(dfs)):
                sheet_name = sheet_names[i]
                if sheet_name not in [sheet.name for sheet in wb.sheets]:
                    wb.sheets.add(name=sheet_name)
                wb.sheets[sheet_name].range(clear_ranges[i]).clear_contents()
                wb.sheets[sheet_name].range(date_ranges[i]).options(index=False, header=headers).value = dfs[i]

            wb.save()
            wb.close()
            shutil.copyfile(filename, send_file)
            self.logger.info(f'表格 {os.path.basename(send_file)} 处理完成')
            print(f'表格 {os.path.basename(send_file)} 处理完成')
        except Exception as e:
            self.logger.error(f"Excel处理失败: {str(e)}", exc_info=True)
            raise
        finally:
            # 安全关闭Excel进程
            if app is not None:
                self._safe_quit_excel(app)

    # -------------------------- 检查数据量 --------------------------
    def Yesterday_data_num(self, data, sql_name, columns, num):
        self.logger.info(f'检查{sql_name}表中昨日数据数量')
        print(f'检查{sql_name}表中昨日数据数量')
        df = data[[columns]].copy()
        df = df[~df[columns].isnull()]
        df.loc[:, 'date'] = pd.to_datetime(df[columns]).dt.strftime('%Y/%m/%d')
        df_filter = df[df['date'] == self.get_date_and_time('%Y/%m/%d', 1)]
        df_filter_group = df_filter.groupby(['date']).agg({columns: 'count'}).reset_index(drop=False)
        df_filter_group.rename(columns={columns: '昨日数据量'}, inplace=True)
        df_num = df_filter_group['昨日数据量']

        if pd.isnull(df_filter_group['昨日数据量']).any():
            self.logger.warning(f'警告：数据表 {sql_name} 昨日数据量为0，请尽快检查数据')
            print(f'警告：数据表 {sql_name} 昨日数据量为0，请尽快检查数据')
            self.uxin_wx('dongyang', f'警告：数据表 {sql_name} 昨日数据量为0，请尽快检查数据')
        else:
            df_num_value = df_num.iloc[0] if len(df_num) > 0 else 0
            if df_num_value < num:
                self.logger.warning(f'警告：数据表 {sql_name} 昨日数据量不足{num}，只有{df_num_value}，请尽快检查数据')
                print(f'警告：数据表 {sql_name} 昨日数据量不足{num}，只有{df_num_value}，请尽快检查数据')
                self.uxin_wx('dongyang',
                             f'警告：数据表 {sql_name} 昨日数据量不足{num}，只有{df_num_value}，请尽快检查数据')

    # -------------------------- 获取文件大小（KB） --------------------------
    def get_FileSize(self, img_name):
        fsize = os.path.getsize(img_name)
        fsize = fsize / float(1024)
        return round(fsize, 2)

    # -------------------------- Excel截图（安全版） --------------------------
    def screen(self, filename, sheetname, screen_area, img_name):
        self.logger.info('开始截图')
        print('开始截图')
        pythoncom.CoInitialize()
        app = None
        try:
            # 检查文件是否被占用
            if self.is_file_locked(filename):
                raise Exception(f"文件被占用：{filename}")

            app = xw.App(visible=False, add_book=False)
            app.display_alerts = False
            app.screen_updating = False
            wb = app.books.open(filename)
            sht = wb.sheets[sheetname]
            range_val = sht.range(screen_area)
            range_val.api.CopyPicture()
            sht.api.Paste()
            pic = sht.pictures[0]
            pic.api.Copy()

            # 剪贴板获取图片（带超时）
            img = None
            timeout = 50  # 5秒超时
            while timeout > 0:
                img = ImageGrab.grabclipboard()
                if img is not None:
                    break
                time.sleep(0.1)
                timeout -= 1
            if img is None:
                raise Exception("剪贴板中未获取到图片数据，截图失败")

            if os.path.exists(img_name):
                os.remove(img_name)
            img.save(img_name)
            pic.delete()
            wb.close()

            # 调整图片大小
            def change_size(img_path):
                p_size = self.get_FileSize(img_path)
                if p_size < 101:
                    with Image.open(img_path) as s_img:
                        w, h = s_img.size
                        d_img = s_img.resize((int(w * 1.1), int(h * 1.1)), Image.LANCZOS)
                        d_img.save(img_path)

            change_size(img_name)
            self.logger.info(f'图片：{img_name} 截图并保存完成')
            print(f'图片：{img_name} 截图并保存完成')
        except Exception as e:
            self.logger.error(f"截图失败: {str(e)}", exc_info=True)
            raise
        finally:
            if app is not None:
                self._safe_quit_excel(app)
            pythoncom.CoUninitialize()

    # -------------------------- 列标转换（A,B,C...） --------------------------
    def column_label(self, n):
        result = ""
        while n > 0:
            n, remainder = divmod(n - 1, 26)
            result = chr(65 + remainder) + result
        return result

    # -------------------------- Excel区域截图 --------------------------
    def excel_catch_screen(self, data, path, filename, sheet_name, start_range, image_filename):
        image_path = path + image_filename + '.png'
        self.screen(filename, sheet_name,
                    f"{start_range}:%s" % (self.column_label(len(data.columns)) + str(len(data) + 3)), image_path)

    # -------------------------- 发送邮件（新版） --------------------------
    def send_email_new(self, recipient_emails, cc_emails=None, bcc_emails=None, subject="", html_body="",
                       attachments=None):
        self.logger.info(f"开始发送邮件 - 主题: {subject}")
        self.logger.info(f"收件人: {', '.join(recipient_emails)}")
        if cc_emails:
            self.logger.info(f"抄送: {', '.join(cc_emails)}")
        if bcc_emails:
            self.logger.info(f"密送: {', '.join(bcc_emails) if bcc_emails else '无'}")
        if attachments:
            attach_names = [os.path.basename(att) for att in attachments]
            self.logger.info(f"附件: {', '.join(attach_names)}")

        sender_email = 'cc_yingxiao@xin.com'
        sender_password = 'cw46pfeznNQx'

        try:
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = ', '.join(recipient_emails)
            if cc_emails:
                msg['Cc'] = ', '.join(cc_emails)
            if bcc_emails:
                msg['Bcc'] = ', '.join(bcc_emails)
            msg['Subject'] = subject

            body = MIMEText(html_body, 'html')
            msg.attach(body)

            if attachments:
                for attachment in attachments:
                    if not os.path.exists(attachment):
                        error_msg = f"附件不存在: {attachment}"
                        self.logger.error(error_msg)
                        raise FileNotFoundError(error_msg)

                    with open(attachment, 'rb') as file:
                        part = MIMEApplication(file.read(), Name=os.path.basename(attachment))
                        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment)}"'
                        msg.attach(part)
                    self.logger.debug(f"已添加附件: {os.path.basename(attachment)}")

            with smtplib.SMTP('mail.xin.com', 587, timeout=120) as smtp:
                smtp.login(sender_email, sender_password)
                all_recipients = recipient_emails.copy()
                if cc_emails:
                    all_recipients.extend(cc_emails)
                if bcc_emails:
                    all_recipients.extend(bcc_emails)
                smtp.sendmail(sender_email, all_recipients, msg.as_string())

            self.logger.info(f"邮件发送成功 - 主题: {subject}")

        except Exception as e:
            error_msg = f"邮件发送失败 - 主题: {subject}, 错误: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            raise

    # -------------------------- Excel格式化 --------------------------
    def format_excel_worksheet(self, worksheet, df, workbook):
        date_format = workbook.add_format({
            'num_format': 'yyyy-mm-dd',
            'font_name': '微软雅黑',
            'font_size': 10,
            'border': 1,
            'align': 'center'
        })

        data_format = workbook.add_format({
            'font_name': '微软雅黑',
            'font_size': 10,
            'border': 1,
            'align': 'center'
        })

        header_format = workbook.add_format({
            'font_name': '微软雅黑',
            'font_size': 10,
            'bold': True,
            'bg_color': '#ADD8E6',
            'font_color': 'black',
            'border': 1,
            'align': 'center'
        })

        columns_dtypes = df.dtypes

        def get_char_length(text):
            text = str(text).strip()
            return sum(2 if re.match(r'[\u4e00-\u9fff\uff00-\uffef]', c) else 1 for c in text)

        for col_num, (column_name, col_dtype) in enumerate(zip(df.columns, columns_dtypes)):
            max_data_len = df[column_name].apply(get_char_length).max()
            header_len = get_char_length(column_name)
            max_len = max(max_data_len, header_len) + 2
            worksheet.set_column(col_num, col_num, max_len)

        worksheet.write_row(0, 0, df.columns, header_format)

        max_row, max_col = df.shape
        for row in range(1, max_row + 1):
            for col in range(max_col):
                value = df.iat[row - 1, col]
                col_dtype = columns_dtypes[col]

                if pd.api.types.is_datetime64_any_dtype(col_dtype):
                    if pd.isna(value):
                        worksheet.write_blank(row, col, None, date_format)
                    else:
                        worksheet.write(row, col, value, date_format)
                else:
                    worksheet.write(row, col, value, data_format)

        worksheet.freeze_panes(1, 0)
        worksheet.autofilter(0, 0, max_row, max_col - 1)  # 修正：结束列=max_col-1（比如2）

    # -------------------------- 导出DataFrame到Excel --------------------------
    def export_df_to_excel(self, df_list, sheet_names, file_path):
        new_df_list = []
        for df in df_list:
            df = df.replace([np.inf, -np.inf, np.nan], None)
            new_df_list.append(df)

        writer = pd.ExcelWriter(file_path, engine='xlsxwriter')

        for idx, (df, sheet_name) in enumerate(zip(new_df_list, sheet_names)):
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            worksheet = writer.sheets[sheet_name]
            workbook = writer.book
            self.format_excel_worksheet(worksheet, df, workbook)

        writer.close()
        self.logger.info(f'Excel 文件导出完成: {file_path}')
        print(f'Excel 文件导出完成: {file_path}')

    # -------------------------- 中文转拼音 --------------------------
    def name_to_pinyin(self, name):
        chinese_chars = re.findall(r'[\u4e00-\u9fa5]', name)
        non_chinese_part = re.sub(r'[\u4e00-\u9fa5]', '', name)

        if not chinese_chars:
            return name

        pinyin = ''.join(lazy_pinyin(chinese_chars))
        return pinyin + non_chinese_part

    # -------------------------- 车辆转移任务 --------------------------
    def car_task_transfer(self, df, name_column):
        self.logger.info("开始处理车辆分配任务（使用requests调用API）")
        print("开始处理车辆分配任务（使用requests调用API）")

        try:
            if 'vin' not in df.columns:
                raise ValueError("数据框中缺少必要的'vin'列")
            if name_column not in df.columns:
                raise ValueError(f"数据框中缺少指定的名称列: {name_column}")

            df["name"] = df[name_column].apply(self.name_to_pinyin)
            process_df = df[['vin', 'name']].copy().reset_index()
            self.logger.info(f"成功转换{len(process_df)}条记录")

            today = self.get_date_and_time("%Y-%m-%d", 0)
            self.logger.info(f"当前处理日期: {today}")

            success_count = 0
            fail_count = 0
            for index, row in process_df.iterrows():
                try:
                    api_url = f"http://api-cs.xin.com/super/tool/again_allot_car_task?date={today}&vin={row['vin']}&master_name={row['name']}"
                    headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
                    }
                    response = requests.get(api_url, headers=headers, timeout=10)

                    if response.status_code == 200:
                        success_count += 1
                        self.logger.info(f"第{index + 1}条成功：{row['vin']} 任务分配给{row['name']}")
                    else:
                        fail_count += 1
                        self.logger.error(
                            f"第{index + 1}条失败（状态码：{response.status_code}）：{row['vin']} 任务分配给{row['name']}")

                    time.sleep(2)
                except Exception as e:
                    fail_count += 1
                    self.logger.error(f"第{index + 1}条出错：{str(e)}")

            self.logger.info(f"处理完成 - 成功: {success_count}, 失败: {fail_count}")
            print(f"处理完成 - 成功: {success_count}, 失败: {fail_count}")

        except Exception as e:
            self.logger.error(f"车辆分配处理出错: {str(e)}")
            raise

    # -------------------------- 企微文档：获取Access Token（带重试） --------------------------
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def _wechat_doc_get_access_token(self):
        url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={self.WECHAT_DOC_CORP_ID}&corpsecret={self.WECHAT_DOC_SECRET}"
        try:
            response = requests.get(url, timeout=10)
            result = response.json()
            if result.get("errcode") != 0:
                error_msg = f"获取文档access_token失败: {result.get('errmsg')}"
                self._wechat_doc_log(error_msg)
                raise Exception(error_msg)
            self._wechat_doc_log("成功获取文档access_token")
            return result.get("access_token")
        except Exception as e:
            error_msg = f"获取文档access_token异常: {str(e)}"
            self._wechat_doc_log(error_msg)
            raise

    # -------------------------- 企微文档：刷新Token --------------------------
    def _wechat_doc_refresh_token_if_needed(self):
        if not self.wechat_doc_access_token:
            self.wechat_doc_access_token = self._wechat_doc_get_access_token()
            return

        # 检查token有效性
        test_url = f"https://qyapi.weixin.qq.com/cgi-bin/wedoc/smartsheet/get_sheet?access_token={self.wechat_doc_access_token}"
        test_data = {"docid": "test", "need_all_type_sheet": True}
        try:
            response = requests.post(test_url, json=test_data, timeout=10)
            result = response.json()
            if result.get("errcode") in (40014, 42001):
                self._wechat_doc_log("文档access_token已过期，重新获取")
                self.wechat_doc_access_token = self._wechat_doc_get_access_token()
        except Exception as e:
            self._wechat_doc_log(f"检查token有效性失败，强制刷新: {str(e)}")
            self.wechat_doc_access_token = self._wechat_doc_get_access_token()

    # -------------------------- 企微文档：创建表格 --------------------------
    def wx_create_table(self, sheet_name, admin_users=None):
        self._wechat_doc_log(f"开始创建智能表格：{sheet_name}")
        self._wechat_doc_refresh_token_if_needed()

        url = f"https://qyapi.weixin.qq.com/cgi-bin/wedoc/create_doc?access_token={self.wechat_doc_access_token}"
        data = {
            "spaceid": self.WECHAT_DOC_SPACE_ID,
            "fatherid": self.WECHAT_DOC_SPACE_ID,
            "doc_type": 10,
            "doc_name": sheet_name
        }
        if admin_users:
            data["admin_users"] = admin_users

        try:
            response = requests.post(url, json=data, timeout=10)
            result = response.json()
            if result.get("errcode") != 0:
                error_msg = f"创建失败: {result.get('errmsg')}"
                self._wechat_doc_log(error_msg)
                raise Exception(error_msg)
            docid = result.get("docid")
            # ========== 新增：添加创建时间 ==========
            # 获取当前时间（北京时间，格式：YYYY-MM-DD HH:MM:SS）
            create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # ========== 核心新增：创建成功后自动查询子sheet ==========
            self._wechat_doc_log(f"开始查询新创建表格[{docid}]的子表信息")
            # 然后修改wx_create_table中调用wx_get_sheets的代码，传入send_notice=False：
            sheet_list = self.wx_get_sheets(docid, send_notice=False)

            # ========== 构造包含子sheet的完整消息内容 ==========
            # 基础信息
            msg_content = f"✅ 智能表格创建成功\n表格名称：{sheet_name}\n创建时间：{create_time}\ndocid：{docid}\n\n子表信息："
            # 子sheet信息
            if sheet_list:
                for idx, sheet in enumerate(sheet_list, 1):
                    sheet_visibility = '可见' if sheet['is_visible'] else '不可见'
                    msg_content += f"\n{idx}. ID: {sheet['sheet_id']} | 标题: {sheet['title']} | 类型: {sheet['type']} | 可见性: {sheet_visibility}"
            else:
                msg_content += "\n暂无子表信息"

            self._wechat_doc_log(
                f"智能表格：{sheet_name} 创建成功，docid={docid}，创建时间={create_time}，子表数量：{len(sheet_list)}")
            print(f"智能表格：{sheet_name} 创建成功，docid={docid}，创建时间={create_time}")
            print(f"该表格的子表信息：")
            if sheet_list:
                for idx, sheet in enumerate(sheet_list, 1):
                    sheet_visibility = '可见' if sheet['is_visible'] else '不可见'
                    print(
                        f"  {idx}. ID: {sheet['sheet_id']} | 标题: {sheet['title']} | 类型: {sheet['type']} | 可见性: {sheet_visibility}")
            else:
                print("  暂无子表信息")

            # 调用uxin_wx发送包含子sheet的完整消息
            self.uxin_wx('dongyang', msg_content)

            return {
                "智能表格": sheet_name,
                "docid": docid,
                "url": result.get("url"),
                "创建时间": create_time,
                "子表列表": sheet_list  # 返回值新增子sheet列表
            }
        except Exception as e:
            self._wechat_doc_log(f"创建异常: {str(e)}")
            raise

    # -------------------------- 企微文档：查询子表 --------------------------
    # 修改wx_get_sheets方法的定义，新增send_notice参数
    def wx_get_sheets(self, docid, send_notice=True):
        self._wechat_doc_log(f"查询文档[{docid}]的子表信息")
        self._wechat_doc_refresh_token_if_needed()

        url = f"https://qyapi.weixin.qq.com/cgi-bin/wedoc/smartsheet/get_sheet?access_token={self.wechat_doc_access_token}"
        data = {
            "docid": docid,
            "need_all_type_sheet": True
        }

        response = requests.post(url, json=data, timeout=10)
        result = response.json()

        if result.get("errcode") != 0:
            error_msg = f"查询子表失败: {result.get('errmsg')}"
            self._wechat_doc_log(error_msg)
            # 失败时仍发送通知
            fail_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            fail_content = f"⚠️ 企微文档子表查询失败\n查询时间：{fail_time}\n文档ID：{docid}\n错误信息：{result.get('errmsg')}"
            self.uxin_wx('dongyang', fail_content)
            raise Exception(error_msg)

        sheet_list = result.get("sheet_list", [])
        query_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._wechat_doc_log(f"查询文档[{docid}]子表完成，共找到{len(sheet_list)}个子表")

        # 构造通知内容
        msg_content = f"✅ 企微文档子表查询完成\n查询时间：{query_time}\n文档ID：{docid}\n子表总数：{len(sheet_list)}\n\n子表详细信息："
        if sheet_list:
            for idx, sheet in enumerate(sheet_list, 1):
                sheet_visibility = '可见' if sheet['is_visible'] else '不可见'
                msg_content += f"\n{idx}. ID: {sheet['sheet_id']} | 标题: {sheet['title']} | 类型: {sheet['type']} | 可见性: {sheet_visibility}"
        else:
            msg_content += "\n暂无子表信息"

        # 仅当send_notice为True时发送通知
        if send_notice:
            self.uxin_wx('dongyang', msg_content)

        # 原有日志和打印逻辑
        for sheet in sheet_list:
            sheet_info = (f"子表信息 - ID: {sheet['sheet_id']}, 标题: {sheet['title']}, "
                          f"类型: {sheet['type']}, 可见性: {'可见' if sheet['is_visible'] else '不可见'}")
            self._wechat_doc_log(sheet_info)
            print(f"[企业微信文档] {sheet_info}")

        return sheet_list

    # -------------------------- 企微文档：读取表格数据 --------------------------
    def wx_run_excel(self, docid, sheet_id):
        self._wechat_doc_log(f"开始读取文档[{docid}]子表[{sheet_id}]的记录到dataframe")
        self._wechat_doc_refresh_token_if_needed()

        url = f"https://qyapi.weixin.qq.com/cgi-bin/wedoc/smartsheet/get_records?access_token={self.wechat_doc_access_token}"
        data = {
            "docid": docid,
            "sheet_id": sheet_id,
            "key_type": "CELL_VALUE_KEY_TYPE_FIELD_TITLE",
            "limit": 1000,
            "offset": 0
        }

        all_records = []
        has_more = True
        while has_more:
            response = requests.post(url, json=data, timeout=10)
            result = response.json()
            if result.get("errcode") != 0:
                error_msg = f"查询记录失败: {result.get('errmsg')}"
                self._wechat_doc_log(error_msg)
                raise Exception(error_msg)
            records = result.get("records", [])
            all_records.extend(records)
            has_more = result.get("has_more", False)
            data["offset"] = result.get("next", 0)

        if not all_records:
            msg = f"文档[{docid}]子表[{sheet_id}]没有找到记录，无需导出"
            self._wechat_doc_log(msg)
            print(f"[企业微信文档] {msg}")
            return pd.DataFrame()

        # 时间转换工具
        def _unified_time_convert(value):
            if value is None or str(value).strip() in ["", "None", "nan"]:
                return ""

            if isinstance(value, dict) and value.get("type") == "DateTimeFieldProperty":
                ts = value.get("value")
                if isinstance(ts, (int, float)):
                    return _timestamp_to_beijing(ts)
                else:
                    self._wechat_doc_log(f"DateTimeFieldProperty时间戳非数字：{value}")
                    return str(value)

            elif isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
                nested_dict = value[0]
                if nested_dict.get("type") == "DateTimeFieldProperty":
                    ts = nested_dict.get("value")
                    if isinstance(ts, (int, float)):
                        return _timestamp_to_beijing(ts)
                    else:
                        self._wechat_doc_log(f"嵌套DateTimeFieldProperty时间戳非数字：{value}")
                        return str(value)
                elif "text" in nested_dict:
                    text_val = nested_dict["text"]
                    return _extract_and_convert_ts(text_val)
                else:
                    return str(nested_dict.get("title", nested_dict.get("text", str(value))))

            else:
                return _extract_and_convert_ts(str(value))

        def _timestamp_to_beijing(timestamp):
            try:
                ts = int(timestamp)
                if len(str(ts)) == 10:
                    ts *= 1000
                utc_dt = datetime.datetime.utcfromtimestamp(ts / 1000)
                beijing_dt = utc_dt + datetime.timedelta(hours=8)
                return beijing_dt.strftime("%Y-%m-%d %H:%M:%S")
            except (ValueError, OverflowError) as e:
                self._wechat_doc_log(f"时间戳转换失败（值：{timestamp}），错误：{str(e)}")
                return str(timestamp)

        def _extract_and_convert_ts(raw_text):
            ts_match = re.search(r"\d{10,13}", raw_text)
            if ts_match:
                ts = ts_match.group()
                return _timestamp_to_beijing(ts)
            else:
                return raw_text

        # 处理记录
        rows = []
        custom_fields = set()
        for record in all_records[:1]:
            if record.get("values"):
                custom_fields = set(record["values"].keys())
                break
        all_fields = ["记录ID", "创建时间", "更新时间", "最后编辑者"] + list(custom_fields)
        date_related_columns = [col for col in all_fields if any(kw in str(col) for kw in ["日期", "时间"])]
        self._wechat_doc_log(f"识别到需转换的日期相关列：{date_related_columns}")

        for record in all_records:
            row = {
                "记录ID": record.get("record_id"),
                "创建时间": _unified_time_convert(record.get("create_time")),
                "更新时间": _unified_time_convert(record.get("update_time")),
                "最后编辑者": record.get("updater_name")
            }

            values = record.get("values", {})
            for field_name, field_value in values.items():
                if field_name in date_related_columns:
                    row[field_name] = _unified_time_convert(field_value)
                else:
                    if isinstance(field_value, list) and len(field_value) > 0:
                        if isinstance(field_value[0], dict):
                            row[field_name] = field_value[0].get("text",
                                                                 field_value[0].get("title", str(field_value[0])))
                        else:
                            row[field_name] = str(field_value)
                    else:
                        row[field_name] = str(field_value) if field_value is not None else ""

            rows.append(row)

        df = pd.DataFrame(rows)
        df = df[df['更新时间'] != '0']

        msg = f"成功读取{len(rows)}条记录到dataframe（{len(date_related_columns)}个日期相关列已转为北京时间）"
        self._wechat_doc_log(msg)
        print(f"[企业微信文档] {msg}")

        return df

    # -------------------------- 企微文档：删除表格 --------------------------
    def wx_delete_table(self, docid):
        self._wechat_doc_log(f"开始删除文档：docid={docid}")
        self._wechat_doc_refresh_token_if_needed()

        url = f"https://qyapi.weixin.qq.com/cgi-bin/wedoc/del_doc?access_token={self.wechat_doc_access_token}"
        data = {"docid": docid}

        response = requests.post(url, json=data, timeout=10)
        result = response.json()

        if result.get("errcode") != 0:
            error_msg = f"删除文档失败: {result.get('errmsg')}"
            self._wechat_doc_log(error_msg)
            raise Exception(error_msg)

        # 获取当前时间（北京时间，格式：YYYY-MM-DD HH:MM:SS）
        create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg_content = f"企微文档删除成功：docid={docid} \n 删除时间：{create_time}"
        self._wechat_doc_log(msg_content)
        print(msg_content)
        self.uxin_wx('dongyang', msg_content)
        return True

    # -------------------------- 辅助方法：检查文件是否被占用 --------------------------
    def is_file_locked(self, file_path):
        if not os.path.exists(file_path):
            return False
        try:
            with open(file_path, 'a', encoding='utf-8') as f:
                pass
            return False
        except IOError:
            return True

    # -------------------------- 辅助方法：安全关闭Excel进程 --------------------------
    def _safe_quit_excel(self, app):
        """安全关闭Excel进程，优化时序检查逻辑"""
        try:
            pid = app.pid
            # 先尝试正常退出
            app.quit()

            # 增加短暂延迟，等待进程自然退出（解决时序问题）
            time.sleep(0.5)

            # 检查进程是否还存在
            if psutil.pid_exists(pid):
                # 尝试优雅终止
                proc = psutil.Process(pid)
                proc.terminate()  # 发送终止信号

                # 等待进程退出，最多等待3秒
                try:
                    proc.wait(timeout=3)
                    self.logger.debug(f"Excel进程（PID: {pid}）已被强制终止")
                except psutil.TimeoutExpired:
                    # 超时后强制杀死进程
                    proc.kill()
                    self.logger.debug(f"Excel进程（PID: {pid}）超时未退出，已强制杀死")
            else:
                # 进程已正常退出，不记录警告
                self.logger.debug(f"Excel进程（PID: {pid}）已正常退出")

        except psutil.NoSuchProcess:
            # 进程在检查前已退出，属于正常情况，不记录警告
            self.logger.debug(f"Excel进程已提前退出（PID: {pid}）")
        except Exception as e:
            # 其他未知错误才记录警告
            self.logger.warning(f"关闭Excel进程时发生异常: {str(e)}")


# 使用示例
if __name__ == "__main__":
    # 实例化 DataProcessingAndMessaging 类
    ux = DataProcessingAndMessaging()
    for method_name in dir(ux):
        if not method_name.startswith("__"):
            globals()[method_name] = getattr(ux, method_name)
    # 开始运行脚本，这将设置路径，确保 path和 current_script_name已被正确赋值
    Start_Get_filepath_and_filename()
    path = ux.path
    current_script_name = ux.current_script_name
    # 开启多线程
    # pythoncom.CoInitialize()

    # 示例：发送企业微信消息
    # dp.uxin_wx("dongyang", "测试消息")

    # 示例：执行SQL查询
    # sql = "SELECT * FROM test_table LIMIT 10"
    # result = dp.run_sql(sql_content=sql)
    # print(result)

    # 示例：导出Excel
    # df = pd.DataFrame({"col1": [1, 2], "col2": ["a", "b"]})
    # dp.export_df_to_excel([df], ["测试表"], "test.xlsx")

    # pythoncom.CoUninitialize()
    End_operation()  # 结束运行脚本