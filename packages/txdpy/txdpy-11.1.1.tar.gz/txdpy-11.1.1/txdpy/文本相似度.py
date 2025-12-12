# -*- coding: utf-8 -*-
class TextSimilar:
    def __init__(self):
        # 安装"paddlepaddle"、"paddlenlp"
        from paddlenlp import Taskflow
        self.similarity = Taskflow("text_similarity")

    def __call__(self, text_1:str, text_2:str):
        """文本相似度
        :param text_1:文本一
        :param text_2:文本二
        :return: 返回文本相似度
        """
        if text_1 == text_2:
            return 1
        return self.similarity([[text_1, text_2]])[0]['similarity']