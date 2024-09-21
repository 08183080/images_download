import os, requests
from zhipuai import ZhipuAI

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

def generate_and_save_images(actor, num_images, path):
    
    for i in range(1, num_images + 1):
        image_url = get_image_url(actor)
        filename = os.path.join(path, f"{actor}_{i}.png")
        save_image(image_url, filename)

def ai_generate_images():
    actor = input("请输入角色名：")
    num_images = int(input("请输入生成图片的数量："))
    path = input("请输入保存路径：")
    generate_and_save_images(actor, num_images, path)


if __name__ == "__main__":
    ai_generate_images()
