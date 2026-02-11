"""
신살(神殺) 계산 모듈
Spiritual Influences Calculation Module

주요 신살: 천을귀인, 역마살, 도화살, 공망, 원진 등
"""

# 천을귀인 (天乙貴人) - 일간 또는 년간 기준
CHEONUL_TABLE = {
    '甲': ['丑', '未'], '戊': ['丑', '未'],
    '乙': ['子', '申'], '己': ['子', '申'],
    '丙': ['亥', '酉'], '丁': ['亥', '酉'],
    '庚': ['丑', '未'], 
    '辛': ['寅', '午'],
    '壬': ['卯', '巳'], 
    '癸': ['卯', '巳']
}

# 역마살 (驛馬殺) - 연지, 일지 기준
YEOKMA_TABLE = {
    '寅': '申', '午': '申', '戌': '申',  # 寅午戌 → 申
    '申': '寅', '子': '寅', '辰': '寅',  # 申子辰 → 寅
    '巳': '亥', '酉': '亥', '丑': '亥',  # 巳酉丑 → 亥
    '亥': '巳', '卯': '巳', '未': '巳'   # 亥卯未 → 巳
}

# 도화살 (桃花殺) - 연지, 일지 기준
DOHWA_TABLE = {
    '寅': '卯', '午': '卯', '戌': '卯',  # 寅午戌 → 卯
    '申': '酉', '子': '酉', '辰': '酉',  # 申子辰 → 酉
    '巳': '午', '酉': '午', '丑': '午',  # 巳酉丑 → 午
    '亥': '子', '卯': '子', '未': '子'   # 亥卯未 → 子
}

# 공망 (空亡) - 일주(60갑자) 기준
# 甲子旬 → 戌亥空, 甲戌旬 → 申酉空, 甲申旬 → 午未空, 甲午旬 → 辰巳空, 甲辰旬 → 寅卯空, 甲寅旬 → 子丑空
GONGMANG_TABLE = {
    # 甲子旬 (0-9)
    '甲子': ['戌', '亥'], '乙丑': ['戌', '亥'], '丙寅': ['戌', '亥'], '丁卯': ['戌', '亥'],
    '戊辰': ['戌', '亥'], '己巳': ['戌', '亥'], '庚午': ['戌', '亥'], '辛未': ['戌', '亥'],
    '壬申': ['戌', '亥'], '癸酉': ['戌', '亥'],
    # 甲戌旬 (10-19)
    '甲戌': ['申', '酉'], '乙亥': ['申', '酉'], '丙子': ['申', '酉'], '丁丑': ['申', '酉'],
    '戊寅': ['申', '酉'], '己卯': ['申', '酉'], '庚辰': ['申', '酉'], '辛巳': ['申', '酉'],
    '壬午': ['申', '酉'], '癸未': ['申', '酉'],
    # 甲申旬 (20-29)
    '甲申': ['午', '未'], '乙酉': ['午', '未'], '丙戌': ['午', '未'], '丁亥': ['午', '未'],
    '戊子': ['午', '未'], '己丑': ['午', '未'], '庚寅': ['午', '未'], '辛卯': ['午', '未'],
    '壬辰': ['午', '未'], '癸巳': ['午', '未'],
    # 甲午旬 (30-39)
    '甲午': ['辰', '巳'], '乙未': ['辰', '巳'], '丙申': ['辰', '巳'], '丁酉': ['辰', '巳'],
    '戊戌': ['辰', '巳'], '己亥': ['辰', '巳'], '庚子': ['辰', '巳'], '辛丑': ['辰', '巳'],
    '壬寅': ['辰', '巳'], '癸卯': ['辰', '巳'],
    # 甲辰旬 (40-49)
    '甲辰': ['寅', '卯'], '乙巳': ['寅', '卯'], '丙午': ['寅', '卯'], '丁未': ['寅', '卯'],
    '戊申': ['寅', '卯'], '己酉': ['寅', '卯'], '庚戌': ['寅', '卯'], '辛亥': ['寅', '卯'],
    '壬子': ['寅', '卯'], '癸丑': ['寅', '卯'],
    # 甲寅旬 (50-59)
    '甲寅': ['子', '丑'], '乙卯': ['子', '丑'], '丙辰': ['子', '丑'], '丁巳': ['子', '丑'],
    '戊午': ['子', '丑'], '己未': ['子', '丑'], '庚申': ['子', '丑'], '辛酉': ['子', '丑'],
    '壬戌': ['子', '丑'], '癸亥': ['子', '丑']
}

# 원진 (怨嗔)
WONJIN_PAIRS = [
    ('子', '未'), ('丑', '午'), ('寅', '巳'), ('卯', '辰'),
    ('申', '亥'), ('酉', '戌')
]

# 육해 (六害)
YUKHAE_PAIRS = [
    ('子', '未'), ('丑', '午'), ('寅', '巳'), ('卯', '辰'),
    ('申', '亥'), ('酉', '戌')
]


def get_cheonul(stem: str, branches: list) -> list:
    """천을귀인 찾기"""
    if stem in CHEONUL_TABLE:
        gwiin_branches = CHEONUL_TABLE[stem]
        found = []
        for branch in branches:
            if branch in gwiin_branches:
                found.append(f"천을귀인({branch})")
        return found
    return []


def get_yeokma(day_branch: str, all_branches: list) -> list:
    """역마살 찾기"""
    if day_branch in YEOKMA_TABLE:
        yeokma = YEOKMA_TABLE[day_branch]
        found = []
        for branch in all_branches:
            if branch == yeokma:
                found.append(f"역마살({branch})")
        return found
    return []


def get_dohwa(day_branch: str, all_branches: list) -> list:
    """도화살 찾기"""
    if day_branch in DOHWA_TABLE:
        dohwa = DOHWA_TABLE[day_branch]
        found = []
        for branch in all_branches:
            if branch == dohwa:
                found.append(f"도화살({branch})")
        return found
    return []


def get_gongmang(day_pillar: str, all_branches: list) -> list:
    """공망 찾기 (일주 기준)"""
    if day_pillar in GONGMANG_TABLE:
        gongmang_branches = GONGMANG_TABLE[day_pillar]
        found = []
        for branch in all_branches:
            if branch in gongmang_branches:
                found.append(f"공망({branch})")
        return found
    return []


def get_wonjin(branches: list) -> list:
    """원진 찾기"""
    found = []
    for i, b1 in enumerate(branches):
        for j, b2 in enumerate(branches):
            if i < j:
                if (b1, b2) in WONJIN_PAIRS or (b2, b1) in WONJIN_PAIRS:
                    found.append(f"원진({b1}-{b2})")
    return found


def get_all_sinsal(day_stem: str, day_branch: str, day_pillar: str, 
                   year_stem: str, year_branch: str,
                   month_branch: str, hour_branch: str) -> dict:
    """
    모든 신살 계산
    
    Returns:
        {
            'cheonul': [...],      # 천을귀인
            'yeokma': [...],       # 역마살
            'dohwa': [...],        # 도화살
            'gongmang': [...],     # 공망
            'wonjin': [...]        # 원진
        }
    """
    all_branches = [year_branch, month_branch, day_branch, hour_branch]
    
    # 천을귀인 (일간과 년간 모두 체크)
    cheonul = get_cheonul(day_stem, all_branches)
    cheonul.extend(get_cheonul(year_stem, all_branches))
    
    return {
        'cheonul': list(set(cheonul)),  # 중복 제거
        'yeokma': get_yeokma(day_branch, all_branches),
        'dohwa': get_dohwa(day_branch, all_branches),
        'gongmang': get_gongmang(day_pillar, all_branches),
        'wonjin': get_wonjin(all_branches)
    }
