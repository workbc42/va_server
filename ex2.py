from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# ========================================
# 1~5단계 모든 함수 (Atomic → Complete)
# ========================================

# 1단계: 기본 태그
def pikachu():
    return "<div class='pokemon'>피카츄⚡️</div>"

# 2단계: Atomic 아이템 + 컨테이너
def skill_item(name):
    return f"<li>{name}</li>"

def skill_list(skills):
    items = "".join(skill_item(s) for s in skills)
    return f"<ul class='skills'>{items}</ul>"

# 3단계: 폼
def skill_form():
    return """
    <form method='GET'>
        <input name='skill' placeholder='스킬입력'>
        <button>배우기</button>
    </form>"""

# 4단계: 데이터
PIKACHU = {"name": "피카츄", "skills": ["10만볼트", "전광석화"]}

def pikachu_card(skill=None):
    skills_html = skill_list(PIKACHU["skills"])
    return f"""
    <div class='card'>
        <h2>{PIKACHU['name']}</h2>
        {skills_html}
        <p>새스킬: {skill or '없음'}</p>
    </div>"""

# 5단계: Atomic 재조립 (XSS 방지 포함)
def escape_html(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def text_node(text):
    return escape_html(text)

def element(tag, attrs, children):
    attr_str = " ".join(f'{k}="{escape_html(v)}"' for k,v in attrs.items())
    return f"<{tag} {attr_str}>{children}</{tag}>"

def pikachu_complete(skill):
    safe_skill = escape_html(skill or '없음')
    return element("div", {"class": "pokemon-card"},
        element("h2", {}, text_node("피카츄⚡️")) +
        skill_list(PIKACHU["skills"]) +
        text_node(f"최신스킬: {safe_skill}")
    )

# ========================================
# 통합 핸들러 (1~5단계 모두 동작)
# ========================================
class PikachuHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 쿼리 파싱 (?skill=10만볼트)
        skill = parse_qs(urlparse(self.path).query).get('skill', [''])[0]
        
        # 1~5단계 중 하나 선택 (확장 가능)
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset='utf-8'>
    <title>피카츄 SSR 서버</title>
    <style>
        .pokemon-card {{ border: 2px solid gold; padding: 20px; margin: 20px; }}
        .skills {{ color: orange; }}
        form {{ margin: 20px 0; }}
    </style>
</head>
<body>
    <h1>🚀 SSR 5단계 완성! ({self.path})</h1>
    
    <h2>1단계: 기본태그</h2>{pikachu()}
    <h2>2단계: 스킬리스트</h2>{pikachu_card()}
    <h2>3단계: 폼</h2>{skill_form()}
    <h2>4단계: 데이터반영</h2>{pikachu_card(skill)}
    <h2>5단계: Atomic완성</h2>
    <div>{pikachu_complete(skill)}</div>
</body></html>"""
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

# ========================================
# 서버 실행
# ========================================
if __name__ == '__main__':
    print("🚀 피카츄 SSR 서버 (5단계 완성)")
    print("http://localhost:8000/?skill=10만볼트")
    print("Ctrl+C로 종료")
    print("-" * 50)
    
    server = HTTPServer(('localhost', 8000), PikachuHandler)
    server.serve_forever()
