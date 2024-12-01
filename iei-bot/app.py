from time import sleep
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from fastapi import FastAPI, HTTPException

app = FastAPI()

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--window-size=2560,1440")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        print(f"Chrome driver initialization error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to initialize Chrome driver: {str(e)}"
        )

@app.get("/utm-to-lat-long/{utm_north}/{utm_east}")
async def utm_to_lat_long(utm_north: float, utm_east: float):
    driver = None
    try:
        driver = setup_driver()
        print("Driver initialized")

        driver.get("https://www.ign.es/web/calculadora-geodesica")
        print("Navigated to the calculator page")
        
        # Wait for and click the UTM button
        wait = WebDriverWait(driver, 10)
        print("Finished waiting for website to load")

        utm_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[3]/div/div/div/div/div/div/div/div/div[1]/fieldset[1]/div[2]/fieldset[2]/div[2]/label"))
        )
        print("UTM button found")

        utm_button.click()
        print("UTM button clicked")
        
        # Wait for and fill in the UTM coordinates
        north_input = wait.until(
            EC.presence_of_element_located((By.ID, "datacoord1"))
        )
        east_input = wait.until(
            EC.presence_of_element_located((By.ID, "datacoord2"))
        )

        print("Input fields found")
        
        # Clear and fill the input fields
        north_input.clear()
        north_input.send_keys(str(utm_north))
        east_input.clear()
        east_input.send_keys(str(utm_east))

        print("Input fields filled")

        cookie_button = wait.until(
            EC.element_to_be_clickable((By.ID, "acepto_galleta"))
        )
        cookie_button.click()
        print("Cookie button clicked")

        # Click calculate button
        calculate_button = wait.until(
            EC.element_to_be_clickable((By.ID, "trd_calc"))
        )
        calculate_button.click()
        print("Calculate button clicked")

        wait.until(
            lambda driver: driver.find_element(By.ID, "txt_etrs89_latgd").get_attribute("value") != ""
        )
        print("Results loaded")
        
        # Wait for and get the results
        latitude = wait.until(
            EC.presence_of_element_located((By.ID, "txt_etrs89_latgd"))
        ).get_attribute("value")
        print("latitude: ", latitude)
        
        longitude = wait.until(
            EC.presence_of_element_located((By.ID, "txt_etrs89_longd"))
        ).get_attribute("value")
        print("longitude: ", longitude)

        print("Results found")
        
        return {
            "latitude": latitude,
            "longitude": longitude
        }
        
    except Exception as e:
        print(f"Error during UTM to latitude/longitude conversion: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to convert UTM to latitude/longitude: {str(e)}"
        )
    finally:
        if driver:
            driver.quit()
