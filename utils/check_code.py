#!/usr/bin/env python
# -*- coding:utf-8 -*-

import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

_letter_cases = "abcdefghjkmnpqrstuvwxy"    # 小写字母，去除可能干扰的i，l，o，z，不希望被访问到
_upper_cases = _letter_cases.upper()        # 大写字母
_numbers = ''.join(map(str, range(3, 10)))  # 数字3-9 返回'3456789'
init_chars = ''.join((_letter_cases, _upper_cases, _numbers))   # 返回'abcdefghjkmnpqrstuvwxyABCDEFGHJKMNPQRSTUVWXY3456789'


def create_validate_code(
        size=(120, 30),             # 图片的大小，格式（宽，高），默认为(120, 30)
        chars=init_chars,           # 允许的字符集合，格式字符串
        img_type="GIF",             # 图片保存的格式，默认为GIF，可选的为GIF，JPEG，TIFF，PNG
        mode="RGB",                 # 图片模式，默认为RGB
        bg_color=(255, 255, 255),   # 背景颜色，默认为白色
        fg_color=(0, 0, 255),       # 前景色，验证码字符颜色，默认为蓝色#0000FF
        font_size=18,               # 验证码字体大小
        font_type="Monaco.ttf",     # 验证码字体，默认为 ae_AlArabiya.ttf
        length=4,                   # 验证码字符个数
        draw_lines=True,            # 是否划干扰线
        n_line=(1, 2),              # 干扰线的条数范围，格式元组，默认为(1, 2)，只有draw_lines为True时有效
        draw_points=True,           # 是否画干扰点
        point_chance=2              # 干扰点出现的概率，大小范围[0, 100]
        ):

    width, height = size  # 宽：120，高：30

    #### 创建图形
    img = Image.new(mode, size, bg_color)   # 创建画布
    draw = ImageDraw.Draw(img)              # 创建画笔

    def get_chars():
        """生成给定长度的字符串，返回列表格式"""
        return random.sample(chars, length)

    def create_lines():
        """绘制干扰线"""
        line_num = random.randint(*n_line)  # 干扰线条数

        for i in range(line_num):
            # 起始点
            begin = (random.randint(0, width), random.randint(0, height))
            # 结束点
            end = (random.randint(0, width), random.randint(0, height))
            draw.line([begin, end], fill=(0, 0, 0))

    def create_points():
        """绘制干扰点"""
        chance = min(100, max(0, int(point_chance)))  # 大小限制在[0, 100]，chance = 2

        for w in range(width):
            for h in range(height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:      # tmp > 98
                    draw.point((w, h), fill=(0, 0, 0))

    def create_strs():
        """绘制验证码字符"""
        c_chars = get_chars()
        strs = ' %s ' % ' '.join(c_chars)  # 每个字符前后以空格隔开

        font = ImageFont.truetype(font_type, font_size)
        font_width, font_height = font.getsize(strs)

        draw.text(((width - font_width) / 3, (height - font_height) / 3),
                  strs, font=font, fill=fg_color)

        return ''.join(c_chars)

    if draw_lines:
        create_lines()

    if draw_points:
        create_points()

    strs = create_strs()

    #### 图形扭曲参数
    params = [1 - float(random.randint(1, 2)) / 100,
              0,
              0,
              0,
              1 - float(random.randint(1, 10)) / 100,
              float(random.randint(1, 2)) / 500,
              0.001,
              float(random.randint(1, 2)) / 500
              ]
    img = img.transform(size, Image.PERSPECTIVE, params)    # 创建扭曲

    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)         # 滤镜，边界加强（阈值更大）

    return img, strs

if __name__ == '__main__':
    a = create_validate_code()