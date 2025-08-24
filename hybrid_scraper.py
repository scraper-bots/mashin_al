import asyncio
import aiohttp
import json
import pandas as pd
import logging
import time
from typing import List, Dict, Optional
from asyncio import Semaphore

# Import our working Selenium extractor for full phone numbers
from selenium_phone_extractor import SeleniumPhoneExtractor

class HybridMashinScraper:
    """
    Hybrid scraper that combines:
    1. Fast async API scraping for car listings
    2. Selenium-based phone extraction (full phone numbers via clicking)
    """
    
    def __init__(self, concurrent_requests: int = 10):
        self.base_url = "https://v2.mashin.al/api/v2"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8,ru;q=0.7,az;q=0.6",
            "Content-Type": "application/json",
            "Origin": "https://mashin.al",
            "Referer": "https://mashin.al/",
            "locale": "az",
            "breakpointm": "true",
            "DNT": "1",
        }
        
        self.semaphore = Semaphore(concurrent_requests)
        self.phone_extractor = SeleniumPhoneExtractor()
        
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    async def create_session(self) -> aiohttp.ClientSession:
        """Create aiohttp session"""
        timeout = aiohttp.ClientTimeout(total=30, connect=10)
        connector = aiohttp.TCPConnector(limit=50, limit_per_host=10)
        return aiohttp.ClientSession(
            headers=self.headers,
            timeout=timeout,
            connector=connector
        )

    async def get_car_listings_page(self, session: aiohttp.ClientSession, page: int) -> Optional[Dict]:
        """Fetch car listings page"""
        url = f"{self.base_url}/car"
        
        async with self.semaphore:
            try:
                async with session.post(url, json={}, params={"page": page}) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        self.logger.error(f"Failed to fetch page {page}: HTTP {response.status}")
                        return None
            except Exception as e:
                self.logger.error(f"Error fetching page {page}: {e}")
                return None

    async def scrape_all_listings(self, max_pages: Optional[int] = None) -> List[Dict]:
        """Scrape all car listings"""
        session = await self.create_session()
        try:
            # Get total pages
            first_page_data = await self.get_car_listings_page(session, 1)
            if not first_page_data:
                return []
            
            total_pages = first_page_data.get('meta', {}).get('total_pages', 1)
            if max_pages:
                total_pages = min(total_pages, max_pages)
            
            self.logger.info(f"🚗 Scraping {total_pages} pages...")
            
            # Create tasks for all pages
            page_tasks = [
                self.get_car_listings_page(session, page) 
                for page in range(1, total_pages + 1)
            ]
            
            # Fetch concurrently
            page_results = await asyncio.gather(*page_tasks, return_exceptions=True)
            
            # Collect cars
            all_cars = []
            for i, result in enumerate(page_results):
                if isinstance(result, dict) and 'data' in result:
                    cars = result['data']
                    all_cars.extend(cars)
                    self.logger.info(f"📄 Page {i+1}: {len(cars)} cars")
            
            self.logger.info(f"✅ Total cars: {len(all_cars)}")
            return all_cars
        finally:
            await session.close()

    async def extract_phone_numbers(self, cars: List[Dict]) -> List[Dict]:
        """Extract phone numbers using HTML method"""
        if not cars:
            return cars
        
        self.logger.info(f"📱 Extracting phone numbers for {len(cars)} cars...")
        
        # Get car IDs
        car_ids = [car.get('id_unique') for car in cars if car.get('id_unique')]
        
        # Extract phones using our working Selenium method
        phone_results = await self.phone_extractor.get_phone_numbers_batch(car_ids)
        
        # Assign to cars
        phones_found = 0
        for car in cars:
            car_id = car.get('id_unique')
            if car_id in phone_results:
                phone = phone_results[car_id]
                car['phone_number'] = phone
                if phone:
                    phones_found += 1
            else:
                car['phone_number'] = None
        
        self.logger.info(f"📞 Found {phones_found}/{len(cars)} phone numbers ({phones_found/len(cars)*100:.1f}% success)")
        return cars

    def flatten_car_data(self, cars: List[Dict]) -> List[Dict]:
        """Flatten car data for CSV"""
        flattened = []
        for car in cars:
            flat = {
                'id': car.get('id'),
                'id_unique': car.get('id_unique'),
                'brand': car.get('brand'),
                'model': car.get('model'),
                'price': car.get('price'),
                'year': car.get('year'),
                'mileage': car.get('mileage'),
                'capacity': car.get('car_catalog', {}).get('capacity') if car.get('car_catalog') else None,
                'created_at': car.get('created_at'),
                'credit': car.get('credit'),
                'tradeable': car.get('tradeable'),
                'image': car.get('image'),
                'original_image': car.get('original_image'),
                'region': car.get('region', {}).get('name') if car.get('region') else None,
                'phone_number': car.get('phone_number'),
                'is_auto_salon': car.get('is_auto_salon'),
                'has_360': car.get('has_360'),
                'show_vin': car.get('show_vin')
            }
            
            # Price conversions
            price_converted = car.get('price_converted', [])
            if len(price_converted) >= 1:
                flat['price_usd'] = price_converted[0]
            if len(price_converted) >= 2:
                flat['price_eur'] = price_converted[1]
            
            flattened.append(flat)
        
        return flattened

    async def save_data(self, cars: List[Dict], prefix: str = "hybrid_mashin"):
        """Save to both CSV and JSON"""
        if not cars:
            return
        
        csv_file = f"{prefix}_cars.csv"
        json_file = f"{prefix}_cars.json"
        
        # Save CSV
        flattened = self.flatten_car_data(cars)
        df = pd.DataFrame(flattened)
        await asyncio.get_event_loop().run_in_executor(
            None, lambda: df.to_csv(csv_file, index=False, encoding='utf-8')
        )
        
        # Save JSON
        def write_json():
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(cars, f, ensure_ascii=False, indent=2)
        
        await asyncio.get_event_loop().run_in_executor(None, write_json)
        
        self.logger.info(f"💾 Saved: {csv_file} & {json_file}")

    async def scrape_complete(self, max_pages: Optional[int] = None):
        """Main scraping method"""
        start_time = time.time()
        
        self.logger.info("🚀 Starting Hybrid Mashin.al Scraper!")
        
        # Step 1: Get car listings
        cars = await self.scrape_all_listings(max_pages)
        if not cars:
            self.logger.error("❌ No cars found!")
            return
        
        # Step 2: Get phone numbers 
        cars_with_phones = await self.extract_phone_numbers(cars)
        
        # Step 3: Save data
        await self.save_data(cars_with_phones)
        
        # Statistics
        total_time = time.time() - start_time
        phones_found = sum(1 for car in cars_with_phones if car.get('phone_number'))
        
        self.logger.info(f"""
🎉 HYBRID SCRAPING COMPLETED!

📊 Statistics:
   • Total cars: {len(cars_with_phones)}
   • Phone numbers: {phones_found}
   • Success rate: {phones_found/len(cars_with_phones)*100:.1f}%
   • Total time: {total_time:.1f}s
   
📱 Phone format: Full phone numbers via Selenium clicking
📁 Files: hybrid_mashin_cars.csv & hybrid_mashin_cars.json
        """)

async def main():
    """Run the hybrid scraper"""
    scraper = HybridMashinScraper(concurrent_requests=10)
    
    # Scrape all pages
    await scraper.scrape_complete()

if __name__ == "__main__":
    asyncio.run(main())