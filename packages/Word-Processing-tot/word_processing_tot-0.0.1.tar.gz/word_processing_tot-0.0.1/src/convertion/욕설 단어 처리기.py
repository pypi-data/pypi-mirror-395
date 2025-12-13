#욕설->우리말 순화 딕셔너리
curse_mapping = {
    "찐따": "아웃사이더",
    "염병": "장티푸스",
    "존나": "엄청",
    "ㅈㄴ": "엄청",
    "시발": "빌어먹을",
    "ㅅㅂ": "빌어먹을",
    "씨발": "빌어먹을",
    "병신": "어리석은 사람",
    "ㅂㅅ": "어리석은 사람",
    "븅신": "어리석은 사람",
    "개새끼":"못된 아이",
    "개자식":"못된 아이",
    "ㄱㅅㄲ":"못된 아이",
}
def clean_text(text, mode): # 입력받은 문장에서 욕설을 찾아서 순화된 말로 바꾸거나 별표로 대체하는 함수
    # mode = "replace" | "star"
    for swear, replacement in curse_mapping.items(): # 딕셔너리의 각 욕설과 순화된 말을 반복
        if mode == "replace": # 모드가 replace일 때
            text = text.replace(swear, replacement) # 욕설(swear)을 순화된 말(replacement)로 바꿈(swear가 input 문장에 있을 시에만 작동)
        elif mode == "star": # 모드가 star일 때
            text = text.replace(swear, "*" * len(swear)) # 욕설(swear)을 별표(*)로 대체(len(swear)만큼 별표 생성)
    return text 


while True: # 무한 루프를 돌며 사용자 입력을 받음
    users_mode=input("변환 방법을 선택하세요(replace/star): ") # 사용자에게 변환 방법 선택 요청
    if users_mode not in ["replace","star"]: # 잘못된 입력 처리
        print("잘못된 입력입니다. 다시 시도해주세요.")
        continue
    elif users_mode=="replace": # replace 모드 선택 시
        users_input=input("문장을 입력하세요: ") # 사용자에게 문장 입력 요청
        switched_text=clean_text(users_input, mode='replace') # 입력 문장을 clean_text 함수로 처리
        print(switched_text)
    elif users_mode=="star": # star 모드 선택 시
        users_input=input("문장을 입력하세요: ") # 사용자에게 문장 입력 요청
        switched_text=clean_text(users_input, mode='star') # 입력 문장을 clean_text 함수로 처리
        print(switched_text)
        

   

   