import streamlit as st
import requests
import json
import time
import random
import urllib.parse
import streamlit.components.v1 as components

# 🔑 [필독] 새로 발급받으신 API 키를 여기에 꼭 넣어주세요!
api_key = st.secrets["GCP_API_KEY"]

# 1. 페이지 설정
st.set_page_config(page_title="Dr.Rang | 👑 군주의 실전 투자", layout="centered")

# 2. 🎨 [CSS] 디자인 & 모바일 최적화
st.markdown("""
    <style>
    .stApp { background-color: transparent; }
    .stButton button { width: 100% !important; border-radius: 12px !important; font-weight: 800 !important; height: auto !important; padding: 12px 5px !important; }
    button[key*="p_btn"] { background-color: #ffffff !important; color: #000000 !important; border: 2px solid #eeeeee !important; }
    button[key*="v_yes"] { background-color: #007bff !important; color: white !important; }
    button[key*="v_no"] { background-color: #ff4b4b !important; color: white !important; }
    .ranking-container { background-color: #1e1e1e; padding: 15px; border-radius: 15px; color: white; margin: 15px 0; }
    .rank-row { display: flex; justify-content: space-between; padding: 12px; border-bottom: 1px solid #333; }
    .my-rank { background-color: #2c3e50; border: 1px solid #4da3ff; border-radius: 8px; color: #ffcc00; }
    .invest-guide { background-color: #fff9db; border-left: 5px solid #ffcc00; padding: 15px; border-radius: 10px; color: #856404; margin: 15px 0; text-align: center; font-size: 1.1rem; font-weight: bold; }
    .balance-text { font-size: 2.8rem; font-weight: 800; color: #4da3ff; }
    .premium-footer { text-align: center; padding-top: 50px; padding-bottom: 20px; font-family: 'serif'; }
    .section-header { font-size: 1.3rem; font-weight: bold; color: #31333F; margin-top: 25px; margin-bottom: 15px; white-space: nowrap; }

    @media (max-width: 600px) {
        .balance-text { font-size: 2.1rem !important; }
        .section-header { font-size: 1.1rem !important; }
        .stButton button { font-size: 0.85rem !important; }
    }
    </style>
""", unsafe_allow_html=True)

# 3. 💰 상태 관리
if 'balance' not in st.session_state: st.session_state.balance = 10000 
if 'p_choice' not in st.session_state: st.session_state.p_choice = "100P"
if 'bet_status' not in st.session_state: st.session_state.bet_status = "waiting"
if 'item_index' not in st.session_state: st.session_state.item_index = 0
if 'lyrics' not in st.session_state: st.session_state.lyrics = None
if 'rank_data' not in st.session_state:
    st.session_state.rank_data = [{"name": "🔥 불사조군주", "score": 15000}, {"name": "💎 다이아수저", "score": 12500}, {"name": "⚡ 번개투자자", "score": 9000}]

# 4. 📦 ITEMS
ITEMS = [
    {"title": "🥩 Rick Astley - Never Gonna Give You Up", "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"},
    {"title": "🕶️ 눈도장빵 - 해머스미스커피 학동역점", "url": "https://youtu.be/PzdBmhGDMBg?si=1laa1z0x18yCgDKt"},
    {"title": "🛸 감자도리 - 도리도리쏭", "url": "https://youtu.be/sowbaxMLrBY?si=-rVtVWXpGkOOlhw-"},
    {"title": "🤖 감자도리 - 만원쏭", "url": "https://youtu.be/JzSW_7frZNk?si=Kga2UssA3nR-dURj"}
]

# --- 🚀 기능 정의 (버튼 실행 전에 위치해야 함) ---
def play_real_investment(user_prediction):
    bet_amount = int(st.session_state.p_choice.replace('P',''))
    if st.session_state.balance < bet_amount:
        st.error("잔액 부족!"); return
    market_result = "YES" if random.random() > 0.5 else "NO"
    with st.spinner('시장의 반응 분석 중...'): time.sleep(1.2)
    if user_prediction == market_result:
        st.session_state.balance += bet_amount
        st.balloons()
        st.success(f"🎯 적중! 시장도 [{market_result}]였습니다! +{bet_amount:,}P")
    else:
        st.session_state.balance -= bet_amount
        st.error(f"📉 실패! 시장은 [{market_result}]였습니다. -{bet_amount:,}P")
    st.session_state.bet_status = "finished" 
    time.sleep(1); st.rerun()

# --- ✨ [상단] 타이틀 영역 ---
st.markdown("<h1 style='text-align: center; color: #ffcc00; margin-bottom: 0;'>Dr.Rang (닥터랭)</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #ffcc00; margin-top: 5px; font-weight: normal; font-size: 1.0rem; white-space: nowrap;'>당신의 스토리가 음악이 되는 공간</h3>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; font-size: 0.95rem; color: #ffcc00; margin-top: 5px; margin-bottom: 25px; font-weight: bold;'>👑 군주의 실전 투자</div>", unsafe_allow_html=True)

# --- 1. 대시보드 ---
st.markdown(f"""
    <div style="background-color: #1a1a1a; padding: 25px; border-radius: 20px; color: white; text-align: center; margin-bottom: 25px; border: 1px solid #333;">
        <div style="display: flex; justify-content: space-between; font-size: 0.8rem; font-weight: bold; margin-bottom: 10px;">
            <span style="color: #ffcc00; border: 1px solid #ffcc00; padding: 2px 8px; border-radius: 5px;">👑 군주</span>
            <span style="color: #ffffff;">💪 LV.{st.session_state.balance//1000}</span>
        </div>
        <div style="font-size: 0.9rem; color: #aaa;">가용 자산</div>
        <div class="balance-text">{st.session_state.balance:,}P</div>
    </div>
""", unsafe_allow_html=True)

# --- 2. 아이템 & 베팅 ---
current_item = ITEMS[st.session_state.item_index]
st.markdown(f"<div class='section-header'>📽️ {current_item['title']}</div>", unsafe_allow_html=True)
st.video(current_item['url'])
st.markdown(f"""<div class="invest-guide">이 아이템이 성공 할까요?</div>""", unsafe_allow_html=True)

# --- 💰 [윗줄] 투자 포인트 선택 (3칸) ---
st.markdown(f"<div class='section-header'>💰 투자 포인트 선택</div>", unsafe_allow_html=True)
p_col1, p_col2, p_col3 = st.columns(3)
pts = ["100P", "500P", "1000P"]

for i, p_val in enumerate(pts):
    with [p_col1, p_col2, p_col3][i]:
        label = f"✔️ {p_val}" if st.session_state.p_choice == p_val else p_val
        if st.button(label, key=f"p_btn_{p_val}", use_container_width=True, disabled=(st.session_state.bet_status == "finished")):
            st.session_state.p_choice = p_val
            st.rerun()

# --- 🔥 [아랫줄] YES / NO 결정 (2칸) ---
st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
v_col1, v_col2 = st.columns(2)

with v_col1:
    if st.button("YES 🔥", key="v_yes", type="primary", use_container_width=True, disabled=(st.session_state.bet_status == "finished")):
        play_real_investment("YES")

with v_col2:
    if st.button("NO ❄️", key="v_no", use_container_width=True, disabled=(st.session_state.bet_status == "finished")):
        play_real_investment("NO")

# 다음 아이템 버튼 (결과 확인 후)
if st.session_state.bet_status == "finished":
    if st.button("🚀 다음 아이템 투자하기", use_container_width=True):
        st.session_state.bet_status = "waiting"
        st.session_state.item_index = (st.session_state.item_index + 1) % len(ITEMS)
        st.session_state.lyrics = None
        st.rerun()

# 🏆 실시간 랭킹 영역
st.markdown("<div class='section-header'>🏆 실시간 군주 랭킹</div>", unsafe_allow_html=True)
all_ranks = st.session_state.rank_data + [{"name": "⭐ 나(사장님)", "score": st.session_state.balance}]
sorted_ranks = sorted(all_ranks, key=lambda x: x['score'], reverse=True)
ranking_html = '<div class="ranking-container">'
for i, r in enumerate(sorted_ranks[:5]):
    is_me = "my-rank" if r['name'] == "⭐ 나(사장님)" else ""
    ranking_html += f'<div class="rank-row {is_me}"><span>{i+1}위. {r["name"]}</span><span>{r["score"]:,}P</span></div>'
ranking_html += '</div>'
st.markdown(ranking_html, unsafe_allow_html=True)

# --- 3. [하단] AI 작사 영역 ---
st.markdown("---")
st.markdown("<div class='section-header'>🎵 1단계: 나만의 랭송 만들기</div>", unsafe_allow_html=True)

song_style = st.radio("🎸 노래 스타일 선택", ["🎤 감성 가요 버전 (Full)", "📢 강렬 홍보쏭 버전 (Short)"], horizontal=True)
user_story = st.text_area("스토리를 입력하세요", value=f"{current_item['title']} 투자 군주의 심정", height=100)

if st.button("🚀 AI 작사 시작", type="primary", use_container_width=True):
    models = ["gemini-3-flash", "gemini-3-pro", "gemini-2.5-flash", "gemini-1.5-flash"]
    if "홍보쏭" in song_style:
        prompt = f"너는 최고의 전문 작사가다. [Hook], [Verse], [Hook] 형식의 짧고 강렬한 30초 분량 홍보 CM송 가사만 써줘. 주제: '{user_story}'"
    else:
        prompt = f"너는 최고의 전문 작사가다. [Verse 1], [Chorus], [Verse 2], [Chorus], [Outro] 형식의 풀버전 K-pop 가사만 써줘. 주제: '{user_story}'"

    success = False
    with st.status("🛠️ AI 작사 엔진 가동 중...", expanded=True) as status:
        for m_name in models:
            try:
                url = f"https://generativelanguage.googleapis.com/v1/models/{m_name}:generateContent?key={MY_API_KEY}"
                res = requests.post(url, headers={'Content-Type': 'application/json'}, 
                                    data=json.dumps({"contents": [{"parts": [{"text": prompt}]}]}), timeout=30)
                if res.status_code == 200:
                    data = res.json()
                    st.session_state.lyrics = data['candidates'][0]['content']['parts'][0]['text']
                    status.update(label="✨ 작사 완료!", state="complete", expanded=False)
                    success = True; break
            except: continue
    if success: st.rerun()

if st.session_state.lyrics:
    st.markdown("<div class='section-header'>✨ 완성된 가사</div>", unsafe_allow_html=True)
    st.code(st.session_state.lyrics)
    st.link_button("🔥 Suno 열고 노래 만들기", "https://suno.com/create", use_container_width=True)

# --- ✨ [엔딩] 명품 푸터 ---
st.markdown("<br><br><hr style='border: 0.5px solid #eee;'>", unsafe_allow_html=True)
st.markdown(f"""
    <div class="premium-footer">
        <div class="footer-rank">PM PALM <span style="font-weight: 700; color: #444;">DecisionRank</span><sup style="font-size: 0.6rem;">TM</sup> 88.52 Ver.</div>
        <div style="color: #999; font-size: 0.75rem; letter-spacing: 1px; margin-top: 5px;">© 2026 Dr.Rang AI Lab. All Rights Reserved.</div>
    </div>
""", unsafe_allow_html=True)
