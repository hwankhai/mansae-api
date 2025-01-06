from mansae import MansaeAPI

def print_saju_info(saju_data):
    """사주 정보를 보기 좋게 출력"""
    print("\n[사주 정보]")
    print(f"년주: {saju_data['year']['ganji']} ({saju_data['year']['hganji']})")
    print(f"월주: {saju_data['month']['ganji']} ({saju_data['month']['hganji']})")
    print(f"일주: {saju_data['day']['ganji']} ({saju_data['day']['hganji']})")
    print(f"시주: {saju_data['hour']['ganji']} ({saju_data['hour']['hganji']})")

def get_valid_input(prompt: str, min_val: int, max_val: int) -> int:
    """사용자로부터 유효한 입력을 받음"""
    while True:
        try:
            value = int(input(prompt))
            if min_val <= value <= max_val:
                return value
            print(f"입력값은 {min_val}에서 {max_val} 사이여야 합니다.")
        except ValueError:
            print("올바른 숫자를 입력해주세요.")

def main():
    try:
        # API 인스턴스 생성
        api = MansaeAPI()
        
        # 사용자 입력 받기
        year = get_valid_input("년도를 입력하세요 (1900-2100): ", 1900, 2100)
        month = get_valid_input("월을 입력하세요 (1-12): ", 1, 12)
        day = get_valid_input("일을 입력하세요 (1-31): ", 1, 31)
        hour = get_valid_input("시를 입력하세요 (0-23): ", 0, 23)
        minute = get_valid_input("분을 입력하세요 (0-59): ", 0, 59)
        
        # 사주 계산
        print(f"\n{year}년 {month}월 {day}일 {hour}시 {minute}분의 사주")
        saju = api.get_saju(year, month, day, hour, minute)
        print_saju_info(saju)
        
    except ValueError as e:
        print(f"오류 발생: {e}")
    except Exception as e:
        print(f"예상치 못한 오류 발생: {e}")

if __name__ == "__main__":
    main() 