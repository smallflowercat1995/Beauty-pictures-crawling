# 思路
'''
    在脚本所在目录下创建 美女图集 文件夹并进入文件夹，如果存在则忽略创建直接进入目录,创建重试函数，为了规避网络问题导致的 tls 报错，并且使用脚本实现需求

    定义 跳过链接集
    创建判断链接是在跳过链接集中存在，并返回布尔
    
    定义 a_url 为 https://meiru.neocities.org
    请求 a_url 若为 200 且有内容则返回 a_content

    从 a_content 中 <div id="pagination"></div> 的元素中获得最后一个 <div ></div> 的元素中获得最后一个 <div ></div> 的元素并从中获取倒数第二个 <a href="" class="bg-white border-gray-300 text-gray-500 hover:bg-gray-50 relative inline-flex items-center px-4 py-2 border text-sm font-medium" one-link-mark="yes"></a> 元素并从 href 属性中得到总页数(比如得到了 https://meiru.neocities.org/page/226/ 则返回总页数 226) a_pager

    从 1 开始循环便利总页数到 a_pager 范围 [1,a_pager+1]
    当为 1 则拼接 a_url 对应的链接赋值给 a_pager_url ，将 a_content 赋值给 a_pager_url_content
    当不为1 则拼接 a_url + a_pager 得到类似 https://meiru.neocities.org/page/2/ 的拼接其中 /page/2/ 代表第2页之后的拼接以此类推，得到拼接 a_pager_url ，请求 a_pager_url 若为 200 且有内容则返回 a_pager_url_content
    
    从 a_pager_url_content 中 <div class="p-2"></div> 中匹配 <div class="text-sm text-gray-500 text-center"></div> 中匹配 <a href=""></a> 提取全部的链接 b_url 和对应链接名 b_name（废除项） 并统计返回数量 b_count

    从 0 开始循环便利总数到 b_count 范围 [0,b_count]
    在当前目录下创建对应的 b_name 目录并进入目录，如果存在则不创建目录直接进入目录（废除项）
    请求 b_url 对应的链接，若为 200 且有内容则返回 b_content

    从 b_content 中 <div id="pagination"></div> 的元素中获得最后一个 <div ></div> 的元素中获得最后一个 <div ></div> 的元素并从中获取倒数第二个 <a href="" class="bg-white border-gray-300 text-gray-500 hover:bg-gray-50 relative inline-flex items-center px-4 py-2 border text-sm font-medium" one-link-mark="yes"></a> 元素并从 href 属性值中得到链接总页数(比如得到了 https://meiru.neocities.org/models/%E5%B9%B4%E5%B9%B4/page/226/ 则返回总页数 226) b_pager ，如果没有获取到 获取倒数第二个 <a href="" class="bg-white border-gray-300 text-gray-500 hover:bg-gray-50 relative inline-flex items-center px-4 py-2 border text-sm font-medium" one-link-mark="yes"></a>元素，则说明只有1页默认返回 1 即 b_pager=1 ，并提取链接（比如提取得到 https://meiru.neocities.org/models/%E5%B9%B4%E5%B9%B4/page/ ）返回 c_url

    从 1 开始循环便利总页数到 b_pager 范围 [1,b_pager+1]
    当为 1 则将 c_url 对应的链接赋值给 c_b_pager_url ，并将 b_content 赋值给 c_b_pager_url_content
    当不为 1 则拼接 c_url+b_pager 得到类似 https://meiru.neocities.org/models/%E5%B9%B4%E5%B9%B4/page/2/ 的拼接，其中 https://meiru.neocities.org/models/%E5%B9%B4%E5%B9%B4/page/ 是 c_url ，2/ 代表第2页之后的拼接以此类推，得到拼接 c_b_pager_url 并请求，若为 200 且有内容则返回 c_b_pager_url_content
    
    从 c_b_pager_url_content 中获取 <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-1 p-1"></div> 元素并从中匹配全部的 <div class="p-2"></div> 中匹配第一个 <div ></div> 元素并从中匹配  <a href=""></a> 的链接 d_url 并从中匹配 <img src="" alt="" class="rounded-lg shadow-sm w-full h-72 md:h-96 object-cover" > 的 alt 文件夹名 d_name 并统计总数量 d_count

    从 0 开始循环便利总数到 d_count 范围 [0,d_count]
    创建对应的 d_name 目录并进入目录，如果存在则不创建目录直接进入目录
    拼接 d_url 对应的链接并请求 若为 200 且有内容则返回 d_content

    从 d_content 中获取 <div id="gallery"></div> 元素并从中获取 <img src="" alt="" title="" class="block my-2 mx-auto" > 中匹配 src 获取全部图片链接 e_url ，并得到图片链接总数量 e_count
    
    从 0 开始循环便利总数到 e_count 范围 [0,e_count]
    处理图片链接 e_url 并截取文件名得到 e_name ，检查文件路径中是否与 e_name 重名，如果找到重名文件则代表文件存在也就不用请求图片链接，如果找不到重名文件则说明文件不存在则请求图片链接并存储下载并截取文件名存储到 d_name 目录中，比如获取的链接为 https://telegraph-image.pages.dev/file/dbcc75fbf6f8a11dccbad.jpg 那么存储的文件名就为 dbcc75fbf6f8a11dccbad.jpg 并睡眠3s
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

# 定义 a_url 为 https://meiru.neocities.org
a_url = "https://meiru.neocities.org"

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# 定义跳过链接集
urls_set = {
    "https://meiru.neocities.org/view/aqua-kiara-sessyoin",
}

# 创建判断链接是否存在屏蔽链接集中，并返回布尔
def check_url_exists(test_url):
    return test_url in urls_set

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

# 使用 BeautifulSoup 解析 a_content
soup = BeautifulSoup(a_content, 'html.parser')
# 从 a_content 中获取总页数 a_pager
last_page_link = int(soup.select_one('div#pagination div:last-child div:last-child a:nth-last-child(2)')['href'].split('/')[-2])
a_pager = last_page_link if last_page_link else 1
print(f'总网址：{a_url}，总页数：{a_pager}')
# 从 1 开始循环便利总页数到 a_pager 范围 [1,a_pager+1]
for i in range(1, a_pager + 1):
    # 当为 1 则拼接 a_url 对应的链接赋值给 a_pager_url ，将 a_content 赋值给 a_pager_url_content
    if i == 1:
        a_pager_url = a_url
        a_pager_url_content = a_content
    else:
        # 当不为1 则拼接 a_url + a_pager 得到类似 https://meiru.neocities.org/page/2/ 的拼接其中 /page/2/ 代表第2页之后的拼接以此类推，得到拼接 a_pager_url ，请求 a_pager_url 若为 200 且有内容则返回 a_pager_url_content
        a_pager_url = a_url + '/page/' + str(i) + '/'
        a_pager_url_content = request_with_retry(a_pager_url)

    print(f'第{i}页，网址：{a_pager_url}')

    # 从 a_pager_url_content 中提取全部的链接 b_url
    soup = BeautifulSoup(a_pager_url_content, 'html.parser')
    links = soup.select('div.p-2 div.text-sm.text-gray-500.text-center a[href]')
    b_urls = [link['href'] for link in links]
    b_count = len(b_urls)
    # b_names = [link.text for link in links]
    # 从 0 开始循环便利总数到 b_count 范围 [0,b_count]
    for j in range(b_count):
        # 请求 b_url 对应的链接，若为 200 且有内容则返回 b_content
        b_url = b_urls[j]
        b_content = request_with_retry(b_url)

        # 从 b_content 中获取链接总页数 b_pager
        soup = BeautifulSoup(b_content, 'html.parser')
        last_page_link = int(soup.select_one('div#pagination div:last-child div:last-child a:nth-last-child(2)')['href'].split('/')[-2])
        c_url = soup.select_one('div#pagination div:last-child div:last-child a:nth-last-child(2)')['href'].rsplit('/', 2)[0] + '/'
        b_pager = last_page_link if last_page_link else 1
        print(f'第{j+1}条，网址：{b_url}，总页数：{b_pager}')
        # 从 1 开始循环便利总页数到 b_pager 范围 [1,b_pager+1]
        for k in range(1, b_pager + 1):
            # 当为 1 则将 c_url 对应的链接赋值给 c_b_pager_url ，并将 b_content 赋值给 c_b_pager_url_content
            if k == 1:
                c_b_pager_url = c_url
                c_b_pager_url_content = b_content
            else:
                # 当不为 1 则拼接 c_url+b_pager 得到类似 https://meiru.neocities.org/models/%E5%B9%B4%E5%B9%B4/page/2/ 的拼接，其中 https://meiru.neocities.org/models/%E5%B9%B4%E5%B9%B4/page/ 是 c_url ，2/ 代表第2页之后的拼接以此类推，得到拼接 c_b_pager_url 并请求，若为 200 且有内容则返回 c_b_pager_url_content
                c_b_pager_url = c_url + '/' + str(k) + '/'
                c_b_pager_url_content = request_with_retry(c_b_pager_url)
            # 从 c_b_pager_url_content 中获取全部图片链接 d_url 和文件夹名 d_name
            soup = BeautifulSoup(c_b_pager_url_content, 'html.parser')
            divs = soup.select('div.p-2 div:first-child a[href]')
            d_urls = [div['href'] for div in divs]
            d_names = [div.find('img', {'class': 'rounded-lg shadow-sm w-full h-72 md:h-96 object-cover'})['alt'] for div in divs]
            d_count = len(d_urls)
            
            print(f'第{k}页，网址：{c_b_pager_url}')
            # 从 0 开始循环便利总数到 c_count 范围 [0,c_count]
            for l in range(d_count):
                # 将 b_name 修改为 a_name
                d_name = os.path.join(a_name, d_names[l].replace(' ','-').replace('-–-','-').replace('--','-').replace('#','').replace('@','').lstrip('-').rstrip('-'))
                # 创建对应的 d_name 目录并进入目录，如果存在则不创建目录直接进入目录
                if not os.path.exists(d_name):
                    os.makedirs(d_name)
                os.chdir(d_name)
                print(f'创建目录：{d_name}')
                # 拼接 d_url 对应的链接并请求 若为 200 且有内容则返回 d_content
                d_url = d_urls[l]
                # 判断 c_urls 是否在跳过链接集中，如果存在则打印链接+存在跳过不进行获取 continue 如果不存在则打印链接+不存在，继续运行
                if check_url_exists(d_url):
                    print(f"{d_url} exists.")
                    continue
                else:
                    print(f"{d_url} doesn't exist. run!")
                d_content = request_with_retry(d_url)

                # 从 d_content 中获取全部图片链接 e_url
                soup = BeautifulSoup(d_content, 'html.parser')
                e_urls = [img['src'] for img in soup.select('div#gallery img.block.my-2.mx-auto')]
                e_count = len(e_urls)

                # 从 0 开始循环便利总数到 e_count 范围 [0,e_count]
                for m in range(e_count):
                    # 处理图片链接 e_url 并截取文件名得到 e_name ，检查文件路径中是否与 e_name 重名，如果找到重名文件则代表文件存在也就不用请求图片链接，如果找不到重名文件则说明文件不存在则请求图片链接并存储下载并截取文件名存储到 d_name 目录中，比如获取的链接为 https://telegraph-image.pages.dev/file/dbcc75fbf6f8a11dccbad.jpg 那么存储的文件名就为 dbcc75fbf6f8a11dccbad.jpg 并睡眠3s
                    e_url = e_urls[m]
                    e_name = e_url.split('/')[-1]
                    e_path = os.path.join(d_name, e_name)
                    if not os.path.exists(e_path):
                        print(f'第{m+1}张，网址：{e_url}，存储文件：{e_path}')
                        e_content = request_with_retry(e_url)
                        with open(e_path, 'wb') as f:
                            f.write(e_content)
                    else:
                        print('文件已存在')
                    print('休息3s')
                    time.sleep(3)
