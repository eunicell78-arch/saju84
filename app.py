import streamlit as st
from saju_calculator import calculate_four_pillars

st.set_page_config(page_title="만세력", page_icon="🔮", layout="wide")

st.title("🔮 만세력 - 사주팔자 계산기")
st.markdown("### 동양의 전통 만세력을 확인하세요")
st.markdown("---")

# 입력
col1, col2 = st.columns(2)

with col1:
    st.subheader("📅 생년월일")
    calendar_type = st.radio("달력 선택", ["양력", "음력"], horizontal=True)
    
    year = st.number_input("연도", 1900, 2100, 1990, help="1900-2100년 범위")
    month = st.number_input("월", 1, 12, 1)
    day = st.number_input("일", 1, 31, 1)
    
    if calendar_type == "음력":
        is_leap_month = st.checkbox("윤달")
    else:
        is_leap_month = False

with col2:
    st.subheader("🕐 시간")
    hour = st.number_input("시", 0, 23, 12)
    minute = st.number_input("분", 0, 59, 0)

st.markdown("---")

if st.button("🔮 사주팔자 계산하기", type="primary", use_container_width=True):
    try:
        result = calculate_four_pillars({
            'year': year,
            'month': month,
            'day': day,
            'hour': hour,
            'minute': minute,
            'is_lunar': calendar_type == "음력",
            'is_leap_month': is_leap_month
        })
        
        st.success("✅ 계산 완료!")
        
        # 날짜 정보
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"📅 양력: {result['solar_date']['year']}년 {result['solar_date']['month']}월 {result['solar_date']['day']}일")
        with col2:
            lunar = result['lunar_date']
            lunar_str = f"🌙 음력: {lunar['year']}년 {'윤' if lunar.get('is_leap_month') else ''}{lunar['month']}월 {lunar['day']}일"
            st.info(lunar_str)
        
        st.markdown("---")
        st.subheader("📊 사주팔자")
        
        # 사주 표시
        col1, col2, col3, col4 = st.columns(4)
        pillars = [
            ("年柱<br>연주", result['year']),
            ("月柱<br>월주", result['month']),
            ("日柱<br>일주", result['day']),
            ("時柱<br>시주", result['hour'])
        ]
        
        for col, (title, pillar) in zip([col1, col2, col3, col4], pillars):
            with col:
                st.markdown(f"<h4 style='text-align:center'>{title}</h4>", unsafe_allow_html=True)
                st.markdown(f"<h1 style='text-align:center; font-size:3.5em'>{pillar['hanja']}{pillar['branch_hanja']}</h1>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align:center; font-size:1.2em'>({pillar['ko']}{pillar['branch_ko']})</p>", unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("🌳 오행 분석")
        
        col1, col2, col3, col4 = st.columns(4)
        for col, key in zip([col1, col2, col3, col4], ['year', 'month', 'day', 'hour']):
            with col:
                elem = result['elements'][key]
                st.write(f"**천간**: {elem['stem']}")
                st.write(f"**지지**: {elem['branch']}")
        
        st.markdown("---")
        st.subheader("☯️ 음양 분석")
        
        col1, col2, col3, col4 = st.columns(4)
        for col, key in zip([col1, col2, col3, col4], ['year', 'month', 'day', 'hour']):
            with col:
                yy = result['yin_yang'][key]
                st.write(f"**천간**: {yy['stem']}")
                st.write(f"**지지**: {yy['branch']}")
        
    except Exception as e:
        st.error(f"❌ 오류: {str(e)}")

st.markdown("---")
st.markdown("<p style='text-align:center; color:gray'>yhj1024/manseryeok와 0ssw1/sajupy의 계산 로직 참고</p>", unsafe_allow_html=True)
