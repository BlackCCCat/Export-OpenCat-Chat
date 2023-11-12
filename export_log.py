import logging
import os
import re
import json

from load_table import LoadTable

class Logger:
    def __init__(self, title):
        self.logger = logging.getLogger(title)
        if not self.logger.handlers:
            self.configure_logging()
        self.title = title

    def configure_logging(self):
        """
        生成日志配置
        """        
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler = logging.FileHandler('export.log')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def log(self, log_text):
        """
        记录日志，包含每个对话的标题、导出时间、已导出对话的最新时间、导出条数、导出位置
        :param log_text: 记录的日志信息（已导出对话的最新时间、导出条数），格式为JSON字符串
        :return None
        """
        # 记录日志
        self.logger.info(json.dumps(log_text, ensure_ascii=False))
        return
    
    def writeLog(self, export_path, logged_time, file_type):

        log_dict = dict()
        _timestamp, _time = LoadTable().getLastTime(self.title)
        title_count = LoadTable().titleCount(title=self.title, start_time=logged_time).get(self.title)
        file_path = os.path.join(export_path, f"{self.title}({_time}).{file_type}")
        log_dict.update({"timestamp": _timestamp, "total": title_count, "time": _time, "abs_path": file_path})
        
        self.log(log_dict)
        return 
    
    def readLog(self) -> dict:
        """
        读取已有日志，找到对应title的已导出对话的最大时间，以便再次导出时，不重复导出
        :param title: 标题
        :return title_dict: dict
        """
        log_dict = dict()

        with open("export.log", "r", encoding="utf-8") as f:
            log_text = f.readlines()

            if log_text:
                regex = '(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - (%s) - (.*) - (.*)' % self.title
                for line in log_text:
                    re_res = re.match(regex, line)
                    if re_res:
                        res_title = re_res.group(2)
                        res_txt = re_res.group(4)
                        log_dict.update({res_title: res_txt})

                    if not log_dict.get(self.title):
                        res_title = self.title
                        res_txt = '{"timestamp": 0}'
                        log_dict.update({res_title: res_txt})

                    # log_dict.update({name: res_txt})
                return json.loads(log_dict[res_title])



def main():
    log_dict = Logger('英语单词释义').readLog()
    # print(log_dict)
    # value_of_title = json.loads(log_dict['SQL'])
    try:
        _timestamp = log_dict['timestamp']
        print(_timestamp)
        print(log_dict)
    except:
        pass

if __name__ == "__main__":
    main()