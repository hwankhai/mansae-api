# Mansae API (만세력 API)

만세력(사주) 계산을 위한 Python API입니다.

## 설치

다음 두 가지 방법 중 하나로 설치할 수 있습니다:

1. GitHub에서 직접 설치:
```bash
pip install git+https://github.com/hwankhai/mansae-api.git
```

2. 소스코드에서 직접 설치:
```bash
git clone https://github.com/hwankhai/mansae-api.git
cd mansae-api
pip install -e .
```

## 사용법

```python
from mansae import MansaeAPI

# API 인스턴스 생성
api = MansaeAPI()

# 양력 날짜로 사주 계산
saju = api.get_saju(2024, 1, 6, 12, 30)
print("\n[사주 정보]")
print(f"년주: {saju['year']['ganji']} ({saju['year']['hganji']})")
print(f"월주: {saju['month']['ganji']} ({saju['month']['hganji']})")
print(f"일주: {saju['day']['ganji']} ({saju['day']['hganji']})")
print(f"시주: {saju['hour']['ganji']} ({saju['hour']['hganji']})")
```

## 기능

1. 양력 날짜 기준 사주 계산
   - 년주, 월주, 일주, 시주 계산
   - 한글과 한자 간지 지원

## 반환 데이터 형식

```python
{
    'year': {
        'gan': '갑',      # 천간
        'ji': '자',       # 지지
        'ganji': '갑자',  # 간지
        'hganji': '甲子'  # 한자 간지
    },
    'month': { ... },
    'day': { ... },
    'hour': { ... }
}
```

## 요구사항

- Python >= 3.7
- NumPy >= 1.21.0
- Windows 사용자의 경우 tzdata 패키지가 자동으로 설치됩니다.

## 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.

## 저자

- hwankhai (https://github.com/hwankhai)

## 기여

이슈나 풀 리퀘스트는 GitHub를 통해 제출해주세요: https://github.com/hwankhai/mansae-api 