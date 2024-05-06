# -*- coding: utf-8 -*-
"""
    Created by w at 2024/3/4.
    Description:用【jieba】分词提取关键字，SnowNLP判断词语的情感（适用于购物）
    Changelog: all notable changes to this file will be documented
"""


def test():
    import jieba
    import jieba.analyse
    import jieba.posseg as seg
    from snownlp import SnowNLP

    word_list = ["这个实在是太好用了，我非常的喜欢，下次一定还会购买的！"]
    for analysis_text in word_list:
        # Using the jieba module to cut the analysis_text into a list of words.
        # 全词模式
        analysis_list = list(jieba.cut(analysis_text))
        # 关键词
        print(jieba.analyse.extract_tags(analysis_text))
        # 调整关键词
        jieba.suggest_freq("太好用", True)
        # 删除关键词
        jieba.del_word("游戏")
        # 关键词库的停词 词库
        jieba.analyse.set_stop_words("stop_words.txt")
        # 元组包含单词和标志。
        keywords = [(word.word, word.flag) for word in seg.cut(analysis_text)]
        print(keywords)

        # [('这个', 'r'), ('实在', 'v'), ('是', 'v'), ('太', 'd'), ('好用', 'v'), ('了', 'ul'), ('，', 'x'), ('我', 'r'), ('非常', 'd'), ('的', 'uj'), ('喜欢', 'v'), ('，', 'x'), ('下次', 't'), ('一定', 'd'), ('还', 'd'), ('会', 'v'), ('购买', 'v'), ('的', 'uj'), ('！', 'x')]
        # This is a list comprehension that is creating a list of tuples. Each tuple contains the word and the flag.
        # keywords = [x for x in analysis_words if x[1] in ['a', 'd', 'v']]

        # Printing the list of tuples that were created in the list comprehension.
        # print(keywords)

        # [('实在', 'v'), ('是', 'v'), ('太', 'd'), ('好用', 'v'), ('非常', 'd'), ('喜欢', 'v'), ('一定', 'd'), ('还', 'd'), ('会', 'v'), ('购买', 'v')]
        # Creating a variable called `pos_num` and assigning it the value of 0.
        pos_num = 0

        # Creating a variable called `neg_num` and assigning it the value of 0.
        neg_num = 0

        # This is a for loop that is looping through each word in the list of keywords.
        for word in keywords:
            # Creating a variable called `sl` and assigning it the value of the `SnowNLP` function.
            sl = SnowNLP(word[0])
            # This is an if statement that is checking to see if the sentiment of the word is greater than 0.5.
            if sl.sentiments > 0.5:
                # Adding 1 to the value of `pos_num`.
                pos_num = pos_num + 1
            else:
                # Adding 1 to the value of `neg_num`.
                neg_num = neg_num + 1
            # This is printing the word and the sentiment of the word.
            print(word, str(sl.sentiments))


if __name__ == "__main__":
    test()
