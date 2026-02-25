"""
음력 변환 모듈 테스트
Test for Lunar Calendar Conversion Module
"""

from lunar import lunar_to_solar, solar_to_lunar


def test_lunar_to_solar():
    """음력 → 양력 변환 테스트"""
    print("=== 음력 → 양력 변환 테스트 ===\n")
    
    # 테스트 1: 음력 2009년 11월 13일 → 양력 2009년 12월 28일
    result = lunar_to_solar(2009, 11, 13)
    assert result == {'year': 2009, 'month': 12, 'day': 28}
    print(f"✓ 음력 2009년 11월 13일 → 양력 {result['year']}년 {result['month']}월 {result['day']}일")
    
    # 테스트 2: 음력 2009년 윤5월 15일
    result = lunar_to_solar(2009, 5, 15, is_leap_month=True)
    print(f"✓ 음력 2009년 윤5월 15일 → 양력 {result['year']}년 {result['month']}월 {result['day']}일")
    
    # 테스트 3: 경계값 - 1900년
    result = lunar_to_solar(1900, 1, 1)
    assert result == {'year': 1900, 'month': 1, 'day': 31}
    print(f"✓ 음력 1900년 1월 1일 → 양력 {result['year']}년 {result['month']}월 {result['day']}일")
    
    # 테스트 4: 경계값 - 2100년
    result = lunar_to_solar(2100, 12, 1)
    print(f"✓ 음력 2100년 12월 1일 → 양력 {result['year']}년 {result['month']}월 {result['day']}일")


def test_solar_to_lunar():
    """양력 → 음력 변환 테스트"""
    print("\n=== 양력 → 음력 변환 테스트 ===\n")
    
    # 테스트 1: 양력 2009년 12월 28일 → 음력 2009년 11월 13일
    result = solar_to_lunar(2009, 12, 28)
    assert result['year'] == 2009 and result['month'] == 11 and result['day'] == 13
    print(f"✓ 양력 2009년 12월 28일 → 음력 {result['year']}년 {result['month']}월 {result['day']}일")
    
    # 테스트 2: 윤달 변환
    result = solar_to_lunar(2009, 7, 7)
    leap_str = "윤" if result['is_leap_month'] else ""
    print(f"✓ 양력 2009년 7월 7일 → 음력 {result['year']}년 {leap_str}{result['month']}월 {result['day']}일")
    
    # 테스트 3: 경계값
    result = solar_to_lunar(1900, 1, 31)
    print(f"✓ 양력 1900년 1월 31일 → 음력 {result['year']}년 {result['month']}월 {result['day']}일")


def test_error_handling():
    """에러 처리 테스트"""
    print("\n=== 에러 처리 테스트 ===\n")
    
    # 테스트 1: 윤달 오류
    try:
        lunar_to_solar(2010, 5, 15, is_leap_month=True)
        print("✗ 윤달 오류가 감지되지 않음")
    except ValueError as e:
        print(f"✓ 윤달 오류 처리: {e}")
    
    # 테스트 2: 범위 초과
    try:
        lunar_to_solar(1899, 1, 1)
        print("✗ 범위 초과 오류가 감지되지 않음")
    except ValueError as e:
        print(f"✓ 범위 초과 처리: {e}")
    
    # 테스트 3: 유효하지 않은 날짜
    try:
        lunar_to_solar(2009, 2, 31)
        print("✗ 유효하지 않은 날짜 오류가 감지되지 않음")
    except ValueError as e:
        print(f"✓ 유효하지 않은 날짜 처리: {e}")
    
    # 테스트 4: 잘못된 월
    try:
        lunar_to_solar(2009, 13, 1)
        print("✗ 잘못된 월 오류가 감지되지 않음")
    except ValueError as e:
        print(f"✓ 잘못된 월 처리: {e}")


def main():
    """메인 테스트 함수"""
    print("=" * 60)
    print("음력 변환 모듈 테스트")
    print("=" * 60 + "\n")
    
    try:
        test_lunar_to_solar()
        test_solar_to_lunar()
        test_error_handling()
        
        print("\n" + "=" * 60)
        print("✅ 모든 테스트 통과!")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n❌ 테스트 실패: {e}")
        raise
    except Exception as e:
        print(f"\n❌ 예상치 못한 오류: {e}")
        raise


if __name__ == '__main__':
    main()
