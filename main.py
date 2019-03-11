from urllib.request import urlopen
from collections import OrderedDict
import re
import string


from wordcloud import WordCloud, ImageColorGenerator
import numpy as np
import PIL.Image as Image



def cleanInput(input):
    input = re.sub('\s+', ' ', input).lower()
    input = re.sub('\[[0-9]\]', '', input)
    input = re.sub(' +', ' ', input)
    input = bytes(input, 'utf-8')
    input = input.decode('ascii', 'ignore')
    cleanInput=[]
    input = input.split(' ')
    for item in input:
        item = item.strip(string.punctuation)
        if len(item) > 1 or (item.lower() == 'a' or item.lower() == 'i'):
            cleanInput.append(item)
    return cleanInput

#去除无意义词汇（停用词）
def isCommon(ngram):
    commonWords = ["the", "be", "and", "of", "a", "in", "to", "have", "it",
    "i", "that", "for", "you", "he", "with", "on", "do", "say", "this",
    "they", "is", "an", "at", "but","we", "his", "from", "that", "not",
    "by", "she", "or", "as", "what", "go", "their","can", "who", "get",
    "if", "would", "her", "all", "my", "make", "about", "know", "will",
    "as", "up", "one", "time", "has", "been", "there", "year", "so",
    "think", "when", "which", "them", "some", "me", "people", "take",
    "out", "into", "just", "see", "him", "your", "come", "could", "now",
    "than", "like", "other", "how", "then", "its", "our", "two", "more",
    "these", "want", "way", "look", "first", "also", "new", "because",
    "day", "more", "use", "no", "man", "find", "here", "thing", "give",
    "many", "well"]
    for word in ngram:
        if word in commonWords:
            return True
    return False

def grams(input, n):
    input = cleanInput(input)
    output = {}
    for i in range(len(input) -n +1):
        ngramTemp = ' '.join(input[i:i+n])
        if not isCommon(ngramTemp.split()):
            if ngramTemp not in output:
                output[ngramTemp] = 0
            output[ngramTemp] += 1
    return output

#找出高频词组所对应的句子
def getFirstSentenceContaining(ngram, content):
    print(ngram)
    sentences = content.split('.')
    for sentence in sentences:
        if ngram in sentence:
            return sentence
    return ""


def make_cloud(dict_):
    #字体
    font = r'SourceSerifPro-BoldIt.ttf'
    coloring = np.array(Image.open("img3.jpg"))  # 遮罩层自己定义，可选自己的图片
    # wc = WordCloud(background_color="white",
    #                collocations=False,
    #                font_path=font,
    #                width=1400,
    #                height=1400,
    #                margin=2,
    #                mask=coloring).generate_from_frequencies(dict_)

    wc = WordCloud(background_color="white", max_words=2000,
              mask=coloring, max_font_size=60, random_state=42, scale=2,
              font_path=font).generate_from_frequencies(dict_)



    # 这里采用了generate_from_frequencies(dict_)的方法，里面传入的值是{‘歌手1’:5,‘歌手2’:8,},分别是歌手及出现次数，其实和jieba分词
    # 之后使用generate(text)是一个效果，只是这里的text已经被jieba封装成字典了

    # 从图像创建着色
    image_colors = ImageColorGenerator(coloring)

    wc.recolor(color_func=image_colors)

    wc.to_file('report.png')  # 把词云保存下来

if __name__ == '__main__':
    content = str(urlopen("http://pythonscraping.com/files/inaugurationSpeech.txt").read())
    ngrams = grams(content, 2)
    sortedNGrams = OrderedDict(sorted(ngrams.items(), key=lambda t:t[1], reverse=True))
    print(sortedNGrams)
    print('\n\n')

    #显示句子
    count = 0
    for key in sortedNGrams.keys():
        sentence = getFirstSentenceContaining(key, content.lower())
        print(sentence)
        print('\n')
        count += 1
        if count == 4:
            break

    make_cloud(sortedNGrams)
