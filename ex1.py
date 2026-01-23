def pikachu():
    return "<div class='pokemon'>피카츄⚡️</div>"

def handler(): 
    html = f"""
    <!DOCTYPE html>
    <html><body>{pikachu()}</body></html>"""
    return html

print(handler())

def skill_item(name):      # Atomic: 개별 li
    return f"<li>{name}</li>"

def skill_list(skills):    # 컨테이너: ul 감싸기
    items = "".join(skill_item(s) for s in skills)
    return f"<ul class='skills'>{items}</ul>"

def pikachu_page():
    skills = ["10만볼트", "전광석화"]
    return f"""
    <div class='pikachu'>
        {pikachu()}
        {skill_list(skills)}
    </div>"""

def skill_form():
    return """
    <form method='GET'>
        <input name='skill' placeholder='스킬입력'>
        <button>배우기</button>
    </form>"""

def handler(path):  # ?skill=10만볼트 파싱
    skill = parse_qs(urlparse(path).query).get('skill', [''])[0]
    return f"<body>{skill_form()}<p>{skill}</p></body>"

PIKACHU = {"name": "피카츄", "skills": ["10만볼트", "전광석화"]}

def pikachu_card(skill=None):
    skills_html = skill_list(PIKACHU["skills"])
    return f"""
    <div class='card'>
        <h2>{PIKACHU['name']}</h2>
        {skills_html}
        <p>새스킬: {skill or '없음'}</p>
    </div>"""

def text_node(text):      # Text Atomic
    return escape_html(text)

def element(tag, attrs, children):  # Element Atomic
    attr_str = " ".join(f'{k}="{v}"' for k,v in attrs.items())
    return f"<{tag} {attr_str}>{children}</{tag}>"

def pikachu_complete(skill):
    # 완전 재조립!
    return element("div", {"class": "pokemon-card"},
        element("h2", {}, text_node("피카츄⚡️")) +
        skill_list(PIKACHU["skills"]) +
        text_node(f"최신: {skill}")
    )
