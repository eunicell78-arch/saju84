"""
십신(十神) 계산 모듈
Ten Gods Calculation Module
"""

# 천간 한자만
STEMS_HANJA = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']

# 천간 오행
STEM_ELEMENTS_HANJA = {
    '甲': '木', '乙': '木',
    '丙': '火', '丁': '火',
    '戊': '土', '己': '土',
    '庚': '金', '辛': '金',
    '壬': '水', '癸': '水'
}

# 음양 판별
def is_yang_stem(stem_hanja: str) -> bool:
    """천간이 양간인지 판별"""
    yang_stems = ['甲', '丙', '戊', '庚', '壬']
    return stem_hanja in yang_stems


# 오행 생극 관계
def get_element_relation(day_element: str, target_element: str) -> str:
    """
    일간 오행과 타 오행의 관계
    - 같음: 비겁
    - 생함: 식상
    - 극함: 재성
    - 극당함: 관살
    - 생당함: 인성
    """
    # 오행 생극 규칙
    # 木生火, 火生土, 土生金, 金生水, 水生木
    # 木克土, 火克金, 土克水, 金克木, 水克火
    
    sheng_map = {
        '木': '火', '火': '土', '土': '金', '金': '水', '水': '木'
    }
    
    keuk_map = {
        '木': '土', '火': '金', '土': '水', '金': '木', '水': '火'
    }
    
    if day_element == target_element:
        return '비겁'  # 같은 오행
    elif sheng_map[day_element] == target_element:
        return '식상'  # 일간이 생하는 오행
    elif keuk_map[day_element] == target_element:
        return '재성'  # 일간이 극하는 오행
    elif keuk_map[target_element] == day_element:
        return '관살'  # 일간을 극하는 오행
    elif sheng_map[target_element] == day_element:
        return '인성'  # 일간을 생하는 오행
    else:
        return '기타'


def get_sipsin(day_stem_hanja: str, target_stem_hanja: str) -> str:
    """
    십신 계산
    일간을 기준으로 타 천간의 십신을 계산
    """
    # 오행 추출
    day_element = STEM_ELEMENTS_HANJA[day_stem_hanja]
    target_element = STEM_ELEMENTS_HANJA[target_stem_hanja]
    
    # 음양 판별
    day_yang = is_yang_stem(day_stem_hanja)
    target_yang = is_yang_stem(target_stem_hanja)
    same_yin_yang = (day_yang == target_yang)
    
    # 오행 관계
    relation = get_element_relation(day_element, target_element)
    
    # 십신 결정
    if relation == '비겁':
        if day_stem_hanja == target_stem_hanja:
            return '비견'  # 완전히 같음
        elif same_yin_yang:
            return '비견'  # 같은 오행, 같은 음양
        else:
            return '겁재'  # 같은 오행, 다른 음양
    elif relation == '식상':
        if same_yin_yang:
            return '식신'  # 같은 음양
        else:
            return '상관'  # 다른 음양
    elif relation == '재성':
        if same_yin_yang:
            return '편재'  # 같은 음양
        else:
            return '정재'  # 다른 음양
    elif relation == '관살':
        if same_yin_yang:
            return '편관'  # 같은 음양 (칠살)
        else:
            return '정관'  # 다른 음양
    elif relation == '인성':
        if same_yin_yang:
            return '편인'  # 같은 음양 (도식)
        else:
            return '정인'  # 다른 음양
    else:
        return '기타'


def get_sipsin_for_branch(day_stem_hanja: str, branch_hanja: str) -> str:
    """
    지지의 십신 계산
    지지 본기 기준으로 계산
    """
    # 지지의 본기(장간) - 대표 천간
    branch_main_stem = {
        '子': '癸', '丑': '己', '寅': '甲', '卯': '乙',
        '辰': '戊', '巳': '丙', '午': '丁', '未': '己',
        '申': '庚', '酉': '辛', '戌': '戊', '亥': '壬'
    }
    
    main_stem = branch_main_stem.get(branch_hanja, '甲')
    return get_sipsin(day_stem_hanja, main_stem)
