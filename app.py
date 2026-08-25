import random
from collections import defaultdict
import streamlit as st

st.set_page_config(page_title="LearnQuest Mumbai", page_icon="🚀", layout="wide")
LEVELS = ["Easy", "Medium", "Hard", "Difficult"]

# Every listed subtopic has 10 knowledge areas x 10 question forms = 100 questions.
FACTS = {
"Plants": [("Which part absorbs water from soil?","Roots",["Leaves","Flower","Fruit"]),("Which part makes food using sunlight?","Leaves",["Roots","Stem","Seed"]),("Which part holds a plant upright?","Stem",["Petal","Fruit","Thorn"]),("Which part grows into a new plant?","Seed",["Leaf","Bark","Flower"]),("What do plants need to grow?","Water, air, sunlight, and soil",["Only toys","Only darkness","Only plastic"]),("Which part becomes a fruit?","Flower",["Root","Stem","Leaf"]),("What is germination?","A seed beginning to grow",["A leaf falling","A fruit drying","A flower closing"]),("Which part carries water to leaves?","Stem",["Petal","Fruit","Seed coat"]),("Why are leaves green?","They contain chlorophyll",["They drink ink","They grow only at night","They are made of grass"]),("Which plant do we eat as a root?","Carrot",["Mango","Spinach","Tomato"])],
"Animals": [("Which animal is a herbivore?","Cow",["Tiger","Eagle","Lion"]),("Which animal is a carnivore?","Tiger",["Goat","Deer","Cow"]),("Which animal lives on land and in water?","Frog",["Fish","Camel","Sparrow"]),("Which animal lays eggs?","Hen",["Dog","Cat","Cow"]),("Where does a fish live?","In water",["In a nest","In a burrow","On a tree"]),("Which animal has a trunk?","Elephant",["Horse","Rabbit","Monkey"]),("What eats plants and meat?","Omnivore",["Herbivore","Carnivore","Reptile"]),("Which animal carries a shell?","Turtle",["Dolphin","Parrot","Rabbit"]),("What helps a bird fly?","Wings",["Fins","Hooves","Paws"]),("Why do animals need habitats?","Food, water, and shelter",["To buy books","To watch television","To wear uniforms"])],
"English Grammar": [("Choose the noun.","Elephant",["Quickly","Jump","Happy"]),("Choose the verb.","Dance",["Purple","School","Tiny"]),("Choose the adjective.","Sparkly",["Run","Garden","Slowly"]),("Which is a pronoun?","She",["Riya","Table","Kind"]),("Complete: I ___ to school every day.","go",["goes","gone","going"]),("Complete: The dogs ___ loudly.","bark",["barks","barkinged","is bark"]),("Which sentence has correct capital letters?","Mumbai is busy.",["mumbai is busy.","mumbai Is busy.","mumbai is Busy."]),("Which mark ends a question?","Question mark (?)",["Full stop (.)","Comma (,)","Apostrophe (')"]),("Which word is plural?","Books",["Book","Child","Mango"]),("Choose: ___ apple is red.","An",["A","The","No article"])],
"Hindi शब्द भंडार": [("‘पानी’ का English word क्या है?","Water",["Fire","Wind","Food"]),("‘घर’ का English word क्या है?","House",["School","Tree","Road"]),("‘सूरज’ का English word क्या है?","Sun",["Moon","Star","Cloud"]),("‘किताब’ का English word क्या है?","Book",["Pen","Bag","Table"]),("‘आम’ किस प्रकार की वस्तु है?","फल",["जानवर","रंग","जगह"]),("‘बड़ा’ का विलोम शब्द चुनो।","छोटा",["लंबा","भारी","सुंदर"]),("‘दिन’ का विलोम शब्द चुनो।","रात",["सुबह","शाम","दोपहर"]),("कौन-सा शब्द एक रंग है?","लाल",["घर","कलम","बिल्ली"]),("कौन-सा शब्द जानवर का नाम है?","हाथी",["कुर्सी","किताब","नदी"]),("‘खुश’ का विलोम शब्द चुनो।","दुखी",["तेज़","मीठा","साफ़"])],
"Marathi शब्दसंग्रह": [("‘पाणी’ म्हणजे काय?","Water",["Book","Sun","Tree"]),("‘घर’ म्हणजे काय?","House",["Road","School","Garden"]),("‘फूल’ म्हणजे काय?","Flower",["Fruit","Animal","Colour"]),("‘आंबा’ कोणता आहे?","फळ",["पक्षी","रंग","खेळ"]),("‘मोठा’चा विरुद्धार्थी शब्द कोणता?","लहान",["उंच","जाड","नवा"]),("‘दिवस’चा विरुद्धार्थी शब्द कोणता?","रात्र",["सकाळ","संध्याकाळ","दुपार"]),("कोणता शब्द रंगाचे नाव आहे?","हिरवा",["घर","पुस्तक","मांजर"]),("कोणता शब्द प्राण्याचे नाव आहे?","मांजर",["टेबल","पेन","शाळा"]),("‘शाळा’ म्हणजे काय?","School",["Hospital","Market","Station"]),("‘आनंदी’चा विरुद्धार्थी शब्द कोणता?","दुःखी",["गोड","वेगवान","स्वच्छ"])],
"National Symbols": [("What is India's national animal?","Bengal Tiger",["Lion","Elephant","Leopard"]),("What is India's national bird?","Indian Peacock",["Parrot","Eagle","Sparrow"]),("What is India's national flower?","Lotus",["Rose","Sunflower","Jasmine"]),("What is India's national tree?","Banyan",["Coconut","Mango","Pine"]),("What is India's national fruit?","Mango",["Apple","Banana","Grapes"]),("What are the flag colours?","Saffron, white, and green",["Red, blue, and yellow","Black, white, and red","Orange, pink, and purple"]),("What is at the flag's centre?","Ashoka Chakra",["Star","Lotus","Tiger"]),("How many spokes are in the Ashoka Chakra?","24",["12","18","36"]),("What is India's national anthem?","Jana Gana Mana",["Vande Mataram","Saare Jahan Se Achha","Maa Tujhe Salaam"]),("What is India's national river?","Ganga",["Yamuna","Godavari","Narmada"])],
"Historical Monuments": [("In which city is the Taj Mahal?","Agra",["Mumbai","Delhi","Pune"]),("Which monument is in Mumbai?","Gateway of India",["Red Fort","Qutub Minar","Charminar"]),("In which city is the Red Fort?","Delhi",["Agra","Mumbai","Jaipur"]),("Which monument is a tall tower in Delhi?","Qutub Minar",["Gateway of India","Taj Mahal","India Gate"]),("Why protect monuments?","They teach us about history",["To paint on them","To break them","To play inside them"]),("Who built the Taj Mahal?","Shah Jahan",["Akbar","Ashoka","Shivaji"]),("Which is a big gateway in Delhi?","India Gate",["Taj Mahal","Charminar","Gateway of India"]),("Which city has Charminar?","Hyderabad",["Kolkata","Chennai","Mumbai"]),("What should we not do at monuments?","Write on their walls",["Read about them","Keep them clean","Listen to a guide"]),("Which monument stands near Mumbai harbour?","Gateway of India",["Red Fort","Mysore Palace","Sanchi Stupa"])],
"Basic Geography": [("What is India's capital city?","New Delhi",["Mumbai","Kolkata","Chennai"]),("India is in which continent?","Asia",["Europe","Africa","Australia"]),("Where does the Sun rise?","East",["West","North","South"]),("What helps find places and directions?","Map",["Spoon","Pillow","Paintbrush"]),("Which is a huge salty water body?","Ocean",["Pond","River","Well"]),("Mumbai is in which state?","Maharashtra",["Gujarat","Goa","Kerala"]),("What is a globe?","A model of the Earth",["A plant","A railway station","A weather tool"]),("What is opposite east?","West",["North","South","Up"]),("What is land surrounded by water?","Island",["Mountain","Desert","Forest"]),("What divides Earth into north and south halves?","Equator",["Prime Meridian","Tropic of Cancer","Horizon"])],
}

TOPICS = {"Maths":["Number Skills","Geometry & Measurement"],"Science":["Plants","Animals"],"English":["English Grammar"],"Hindi":["Hindi शब्द भंडार"],"Marathi":["Marathi शब्दसंग्रह"],"Social Studies":["National Symbols","Historical Monuments","Basic Geography"],"Logical Reasoning":["Patterns & Puzzles"]}

def opts(answer, wrong, seed):
    result = list(dict.fromkeys([answer, *wrong])); random.Random(seed).shuffle(result); return result

def fact_bank(topic, level):
    notes = {"Easy":"Quick check!","Medium":"Think carefully.","Hard":"Brain boost: choose precisely.","Difficult":"Master challenge: reason carefully."}[level]
    bank=[]
    for group,(question,answer,wrong) in enumerate(FACTS[topic]):
        for variant in range(10):
            bank.append({"group":group,"q":f"{notes}\n\n{question}","a":answer,"o":opts(answer,wrong,f"{topic}{level}{group}{variant}"),"why":f"Correct answer: {answer}."})
    return bank

def maths_or_logic(subject, topic, level):
    size={"Easy":9,"Medium":14,"Hard":20,"Difficult":30}[level]; r=random.Random(f"{subject}{topic}{level}"); bank=[]
    for i in range(100):
        if subject=="Maths" and topic=="Geometry & Measurement":
            name,sides=[("triangle",3),("square",4),("pentagon",5),("hexagon",6)][i%4]
            if i%2: q,a=f"How many sides does a {name} have?",str(sides)
            else:
                side=r.randint(2,size); q,a=f"A {name} has sides of {side} cm each. What is its perimeter?",f"{side*sides} cm"
            wrong=[str(max(1,sides-1)),str(sides+1),str(sides+2)] if a.isdigit() else [f"{side*(sides-1)} cm",f"{side*(sides+1)} cm",f"{side*(sides+2)} cm"]
        elif subject=="Maths":
            x,y=r.randint(2,size),r.randint(2,size)
            if i%3==0: q,a=f"What is {x} × {y}?",str(x*y)
            elif i%3==1: q,a=f"{x*y} ÷ {x} = ?",str(y)
            else: q,a=f"Ayaan has {x} packets with {y} stickers each. How many stickers?",str(x*y)
            n=int(a); wrong=[str(max(0,n-x)),str(n+y),str(max(1,n-y))]
        else:
            start,step=r.randint(1,size),r.randint(2,max(3,size//2)); seq=[start+step*j for j in range(4)]; a=str(start+step*4); q=f"What comes next? {', '.join(map(str,seq))}, ___"; wrong=[str(int(a)-1),str(int(a)+1),str(int(a)+step)]
        bank.append({"group":i%10,"q":q,"a":a,"o":opts(a,wrong,i),"why":f"The correct answer is {a}."})
    return bank

def bank_for(subject,topic,level): return maths_or_logic(subject,topic,level) if subject in ["Maths","Logical Reasoning"] else fact_bank(topic,level)

def start(subject,topic,level):
    grouped=defaultdict(list)
    for q in bank_for(subject,topic,level): grouped[q["group"]].append(q)
    r=random.Random(); questions=[r.choice(grouped[g]) for g in sorted(grouped)]; r.shuffle(questions)
    st.session_state.run={"subject":subject,"topic":topic,"level":level,"qs":questions,"i":0,"score":0,"checked":False}

if "stars" not in st.session_state: st.session_state.stars=0
if "run" not in st.session_state: st.session_state.run=None

st.markdown("""<style>
.stApp{background:#f7f8fc;color:#182230}.block-container{max-width:960px;padding-top:1.3rem}.hero{background:linear-gradient(120deg,#6d4aff,#2d5bff);color:#fff;padding:24px 30px;border-radius:22px;margin-bottom:20px}.hero h1{margin:0}.card{background:#fff;padding:22px;border-radius:18px;box-shadow:0 4px 18px #e1e6f1}div.stButton>button{background:#6d4aff!important;color:#fff!important;border:0!important;border-radius:12px!important;font-weight:800!important;min-height:44px}div.stButton>button *{color:#fff!important}div[data-baseweb="select"]>div{background:#fff!important;border:2px solid #b8c1d1!important;border-radius:10px!important}div[data-baseweb="select"] *{color:#182230!important}</style>""",unsafe_allow_html=True)
st.markdown("<div class='hero'><h1>🚀 LearnQuest Mumbai</h1><p>Hi, Ayaan! Build your brain with a fresh Daily 10.</p></div>",unsafe_allow_html=True)

if st.session_state.run is None:
    a,b=st.columns([1.5,1])
    with a:
        st.markdown("### Choose today's mission")
        subject=st.selectbox("Subject",list(TOPICS)); topic=st.selectbox("Subtopic",TOPICS[subject]); level=st.select_slider("Difficulty",LEVELS,value="Medium")
        st.info(f"📚 **100 questions** are ready for **{topic}** at **{level}** level. Today's mission is 10 varied questions.")
        if st.button("Start my Daily 10 🚀",use_container_width=True): start(subject,topic,level); st.rerun()
    with b: st.markdown(f"<div class='card'><h3>⭐ My stars</h3><h1>{st.session_state.stars}</h1><p>Every correct answer earns one star.</p><hr><b>Daily rhythm</b><p>Choose any subtopic and difficulty. Ayaan gets a fresh set of 10 questions from its 100-question bank every day.</p></div>",unsafe_allow_html=True)
else:
    run=st.session_state.run
    if run["i"]==10:
        st.balloons(); st.success(f"Daily 10 complete! Ayaan scored {run['score']} out of 10 in {run['topic']}.")
        if st.button("Choose another Daily 10"): st.session_state.run=None; st.rerun()
    else:
        q=run["qs"][run["i"]]; st.progress(run["i"]/10,text=f"Question {run['i']+1} of 10 · {run['subject']} › {run['topic']} · {run['level']}")
        st.markdown("<div class='card'>",unsafe_allow_html=True); st.markdown(f"### {q['q']}")
        answer=st.selectbox("Tap to choose an answer",q["o"],index=None,placeholder="Choose your answer…",key=f"answer-{run['i']}")
        if not run["checked"]:
            if st.button("Check my answer",use_container_width=True):
                if answer is None: st.warning("Choose an answer first, Ayaan!")
                else:
                    run["checked"]=True; run["correct"]=answer==q["a"]
                    if run["correct"]: run["score"]+=1; st.session_state.stars+=1
                    st.rerun()
        else:
            st.success("Brilliant! ⭐") if run["correct"] else st.info("Good try! "+q["why"])
            if st.button("Next question →",use_container_width=True): run["i"]+=1; run["checked"]=False; st.rerun()
        st.markdown("</div>",unsafe_allow_html=True)
