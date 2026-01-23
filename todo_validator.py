from jsonschema import validate, ValidationError

# 스키마 정의
todo_schema = {
    "type": "object",
    "properties": {
        "title": {
            "type": "string",
            "minLength": 1,
            "maxLength": 100
        },
        "done": {
            "type": "boolean"
        }
    },
    "required": ["title"]
}

# 검증
data = {"title": "공부하기", "done": False}

try:
    validate(instance=data, schema=todo_schema)
    print("✅ 검증 성공")
except ValidationError as e:
    print(f"❌ 검증 실패: {e.message}")
