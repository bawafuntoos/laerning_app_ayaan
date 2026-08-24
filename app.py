import random
import streamlit as st


st.set_page_config(page_title="LearnQuest Mumbai", page_icon="🚀", layout="wide")

SUBJECTS = {
    "Maths": {"emoji": "🔢", "colour": "#7C4DFF", "tag": "Number Ninja", "lessons": [
        ("How much is 7 × 8?", ["54", "56", "63", "48"], "56", "7 groups of 8 make 56."),
        ("A Mumbai local has 36 passengers. 14 get down. How many stay?", ["20", "22", "24", "50"], "22", "36 − 14 = 22."),
        ("Which fraction shows half a pizza?", ["1/3", "1/2", "1/4", "2/3"], "1/2", "A half means 1 out of 2 equal parts."),
    ]},
    "Science": {"emoji": "🔬", "colour": "#00A884", "tag": "Curious Scientist", "lessons": [
        ("Which part of a plant takes in water from soil?", ["Flower", "Leaf", "Root", "Fruit"], "Root", "Roots absorb water and hold the plant in place."),
        ("Which is a source of light?", ["Moon", "Mirror", "Sun", "Book"], "Sun", "The Sun makes its own light."),
        ("What do we breathe in to stay alive?", ["Oxygen", "Water", "Sand", "Smoke"], "Oxygen", "Our lungs take oxygen from the air."),
    ]},
    "English": {"emoji": "📚", "colour": "#3F8EFC", "tag": "Word Wizard", "lessons": [
        ("Which word is a naming word (noun)?", ["Jump", "Happy", "Elephant", "Quickly"], "Elephant", "A noun names a person, place, animal, or thing."),
        ("Choose the correct word: I ___ to school every day.", ["go", "goes", "going", "gone"], "go", "With ‘I’, we say ‘I go’."),
        ("Which word rhymes with ‘cat’?", ["Dog", "Hat", "Sun", "Tree"], "Hat", "Cat and hat end with the same sound: ‘at’."),
    ]},
    "Hindi": {"emoji": "अ", "colour": "#FF7043", "tag": "शब्द सितारा", "lessons": [
        ("‘पानी’ का सही English word क्या है?", ["Fire", "Water", "Wind", "Food"], "Water", "पानी = Water."),
        ("‘बड़ा’ का विलोम शब्द चुनो।", ["लंबा", "छोटा", "मोटा", "सुंदर"], "छोटा", "बड़ा का विलोम छोटा है।"),
        ("कौन-सा शब्द एक फल है?", ["आम", "घर", "कलम", "किताब"], "आम", "आम एक मीठा फल है।"),
    ]},
    "Marathi": {"emoji": "अ", "colour": "#EC407A", "tag": "मराठी मित्र", "lessons": [
        ("‘पाणी’ म्हणजे काय?", ["Water", "Book", "Sun", "Tree"], "Water", "पाणी म्हणजे Water."),
        ("‘मोठा’चा विरुद्धार्थी शब्द निवडा.", ["लहान", "उंच", "गोड", "नवा"], "लहान", "मोठा विरुद्ध लहान."),
        ("कोणता शब्द प्राण्याचे नाव आहे?", ["मांजर", "टेबल", "पेन", "शाळा"], "मांजर", "मांजर हा एक पाळीव प्राणी आहे."),
    ]},
    "Social Studies": {"emoji": "🌏", "colour": "#FFB300", "tag": "Mumbai Explorer", "lessons": [
        ("Mumbai is in which state?", ["Gujarat", "Maharashtra", "Goa", "Kerala"], "Maharashtra", "Mumbai is the capital city of Maharashtra."),
        ("Which place is a famous Mumbai landmark?", ["Gateway of India", "Taj Mahal", "Red Fort", "Charminar"], "Gateway of India", "The Gateway of India stands near the Mumbai harbour."),
        ("Why do we need rules in school?", ["To stay safe and learn well", "To make more noise", "To skip class", "To lose things"], "To stay safe and learn well", "Rules help everyone feel safe, fair, and ready to learn."),
    ]},
    "Logical Reasoning": {"emoji": "🧩", "colour": "#5C6BC0", "tag": "Brain Detective", "lessons": [
        ("What comes next? 2, 4, 6, 8, ___", ["9", "10", "12", "16"], "10", "The numbers increase by 2 each time."),
        ("Find the odd one out.", ["Circle", "Square", "Triangle", "Apple"], "Apple", "The first three are shapes; an apple is a fruit."),
        ("If today is Monday, what day comes after Wednesday?", ["Tuesday", "Thursday", "Friday", "Sunday"], "Thursday", "The days go Monday, Tuesday, Wednesday, Thursday."),
    ]},
}


def setup_state():
    defaults = {"stars": 0, "streak": 1, "done": set(), "answers": {}, "view": "Home"}
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def subject_card(name, data):
    completed = sum(f"{name}-{i}" in st.session_state.done for i in range(3))
    st.markdown(f"""
    <div class='subject-card' style='border-top: 7px solid {data["colour"]};'>
      <div class='card-emoji'>{data["emoji"]}</div><div>
      <h3>{name}</h3><p>{data["tag"]}</p><div class='progress'><span style='width:{completed / 3 * 100}%; background:{data["colour"]}'></span></div>
      <small>{completed}/3 missions finished</small></div>
    </div>""", unsafe_allow_html=True)
    if st.button(f"Explore {name}", key=f"open-{name}", use_container_width=True):
        st.session_state.view = name
        st.rerun()


def mission_page(subject, data):
    st.button("← Back to my map", on_click=lambda: st.session_state.update(view="Home"))
    st.markdown(f"<div class='hero' style='background:linear-gradient(115deg, {data["colour"]}, #1e293b)'><span>{data["emoji"]}</span><div><h1>{subject} Quest</h1><p>{data["tag"]} · Choose a mission and earn stars!</p></div></div>", unsafe_allow_html=True)
    for index, (question, options, answer, clue) in enumerate(data["lessons"]):
        key = f"{subject}-{index}"
        with st.container(border=True):
            status = "⭐ Completed" if key in st.session_state.done else f"Mission {index + 1}"
            st.markdown(f"**{status}**")
            st.markdown(f"### {question}")
            choice = st.radio("Pick your answer", options, key=f"pick-{key}", index=None, horizontal=True, label_visibility="collapsed")
            if st.button("Check my answer", key=f"check-{key}"):
                if choice is None:
                    st.warning("Pick an answer first, explorer!")
                elif choice == answer:
                    if key not in st.session_state.done:
                        st.session_state.done.add(key)
                        st.session_state.stars += 10
                    st.balloons()
                    st.success(f"Amazing! {clue} You earned 10 stars!")
                else:
                    st.info("Nice try! Think once more — you can do it. 💪")
            if key in st.session_state.done:
                st.caption(f"💡 {clue}")


setup_state()

st.markdown("""
<style>
    .stApp { background: #f7f8fc; color: #1e293b; }
    .block-container { padding-top: 1.5rem; max-width: 1120px; }
    .topbar {display:flex; align-items:center; justify-content:space-between; background:#fff; padding:15px 22px; border-radius:20px; box-shadow:0 4px 18px #dce2ef; margin-bottom:24px;}
    .brand {font-size:1.5rem; font-weight:800;} .brand span {color:#7C4DFF;}
    .pill {display:inline-block; background:#fff4cb; border-radius:20px; padding:7px 13px; font-weight:700; margin-left:7px;}
    .subject-card {background:#fff; border-radius:18px; padding:18px; min-height:155px; box-shadow:0 4px 15px #e3e7f0; display:flex; gap:14px; margin-bottom:9px;}
    .subject-card h3 {margin:0; font-size:1.2rem;} .subject-card p {margin:4px 0 11px; color:#667085;}
    .card-emoji {font-size:2.6rem;} .progress {height:8px; background:#edf0f5; border-radius:8px; overflow:hidden; width:100%;}.progress span {display:block; height:100%; border-radius:8px;}
    .hero {color:#fff; padding:26px 32px; border-radius:24px; display:flex; gap:20px; align-items:center; margin-bottom:20px;} .hero span {font-size:4rem;} .hero h1 {margin:0;} .hero p {margin:4px 0 0;}
    .tip {background:#e6f6ff; border-radius:16px; padding:16px 20px; border-left:5px solid #22a7f0;}
    /* High-contrast controls make the app easy to use on phones and dark browser themes. */
    div.stButton > button, button[kind="secondary"] {background:#6D4AFF !important; color:#FFFFFF !important; border:0 !important; border-radius:12px !important; font-weight:750 !important; min-height:44px !important;}
    div.stButton > button:hover, button[kind="secondary"]:hover {background:#5134CE !important; color:#FFFFFF !important; border:0 !important;}
    div.stButton > button * {color:#FFFFFF !important;}
    [data-baseweb="radio"] label {background:#FFFFFF !important; color:#182230 !important; border:2px solid #D0D5DD !important; border-radius:10px !important; padding:9px 12px !important; margin:4px !important;}
    [data-baseweb="radio"] label *, [data-baseweb="radio"] label div {color:#182230 !important;}
    [data-baseweb="radio"] label:has(input:checked) {border-color:#6D4AFF !important; background:#F0ECFF !important;}
</style>""", unsafe_allow_html=True)

done_count = len(st.session_state.done)
st.markdown(f"<div class='topbar'><div class='brand'>🚀 Learn<span>Quest</span> Mumbai</div><div><span class='pill'>🔥 {st.session_state.streak} day streak</span><span class='pill'>⭐ {st.session_state.stars} stars</span></div></div>", unsafe_allow_html=True)

if st.session_state.view == "Home":
    st.markdown("## Hi, Champion! 👋")
    st.markdown("### Today’s adventure is waiting")
    st.markdown("<div class='tip'>🌟 <b>Little steps, big learning!</b> Finish any 3 missions today to become a LearnQuest Hero.</div>", unsafe_allow_html=True)
    st.write("")
    left, right = st.columns([1.6, 1])
    with left:
        st.markdown("### Pick a world to explore")
        grid = st.columns(2)
        for i, (name, data) in enumerate(SUBJECTS.items()):
            with grid[i % 2]:
                subject_card(name, data)
    with right:
        st.markdown("### My explorer badge")
        st.metric("Missions complete", f"{done_count} / 21")
        if done_count >= 9:
            badge = "🏆 Learning Legend"
        elif done_count >= 3:
            badge = "🦁 Brave Explorer"
        else:
            badge = "🐣 Quest Starter"
        st.success(f"**{badge}**\n\nKeep collecting stars. Every answer helps your brain grow!")
        st.markdown("### Grown-up corner")
        st.caption("This app uses short, encouraging practice — ideal for 10–15 minutes a day. Answers stay only in this browser session.")
else:
    mission_page(st.session_state.view, SUBJECTS[st.session_state.view])
