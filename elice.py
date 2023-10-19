from apscheduler.schedulers.background import BackgroundScheduler
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from datetime import datetime

# 파일 경로를 raw 문자열로 작성하고 백슬래시를 이스케이프 문자로 처리
# 자신의 파일 상대경로로 지정
# json 파일에 자신의 아이디와 비밀번호로 변경

def schedulerJob():
    with open('./My_Json.json', 'r') as f:
        json_data = json.load(f)

# JSON 데이터에서 필요한 값을 추출
    My_id = json_data['elice']['id']
    My_pw = json_data['elice']['pw']


    # WebDriver 초기화
    driver = webdriver.Chrome()

    try:
        driver.get("https://2023-gj-aischool.elice.io/my")

        # 로그인 버튼이 나타날 때까지 기다림
        try:
            login_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#mui-3"))
            )
            login_button.click()
        except TimeoutException:
            print("로그인 버튼이 발견되지 않았습니다.")
            driver.quit()
            

        # 로그인
        id_input = driver.find_element(By.NAME, "loginId")
        pw_input = driver.find_element(By.NAME, "password")
        id_input.send_keys(My_id)
        pw_input.send_keys(My_pw)
        pw_input.send_keys(Keys.ENTER)
        print("로그인 완료")
        time.sleep(3)

        my_lecture = driver.find_element(By.CSS_SELECTOR, ".buttoncss-1rc2wrl")
        time.sleep(2)
        my_lecture = my_lecture.text
        print(my_lecture)
        if my_lecture != "Spring" : #spring이 아니면 종료
            driver.quit()
        print("출석 버튼이 나타날 때까지 기다림")

        #시간에 따라 출석하기 버튼이 있는 선택자 찾기
        current_hour = datetime.now().hour
        if current_hour<10: # 10시 이전이라면
            button_text = "출석하기"
            print(f'지금 시간은 {button_text} 시간입니다.')
            
        elif current_hour >= 17:
            button_text = "퇴실하기"
            print(f'지금 시간은 {button_text} 시간입니다.')
            
        
        try:
            attendance_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//button[contains(text(), '{button_text}')]"))  
                # F-String으로 button-text가 들어가 있는 버튼을 찾기
            )
            attendance_button.click()
        except TimeoutException:
            print("출석 버튼이 발견되지 않았습니다.")
            driver.quit()

    finally:
        # WebDriver 종료
        time.sleep(3)
        driver.quit()
        print("작업이 끝났습니다.")

    # 파일 열기
    # 백그라운드 스케줄러 사용 함수 필요 daemon?
def backgroundScheduler():
    scheduler =BackgroundScheduler(daemon =True)
    scheduler.start()
    # 올바른 방법
    scheduler.add_job(schedulerJob, 'cron', day_of_week='mon-fri', hour=17, minute=50)
    scheduler.add_job(schedulerJob, 'cron', day_of_week='mon-fri', hour=8, minute=50)
if __name__ == '__main__':
    backgroundScheduler()


    