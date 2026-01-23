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