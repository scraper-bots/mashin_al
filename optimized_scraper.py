import asyncio
import aiohttp
import json
import pandas as pd
import logging
import time
from typing import List, Dict, Optional
from asyncio import Semaphore
import signal
import sys

# Import our working Selenium extractor for full phone numbers
from selenium_phone_extractor import SeleniumPhoneExtractor

class OptimizedMashinScraper:
    """
    Optimized scraper with better progress tracking and controls
    """
    
    def __init__(self, concurrent_requests: int = 10, max_workers: int = 5):
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
        self.phone_extractor.max_workers = max_workers  # More workers for faster phone extraction
        
        # Progress tracking
        self.total_cars_processed = 0
        self.total_phones_found = 0
        self.start_time = None
        self.should_stop = False
        
        # Setup graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def signal_handler(self, signum, frame):
        """Handle graceful shutdown"""
        self.logger.info(f"🛑 Received signal {signum}. Gracefully shutting down...")
        self.should_stop = True

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
        """Scrape all car listings with progress tracking"""
        session = await self.create_session()
        try:
            # Get total pages
            first_page_data = await self.get_car_listings_page(session, 1)
            if not first_page_data:
                return []
            
            total_pages = first_page_data.get('meta', {}).get('total_pages', 1)
            if max_pages:
                total_pages = min(total_pages, max_pages)
            
            self.logger.info(f"🚗 Scraping {total_pages} pages (~{total_pages * 20} cars)...")
            
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
                    if (i + 1) % 100 == 0:  # Log every 100 pages
                        self.logger.info(f"📄 Processed {i+1}/{total_pages} pages ({len(all_cars)} cars so far)")
            
            self.logger.info(f"✅ Total cars: {len(all_cars)}")
            return all_cars
        finally:
            await session.close()

    async def extract_phone_numbers_batch(self, cars: List[Dict], batch_size: int = 50) -> List[Dict]:
        """Extract phone numbers in smaller batches with progress tracking"""
        if not cars:
            return cars
        
        self.logger.info(f"📱 Starting phone extraction for {len(cars)} cars (batch size: {batch_size})...")
        
        # Process in batches to avoid overwhelming and provide progress updates
        for batch_start in range(0, len(cars), batch_size):
            if self.should_stop:
                self.logger.info("🛑 Stopping due to signal...")
                break
                
            batch_end = min(batch_start + batch_size, len(cars))
            batch_cars = cars[batch_start:batch_end]
            
            # Get car IDs for this batch
            car_ids = [car.get('id_unique') for car in batch_cars if car.get('id_unique')]
            
            self.logger.info(f"🔄 Processing batch {batch_start//batch_size + 1}/{(len(cars)-1)//batch_size + 1} ({len(car_ids)} cars)")
            
            # Extract phones for this batch
            phone_results = await self.phone_extractor.get_phone_numbers_batch(car_ids)
            
            # Assign to cars
            batch_phones_found = 0
            for car in batch_cars:
                car_id = car.get('id_unique')
                if car_id in phone_results:
                    phone = phone_results[car_id]
                    car['phone_number'] = phone
                    if phone:
                        batch_phones_found += 1
                else:
                    car['phone_number'] = None
            
            # Update progress
            self.total_cars_processed += len(batch_cars)
            self.total_phones_found += batch_phones_found
            
            # Calculate progress stats
            elapsed_time = time.time() - self.start_time if self.start_time else 0
            cars_per_minute = (self.total_cars_processed / elapsed_time * 60) if elapsed_time > 0 else 0
            eta_minutes = ((len(cars) - self.total_cars_processed) / cars_per_minute) if cars_per_minute > 0 else 0
            
            self.logger.info(f"""
📊 PROGRESS UPDATE:
   • Processed: {self.total_cars_processed}/{len(cars)} cars ({self.total_cars_processed/len(cars)*100:.1f}%)
   • Phones found: {self.total_phones_found} ({self.total_phones_found/self.total_cars_processed*100:.1f}% success)
   • Speed: {cars_per_minute:.1f} cars/minute
   • Elapsed: {elapsed_time/60:.1f} minutes
   • ETA: {eta_minutes:.1f} minutes remaining
            """)
            
            # Save intermediate progress every 5 batches
            if (batch_start // batch_size + 1) % 5 == 0:
                await self.save_intermediate_progress(cars[:batch_end])
        
        return cars

    async def save_intermediate_progress(self, cars: List[Dict]):
        """Save intermediate progress"""
        try:
            csv_file = "hybrid_mashin_cars_progress.csv"
            json_file = "hybrid_mashin_cars_progress.json"
            
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
            
            self.logger.info(f"💾 Saved intermediate progress: {csv_file} & {json_file}")
        except Exception as e:
            self.logger.error(f"Failed to save intermediate progress: {e}")

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

    async def save_data(self, cars: List[Dict], prefix: str = "optimized_mashin"):
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

    async def scrape_complete(self, max_pages: Optional[int] = None, batch_size: int = 50):
        """Main scraping method with better progress tracking"""
        self.start_time = time.time()
        
        self.logger.info("🚀 Starting Optimized Mashin.al Scraper!")
        
        # Step 1: Get car listings
        cars = await self.scrape_all_listings(max_pages)
        if not cars:
            self.logger.error("❌ No cars found!")
            return
        
        # Step 2: Get phone numbers in batches
        cars_with_phones = await self.extract_phone_numbers_batch(cars, batch_size)
        
        if self.should_stop:
            self.logger.info("🛑 Scraping stopped by user. Saving partial results...")
        
        # Step 3: Save final data
        await self.save_data(cars_with_phones)
        
        # Statistics
        total_time = time.time() - self.start_time
        phones_found = sum(1 for car in cars_with_phones if car.get('phone_number'))
        
        self.logger.info(f"""
🎉 OPTIMIZED SCRAPING COMPLETED!

📊 Final Statistics:
   • Total cars: {len(cars_with_phones)}
   • Phone numbers: {phones_found}
   • Success rate: {phones_found/len(cars_with_phones)*100:.1f}%
   • Total time: {total_time/60:.1f} minutes
   • Speed: {len(cars_with_phones)/(total_time/60):.1f} cars/minute
   
📱 Phone format: Full phone numbers via Selenium clicking
📁 Files: optimized_mashin_cars.csv & optimized_mashin_cars.json
        """)

async def main():
    """Run the optimized scraper"""
    # More workers and better batching for faster processing
    scraper = OptimizedMashinScraper(concurrent_requests=15, max_workers=5)
    
    # Full scraping - all pages
    await scraper.scrape_complete(max_pages=None, batch_size=30)  # 30 car batches

if __name__ == "__main__":
    asyncio.run(main())