import os, requests
from zhipuai import ZhipuAI
from concurrent.futures import ThreadPoolExecutor

'''
智谱 AI 图片生成
'''

client = ZhipuAI(api_key=os.environ.get("ZHIPUAI_API_KEY"))

def get_prompt(actor):
    response = client.chat.completions.create(
        model="glm-4-flash",  # 请填写您要调用的模型名称
        messages=[
            {"role": "user", "content": f"以{actor}为主角，按照天气+地点+{actor}+动作+背景的格式，随机生成一句话，在50字以内。\
             天气可选有阴晴雨雪，动作有坐卧趟睡走跑爬静，背景有山川湖泊城市街道等。"}
        ],
    )
    # print(response.choices[0].message)
    return response.choices[0].message.content

def get_image_url(actor):
    response = client.images.generations(
        model="cogview-3-plus", #填写需要调用的模型编码
        prompt=get_prompt(actor),
    )
    # print(response.data[0].url)
    return response.data[0].url

def save_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"Image saved as {filename}")
    else:
        print(f"Failed to download image from {url}")

# def generate_and_save_images(actor, num_images, path):
#     for i in range(1, num_images + 1):
#         image_url = get_image_url(actor)
#         filename = os.path.join(path, f"{actor}_glm_{i}.png")
#         save_image(image_url, filename)

def generate_and_save_images(actor, start_index, end_index, path):
    for i in range(start_index, end_index):
        image_url = get_image_url(actor)
        filename = os.path.join(path, f"{actor}_glm_{i}.png")
        save_image(image_url, filename)

def generate_and_save_images_multithreaded(actor, num_images, path, max_workers=5):
    images_per_thread = num_images // max_workers
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        start_index = 1
        for i in range(max_workers):
            end_index = start_index + images_per_thread
            if i == max_workers - 1:  # 确保最后一个线程获取所有剩余的图片
                end_index = num_images + 1
            futures.append(executor.submit(generate_and_save_images, actor, start_index, end_index, path))
            start_index = end_index
        for future in futures:
            future.result()  # 等待所有线程完成