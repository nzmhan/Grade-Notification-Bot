import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def initialize(id, password, url):
    options = Options()
    options.add_argument('--headless=new') ## chrome sekmesini açmaz
    driver = webdriver.Chrome(options=options)

    driver.get(url)

    main_button = driver.find_elements(By.CSS_SELECTOR, 'a.btn.btn-default.btn-xs')[2]
    main_button.click()

    # filling login information, id-password
    driver.find_element(By.ID, 'tridField') .send_keys(id)
    driver.find_element(By.ID, 'egpField') .send_keys(password)

    # click button
    login_button = driver.find_element(By.CSS_SELECTOR, 'button[class="btn btn-send"]')
    login_button.click()

    time.sleep(2)
    
    return driver

def check(driver, prev_lessons):
    driver.refresh() # redundent on first
    time.sleep(3) 
    
    p_note_list = driver.find_element(By.XPATH, ".//p[normalize-space()='Not Listesi']")
    a_note_list = p_note_list.find_element(By.XPATH, ".//ancestor::a")
    driver.execute_script("arguments[0].click();", a_note_list)

    time.sleep(2) # not sayfası

    frame = driver.find_element(By.ID, "IFRAME1") # not tablosu frame
    driver.switch_to.frame(frame)

    time.sleep(1) # frame inner request için bekleme

    status = False

    course_table = driver.find_element(By.CSS_SELECTOR, 'table.grdStyle')
    grade_rows = course_table.find_elements(By.TAG_NAME, 'tr')[1:]
    changes = []
    lessons = []

    for row in grade_rows:
        columns = row.find_elements(By.XPATH, "./*")

        lesson = Lesson(columns[1].text, columns[2].text, columns[3].text, columns[4], columns[5].text, columns[6].text, columns[7].text)
        lessons.append(lesson)

        for prev in prev_lessons:
            change = prev.check_for_change(lesson)
            if change is not None:
                changes.append((lesson, change))
                status = True


    return status, lessons, changes

class Lesson:
    def __init__(self, code, name, status, exams_elem, median, note_xx, state):
        self.code = code
        self.name = name
        self.median = median
        self.note_xx = note_xx
        self.state = state
        self.exams = []

        spans = exams_elem.find_elements(By.TAG_NAME, 'span')
        for i in range(0, len(spans), 2):
            name = spans[i].text
            grade = spans[i + 1].text
            self.exams.append(Exam(name, grade))

    def check_for_change(self, compare):
        if compare.name != self.name:
            return None
        
        for exam in self.exams:
            target = next(filter(lambda x: x.name == exam.name, compare.exams), None)
            if target is not None and target.is_changed(exam): 
                return exam
            
        return None
    
    def __str__(self) -> str:
        return f'{self.name}[{self.code}]'

class Exam:
    def  __init__(self, name, grade):
        self.name = name
        self.grade = grade

    def is_changed(self, compare):
        self.grade != compare.grade

    def __str__(self) -> str:
        return f'{self.name}: {self.grade}'
