"""
신살(神殺) 계산 모듈
Spirit Stars Calculation Module
"""

# 천을귀인 (天乙貴人) - 가장 중요한 길신
CHEONUL_TABLE = {
    '甲': ['丑', '未'], '戊': ['丑', '未'],
    '乙': ['子', '申'], '己': ['子', '申'],
    '丙': ['亥', '酉'], '丁': ['亥', '酉'],
    '庚': ['丑', '未'], '辛': ['寅', '午'],
    '壬': ['卯', '巳'], '癸': ['卯', '巳']
}

# 역마살 (驛馬殺) - 이동, 변동
YEOKMA_TABLE = {
    '申子辰': '寅', '寅午戌': '申', '巳酉丑': '亥', '亥卯未': '巳'
}

# 도화살 (桃花殺) - 인기, 이성
DOHWA_TABLE = {
    '申子辰': '酉', '寅午戌': '卯', '巳酉丑': '午', '亥卯未': '子'
}

# 화개살 (華蓋殺) - 예술, 종교, 고독
HWAGAE_TABLE = {
    '申子辰': '辰', '寅午戌': '戌', '巳酉丑': '丑', '亥卯未': '未'
}

# 공망 (空亡) - 60갑자별 공망
# 甲子순~癸亥순 각 10개씩
GONGMANG_TABLE = {
    # 甲子순 (0-9): 戌亥 공망
    0: ['戌', '亥'], 1: ['戌', '亥'], 2: ['戌', '亥'], 3: ['戌', '亥'], 4: ['戌', '亥'],
    5: ['戌', '亥'], 6: ['戌', '亥'], 7: ['戌', '亥'], 8: ['戌', '亥'], 9: ['戌', '亥'],
    # 甲戌순 (10-19): 申酉 공망
    10: ['申', '酉'], 11: ['申', '酉'], 12: ['申', '酉'], 13: ['申', '酉'], 14: ['申', '酉'],
    15: ['申', '酉'], 16: ['申', '酉'], 17: ['申', '酉'], 18: ['申', '酉'], 19: ['申', '酉'],
    # 甲申순 (20-29): 午未 공망
    20: ['午', '未'], 21: ['午', '未'], 22: ['午', '未'], 23: ['午', '未'], 24: ['午', '未'],
    25: ['午', '未'], 26: ['午', '未'], 27: ['午', '未'], 28: ['午', '未'], 29: ['午', '未'],
    # 甲午순 (30-39): 辰巳 공망
    30: ['辰', '巳'], 31: ['辰', '巳'], 32: ['辰', '巳'], 33: ['辰', '巳'], 34: ['辰', '巳'],
    35: ['辰', '巳'], 36: ['辰', '巳'], 37: ['辰', '巳'], 38: ['辰', '巳'], 39: ['辰', '巳'],
    # 甲辰순 (40-49): 寅卯 공망
    40: ['寅', '卯'], 41: ['寅', '卯'], 42: ['寅', '卯'], 43: ['寅', '卯'], 44: ['寅', '卯'],
    45: ['寅', '卯'], 46: ['寅', '卯'], 47: ['寅', '卯'], 48: ['寅', '卯'], 49: ['寅', '卯'],
    # 甲寅순 (50-59): 子丑 공망
    50: ['子', '丑'], 51: ['子', '丑'], 52: ['子', '丑'], 53: ['子', '丑'], 54: ['子', '丑'],
    55: ['子', '丑'], 56: ['子', '丑'], 57: ['子', '丑'], 58: ['子', '丑'], 59: ['子', '丑'],
}


def get_sam_group(branch_hanja: str) -> str:
    """지지의 삼합/방합 그룹 찾기"""
    if branch_hanja in ['申', '子', '辰']:
        return '申子辰'
    elif branch_hanja in ['寅', '午', '戌']:
        return '寅午戌'
    elif branch_hanja in ['巳', '酉', '丑']:
        return '巳酉丑'
    elif branch_hanja in ['亥', '卯', '未']:
        return '亥卯未'
    return ''


def get_cheonul(day_stem_hanja: str, branches: list) -> list:
    """천을귀인 찾기"""
    guiin_branches = CHEONUL_TABLE.get(day_stem_hanja, [])
    found = []
    for branch_hanja in branches:
        if branch_hanja in guiin_branches:
            found.append(f"천을귀인({branch_hanja})")
    return found


def get_yeokma(year_branch_hanja: str, branches: list) -> list:
    """역마살 찾기 (연지 기준)"""
    group = get_sam_group(year_branch_hanja)
    if not group:
        return []
    
    yeokma_branch = YEOKMA_TABLE.get(group, '')
    found = []
    for branch_hanja in branches:
        if branch_hanja == yeokma_branch:
            found.append(f"역마살({branch_hanja})")
    return found


def get_dohwa(year_branch_hanja: str, branches: list) -> list:
    """도화살 찾기 (연지 기준)"""
    group = get_sam_group(year_branch_hanja)
    if not group:
        return []
    
    dohwa_branch = DOHWA_TABLE.get(group, '')
    found = []
    for branch_hanja in branches:
        if branch_hanja == dohwa_branch:
            found.append(f"도화살({branch_hanja})")
    return found


def get_hwagae(year_branch_hanja: str, branches: list) -> list:
    """화개살 찾기 (연지 기준)"""
    group = get_sam_group(year_branch_hanja)
    if not group:
        return []
    
    hwagae_branch = HWAGAE_TABLE.get(group, '')
    found = []
    for branch_hanja in branches:
        if branch_hanja == hwagae_branch:
            found.append(f"화개살({branch_hanja})")
    return found


def get_gongmang(day_pillar_index: int, branches: list) -> list:
    """공망 찾기 (일주 기준)"""
    gongmang_branches = GONGMANG_TABLE.get(day_pillar_index, [])
    found = []
    for branch_hanja in branches:
        if branch_hanja in gongmang_branches:
            found.append(f"공망({branch_hanja})")
    return found


def get_all_sinsal(day_stem_hanja: str, year_branch_hanja: str, 
                   day_pillar_index: int, branches: list) -> dict:
    """모든 신살 계산"""
    return {
        'cheonul': get_cheonul(day_stem_hanja, branches),
        'yeokma': get_yeokma(year_branch_hanja, branches),
        'dohwa': get_dohwa(year_branch_hanja, branches),
        'hwagae': get_hwagae(year_branch_hanja, branches),
        'gongmang': get_gongmang(day_pillar_index, branches)
    }
