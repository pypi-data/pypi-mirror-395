import re
from collections import Counter

def count_word_frequency(sentence: str):
    # 모두 소문자로 변환
    sentence = sentence.lower()

    # 한글/영어/숫자로 된 단어만 추출
    words = re.findall(r"[0-9a-z가-힣]+", sentence)

    # 단어 빈도 계산
    return Counter(words)
