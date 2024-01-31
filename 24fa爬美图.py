# 思路
'''
    在脚本所在目录下创建 美女图集 文件夹，存在则忽略，并进入文件夹,创建重试函数，为了规避网络问题导致的 tls 报错，并且使用脚本实现需求
    
    定义 a_url 为 https://www.248.one/
    拼接 a_url 和 c49.aspx 得到 b_url
    请求 b_url 若为 200 且有内容则返回 b_url_content
    
    从 b_url_content 中的 <div class="conL"></div> 中获得总页数 b_pager

    从 1 开始循环便利总页数到 b_pager 范围 [1,b_pager]
    当为 1 则直接使用 b_url_content 赋值给 b_url_pager_content
    当不为 1 则处理 b_url 将结尾类似 c49.aspx 的部分中 .aspx 去掉，得到 b_url_cut 用于后续拼接 
    拼接 b_url_cut 和 b_pager 得到类似 https://www.248.one/c49p2.aspx 的拼接其中 p2 代表第一页之后的拼接以此类推，得到拼接 b_url_pager
    请求 b_url_pager 若为 200 且有内容则返回 b_url_pager_content

    从 b_url_pager_content 中的 <div class="conL"></div> 中匹配获得以下两个内容，并统计总数量 b_url_content_text_count
        n 开头 .aspx 结尾的全部文本 b_url_content_text
        标题 b_url_content_title
    在当前目录下创建 b_url_content_title 目录，存在则忽略，并进入目录
    
    从 1 开始循环便利总页数到 b_url_content_text_count 范围 [1,b_url_content_text_count]
    拼接 a_url 和 b_url_content_text 中的每一个文本得到 c_url
    请求 c_url 若为 200 且有内容则返回 c_url_content
    从 c_url_content 中的 <div id="printBody" style="word-break:break-all;"></div> 中获得总页数 c_pager
    从 1 开始循环便利总页数到 c_pager 范围 [1,c_pager]
    当为 1 则直接使用 c_url_content 赋值给 c_url_pager_content
    当不为 1 则处理 c_url 将结尾类似 n106083c49.aspx 的部分中 .aspx 去掉的到 c_url_cut 用于后续拼接 
    拼接 c_url_cut 和 c_pager 得到类似 https://www.248.one/n106083c49p1.aspx 的拼接其中 p1 代表第一页之后的拼接以此类推，得到拼接 c_url_pager
    请求 c_url_pager  若为 200 且有内容则返回 c_url_pager_content
    从 c_url_pager_content 中的 <div id="printBody" style="word-break:break-all;"></div> 中匹配获得 upload 开头 .jpg_gzip.aspx 结尾的全部文本 c_url_content_text 并统计数量 c_url_content_text_count
    
    从 1 开始循环遍历总页数到 c_url_content_text_count 范围 [1,c_url_content_text_count]
    处理 c_url_content_text 的每一个文本只截取类似 24011909415963.jpg_gzip.aspx 的部分并且替换 .jpg_gzip.aspx 为 .jpg 作为文件名 filename
    
    拼接 a_url 和 c_url_content_text 得到 d_url
    请求 d_url 获取图片并保存到 b_url_content_title 目录，并命名为 filename，如果存在则跳过
'''
# 在脚本所在目录下创建 图集 文件夹，存在则忽略，并进入文件夹
import os
os.makedirs("美女图集", exist_ok=True)
os.chdir("美女图集")
base_path = os.path.abspath('.')
print(base_path)
# 创建重试函数，为了规避网络问题导致的 tls 报错
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def retry_request(url, max_retries=3, backoff_factor=0.3):
    # 设置请求头，模拟浏览器访问
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0"
    }
    session = requests.Session()
    retry = Retry(total=max_retries, backoff_factor=backoff_factor)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    response = session.get(url, headers=headers)
    return response

# 定义 a_url 为 https://www.248.one/
a_url = "https://www.24fa.icu/"

# 拼接 a_url 和 c49.aspx 得到 b_url
b_url = a_url + "c49.aspx"

# 请求 b_url 若为 200 且有内容则返回 b_url_content
b_url_content = None
response = retry_request(b_url)
if response.status_code == 200 and response.content:
    b_url_content = response.content

# 从 b_url_content 中的 <div class="conL"></div> 中获得总页数 b_pager
b_pager = None
if b_url_content:
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(b_url_content, "html.parser")
    div = soup.find("div", class_="conL").find("div",class_="pager").find_all('li')
    if div:
        b_pager = int(div[-3].text.split()[-1])

# 从 1 开始循环便利总页数到 b_pager 范围 [1,b_pager]
for i in range(1, b_pager + 1):
    # 当为 1 则直接使用 b_url_content 赋值给 b_url_pager_content
    if i == 1:
        b_url_pager_content = b_url_content
    # 当不为 1 则处理 b_url 将结尾类似 c49.aspx 的部分中 .aspx 去掉，得到 b_url_cut 用于后续拼接 
    else:
        b_url_cut = b_url.replace(".aspx", "")
        # 拼接 b_url_cut 和 b_pager 得到类似 https://www.248.one/c49p2.aspx 的拼接其中 p2 代表第一页之后的拼接以此类推，得到拼接 b_url_pager
        b_url_pager = b_url_cut + "p" + str(i) + ".aspx"
        # 请求 b_url_pager 若为 200 且有内容则返回 b_url_pager_content
        b_url_pager_content = None
        response = retry_request(b_url_pager)
        if response.status_code == 200 and response.content:
            b_url_pager_content = response.content

    # 从 b_url_pager_content 中的 <div class="conL"></div> 中匹配获得以下两个内容，并统计总数量 b_url_content_text_count
    #     n 开头 .aspx 结尾的全部文本 b_url_content_text
    #     标题 b_url_content_title
    b_url_content_text = []
    b_url_content_title = []
    b_url_content_text_count = 0
    if b_url_pager_content:
        soup = BeautifulSoup(b_url_pager_content, "html.parser")
        divs = soup.find_all("div", class_="wrapper")
        for div in divs:
            a = div.find("a")
            if a:
                b_url_content_text.append(a["href"])
                b_url_content_title.append(a.text)
                b_url_content_text_count += 1

    # 在当前目录下创建 b_url_content_title 目录，存在则忽略，并进入目录
    for j in range(b_url_content_text_count):
        b_url_content_title_path = os.path.join(base_path, b_url_content_title[j])
        os.makedirs(b_url_content_title_path, exist_ok=True)
        os.chdir(b_url_content_title_path)
        print(b_url_content_title_path)
        # 拼接 a_url 和 b_url_content_text 中的每一个文本得到 c_url
        c_url = a_url + b_url_content_text[j]
        # 请求 c_url 若为 200 且有内容则返回 c_url_content
        c_url_content = None
        response = retry_request(c_url)
        if response.status_code == 200 and response.content:
            c_url_content = response.content

        # 从 c_url_content 中的 <div id="printBody" style="word-break:break-all;"></div> 中获得总页数 c_pager
        c_pager = None
        if c_url_content:
            soup = BeautifulSoup(c_url_content, "html.parser")
            div = soup.find("div", id="printBody", style="word-break:break-all;").find("div",class_="pager").find_all('li')
            if div:
                c_pager = int(div[-3].text.split()[-1])

        # 从 1 开始循环便利总页数到 c_pager 范围 [1,c_pager]
        for k in range(1, c_pager + 1):
            # 当为 1 则直接使用 c_url_content 赋值给 c_url_pager_content
            if k == 1:
                c_url_pager_content = c_url_content
            # 当不为 1 则处理 c_url 将结尾类似 n106083c49.aspx 的部分中 .aspx 去掉的到 c_url_cut 用于后续拼接 
            else:
                c_url_cut = c_url.replace(".aspx", "")
                # 拼接 c_url_cut 和 c_pager 得到类似 https://www.248.one/n106083c49p1.aspx 的拼接其中 p1 代表第一页之后的拼接以此类推，得到拼接 c_url_pager
                c_url_pager = c_url_cut + "p" + str(k) + ".aspx"
                # 请求 c_url_pager  若为 200 且有内容则返回 c_url_pager_content
                c_url_pager_content = None
                response = retry_request(c_url_pager)
                if response.status_code == 200 and response.content:
                    c_url_pager_content = response.content

            # 从 c_url_pager_content 中的 <div id="printBody" style="word-break:break-all;"></div> 中匹配获得 upload 开头 .jpg_gzip.aspx 结尾的全部文本 c_url_content_text 并统计数量 c_url_content_text_count
            c_url_content_text = []
            c_url_content_text_count = 0
            if c_url_pager_content:
                soup = BeautifulSoup(c_url_pager_content, "html.parser")
                div = soup.find("div", id="printBody", style="word-break:break-all;")
                if div:
                    img_tags = div.find_all("img")
                    for img in img_tags:
                        if img["src"].startswith("upload") and img["src"].endswith(".jpg_gzip.aspx"):
                            c_url_content_text.append(img["src"])
                            c_url_content_text_count += 1
            
            # 从 1 开始循环遍历总页数到 c_url_content_text_count 范围 [1,c_url_content_text_count]
            for l in range(c_url_content_text_count):
                # 处理 c_url_content_text 的每一个文本只截取类似 24011909415963.jpg_gzip.aspx 的部分并且替换 .jpg_gzip.aspx 为 .jpg 作为文件名 filename
                filename = c_url_content_text[l].replace(".jpg_gzip.aspx", ".jpg").split('/')[-1]
                # 拼接 a_url 和 c_url_content_text 得到 d_url
                d_url = a_url + c_url_content_text[l]
                # 请求 d_url 获取图片并保存到 b_url_content_title 目录，并命名为 filename，如果存在则跳过
                if not os.path.exists(filename):
                    response = retry_request(d_url)
                    if response.status_code == 200 and response.content:
                        with open(filename, "wb") as f:
                            print(d_url,'-->',filename)
                            f.write(response.content)

        # 返回上一级目录
        os.chdir(os.path.join(b_url_content_title_path, ".."))