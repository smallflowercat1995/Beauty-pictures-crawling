# 思路
'''
    在脚本所在目录下创建 美女图集 文件夹并进入文件夹，如果存在则忽略创建直接进入目录,创建重试函数，为了规避网络问题导致的 tls 报错，并且使用脚本实现需求，
    
    定义 a_url 为 https://fuligirl.top
    请求 a_url 若为 200 且有内容则返回 a_content

    从 a_content 中 <nav class="my-2"></nav> 元素中获得 <div></div> 并从中获取 <span></span> 并从 中获取倒数第二个元素 <a href=""></a> 属性中得到总页数(比如得到了 /?page=308 则返回总页数 308) a_pager

    从 1 开始循环便利总页数到 a_pager 范围 [1,a_pager+1]
    当为 1 则拼接 a_url 对应的链接赋值给 a_pager_url ，将 a_content 赋值给 a_pager_url_content
    当不为1 则拼接 a_url + a_pager 得到类似 https://fuligirl.top/?page=2 的拼接其中 /?page=2 代表第2页之后的拼接以此类推，得到拼接 a_pager_url ，请求 a_pager_url 若为 200 且有内容则返回 a_pager_url_content
    
    从 a_pager_url_content 中 <div class="my-1"></div> 中匹配 <a href=""></a> 和 <h2 class="font-semibold"></h2> 提取全部的链接 b_url 和对应链接 h2 标题名 b_name 并统计返回数量 b_count

    从 0 开始循环便利总数到 b_count 范围 [0,b_count]
    在当前目录下创建对应的 b_name 目录并进入目录，如果存在则不创建目录直接进入目录
    请求 b_url 链接，若为 200 且有内容则返回 b_content

    从 b_content 中 <nav class="my-2"></nav> 元素中获得 <div></div> 并从中获取 <span></span> 并从中获取倒数第二个元素 <a href=""></a> 属性中得到总页数(比如得到了 /?page=11 则返回总页数 11) b_pager ，如果没有获取到 则说明只有1页默认返回 1 即 b_pager=1

    从 1 开始循环便利总页数到 b_pager 范围 [1,b_pager+1]
    当为 1 则直接将 b_content 赋值给 a_b_pager_url_content
    当不为 1 则拼接 b_url 和 b_pager 得到拼接 a_b_pager_url 类似 https://fuligirl.top/albums/3702?page=11 的拼接，其中 https://fuligirl.top/albums/3702 是 b_url， ?page=2 代表第2页之后的拼接以此类推，并请求，若为 200 且有内容则返回 a_b_pager_url_content
    
    从 a_b_pager_url_content 中获取 <div class="pt-4"></div> 元素并从中匹配 <div class="my-1"></div> 并从中匹配全部的 <img class="block my-1" src="" title="" alt=""> 的图像资源并提取其中的src链接为 c_url 并统计总数量 c_count

    从 0 开始循环便利总数到 c_count 范围 [0,c_count]
    请求 c_url 链接 若为 200 且有内容则返回 c_content
    处理图片链接 c_url 并截取文件名得到 c_name ，检查文件路径中是否与 c_name 重名，如果找到重名文件则代表文件存在也就不用请求图片链接，如果找不到重名文件则说明文件不存在则请求图片链接并存储下载并截取文件名存储到 c_name 目录中，比如获取的链接为 https://telegraph-image.pages.dev/file/d9831eb87fbe154411dee.jpg 那么存储的文件名就为 d9831eb87fbe154411dee.jpg 并睡眠3s
'''

import os,time
import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

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

# 在脚本所在目录下创建 美女图集 文件夹并进入文件夹，如果存在则忽略创建直接进入目录
if not os.path.exists("美女图集"):
    os.mkdir("美女图集")
os.chdir("美女图集")
a_name = os.path.abspath('.')
print(f'总路径：{a_name}')

# 定义 a_url 为 https://fuligirl.top
a_url = "https://fuligirl.top"

# 请求 a_url 若为 200 且有内容则返回 a_content
a_content = request_with_retry(a_url)

# 从 a_content 中 <nav class="my-2"></nav> 元素中获得 <div></div> 并从中获取 <span></span> 并从 中获取倒数第二个元素 <a href=""></a> 属性中得到总页数(比如得到了 /?page=308 则返回总页数 308) a_pager
soup = BeautifulSoup(a_content, 'html.parser')
nav = soup.find('nav', {'class': 'my-2'})
div = nav.find('div')
span = div.find('span')
a = span.find_all('a')[-2]
a_pager = int(a['href'].split('=')[-1])
print(f'网址：{a_url}，总页数：{a_pager}')
# 从 1 开始循环便利总页数到 a_pager 范围 [1,a_pager+1]
for i in range(1, a_pager + 1):
    # 当为 1 则拼接 a_url 对应的链接赋值给 a_pager_url ，将 a_content 赋值给 a_pager_url_content
    if i == 1:
        a_pager_url = a_url
        a_pager_url_content = a_content
    # 当不为1 则拼接 a_url + a_pager 得到类似 https://fuligirl.top/?page=2 的拼接其中 /?page=2 代表第2页之后的拼接以此类推，得到拼接 a_pager_url ，请求 a_pager_url 若为 200 且有内容则返回 a_pager_url_content
    else:
        a_pager_url = a_url + "/?page=" + str(i)
        a_pager_url_content = request_with_retry(a_pager_url)

    # 从 a_pager_url_content 中 <div class="my-1"></div> 中匹配 <a href=""></a> 和 <h2 class="font-semibold"></h2> 提取全部的链接 b_url 和对应链接 h2 标题名 b_name 并统计返回数量 b_count
    soup = BeautifulSoup(a_pager_url_content, 'html.parser')
    divs = soup.select('div.my-1:not([class*=" "])')
    b_urls = [div.find('a')['href'] for div in divs]
    b_names = [div.find('h2', {'class': 'font-semibold'}).text for div in divs]
    b_count = len(b_urls)
    print(f'第{i}页，网址：{a_pager_url}')
    # 从 0 开始循环便利总数到 b_count 范围 [0,b_count]
    for j in range(b_count):
        # 在当前目录下创建对应的 b_name 目录并进入目录，如果存在则不创建目录直接进入目录
        b_name = os.path.join(a_name, b_names[j].replace(' ','-').replace('---','-').replace('--','-').replace('#','').replace('@','').lstrip('-').rstrip('-'))
        if not os.path.exists(b_name):
            os.makedirs(b_name)
        os.chdir(b_name)
        print(f'创建目录：{b_name}')

        # 请求 b_url 链接，若为 200 且有内容则返回 b_content
        b_url = b_urls[j]
        b_content = request_with_retry(b_url)

        # 从 b_content 中 <nav class="my-2"></nav> 元素中获得 <div></div> 并从中获取 <span></span> 并从中获取倒数第二个元素 <a href=""></a> 属性中得到总页数(比如得到了 /?page=11 则返回总页数 11) b_pager ，如果没有获取到 则说明只有1页默认返回 1 即 b_pager=1
        soup = BeautifulSoup(b_content, 'html.parser')
        nav = soup.find('nav', {'class': 'my-2'})
        div = nav.find('div')
        span = div.find('span')
        a = span.find_all('a')[-2]
        b_pager = int(a['href'].split('=')[-1]) if a else 1
        print(f'网址：{b_url}，总页数：{b_pager}')
        # 从 1 开始循环便利总页数到 b_pager 范围 [1,b_pager+1]
        for k in range(1, b_pager + 1):
            # 当为 1 则直接将 b_content 赋值给 a_b_pager_url_content
            if k == 1:
                a_b_pager_url=b_url
                a_b_pager_url_content = b_content
            # 当不为 1 则拼接 b_url 和 b_pager 得到拼接 a_b_pager_url 类似 https://fuligirl.top/albums/3702?page=11 的拼接，其中 https://fuligirl.top/albums/3702 是 b_url， ?page=2 代表第2页之后的拼接以此类推，并请求，若为 200 且有内容则返回 a_b_pager_url_content
            else:
                a_b_pager_url = b_url + "?page=" + str(k)
                a_b_pager_url_content = request_with_retry(a_b_pager_url)

            # 从 a_b_pager_url_content 中获取 <div class="pt-4"></div> 元素并从中匹配 <div class="my-1"></div> 并从中匹配全部的 <img class="block my-1" src="" title="" alt=""> 的图像资源并提取其中的src链接为 c_url 并统计总数量 c_count
            soup = BeautifulSoup(a_b_pager_url_content, 'html.parser')
            div = soup.find('div', {'class': 'pt-4'})
            imgs = div.find_all('img', {'class': 'block my-1'})
            c_urls = [img['src'] for img in imgs]
            c_count = len(c_urls)
            print(f'第{k}页，网址：{a_b_pager_url}')
            # 从 0 开始循环便利总数到 c_count 范围 [0,c_count]
            for l in range(c_count):
                # 请求 c_url 链接 若为 200 且有内容则返回 c_content
                c_url = c_urls[l]
                c_content = request_with_retry(c_url)

                # 处理图片链接 c_url 并截取文件名得到 c_name ，检查文件路径中是否与 c_name 重名，如果找到重名文件则代表文件存在也就不用请求图片链接，如果找不到重名文件则说明文件不存在则请求图片链接并存储下载并截取文件名存储到 c_name 目录中，比如获取的链接为 https://telegraph-image.pages.dev/file/d9831eb87fbe154411dee.jpg 那么存储的文件名就为 d9831eb87fbe154411dee.jpg 并睡眠3s
                c_name = c_url.split('/')[-1]
                
                # 如果存在则跳过，不存在则请求 c_url 获取图片并保存到 b_title 目录，并命名为 filename 休息3s
                c_name = os.path.join(b_name, c_name)
                if not os.path.exists(c_name):
                    image_content = request_with_retry(c_url)
                    if image_content is None:
                        print(f"Failed to get image from c_url: {c_url}")
                        continue
                    with open(c_name, 'wb') as f:
                        f.write(image_content)
                    print(f'第{l+1}条，网址：{c_url}，存储路径：{c_name}')
                    print('休息3s')
                    time.sleep(3)
                else:
                    print('文件存在')

            # 每次结束一个目录循环休息10s
            print('休息10s')
            time.sleep(10)
            
        # 返回上一层目录
        os.chdir(a_name)
