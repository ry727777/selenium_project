from selenium import webdriver

def check_login():
    driver = webdriver.Chrome()
    driver.get("https://demoqa.com/login")
    
    title = driver.title
    
    print("Title " + title)
    
    driver.quit()

if __name__ == "__main__":
    check_login()