"""
형충회합(刑沖會合) 계산 모듈
Punishments, Clashes, and Harmonies Module
"""

# 지지 충(沖) - 정반대 위치
CHUNG_TABLE = {
    '子': '午', '丑': '未', '寅': '申',
    '卯': '酉', '辰': '戌', '巳': '亥',
    '午': '子', '未': '丑', '申': '寅',
    '酉': '卯', '戌': '辰', '亥': '巳'
}

# 지지 육합(六合)
YUKHAP_TABLE = {
    '子': '丑', '丑': '子',
    '寅': '亥', '亥': '寅',
    '卯': '戌', '戌': '卯',
    '辰': '酉', '酉': '辰',
    '巳': '申', '申': '巳',
    '午': '未', '未': '午'
}

# 지지 삼합(三合)
SAMHAP_TABLE = {
    '申子辰': '水局',
    '亥卯未': '木局',
    '寅午戌': '火局',
    '巳酉丑': '金局'
}

# 지지 방합(方合) - 계절 방위
BANGHAP_TABLE = {
    '寅卯辰': '木局(東方)',
    '巳午未': '火局(南方)',
    '申酉戌': '金局(西方)',
    '亥子丑': '水局(北方)'
}

# 지지 형(刑)
# 무은지형: 寅刑巳, 巳刑申, 申刑寅 (恩을 배반하는 형)
# 무례지형: 丑刑戌, 戌刑未, 未刑丑 (예의없는 형)
# 자형: 辰辰, 午午, 酉酉, 亥亥 (스스로를 해치는 형)
HYUNG_GROUPS = {
    '무은지형': ['寅', '巳', '申'],
    '무례지형': ['丑', '戌', '未'],
    '자형': ['辰', '午', '酉', '亥']
}


def extract_hanja(text: str) -> str:
    """괄호가 있는 텍스트에서 한자만 추출"""
    if '(' in text:
        return text.split('(')[1].rstrip(')')
    return text


def get_chung(branches: list) -> list:
    """
    충(沖) 관계 찾기
    
    Args:
        branches: 4개 지지 리스트 [년지, 월지, 일지, 시지]
    
    Returns:
        충 관계 리스트 (예: ['년지-월지(子-午)', '일지-시지(寅-申)'])
    """
    positions = ['년지', '월지', '일지', '시지']
    result = []
    
    branches_hanja = [extract_hanja(b) for b in branches]
    
    # 모든 지지 쌍 확인
    for i in range(len(branches_hanja)):
        for j in range(i+1, len(branches_hanja)):
            b1, b2 = branches_hanja[i], branches_hanja[j]
            
            # 충 관계인지 확인
            if CHUNG_TABLE.get(b1) == b2:
                result.append(f"{positions[i]}-{positions[j]}({b1}-{b2})")
    
    return result


def get_yukhap(branches: list) -> list:
    """
    육합(六合) 관계 찾기
    
    Args:
        branches: 4개 지지 리스트
    
    Returns:
        육합 관계 리스트
    """
    positions = ['년지', '월지', '일지', '시지']
    result = []
    
    branches_hanja = [extract_hanja(b) for b in branches]
    
    # 모든 지지 쌍 확인
    for i in range(len(branches_hanja)):
        for j in range(i+1, len(branches_hanja)):
            b1, b2 = branches_hanja[i], branches_hanja[j]
            
            # 육합 관계인지 확인
            if YUKHAP_TABLE.get(b1) == b2:
                result.append(f"{positions[i]}-{positions[j]}({b1}-{b2})")
    
    return result


def get_samhap(branches: list) -> list:
    """
    삼합(三合) 관계 찾기
    
    Args:
        branches: 4개 지지 리스트
    
    Returns:
        삼합 관계 리스트
    """
    result = []
    branches_hanja = [extract_hanja(b) for b in branches]
    
    # 삼합 체크
    for key, value in SAMHAP_TABLE.items():
        samhap_set = set(key)
        if samhap_set.issubset(set(branches_hanja)):
            # 위치 찾기
            positions = []
            pos_names = ['년지', '월지', '일지', '시지']
            for i, b in enumerate(branches_hanja):
                if b in samhap_set:
                    positions.append(pos_names[i])
            
            result.append(f"{'-'.join(positions)}({key}) → {value}")
    
    return result


def get_banghap(branches: list) -> list:
    """
    방합(方合) 관계 찾기
    
    Args:
        branches: 4개 지지 리스트
    
    Returns:
        방합 관계 리스트
    """
    result = []
    branches_hanja = [extract_hanja(b) for b in branches]
    
    # 방합 체크
    for key, value in BANGHAP_TABLE.items():
        banghap_set = set(key)
        if banghap_set.issubset(set(branches_hanja)):
            # 위치 찾기
            positions = []
            pos_names = ['년지', '월지', '일지', '시지']
            for i, b in enumerate(branches_hanja):
                if b in banghap_set:
                    positions.append(pos_names[i])
            
            result.append(f"{'-'.join(positions)}({key}) → {value}")
    
    return result


def get_hyung(branches: list) -> list:
    """
    형(刑) 관계 찾기
    
    Args:
        branches: 4개 지지 리스트
    
    Returns:
        형 관계 리스트
    """
    result = []
    branches_hanja = [extract_hanja(b) for b in branches]
    positions = ['년지', '월지', '일지', '시지']
    
    # 무은지형, 무례지형 체크 (3개 중 2개 이상 있으면 형)
    for hyung_type, hyung_branches in HYUNG_GROUPS.items():
        if hyung_type == '자형':
            continue
        
        found_branches = [b for b in branches_hanja if b in hyung_branches]
        if len(found_branches) >= 2:
            # 위치 찾기
            pos_list = []
            for b in found_branches:
                for i, branch in enumerate(branches_hanja):
                    if branch == b:
                        pos_list.append(positions[i])
                        break
            
            result.append(f"{hyung_type}: {'-'.join(pos_list)}({''.join(found_branches)})")
    
    # 자형 체크 (같은 지지가 2개 이상)
    jachung_branches = HYUNG_GROUPS['자형']
    for branch in jachung_branches:
        count = branches_hanja.count(branch)
        if count >= 2:
            pos_list = [positions[i] for i, b in enumerate(branches_hanja) if b == branch]
            result.append(f"자형: {'-'.join(pos_list)}({branch})")
    
    return result


if __name__ == '__main__':
    # 테스트: 2009-12-28생 己丑 丙子 丁未 戊申
    print("=== 형충회합 테스트: 己丑 丙子 丁未 戊申 ===\n")
    branches = ['丑', '子', '未', '申']
    
    chung = get_chung(branches)
    print(f"충(沖): {chung if chung else '없음'}")
    
    yukhap = get_yukhap(branches)
    print(f"육합(六合): {yukhap if yukhap else '없음'}")
    
    samhap = get_samhap(branches)
    print(f"삼합(三合): {samhap if samhap else '없음'}")
    
    banghap = get_banghap(branches)
    print(f"방합(方合): {banghap if banghap else '없음'}")
    
    hyung = get_hyung(branches)
    print(f"형(刑): {hyung if hyung else '없음'}")
    
    # 테스트 2: 충 예시
    print("\n=== 충 테스트: 子午沖 ===")
    branches2 = ['子', '卯', '午', '酉']
    chung2 = get_chung(branches2)
    print(f"충(沖): {chung2}")
