# 思路
'''
    在脚本所在目录下创建 美女图集 文件夹并进入文件夹，如果存在则忽略创建直接进入目录,创建重试函数，为了规避网络问题导致的 tls 报错，并且使用脚本实现需求
    定义 跳过链接集
    创建判断链接是在跳过链接集中存在，并返回布尔
    定义 a_url 为 https://xerocos.com
    请求 a_url 若为 200 且有内容则返回 a_content

    从 a_content 中最后一个 <div class="flex space-x-2"></div> 元素中获得<div class="hidden md:block"></div> 并从中获取 <a class="hover:bg-pink-500 bg-gray-700 relative inline-flex items-center px-4 py-2 border border-pink-500 text-xs font-medium rounded-md text-gray-100" href="">Last</a> 从 href 属性中得到总页数(比如得到了 /?page=226 则返回总页数 226) a_pager

    从 1 开始循环便利总页数到 a_pager 范围 [1,a_pager+1]
    当为 1 则拼接 a_url 对应的链接赋值给 a_pager_url ，将 a_content 赋值给 a_pager_url_content
    当不为1 则拼接 a_url + a_pager 得到类似 https://xerocos.com/?page=2 的拼接其中 /?page=2 代表第2页之后的拼接以此类推，得到拼接 a_pager_url ，请求 a_pager_url 若为 200 且有内容则返回 a_pager_url_content
    
    从 a_pager_url_content 中 <div class="group flex-shrink-0 pb-3"></div> 中匹配 <div class="pt-2"></div> 中匹配 <div class="flex items-center flex-wrap"></div> 中匹配 <a href=""></a> 提取全部的链接 b_url 和对应链接名 b_name（废除项） 并统计返回数量 b_count

    从 0 开始循环便利总数到 b_count 范围 [0,b_count]
    在当前目录下创建对应的 b_name 目录并进入目录，如果存在则不创建目录直接进入目录（废除项）
    拼接 a_url+b_url 对应的链接并请求，若为 200 且有内容则返回 b_content

    从 b_content 中最后一个 <div class="flex space-x-2"></div> 元素中获得<div class="hidden md:block"></div> 并从中获取 <a class="hover:bg-pink-500 bg-gray-700 relative inline-flex items-center px-4 py-2 border border-pink-500 text-xs font-medium rounded-md text-gray-100" href="">Last</a> 从 href 属性中得到总页数(比如得到了 /?page=226 则返回总页数 226) b_pager ，如果没有获取到 <div class="flex space-x-2"></div> 则说明只有1页默认返回 1 即 b_pager=1

    从 1 开始循环便利总页数到 b_pager 范围 [1,b_pager+1]
    当为 1 则拼接 a_url+b_url 对应的链接赋值给 a_b_pager_url，将 b_content 赋值给 a_b_pager_url_content
    当不为 1 则拼接 a_url+b_url 和 b_pager 得到类似 https://xerocos.com/tag/bowsette?page=2 的拼接，其中 https://xerocos.com 是 a_url，/tag/bowsette 是 b_url， ?page=2 代表第2页之后的拼接以此类推，得到拼接 a_b_pager_url 并请求，若为 200 且有内容则返回 a_b_pager_url_content
    
    从 a_b_pager_url_content 中获取 <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 pb-6"></div> 元素并从中匹配全部的 <div class="group flex-shrink-0 pb-3"></div> 中匹配 <div class="relative overflow-hidden rounded-sm shadow-xl latest-card"></div> 中匹配  <a href=""></a> 的链接 c_url 和 <a href=""></a> 中匹配 <img alt="" class="duration-100 ease-in-out group-hover:opacity-75 scale-100 blur-0 grayscale-0" src=""> 的 alt 文件夹名 c_name 并统计总数量 c_count

    从 0 开始循环便利总数到 c_count 范围 [0,c_count]
    创建对应的 c_name 目录并进入目录，如果存在则不创建目录直接进入目录
    拼接 a_url+c_url 对应的链接并请求 若为 200 且有内容则返回 c_content

    从 c_content 中最后一个 <div class="flex items-center my-2 flex-wrap"></div> 元素中获取最后一个 <a rel="" class="" href=""></a> 元素并得到文本值总页数(比如得到了 2 则返回总页数 2) c_pager ，如果没有获取到 <div class="flex items-center my-2 flex-wrap"></div> 则说明只有1页默认返回 1 即 c_pager=1

    从 1 开始循环便利总页数到 c_pager 范围 [1,c_pager+1]
    当为 1 则拼接 a_url+c_url 对应的链接赋值给 a_c_pager_url ，将 c_content 赋值给 a_c_pager_url_content
    当不为 1 则拼接 a_url+c_url 和 c_pager 得到类似 https://xerocos.com/view/nagisa-bowsette?page=2 的拼接，其中 https://xerocos.com 是 a_url ，/view/nagisa-bowsette 是 c_url ， ?page=2 代表第2页之后的拼接以此类推，得到拼接 a_c_pager_url 并请求，若为 200 且有内容则返回 a_c_pager_url_content
    判断 a_url+c_url 是否在跳过链接集中，如果存在则打印链接+存在跳过不进行获取 continue 如果不存在则打印链接+不存在，继续运行
    
    从 a_c_pager_url_content 中的 <div class="max-w-7xl mx-auto px-4 w-full"></div> 中匹配 <div class="md:px-16 xl:px-20 max-w-3xl mx-auto justify-center items-center flex flex-col min-h-screen"></div> 的 <div></div> 的 <img alt="" class="" src="" data-src="" > 中匹配 data-src 获取全部图片链接 d_url ，并得到图片链接总数量 d_count
    
    从 0 开始循环便利总数到 d_count 范围 [0,d_count]
    处理图片链接 d_url 并截取文件名得到 d_name ，检查文件路径中是否与 d_name 重名，如果找到重名文件则代表文件存在也就不用请求图片链接，如果找不到重名文件则说明文件不存在则请求图片链接并存储下载并截取文件名存储到 c_name 目录中，比如获取的链接为 https://i1.wp.com/mitaku.net/wp-content/uploads/2021/07/Nagisa-%E9%AD%94%E7%89%A9%E5%96%B5-Bowsette-1.jpg 那么存储的文件名就为 Nagisa-%E9%AD%94%E7%89%A9%E5%96%B5-Bowsette-1.jpg 并睡眠3s
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

# 定义 a_url 为 https://xerocos.com
a_url = "https://xerocos.com"
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# 定义跳过链接集
c_urls_set = {
    "https://xerocos.com/view/aqua-kiara-sessyoin",
}

# 创建判断链接是否存在屏蔽链接集中，并返回布尔
def check_url_exists(test_url):
    return test_url in c_urls_set

# 创建重试函数，为了规避网络问题导致的 tls 报错
def request_with_retry(url, max_retries=5):
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(url=url,headers=headers)
            if response.status_code == 200:
                return response.content
        except Exception as e:
            print(f"Request to {url} failed with {str(e)}, retrying...")
            retries += 1
    return None

# 请求 a_url 若为 200 且有内容则返回 a_content
a_content = request_with_retry(a_url)

# 从 a_content 中最后一个 <div class="flex space-x-2"></div> 元素中获得<div class="hidden md:block"></div> 并从中获取 <a class="hover:bg-pink-500 bg-gray-700 relative inline-flex items-center px-4 py-2 border border-pink-500 text-xs font-medium rounded-md text-gray-100" href="">Last</a> 从 href 属性中得到总页数(比如得到了 /?page=226 则返回总页数 226) a_pager
soup = BeautifulSoup(a_content, 'html.parser')
last_page_link = soup.select_one('div.flex.space-x-2 div.hidden.md\\:block a.hover\\:bg-pink-500.bg-gray-700.relative.inline-flex.items-center.px-4.py-2.border.border-pink-500.text-xs.font-medium.rounded-md.text-gray-100[href]')
a_pager = int(last_page_link['href'].split('=')[-1]) if last_page_link else 1
print(f'总网址：{a_url}，总页数：{a_pager}')
# 从 1 开始循环便利总页数到 a_pager 范围 [1,a_pager+1]
for i in range(1, a_pager + 1):
    # 当为 1 则拼接 a_url 对应的链接赋值给 a_pager_url ，将 a_content 赋值给 a_pager_url_content
    # 当不为1 则拼接 a_url + a_pager 得到类似 https://xerocos.com/?page=2 的拼接其中 /?page=2 代表第2页之后的拼接以此类推，得到拼接 a_pager_url ，请求 a_pager_url 若为 200 且有内容则返回 a_pager_url_content
    if i == 1:
        # 当为 1 则拼接 a_url 对应的链接赋值给 a_pager_url
        a_pager_url = a_url
        # 当为 1 则直接使用 a_content 赋值给 a_pager_content
        a_pager_url_content = a_content
    else:
        a_pager_url = f"{a_url}/?page={i}"
        a_pager_url_content = request_with_retry(a_pager_url)

    print(f'第{i}页，网址：{a_pager_url}')
    # 从 a_pager_url_content 中 <div class="group flex-shrink-0 pb-3"></div> 中匹配 <div class="pt-2"></div> 中匹配 <div class="flex items-center flex-wrap"></div> 中匹配 <a href=""></a> 提取全部的链接 b_url 和对应链接名 b_name 并统计返回数量 b_count
    soup = BeautifulSoup(a_pager_url_content, 'html.parser')
    links = soup.select('div.group.flex-shrink-0.pb-3 div.pt-2 div.flex.items-center.flex-wrap a[href]')
    b_urls = [link['href'] for link in links]
    # b_names = [link.text for link in links]
    b_count = len(b_urls)
    # 从 0 开始循环便利总数到 b_count 范围 [0,b_count]
    for j in range(b_count):
        # b_name = os.path.join(a_name, b_names[j].replace(' ','-').replace('-–-','-').replace('--','-').replace('#','').replace('@','').lstrip('-').rstrip('-'))
        # # 在当前目录下创建对应的 b_name 目录并进入目录，如果存在则不创建目录直接进入目录
        # if not os.path.exists(b_name):
        #     os.makedirs(b_name)
        # os.chdir(b_name)
        # print(f'创建目录：{b_name}')
        # 拼接 a_url+b_url 对应的链接并请求，若为 200 且有内容则返回 b_content
        b_url = a_url + b_urls[j]
        b_content = request_with_retry(b_url)

        # 从 b_content 中最后一个 <div class="flex space-x-2"></div> 元素中获得<div class="hidden md:block"></div> 并从中获取 <a class="hover:bg-pink-500 bg-gray-700 relative inline-flex items-center px-4 py-2 border border-pink-500 text-xs font-medium rounded-md text-gray-100" href="">Last</a> 从 href 属性中得到总页数(比如得到了 /?page=226 则返回总页数 226) b_pager ，如果没有获取到 <div class="flex space-x-2"></div> 则说明只有1页默认返回 1 即 b_pager=1
        soup = BeautifulSoup(b_content, 'html.parser')
        last_page_link = soup.select_one('div.flex.space-x-2 div.hidden.md\\:block a.hover\\:bg-pink-500.bg-gray-700.relative.inline-flex.items-center.px-4.py-2.border.border-pink-500.text-xs.font-medium.rounded-md.text-gray-100[href]')
        b_pager = int(last_page_link['href'].split('=')[-1]) if last_page_link else 1
        print(f'第{j+1}条，网址：{b_url}，总页数：{b_pager}')
        # 从 1 开始循环便利总页数到 b_pager 范围 [1,b_pager+1]
        for k in range(1, b_pager + 1):
            # 当为 1 则拼接 a_url+b_url 对应的链接赋值给 a_b_pager_url，将 b_content 赋值给 a_b_pager_url_content
            # 当不为 1 则拼接 a_url+b_url 和 b_pager 得到类似 https://xerocos.com/tag/bowsette?page=2 的拼接，其中 https://xerocos.com 是 a_url，/tag/bowsette 是 b_url， ?page=2 代表第2页之后的拼接以此类推，得到拼接 a_b_pager_url 并请求，若为 200 且有内容则返回 a_b_pager_url_content
            if k == 1:
                # 当为 1 则拼接 a_url+b_url 对应的链接赋值给 a_b_pager_url
                a_b_pager_url = b_url
                # 当为 1 则将 b_content 赋值给 a_b_pager_url_content
                a_b_pager_url_content = b_content
            else:
                a_b_pager_url = f"{b_url}?page={k}"
                a_b_pager_url_content = request_with_retry(a_b_pager_url)
            # 从 a_b_pager_url_content 中获取 <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 pb-6"></div> 元素并从中匹配全部的 <div class="group flex-shrink-0 pb-3"></div> 中匹配 <div class="relative overflow-hidden rounded-sm shadow-xl latest-card"></div> 中匹配  <a href=""></a> 的链接 c_url 和 <a href=""></a> 中匹配 <img alt="" class="duration-100 ease-in-out group-hover:opacity-75 scale-100 blur-0 grayscale-0" src=""> 的 alt 文件夹名 c_name 并统计总数量 c_count
            soup = BeautifulSoup(a_b_pager_url_content, 'html.parser')
            links = soup.select('div.grid.grid-cols-2.md\\:grid-cols-3.lg\\:grid-cols-4.gap-4.pb-6 div.group.flex-shrink-0.pb-3 div.relative.overflow-hidden.rounded-sm.shadow-xl.latest-card a[href]')
            c_urls = [link['href'] for link in links]
            c_names = [link.img['alt'] for link in links]
            c_count = len(c_urls)
            print(f'第{k}页，网址：{a_b_pager_url}')
            # 从 0 开始循环便利总数到 c_count 范围 [0,c_count]
            for l in range(c_count):
                # 将 b_name 修改为 a_name
                c_name = os.path.join(a_name, c_names[l].replace(' ','-').replace('-–-','-').replace('--','-').replace('#','').replace('@','').lstrip('-').rstrip('-'))
                # 创建对应的 c_name 目录并进入目录，如果存在则不创建目录直接进入目录
                if not os.path.exists(c_name):
                    os.makedirs(c_name)
                os.chdir(c_name)
                print(f'创建目录：{c_name}')
                # 拼接 a_url+c_url 对应的链接并请求 若为 200 且有内容则返回 c_content
                c_url = a_url + c_urls[l]
                # 判断 c_urls 是否在跳过链接集中，如果存在则打印链接+存在跳过不进行获取 continue 如果不存在则打印链接+不存在，继续运行
                if check_url_exists(c_url):
                    print(f"{c_url} exists.")
                    continue
                else:
                    print(f"{c_url} doesn't exist. run!")
                c_content = request_with_retry(c_url)
                # 从 c_content 中最后一个 <div class="flex items-center my-2 flex-wrap"></div> 元素中获取最后一个 <a rel="" class="" href=""></a> 元素并得到文本值总页数(比如得到了 2 则返回总页数 2) c_pager ，如果没有获取到 <div class="flex items-center my-2 flex-wrap"></div> 则说明只有1页默认返回 1 即 c_pager=1
                soup = BeautifulSoup(c_content, 'html.parser')
                last_page_link = soup.select('div.flex.items-center.my-2.flex-wrap a[rel][class][href]')
                c_pager = int(last_page_link[-1].text) if last_page_link else 1
                print(f'第{l+1}条，网址：{c_url}，总页数：{c_pager}')
                # 从 1 开始循环便利总页数到 c_pager 范围 [1,c_pager+1]
                for m in range(1, c_pager + 1):
                    # 当为 1 则拼接 a_url+c_url 对应的链接赋值给 a_c_pager_url ，将 c_content 赋值给 a_c_pager_url_content
                    # 当不为 1 则拼接 a_url+c_url 和 c_pager 得到类似 https://xerocos.com/view/nagisa-bowsette?page=2 的拼接，其中 https://xerocos.com 是 a_url ，/view/nagisa-bowsette 是 c_url ， ?page=2 代表第2页之后的拼接以此类推，得到拼接 a_c_pager_url 并请求，若为 200 且有内容则返回 a_c_pager_url_content

                    if m == 1:
                        # 当为 1 则拼接 a_url+c_url 对应的链接赋值给 a_c_pager_url
                        a_c_pager_url = c_url
                        # 当为 1 则将 c_content 赋值给 a_c_pager_url_content
                        a_c_pager_url_content = c_content
                    else:
                        a_c_pager_url = f"{c_url}?page={m}"
                        a_c_pager_url_content = request_with_retry(a_c_pager_url)

                    # 从 a_c_pager_url_content 中的 <div class="max-w-7xl mx-auto px-4 w-full"></div> 中匹配 <div class="md:px-16 xl:px-20 max-w-3xl mx-auto justify-center items-center flex flex-col min-h-screen"></div> 的 <div></div> 的 <img alt="" class="" src="" data-src="" > 中匹配 data-src 获取全部图片链接 d_url ，并得到图片链接总数量 d_count
                    soup = BeautifulSoup(a_c_pager_url_content, 'html.parser')
                    images = soup.select('div.max-w-7xl.mx-auto.px-4.w-full div.md\\:px-16.xl\\:px-20.max-w-3xl.mx-auto.justify-center.items-center.flex.flex-col.min-h-screen div img[alt][class][data-src]')
                    d_urls = [image['data-src'] for image in images]
                    d_count = len(d_urls)
                    # 从 0 开始循环便利总数到 d_count 范围 [0,d_count]
                    for n in range(d_count):
                        # 处理图片链接 d_url 并截取文件名得到 d_name ，检查文件路径中是否与 d_name 重名，如果找到重名文件则代表文件存在也就不用请求图片链接，如果找不到重名文件则说明文件不存在则请求图片链接并存储下载并截取文件名存储到 c_name 目录中，比如获取的链接为 https://i1.wp.com/mitaku.net/wp-content/uploads/2021/07/Nagisa-%E9%AD%94%E7%89%A9%E5%96%B5-Bowsette-1.jpg 那么存储的文件名就为 Nagisa-%E9%AD%94%E7%89%A9%E5%96%B5-Bowsette-1.jpg 并睡眠3s
                        d_url = d_urls[n]
                        d_name = d_url.split('/')[-1]
                        d_path = os.path.join(c_name, d_name)
                        if not os.path.exists(d_path):
                            print(f'第{n+1}张，网址：{d_url}，存储文件：{d_path}')
                            d_content = request_with_retry(d_url)
                            with open(d_path, 'wb') as f:
                                f.write(d_content)
                        else:
                            print('文件已存在')
                        print('休息3s')
                        time.sleep(3)
