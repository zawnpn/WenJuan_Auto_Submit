# WenJuan_Auto_Submit
*问卷星自动提交*

## 配置

使用前，需要修改以下配置：

- `QUESTION_ID`：问卷网址里面的数字
- `QUESTION_URL`、`POST_URL_MAP`、`UPMULT_MULT_URL`：有的问卷是.cn域名后缀，有的是.top域名后缀，学校给的问卷是.cn后缀，但你自己注册一个问卷星用于测试的话，应该会是.top后缀，所以需要根据你要使用的问卷地址做调整（只需改这个域名后缀，别的都不用改）。后面两个URL请跟`QUESTION_URL`保持为相同的域名后缀，其他地方都不需要改。
- `PIC_NAME`：第7问需要提交的图片名称（请同时在`auto_submit_wjx.py`的相同目录下附上这张图片）
- `PIC_PATH`：上述图片的**绝对路径**（注意尽量要填绝对路径，这是防止出现一些bug）
- `ANSWER`：对应问卷的6处需要填写的答案（第7问的图片会自动上传，第8问的时间会自动提交为目前时间的后一天），具体的填写指导见下表

| ANSWER数组的元素 | 含义                                       | 示例            |
| ---------------- | ------------------------------------------ | --------------- |
| 第1项            | 姓名                                       | `'张三'`        |
| 第2项            | 手机                                       | `'130XXXXXXXX'` |
| 第3项            | 学号                                       | `'2019211XXX'`  |
| 第4项            | 接收出校许可的邮箱                         | `'xxx@xxx.com'` |
| 第5项            | 是否返校14天的选项（`1`代表是，`2`代表否） | `'1'`           |
| 第6项            | 出校理由                                   | `'外出实习'`    |

另外，为了确保让你得知本程序已正常运行，在本程序成功执行后会立即发送一封邮件告知你，以便提交失败后进行手动提交，因此需要额外填写你的收发邮件的信息：

```python
from_addr = '' # 你的发件邮箱地址 e.g. send@xxx.com
password = '' # 你的发件邮箱密码 e.g. password
to_addr = '' # 你的接收通知的邮箱地址 e.g. recv@xxx.com
smtp_server = '' # 你的发件邮箱的smtp服务器地址 e.g. smtp.xxx.com
```

（如不需要上述功能，请注释掉129-134行）

## 如何自动化运行

请配合linux的`crontab`命令使用，教程可参考[Linux Crontab 定时任务](https://www.runoob.com/w3cnote/linux-crontab-tasks.html)

示例：

```shell
30 10 * * 0-5 /usr/bin/python /path/to/auto_submit_wjx.py > /dev/null 2>&1
```

上述范例的含义是：每周日到每周五 的 10点30分 执行一次本程序

## Tips

建议先自己注册一个问卷星用于测试，可以在问卷星后台查看提交情况，确认无误后再正式用于学校的问卷。

请勿滥用。