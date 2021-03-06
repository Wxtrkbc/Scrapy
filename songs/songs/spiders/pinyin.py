#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os.path

__version__ = '0.9'
__all__ = ["PinYin"]


class PinYin(object):
    def __init__(self, dict_file='songs/spiders/word.data'):
    # def __init__(self, dict_file='word.data'):
        self.word_dict = {}
        self.dict_file = dict_file

    def load_word(self):
        if not os.path.exists(self.dict_file):
            raise IOError("NotFoundFile")

        with open(self.dict_file) as f_obj:
            for f_line in f_obj.readlines():
                try:
                    line = f_line.split('    ')
                    self.word_dict[line[0]] = line[1]
                except:
                    line = f_line.split('   ')
                    self.word_dict[line[0]] = line[1]

    def hanzi2pinyin(self, string=""):
        result = []
        for char in string:
            key = '%X' % ord(char)
            if not self.word_dict.get(key):
                result.append(char)
            else:
                result.append(self.word_dict.get(key, char).split()[0][:-1].lower())

        return result

    def hanzi2pinyin_split(self, string="", split=""):
        result = self.hanzi2pinyin(string=string)
        return split.join(result)


if __name__ == "__main__":
    test = PinYin()
    test.load_word()
    print(test)
    string = "王菲(Faye Wong)"

    print("out: %s" % str(test.hanzi2pinyin_split(string=string, split='').upper()))
