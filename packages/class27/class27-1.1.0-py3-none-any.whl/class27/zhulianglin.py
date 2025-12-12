class Class_27:

    # 保留方法
    def __init__(self,name):
        self.name = name

    # 实例方法

    def Print_Weixin(self):
        studict = dict(
            冯雨晨='不要让时代成为你的悲哀',
            杨雨涵='Sakura最好了',
            尤兴亮='我独我，世间第一等，此间最上乘',
            王雨晨='人生没有太晚的开始',
            代广涵='如果你在的话 下雨也是好天气',
            石韦翔='那就把日子交给春暖花开吧，再为自己申请一个瑰丽的梦',
            沈奕凝='Dasseinzumtode',
            孟紫薇='执着于满足别人的期待是一种微妙的自我暴力',
            孙诚治='enjoy life',
            张诗涵='愿余生无忧顺遂',
            刘梓航='是花自然香，何须迎风扬',
            孙翔薪='纯真而不欠闻达，善良而不失坚强',
            窦一轩='快乐肥宅水',
            赵思怡='当你为错过太阳而哭泣时，你也将要错过群星',
            武加轩='一切是最好的安排，所以，请拥抱明天的你',
            王森='梧高凤必至 花香蝶自来',
            王丘迟='zer',
            张宇='不尽人意',
            朱良林='重要事情打电话！！！',
            殷齐乐='理科之王',
            合影='做鹰一样的自己，筑雁一样的集体'
        )
        from PIL import Image
        import tkinter as tk
        import random
        import os


        # 1. 先获取目标文件夹的绝对路径（假设已正确定义）
        target_abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), f"pic/{self.name}"))
        try:
                # 2. 获取文件夹下的所有图片文件（过滤出常见图片后缀）
                # 定义图片后缀（可根据实际情况补充）
                image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
                # 遍历文件夹，筛选出图片文件的完整路径
                image_files = [
                    os.path.join(target_abs_path, filename)
                    for filename in os.listdir(target_abs_path)
                    if filename.lower().endswith(image_extensions)
                ]
                # 3. 随机选择一个图片文件
                if not image_files:
                    print("错误：目标文件夹中没有图片文件")
                else:
                    random_image = random.choice(image_files)
                    img = Image.open(random_image)
                    img.show()  # 显示图片

        except Exception as e:
            print(f"Pillow: 打开图片失败 - {e}")
        if self.name in studict:
            tip = studict[self.name]
        else:
            tip =  '''这人太懒了，连个微信签名都懒得写。
                                                   ——朱'''

        bg_colors = [
                'lightpink', 'skyblue', 'lightgreen', 'lavender', 'lightyellow',
                'plum', 'coral', 'bisque', 'aquamarine', 'mistyrose', 'honeydew',
                'peachpuff', 'paleturquoise', 'lavenderblush', 'oldlace', 'lemonchiffon',
                'lightcyan', 'lightgray', 'lightpink', 'lightsalmon', 'lightseagreen',
                'lightskyblue', 'lightslategray', 'lightsteelblue', 'lightyellow'
            ]
        bg = random.choice(bg_colors)
        window=tk.Tk()
        window.title(f'{self.name}的微信签名')
        label = tk.Label(
                window,
                text=tip,
                bg=bg,
                font=('仿宋', 18),
                width=100,
                height=3
            )
        label.pack()
        window.attributes('-topmost', True)
        window.mainloop()




