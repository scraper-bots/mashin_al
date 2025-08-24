import asyncio
import time
import re
import logging
from typing import Optional, Dict, List
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from concurrent.futures import ThreadPoolExecutor
import threading

class SeleniumPhoneExtractor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.max_workers = 3  # Limit concurrent browsers
        
    def create_driver(self) -> webdriver.Chrome:
        """Create Chrome WebDriver with stealth options"""
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Stealth options
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Add randomization
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        
        try:
            driver = webdriver.Chrome(options=chrome_options)
            # Remove webdriver property
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            return driver
        except Exception as e:
            self.logger.error(f"Failed to create Chrome driver: {e}")
            raise

    def extract_full_phone_sync(self, car_id: str) -> Optional[str]:
        """Extract full phone number using Selenium with enhanced debugging"""
        url = f"https://mashin.al/masinlar/elan/{car_id}"
        driver = None
        
        try:
            driver = self.create_driver()
            self.logger.info(f"🔍 Loading page for car {car_id}: {url}")
            
            # Load the page
            driver.get(url)
            
            # Wait for page to load
            time.sleep(3)
            
            # Debug: Log current page title
            page_title = driver.title
            self.logger.info(f"📄 Page title: {page_title}")
            
            # Look for different possible phone button selectors
            button_selectors = [
                "//button[contains(text(), 'Nömrəni göstər')]",
                "//button[contains(text(), '+994')]",
                "//button[contains(@class, 'phone')]",
                "//a[contains(text(), 'Nömrəni göstər')]",
                "//div[contains(text(), 'Nömrəni göstər')]",
                "//span[contains(text(), 'Nömrəni göstər')]",
                "//button[contains(text(), 'Zəng et')]",
            ]
            
            phone_button = None
            used_selector = None
            
            # Try to find the phone button
            for selector in button_selectors:
                try:
                    elements = driver.find_elements(By.XPATH, selector)
                    if elements:
                        phone_button = elements[0]
                        used_selector = selector
                        self.logger.info(f"✅ Found phone button with selector: {selector}")
                        break
                except Exception as e:
                    continue
            
            if not phone_button:
                self.logger.warning(f"❌ No phone button found for car {car_id}")
                # Debug: Print page source snippet
                page_source = driver.page_source[:2000]
                self.logger.debug(f"Page source snippet: {page_source}")
                return None
            
            # Log button text before clicking
            button_text_before = phone_button.text
            self.logger.info(f"📱 Button text before click: '{button_text_before}'")
            
            # Click the button
            try:
                driver.execute_script("arguments[0].click();", phone_button)
                self.logger.info(f"🖱️ Clicked phone button for car {car_id}")
            except Exception as e:
                self.logger.error(f"Failed to click button: {e}")
                # Try regular click as fallback
                phone_button.click()
            
            # Wait for phone number to appear with multiple strategies
            phone_number = None
            
            # Strategy 1: Wait and check button text change
            for attempt in range(10):  # Try for 5 seconds
                time.sleep(0.5)
                
                try:
                    # Re-find the button (it might have changed)
                    current_elements = driver.find_elements(By.XPATH, used_selector)
                    if current_elements:
                        current_button = current_elements[0]
                        current_text = current_button.text
                        
                        self.logger.info(f"🔄 Attempt {attempt + 1} - Button text: '{current_text}'")
                        
                        # Look for phone patterns in button text
                        phone_patterns = [
                            r'\+994\s*\(\d{2}\)\s*\d{3}[-\s]*\d{2}[-\s]*\d{2}',  # +994 (55) 320-15-50
                            r'\+994\s*\d{2}\s*\d{3}\s*\d{2}\s*\d{2}',            # +994 55 320 15 50
                            r'0\d{2}\s*\d{3}\s*\d{2}\s*\d{2}',                   # 055 320 15 50
                        ]
                        
                        for pattern in phone_patterns:
                            match = re.search(pattern, current_text)
                            if match:
                                phone_number = match.group()
                                self.logger.info(f"🎉 Found full phone in button: {phone_number}")
                                break
                        
                        if phone_number:
                            break
                            
                except Exception as e:
                    self.logger.error(f"Error checking button text: {e}")
                    continue
            
            # Strategy 2: Check entire page for phone numbers that appeared
            if not phone_number:
                self.logger.info("🔍 Searching entire page for phone numbers...")
                page_source = driver.page_source
                
                phone_patterns = [
                    r'\+994\s*\(\d{2}\)\s*\d{3}[-\s]*\d{2}[-\s]*\d{2}',  # +994 (55) 320-15-50
                    r'\+994\s*\d{2}\s*\d{3}\s*\d{2}\s*\d{2}',            # +994 55 320 15 50
                ]
                
                for pattern in phone_patterns:
                    matches = re.findall(pattern, page_source)
                    if matches:
                        phone_number = matches[0]
                        self.logger.info(f"🎉 Found full phone in page source: {phone_number}")
                        break
            
            # Strategy 3: Look for dynamically added elements
            if not phone_number:
                self.logger.info("🔍 Looking for dynamically added phone elements...")
                
                phone_element_selectors = [
                    "//span[contains(@class, 'phone')]",
                    "//div[contains(@class, 'phone')]",
                    "//a[contains(@href, 'tel:')]",
                    "//*[contains(text(), '+994')]",
                ]
                
                for selector in phone_element_selectors:
                    try:
                        elements = driver.find_elements(By.XPATH, selector)
                        for element in elements:
                            element_text = element.text or element.get_attribute('href') or ''
                            for pattern in [r'\+994\s*\(\d{2}\)\s*\d{3}[-\s]*\d{2}[-\s]*\d{2}', r'\+994\s*\d{2}\s*\d{3}\s*\d{2}\s*\d{2}']:
                                match = re.search(pattern, element_text)
                                if match:
                                    phone_number = match.group()
                                    self.logger.info(f"🎉 Found phone in element {selector}: {phone_number}")
                                    break
                            if phone_number:
                                break
                    except Exception as e:
                        continue
                    
                    if phone_number:
                        break
            
            return phone_number
            
        except Exception as e:
            self.logger.error(f"❌ Error extracting phone for car {car_id}: {e}")
            return None
            
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass

    async def get_phone_numbers_batch(self, car_ids: List[str]) -> Dict[str, Optional[str]]:
        """Extract phone numbers for multiple cars using ThreadPoolExecutor"""
        self.logger.info(f"📱 Starting batch phone extraction for {len(car_ids)} cars...")
        
        results = {}
        
        # Use ThreadPoolExecutor to run Selenium in threads
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Create tasks
            future_to_car_id = {
                executor.submit(self.extract_full_phone_sync, car_id): car_id
                for car_id in car_ids
            }
            
            # Process completed tasks
            for future in future_to_car_id:
                car_id = future_to_car_id[future]
                try:
                    phone_number = future.result(timeout=60)  # 60 second timeout per car
                    results[car_id] = phone_number
                    
                    if phone_number:
                        self.logger.info(f"✅ {car_id}: {phone_number}")
                    else:
                        self.logger.warning(f"❌ {car_id}: No phone found")
                        
                except Exception as e:
                    self.logger.error(f"❌ {car_id}: Exception - {e}")
                    results[car_id] = None
        
        # Statistics
        phones_found = sum(1 for phone in results.values() if phone)
        success_rate = phones_found / len(car_ids) * 100 if car_ids else 0
        
        self.logger.info(f"📊 Batch complete: {phones_found}/{len(car_ids)} phones found ({success_rate:.1f}% success)")
        
        return results

async def test_selenium_phone_extraction():
    """Test the Selenium phone extractor with debug output"""
    # Test with known car IDs
    test_car_ids = [
        "17502397950",  # Kia Rio
        "17506483310",  # Kia Sportage  
        "17506464510",  # Hyundai Santa Fe
    ]
    
    extractor = SeleniumPhoneExtractor()
    
    print("🚀 Testing Selenium phone extraction with enhanced debugging...")
    results = await extractor.get_phone_numbers_batch(test_car_ids)
    
    print(f"\n📱 Results:")
    for car_id, phone in results.items():
        status = "✅" if phone else "❌"
        print(f"  {status} {car_id}: {phone if phone else 'No phone found'}")
    
    return results

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    asyncio.run(test_selenium_phone_extraction())