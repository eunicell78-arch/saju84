"""
십신(十神) 계산 모듈
Ten Gods Calculation Module

십신은 일간(日干)을 기준으로 다른 천간과의 오행 관계를 나타냄
"""

# 오행 관계
ELEMENT_MAP = {
    '甲': '木', '乙': '木',
    '丙': '火', '丁': '火',
    '戊': '土', '己': '土',
    '庚': '金', '辛': '金',
    '壬': '水', '癸': '水'
}

# 음양
YIN_YANG = {
    '甲': '陽', '乙': '陰',
    '丙': '陽', '丁': '陰',
    '戊': '陽', '己': '陰',
    '庚': '陽', '辛': '陰',
    '壬': '陽', '癸': '陰'
}

# 오행 생극 관계
# 상생: 木生火, 火生土, 土生金, 金生水, 水生木
# 상극: 木克土, 火克金, 土克水, 金克木, 水克火

GENERATES = {
    '木': '火',  # 木生火
    '火': '土',  # 火生土
    '土': '金',  # 土生金
    '金': '水',  # 金生水
    '水': '木'   # 水生木
}

CONTROLS = {
    '木': '土',  # 木克土
    '火': '金',  # 火克金
    '土': '水',  # 土克水
    '金': '木',  # 金克木
    '水': '火'   # 水克火
}


def get_sipsin(day_stem: str, target_stem: str) -> str:
    """
    십신 계산
    
    Args:
        day_stem: 일간 (日干) - 한자 형태 예: '甲', '乙', etc.
        target_stem: 대상 천간 - 한자 형태
    
    Returns:
        십신 이름 (비견, 겁재, 식신, 상관, 편재, 정재, 편관, 정관, 편인, 정인)
    """
    # 한자만 추출 (괄호 제거)
    if '(' in day_stem:
        day_stem = day_stem.split('(')[1].replace(')', '')
    if '(' in target_stem:
        target_stem = target_stem.split('(')[1].replace(')', '')
    
    # 같은 천간
    if day_stem == target_stem:
        return '비견'
    
    # 오행 추출
    day_element = ELEMENT_MAP[day_stem]
    target_element = ELEMENT_MAP[target_stem]
    
    # 음양 추출
    day_yy = YIN_YANG[day_stem]
    target_yy = YIN_YANG[target_stem]
    
    same_yy = (day_yy == target_yy)
    
    # 같은 오행 (비겁)
    if day_element == target_element:
        if same_yy:
            return '비견'
        else:
            return '겁재'
    
    # 일간이 생하는 오행 (식상)
    elif GENERATES[day_element] == target_element:
        if same_yy:
            return '식신'
        else:
            return '상관'
    
    # 일간이 극하는 오행 (재성)
    elif CONTROLS[day_element] == target_element:
        if same_yy:
            return '편재'
        else:
            return '정재'
    
    # 일간을 극하는 오행 (관살)
    elif CONTROLS[target_element] == day_element:
        if same_yy:
            return '편관'
        else:
            return '정관'
    
    # 일간을 생하는 오행 (인성)
    elif GENERATES[target_element] == day_element:
        if same_yy:
            return '편인'
        else:
            return '정인'
    
    return '미상'


def get_all_sipsin(day_stem: str, year_stem: str, month_stem: str, hour_stem: str) -> dict:
    """
    사주 전체 십신 계산
    
    Returns:
        {'year': '십신', 'month': '십신', 'day': '일간', 'hour': '십신'}
    """
    return {
        'year': get_sipsin(day_stem, year_stem),
        'month': get_sipsin(day_stem, month_stem),
        'day': '일간',  # 일간 자체
        'hour': get_sipsin(day_stem, hour_stem)
    }
