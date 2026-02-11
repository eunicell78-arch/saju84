"""
십신(十神) 계산 모듈
Ten Gods Calculator Module
"""

# 천간 한자만 (십신 계산용)
STEMS_HANJA = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']

# 오행 (Five Elements) - 천간별
STEM_TO_ELEMENT = {
    '甲': '木', '乙': '木',
    '丙': '火', '丁': '火',
    '戊': '土', '己': '土',
    '庚': '金', '辛': '金',
    '壬': '水', '癸': '水'
}

# 음양 (Yin-Yang) - 천간별
STEM_TO_YIN_YANG = {
    '甲': '양', '乙': '음',
    '丙': '양', '丁': '음',
    '戊': '양', '己': '음',
    '庚': '양', '辛': '음',
    '壬': '양', '癸': '음'
}

# 오행 상생 관계 (Element Generation)
# 木生火, 火生土, 土生金, 金生水, 水生木
ELEMENT_GENERATION = {
    '木': '火',
    '火': '土',
    '土': '金',
    '金': '水',
    '水': '木'
}

# 오행 상극 관계 (Element Conquest)
# 木克土, 火克金, 土克水, 金克木, 水克火
ELEMENT_CONQUEST = {
    '木': '土',
    '火': '金',
    '土': '水',
    '金': '木',
    '水': '火'
}


def get_sipsin(day_stem: str, target_stem: str) -> str:
    """
    십신 계산 함수
    
    일간(日干)을 기준으로 타 천간과의 관계를 십신으로 분류
    
    Args:
        day_stem: 일간 (한자, 예: '丁')
        target_stem: 비교할 천간 (한자, 예: '戊')
    
    Returns:
        십신 이름 (예: '식신', '편재', '정관' 등)
    """
    # 한자만 추출 (괄호 제거)
    if '(' in day_stem:
        day_stem = day_stem.split('(')[1].rstrip(')')
    if '(' in target_stem:
        target_stem = target_stem.split('(')[1].rstrip(')')
    
    # 일간과 비교 천간의 오행
    day_element = STEM_TO_ELEMENT.get(day_stem)
    target_element = STEM_TO_ELEMENT.get(target_stem)
    
    if not day_element or not target_element:
        return '미상'
    
    # 음양 확인
    day_yy = STEM_TO_YIN_YANG.get(day_stem)
    target_yy = STEM_TO_YIN_YANG.get(target_stem)
    same_yy = (day_yy == target_yy)
    
    # 1. 비겁(比劫): 일간과 같은 오행
    if day_element == target_element:
        if day_stem == target_stem:
            return '비견(比肩)'  # 완전히 동일
        else:
            return '비견(比肩)' if same_yy else '겁재(劫財)'
    
    # 2. 식상(食傷): 일간이 生하는 오행
    if ELEMENT_GENERATION[day_element] == target_element:
        return '식신(食神)' if same_yy else '상관(傷官)'
    
    # 3. 재성(財星): 일간이 克하는 오행
    if ELEMENT_CONQUEST[day_element] == target_element:
        return '편재(偏財)' if same_yy else '정재(正財)'
    
    # 4. 관살(官殺): 일간을 克하는 오행
    if ELEMENT_CONQUEST[target_element] == day_element:
        return '편관(偏官)' if same_yy else '정관(正官)'
    
    # 5. 인성(印星): 일간을 生하는 오행
    if ELEMENT_GENERATION[target_element] == day_element:
        return '편인(偏印)' if same_yy else '정인(正印)'
    
    return '미상'


def get_branch_sipsin(day_stem: str, branch: str) -> str:
    """
    지지의 십신 계산
    
    지지의 본기(本氣)를 기준으로 십신 계산
    
    Args:
        day_stem: 일간 (한자)
        branch: 지지 (한자)
    
    Returns:
        십신 이름
    """
    # 지지의 본기 (장간, 藏干)
    # 간단히 본기만 사용
    BRANCH_MAIN_STEM = {
        '子': '癸',  # 자 = 계수
        '丑': '己',  # 축 = 기토
        '寅': '甲',  # 인 = 갑목
        '卯': '乙',  # 묘 = 을목
        '辰': '戊',  # 진 = 무토
        '巳': '丙',  # 사 = 병화
        '午': '丁',  # 오 = 정화
        '未': '己',  # 미 = 기토
        '申': '庚',  # 신 = 경금
        '酉': '辛',  # 유 = 신금
        '戌': '戊',  # 술 = 무토
        '亥': '壬'   # 해 = 임수
    }
    
    # 한자만 추출
    if '(' in branch:
        branch = branch.split('(')[1].rstrip(')')
    
    main_stem = BRANCH_MAIN_STEM.get(branch)
    if main_stem:
        return get_sipsin(day_stem, main_stem)
    
    return '미상'


def get_sipsin_description(sipsin: str) -> str:
    """
    십신의 의미 설명
    
    Args:
        sipsin: 십신 이름
    
    Returns:
        십신의 간단한 설명
    """
    descriptions = {
        '비견(比肩)': '나와 같은 형제, 동료, 경쟁자',
        '겁재(劫財)': '재물을 빼앗는 자, 경쟁자',
        '식신(食神)': '표현력, 재능, 의식주',
        '상관(傷官)': '창의력, 표현, 관을 상하게 함',
        '편재(偏財)': '움직이는 재물, 사업, 아버지',
        '정재(正財)': '고정재산, 아내(남자), 근면',
        '편관(偏官)': '칠살, 권력, 남편(여자), 폭력',
        '정관(正官)': '명예, 직장, 남편(여자), 법',
        '편인(偏印)': '효도, 학문, 어머니',
        '정인(正印)': '학문, 자격증, 어머니'
    }
    
    return descriptions.get(sipsin, '')


if __name__ == '__main__':
    # 테스트: 2009-12-28생 일간 丁
    day_stem = '丁'
    
    test_cases = [
        ('己', '년간'),  # 己丑
        ('丙', '월간'),  # 丙子
        ('丁', '일간'),  # 丁未
        ('戊', '시간')   # 戊申
    ]
    
    print(f"일간: {day_stem}\n")
    for stem, position in test_cases:
        sipsin = get_sipsin(day_stem, stem)
        desc = get_sipsin_description(sipsin)
        print(f"{position} {stem}: {sipsin}")
        if desc:
            print(f"  → {desc}")
    
    # 지지 테스트
    print("\n지지 십신:")
    test_branches = [
        ('丑', '년지'),
        ('子', '월지'),
        ('未', '일지'),
        ('申', '시지')
    ]
    
    for branch, position in test_branches:
        sipsin = get_branch_sipsin(day_stem, branch)
        print(f"{position} {branch}: {sipsin}")
