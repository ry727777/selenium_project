import pytest
import random
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains


# ✅ Fixture defined at the top level
@pytest.fixture(autouse=True)
def setup_driver(request):
    driver = webdriver.Chrome()
    request.cls.driver = driver
    yield
    driver.quit()

@pytest.mark.usefixtures("setup_driver")
class TestLogin:

    @pytest.mark.test1
    def test_user_creation(self):
        self.driver.get("https://demoqa.com/login")
        assert "DEMOQA" in self.driver.title

        username = "automation"
        password = "Automation@123"

        self.driver.find_element(By.ID, "userName").send_keys(username)
        self.driver.find_element(By.ID, "password").send_keys(password)

        # Handle potential overlays
        try:
            self.driver.find_element(By.ID, "close-fixedban").click()
        except:
            pass  # overlay not found

        login_btn = self.driver.find_element(By.ID, "login")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", login_btn)

        # Wait and click the login button
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable((By.ID, "login"))).click()
    
    @pytest.mark.drag_and_drop
    @pytest.mark.regression
    def test_drag_and_drop(self):
        self.driver.get("https://the-internet.herokuapp.com/drag_and_drop")
        assert "The Internet" == self.driver.title
        
        source = self.driver.find_element(By.ID, "column-a")
        destination = self.driver.find_element(By.ID, "column-b")
        
        action = ActionChains(self.driver)
        action.drag_and_drop(source,destination).perform
    
    @pytest.mark.check_box
    @pytest.mark.regression
    def test_check_box(self):
        self.driver.get("https://the-internet.herokuapp.com/checkboxes")
        assert "The Internet" == self.driver.title
        
        try:
            tmp = self.driver.find_element(By.XPATH,'//h3[text()="Checkboxes"]/following-sibling::form//input[@type="checkbox"][1]').is_selected()
            if not tmp:
                self.driver.find_element(By.XPATH,'//h3[text()="Checkboxes"]/following-sibling::form//input[@type="checkbox"][1]').click()
        except:
            print("error")
            
    @pytest.mark.drop_down
    @pytest.mark.regression
    def test_drop_down(self):
        self.driver.get("https://the-internet.herokuapp.com/dropdown")
        assert "The Internet" == self.driver.title
        
        self.driver.find_element(By.ID,'dropdown').click()
        WebDriverWait(self.driver,20)
        self.driver.find_element(By.XPATH,'//option[text()="Option 1"]').click()
        
    @pytest.mark.scroll
    @pytest.mark.regression
    def test_scroll(self):
        self.driver.get("https://the-internet.herokuapp.com/floating_menu")
        assert "The Internet" == self.driver.title
        
        assert self.driver.find_element(By.XPATH,"//a[text()='Home']").is_displayed()
        
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        assert self.driver.find_element(By.XPATH,"//a[text()='Home']").is_displayed()
        
    @pytest.mark.hover
    @pytest.mark.regression
    def test_hover(self):
        self.driver.get("https://the-internet.herokuapp.com/hovers")
        assert "The Internet" == self.driver.title
        figure = self.driver.find_element(By.XPATH, '//div[@class="figure"][1]')
        action = ActionChains(self.driver)
        action.move_to_element(figure).perform()
        temp = self.driver.find_element(By.XPATH, "//img/following-sibling::div//h5[text()='name: user1']").is_displayed()
        assert temp
        
    @pytest.mark.redirect
    @pytest.mark.regression
    def test_redirect(self):
        self.driver.get("https://the-internet.herokuapp.com/redirector")

        # Confirm you're on the redirector page
        assert "The Internet" in self.driver.title

        # Click the "Here" link
        self.driver.find_element(By.LINK_TEXT, "here").click()

        # Wait for the redirect to complete (basic sleep or WebDriverWait)
        self.driver.implicitly_wait(5)

        # Verify redirected URL
        current_url = self.driver.current_url
        print("Redirected to:", current_url)
    
    @pytest.mark.regression
    @pytest.mark.upload
    def test_file_upload(self):
        # Step 1: Load the upload page
        self.driver.get("https://the-internet.herokuapp.com/upload")
        assert "The Internet" in self.driver.title

        # Step 2: Build absolute path to the file
        file_name = "images.png"
        file_path = os.path.abspath(file_name)

        # Step 3: Verify file exists before upload
        assert os.path.exists(file_path), f"❌ File not found: {file_path}"

        # Step 4: Upload the file using input[type="file"]
        upload_input = self.driver.find_element(By.ID, "file-upload")
        upload_input.send_keys(file_path)

        # Step 5: Click the upload button
        self.driver.find_element(By.ID, "file-submit").click()

        # Step 6: Wait until the uploaded file name appears
        uploaded_file = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "uploaded-files"))
        )

        # Step 7: Assert uploaded file name is correct
        assert uploaded_file.text == file_name, f"❌ Upload failed. Expected: {file_name}, Got: {uploaded_file.text}"

        print(f"✅ File '{file_name}' uploaded successfully.")
            
            