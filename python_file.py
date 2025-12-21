# -*- coding: utf-8 -*-

# 유니코드 상에서 한글 음절의 시작과 끝 코드값
HANGUL_BASE = 0xAC00   # '가'의 코드값
HANGUL_LAST = 0xD7A3   # '힣'의 코드값

# 중성(모음) 개수와 종성(받침) 개수
NUM_JUNG = 21
NUM_JONG = 28

# 한 초성 블록의 크기 (중성 * 종성)
BLOCK = NUM_JUNG * NUM_JONG  # 588

# 초성 리스트 (총 19개)
CHOSEONG_LIST = [
    'ㄱ','ㄲ','ㄴ','ㄷ','ㄸ','ㄹ','ㅁ','ㅂ','ㅃ','ㅅ','ㅆ',
    'ㅇ','ㅈ','ㅉ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ'
]

def choseong_char(ch):
    
    #한 글자의 초성을 반환하는 함수.
    #- 입력: 한글 음절 문자 (예: '가', '힣')
    #- 출력: 해당 글자의 초성 (예: 'ㄱ', 'ㅎ')
    #- 한글 음절이 아닌 경우 원래 문자를 그대로 반환
    
    code = ord(ch)  # 문자 → 유니코드 코드값
    if HANGUL_BASE <= code <= HANGUL_LAST:
        index = (code - HANGUL_BASE) // BLOCK
        return CHOSEONG_LIST[index]
    return ch  # 한글 음절이 아니면 그대로 반환

def choseong(s):
    
    #문자열 전체의 초성을 추출하는 함수.
    #- 입력: 문자열 (예: "안녕하세요")
    #- 출력: 초성 문자열 (예: "ㅇㄴㅎㅅㅇ")
    
    return ''.join(choseong_char(ch) for ch in s)

def hangul(foobar):
    unicode = ord(foobar)
    if HANGUL_BASE <= unicode <= HANGUL_LAST:
        foobar = True
    else:
        foobar = False
