from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs  # 쿼리 + 폼 파싱 모두 가능

PORT = 8000

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """
        GET 요청: 쿼리스트링 파싱
        테스트: http://localhost:8000/search?q=파이썬&page=2
        """
        # 1. URL 파싱
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()

        # 2. 경로별 응답
        if path == "/":
            body = """
                <h1>🏠 홈페이지</h1>
                <p><a href="/search?q=파이썬&page=2">🔍 GET 검색 테스트</a></p>
                <p><a href="/form">📝 POST 폼 테스트</a></p>
            """
        elif path == "/search":
            search_query = query_params.get('q', [''])[0]
            page = query_params.get('page', ['1'])[0]
            
            body = f"""
                <h1>🔍 GET 검색 결과</h1>
                <p>검색어: <b>{search_query}</b></p>
                <p>페이지: <b>{page}</b></p>
                <p>총 <b>{len(search_query)}자</b> 검색됨</p>
                <hr>
                <a href="/">🏠 홈으로</a>
            """
        elif path == "/form":
            # GET으로 폼 페이지 보여주기
            body = """
                <h1>📝 POST 폼 입력</h1>
                <form method="POST" action="/submit">
                    이름: <input type="text" name="name" required><br><br>
                    나이: <input type="number" name="age" min="1" max="100"><br><br>
                    <button type="submit">🚀 제출하기</button>
                </form>
                <hr>
                <a href="/">🏠 홈으로</a>
            """
        else:
            self.send_response(404)
            body = "<h1>❌ 404 페이지 없음</h1><a href='/'>홈으로</a>"
        
        self.wfile.write(body.encode('utf-8'))

    def do_POST(self):
        """
        POST 요청: 폼 데이터 파싱 (cgi 없이 urllib.parse만 사용)
        """
        # 1. 바디 크기 확인
        content_length = int(self.headers.get('Content-Length', 0))
        
        # 2. 바디 읽기 (바이트 → 문자열)
        post_body = self.rfile.read(content_length).decode('utf-8')
        
        # 3. 폼 데이터 파싱 (name=value&name2=value2 형식)
        form_data = parse_qs(post_body)
        
        # 4. 값 꺼내기 (안전하게 기본값 처리)
        name = form_data.get('name', [''])[0]
        age = form_data.get('age', [''])[0]
        
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        
        body = f"""
            <h1>✅ POST 폼 제출 완료!</h1>
            <div style="background:#e8f5e8; padding:20px;">
                <p><b>이름:</b> {name or '미입력'}</p>
                <p><b>나이:</b> {age or '미입력'}</p>
            </div>
            <p>📋 개발자도구(F12) → Network 탭에서 POST 요청 확인하세요!</p>
            <hr>
            <a href="/form">📝 다시 폼으로</a> | <a href="/">🏠 홈으로</a>
        """
        self.wfile.write(body.encode('utf-8'))

# 서버 실행
if __name__ == "__main__":
    server = HTTPServer(("localhost", PORT), RequestHandler)
    print(f"🚀 서버 시작: http://localhost:{PORT}")
    print("📋 GET 테스트: http://localhost:8000/search?q=파이썬")
    print("📋 POST 테스트: http://localhost:8000/form → 폼 제출")
    print("⚠️  Ctrl+C로 종료")
    server.serve_forever()
