import time
import json
#from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class InstagramBot:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--window-size=930,820")
        # chrome_options.add_argument("--start-maximized")  # Maximize the Chrome window
        # Use webdriver_manager to automatically download and manage the ChromeDriver
        # add undetected_chromedriver here 
        self.driver = uc.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def login(self, email, password):
        # Open Instagram
        self.driver.get("https://www.instagram.com/")
        # Wait for the login elements to become available
        wait = WebDriverWait(self.driver, 10)
        email_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))

        # Find the login elements and enter email and password
        email_field.send_keys(email)
        password_field.send_keys(password)

        # Submit the login form
        password_field.send_keys(Keys.RETURN)

        # Wait for the login process to complete (you may need to adjust the delay based on your internet speed)
        time.sleep(5)  # Wait for 5 seconds (adjust as needed)

    def scrape_hashtag_posts(self, hashtag):
        # Open Instagram and navigate to the hashtag page
        self.driver.get(f"https://www.instagram.com/explore/tags/{hashtag}/")
        time.sleep(8)
        # Wait for the posts to load
        wait = WebDriverWait(self.driver, 10)
        # wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="mount_0_0_GQ"]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/article/div[2]/div')))
        most_recent = self.driver.find_element(By.XPATH, '//div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/article/div[2]/div')
        # Scrape the most recent posts from the hashtag
        posts = most_recent.find_elements(By.TAG_NAME, "a")

        links = []
        for post in posts:
            # Retrieve the href attribute value
            href = post.get_attribute("href")
            # Process each href as needed
            links.append(href)
        
        return links
    
    def scrape_usernames(self, links):
        usernames = []
        for link in links:
            self.driver.get(link)
            time.sleep(3)
            # Wait for the username element to load
            wait = WebDriverWait(self.driver, 10)
            username_element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[1]/header/div[2]/div[1]/div[1]/div/div/span/div/div/a')))
            # Extract the username text
            username = username_element.text
            usernames.append(username)
        
        # Remove duplicate usernames
        usernames = list(set(usernames))
        
        return usernames
    
    def send_dm(self, usernames, message, delay_time):
        # Go to the Instagram Direct Inbox
        self.driver.get("https://www.instagram.com/direct/inbox/")
        time.sleep(3)

        # Check if the notification pop-up is displayed
        notification_popup = self.driver.find_element(By.XPATH, '//div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]')
        if notification_popup.is_displayed():
            notification_popup.click()
            time.sleep(2)

       
        for username in usernames:
             # Click the 'New Message' button
            new_message_button = self.driver.find_element(By.XPATH, '//div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/div/div/div/div[1]/div/div[1]/div/div[1]/div[2]/div/div')
            new_message_button.click()
            time.sleep(2)

            # Wait for the recipient input field to become available
            wait = WebDriverWait(self.driver, 10)
            recipient_input = wait.until(EC.presence_of_element_located((By.XPATH, '//div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/div[2]/div[2]/input')))

            # Type each username and press Enter to add as a recipient
            recipient_input.send_keys(username)
            time.sleep(1)
            recipient_input.send_keys(Keys.ENTER)
            time.sleep(1)

            
            select_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div')))
            select_button.click()
            time.sleep(2)

            # Wait for the next button to become clickable
            next_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/div[4]/div')))

            # Click the Next button to proceed to the message input
            next_button.click()
            time.sleep(3)

            # Create an instance of ActionChains
            actions = ActionChains(self.driver)
            actions.send_keys(message)
            actions.send_keys(Keys.RETURN)
            # Perform the actions
            actions.perform()

            time.sleep(delay_time)
        
        self.driver.quit()


    def comment_on_posts(self, links, comment, delay_time):
        for link in links:
            # Open each post link
            self.driver.get(link)
            time.sleep(2)

            # Find the comment input field
            comment_input = self.driver.find_element(By.CSS_SELECTOR, 'textarea[aria-label="Add a comment…"]')
            comment_input.click()
            time.sleep(1)

            # Create an instance of ActionChains
            actions = ActionChains(self.driver)
            actions.send_keys(comment)
            actions.send_keys(Keys.RETURN)
            # Perform the actions
            actions.perform()

            time.sleep(delay_time)
        
        self.driver.quit()


