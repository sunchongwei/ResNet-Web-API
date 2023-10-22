import requests
import json

def translate_word(word):
    """
    翻译单词，将英文翻译为中文
    """
    base_url = r"http://translate.google.com/translate_a/single?client=gtx&dt=t&dj=1&ie=UTF-8&sl=auto&tl=zh-CN&q="
    url  = base_url + word
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        trans_word = data['sentences'][0]['trans']
        return word + '-' + trans_word
    else:
        return word
en_file = "./data/imagenet_classes.txt"
en_list = []
ch_list = []
with open(en_file) as f:
    for w in f.readlines():
        en_word = w.strip()
        en_list.append(en_word)
        ch_word = translate_word(en_word)
        ch_list.append(ch_word)
        print(ch_word)

# 创建文件，保存翻译后的内容
w_file = './data/imagenet_classes_chinese.txt'
with open(w_file, 'w') as f:
    for w in ch_list:
        f.write(w + '\n')
