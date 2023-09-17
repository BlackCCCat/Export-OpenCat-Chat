# OpenCat 对话记录导出工具

该项目用于在Mac上导出OpenCat的对话记录，输出为markdown格式文件，文件名称为`[对话标题(最后对话时间)].md`

文件内容格式大致如下：
```markdown
**prompt**
> (yyyy-mm-dd HH:MM:SS)❓: 你的提问
(yyyy-mm-dd HH:MM:SS)🤖:
AI的回答
> (yyyy-mm-dd HH:MM:SS)❓: 你的提问
(yyyy-mm-dd HH:MM:SS)🤖:
AI的回答
...
```

# 功能
- 对单个对话进行操作
- 对所有对话进行操作
- 可以根据上次导出的记录导出最新未导出的对话，避免重复导出
- 可以选择重新导出所有对话，即使上次已经导出部分对话内容
- 指定导出路径
    - 默认桌面
    - 可选当前路径
    - 手动输入其他路径（绝对路径）
- 提供简单的导出情况日志

# 使用
## 所需环境

需要Python3，所使用应该都是Python自带包，无需下载其他第三方包，如果有报包或者模块不存在，请直接使用`pip`下载

## 下载源码

```shell
cd [your path]
git clone https://github.com/BlackCCCat/Export-OpenCat-Chat.git
```
`[your path]`换成你要放置项目脚本的路径
## 开始使用
在`[your path]`中打开终端：
- 一次导出所有对话
```Python
python start_all.py
```
根据终端输出信息操作即可

- 一次导出一个对话

```Python
python start.py
```
根据终端输出信息操作即可

# 注意事项
- 尽量根据终端输出信息输入正确的操作选项
- 欢迎使用及指出代码的各种问题，帮助我进步，感谢