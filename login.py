import sys
from time import sleep
import cv2

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import base64

def create_html_with_embedded_image(image_path, output_path="index.html"):
    """
    创建一个包含嵌入图片的 HTML 文件。

    Args:
        image_path: 图片文件的路径。
        output_path: 输出 HTML 文件的路径。
    """

    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
        return

    mime_type = "image/jpeg"  # 默认 MIME 类型
    if image_path.lower().endswith(".png"):
        mime_type = "image/png"
    elif image_path.lower().endswith(".gif"):
        mime_type = "image/gif"
    elif image_path.lower().endswith(".webp"):
        mime_type = "image/webp"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
    </head>
    <body>
        <img src="data:{mime_type};base64,{encoded_string}" alt="嵌入的图片">
    </body>
    </html>
    """

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)


acccounts = int(len(sys.argv[1:])/2)
print(f'Config {acccounts} accounts')
for i in range(acccounts):
    email = sys.argv[1+i]
    passwd = sys.argv[1+i+acccounts]
    print('----------------------------')
def compare_images_hist(image1_path, image2_path):
    image1 = cv2.imread(image1_path)
    image2 = cv2.imread(image2_path)

    # 计算直方图
    hist1 = cv2.calcHist([image1], [0, 1, 2], None, [256, 256, 256], [0, 256, 0, 256, 0, 256])
    hist2 = cv2.calcHist([image2], [0, 1, 2], None, [256, 256, 256], [0, 256, 0, 256, 0, 256])

    # 归一化直方图
    cv2.normalize(hist1, hist1, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    cv2.normalize(hist2, hist2, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)

    # 计算直方图相似度
    similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
    print(f"Histogram Similarity: {similarity}")
    return similarity

def login():
    #1.open browser
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1000, 720)
    driver.get("https://game.maj-soul.net/1/")
    # print(f'Account {i+1} loading game...')
    sleep(20)

    #2.input email
    screen = driver.find_element(By.ID, 'layaCanvas')
    ActionChains(driver)\
        .move_to_element_with_offset(screen, 250, -100)\
        .click()\
        .perform()
    driver.find_element(By.NAME, 'input').send_keys(email)
    print('Input email successfully')

    #3.input password
    ActionChains(driver)\
        .move_to_element_with_offset(screen, 250, -50)\
        .click()\
        .perform()
    driver.find_element(By.NAME, 'input_password').send_keys(passwd)
    print('Input password successfully')

    #4.login
    ActionChains(driver)\
        .move_to_element_with_offset(screen, 250, 50)\
        .click()\
        .perform()
    print('Entering game...')
    sleep(20) #loading...
    print('Login success')
    driver.get_screenshot_as_file('screenshot.png')
    driver.quit()
    # create_html_with_embedded_image("screenshot.png", "index.html")

retry = 0
threshold = 0.8 
image1_path = 'screenshot.png'
image2_path = 'screenshot_recompress1.jpg'
# ssim_score = compare_images_hist(image1_path, image2_path)
# print(f'retry {retry} times...')
ssim_score = 0.8

while ssim_score>=threshold and retry<3:
    login()
    ssim_score = compare_images_hist(image1_path, image2_path)
    retry +=1
    print(f'retry {retry} times...')
