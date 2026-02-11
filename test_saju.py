"""
사주팔자 계산 테스트
Test Cases for Saju Calculator
"""
from datetime import datetime
from saju_calculator import calculate_four_pillars, get_element_count


def test_case_1():
    """
    Test Case 1: 2009-12-28 16:35, Female
    Expected Results based on 천을귀인 만세력 v5.05
    """
    print("=" * 60)
    print("Test Case 1: 2009-12-28 16:35, Female")
    print("=" * 60)
    
    birth_datetime = datetime(2009, 12, 28, 16, 35)
    result = calculate_four_pillars(birth_datetime, '여')
    
    # Test 사주팔자
    expected = {
        'year': '己丑',
        'month': '丙子',
        'day': '丁未',
        'hour': '戊申'
    }
    
    actual = {
        'year': result['year_hanja'],
        'month': result['month_hanja'],
        'day': result['day_hanja'],
        'hour': result['hour_hanja']
    }
    
    print("\n[사주팔자]")
    for key in ['year', 'month', 'day', 'hour']:
        status = "✓" if actual[key] == expected[key] else "✗"
        print(f"  {key.capitalize():6} {status} Expected: {expected[key]}, Got: {actual[key]}")
    
    # Test 오행 개수
    print("\n[오행 개수]")
    element_count = get_element_count(result)
    expected_elements = {'목(木)': 0, '화(火)': 2, '토(土)': 4, '금(金)': 1, '수(水)': 1}
    
    for elem, expected_count in expected_elements.items():
        actual_count = element_count[elem]
        status = "✓" if actual_count == expected_count else "✗"
        print(f"  {elem} {status} Expected: {expected_count}, Got: {actual_count}")
    
    # Test 일간
    print(f"\n[일간]")
    print(f"  일간: {result['day_stem_hanja']} (Expected: 丁)")
    
    # Test 십신
    print(f"\n[십신]")
    print(f"  연주: {result['sipsin']['year']}")
    print(f"  월주: {result['sipsin']['month']}")
    print(f"  일주: {result['sipsin']['day']}")
    print(f"  시주: {result['sipsin']['hour']}")
    
    # Test 12운성
    print(f"\n[12운성]")
    print(f"  연주: {result['unsung']['year']}")
    print(f"  월주: {result['unsung']['month']}")
    print(f"  일주: {result['unsung']['day']}")
    print(f"  시주: {result['unsung']['hour']}")
    
    # Test 신살
    print(f"\n[신살]")
    for key, values in result['sinsal'].items():
        if values:
            print(f"  {key}: {', '.join(values)}")
    
    # Test 형충회합
    print(f"\n[형충회합]")
    hch = result['hyungchunghap']
    if hch['chung']:
        print(f"  충(沖): {', '.join(hch['chung'])}")
    if hch['yukhap']:
        print(f"  육합: {', '.join(hch['yukhap'])}")
    if hch['samhap']:
        print(f"  삼합: {', '.join(hch['samhap'])}")
    if hch['hyung']:
        print(f"  형(刑): {', '.join(hch['hyung'])}")
    
    # Test 대운
    print(f"\n[대운]")
    daeun = result['daeun']
    print(f"  방향: {daeun['direction']}")
    print(f"  시작 나이: {daeun['start_age']}세")
    print(f"  첫 대운: {daeun['list'][0]['pillar']} ({daeun['list'][0]['age']}~{daeun['list'][0]['age']+9}세)")
    
    # Test 세운
    print(f"\n[세운]")
    current_seun = [s for s in result['seun'] if s['is_current']]
    if current_seun:
        s = current_seun[0]
        print(f"  현재 ({s['year']}년): {s['jiazi']} ({s['age']}세)")
    
    # Check if all core calculations match
    all_match = all([
        actual[key] == expected[key] for key in ['year', 'month', 'day', 'hour']
    ]) and all([
        element_count[elem] == expected_elements[elem] 
        for elem in expected_elements
    ])
    
    if all_match:
        print("\n" + "=" * 60)
        print("✅ TEST PASSED: All calculations match 천을귀인 v5.05!")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ TEST FAILED: Some calculations do not match!")
        print("=" * 60)
    
    return all_match


def test_case_2():
    """
    Test Case 2: 1990-01-01 00:00, Male
    Additional test for variety
    """
    print("\n" + "=" * 60)
    print("Test Case 2: 1990-01-01 00:00, Male")
    print("=" * 60)
    
    birth_datetime = datetime(1990, 1, 1, 0, 0)
    result = calculate_four_pillars(birth_datetime, '남')
    
    print(f"\n[사주팔자]")
    print(f"  년주: {result['year_hanja']}")
    print(f"  월주: {result['month_hanja']}")
    print(f"  일주: {result['day_hanja']}")
    print(f"  시주: {result['hour_hanja']}")
    
    print(f"\n[일간]")
    print(f"  일간: {result['day_stem_hanja']}")
    
    print(f"\n[대운]")
    daeun = result['daeun']
    print(f"  방향: {daeun['direction']} (양년생 남자이므로 순행 예상)")
    print(f"  시작 나이: {daeun['start_age']}세")
    
    element_count = get_element_count(result)
    print(f"\n[오행 개수]")
    for elem, count in element_count.items():
        print(f"  {elem}: {count}개")
    
    print("\n✅ Test Case 2 executed successfully")
    return True


if __name__ == "__main__":
    print("\n사주팔자 계산기 종합 테스트")
    print("=" * 60)
    
    test1_passed = test_case_1()
    test2_passed = test_case_2()
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Test Case 1 (2009-12-28 Female): {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"Test Case 2 (1990-01-01 Male):   {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    print("=" * 60)
