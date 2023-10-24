# -------------------------------------------------------------------------------------------------
# Imports
# -------------------------------------------------------------------------------------------------
import logging
import time
from datetime import datetime as dt
# import config as env
from general import GeneralUtil as gen_util
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
# level = logging.INFO
# fmt = "[%(levelname)s] %(asctime)s - %(message)s"
# logging.basicConfig(
#     filename=f'{env.ROOT_DIR}/log/{dt.now().strftime("%Y-%m-%d")} form-filling.log',
#     level=level,
#     format=fmt,
# )

import chromedriver_autoinstaller
from pyvirtualdisplay import Display
display = Display(visible=0, size=(800, 800))  
display.start()

chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
                                      # and if it doesn't exist, download it automatically,
                                      # then add chromedriver to path

chrome_options = Options()
chrome_options.add_argument("-incognito")
chrome_options.add_argument("--headless")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

logging.info("Running main.py\n")

today_ = dt.now().strftime("%B %d, %H:%M:%S")
# ids = ["210072", "210071", "210029", "210143"]
ids = ["210232"]
reference_name = "Minh"
# persons = {
    # 'chris': {
    #     'number': 9292649156,
    #     'carrier': 'cricket'
    # },
    # "makai": {"number": 5203096035, "carrier": "verizon"},
    # "rumi": {"number": 5203091772, "carrier": "verizon"},
# }
# persons  = {
    # 'minh': {
        # 'number': 8458200513, "carrier": "verizon"
    # }
# }

def main():
    def fill_form(student_id, reference_name):
        """Fill out x sheet

        Parameters
        ----------
        id : int
            student ID
        reference_name : str
            person for reference
        """
        logging.info(f"Filling out form for {student_id} with {reference_name} as reference")
        # Open URL
        chrome_options = webdriver.ChromeOptions()    
        # Add your options as needed    
        options = [
          # Define window size here
           "--window-size=1200,1200",
            "--ignore-certificate-errors"
         
            #"--headless",
            #"--disable-gpu",
            #"--window-size=1920,1200",
            #"--ignore-certificate-errors",
            #"--disable-extensions",
            #"--no-sandbox",
            #"--disable-dev-shm-usage",
            #'--remote-debugging-port=9222'
        ]
        
        for option in options:
            chrome_options.add_argument(option)
        
            
        driver = webdriver.Chrome(options = chrome_options)
        
        # driver.get("https://docs.google.com/forms/d/e/1FAIpQLSf7LSpENMM8nB_YBcDUqgUQFbYNrGwKyIUndz54Fp-U-8ZdwA/viewform?usp=sf_link") #clone
        driver.get("https://docs.google.com/forms/d/1sjD-62V_m5B6PAf28PiX7K17U8XNyo8vGAjbtiRZ9oI") #real

        # wait for one second, until page gets fully loaded
        time.sleep(3)

        # Select input box
        textbox = driver.find_elements(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
        for box in textbox:
            box.send_keys(student_id)
        
        # Which attendance: 1-hour group study
        attendance = driver.find_element(By.XPATH, "(//div[@role='radio']//div)[3]") #official form
        # attendance = driver.find_element(By.XPATH, "(//div[@class='vd3tt']//div)[1]") #clone form
        attendance.click()
        
        # Room of attendance: D430
        duration = driver.find_element(By.XPATH, "//div[@id='i34']/div[3]/div[1]") #official form
        # duration = driver.find_element(By.XPATH, "//div[@id='i34']/div[3]/div[1]") #clone form
        duration.click()
        
        # Click on submit button
        submit = driver.find_element(By.XPATH, "//span[contains(text(),'Submit')]") #official form
        submit.click()

        # close the window
        logging.info("Successfully submitted form\n")
        driver.close()
        driver.quit()

    for id in ids:
        fill_form(id, reference_name)

    msg_out = f"Successfully Filled Google Form.\n{today_}"
    print(msg_out)
    # gen_util.send_sms(env.SMS["SENDER"], env.SMS["PASSWORD"], persons, msg=msg_out)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        msg_out = f"Error occured autofilling Google Form. Check with Minh for details.\n{today_}"
        print(msg_out)
        print(e)
        # gen_util.send_sms(env.SMS["SENDER"], env.SMS["PASSWORD"], persons, msg=msg_out)
        # logging.error(f"Error: {e}")
