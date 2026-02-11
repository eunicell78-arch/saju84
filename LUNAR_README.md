# 음력 변환 모듈 (Lunar Calendar Conversion Module)

음력과 양력 간의 변환을 제공하는 Python 모듈입니다.

## 기능

- **음력 → 양력 변환**: 음력 날짜를 양력 날짜로 변환
- **양력 → 음력 변환**: 양력 날짜를 음력 날짜로 변환
- **윤달 지원**: 윤달(leap month) 처리 완벽 지원
- **넓은 범위**: 1900년~2100년 지원
- **에러 처리**: 입력 검증 및 명확한 오류 메시지

## 설치

모듈은 별도의 외부 의존성이 없으며, 표준 Python 라이브러리만 사용합니다.

```python
from lunar import lunar_to_solar, solar_to_lunar
```

## 사용법

### 1. 음력을 양력으로 변환

```python
from lunar import lunar_to_solar

# 기본 사용법
result = lunar_to_solar(2009, 11, 13)
print(f"{result['year']}년 {result['month']}월 {result['day']}일")
# 출력: 2009년 12월 28일

# 윤달 변환
result = lunar_to_solar(2009, 5, 15, is_leap_month=True)
print(f"{result['year']}년 {result['month']}월 {result['day']}일")
# 출력: 2009년 7월 7일
```

### 2. 양력을 음력으로 변환

```python
from lunar import solar_to_lunar

# 기본 사용법
result = solar_to_lunar(2009, 12, 28)
leap_str = "윤" if result['is_leap_month'] else ""
print(f"{result['year']}년 {leap_str}{result['month']}월 {result['day']}일")
# 출력: 2009년 11월 13일

# 윤달이 포함된 변환
result = solar_to_lunar(2009, 7, 7)
leap_str = "윤" if result['is_leap_month'] else ""
print(f"{result['year']}년 {leap_str}{result['month']}월 {result['day']}일")
# 출력: 2009년 윤5월 15일
```

## API 문서

### `lunar_to_solar(year, month, day, is_leap_month=False)`

음력을 양력으로 변환합니다.

**매개변수:**
- `year` (int): 음력 연도 (1900-2100)
- `month` (int): 음력 월 (1-12)
- `day` (int): 음력 일 (1-29/30)
- `is_leap_month` (bool, optional): 윤달 여부. 기본값은 `False`

**반환값:**
- `dict`: `{'year': 양력연도, 'month': 양력월, 'day': 양력일}`

**예외:**
- `ValueError`: 유효하지 않은 날짜, 범위 초과, 윤달 오류

**예제:**
```python
result = lunar_to_solar(2009, 11, 13)
# {'year': 2009, 'month': 12, 'day': 28}

result = lunar_to_solar(2009, 5, 15, is_leap_month=True)
# {'year': 2009, 'month': 7, 'day': 7}
```

### `solar_to_lunar(year, month, day)`

양력을 음력으로 변환합니다.

**매개변수:**
- `year` (int): 양력 연도
- `month` (int): 양력 월 (1-12)
- `day` (int): 양력 일 (1-31)

**반환값:**
- `dict`: `{'year': 음력연도, 'month': 음력월, 'day': 음력일, 'is_leap_month': 윤달여부}`

**예외:**
- `ValueError`: 유효하지 않은 날짜, 범위 초과

**예제:**
```python
result = solar_to_lunar(2009, 12, 28)
# {'year': 2009, 'month': 11, 'day': 13, 'is_leap_month': False}

result = solar_to_lunar(2009, 7, 7)
# {'year': 2009, 'month': 5, 'day': 15, 'is_leap_month': True}
```

## 테스트

테스트 파일을 실행하여 모듈의 정확성을 확인할 수 있습니다:

```bash
python test_lunar.py
```

또는 내장된 테스트를 실행:

```bash
python lunar.py
```

## 테스트 케이스

모듈은 다음 테스트 케이스를 통과합니다:

1. **음력 2009년 11월 13일 → 양력 2009년 12월 28일** ✓
2. **음력 2009년 윤5월 15일 → 양력 2009년 7월 7일** ✓
3. **경계값 테스트 (1900년)** ✓
4. **경계값 테스트 (2100년)** ✓
5. **양력 → 음력 역변환** ✓
6. **윤달 오류 처리** ✓
7. **범위 초과 처리** ✓
8. **유효하지 않은 날짜 처리** ✓

## 구현 방법

이 모듈은 한국천문연구원의 음력 알고리즘을 기반으로 하며, 다음과 같은 방식으로 구현되었습니다:

1. **음력 데이터 테이블**: 1900년~2100년의 각 연도별 월별 일수와 윤달 정보를 16진수로 인코딩
2. **일수 계산 방식**: 기준일(1900년 1월 31일 = 음력 1900년 1월 1일)로부터의 일수 차이로 변환
3. **윤달 처리**: 각 연도의 윤달 위치와 일수를 정확히 계산

## 제한사항

- 지원 범위: 1900년~2100년
- 음력 데이터는 한국 천문 계산에 기반함
- 1900년 1월 31일 이전의 날짜는 지원하지 않음

## 라이선스

이 모듈은 사주팔자 만세력 계산기의 일부로, 동일한 라이선스를 따릅니다.

## 참고

- 한국천문연구원 음력 알고리즘
- 검증된 음력 변환 라이브러리 로직 참고
