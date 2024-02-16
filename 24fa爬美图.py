# 思路
'''
    在脚本所在目录下创建 美女图集 文件夹，存在则忽略，并进入文件夹,创建重试函数，为了规避网络问题导致的 tls 报错，并且使用脚本实现需求
    
    定义 a_url 为 https://www.24fa.icu/
    拼接 a_url 和 c49.aspx 得到 b_url
    请求 b_url 若为 200 且有内容则返回 b_url_content
    
    从 b_url_content 中的 <div class="conL"></div> 中获得总页数 b_pager

    从 1 开始循环便利总页数到 b_pager 范围 [1,b_pager]
    当为 1 则直接使用 b_url_content 赋值给 b_url_pager_content
    当不为 1 则处理 b_url 将结尾类似 c49.aspx 的部分中 .aspx 去掉，得到 b_url_cut 用于后续拼接 
    拼接 b_url_cut 和 b_pager 得到类似 https://www.24fa.icu/c49p2.aspx 的拼接其中 p2 代表第一页之后的拼接以此类推，得到拼接 b_url_pager
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
    拼接 c_url_cut 和 c_pager 得到类似 https://www.24fa.icu/n106083c49p1.aspx 的拼接其中 p1 代表第一页之后的拼接以此类推，得到拼接 c_url_pager
    请求 c_url_pager  若为 200 且有内容则返回 c_url_pager_content
    从 c_url_pager_content 中的 <div id="printBody" style="word-break:break-all;"></div> 中匹配获得 upload 开头 .jpg_gzip.aspx 结尾的全部文本 c_url_content_text 并统计数量 c_url_content_text_count
    
    从 1 开始循环遍历总页数到 c_url_content_text_count 范围 [1,c_url_content_text_count]
    处理 c_url_content_text 的每一个文本只截取类似 24011909415963.jpg_gzip.aspx 的部分并且替换 .jpg_gzip.aspx 为 .jpg 作为文件名 filename
    
    拼接 a_url 和 c_url_content_text 得到 d_url
    如果存在则跳过，不存在则请求 d_url 获取图片并保存到 b_url_content_title 目录，并命名为 filename 休息3s
    每次结束一个目录循环休息10s
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

def retry_if_result_none(result):
    """
    定义重试函数，为了规避网络问题导致的报错
    """
    return result is None

def get_filename(c_url_content_text):
    """
    处理 c_url_content_text 的每一个文本只截取类似 24011909415963.jpg_gzip.aspx 的部分并且替换 .jpg_gzip.aspx 为 .jpg 作为文件名 filename
    """
    filename = c_url_content_text.replace(".jpg_gzip.aspx", ".jpg").split('/')[-1]
    return filename

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
    # 在脚本所在目录下创建 美女图集 文件夹，存在则忽略，并进入文件夹
    image_dir = '美女图集'
    os.makedirs(image_dir, exist_ok=True)
    os.chdir(image_dir)
    base_path = os.path.abspath('.')
    print(f'总路径：{base_path}')

    # 定义 a_url
    a_url = 'https://www.24fa.icu/'
    
    # a_url 和 c49.aspx 得到 b_url
    b_url = a_url + 'c49.aspx'

    # 请求 b_url 若为 200 且有内容则返回 b_url_content
    @retry(retry_on_result=retry_if_result_none)
    def _get_b_url_content():
        response = requests.get(b_url,headers=headers)
        if response.status_code == 200 and response.content:
            return response.content
        return None
    b_url_content = _get_b_url_content()
    
    # 从 b_url_content 中的 <div class="conL"></div> 中获得总页数 b_pager
    soup = BeautifulSoup(b_url_content, 'lxml')
    b_pager = int(soup.find('div', class_='conL').find_all('a')[-2].text)
    print(f'网址：{b_url}，总页数：{b_pager}')

    # 从 1 开始循环便利总页数到 b_pager 范围 [1,b_pager]
    for page_num in range(1, b_pager + 1):
        # 当不为 1 则处理 b_url 将结尾类似 c49.aspx 的部分中 .aspx 去掉，得到 b_url_cut后续
        # b_url_cut 和 b_pager 得到类似 https://www.24fa.icu/c49p2.aspx 的其中 p2 代表第一页之后的以此类推，得到 b_url_pager
        b_url_cut = b_url[:-len('.aspx')]
        b_url_pager = f'{b_url_cut}p{page_num}.aspx'
        print(f'第{page_num}页，网址：{b_url_pager}')
        # 当为 1 则直接使用 b_url_content 给他 b_url_pager_content
        if page_num == 1:
            b_url_pager_content = b_url_content
        else:
            """
            从 1 开始循环便利总页数到 b_pager 范围 [1,b_pager]
            当为 1 则直接使用 b_url_content 给 b_url_pager_content
            当不为 1 则处理 b_url 将结尾类似 c49.aspx 的部分中 .aspx 去掉，得到 b_url_cut
            后续 b_url_cut 和 b_pager 得到类似 https://www.24fa.icu/c49p2.aspx 的
            其中 p2 代表第一页之后的以此类推，得到 b_url_pager
            请求 b_url_pager 若为 200 且有内容则返回 b_url_pager_content
            """
            @retry(retry_on_result=retry_if_result_none)
            def _get_b_url_pager_content():
                response = requests.get(b_url_pager,headers=headers)
                if response.status_code == 200 and response.content:
                    return response.content
                return None
            b_url_pager_content = _get_b_url_pager_content()
        # 从 b_url_pager_content 中的 <div class="conL"></div> 中匹配获得以下两个内容，并统计总数量 b_url_content_text_count
        # n 开头 .aspx 结尾的全部文本 b_url_content_text
        # 标题 b_url_content_title
        soup = BeautifulSoup(b_url_pager_content, 'lxml')
        b_url_content_text = [a['href'] for a in soup.find('div', class_='conL').find_all('a') if a['href'].startswith('n') and a['href'].endswith('.aspx')]
        b_url_content_text_count = len(b_url_content_text)
        b_url_content_title = [a.text for a in soup.find('div', class_='conL').find_all('h5') if a.text]

        # 从 1 开始循环便利总页数到 b_url_content_text_count 范围 [1,b_url_content_text_count]
        for i in range(1, b_url_content_text_count + 1):
            # 在当前目录下创建 b_url_content_title 目录，存在则忽略，并进入目录
            image_dir = os.path.join(base_path, b_url_content_title[i-1])
            os.makedirs(image_dir, exist_ok=True)
            os.chdir(image_dir)
            print(f'创建目录：{image_dir}')
            # 拼接 a_url 和 b_url_content_text 中的每一个文本得到 c_url
            c_url = a_url+b_url_content_text[i-1]
            print(f'第{i}条网址：{c_url}')

            # 请求 c_url 若为 200 且有内容则返回 c_url_content
            @retry(retry_on_result=retry_if_result_none)
            def _get_c_url_content():
                response = requests.get(c_url,headers=headers)
                if response.status_code == 200 and response.content:
                    return response.content
                return None
            c_url_content = _get_c_url_content()

            # 从 c_url_content 中的 <div id="printBody" style="word-break:break-all;"></div> 中获得总页数 c_pager
            soup = BeautifulSoup(c_url_content, 'lxml')
            c_pager = int(soup.find('div', id='printBody').find_all('a')[-2].text)
            print(f'网址：{c_url}，总页数{c_pager}')
            # 从 1 开始循环便利总页数到 c_pager 范围 [1,c_pager]
            for page_num in range(1, c_pager + 1):
                # 当不为 1 则处理 c_url 将结尾类似 n106083c49.aspx 的部分中 .aspx 去掉的到 c_url_cut
                # 后续 c_url_cut 和 c_pager 得到类似 https://www.24fa.icu/n106083c49p1.aspx 的
                # 其中 p1 代表第一页之后的以此类推，得到 c_url_pager
                c_url_cut = c_url[:-len('.aspx')]
                c_url_pager = f'{c_url_cut}p{page_num}.aspx'
                print(f'第{page_num}页，网址：{c_url_pager}')
                # 当为 1 则直接使用 c_url_content 给 c_url_pager_content
                if page_num == 1:
                    c_url_pager_content = c_url_content
                else:
                    """
                    从 1 开始循环便利总页数到 c_pager 范围 [1,c_pager]
                    当为 1 则直接使用 c_url_content 给 c_url_pager_content
                    当不为 1 则处理 c_url 将结尾类似 n106083c49.aspx 的部分中 .aspx 去掉的到 c_url_cut
                    后续 c_url_cut 和 c_pager 得到类似 https://www.24fa.icu/n106083c49p1.aspx 的
                    其中 p1 代表第一页之后的以此类推，得到 c_url_pager
                    请求 c_url_pager  若为 200 且有内容则返回 c_url_pager_content
                    """
                    # 请求 c_url_pager  若为 200 且有内容则返回 c_url_pager_content
                    @retry(retry_on_result=retry_if_result_none)
                    def _get_c_url_pager_content():
                        response = requests.get(c_url_pager)
                        if response.status_code == 200 and response.content:
                            return response.content
                        return None
                    c_url_pager_content = _get_c_url_pager_content()

                # 从 c_url_pager_content 中的 <div id="printBody" style="word-break:break-all;"></div> 中匹配获得 upload 开头 .jpg_gzip.aspx 结尾的全部文本 
                # c_url_content_text并统计数量 c_url_content_text_count
                soup = BeautifulSoup(c_url_pager_content, 'lxml')
                c_url_content_text = [img['src'] for img in soup.find('div', id='printBody').find_all('img') if img['src'].startswith('upload/') and img['src'].endswith('.jpg_gzip.aspx')]
                c_url_content_text_count = len(c_url_content_text)
                
                # 从 1 开始循环遍历总页数到 c_url_content_text_count 范围 [1,c_url_content_text_count]
                for i in range(1, c_url_content_text_count + 1):
                    # 处理 c_url_content_text 的每一个文本只截取类似 24011909415963.jpg_gzip.aspx 的部分并且替换 .jpg_gzip.aspx 为 .jpg 作为文件名 filename
                    filename = get_filename(c_url_content_text[i-1])
                   
                    # 拼接 a_url 和 c_url_content_text 得到 d_url
                    d_url = a_url + c_url_content_text[i-1]
                    print(f'第{i}张网址：{d_url}')
                    
                    # 拼接存储路径
                    image_dir = os.path.join(base_path, image_dir)

                    # 如果存在则跳过，不存在则请求 d_url 获取图片并保存到 b_url_content_title 目录，并命名为 filename
                    save_image(d_url, filename, image_dir)
            print('休息50s')
            sleep(50)
        # 返回上一层目录
        os.chdir(base_path)

if __name__ == '__main__':
    main()
