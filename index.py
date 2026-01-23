from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

# 요청을 처리할 핸들러 클래스
class MyVanillaHandler(BaseHTTPRequestHandler):
    
    # [보안 검증 함수] - 중복 코드를 방지하기 위해 별도로 만듭니다.
    def check_auth(self):
        # 게임사에서 약속한 특수 키가 헤더에 있는지 확인 (가상의 키: secret-token-123)
        api_key = self.headers.get('X-Game-Auth')
        return api_key == 'secret-token-123'

    # 브라우저 접속(GET 요청) 처리
    def do_GET(self):
        # 1. 보안 검사 실시
        if not self.check_auth():
            self.send_response(403) # 거부(Forbidden)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write("<h1>접근 권한이 없습니다! ⛔</h1><p>보안 헤더가 누락되었습니다.</p>".encode('utf-8'))
            return

        # 2. 통과 시 정상 응답 처리
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        # 현재 서버 시간 계산
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 로그 출력
        print(f"[{self.date_time_string()}] 인증 성공! 주소: {self.path}")

        if self.path == '/':
            message = f"""
            <html>
                <body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
                    <h1>동적 페이지 테스트 🚀</h1>
                    <p style="font-size: 1.2em;">현재 서버 시간: <b style="color: blue;">{now}</b></p>
                    <p>인증에 성공하여 서버 데이터를 열람 중입니다.</p>
                </body>
            </html>
            """
        else:
            message = "<h1>404 Not Found</h1>"

        self.wfile.write(message.encode('utf-8'))

    # 게임사 콜백(POST 요청) 처리 예시
    def do_POST(self):
        print("--- [수신된 헤더 정보] ---")
        print(self.headers)
        print("------------------------")
        
        if self.check_auth():
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        else:
            self.send_response(403)
            self.end_headers()

# 서버 설정 및 실행
port = 8000
server_address = ('localhost', port)
httpd = HTTPServer(server_address, MyVanillaHandler)

print(f"서버가 준비되었습니다! http://localhost:{port}")
httpd.serve_forever()