import os
import json
import shutil
import imghdr
import concurrent.futures
import requests
import socket

from urllib.parse import unquote, quote
from concurrent import futures


proxies={'http':{}, 'https': {}}

g_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Accept-Encoding": "gzip, deflate, sdch"
}


def baidu_get_image_url_using_api(keywords, max_number=10000, face_only=False):
    def decode_url(url):
        in_table = '0123456789abcdefghijklmnopqrstuvw'
        out_table = '7dgjmoru140852vsnkheb963wtqplifca'
        translate_table = str.maketrans(in_table, out_table)    

        mapping = {'_z2C$q': ':', '_z&e3B': '.', 'AzdH3F': '/'}
        for k, v in mapping.items():
            url = url.replace(k, v)
        return url.translate(translate_table)

    base_url = "https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592"\
               "&lm=7&fp=result&ie=utf-8&oe=utf-8&st=-1"
    keywords_str = "&word={}&queryWord={}".format(
        quote(keywords), quote(keywords))
    query_url = base_url + keywords_str
    query_url += "&face={}".format(1 if face_only else 0)

    init_url = query_url + "&pn=0&rn=30"

    res = requests.get(init_url, headers=g_headers, proxies=proxies)
    init_json = json.loads(res.text.replace(r"\'", "").encode("utf-8"), strict=False)

    total_num = init_json['listNum']
    target_num = min(max_number, total_num)
    crawl_num = min(target_num * 2, total_num)

    crawled_urls = list()
    batch_size = 30

    with futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_list = list()

        def process_batch(batch_no, batch_size):
            image_urls = list()
            url = query_url + \
                "&pn={}&rn={}".format(batch_no * batch_size, batch_size)
            try_time = 0
            while True:
                try:
                    response = requests.get(url, headers=g_headers, proxies=proxies)
                    break
                except Exception as e:
                    try_time += 1
                    if try_time > 3:
                        print(e)
                        return image_urls
            response.encoding = 'utf-8'
            res_json = json.loads(response.text.replace(r"\'", ""), strict=False)
            for data in res_json['data']:
                if 'objURL' in data.keys():
                    url = unquote(decode_url(data['objURL']))
                    if 'src=' in url:
                        url_p1 = url.split('src=')[1]
                        url = url_p1.split('&refer=')[0]
                    image_urls.append(url)
                    # print(url)
                elif 'replaceUrl' in data.keys() and len(data['replaceUrl']) == 2:
                    image_urls.append(data['replaceUrl'][1]['ObjURL'])

            return image_urls

        for i in range(0, int((crawl_num + batch_size - 1) / batch_size)):
            future_list.append(executor.submit(process_batch, i, batch_size))
        for future in futures.as_completed(future_list):
            if future.exception() is None:
                crawled_urls += future.result()
            else:
                print(future.exception())

    return crawled_urls[:min(len(crawled_urls), target_num)]


def download_image(image_url, dst_dir, file_name, timeout=20):
    response = None
    file_path = os.path.join(dst_dir, file_name)
    try_times = 0
    while True:
        try:
            try_times += 1
            response = requests.get(image_url, headers=g_headers, timeout=timeout, proxies=proxies)
            with open(file_path, 'wb') as f:
                f.write(response.content)
            response.close()
            file_type = imghdr.what(file_path)
            # if file_type is not None:
            if file_type in ["jpg", "jpeg", "png", "bmp", "webp"]:
                new_file_name = "{}.{}".format(file_name, file_type)
                new_file_path = os.path.join(dst_dir, new_file_name)
                shutil.move(file_path, new_file_path)
                print("## OK:  {}  {}".format(new_file_name, image_url))
            else:
                os.remove(file_path)
                print("## Err: TYPE({})  {}".format(file_type, image_url))
            break
        except Exception as e:
            if try_times < 3:
                continue
            if response:
                response.close()
            print("## Fail:  {}  {}".format(image_url, e.args))
            break


def download_images(image_urls, dst_dir, file_prefix, concurrency=50, timeout=20):
    socket.setdefaulttimeout(timeout)

    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        future_list = list()
        count = 0
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for image_url in image_urls:
            file_name = file_prefix + '_' +'%d' % count
            future_list.append(executor.submit(
                download_image, image_url, dst_dir, file_name, timeout))
            count += 1
        concurrent.futures.wait(future_list, timeout=180)