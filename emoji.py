import json

data = {"name": "김철수", "emoji": "😀"}

print(json.dumps(data))

# 기본 (한글 깨짐)
print(json.dumps(data))
# {"name": "\uae40\ucca0\uc218", ...}

# ensure_ascii=False (한글 유지)
print(json.dumps(data, ensure_ascii=False))
# {"name": "김철수", "emoji": "😀"}

