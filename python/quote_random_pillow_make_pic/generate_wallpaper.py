# -*- coding: utf-8 -*-
"""
隨機勵志金句桌布產生器
使用 Pillow 生成 1920x1080 漸層背景桌布，將文字優美地排版在正中央
"""

import random
from PIL import Image, ImageDraw, ImageFont
import os

QUOTES = [
    ('你所付出的努力，不會背叛你。', '努力は必ず報われる。'),
    ('千里之行，始於足下。', 'A journey of a thousand miles begins with a single step.'),
    ('失敗為成功之母。', 'Failure is the mother of success.'),
    ('活在當下，珍惜每一刻。', 'Carpe diem. Seize the day.'),
    ('Never give up. Great things take time.', '永不放棄，偉大的事需要時間。'),
    ('你的極限，只是別人的起點。', '你的極限，只是別人的起點。'),
    ('Believe you can and you are halfway there.', '相信自己，你就已經成功了一半。'),
    ('行動是戰勝恐懼的唯一方法。', '行動は恐怖に打ち勝つ唯一の方法です。'),
    ('天道酬勤。', 'Heaven rewards the diligent.'),
    ('不要等待機會，而要創造機會。', "Don't wait for opportunity, create it."),
    ('今天的努力，是明天的實力。', '今日の努力は明日の実力。'),
    ('與其怨憨，不如埋頭。', '愚痴るより、潜り込め。'),
    ('堅持下去，你比你以為的更堅強。', 'Stay strong. You are tougher than you think.'),
    ('慢慢來，比較快。', 'ゆっくり行けば、遠くまで行ける。'),
    ("Happiness is not a destination, it's a way of life.", '幸福不是終點，而是一種生活方式。'),
    ('夢想還是要有的，萬一實現了呢？', '夢想還是要有的，萬一實現了呢？'),
    ('You are the artist of your own life.', '你是自己人生的藝術家。'),
    ('每一次挫折，都是一次成長。', 'Every setback is a setup for a comeback.'),
    ('不要讓昨天的失敗，耍誤今天的精彩。', "Don't let yesterday's failure ruin today's brilliance."),
    ('自律即自由。', '自律は自由なり。'),
    ('生活不僅有眼前的苟且，還有詩和遠方。', '生活不僅有眼前的苟且，還有詩和遠方。'),
    ('不怕慢，只怕站。', '不怕慢，只怕站。'),
    ('態度決定高度。', 'Attitude determines altitude.'),
    ('做最好的自己。', 'Be your best self.'),
    ('把握現在，就是創造未來。', '把握現在，就是創造未來。'),
    ('人生沒有白走的路，每一步都算數。', '人生沒有白走的路，每一步都算數。'),
    ('盡其在我，成敗不必在我。', '盡其在我，成敗不必在我。'),
    ('心有多大，舞台就有多大。', '心有多大，舞台就有多大。'),
    ('今天不走，明天要跑。', '今天不走，明天要跑。'),
    ('只要有信心，人永遠不會挫敗。', '只要有信心，人永遠不會挫敗。'),
]


def random_gradient_color():
    def rc():
        return (random.randint(40, 220), random.randint(40, 220), random.randint(40, 220))
    return rc(), rc()

def draw_gradient(draw, w, h, c1, c2):
    for y in range(h):
        r = y / h
        draw.line([(0, y), (w, y)], fill=(
            int(c1[0]*(1-r) + c2[0]*r),
            int(c1[1]*(1-r) + c2[1]*r),
            int(c1[2]*(1-r) + c2[2]*r)
        ))

def load_font(size, preferred=None):
    paths = []
    if preferred:
        paths.append(preferred)
    paths += [
        'C:/Windows/Fonts/msjh.ttc',
        'C:/Windows/Fonts/msyh.ttc',
        'C:/Windows/Fonts/simsun.ttc',
        'C:/Windows/Fonts/simfang.ttf',
        'C:/Windows/Fonts/kaiu.ttf',
        'C:/Windows/Fonts/NotoSansCJK-Regular.ttc',
        'C:/Windows/Fonts/NotoSansSC-Regular.otf',
        '/System/Library/Fonts/PingFang.ttc',
        '/System/Library/Fonts/STHeiti Light.ttc',
        '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except:
                continue
    return ImageFont.load_default()

def wrap_text(text, font, max_w):
    lines = []
    for para in text.split("\n"):
        if not para:
            lines.append("")
            continue
        while para:
            for i in range(len(para), 0, -1):
                sub = para[:i]
                bb = font.getbbox(sub)
                if bb[2] - bb[0] <= max_w:
                    lines.append(sub)
                    para = para[i:]
                    break
            else:
                lines.append(para[:1])
                para = para[1:]
    return lines

def create_wallpaper(out='wallpaper.png', w=1920, h=1080, fs1=72, fs2=48, fn=None):
    t1, t2 = random.choice(QUOTES)
    img = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(img)
    c1, c2 = random_gradient_color()
    draw_gradient(draw, w, h, c1, c2)
    ft1 = load_font(fs1, fn)
    ft2 = load_font(fs2, fn)
    bright = (c1[0]+c1[1]+c1[2]+c2[0]+c2[1]+c2[2]) / 6
    tc = (255, 255, 255) if bright < 140 else (30, 30, 30)
    margin = int(w * 0.1)
    mw = w - 2 * margin
    l1 = wrap_text(t1, ft1, mw)
    l2 = wrap_text(t2, ft2, mw)
    ls1 = int(fs1 * 1.6)
    ls2 = int(fs2 * 1.6)
    gap = int(fs1 * 0.6)
    th = len(l1) * ls1 + gap + len(l2) * ls2
    sy = (h - th) // 2
    y = sy
    for line in l1:
        bb = ft1.getbbox(line)
        lw = bb[2] - bb[0]
        x = (w - lw) // 2
        draw.text((x+2, y+2), line, fill=(0, 0, 0, 80), font=ft1)
        draw.text((x, y), line, fill=tc, font=ft1)
        y += ls1
    y += gap
    for line in l2:
        bb = ft2.getbbox(line)
        lw = bb[2] - bb[0]
        x = (w - lw) // 2
        sc = tuple(min(c+60, 255) for c in tc)
        draw.text((x+1, y+1), line, fill=(0, 0, 0, 50), font=ft2)
        draw.text((x, y), line, fill=sc, font=ft2)
        y += ls2
    img.save(out, "PNG")
    print("Wallpaper saved ->", out)
    print(QUOTES[0][0])
    return out

if __name__ == "__main__":
    o = os.path.join(os.path.expanduser("~"), "Desktop", "motivational_wallpaper.png")
    create_wallpaper(out=o)
    print("Done! Check desktop for motivational_wallpaper.png")