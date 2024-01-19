# Beauty-pictures-24fa-crawling
Python脚本获取24fa美女图片下载

![Watchers](https://img.shields.io/github/watchers/smallflowercat1995/Beauty-pictures-24fa-crawling) ![Stars](https://img.shields.io/github/stars/smallflowercat1995/Beauty-pictures-24fa-crawling) ![Forks](https://img.shields.io/github/forks/smallflowercat1995/Beauty-pictures-24fa-crawling) ![Vistors](https://visitor-badge.laobi.icu/badge?page_id=smallflowercat1995.Python-script-EEBBK-learning-computer-H6-learning-materials-download) ![LICENSE](https://img.shields.io/badge/license-CC%20BY--SA%204.0-green.svg)
<a href="https://star-history.com/#smallflowercat1995/Beauty-pictures-24fa-crawling&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=smallflowercat1995/Beauty-pictures-24fa-crawling&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=smallflowercat1995/Beauty-pictures-24fa-crawling&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=smallflowercat1995/Beauty-pictures-24fa-crawling&type=Date" />
  </picture>
</a>

# 目录结构：
    .
    ├── 24fa爬美图.py                                # Python脚本
    └── README.md                                   # 这个是说明文件   

# 起因：
    最近用 python 写了一个脚本用来获取一些图片，用于解决生理需求，大概就是这样

# 思路：
    创建重试函数，为了规避网络问题导致的 tls 报错
    在脚本所在目录下创建 美女图集 文件夹，如果存在则忽略
    定义 a_url 为 https://www.248.one/
    拼接 a_url 和 c49.aspx 得到 b_url
    请求 b_url 若为 200 且有内容则返回 b_url_content
    
    从 b_url_content 中的 <div class="conL"></div> 中获得总页数 b_pager
    从 1开始循环便利总页数到 b_pager 范围 [1,b_pager]
    处理 b_url 将结尾类似 c49.aspx 的部分中 .aspx 去掉的到 b_url_cut 用于后续拼接 
    拼接 b_url_cut 和 b_pager 得到类似 https://www.248.one/c49p1.aspx 的拼接其中 p1 代表第一页之后的拼接以此类推，得到拼接 b_url_pager
    请求 b_url_pager  若为 200 且有内容则返回 b_url_content
    从 b_url_content 中的 <div class="conL"></div> 中匹配获得以下两个内容
        n 开头 .aspx 结尾的全部文本 b_url_content_text
        标题 b_url_content_title
    在当前目录下创建 b_url_content_title 目录，如果存在则忽略
    
    根据 b_url_content_text 的数量进行遍历
    拼接 a_url 和 b_url_content_text 中的每一个文本 得到 c_url
    请求 c_url 若为 200 且有内容则返回 c_url_content
    从 c_url_content 中的 <div id="printBody" style="word-break:break-all;"></div> 中获得总页数 c_pager
    从 1开始循环便利总页数到 c_pager 范围 [1,c_pager]
    处理 c_url 将结尾类似 n106083c49.aspx 的部分中 .aspx 去掉的到 c_url_cut 用于后续拼接 
    拼接 c_url_cut 和 c_pager 得到类似 https://www.248.one/n106083c49p1.aspx 的拼接其中 p1 代表第一页之后的拼接以此类推，得到拼接 c_url_pager
    请求 c_url_pager  若为 200 且有内容则返回 c_url_content
    从 c_url_content 中的 <div id="printBody" style="word-break:break-all;"></div> 中匹配获得 upload 开头 .jpg_gzip.aspx 结尾的全部文本 c_url_content_text
    
    根据 c_url_content_text 的数量进行遍历
    处理 c_url_content_text 的每一个文本只截取类似 24011909415963.jpg_gzip.aspx 的部分并且替换 .jpg_gzip.aspx 为 .jpg 作为文件名 filename
    
    拼接 a_url 和 c_url_content_text 得到 d_url
    请求 d_url 获取图片并保存到 b_url_content_title 目录并命名为 filename，如果存在则跳过


# 成品代码：
    # 思路
    # 导入所需的模块
    import requests
    from bs4 import BeautifulSoup
    import os
    import lxml
    from requests.adapters import HTTPAdapter
    from requests.packages.urllib3.util.retry import Retry
    
    # 定义一个重试函数，用于发送请求并处理异常
    def retry_request(url, session, timeout, max_retries, backoff_factor):
        # 创建一个重试策略
        retry = Retry(total=max_retries, backoff_factor=backoff_factor, status_forcelist=[500, 502, 503, 504])
        # 创建一个适配器，将重试策略应用到会话对象上
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        # 发送请求，并返回响应或者异常
        try:
            response = session.get(url, timeout=timeout)
            return response
        except requests.exceptions.RequestException as e:
            return e
    
    # 在脚本所在目录下创建 美女图集 文件夹，如果存在则忽略
    folder = "美女图集"
    if not os.path.exists(folder):
        os.mkdir(folder)
        print(f"创建 {folder} 文件夹成功")
    else:
        print(f"{folder} 文件夹已存在")
    
    # 定义 a_url 为 https://www.248.one/
    a_url = "https://www.248.one/"
    
    # 拼接 a_url 和 c49.aspx 得到 b_url
    b_url = a_url + "c49.aspx"
    print(f"b_url 为 {b_url}")
    
    # 创建一个会话对象
    session = requests.Session()
    # 请求 b_url，设置超时时间为 5 秒，最大重试次数为 3 次，重试间隔因子为 2
    b_url_response = retry_request(b_url, session, 5, 3, 2)
    
    # 判断 b_url_response 是否为 requests.Response 类型，如果是，说明请求成功，否则，说明请求失败
    if isinstance(b_url_response, requests.Response):
        # 请求 b_url 若为 200 且有内容则返回 b_url_content
        b_url_response = requests.get(b_url)
        if b_url_response.status_code == 200 and b_url_response.content:
            b_url_content = b_url_response.content
            print(f"请求 b_url 成功，返回 b_url_content")
        else:
            print(f"请求 b_url 失败，退出程序")
            exit()
    else:
        # 如果请求失败，打印异常信息，退出程序
        print(f"请求 b_url 失败，异常信息为：{b_url_response}")
        exit()
        
    # 从 b_url_content 中的 <div class="conL"></div> 中获得总页数 b_pager
    b_url_soup = BeautifulSoup(b_url_content, "lxml")
    b_url_div = b_url_soup.find("div", class_="conL")
    b_pager = int(b_url_div.find("div", class_="pager").find_all('li')[0].text.split("/")[1])
    print(f"从 b_url_content 中获得总页数 b_pager 为 {b_pager}")
    
    # 从 1开始循环便利总页数到 b_pager 范围 [1,b_pager]
    for i in range(1, b_pager + 1):
        print(f"开始处理第 {i} 页")
    
        # 处理 b_url 将结尾类似 c49.aspx 的部分中 .aspx 去掉的到 b_url_cut 用于后续拼接 
        b_url_cut = b_url.replace(".aspx", "")
        print(f"处理 b_url 得到 b_url_cut 为 {b_url_cut}")
    
        # 拼接 b_url_cut 和 b_pager 得到类似 https://www.248.one/c49p1.aspx 的拼接其中 p1 代表第一页之后的拼接以此类推，得到拼接 b_url_pager
        b_url_pager = b_url_cut + f"p{i}.aspx"
        print(f"拼接 b_url_cut 和 b_pager 得到 b_url_pager 为 {b_url_pager}")
    
        # 请求 b_url_pager，设置超时时间为 5 秒，最大重试次数为 3 次，重试间隔因子为 2
        b_url_pager_response = retry_request(b_url_pager, session, 5, 3, 2)
    
        # 判断 b_url_pager_response 是否为 requests.Response 类型，如果是，说明请求成功，否则，说明请求失败
        if isinstance(b_url_pager_response, requests.Response):
            # 请求 b_url_pager  若为 200 且有内容则返回 b_url_content
            b_url_pager_response = requests.get(b_url_pager)
            if b_url_pager_response.status_code == 200 and b_url_pager_response.content:
                b_url_pager_content = b_url_pager_response.content
                print(f"请求 b_url_pager 成功，返回 b_url_pager_content")
            else:
                print(f"请求 b_url_pager 失败，跳过该页")
                continue
        else:
            # 如果请求失败，打印异常信息，跳过该页
            print(f"请求 b_url_pager 失败，异常信息为：{b_url_pager_response}")
            continue
        
        # 从 b_url_pager_content 中的 <div class="conL"></div> 中匹配获得以下两个内容
        #     n 开头 .aspx 结尾的全部文本 b_url_pager_content_text
        #     标题 b_url_pager_content_title
        b_url_pager_soup = BeautifulSoup(b_url_pager_content, "lxml")
        b_url_pager_div = b_url_pager_soup.find("div", class_="conL")
        b_url_pager_content_text = [a["href"] for a in b_url_pager_div.find_all("a") if a["href"].startswith("n") and a["href"].endswith(".aspx")]
        b_url_pager_content_title = [a.text for a in b_url_pager_div.find_all("h5")]
    
        print(f"从 b_url_pager_content 中匹配获得 b_url_pager_content_text 为 {b_url_pager_content_text}")
        print(f"从 b_url_pager_content 中匹配获得 b_url_pager_content_title 为 {b_url_pager_content_title}")
    
        # 根据 b_url_pager_content_text 的数量进行遍历
        for j in range(len(b_url_pager_content_text)):
            print(f"开始处理第 {j + 1} 个文本")
    
            # 拼接 a_url 和 b_url_pager_content_text 中的每一个文本 得到 c_url
            c_url = a_url + b_url_pager_content_text[j]
            print(f"拼接 a_url 和 b_url_pager_content_text 得到 c_url 为 {c_url}")
    
            # 请求 c_url，设置超时时间为 5 秒，最大重试次数为 3 次，重试间隔因子为 2
            c_url_response = retry_request(c_url, session, 5, 3, 2)
    
            # 判断 c_url_response 是否为 requests.Response 类型，如果是，说明请求成功，否则，说明请求失败
            if isinstance(c_url_response, requests.Response):
                # 请求 c_url 若为 200 且有内容则返回 c_url_content
                c_url_response = requests.get(c_url)
                if c_url_response.status_code == 200 and c_url_response.content:
                    c_url_content = c_url_response.content
                    print(f"请求 c_url 成功，返回 c_url_content")
                else:
                    print(f"请求 c_url 失败，跳过该文本")
                    continue
            else:
                # 如果请求失败，打印异常信息，跳过该文本
                print(f"请求 c_url 失败，异常信息为：{c_url_response}")
                continue
            
            # 从 c_url_content 中的 <div id="printBody" style="word-break:break-all;"></div> 中获得总页数 c_pager
            c_url_soup = BeautifulSoup(c_url_content, "lxml")
            c_url_div = c_url_soup.find("div", id="printBody", style="word-break:break-all;").find("div",class_="pager")
            c_pager = int(c_url_div.find_all("li")[-3].text)
            print(f"从 c_url_content 中获得总页数 c_pager 为 {c_pager}")
    
            # 在当前目录下创建 b_url_pager_content_title 目录，如果存在则忽略
            subfolder = b_url_pager_content_title[j]
            subfolder_path = os.path.join(folder, subfolder)
            if not os.path.exists(subfolder_path):
                os.mkdir(subfolder_path)
                print(f"创建 {subfolder} 目录成功")
            else:
                print(f"{subfolder} 目录已存在")
    
            # 从 1开始循环便利总页数到 c_pager 范围 [1,c_pager]
            for k in range(1, c_pager + 1):
                print(f"开始处理第 {k} 页")
    
                # 处理 c_url 将结尾类似 n106083c49.aspx 的部分中 .aspx 去掉的到 c_url_cut 用于后续拼接 
                c_url_cut = c_url.replace(".aspx", "")
                print(f"处理 c_url 得到 c_url_cut 为 {c_url_cut}")
    
                # 拼接 c_url_cut 和 c_pager 得到类似 https://www.248.one/n106083c49p1.aspx 的拼接其中 p1 代表第一页之后的拼接以此类推，得到拼接 c_url_pager
                c_url_pager = c_url_cut + f"p{k}.aspx"
                print(f"拼接 c_url_cut 和 c_pager 得到 c_url_pager 为 {c_url_pager}")
    
                # 请求 c_url_pager，设置超时时间为 5 秒，最大重试次数为 3 次，重试间隔因子为 2
                c_url_pager_response = retry_request(c_url_pager, session, 5, 3, 2)
    
                # 判断 c_url_pager_response 是否为 requests.Response 类型，如果是，说明请求成功，否则，说明请求失败
                if isinstance(c_url_pager_response, requests.Response):
                    # 如果请求成功，判断状态码是否为 200，且响应内容是否存在
                    if c_url_pager_response.status_code == 200 and c_url_pager_response.content:
                        c_url_pager_content = c_url_pager_response.content
                        print(f"请求 c_url_pager 成功，返回 c_url_pager_content")
                    else:
                        print(f"请求 c_url_pager 失败，跳过该页")
                        continue
                else:
                    # 如果请求失败，打印异常信息，跳过该页
                    print(f"请求 c_url_pager 失败，异常信息为：{c_url_pager_response}")
                    continue
                # 从 c_url_pager_content 中的 <div id="printBody" style="word-break:break-all;"></div> 中匹配获得 upload 开头 .jpg_gzip.aspx 结尾的全部文本 c_url_pager_content_text
                c_url_pager_soup = BeautifulSoup(c_url_pager_content, "lxml")
                c_url_pager_div = c_url_pager_soup.find("div", id="printBody", style="word-break:break-all;")
                c_url_pager_content_text = [img["src"] for img in c_url_pager_div.find_all("img") if img["src"].startswith("upload") and img["src"].endswith(".jpg_gzip.aspx")]
    
                # 根据 c_url_pager_content_text 的数量进行遍历
                for l in range(len(c_url_pager_content_text)):
                    print(f"开始处理第 {l + 1} 个图片")
    
                    # 处理 c_url_pager_content_text 的每一个文本只截取类似 24011909415963.jpg_gzip.aspx 的部分并且替换 .jpg_gzip.aspx 为 .jpg 作为文件名 filename
                    filename = c_url_pager_content_text[l].split("/")[-1].replace(".jpg_gzip.aspx", ".jpg")
                    print(f"处理 c_url_pager_content_text 得到 filename 为 {filename}")
    
                    # 拼接 a_url 和 c_url_pager_content_text 得到 d_url
                    d_url = a_url + c_url_pager_content_text[l]
                    print(f"拼接 a_url 和 c_url_pager_content_text 得到 d_url 为 {d_url}")
    
                    # 请求 d_url 获取图片并保存到 b_url_pager_content_title 目录并命名为 filename，如果存在则跳过
                    file_path = os.path.join(subfolder_path, filename)
                    if not os.path.exists(file_path):
                        # 请求 c_url_pager，设置超时时间为 5 秒，最大重试次数为 3 次，重试间隔因子为 2
                        d_url_response = retry_request(d_url, session, 5, 3, 2)
                        # 判断 c_url_pager_response 是否为 requests.Response 类型，如果是，说明请求成功，否则，说明请求失败
                        if isinstance(d_url_response, requests.Response):
                            # 如果请求成功，判断状态码是否为 200，且响应内容是否存在
                            if d_url_response.status_code == 200 and d_url_response.content:
                                with open(file_path, "wb") as f:
                                    f.write(d_url_response.content)
                                    print(f"请求 d_url 成功，保存图片到 {file_path}")
                            else:
                                print(f"请求 d_url 失败，跳过该图片")
                        else:
                            # 如果请求失败，打印异常信息，跳过该图片
                            print(f"请求 d_url 失败，异常信息为：{d_url_response}")
                    else:
                        print(f"{file_path} 已存在，跳过该图片")

# 声明
本项目仅作学习交流使用，用于查找资料，学习知识，不做任何违法行为。所有资源均来自互联网，仅供大家交流学习使用，出现违法问题概不负责。 
