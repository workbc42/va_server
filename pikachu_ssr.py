""" Docstring
pikachu_ssr/
├── 01_pikachu_tag.py       # 1단계: 기본 태그
├── 02_pikachu_skills.py    # 2단계: 컨테이너+아이템  
├── 03_pikachu_form.py      # 3단계: GET 폼
├── 04_pikachu_data.py      # 4단계: 데이터 반영
└── 05_pikachu_atomic.py    # 5단계: 완전 재조립
"""
#────────────────────────────────────────────────────────────────────────────
# 01_pikachu_tag.py (15줄)
from http.server import HTTPServer, BaseHTTPRequestHandler

def pikachu():
    return "<div class='pokemon'>피카츄⚡️</div>"

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        html = f"<!DOCTYPE html><html><body>{pikachu()}</body></html>"
        self.wfile.write(html.encode('utf-8'))

if __name__ == '__main__':
    print("🚀 1단계: http://localhost:8000")
    HTTPServer(('localhost', 8000), Handler).serve_forever()


#────────────────────────────────────────────────────────────────────────────
# 02_pikachu_skills.py (20줄 - 01에 skill_list 추가)
# 01의 코드 + 아래 추가
def skill_item(name):
    return f"<li>{name}</li>"

def skill_list(skills):
    items = "".join(skill_item(s) for s in skills)
    return f"<ul class='skills'>{items}</ul>"

def pikachu_page():
    skills = ["10만볼트", "전광석화"]
    return f"<div class='pikachu'>{pikachu()}{skill_list(skills)}</div>"

# do_GET에서 html = f"...{pikachu_page()}..."


#────────────────────────────────────────────────────────────────────────────
# 03_pikachu_form.py (25줄 - GET 쿼리 파싱 추가)
def skill_form():
    return """
    <form method='GET'>
        <input name='skill' placeholder='스킬입력'>
        <button>배우기</button>
    </form>"""

def handler(path):  # ?skill=10만볼트 파싱
    skill = parse_qs(urlparse(path).query).get('skill', [''])[0]
    return f"<body>{skill_form()}<p>{skill}</p></body>"


#────────────────────────────────────────────────────────────────────────────
# 04_pikachu_data.py (30줄 - 데이터 반영)
PIKACHU = {"name": "피카츄", "skills": ["10만볼트", "전광석화"]}

def pikachu_card(skill=None):
    skills_html = skill_list(PIKACHU["skills"])
    return f"""
    <div class='card'>
        <h2>{PIKACHU['name']}</h2>
        {skills_html}
        <p>새스킬: {skill or '없음'}</p>
    </div>"""

#────────────────────────────────────────────────────────────────────────────
# 05_pikachu_atomic.py (35줄 - 재조립)
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

