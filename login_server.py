from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import uuid
import hashlib
import html

PORT = 8000

# 1. 하드코딩 사용자 DB (실제론 DB)
USERS = {
    "test": hashlib.sha256("1234".encode()).hexdigest(),  # 비밀번호 해싱
    "admin": hashlib.sha256("admin".encode()).hexdigest()
}

# 2. 세션 저장소 (메모리)
SESSIONS = {}

class LoginHandler(BaseHTTPRequestHandler):
    def get_session_id(self):
        """쿠키에서 session_id 추출"""
        cookie_header = self.headers.get('Cookie', '')
        if 'session_id=' in cookie_header:
            return cookie_header.split('session_id=')[1].split(';')[0]
        return None

    def get_user_from_session(self):
        """세션ID → 사용자 정보 반환"""
        session_id = self.get_session_id()
        if session_id and session_id in SESSIONS:
            return SESSIONS[session_id]
        return None

    def require_login(self):
        """로그인 체크, 필요시 리다이렉트"""
        user = self.get_user_from_session()
        if not user:
            self.send_response(302)
            self.send_header('Location', '/login')
            self.end_headers()
            return False
        return user

    def send_html_response(self, status=200, body=""):
        """HTML 응답 공통 처리"""
        self.send_response(status)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(body.encode('utf-8'))

    def do_GET(self):
        parsed_url = urlparse(self.path).path
        
        if parsed_url == "/":
            body = """
                <h1>🏠 홈페이지</h1>
                <p><a href="/login">로그인</a> | <a href="/dashboard">대시보드</a></p>
            """
            self.send_html_response(200, body)
            
        elif parsed_url == "/login":
            # 로그인 페이지 (언제든 접근 가능)
            body = """
                <h1>🔐 로그인</h1>
                <form method="POST" action="/login">
                    <p>아이디: <input type="text" name="username" required></p>
                    <p>비밀번호: <input type="password" name="password" required></p>
                    <button type="submit">로그인</button>
                </form>
            """
            self.send_html_response(200, body)
            
        elif parsed_url == "/dashboard":
            # 로그인 체크
            user = self.require_login()
            if user:
                body = f"""
                    <h1>🎉 대시보드</h1>
                    <p>환영합니다, <b>{html.escape(user['username'])}</b>님!</p>
                    <p><a href="/logout">로그아웃</a></p>
                """
                self.send_html_response(200, body)
                
        else:
            self.send_html_response(404, "<h1>404 페이지 없음</h1>")

    def do_POST(self):
        parsed_url = urlparse(self.path).path
        
        if parsed_url == "/login":
            # 1. 폼 데이터 파싱
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = parse_qs(self.rfile.read(content_length).decode())
            
            username = post_data.get('username', [''])[0]
            password = post_data.get('password', [''])[0]
            
            # 2. 사용자 인증
            if (username in USERS and 
                USERS[username] == hashlib.sha256(password.encode()).hexdigest()):
                
                # 3. 세션 생성
                session_id = str(uuid.uuid4())
                SESSIONS[session_id] = {
                    'user_id': username,
                    'username': username
                }
                
                # 4. 쿠키 설정 + 리다이렉트
                self.send_response(302)
                self.send_header('Location', '/dashboard')
                self.send_header('Set-Cookie', f'session_id={session_id}; Path=/; HttpOnly')
                self.end_headers()
            else:
                # 5. 로그인 실패
                self.send_response(302)
                self.send_header('Location', '/login?error=1')
                self.end_headers()
                
        else:
            self.send_html_response(404, "<h1>404</h1>")

    def do_GET_logout(self):
        """로그아웃 처리"""
        session_id = self.get_session_id()
        if session_id:
            SESSIONS.pop(session_id, None)
        
        self.send_response(302)
        self.send_header('Location', '/login')
        # 쿠키 삭제 (Max-Age=0)
        self.send_header('Set-Cookie', 'session_id=; Path=/; Max-Age=0; HttpOnly')
        self.end_headers()

# 서버 실행
if __name__ == "__main__":
    server = HTTPServer(("localhost", PORT), LoginHandler)
    print(f"🚀 로그인 서버 시작: http://localhost:{PORT}")
    print("테스트 계정: test/1234, admin/admin")
    server.serve_forever()
