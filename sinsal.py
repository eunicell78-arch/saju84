"""
신살(神殺) 계산 모듈
Spirit Stars Calculator Module
"""

# 천을귀인 (天乙貴人) - 가장 길한 귀인
CHEONUL_TABLE = {
    '甲': ['丑', '未'], '戊': ['丑', '未'],
    '乙': ['子', '申'], '己': ['子', '申'],
    '丙': ['亥', '酉'], '丁': ['亥', '酉'],
    '庚': ['丑', '未'], '辛': ['寅', '午'],
    '壬': ['卯', '巳'], '癸': ['卯', '巳']
}

# 역마살 (驛馬殺) - 이동, 변동
# 년지/일지 기준
YEOKMA_TABLE = {
    '寅': '申', '午': '申', '戌': '申',  # 寅午戌 삼합 → 申
    '申': '寅', '子': '寅', '辰': '寅',  # 申子辰 삼합 → 寅
    '巳': '亥', '酉': '亥', '丑': '亥',  # 巳酉丑 삼합 → 亥
    '亥': '巳', '卯': '巳', '未': '巳'   # 亥卯未 삼합 → 巳
}

# 도화살 (桃花殺) - 이성, 매력, 예술
DOHWA_TABLE = {
    '寅': '卯', '午': '卯', '戌': '卯',  # 寅午戌 → 卯
    '申': '酉', '子': '酉', '辰': '酉',  # 申子辰 → 酉
    '巳': '午', '酉': '午', '丑': '午',  # 巳酉丑 → 午
    '亥': '子', '卯': '子', '未': '子'   # 亥卯未 → 子
}

# 공망 (空亡) - 60갑자별
# 일주 기준으로 판단
GONGMANG_TABLE = {
    # 갑자순 (甲子~癸酉): 戌亥 공망
    '甲子': ['戌', '亥'], '乙丑': ['戌', '亥'], '丙寅': ['戌', '亥'], '丁卯': ['戌', '亥'],
    '戊辰': ['戌', '亥'], '己巳': ['戌', '亥'], '庚午': ['戌', '亥'], '辛未': ['戌', '亥'],
    '壬申': ['戌', '亥'], '癸酉': ['戌', '亥'],
    # 갑술순 (甲戌~癸未): 申酉 공망
    '甲戌': ['申', '酉'], '乙亥': ['申', '酉'], '丙子': ['申', '酉'], '丁丑': ['申', '酉'],
    '戊寅': ['申', '酉'], '己卯': ['申', '酉'], '庚辰': ['申', '酉'], '辛巳': ['申', '酉'],
    '壬午': ['申', '酉'], '癸未': ['申', '酉'],
    # 갑신순 (甲申~癸巳): 午未 공망
    '甲申': ['午', '未'], '乙酉': ['午', '未'], '丙戌': ['午', '未'], '丁亥': ['午', '未'],
    '戊子': ['午', '未'], '己丑': ['午', '未'], '庚寅': ['午', '未'], '辛卯': ['午', '未'],
    '壬辰': ['午', '未'], '癸巳': ['午', '未'],
    # 갑오순 (甲午~癸卯): 辰巳 공망
    '甲午': ['辰', '巳'], '乙未': ['辰', '巳'], '丙申': ['辰', '巳'], '丁酉': ['辰', '巳'],
    '戊戌': ['辰', '巳'], '己亥': ['辰', '巳'], '庚子': ['辰', '巳'], '辛丑': ['辰', '巳'],
    '壬寅': ['辰', '巳'], '癸卯': ['辰', '巳'],
    # 갑진순 (甲辰~癸丑): 寅卯 공망
    '甲辰': ['寅', '卯'], '乙巳': ['寅', '卯'], '丙午': ['寅', '卯'], '丁未': ['寅', '卯'],
    '戊申': ['寅', '卯'], '己酉': ['寅', '卯'], '庚戌': ['寅', '卯'], '辛亥': ['寅', '卯'],
    '壬子': ['寅', '卯'], '癸丑': ['寅', '卯'],
    # 갑인순 (甲寅~癸亥): 子丑 공망
    '甲寅': ['子', '丑'], '乙卯': ['子', '丑'], '丙辰': ['子', '丑'], '丁巳': ['子', '丑'],
    '戊午': ['子', '丑'], '己未': ['子', '丑'], '庚申': ['子', '丑'], '辛酉': ['子', '丑'],
    '壬戌': ['子', '丑'], '癸亥': ['子', '丑']
}

# 원진 (怨瞋) - 원한과 시기
WONJIN_PAIRS = [
    ('子', '未'), ('丑', '午'), ('寅', '巳'),
    ('卯', '辰'), ('申', '亥'), ('酉', '戌')
]

# 양인 (羊刃) - 강한 칼날, 폭력성
YANGIN_TABLE = {
    '甲': '卯', '乙': '寅',
    '丙': '午', '丁': '巳',
    '戊': '午', '己': '巳',
    '庚': '酉', '辛': '申',
    '壬': '子', '癸': '亥'
}


def extract_hanja(text: str) -> str:
    """괄호가 있는 텍스트에서 한자만 추출"""
    if '(' in text:
        return text.split('(')[1].rstrip(')')
    return text


def get_cheonul_gwiin(year_stem: str, month_stem: str, day_stem: str, branches: list) -> list:
    """
    천을귀인 확인
    
    Args:
        year_stem: 년간
        month_stem: 월간
        day_stem: 일간
        branches: 4개 지지 리스트 [년지, 월지, 일지, 시지]
    
    Returns:
        천을귀인이 있는 위치 리스트 (예: ['년지', '시지'])
    """
    # 일간 기준으로 천을귀인 확인 (년간, 월간도 참고 가능)
    day_stem = extract_hanja(day_stem)
    gwiin_branches = CHEONUL_TABLE.get(day_stem, [])
    
    positions = ['년지', '월지', '일지', '시지']
    result = []
    
    for i, branch in enumerate(branches):
        branch = extract_hanja(branch)
        if branch in gwiin_branches:
            result.append(positions[i])
    
    return result


def get_yeokma(branches: list) -> list:
    """
    역마살 확인 (년지 또는 일지 기준)
    
    Args:
        branches: 4개 지지 리스트
    
    Returns:
        역마살이 있는 위치 리스트
    """
    positions = ['년지', '월지', '일지', '시지']
    result = []
    
    # 년지 기준
    year_branch = extract_hanja(branches[0])
    yeokma_branch = YEOKMA_TABLE.get(year_branch)
    
    if yeokma_branch:
        for i, branch in enumerate(branches):
            branch = extract_hanja(branch)
            if branch == yeokma_branch:
                result.append(positions[i])
    
    return result


def get_dohwa(branches: list) -> list:
    """
    도화살 확인 (년지 또는 일지 기준)
    
    Args:
        branches: 4개 지지 리스트
    
    Returns:
        도화살이 있는 위치 리스트
    """
    positions = ['년지', '월지', '일지', '시지']
    result = []
    
    # 년지 기준
    year_branch = extract_hanja(branches[0])
    dohwa_branch = DOHWA_TABLE.get(year_branch)
    
    if dohwa_branch:
        for i, branch in enumerate(branches):
            branch = extract_hanja(branch)
            if branch == dohwa_branch:
                result.append(positions[i])
    
    return result


def get_gongmang(day_pillar: str, branches: list) -> list:
    """
    공망 확인 (일주 기준)
    
    Args:
        day_pillar: 일주 (예: '丁未')
        branches: 4개 지지 리스트
    
    Returns:
        공망에 해당하는 위치 리스트
    """
    positions = ['년지', '월지', '일지', '시지']
    result = []
    
    gongmang_branches = GONGMANG_TABLE.get(day_pillar, [])
    
    for i, branch in enumerate(branches):
        branch = extract_hanja(branch)
        if branch in gongmang_branches:
            result.append(positions[i])
    
    return result


def get_wonjin(branches: list) -> list:
    """
    원진 확인 (지지 간 충돌)
    
    Args:
        branches: 4개 지지 리스트
    
    Returns:
        원진 관계 리스트 (예: ['년지-시지(子-未)'])
    """
    positions = ['년지', '월지', '일지', '시지']
    result = []
    
    branches_hanja = [extract_hanja(b) for b in branches]
    
    # 모든 지지 쌍 확인
    for i in range(len(branches_hanja)):
        for j in range(i+1, len(branches_hanja)):
            pair = (branches_hanja[i], branches_hanja[j])
            reverse_pair = (branches_hanja[j], branches_hanja[i])
            
            if pair in WONJIN_PAIRS or reverse_pair in WONJIN_PAIRS:
                result.append(f"{positions[i]}-{positions[j]}({branches_hanja[i]}-{branches_hanja[j]})")
    
    return result


def get_yangin(day_stem: str, branches: list) -> list:
    """
    양인 확인 (일간 기준)
    
    Args:
        day_stem: 일간
        branches: 4개 지지 리스트
    
    Returns:
        양인이 있는 위치 리스트
    """
    positions = ['년지', '월지', '일지', '시지']
    result = []
    
    day_stem = extract_hanja(day_stem)
    yangin_branch = YANGIN_TABLE.get(day_stem)
    
    if yangin_branch:
        for i, branch in enumerate(branches):
            branch = extract_hanja(branch)
            if branch == yangin_branch:
                result.append(positions[i])
    
    return result


if __name__ == '__main__':
    # 테스트: 2009-12-28생 己丑 丙子 丁未 戊申
    print("=== 신살 테스트: 2009-12-28생 ===")
    year_stem, month_stem, day_stem = '己', '丙', '丁'
    branches = ['丑', '子', '未', '申']
    day_pillar = '丁未'
    
    print(f"사주: 己丑 丙子 丁未 戊申\n")
    
    cheonul = get_cheonul_gwiin(year_stem, month_stem, day_stem, branches)
    print(f"천을귀인: {cheonul if cheonul else '없음'}")
    
    yeokma = get_yeokma(branches)
    print(f"역마살: {yeokma if yeokma else '없음'}")
    
    dohwa = get_dohwa(branches)
    print(f"도화살: {dohwa if dohwa else '없음'}")
    
    gongmang = get_gongmang(day_pillar, branches)
    print(f"공망: {gongmang if gongmang else '없음'}")
    
    wonjin = get_wonjin(branches)
    print(f"원진: {wonjin if wonjin else '없음'}")
    
    yangin = get_yangin(day_stem, branches)
    print(f"양인: {yangin if yangin else '없음'}")
