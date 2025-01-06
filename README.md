# Mansae API (만세력 API)

만세력(사주) 계산을 위한 Python API입니다.

## 프로젝트 소개

이 프로젝트는 [OOPS-ORG-PHP의 Lunar 프로젝트](https://github.com/OOPS-ORG-PHP/Lunar)를 Python으로 재구현하고, 여기에 만세력(사주) 계산 기능을 추가한 것입니다. 기존의 음력/양력 변환 알고리즘을 기반으로 하되, 현대적인 Python 개발 방식과 객체지향 설계 원칙을 적용하여 새롭게 작성되었습니다.

### 주요 특징
- 기존 PHP 코드의 Python 포팅
- 만세력(사주) 계산 기능 추가
- 현대적인 Python 패키지 구조 적용
- 타입 힌트와 상세한 문서화
- 포괄적인 테스트 커버리지

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