import streamlit as st
from PIL import Image
import datetime
import time

# --- 1. 데이터 저장소 및 상세 가이드 데이터베이스 ---
if 'history' not in st.session_state:
    st.session_state['history'] = []
if 'community' not in st.session_state:
    st.session_state['community'] = [
        {"user": "지구지킴이", "item": "페트병 화분", "likes": 12},
        {"user": "DIY장인", "item": "우유팩 필통", "likes": 25}
    ]

# 아이템별 상세 제작 데이터 (도안 및 상세 가이드)
UPCYCLING_DETAILS = {
    "자동 급수 화분": {
        "materials": "플라스틱병, 칼, 면끈(운동화끈), 송곳, 흙, 식물",
        "blueprint": "병의 1/2 지점을 자릅니다. 뚜껑에 구멍을 뚫고 끈을 통과시키는 것이 핵심입니다.",
        "steps": [
            "페트병의 중간 부분을 칼로 깨끗하게 자릅니다.",
            "병뚜껑 중앙에 송곳으로 구멍을 뚫고, 물을 빨아올릴 면끈을 10cm 정도 끼웁니다.",
            "병 하단부에는 물을 채우고, 뚜껑을 닫은 상단부를 뒤집어서 꽂습니다.",
            "상단부에 흙을 채우고 식물을 심으면 완성! (끈이 흙 속에 파묻혀야 합니다)"
        ],
        "image_url": "https://images.unsplash.com/photo-1592150621344-220b282dd9fe?w=400"
    },
    "데스크 정리함": {
        "materials": "플라스틱병 3개, 가위, 마스킹 테이프, 접착제",
        "blueprint": "병의 높이를 서로 다르게(5cm, 8cm, 12cm) 잘라 계단식으로 배치합니다.",
        "steps": [
            "각기 다른 높이로 병의 아랫부분을 자릅니다.",
            "잘린 단면이 날카로우니 마스킹 테이프나 다리미 열로 매끄럽게 마감합니다.",
            "세 개의 병을 접착제로 붙여서 하나로 합칩니다.",
            "펜, 가위, 포스트잇 등을 나누어 수납하세요."
        ],
        "image_url": "https://images.unsplash.com/photo-1591123109285-df7d9936ec35?w=400"
    },
    "카드 지갑": {
        "materials": "우유팩 1개, 칼, 벨크로(찍찍이), 자",
        "blueprint": "우유팩의 사각형 면을 펼친 뒤, 카드 크기에 맞춰 3단 접기 도안을 그립니다.",
        "steps": [
            "우유팩의 위아래를 자르고 펼쳐서 긴 직사각형 모양으로 만듭니다.",
            "카드를 올려두고 가로/세로 여유를 1cm씩 두어 도안을 그립니다.",
            "도안대로 접은 후, 뚜껑이 덮이는 부분에 벨크로를 붙입니다.",
            "우유팩 특유의 방수 재질 덕분에 튼튼한 지갑이 완성됩니다!"
        ],
        "image_url": "https://images.unsplash.com/photo-1621439242095-02be966a4087?w=400"
    }
}

# 분석 결과 추천 리스트 (기능 1용)
UPCYCLING_DB = {
    "플라스틱병": ["자동 급수 화분", "데스크 정리함"],
    "우유팩": ["카드 지갑", "연필꽂이"]
}

# --- 2. 화면 구성 함수 ---

def main_page():
    st.title("♻️ 리본(Re-Born)")
    st.subheader("버리는 물건에 새로운 삶을!")
    
    uploaded_file = st.file_uploader("사진을 업로드하면 AI가 제작 아이디어를 드립니다.", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        st.image(uploaded_file, caption='업로드된 사진', width=300)
        with st.spinner('사물을 분석 중...'):
            time.sleep(1.5)
            # 여기서는 예시로 '플라스틱병'이 인식되었다고 가정
            detected = "플라스틱병"
            st.success(f"이 물건은 **{detected}**네요! 아래 프로젝트를 추천합니다.")
            
            cols = st.columns(len(UPCYCLING_DB[detected]))
            for idx, item_name in enumerate(UPCYCLING_DB[detected]):
                with cols[idx]:
                    if st.button(item_name):
                        st.session_state['selected_item'] = item_name
                        st.session_state['page'] = 'guide'
                        st.rerun()

def guide_page():
    item_name = st.session_state.get('selected_item')
    data = UPCYCLING_DETAILS.get(item_name)

    if not data:
        st.error("가이드 정보를 찾을 수 없습니다.")
        if st.button("홈으로"):
            st.session_state['page'] = 'home'
            st.rerun()
        return

    st.title(f"🛠️ {item_name} 제작 가이드")
    
    # 1. 도안 및 재료 섹션
    col1, col2 = st.columns(2)
    with col1:
        st.image(data['image_url'], caption="완성 예시 비주얼")
    with col2:
        st.markdown(f"### 📋 준비물\n{data['materials']}")
        st.info(f"**📐 도안 포인트:**\n{data['blueprint']}")

    st.write("---")
    
    # 2. 단계별 가이드
    st.subheader("📝 제작 단계 (Step-by-Step)")
    for i, step in enumerate(data['steps']):
        with st.expander(f"Step {i+1}", expanded=True):
            st.write(step)

    # 3. 완료 버튼
    if st.button("✅ 제작 완료! 내 기록에 추가"):
        st.session_state['history'].append({
            "item": item_name,
            "date": datetime.date.today().strftime("%Y-%m-%d"),
            "amount": 0.3
        })
        st.balloons()
        st.success("히스토리에 저장되었습니다!")
        time.sleep(2)
        st.session_state['page'] = 'home'
        st.rerun()

def history_page():
    st.title("👤 나의 리본 히스토리")
    if not st.session_state['history']:
        st.write("아직 활동 내역이 없습니다.")
    else:
        for entry in reversed(st.session_state['history']):
            st.info(f"**{entry['date']}** - {entry['item']} (약 {entry['amount']}kg 탄소 절감)")

# --- 3. 내비게이션 제어 ---
st.sidebar.title("Re-Born")
nav = st.sidebar.radio("메뉴", ["홈", "나의 기록"])

if nav == "홈":
    if st.session_state.get('page') == 'guide':
        guide_page()
    else:
        main_page()
else:
    history_page()