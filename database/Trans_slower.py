from translate import Translator

def trans_to_chinese(text):
    return Translator(from_lang='en',to_lang='zh').translate(text)

def trans_to_english(text):
    return Translator(from_lang='zh',to_lang='en').translate(text)

if __name__ == '__main__':
    print(trans_to_chinese('Hello')) 
    print(trans_to_english('你好'))    