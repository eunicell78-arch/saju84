"""
형충회합(刑沖會合) 계산 모듈
Clash and Harmony Calculation Module
"""

# 지지 충(沖) - 정반대 지지
CHUNG = {
    '子': '午', '丑': '未', '寅': '申',
    '卯': '酉', '辰': '戌', '巳': '亥',
    '午': '子', '未': '丑', '申': '寅',
    '酉': '卯', '戌': '辰', '亥': '巳'
}

# 지지 육합(六合) - 6쌍의 조화
YUKHAP = {
    '子': '丑', '丑': '子',
    '寅': '亥', '亥': '寅',
    '卯': '戌', '戌': '卯',
    '辰': '酉', '酉': '辰',
    '巳': '申', '申': '巳',
    '午': '未', '未': '午'
}

# 지지 삼합(三合) - 3개가 모여 국을 이룸
SAMHAP = {
    '申子辰': '수국(水局)',
    '亥卯未': '목국(木局)',
    '寅午戌': '화국(火局)',
    '巳酉丑': '금국(金局)'
}

# 지지 방합(方合) - 같은 방위의 합
BANGHAP = {
    '亥子丑': '북방수(北方水)',
    '寅卯辰': '동방목(東方木)',
    '巳午未': '남방화(南方火)',
    '申酉戌': '서방금(西方金)'
}

# 지지 형(刑)
# 무은지형: 寅刑巳, 巳刑申, 申刑寅
# 무례지형: 丑刑戌, 戌刑未, 未刑丑
# 자형: 辰辰, 午午, 酉酉, 亥亥
HYUNG_MUEUN = [['寅', '巳', '申']]  # 무은지형
HYUNG_MURYE = [['丑', '戌', '未']]  # 무례지형
HYUNG_JA = ['辰', '午', '酉', '亥']  # 자형


def find_chung(branches: list) -> list:
    """
    지지 충(沖) 찾기
    
    Args:
        branches: 지지 한자 리스트 (예: ['丑', '子', '未', '申'])
    
    Returns:
        충 관계 리스트 (예: ['丑-未 충'])
    """
    chung_list = []
    for i, branch1 in enumerate(branches):
        for j, branch2 in enumerate(branches):
            if i < j and CHUNG.get(branch1) == branch2:
                chung_list.append(f"{branch1}-{branch2} 충")
    return chung_list


def find_hap(branches: list) -> list:
    """
    지지 합(合) 찾기 - 육합과 삼합
    
    Args:
        branches: 지지 한자 리스트
    
    Returns:
        합 관계 리스트
    """
    hap_list = []
    
    # 육합 찾기
    for i, branch1 in enumerate(branches):
        for j, branch2 in enumerate(branches):
            if i < j and YUKHAP.get(branch1) == branch2:
                hap_list.append(f"{branch1}-{branch2} 육합")
    
    # 삼합 찾기
    for pattern, name in SAMHAP.items():
        found = []
        for branch in branches:
            if branch in pattern:
                found.append(branch)
        
        # 3개 모두 있으면 삼합 성립
        if len(found) == 3:
            hap_list.append(f"{'-'.join(found)} {name} 삼합")
        # 2개만 있으면 반합
        elif len(found) == 2:
            hap_list.append(f"{'-'.join(found)} 반합")
    
    # 방합 찾기
    for pattern, name in BANGHAP.items():
        found = []
        for branch in branches:
            if branch in pattern:
                found.append(branch)
        
        # 3개 모두 있으면 방합 성립
        if len(found) == 3:
            hap_list.append(f"{'-'.join(found)} {name} 방합")
    
    return hap_list


def find_hyung(branches: list) -> list:
    """
    지지 형(刑) 찾기
    
    Args:
        branches: 지지 한자 리스트
    
    Returns:
        형 관계 리스트
    """
    hyung_list = []
    
    # 무은지형
    for pattern in HYUNG_MUEUN:
        found = []
        for branch in branches:
            if branch in pattern:
                found.append(branch)
        
        if len(found) >= 2:
            hyung_list.append(f"{'-'.join(found)} 무은지형")
    
    # 무례지형
    for pattern in HYUNG_MURYE:
        found = []
        for branch in branches:
            if branch in pattern:
                found.append(branch)
        
        if len(found) >= 2:
            hyung_list.append(f"{'-'.join(found)} 무례지형")
    
    # 자형 (같은 지지가 2개 이상)
    branch_count = {}
    for branch in branches:
        if branch in HYUNG_JA:
            branch_count[branch] = branch_count.get(branch, 0) + 1
    
    for branch, count in branch_count.items():
        if count >= 2:
            hyung_list.append(f"{branch} 자형 ({count}개)")
    
    return hyung_list


def get_hyungchunghap(branches: list) -> dict:
    """
    형충회합 전체 계산
    
    Args:
        branches: 지지 한자 리스트 (4개)
    
    Returns:
        {'chung': [...], 'hap': [...], 'hyung': [...]}
    """
    return {
        'chung': find_chung(branches),
        'hap': find_hap(branches),
        'hyung': find_hyung(branches)
    }
