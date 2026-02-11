"""
형충회합(刑沖會合) 계산 모듈
Punishment, Clash, Combination Module

지지 간의 형(刑), 충(沖), 합(合) 관계 분석
"""

# 지지 충(沖) - 정면 대립
CHUNG_PAIRS = {
    '子': '午', '午': '子',
    '丑': '未', '未': '丑',
    '寅': '申', '申': '寅',
    '卯': '酉', '酉': '卯',
    '辰': '戌', '戌': '辰',
    '巳': '亥', '亥': '巳'
}

# 육합(六合) - 두 지지의 조화
YUKHAP_PAIRS = {
    '子': '丑', '丑': '子',
    '寅': '亥', '亥': '寅',
    '卯': '戌', '戌': '卯',
    '辰': '酉', '酉': '辰',
    '巳': '申', '申': '巳',
    '午': '未', '未': '午'
}

# 삼합(三合) - 세 지지가 모여 하나의 오행 형성
SAMHAP_GROUPS = {
    '水局': ['申', '子', '辰'],
    '木局': ['亥', '卯', '未'],
    '火局': ['寅', '午', '戌'],
    '金局': ['巳', '酉', '丑']
}

# 방합(方合) - 같은 방위의 세 지지
BANGHAP_GROUPS = {
    '東方木局': ['寅', '卯', '辰'],
    '南方火局': ['巳', '午', '未'],
    '西方金局': ['申', '酉', '戌'],
    '北方水局': ['亥', '子', '丑']
}

# 형(刑) - 상호 해침
# 무은지형(無恩之刑): 寅-巳-申 (서로 형)
# 무례지형(無禮之刑): 丑-未-戌 (서로 형)
# 자형(自刑): 辰-辰, 午-午, 酉-酉, 亥-亥
HYUNG_GROUPS = {
    '무은지형': ['寅', '巳', '申'],
    '무례지형': ['丑', '未', '戌']
}

HYUNG_SELF = ['辰', '午', '酉', '亥']  # 자형


def find_chung(branches: list) -> list:
    """충(沖) 찾기"""
    result = []
    for i, b1 in enumerate(branches):
        for j, b2 in enumerate(branches):
            if i < j and b1 in CHUNG_PAIRS and CHUNG_PAIRS[b1] == b2:
                pos_names = ['연지', '월지', '일지', '시지']
                result.append(f"{pos_names[i]}-{pos_names[j]} 충({b1}↔{b2})")
    return result


def find_yukhap(branches: list) -> list:
    """육합(六合) 찾기"""
    result = []
    for i, b1 in enumerate(branches):
        for j, b2 in enumerate(branches):
            if i < j and b1 in YUKHAP_PAIRS and YUKHAP_PAIRS[b1] == b2:
                pos_names = ['연지', '월지', '일지', '시지']
                result.append(f"{pos_names[i]}-{pos_names[j]} 육합({b1}+{b2})")
    return result


def find_samhap(branches: list) -> list:
    """삼합(三合) 찾기"""
    result = []
    for name, group in SAMHAP_GROUPS.items():
        # 세 개가 모두 있는지 확인
        found = [b for b in branches if b in group]
        if len(found) == 3:
            result.append(f"삼합 {name}({'+'.join(sorted(found))})")
        # 반합(두 개만 있어도 반합으로 인정)
        elif len(found) == 2:
            result.append(f"반합 {name}({'+'.join(sorted(found))})")
    return result


def find_banghap(branches: list) -> list:
    """방합(方合) 찾기"""
    result = []
    for name, group in BANGHAP_GROUPS.items():
        found = [b for b in branches if b in group]
        if len(found) == 3:
            result.append(f"방합 {name}({'+'.join(sorted(found))})")
    return result


def find_hyung(branches: list) -> list:
    """형(刑) 찾기"""
    result = []
    
    # 무은지형, 무례지형
    for name, group in HYUNG_GROUPS.items():
        found = [b for b in branches if b in group]
        if len(found) >= 2:
            result.append(f"{name}({'+'.join(sorted(found))})")
    
    # 자형
    branch_count = {}
    for b in branches:
        if b in HYUNG_SELF:
            branch_count[b] = branch_count.get(b, 0) + 1
    
    for b, count in branch_count.items():
        if count >= 2:
            result.append(f"자형({b})")
    
    return result


def analyze_hyungchunghap(year_branch: str, month_branch: str, 
                          day_branch: str, hour_branch: str) -> dict:
    """
    형충회합 종합 분석
    
    Returns:
        {
            'chung': [...],      # 충
            'yukhap': [...],     # 육합
            'samhap': [...],     # 삼합
            'banghap': [...],    # 방합
            'hyung': [...]       # 형
        }
    """
    branches = [year_branch, month_branch, day_branch, hour_branch]
    
    return {
        'chung': find_chung(branches),
        'yukhap': find_yukhap(branches),
        'samhap': find_samhap(branches),
        'banghap': find_banghap(branches),
        'hyung': find_hyung(branches)
    }
