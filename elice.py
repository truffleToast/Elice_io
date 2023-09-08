import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

# 파일 경로를 raw 문자열로 작성하고 백슬래시를 이스케이프 문자로 처리
## 자기 파일 절대경로 지정
# json 파일에 자기 아이디랑 비밀번호로 변경

# 파일 열기
with open('../My_Json.json', 'r' ) as f:
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

    # 로그인
    id_input = driver.find_element(By.NAME, "loginId")
    pw_input = driver.find_element(By.NAME, "password")
    id_input.send_keys(My_id)
    pw_input.send_keys(My_pw)
    pw_input.send_keys(Keys.ENTER)

    # 출석 버튼이 나타날 때까지 기다림
    try:
        chulsuk_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".MuiBox-root.css-8atqhb"))
        )
        chulsuk_button.click()
    except TimeoutException:
        print("출석 버튼이 발견되지 않았습니다.")

finally:
    # WebDriver 종료
    driver.quit()
    print("잘 됫습니다.")
