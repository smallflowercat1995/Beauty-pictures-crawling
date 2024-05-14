# 思路
'''
    在脚本所在目录下创建 美女图集 文件夹，存在则忽略，并进入文件夹,创建重试函数，为了规避网络问题导致的 tls 报错，并且使用脚本实现需求
    
    定义 url 为 https://www.2488.one/
    拼接 url 和 c49.aspx 得到 a_url
    请求 a_url 若为 200 且有内容则返回 a_content
    
    从 a_content 中的 <div class="pager"></div> 中获得 倒数第3个<li></li> 元素并获取文本值为总页数 a_pager

    从 1 开始循环便利总页数到 a_pager 范围 [1,a_pager+1]
    当为 1 则直接使用 a_content 赋值给 a_pager_content
    当不为 1 则处理 a_url 将结尾类似 c49.aspx 的部分中 .aspx 去掉，得到 a_url_cut 用于后续拼接 
    拼接 a_url_cut 和 a_pager 得到类似 https://www.2488.one/c49p2.aspx 的拼接其中 p2 代表第一页之后的拼接以此类推，得到拼接 a_url_pager
    请求 a_url_pager 若为 200 且有内容则返回 a_pager_content

    从 a_pager_content 中的 <div class="mx"></div> 中匹配获得以下两个内容，并统计总数量 b_count
        n 开头 .aspx 结尾的全部文本 b_text
        标题 b_title
    在当前目录下创建 b_title 目录，存在则忽略，并进入目录
    
    从 0 开始循环便利总页数到 b_count 范围 [0,b_count]
    拼接 url 和 b_text 中的每一个文本得到 b_url
    请求 b_url 若为 200 且有内容则返回 b_content
    从 b_content 中的 <div class="pager"></div> 中获得倒数第3个 <li></li> 元素获取文本值总页数 b_pager

    从 1 开始循环便利总页数到 c_pb_pagerager 范围 [1,b_pager]
    当为 1 则直接使用 b_content 赋值给 b_pager_content
    当不为 1 则处理 b_url 将结尾类似 n106083c49.aspx 的部分中 .aspx 去掉的到 b_url_cut 用于后续拼接 
    拼接 b_url_cut 和 b_count 得到类似 https://www.2488.one/n106083c49p1.aspx 的拼接其中 p1 代表第一页之后的拼接以此类推，得到拼接 b_url_pager
    请求 b_url_pager  若为 200 且有内容则返回 b_pager_content
    从 b_pager_content 中的 <div id="content"></div></div> 中匹配获得 upload 开头 .jpg_gzip.aspx 结尾的全部文本 c_text 并统计数量 c_count
    
    从 0 开始循环遍历总页数到 c_count 范围 [0,c_count]
    处理 c_text 的每一个文本只截取类似 24011909415963.jpg_gzip.aspx 的部分并且替换 .jpg_gzip.aspx 为 .jpg 作为文件名 filename
    
    拼接 url 和 c_text 得到 c_url
    如果存在则跳过，不存在则请求 c_url 获取图片并保存到 b_title 目录，并命名为 filename 休息3s
    每次结束一个目录循环休息10s
'''


import os,time
import requests
from bs4 import BeautifulSoup

# 安装必备包 python -m pip install --upgrade pip ; python -m pip install bs4 requests

# 在脚本所在目录下创建 美女图集 文件夹并进入文件夹，如果存在则忽略创建直接进入目录
if not os.path.exists("美女图集"):
    os.makedirs("美女图集")
os.chdir("美女图集")
a_name = os.path.abspath('.')
print(f'总路径：{a_name}')

# 定义 url
url = "https://www.2488.one/"

# 定义重试函数
def request_with_retry(url, max_retries=5):
    for _ in range(max_retries):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.content
        except requests.exceptions.RequestException as e:
            print(f"Request failed with {e}, retrying...")
    return None

# 拼接 url 和 c49.aspx 得到 a_url
a_url = url + "c49.aspx"

# 请求 a_url 若为 200 且有内容则返回 a_content
a_content = request_with_retry(a_url)
if a_content is None:
    print("Failed to get content from a_url")
    exit(1)

# 使用 BeautifulSoup 解析 a_content
soup = BeautifulSoup(a_content, 'html.parser')

# 从 a_content 中的 <div class="pager"></div> 中获得倒数第3个 <li></li> 元素并获取文本值为总页数 a_pager
a_pager = int(soup.find('div', {'class': 'pager'}).find_all('li')[-3].text)
print(f'网址：{a_url}，总页数：{a_pager}')
# 从 1 开始循环便利总页数到 a_pager 范围 [1,a_pager]
for i in range(1, a_pager + 1):
    if i == 1:
        a_url_pager = a_url
        # 当为 1 则直接使用 a_content 赋值给 a_pager_content
        a_pager_content = a_content
    else:
        # 当不为 1 则处理 a_url 将结尾类似 c49.aspx 的部分中 .aspx 去掉，得到 a_url_cut 用于后续拼接 
        a_url_cut = a_url.rsplit('.', 1)[0]
        
        # 拼接 a_url_cut 和 a_pager 得到类似 https://www.2488.one/c49p2.aspx 的拼接其中 p2 代表第一页之后的拼接以此类推，得到拼接 a_url_pager
        a_url_pager = f"{a_url_cut}p{i}.aspx"
        
        # 请求 a_url_pager 若为 200 且有内容则返回 a_pager_content
        a_pager_content = request_with_retry(a_url_pager)
        while True:
            if a_pager_content is None:
                print(f"Failed to get content from a_url_pager: {a_url_pager}")
                a_pager_content = request_with_retry(a_url_pager)
            elif "window.location.href" in str(b_pager_content):
                print(f"true,window.location.href in this!try again: {a_url_pager}!")
                a_pager_content = request_with_retry(a_url_pager)
            else:
                break
    a_pager_soup = BeautifulSoup(a_pager_content, 'html.parser')
    # 从 a_pager_content 中的 <div class="pager"></div> 中匹配获得以下两个内容
    # n 开头 .aspx 结尾的全部文本，标题 b_title ，b_text，并统计总数量 b_count
    b_links = [a['href'] for a in a_pager_soup.find('div', class_='mx').find_all('a') if a['href'].startswith('n') and a['href'].endswith('.aspx')]
    b_title = [a.text for a in a_pager_soup.find('div', class_='mx').find_all('h5') if a.text]
    b_count = len(b_links)
    print(f'第{i}页，网址：{a_url_pager}')
    # 遍历每个链接
    for j in range(0,b_count):
        # 在当前目录下创建 b_title 目录，存在则忽略，并进入目录
        b_name = os.path.join(a_name, b_title[j].replace(' ','-').replace('---','-').replace('--','-').replace('#','').replace('@','').lstrip('-').rstrip('-'))
        if not os.path.exists(b_name):
            os.makedirs(b_name)
        os.chdir(b_name)
        print(f'创建目录：{b_name}')
        # 拼接 url 和 b_text 中的每一个文本得到 b_url
        b_url = url + b_links[j]
        
        # 请求 b_url 若为 200 且有内容则返回 b_content
        b_content = request_with_retry(b_url)

        while True:
            if b_content is None:
                print(f"Failed to get content from b_url: {b_url}")
                b_content = request_with_retry(b_url)
            elif "window.location.href" in str(b_content):
                print(f"true,window.location.href in this!try again: {b_url} !")
                b_content = request_with_retry(b_url)
            else:
                break
        # 从 b_content 中的 <div class="pager"></div> 中获得倒数第3个 <li></li> 元素获取文本值总页数 b_pager
        b_soup = BeautifulSoup(b_content, 'html.parser')
        b_pager = int(b_soup.find('div', {'class': 'pager'}).find_all('li')[-3].text)
        print(f'网址：{b_url}，总页数：{b_pager}')
        # 从 1 开始循环便利总页数到 c_pb_pagerager 范围 [1,b_pager]
        for j in range(1, b_pager + 1):
            if j == 1:
                b_url_pager = b_url
                # 当为 1 则直接使用 b_content 赋值给 b_pager_content
                b_pager_content = b_content
            else:
                # 当不为 1 则处理 b_url 将结尾类似 n106083c49.aspx 的部分中 .aspx 去掉的到 b_url_cut 用于后续拼接 
                b_url_cut = b_url.rsplit('.', 1)[0]
                
                # 拼接 b_url_cut 和 b_count 得到类似 https://www.2488.one/n106083c49p1.aspx 的拼接其中 p1 代表第一页之后的拼接以此类推，得到拼接 b_url_pager
                b_url_pager = f"{b_url_cut}p{j}.aspx"
                # 请求 b_url_pager  若为 200 且有内容则返回 b_pager_content
                b_pager_content = request_with_retry(b_url_pager)
                while True:
                    if b_pager_content is None:
                        print(f"Failed to get content from b_url_pager: {b_url_pager}")
                        b_pager_content = request_with_retry(b_url_pager)
                    elif "window.location.href" in str(b_pager_content):
                        print(f"true,window.location.href in this!try again: {b_url_pager}!")
                        b_pager_content = request_with_retry(b_url_pager)
                    else:
                        break
            # 从 b_pager_content 中的 <div id="content"></div> 中匹配获得 upload 开头 .jpg_gzip.aspx 结尾的全部文本 c_text 并统计数量 c_count
            b_pager_soup = BeautifulSoup(b_pager_content, 'html.parser')
            c_text = [img['src'] for img in b_pager_soup.find('div', id='content').find_all('img') if img['src'].startswith('upload/') and img['src'].endswith('.jpg_gzip.aspx')]
            c_count = len(c_text)
            print(f'第{j}页，网址：{b_url_pager}')
            # 从 0 开始循环遍历总页数到 c_count 范围 [0,c_count]
            for k in range(c_count):
                # 处理 c_text 的每一个文本只截取类似 24011909415963.jpg_gzip.aspx 的部分并且替换 .jpg_gzip.aspx 为 .jpg 作为文件名 filename
                filename = c_text[k].replace(".jpg_gzip.aspx", ".jpg").split('/')[-1]
                
                # 拼接 url 和 c_text 得到 c_url
                c_url = url + c_text[k]
                # 如果存在则跳过，不存在则请求 c_url 获取图片并保存到 b_title 目录，并命名为 filename 休息3s
                c_name = os.path.join(b_name, filename)
                if not os.path.exists(c_name):
                    image_content = request_with_retry(c_url)
                    if image_content is None:
                        print(f"Failed to get image from c_url: {c_url}")
                        continue
                    with open(c_name, 'wb') as f:
                        f.write(image_content)
                    print(f'第{k+1}条，网址：{c_url}，存储路径：{c_name}')
                    print('休息3s')
                    time.sleep(3)
                else:
                    print('文件存在')
                    
            # 每次结束一个目录循环休息10s
            print('休息10s')
            time.sleep(10)
            
        # 返回上一层目录
        os.chdir(a_name)
