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

# 2. 🎨 [CSS] 디자인 & 모바일 최적화 (반응형 추가)
st.markdown("""
    <style>
    /* 1. 전체 배경 */
    .stApp { background-color: transparent; }
    
   /* 2. 버튼 공통: 높이를 자동으로 하여 글자가 짤리지 않게 함 */
    .stButton button {
        width: 100% !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
        height: auto !important;
        padding: 12px 5px !important;
    }

    /* 3. 윗줄 포인트 버튼: 흰색 바탕에 테두리 */
    button[key*="p_btn"] {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #eeeeee !important;
    }

    /* 4. 아랫줄 YES 버튼: 파란색 */
    button[key*="v_btn_yes"] {
        background-color: #007bff !important;
        color: white !important;
    }

    /* 5. 아랫줄 NO 버튼: 빨간색 */
    button[key*="v_btn_no"] {
        background-color: #ff4b4b !important;
        color: white !important;
    }
    
    /* 6. 포인트 선택 버튼: 흰색 바탕 */
    div[data-testid="stHorizontalBlock"] button[key*="p_btn"] { 
        background-color: #ffffff !important; color: #000000 !important; border: 2px solid #ddd !important; font-weight: 900 !important;
    }
    
    /* 랭킹 컨테이너 */
    .ranking-container { background-color: #1e1e1e; padding: 15px; border-radius: 15px; color: white; margin: 15px 0; }
    .rank-row { display: flex; justify-content: space-between; padding: 12px; border-bottom: 1px solid #333; }
    .my-rank { background-color: #2c3e50; border: 1px solid #4da3ff; border-radius: 8px; color: #ffcc00; }
    
    /* 투자 가이드 박스 */
    .invest-guide {
        background-color: #fff9db; border-left: 5px solid #ffcc00; padding: 15px;
        border-radius: 10px; color: #856404; margin: 15px 0; text-align: center; font-size: 1.1rem; font-weight: bold;
    }

    /* 대시보드 자산 텍스트 클래스 */
    .balance-text { font-size: 2.8rem; font-weight: 800; color: #4da3ff; }

    /* 명품 푸터 스타일 */
    .premium-footer { text-align: center; padding-top: 50px; padding-bottom: 20px; font-family: 'serif'; }
    .footer-rank { color: #666; font-size: 1rem; letter-spacing: 1px; margin-bottom: 5px; }
    
    /* 섹션 헤더 */
    .section-header { font-size: 1.3rem; font-weight: bold; color: #31333F; margin-top: 25px; margin-bottom: 15px; white-space: nowrap; }

    /* 📱 [모바일 최적화] 화면 폭 600px 이하일 때 적용 */
    @media (max-width: 600px) {
        .balance-text { font-size: 2.1rem !important; } /* 자산 숫자 크기 축소 */
        .section-header { font-size: 1.1rem !important; } /* 헤더 크기 축소 */
        .invest-guide { font-size: 1rem !important; padding: 10px !important; }
        h1 { font-size: 1.5rem !important; } /* 메인 타이틀 축소 */
        h3 { font-size: 0.9rem !important; } /* 서브 타이틀 축소 */
        .stButton button { font-size: 0.85rem !important; } /* 버튼 글자 뭉침 방지 */
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

# --- ✨ [상단] 타이틀 영역 ---
st.markdown("<h1 style='text-align: center; color: #ffcc00; margin-bottom: 0;'>Dr.Rang (닥터랭)</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #ffcc00; margin-top: 5px; font-weight: normal;'>당신의 스토리가 음악이 되는 공간</h3>", unsafe_allow_html=True)
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

# --- 💰 [1단] 투자 포인트 선택 (3칸 배치) ---
st.markdown(f"<div class='section-header'>💰 투자 포인트 선택</div>", unsafe_allow_html=True)
p_cols = st.columns(3)
pts = ["100P", "500P", "1000P"]

for i, p_val in enumerate(pts):
    with p_cols[i]:
        label = f"✔️ {p_val}" if st.session_state.p_choice == p_val else p_val
        if st.button(label, key=f"p_btn_{p_val}", use_container_width=True, disabled=(st.session_state.bet_status == "finished")):
            st.session_state.p_choice = p_val
            st.rerun()

# --- 🔥 [2단] YES / NO 결정 (2칸 배치) ---
st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True) 
v_cols = st.columns(2)

with v_cols[0]:
    if st.button("YES 🔥", key="v_btn_yes", type="primary", use_container_width=True, disabled=(st.session_state.bet_status == "finished")):
        play_real_investment("YES")

with v_cols[1]:
    if st.button("NO ❄️", key="v_btn_no", use_container_width=True, disabled=(st.session_state.bet_status == "finished")):
        play_real_investment("NO")

if st.session_state.bet_status == "finished":
    if st.button("🚀 다음 아이템 투자하기 (영상 교체)", use_container_width=True):
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

if st.button("🚀 AI 작사 시작 (Gemini 3 정식 엔진 가동)", type="primary", use_container_width=True):
    models = ["gemini-3-flash", "gemini-3-pro", "gemini-2.5-flash", "gemini-1.5-flash"]
    
    if "홍보쏭" in song_style:
        prompt = f"너는 최고의 전문 작사가다. [Hook], [Verse], [Hook] 형식의 짧고 강렬한 30초 분량 홍보 CM송 가사만 써줘. 주제: '{user_story}'"
    else:
        prompt = f"너는 최고의 전문 작사가다. [Verse 1], [Chorus], [Verse 2], [Chorus], [Outro] 형식의 풀버전 K-pop 가사만 써줘. 주제: '{user_story}'"

    success = False
    error_logs = []
    
    with st.status("🛠️ 정식 엔진 경로(v1) 탐색 중...", expanded=True) as status:
        for idx, m_name in enumerate(models):
            st.write(f"🔄 ({idx+1}/{len(models)}) {m_name} 엔진 가동 시도...")
            try:
                for path in ["v1", "v1beta"]:
                    url = f"https://generativelanguage.googleapis.com/{path}/models/{m_name}:generateContent?key={MY_API_KEY}"
                    res = requests.post(url, headers={'Content-Type': 'application/json'}, 
                                        data=json.dumps({"contents": [{"parts": [{"text": prompt}]}]}), timeout=30)
                    
                    if res.status_code == 200:
                        data = res.json()
                        if 'candidates' in data and data['candidates'][0].get('content'):
                            st.session_state.lyrics = data['candidates'][0]['content']['parts'][0]['text']
                            status.update(label="✨ 작사 완료!", state="complete", expanded=False)
                            success = True; break
                    elif res.status_code == 404: continue
                if success: break
                else:
                    err_msg = res.json().get('error', {}).get('message', 'Engine Failure')
                    error_logs.append(f"{m_name}: {res.status_code} ({err_msg})")
            except Exception as e:
                error_logs.append(f"{m_name}: {str(e)}")
                continue
                
    if success: st.rerun()
    else:
        st.error("❌ 작사 실패. API 키나 로그를 확인하세요.")
        with st.expander("에러 상세 로그"):
            for log in error_logs: st.write(log)

if st.session_state.lyrics:
    st.markdown("<div class='section-header'>✨ 완성된 가사</div>", unsafe_allow_html=True)
    st.code(st.session_state.lyrics)
    safe_lyrics = st.session_state.lyrics.replace("`", "'").replace("\n", "\\n")
    copy_js = f"""<button onclick="copyToClipboard()" style="width:100%; height:48px; background-color:#28a745; color:white; border:none; border-radius:10px; font-weight:bold; cursor:pointer;">📋 가사 복사하기</button><script>function copyToClipboard() {{const text = `{safe_lyrics}`;const el = document.createElement('textarea');el.value = text;document.body.appendChild(el);el.select();document.execCommand('copy');document.body.removeChild(el);alert('가사가 복사되었습니다!');}}</script>"""
    components.html(copy_js, height=60)
    st.link_button("🔥 Suno 열고 노래 만들기", "https://suno.com/create", use_container_width=True)

# --- ✨ [엔딩] 명품 푸터 ---
st.markdown("<br><br><hr style='border: 0.5px solid #eee;'>", unsafe_allow_html=True)
st.markdown(f"""
    <div class="premium-footer">
        <div class="footer-rank">
            PM PALM <span style="font-weight: 700; color: #444;">DecisionRank</span><sup style="font-size: 0.6rem;">TM</sup> 88.52 Ver.
        </div>
        <div style="color: #999; font-size: 0.75rem; letter-spacing: 1px; margin-top: 5px;">
            © 2026 Dr.Rang AI Lab. All Rights Reserved.
        </div>
    </div>
""", unsafe_allow_html=True)
