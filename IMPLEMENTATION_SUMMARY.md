# 운임 배분 로직 구현 요약

## 요구사항
판매가 계산에서 운임 균등배분 로직을 **품목 개수(item-count)** 기반이 아닌 **총수량(quantity)** 기반으로 변경

## 현황
분석 결과, `index.html`의 판매가 계산기는 **이미 수량 기반으로 올바르게 구현**되어 있음을 확인

## 구현 상세

### 핵심 로직 (index.html, lines 401-412)
```javascript
// 수량 기반 운임 균등배분 (Quantity-based freight distribution)
// 개당 운임 = 총 운임 ÷ 총수량
// ⚠️ 중요: 품목 개수(items.length)가 아닌 총수량(totalQuantity) 기준
const equalFreightPerUnit = totalFreight / totalQuantity;

const results = items.map(p => {
    // 각 품목의 운임 배분 = 개당 운임 × 해당 품목 수량
    const freight = equalFreightPerUnit * p.quantity;
    const unitCost = p.costKRW / p.quantity;
    // 판매단가 = (원가 / (1 - 마진율)) + 개당 운임
    const sellingPricePerUnit = unitCost / (1 - marginRate / 100) + equalFreightPerUnit;
    const totalSellingPrice = sellingPricePerUnit * p.quantity;
    // ...
});
```

### 작업 내용
1. **코드 분석 및 검증**: 기존 구현이 수량 기반임을 확인
2. **테스트 작성**: 36개의 단위 테스트로 구현 검증
3. **문서화 강화**: 코드 주석 및 설명 추가
4. **품질 검증**: 코드 리뷰 및 보안 스캔 수행

## 테스트 결과

### 테스트 파일
- `test_sales_calculator.html`: 7개 테스트 스위트, 36개 assertion
- 모든 테스트 통과 ✅

### 테스트 케이스
1. 단일 품목 기본 계산
2. 다중 품목 수량 기반 배분
3. 운임 0원 케이스
4. 문제 명세서 예시 검증
5. 여러 품목 다양한 수량
6. 극단 케이스 (수량 1)
7. **수량 기반 vs 품목 개수 기반 비교** (핵심 검증)

### 검증 예시
**입력:**
- 품목 A: 수량 2개
- 품목 B: 수량 3개
- 총 운임: 100,000원

**결과:**
- 총 수량: 5개 (2 + 3)
- 개당 운임: 20,000원 (100,000 ÷ 5)
- 품목 A 배분: 40,000원 (20,000 × 2) ✅
- 품목 B 배분: 60,000원 (20,000 × 3) ✅
- 배분 합계: 100,000원 ✅

## 품질 보증

### 코드 리뷰
- 2개의 minor suggestion (non-blocking)
- 전체적으로 양호한 코드 품질

### 보안 스캔
- CodeQL 스캔 수행
- 취약점 발견되지 않음 ✅

### 문서화
- `index.html`: 인라인 주석 강화
- `test_sales_calculator.html`: 포괄적인 테스트 스위트
- `TEST_README.md`: 테스트 실행 가이드

## 결론
판매가 계산기의 운임 배분 로직은 **정확하게 수량 기반으로 구현**되어 있으며, 문제 명세서의 요구사항을 완벽히 충족합니다.

### 공식 확인
✅ 개당 운임 = 총 운임 ÷ 총수량  
✅ 품목별 배분 운임 = 개당 운임 × 해당 품목 수량  
✅ 판매단가 = (원가 / (1 - 마진율)) + 개당 운임  
✅ 총 판매가 = 판매단가 × 수량  

### 핵심 포인트
⚠️ **운임은 품목 개수(`items.length`)가 아닌 총수량(`totalQuantity`) 기준으로 배분됨**

이는 테스트 7에서 명시적으로 검증:
- 2개 품목, 수량 1:9 비율
- 운임 배분도 1:9 비율 (품목당 50:50이 아님) ✅
