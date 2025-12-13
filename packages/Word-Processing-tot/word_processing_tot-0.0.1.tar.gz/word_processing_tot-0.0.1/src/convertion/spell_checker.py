import Levenshtein # pip install python-Levenshtein 필요

class SimpleSpellChecker:
    def __init__(self, dictionary_words):
        self.dictionary = dictionary_words

    def check(self, word):
        # 입력 단어가 사전에 있으면 그대로 반환
        if word in self.dictionary:
            return word
        
        # 사전에 없다면 가장 유사한 단어 찾기
        # (거리, 단어) 튜플의 리스트 생성 후 최소값 반환
        candidates = [(Levenshtein.distance(word, w), w) for w in self.dictionary]
        if not candidates:
            return word
        best_match = min(candidates, key=lambda x: x[0])
        
        return best_match[1] # 가장 가까운 단어 반환
    
    def check_sentence(self, sentence):
        # 문장을 띄어쓰기 기준으로 쪼갭니다 (예: "파이선 공부" -> ["파이선", "공부"])
        words = sentence.split() 
        
        # 쪼개진 단어들을 하나씩 꺼내서 check()를 돌립니다
        corrected_words = []
        for word in words:
            corrected_words.append(self.check(word))
            
        # 교정된 단어들을 다시 합칩니다 (예: "파이썬" + " " + "공부")
        return " ".join(corrected_words)