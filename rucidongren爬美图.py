# 思路
'''
    在脚本所在目录下创建 美女图集 文件夹并进入文件夹，如果存在则忽略,创建重试函数，为了规避网络问题导致的 tls 报错，并且使用脚本实现需求
        
    定义 a_url 为 https://rucidongren.neocities.org/
    请求 a_url 若为 200 且有内容则返回 b_url_content

    从 b_url_content 中的 <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between"></div> 中获得总页数 b_pager

    从 1 开始循环便利总页数到 b_pager 范围 [1,b_pager]
    当为 1 则 b_url_content 赋值给 b_url_pager 直接请求若为 200 且有内容则返回 b_url_pager_content
    当不为1 则 拼接 b_url 和 b_pager 得到类似 https://rucidongren.neocities.org/page/2 的拼接其中 /page/2 代表第2页之后的拼接以此类推，得到拼接 b_url_pager
    请求 b_url_pager  若为 200 且有内容则返回 b_url_pager_content

    从 b_url_pager_content 中 <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-1 p-1"></div> 中匹配 <div class="p-2"></div> 中匹配 <div class="text-sm text-gray-500 text-center"></div> 中匹配 <a href=""></a> 提取全部的链接 b_url_a 和对应链接名 b_url_a_name 返回数量 b_url_a_count

    从 1 开始循环便利总页数到 b_url_a_count 范围 [0,b_url_a_count]
    在当前目录下创建对应的 b_url_a_name 目录并进入目录，如果存在则忽略
    请求对应的链接 b_url_a 若为 200 且有内容则返回 b_url_a_content

    从 b_url_a_content 中的 <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between"></div> 中获得总页数 b_url_a_pager ，如果没有获取到 <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between"></div> 则说明只有1页默认返回 1 即 b_url_a_pager=1

    从 1 开始循环便利总页数到 b_url_a_pager 范围 [1,b_url_a_pager]
    当为 1 则 b_url_a 赋值给 b_url_a_pager_url 直接请求若为 200 且有内容则返回 b_url_a_pager_url_content
    当不为 1 则拼接 b_url_a 和 b_url_a_pager 得到类似 https://rucidongren.neocities.org/models/%E5%92%AC%E4%B8%80%E5%8F%A3%E5%85%94%E5%A8%98ovo/page/2 的拼接其中 /page/2 代表第2页之后的拼接以此类推，得到拼接 b_url_a_pager_url
    请求 b_url_a_pager_url  若为 200 且有内容则返回 b_url_a_pager_url_content
    从 b_url_a_pager_url_content 中 <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-1 p-1"></div> 中匹配 <div class="p-2"></div> 中匹配 <div></div> 中匹配  <a href=""></a> 的链接 b_url_a_pager_url_link 和 <a href=""></a> 中匹配 <img src="" alt="" class="rounded-lg shadow-sm w-full h-72 md:h-96 object-cover"> 的 alt 文件名 b_url_a_pager_url_name 统计数量 b_url_a_pager_url_link_count


    从 1 开始循环便利总页数到 b_url_a_pager_url_link_count 范围 [0,b_url_a_pager_url_link_count]
    创建对应的 b_url_a_pager_url_name 目录并进入目录，如果存在则忽略
    请求对应的链接 b_url_a_pager_url_link 若为 200 且有内容则返回 b_url_a_pager_url_link_content
    从 b_url_a_pager_url_link_content 中的 <div></div> 中匹配 <div id="gallery"></div> 的 <img src="" alt="" title="" class="block my-2 mx-auto"> 中匹配 src 图片链接 b_url_a_pager_url_link_img 如果文件名存在则跳过，如果文件不存在则请求图片链接并存储下载并截取文件名存储到 b_url_a_pager_url_name 目录中，比如获取的链接为 https://wsrv.nl/?url=telegra.ph/file/070e1eb5914a656ed9853.jpg 那么存储的文件名就为 070e1eb5914a656ed9853.jpg 并睡眠3s
'''

import os
import requests
from bs4 import BeautifulSoup
from time import sleep
from retrying import retry
# 安装必备包 python -m pip install --upgrade pip ; python -m pip install bs4 requests retrying

# 设置请求头，模拟浏览器访问
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0"
}

@retry
def get_response(url):
    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    if response.status_code != 200 or not response.content:
        raise Exception("请求失败")
    return response

def save_image(d_url, filename, b_url_content_title):
    """
    请求 d_url 获取图片并保存到 b_url_content_title 目录，并命名为 filename，如果存在则跳过
    """
    image_path = os.path.join(b_url_content_title, filename)
    if not os.path.exists(image_path):
        response = requests.get(d_url,headers=headers)
        if response.status_code == 200:
            print(f'存储文件：{image_path}')
            with open(image_path, 'wb') as f:
                f.write(response.content)
            print('休息10s')
            sleep(10)
    print('文件已存在')

def main():
    # 在脚本所在目录下创建 美女图集 文件夹，如果存在则忽略
    os.makedirs("美女图集", exist_ok=True)
    os.chdir("美女图集")
    base_path = os.path.abspath('.')
    print(f'总路径：{base_path}')

    # 定义 a_url 为 https://rucidongren.neocities.org/
    a_url = "https://rucidongren.neocities.org/"

    # 请求 a_url 若为 200 且有内容则返回 b_url_content
    b_url_content = get_response(a_url).content

    # 从 b_url_content 中的 <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between"></div> 中获得总页数 b_pager
    b_pager = None
    if b_url_content:
        soup = BeautifulSoup(b_url_content, "html.parser")
        div = soup.find("div", class_="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between")
        if div:
            b_pager = int(div.text.split()[-2])
    print(f'网址：{a_url}，总页数：{b_pager}')
    # 从 1 开始循环便利总页数到 b_pager 范围 [1,b_pager]
    for i in range(1, b_pager + 1):
        # 当不为1 则 拼接 b_url 和 b_pager 得到类似 https://rucidongren.neocities.org/page/2 的拼接其中 /page/2 代表第2页之后的拼接以此类推，得到拼接 b_url_pager
        b_url_pager = a_url + "page/" + str(i)
        print(f'第{i}页，网址：{b_url_pager}')
        # 当为 1 则 b_url_content 赋值给 b_url_pager 直接请求若为 200 且有内容则返回 b_url_pager_content
        if i == 1:
            b_url_pager_content = b_url_content
        else:
            # 请求 b_url_pager  若为 200 且有内容则返回 b_url_pager_content
            b_url_pager_content = get_response(b_url_pager).content

        # 从 b_url_pager_content 中 <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-1 p-1"></div> 中匹配 <div class="p-2"></div> 中匹配 <div class="text-sm text-gray-500 text-center"></div> 中匹配 <a href=""></a> 提取全部的链接 b_url_a 和对应链接名 b_url_a_name 返回数量 b_url_a_count
        b_url_a = []
        b_url_a_name = []
        b_url_a_count = 0
        if b_url_pager_content:
            soup = BeautifulSoup(b_url_pager_content, "html.parser")
            divs = soup.find_all("div", class_="text-sm text-gray-500 text-center")
            for div in divs:
                a = div.find("a")
                if a:
                    b_url_a.append(a["href"])
                    b_url_a_name.append(a.text)
                    b_url_a_count += 1

        # 从 0 开始循环便利总页数到 b_url_a_count 范围 [0,b_url_a_count]
        for j in range(0,b_url_a_count):
            # 在当前目录下创建对应的 b_url_a_name 目录并进入目录，如果存在则忽略
            b_url_a_name_path = os.path.join(base_path, b_url_a_name[j])
            os.makedirs(b_url_a_name_path, exist_ok=True)
            os.chdir(b_url_a_name_path)
            print(f'创建目录：{b_url_a_name_path}')
            # 请求对应的链接 b_url_a 若为 200 且有内容则返回 b_url_a_content
            print(f'第{j+1}条网址：{b_url_a[j]}')
            b_url_a_content = get_response(b_url_a[j]).content
            
            # 从 b_url_a_content 中的 <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between"></div> 中获得总页数 b_url_a_pager ，如果没有获取到 <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between"></div> 则说明只有1页默认返回 1 即 b_url_a_pager=1
            b_url_a_pager = 1
            if b_url_a_content:
                soup = BeautifulSoup(b_url_a_content, "html.parser")
                div = soup.find("div", class_="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between")
                if div:
                    b_url_a_pager = int(div.text.split()[-2])
            print(f'网址：{b_url_a[j]}，总页数：{b_url_a_pager}')
            # 从 1 开始循环便利总页数到 b_url_a_pager 范围 [1,b_url_a_pager]
            for k in range(1, b_url_a_pager + 1):
                # 当不为 1 则拼接 b_url_a 和 b_url_a_pager 得到类似 https://rucidongren.neocities.org/models/%E5%92%AC%E4%B8%80%E5%8F%A3%E5%85%94%E5%A8%98ovo/page/2 的拼接其中 /page/2 代表第2页之后的拼接以此类推，得到拼接 b_url_a_pager_url
                b_url_a_pager_url = b_url_a[j] + "/page/" + str(k)
                print(f'第{k}页，网址：{b_url_a_pager_url}')
                # 当为 1 则 b_url_a 赋值给 b_url_a_pager_url 直接请求若为 200 且有内容则返回 b_url_a_pager_url_content
                if k == 1:
                    b_url_a_pager_url = b_url_a[j]
                    b_url_a_pager_url_content = b_url_a_content
                else:
                    # 请求 b_url_a_pager_url  若为 200 且有内容则返回 b_url_a_pager_url_content
                    b_url_a_pager_url_content = get_response(b_url_a_pager_url).content

                # 从 b_url_a_pager_url_content 中 <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-1 p-1"></div> 中匹配 <div class="p-2"></div> 中匹配 <div></div> 中匹配  <a href=""></a> 的链接 b_url_a_pager_url_link 和 <a href=""></a> 中匹配 <img src="" alt="" class="rounded-lg shadow-sm w-full h-72 md:h-96 object-cover"> 的 alt 文件名 b_url_a_pager_url_name 统计数量 b_url_a_pager_url_link_count
                b_url_a_pager_url_link = []
                b_url_a_pager_url_name = []
                b_url_a_pager_url_link_count = 0
                if b_url_a_pager_url_content:
                    soup = BeautifulSoup(b_url_a_pager_url_content, "html.parser")
                    divs = soup.find_all("div", class_="p-2")
                    for div in divs:
                        a = div.find("a")
                        if a:
                            b_url_a_pager_url_link.append(a["href"])
                            img = a.find("img")
                            if img:
                                b_url_a_pager_url_name.append(img["alt"])
                                b_url_a_pager_url_link_count += 1

                # 从 1 开始循环便利总页数到 b_url_a_pager_url_link_count 范围 [0,b_url_a_pager_url_link_count]
                for l in range(0,b_url_a_pager_url_link_count):
                    # 创建对应的 b_url_a_pager_url_name 目录并进入目录，如果存在则忽略
                    b_url_a_pager_url_name_path = os.path.join(b_url_a_name_path, b_url_a_pager_url_name[l])
                    os.makedirs(b_url_a_pager_url_name_path, exist_ok=True)
                    os.chdir(b_url_a_pager_url_name_path)
                    print(f'创建目录：{b_url_a_pager_url_name_path}')
                    # 请求对应的链接 b_url_a_pager_url_link 若为 200 且有内容则返回 b_url_a_pager_url_link_content
                    print(f'第{l+1}条网址：{b_url_a_pager_url_link[l]}')
                    b_url_a_pager_url_link_content = get_response(b_url_a_pager_url_link[l]).content
                    
                    # 从 b_url_a_pager_url_link_content 中的 <div></div> 中匹配 <div id="gallery"></div> 的 <img src="" alt="" title="" class="block my-2 mx-auto"> 中匹配 src 图片链接 b_url_a_pager_url_link_img 并存储循环遍历下载并截取文件名存储到 b_url_a_pager_url_name 目录中，比如获取的链接为 https://wsrv.nl/?url=telegra.ph/file/070e1eb5914a656ed9853.jpg 那么存储的文件名就为 070e1eb5914a656ed9853.jpg
                    b_url_a_pager_url_link_img = []
                    if b_url_a_pager_url_link_content:
                        soup = BeautifulSoup(b_url_a_pager_url_link_content, "html.parser")
                        div = soup.find("div", id="gallery")
                        if div:
                            imgs = div.find_all("img")
                            for img in imgs:
                                b_url_a_pager_url_link_img.append(img["src"])
                    
                    # 循环遍历下载并截取文件名存储到 b_url_a_pager_url_name 目录中
                    for m in range(0,len(b_url_a_pager_url_link_img)):
                        img_url = b_url_a_pager_url_link_img[m]
                        file_name = img_url.split("/")[-1]
                        print(f'第{m+1}张网址：{img_url}')
                        save_image(img_url, file_name, b_url_a_pager_url_name_path)

                    # 返回上一级目录
                    os.chdir(b_url_a_name_path)
                    print('休息50s')
                    sleep(50)
            # 返回上一级目录
            os.chdir(base_path)


if __name__ == "__main__":
    main()
