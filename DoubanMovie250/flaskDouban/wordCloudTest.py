import sqlite3
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from wordcloud import WordCloud
import jieba
conn = sqlite3.connect('movie250.db')
cur = conn.cursor()
sql = "select introduction from movie250"
data = cur.execute(sql)
text = ""
for item in data:
    text = text + item[0]
print(text)  # 词云所需的数据
cut = jieba.cut(text)
string = ' '.join(cut)
img = Image.open('./static/images/tree.png')
img_arr = np.array(img)
wc = WordCloud(
    background_color='white',
    mask = img_arr,
    font_path = "STHeiti Light.ttc"
)
wc.generate_from_text(string)
fig = plt.figure(1)
plt.imshow(wc)
plt.axis('off')
# plt.show()
plt.savefig('./static/images/treeWord.png')