import os
from load_table import LoadTable
# from export_log import Logger

class Content2File():
    """
    写入文件
    """

    def __init__(self, user_pick=1):
        self.user_pick = user_pick
        self.path = self.get_path()
    
    def get_path(self) -> str:
        """
        根据用户选择,获取文件路径
        :param user_pick: 用户选择 1:桌面 2:当前路径 3:自定义路径(绝对路径)
        :return: path: str
        """
        if self.user_pick == 1:
            path = os.path.join(os.path.expanduser("~"), "Desktop")
        elif self.user_pick == 2:
            path = os.getcwd()
        elif self.user_pick == 3:
            path = input("请输入路径:")
        else:
            path = os.path.join(os.path.expanduser("~"), "Desktop")
        return path
    
    def write(self, content, export_path, user_pick=1):
        """
        将获取的对话信息写入文件，默认生成文件类型为markdown
        :param content: 对话信息 {key:[(),(),...]}
        :param export_path: 导出路径
        :param logged_time: 日志中记录的最新时间
        :param user_pick: 用户选择文件类型, 1:md, 2:txt
        :return:
        """
        if user_pick == 1:
            file_type = "md"
        elif user_pick == 2:
            file_type = "txt"
        else:
            file_type = "md"
        
        for filename, file_content in content.items():
            _, _time = LoadTable().getLastTime(filename)
            file_path = os.path.join(export_path, f"{filename}({_time}).{file_type}")
            prompt = LoadTable().getPrompt(filename)

            # title_count = LoadTable().titleCount(title=filename, start_time=logged_time).get(filename)
            # log_dict = {"timestamp": _timestamp, "total": title_count, "time": _time, "abs_path": file_path}

            with open(file_path, "w", encoding="utf-8") as f:
                f.write("**" + prompt + "**" + "\n\n")
                for save_content in file_content:
                    role = save_content[0].replace('user', '❓:').replace('assistant', '🤖:\n\n')
                    f.write(role)
                    f.write(save_content[1] + "\n")
            
            # 记录日志
            # Logger.log(title=filename, log_text=log_dict)
        # Content2File().writeLog(content, log_dict)
        return file_type


    # def writeLog(self, title, export_path, logged_time, file_type):
    #     log_dict = dict()
    #     _timestamp, _time = LoadTable().getLastTime(title)
    #     title_count = LoadTable().titleCount(title=title, start_time=logged_time).get(title)
    #     file_path = os.path.join(export_path, f"{title}({_time}).{file_type}")
    #     log_dict.update({"timestamp": _timestamp, "total": title_count, "time": _time, "abs_path": file_path})
        
    #     Logger.log(title=title, log_text=log_dict)
    #     return 
    


def main():
    lt = LoadTable()
    # res = lt.titleCount()
    kwargs = {"Apple Script":'1694234876723',}
    sql = lt.sqlQuery(**kwargs)
    content = lt.getContent(sql)
    print(list(content)[0])
    # print(lt.titleCount("Apple Script", '1694234876723'))
    # Content2File().write(content, '/Users/zhangzhexiang/Desktop')



if __name__ == "__main__":
    main()