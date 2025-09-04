import json
from datetime import datetime
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
import base64

# ✅ 1. data 객체 생성
data = {
    "data": {
        "578ec5138b805d44d3d3b360a2874eb26e134468086f969c25e1c38c2b88eba2":{
            "user": "전찬호_SUB_PC",
            "expire": "9999-01-01"
        }
    }
}


# ✅ 2. JSON 구조 만들기 (data만 먼저 넣기)
output = {
    "data": data
}

# ✅ 3. 서명 대상 문자열 만들기 (data만 정렬된 JSON으로 인코딩)
data_json = json.dumps(data, separators=(',', ':'), sort_keys=True, ensure_ascii=False).encode("utf-8")

# ✅ 4. 개인 키 로딩
with open("my_private_key.pem", "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None
    )

# ✅ 5. RSA 서명 생성
signature = private_key.sign(
    data_json,
    padding.PKCS1v15(),
    hashes.SHA256()
)

# ✅ 6. base64 인코딩된 서명 추가
output["signature"] = base64.b64encode(signature).decode("utf-8")

# ✅ 7. JSON 저장
with open("slots_signed.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print("✅ 'slots_signed.json' 파일이 생성되고 서명되었습니다.")
