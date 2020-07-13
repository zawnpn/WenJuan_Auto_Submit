from requests_html import HTMLSession
import time
from datetime import datetime, date, timedelta
from random import randint, sample
import string
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

QUESTION_ID = 83987227
QUESTION_URL = 'https://www.wjx.cn/jq/%s.aspx' % QUESTION_ID
POST_URL_MAP = "https://www.wjx.cn/joinnew/processjq.ashx?submittype=1&curID={}&t={}&starttime={}&rn={}"
UPMULT_URL = 'https://www.wjx.cn/wjx/join/uploadMultiple.aspx?activity=%s&q=7&ms=4096&length=1' % QUESTION_ID
UPPIC_URL = 'https://wjx-z0.qiniup.com/'
PIC_NAME = 'upload.png'
PIC_PATH = '/home/xxx/upload.png'
ANSWER = [ # 问卷的具体答案
    '姓名',
    '手机',
    '学号',
    '邮箱',
    '选项1',
    '理由'
]
from_addr = ''
password = ''
to_addr = ''
smtp_server = ''

def parse_post_url(resp):
    '''
    解析出提交问卷的url
    '''
    # 找到rn
    rn = int(resp.html.search('rndnum="{}"')[0].split('.')[0])
    # 提交问卷的时间
    raw_t = round(time.time(), 3)
    t = int(str(raw_t).replace('.', ''))
    # 模拟开始答题时间
    starttime = datetime.fromtimestamp(
        int(raw_t) - randint(1, 60 * 3)).strftime("%Y/%m/%d %H:%M:%S")

    url = POST_URL_MAP.format(QUESTION_ID, t, starttime, rn)
    return url

def parse_pic_data(resp):
    '''
    解析第7问上传图片的data
    '''
    up_token = resp.html.search('token = "{}"')[0]
    up_dir = resp.html.search("dir = '{}'")[0]
    raw_t = round(time.time(), 0)
    t = str(raw_t).replace('.', '')
    salt = ''.join(sample(string.ascii_letters + string.digits, 6))
    suffix = PIC_NAME.split('.')[1]
    fname = up_dir + t + salt + '.' + suffix
    pic_file = {
        'file':(PIC_NAME, open(PIC_PATH, 'rb'), 'image/' + suffix, {})
    }
    pic_data = {
        'name': PIC_NAME,
        'key': fname,
        'token': up_token
    }
    return pic_data, pic_file, fname

def form_post_data(resp):
    '''
    构造要post的data
    '''
    tomorrow = str(date.today() + timedelta(days=1))
    a = ANSWER
    size = resp.html.search('"size":"{}"')[0]
    name = resp.html.search('"name":"{}"')[0]
    key = resp.html.search('"key":"{}"')[0]
    pic_info = '%s,%s,%s' % (key,size,name)
    data = {
        'submitdata': '1$%s}2$%s}3$%s}4$%s}5$%s}6$%s}7$%s}8$%s' % (
            a[0],
            a[1],
            a[2],
            a[3],
            a[4],
            a[5],
            pic_info, 
            tomorrow
        )
    }
    return data

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def send_notification(success=True):
    if success:
        subject = '「出校申请已自动提交」'
        text = '当日出校申请已自动提交，请注意查收出校凭证。'
    else:
        subject = '「出校申请提交失败！」'
        text = '当日出校申请提交失败，请手动提交：https://www.wjx.cn/m/83987227.aspx'
    msg = MIMEText(text, 'plain', 'utf-8')
    msg['From'] = _format_addr('Bot <%s>' % from_addr)
    msg['To'] = _format_addr('User <%s>' % to_addr)
    msg['Subject'] = Header(subject, 'utf-8').encode()

    server = smtplib.SMTP(smtp_server, 25)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()
    
def main():
    session = HTMLSession()
    
    # 打开页面
    resp = session.get(QUESTION_URL)
    post_url = parse_post_url(resp)
    # 上传图片
    resp = session.get(UPMULT_URL)
    pic_data, pic_file, fname = parse_pic_data(resp)
    resp = session.post(UPPIC_URL, data=pic_data, files=pic_file)
    # 提交问卷
    post_data = form_post_data(resp)
    r = session.post(post_url, post_data)
    
    # 若不需要发邮件功能，请注释掉下面几行
    if r.status_code == 200:
        send_notification()
        print('Success.')
    else:
        send_notification(False)
        print('Failed!')
        
if __name__ == '__main__':
    main()