# 做的原因
看了【败犬女主太多了】实在是仙品，太青春了，特别是八奈见杏菜，她散发的青春气息真是给我看emo了，晚上躺在床上回忆自己是否的青春记忆中是否有这样的女孩，实在是夜不能寐，这个时候突然灵光一现

"诶，我可以做一个每天自动发邮件的脚本来模仿八奈见同学发邮件给我诶"

遂起床开始
# py邮件发送脚本
这个其实很简单，随便做做就可以了

我使用的是SMTP服务，并且使用的是QQ邮箱来发送的邮件，我们就直接用py中的`email库和smtplib来就可以了`

## 处理基本的发送
发送的代码如下
```python
def email_send():
    smtp_server = 'smtp.qq.com'  # 邮箱服务器
    smtp_port = 465  # 邮箱端口
    smtp_ssl = True  # 启用ssl
    smtp_user = ''# 发送者邮箱
    smtp_password = ''  # 邮箱授权码，到邮箱网站中查看

    # 发送邮件信息
    sender = ''  # 发送者邮箱
    receivers = ''  # 接收者邮箱
    
    message = MIMEMultipart('related')
    message['From'] = formataddr(["八奈见杏菜", sender])
    message['To'] = formataddr(["顿感怪", receivers])
    message['Subject'] = Header(heeder, 'utf-8')  # 邮件标题
    
    mail_content = f"""
    <html>
    <body>
        <p>{ans}</p>
    </body>
    </html>
    """
    message.attach(MIMEText(mail_content, 'html', 'utf-8'))
    
    # 发送邮件
    try:
        smtp_obj = smtplib.SMTP_SSL(smtp_server, smtp_port)  # 连接服务器
        smtp_obj.login(smtp_user, smtp_password)  # 登入发送者邮箱
        smtp_obj.sendmail(sender, receivers, message.as_string())  # 发送邮件指令
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print("Error: 邮件发送失败: ", e)
```
## 发送图片的功能
诶但是这样只有文字感觉味不对

所以我就在加上发送图片的功能
```python
    # 邮件正文
    mail_content = f"""
    <html>
    <body>
        <img src="cid:image1">
        <p>{ans}</p>
    </body>
    </html>
    """
    message.attach(MIMEText(mail_content, 'html', 'utf-8'))
    num = random.randint(1,18)
    # 添加图片到正文中
    image_path = './image/'  # 图片路径
    image_path += str(num)
    image_path += '.png'
    try:
        with open(image_path, 'rb') as img_file:
            img_data = img_file.read()
            image = MIMEImage(img_data)
            image.add_header('Content-ID', '<image1>')
            message.attach(image)
    except Exception as e:
        print(f"Error: 无法读取图片: {e}")
```
因为我是通过html格式来规划邮件格式的，所以我们只用在`<body>`加上
```html
<img src="cid:image1">
```
就可以了

然后再把`<image1>`去对应资源就OK了

~~**又有理由重新看一遍漫画**~~

## 处理发送频率
那发送总要有个频率把，我打算一天发一封，但是这要怎么做到呢？

诶，于是我一想，创建了一个文本来存
```day.txt
8
3
```
表示上一次发是8月3号

我们每次运行这个脚本的时候就看看day中的是不是今天是的话就跳过
```python
def check_date_and_update():
    # 读取day.txt中的内容
    try:
        with open('day.txt', 'r') as file:
            lines = file.readlines()
            file_month = int(lines[0].strip())
            file_day = int(lines[1].strip())
    except Exception as e:
        print(f"Error reading day.txt: {e}")
        file_month, file_day = None, None

    # 判断当前日期和文件中的日期是否相同
    if file_month == current_month and file_day == current_day:
        print("今天已经发过了.")
        return  # 跳出函数

    # 如果日期不同，则继续执行email_send并更新day.txt
    email_send()  # 调用你的email_send函数

    # 更新day.txt中的内容
    try:
        with open('day.txt', 'w') as file:
            file.write(f"{current_month}\n{current_day}\n")
        print("日期更新.txt")
    except Exception as e:
        print(f"Error writing to day.txt: {e}")
```
这样应该就ok了
# 文本获取
OK啊，来到最难的地方了，就是发送过来的邮件文本，这个让我苦恼了好一会要怎么实现，其实一开始我是想用接大模型的api接口来实现文本的随机的，但是发现不理想，但是这个时候灵光一现，诶，我可以用随机组合的方式来实现

就是句子通过特点的形式来组合
```text
今天去吃东西吗？
<fat> <loseweight> <eat>
```
元素就这样写
```text
<eat>
好了好了，今天去哪里吃，走吧走嘛？
```

于是我又花了很多时间阅读原文，写她可能会说的话并且分类~~(花了巨久的时间)~~

然后写了个c++程序读取，因为我py真的菜的要死
```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long

unordered_map<int,vector<string>> header;
unordered_map<string,vector<string>> element;

struct ok{
    string ans;
    string heeder;
};

ok get(){
    ifstream inh("Header.b");
    ifstream ine("element.b");
    srand((int)time(0));
    string s;
    int num1 = 0;
    while(getline(inh,s)){
        if(s == "") continue;
        int num = stoi(s);
        string now;
        for(int i = 1;i <= num; i++){
            getline(inh,now);
            header[num1].push_back(now);
        }
        num1++;
    }
    while(getline(ine,s)){
        if(s == "") continue;
        string now;
        getline(ine,now);
        int num = stoi(now);
        getline(ine,now);
        int size = stoi(now);
        for(int i = 1; i <= num-1; i++){
            getline(ine,now);
            element[s].push_back(now);
        }
        while(element[s].size() < size){
            element[s].push_back("");
        }
    }
    int nh = rand()%header.size();
    string str = header[nh][header[nh].size()-1];
    int wok = rand()%(header[nh].size()-1);
    string head = header[nh][wok];
    istringstream iss(str);
    string token;
    string ans = "";
    while (getline(iss, token, ' ')){
        int r = rand()%element[token].size();
        ans += element[token][r];
    }
    return {ans,head};
}

signed main(){
    ok now = get();
    cout << now.heeder << "\n" << now.ans << "\n";
}
```
# 把脚本挂上去
本来是想买个服务器把脚本挂上去的，但是发现好像有点贵，而且为了挂一个小脚本去买服务器感觉很亏，所以我最终把它挂到了我的电脑上

在任务计划程序中创建一个任务就ok了(用cmd输入`taskschd.msc`就可以看到)，设置为在启动时执行就可以了

注意要设置为
1. 不管用户是否登录都要运行
2. 在操作哪里放脚本(.bat)的路径不能有中文，而且要设置起源与(设置为脚本所在的目录)
然后就可以

但是我们要检测是否联网,连接了才可以发邮件，于是
```bat
@echo off
:loop
ping -n 1 www.bilibili.com >nul
if %errorlevel%==0 (
    echo Network is up.
    python "./send.py"
    exit /b
) else (
    echo Network is down, checking again in 1 minute...
    timeout /t 60
    goto loop
)
```
这样就可以达成目的了
# 成果
然后经过我两天的奋战，这个下头脚本终于做好了
![](image/f122632de0e33ea2e481185558d8c57.jpg)
![](image/0a38e17c272acaba3f6ca5f59f83eb7.jpg)
