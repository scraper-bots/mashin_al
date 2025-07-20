# NumberAggregator: Advanced Data Collection & Aggregation System 🔢📊

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-4.9+-green.svg)
![Selenium](https://img.shields.io/badge/Selenium-4.0+-orange.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-teal.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Data](https://img.shields.io/badge/Data-Aggregation-purple.svg)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)

A powerful, scalable system for scraping numerical data from APIs and websites, processing it intelligently, and aggregating results into structured formats. This tool automates the collection of numerical insights from diverse sources with robust error handling, scheduling, and monitoring capabilities.

## 🎯 Project Overview

NumberAggregator is a comprehensive data collection and aggregation platform that:
- **Scrapes** numerical data from websites using advanced parsing techniques
- **Integrates** with multiple APIs for real-time data collection
- **Extracts** numbers, metrics, and statistics from various sources
- **Aggregates** data using sophisticated algorithms and patterns
- **Transforms** raw data into structured formats (JSON, CSV, XML)
- **Deploys** on cloud infrastructure for continuous operation
- **Monitors** data quality and collection performance

### 🌟 Key Features

- **Multi-Source Data Collection**: Web scraping, REST APIs, GraphQL, RSS feeds
- **Intelligent Number Extraction**: Pattern recognition, context-aware parsing
- **Real-Time Processing**: Stream processing and batch aggregation
- **Data Quality Assurance**: Validation, cleaning, and anomaly detection
- **Flexible Output Formats**: JSON, CSV, XML, Parquet, SQL databases
- **Scalable Architecture**: Docker, Kubernetes, cloud-native deployment
- **Comprehensive Monitoring**: Metrics, alerts, and performance dashboards
- **Robust Error Handling**: Retry mechanisms, failover strategies

## 🏗️ System Architecture

```mermaid
graph TB
    A[Data Sources] --> B[Collection Layer]
    B --> C[Processing Engine]
    C --> D[Aggregation Service]
    D --> E[Storage Layer]
    E --> F[Output Services]
    F --> G[Monitoring & Alerts]
    
    subgraph "Data Sources"
        A --> A1[Websites]
        A --> A2[REST APIs]
        A --> A3[GraphQL APIs]
        A --> A4[RSS/XML Feeds]
        A --> A5[FTP/SFTP]
        A --> A6[Databases]
    end
    
    subgraph "Collection Methods"
        B --> B1[BeautifulSoup]
        B --> B2[Selenium WebDriver]
        B --> B3[Scrapy Framework]
        B --> B4[Requests]
        B --> B5[aiohttp]
    end
    
    subgraph "Processing Pipeline"
        C --> C1[Data Parsing]
        C --> C2[Number Extraction]
        C --> C3[Validation]
        C --> C4[Cleaning]
        C --> C5[Transformation]
    end
    
    subgraph "Aggregation Engine"
        D --> D1[Statistical Analysis]
        D --> D2[Time Series Aggregation]
        D --> D3[Pattern Recognition]
        D --> D4[Anomaly Detection]
    end
    
    subgraph "Output Formats"
        F --> F1[JSON API]
        F --> F2[CSV Export]
        F --> F3[XML Feed]
        F --> F4[Database Insert]
        F --> F5[Dashboard]
    end
    
    style A fill:#e1f5fe
    style C fill:#fff3e0
    style D fill:#c8e6c9
    style F fill:#f3e5f5
```

## 🔄 Data Flow Pipeline

```mermaid
flowchart TD
    A[Data Sources] --> B[Source Scheduler]
    B --> C[Collection Workers]
    C --> D[Data Validation]
    D --> E{Valid Data?}
    E -->|Yes| F[Number Extraction]
    E -->|No| G[Error Handler]
    G --> H[Retry Queue]
    H --> C
    F --> I[Data Enrichment]
    I --> J[Aggregation Engine]
    J --> K[Quality Check]
    K --> L{Quality Pass?}
    L -->|Yes| M[Storage Layer]
    L -->|No| N[Manual Review Queue]
    M --> O[Output Generation]
    O --> P[API Endpoints]
    O --> Q[File Export]
    O --> R[Dashboard Update]
    
    subgraph "Monitoring"
        P --> S[Metrics Collection]
        Q --> S
        R --> S
        S --> T[Alerting System]
    end
    
    style A fill:#e1f5fe
    style J fill:#fff3e0
    style M fill:#c8e6c9
    style T fill:#ffebee
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Git
- Docker (optional)
- Chrome/Firefox browser (for Selenium)

### 📦 Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Ismat-Samadov/NumberAggregator.git
   cd NumberAggregator
   ```

2. **Create Virtual Environment**
   ```bash
   # Using conda (recommended)
   conda create -n number_aggregator python=3.9
   conda activate number_aggregator
   
   # Or using venv
   python -m venv number_aggregator_env
   source number_aggregator_env/bin/activate  # On Windows: number_aggregator_env\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   
   # For development
   pip install -r requirements-dev.txt
   ```

4. **Setup Configuration**
   ```bash
   cp config/.env.example config/.env
   # Edit config/.env with your settings
   ```

5. **Initialize Database**
   ```bash
   python scripts/init_database.py
   ```

### 🏃‍♂️ Running the System

#### Option 1: Basic Data Collection
```bash
# Collect data from predefined sources
python main.py --sources financial_apis --output data/collected.json

# Scrape specific websites
python main.py --scrape "https://example.com/stats" --extract numbers --format csv
```

#### Option 2: API Server Mode
```bash
# Start the API server
uvicorn api.main:app --host 0.0.0.0 --port 8000

# Access API documentation at http://localhost:8000/docs
```

#### Option 3: Scheduled Collection
```bash
# Run scheduled data collection
python scheduler.py --config config/collection_schedule.yaml

# Or use cron-style scheduling
python main.py --cron "0 */6 * * *" --sources all
```

#### Option 4: Web Dashboard
```bash
# Launch monitoring dashboard
streamlit run dashboard/app.py

# Access dashboard at http://localhost:8501
```

## 🛠️ Technology Stack

### Core Technologies

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Language** | Python 3.8+ | Core development language |
| **Web Scraping** | BeautifulSoup, Selenium, Scrapy | Data extraction from websites |
| **HTTP Clients** | requests, aiohttp, httpx | API integration and HTTP requests |
| **Data Processing** | Pandas, NumPy, Polars | Data manipulation and analysis |
| **Async Processing** | asyncio, Celery, RQ | Concurrent data collection |
| **Web Framework** | FastAPI, Streamlit | APIs and dashboards |
| **Database** | PostgreSQL, MongoDB, Redis | Data storage and caching |
| **Message Queue** | RabbitMQ, Apache Kafka | Task distribution |
| **Monitoring** | Prometheus, Grafana | Performance monitoring |

### Data Sources & Integration

```mermaid
graph LR
    A[NumberAggregator] --> B[Web Scraping]
    A --> C[API Integration]
    A --> D[File Processing]
    A --> E[Database Connections]
    
    B --> B1[Static HTML]
    B --> B2[JavaScript Heavy Sites]
    B --> B3[Interactive Forms]
    B --> B4[Tables & Lists]
    B --> B5[PDFs & Documents]
    
    C --> C1[REST APIs]
    C --> C2[GraphQL APIs]
    C --> C3[SOAP Services]
    C --> C4[RSS/Atom Feeds]
    C --> C5[WebSocket Streams]
    
    D --> D1[CSV Files]
    D --> D2[Excel Spreadsheets]
    D --> D3[JSON Documents]
    D --> D4[XML Data]
    D --> D5[Text Files]
    
    E --> E1[SQL Databases]
    E --> E2[NoSQL Stores]
    E --> E3[Time Series DBs]
    E --> E4[Data Warehouses]
    
    style A fill:#e1f5fe
    style B fill:#c8e6c9
    style C fill:#fff3e0
    style D fill:#f3e5f5
    style E fill:#ffebee
```

## 📁 Project Structure

```
NumberAggregator/
├── 📁 src/
│   ├── 📁 scrapers/               # Web scraping modules
│   │   ├── base_scraper.py        # Base scraper class
│   │   ├── selenium_scraper.py    # Selenium-based scraper
│   │   ├── beautifulsoup_scraper.py # BeautifulSoup scraper
│   │   ├── scrapy_spiders/        # Scrapy spider collection
│   │   └── browser_automation/    # Browser automation utilities
│   ├── 📁 apis/                   # API integration modules
│   │   ├── rest_client.py         # REST API client
│   │   ├── graphql_client.py      # GraphQL client
│   │   ├── rate_limiter.py        # Rate limiting utilities
│   │   └── auth_handlers/         # Authentication modules
│   ├── 📁 extractors/             # Number extraction engines
│   │   ├── pattern_extractors.py  # Regex-based extraction
│   │   ├── ml_extractors.py       # ML-based extraction
│   │   ├── context_analyzers.py   # Context-aware parsing
│   │   └── validators.py          # Data validation
│   ├── 📁 processors/             # Data processing pipeline
│   │   ├── cleaners.py            # Data cleaning utilities
│   │   ├── transformers.py        # Data transformation
│   │   ├── aggregators.py         # Aggregation algorithms
│   │   └── quality_checks.py      # Quality assurance
│   ├── 📁 storage/                # Data storage layer
│   │   ├── database_managers.py   # Database operations
│   │   ├── file_handlers.py       # File I/O operations
│   │   ├── cache_managers.py      # Caching layer
│   │   └── backup_services.py     # Backup and recovery
│   ├── 📁 schedulers/             # Task scheduling
│   │   ├── cron_scheduler.py      # Cron-like scheduling
│   │   ├── priority_queue.py      # Task prioritization
│   │   └── worker_manager.py      # Worker process management
│   └── 📁 utils/                  # Utility functions
│       ├── config_manager.py      # Configuration management
│       ├── logging_setup.py       # Logging configuration
│       ├── error_handlers.py      # Error handling utilities
│       └── helpers.py             # General helper functions
├── 📁 api/                        # REST API server
│   ├── main.py                    # FastAPI application
│   ├── routers/                   # API route definitions
│   ├── models/                    # Pydantic models
│   ├── dependencies.py           # API dependencies
│   └── middleware/                # Custom middleware
├── 📁 dashboard/                  # Web dashboard
│   ├── app.py                     # Streamlit application
│   ├── components/                # Dashboard components
│   ├── pages/                     # Dashboard pages
│   └── static/                    # Static assets
├── 📁 config/                     # Configuration files
│   ├── sources.yaml               # Data source configurations
│   ├── extractors.yaml            # Extraction patterns
│   ├── aggregation_rules.yaml     # Aggregation rules
│   ├── deployment.yaml            # Deployment settings
│   └── .env.example               # Environment variables template
├── 📁 scripts/                    # Utility scripts
│   ├── data_collection/           # Collection scripts
│   ├── data_migration/            # Migration utilities
│   ├── monitoring/                # Monitoring scripts
│   └── deployment/                # Deployment automation
├── 📁 tests/                      # Test suite
│   ├── unit/                      # Unit tests
│   ├── integration/               # Integration tests
│   ├── performance/               # Performance tests
│   └── fixtures/                  # Test fixtures and mock data
├── 📁 deployments/                # Deployment configurations
│   ├── docker/                    # Docker configurations
│   ├── kubernetes/                # Kubernetes manifests
│   ├── terraform/                 # Infrastructure as code
│   └── ansible/                   # Configuration management
├── 📁 data/                       # Data storage
│   ├── raw/                       # Raw collected data
│   ├── processed/                 # Processed datasets
│   ├── aggregated/                # Aggregated results
│   └── exports/                   # Export files
├── 📁 logs/                       # Application logs
├── 📁 monitoring/                 # Monitoring configurations
│   ├── prometheus/                # Prometheus configs
│   ├── grafana/                   # Grafana dashboards
│   └── alerts/                    # Alert rules
├── 📄 requirements.txt            # Python dependencies
├── 📄 requirements-dev.txt        # Development dependencies
├── 📄 docker-compose.yml          # Multi-container setup
├── 📄 Dockerfile                  # Container configuration
└── 📄 README.md                   # This file
```

## 🔧 Configuration

### Environment Variables

```bash
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/number_aggregator
REDIS_URL=redis://localhost:6379/0

# Web Scraping Configuration
CHROME_DRIVER_PATH=/usr/local/bin/chromedriver
SELENIUM_GRID_URL=http://selenium-hub:4444/wd/hub
USER_AGENT="NumberAggregator Bot 1.0"
REQUEST_TIMEOUT=30
RETRY_ATTEMPTS=3

# API Configuration
API_RATE_LIMIT=100
MAX_CONCURRENT_REQUESTS=10
CACHE_TTL=3600

# Processing Configuration
BATCH_SIZE=1000
WORKER_THREADS=4
AGGREGATION_WINDOW=300

# Storage Configuration
OUTPUT_FORMAT=json
COMPRESSION_ENABLED=true
BACKUP_RETENTION_DAYS=30

# Monitoring Configuration
PROMETHEUS_PORT=9090
GRAFANA_PORT=3000
LOG_LEVEL=INFO
ALERT_WEBHOOK_URL=http://alerts.example.com/webhook

# Cloud Configuration (if applicable)
AWS_REGION=us-east-1
S3_BUCKET=number-aggregator-data
AZURE_STORAGE_ACCOUNT=numberaggregator
GCP_PROJECT_ID=number-aggregator-project
```

### Data Source Configuration

```yaml
# config/sources.yaml
data_sources:
  financial_apis:
    - name: "yahoo_finance"
      type: "api"
      url: "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
      method: "GET"
      headers:
        User-Agent: "NumberAggregator/1.0"
      rate_limit: 100  # requests per minute
      extract_patterns:
        - name: "current_price"
          path: "$.chart.result[0].meta.regularMarketPrice"
          type: "float"
        - name: "volume"
          path: "$.chart.result[0].meta.regularMarketVolume"
          type: "integer"
    
    - name: "crypto_prices"
      type: "api"
      url: "https://api.coindesk.com/v1/bpi/currentprice.json"
      method: "GET"
      extract_patterns:
        - name: "btc_usd"
          path: "$.bpi.USD.rate_float"
          type: "float"
  
  ecommerce_websites:
    - name: "product_prices"
      type: "scrape"
      urls:
        - "https://example-store.com/products/{category}"
      scraper_type: "selenium"
      wait_conditions:
        - type: "element_visible"
          selector: ".price"
          timeout: 10
      extract_patterns:
        - name: "price"
          selector: ".price"
          regex: '\$?([0-9,]+\.?[0-9]*)'
          type: "float"
        - name: "rating"
          selector: ".rating"
          regex: '([0-9]\.[0-9])'
          type: "float"
      pagination:
        enabled: true
        next_button: ".pagination .next"
        max_pages: 10

  statistics_websites:
    - name: "government_stats"
      type: "scrape"
      urls:
        - "https://stats.gov.example/economic-indicators"
      scraper_type: "beautifulsoup"
      extract_patterns:
        - name: "unemployment_rate"
          selector: "#unemployment-rate"
          regex: '([0-9]+\.?[0-9]*)%'
          type: "float"
        - name: "inflation_rate"
          selector: "#inflation-rate"
          regex: '([0-9]+\.?[0-9]*)%'
          type: "float"
```

### Aggregation Rules

```yaml
# config/aggregation_rules.yaml
aggregation_rules:
  price_statistics:
    input_sources: ["financial_apis", "ecommerce_websites"]
    aggregation_type: "statistical"
    functions:
      - name: "average_price"
        operation: "mean"
        fields: ["current_price", "price"]
      - name: "price_volatility"
        operation: "std"
        fields: ["current_price"]
      - name: "price_trend"
        operation: "linear_regression"
        fields: ["current_price"]
        window: "24h"
    
  time_series_aggregation:
    input_sources: ["all"]
    aggregation_type: "temporal"
    windows:
      - name: "hourly"
        duration: "1h"
        functions: ["min", "max", "mean", "count"]
      - name: "daily"
        duration: "24h"
        functions: ["min", "max", "mean", "sum", "std"]
      - name: "weekly"
        duration: "7d"
        functions: ["mean", "sum", "trend"]
    
  anomaly_detection:
    input_sources: ["all"]
    algorithms:
      - name: "z_score"
        threshold: 3.0
        window: "1h"
      - name: "isolation_forest"
        contamination: 0.1
    actions:
      - type: "alert"
        webhook: "${ALERT_WEBHOOK_URL}"
      - type: "quarantine"
        table: "anomalous_data"
```

## 🎛️ Usage Examples

### 1. Simple Web Scraping

```python
from src.scrapers.beautifulsoup_scraper import BeautifulSoupScraper
from src.extractors.pattern_extractors import NumberExtractor

# Initialize scraper and extractor
scraper = BeautifulSoupScraper()
extractor = NumberExtractor()

# Scrape a webpage
html_content = scraper.scrape("https://example.com/statistics")

# Extract numbers from the content
numbers = extractor.extract_numbers(
    html_content,
    patterns=[
        {"name": "revenue", "selector": ".revenue", "regex": r"\$([0-9,]+)"},
        {"name": "users", "selector": ".user-count", "regex": r"([0-9,]+)\s+users"}
    ]
)

print("Extracted numbers:", numbers)
```

### 2. API Data Collection

```python
from src.apis.rest_client import RestAPIClient
from src.processors.aggregators import StatisticalAggregator

# Initialize API client
api_client = RestAPIClient(
    base_url="https://api.example.com",
    rate_limit=100,  # requests per minute
    auth_token="your_api_token"
)

# Collect data from multiple endpoints
endpoints = [
    "/metrics/revenue",
    "/metrics/users",
    "/metrics/engagement"
]

collected_data = []
for endpoint in endpoints:
    data = api_client.get(endpoint)
    collected_data.extend(data.get('results', []))

# Aggregate the collected data
aggregator = StatisticalAggregator()
aggregated_results = aggregator.aggregate(
    collected_data,
    group_by="metric_type",
    functions=["mean", "sum", "std"]
)

print("Aggregated results:", aggregated_results)
```

### 3. Selenium Web Scraping

```python
from src.scrapers.selenium_scraper import SeleniumScraper
from src.extractors.context_analyzers import ContextAwareExtractor

# Initialize Selenium scraper
scraper = SeleniumScraper(
    browser="chrome",
    headless=True,
    implicit_wait=10
)

# Scrape dynamic content
scraper.get("https://dynamic-site.com/dashboard")

# Wait for specific elements and interact
scraper.wait_for_element(".data-table", timeout=15)
scraper.click_element(".load-more-button")

# Extract numbers with context
extractor = ContextAwareExtractor()
extracted_data = extractor.extract_with_context(
    scraper.page_source,
    context_clues=["price", "cost", "revenue", "profit", "loss"]
)

scraper.quit()
print("Extracted data with context:", extracted_data)
```

### 4. Scheduled Data Collection

```python
from src.schedulers.cron_scheduler import CronScheduler
from src.processors.quality_checks import DataQualityChecker

# Initialize scheduler
scheduler = CronScheduler()

# Define collection tasks
tasks = [
    {
        "name": "financial_data_collection",
        "schedule": "0 */6 * * *",  # Every 6 hours
        "source": "financial_apis",
        "output": "data/financial.json"
    },
    {
        "name": "ecommerce_price_scraping",
        "schedule": "0 2 * * *",  # Daily at 2 AM
        "source": "ecommerce_websites",
        "output": "data/prices.csv"
    }
]

# Add quality checks
quality_checker = DataQualityChecker()

for task in tasks:
    def collection_job():
        # Collect data
        data = collect_from_source(task["source"])
        
        # Quality check
        quality_report = quality_checker.check(data)
        if quality_report["passed"]:
            # Save to output
            save_data(data, task["output"])
        else:
            # Handle quality issues
            handle_quality_issues(quality_report)
    
    scheduler.add_job(
        func=collection_job,
        cron=task["schedule"],
        id=task["name"]
    )

# Start the scheduler
scheduler.start()
```

### 5. Real-time Data Streaming

```python
import asyncio
from src.apis.websocket_client import WebSocketClient
from src.processors.stream_processor import StreamProcessor

async def real_time_collection():
    # Initialize WebSocket client and stream processor
    ws_client = WebSocketClient("wss://api.example.com/stream")
    processor = StreamProcessor(
        buffer_size=1000,
        flush_interval=60  # seconds
    )
    
    # Connect and process streaming data
    await ws_client.connect()
    
    async for message in ws_client.listen():
        # Extract numbers from streaming data
        numbers = extract_numbers_from_message(message)
        
        # Add to processing buffer
        processor.add_data(numbers)
        
        # Check if buffer should be flushed
        if processor.should_flush():
            aggregated = processor.flush_and_aggregate()
            await save_aggregated_data(aggregated)

# Run the real-time collection
asyncio.run(real_time_collection())
```

## 📊 Data Processing & Aggregation

### Number Extraction Patterns

```python
# src/extractors/pattern_extractors.py
import re
from typing import List, Dict, Any

class NumberExtractor:
    def __init__(self):
        self.patterns = {
            'currency': r'[\$£€¥]?([0-9,]+\.?[0-9]*)',
            'percentage': r'([0-9]+\.?[0-9]*)%',
            'decimal': r'([0-9]+\.[0-9]+)',
            'integer': r'([0-9,]+)',
            'scientific': r'([0-9]+\.?[0-9]*[eE][+-]?[0-9]+)',
            'phone': r'\(([0-9]{3})\)\s?([0-9]{3})-([0-9]{4})',
            'coordinate': r'(-?[0-9]+\.?[0-9]*),\s*(-?[0-9]+\.?[0-9]*)'
        }
    
    def extract_numbers(self, text: str, pattern_types: List[str] = None) -> Dict[str, List[float]]:
        """Extract numbers based on specified patterns"""
        if pattern_types is None:
            pattern_types = list(self.patterns.keys())
        
        results = {}
        for pattern_type in pattern_types:
            if pattern_type in self.patterns:
                matches = re.findall(self.patterns[pattern_type], text)
                results[pattern_type] = [self._convert_to_number(match) for match in matches]
        
        return results
    
    def _convert_to_number(self, match) -> float:
        """Convert extracted string to number"""
        if isinstance(match, tuple):
            # Handle tuples (like phone numbers or coordinates)
            return match
        
        # Remove commas and convert to float
        cleaned = match.replace(',', '')
        try:
            return float(cleaned)
        except ValueError:
            return 0.0
```

### Advanced Aggregation Engine

```python
# src/processors/aggregators.py
import pandas as pd
import numpy as np
from typing import Dict, List, Any
from datetime import datetime, timedelta

class AdvancedAggregator:
    def __init__(self):
        self.aggregation_functions = {
            'mean': np.mean,
            'median': np.median,
            'std': np.std,
            'min': np.min,
            'max': np.max,
            'sum': np.sum,
            'count': len,
            'percentile_25': lambda x: np.percentile(x, 25),
            'percentile_75': lambda x: np.percentile(x, 75),
            'variance': np.var,
            'skewness': lambda x: pd.Series(x).skew(),
            'kurtosis': lambda x: pd.Series(x).kurtosis()
        }
    
    def time_series_aggregation(self, data: List[Dict], 
                              time_column: str, 
                              value_column: str,
                              window: str = '1H') -> pd.DataFrame:
        """Aggregate time series data by time windows"""
        df = pd.DataFrame(data)
        df[time_column] = pd.to_datetime(df[time_column])
        df.set_index(time_column, inplace=True)
        
        # Resample and aggregate
        aggregated = df[value_column].resample(window).agg([
            'mean', 'min', 'max', 'std', 'count'
        ])
        
        return aggregated
    
    def statistical_aggregation(self, data: List[float], 
                               functions: List[str] = None) -> Dict[str, float]:
        """Apply statistical functions to data"""
        if functions is None:
            functions = ['mean', 'std', 'min', 'max']
        
        results = {}
        for func_name in functions:
            if func_name in self.aggregation_functions:
                try:
                    results[func_name] = self.aggregation_functions[func_name](data)
                except Exception as e:
                    results[func_name] = None
                    print(f"Error applying {func_name}: {e}")
        
        return results
    
    def moving_window_aggregation(self, data: List[float], 
                                 window_size: int,
                                 functions: List[str] = None) -> List[Dict]:
        """Apply moving window aggregation"""
        if functions is None:
            functions = ['mean', 'std']
        
        results = []
        for i in range(len(data) - window_size + 1):
            window_data = data[i:i + window_size]
            window_stats = self.statistical_aggregation(window_data, functions)
            window_stats['window_start'] = i
            window_stats['window_end'] = i + window_size - 1
            results.append(window_stats)
        
        return results
```

## ☁️ Deployment

### Docker Deployment

```yaml
# docker-compose.yml
version: '3.8'

services:
  number-aggregator:
    build: .
    environment:
      - DATABASE_URL=postgresql://postgres:password@postgres:5432/number_aggregator
      - REDIS_URL=redis://redis:6379/0
      - SELENIUM_GRID_URL=http://selenium-hub:4444/wd/hub
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
      - ./config:/app/config
    depends_on:
      - postgres
      - redis
      - selenium-hub
    restart: unless-stopped
    ports:
      - "8000:8000"
  
  postgres:
    image: postgres:13
    environment:
      POSTGRES_DB: number_aggregator
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
  
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
  
  selenium-hub:
    image: selenium/hub:4.0.0
    ports:
      - "4444:4444"
  
  selenium-chrome:
    image: selenium/node-chrome:4.0.0
    shm_size: 2gb
    depends_on:
      - selenium-hub
    environment:
      - HUB_HOST=selenium-hub
      - HUB_PORT=4444
    scale: 3
  
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus:/etc/prometheus
      - prometheus_data:/prometheus
  
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana/dashboards:/etc/grafana/provisioning/dashboards
      - ./monitoring/grafana/datasources:/etc/grafana/provisioning/datasources

volumes:
  postgres_data:
  redis_data:
  prometheus_data:
  grafana_data:
```

### Kubernetes Deployment

```yaml
# deployments/kubernetes/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: number-aggregator
  labels:
    app: number-aggregator
spec:
  replicas: 3
  selector:
    matchLabels:
      app: number-aggregator
  template:
    metadata:
      labels:
        app: number-aggregator
    spec:
      containers:
      - name: number-aggregator
        image: number-aggregator:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        - name: REDIS_URL
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: redis-url
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: number-aggregator-service
spec:
  selector:
    app: number-aggregator
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: LoadBalancer
```

### Cloud Deployment (AWS)

```bash
# Deploy to AWS ECS using Terraform
cd deployments/terraform/aws/

# Initialize Terraform
terraform init

# Plan deployment
terraform plan -var="environment=production"

# Apply deployment
terraform apply

# Or deploy using AWS CLI and ECS
aws ecs create-cluster --cluster-name number-aggregator

# Create task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json

# Create service
aws ecs create-service \
    --cluster number-aggregator \
    --service-name number-aggregator-service \
    --task-definition number-aggregator:1 \
    --desired-count 2
```

## 📈 Monitoring & Observability

### Metrics Collection

```python
# src/monitoring/metrics_collector.py
import time
from prometheus_client import Counter, Histogram, Gauge, start_http_server

class MetricsCollector:
    def __init__(self):
        # Define metrics
        self.requests_total = Counter(
            'scraping_requests_total', 
            'Total scraping requests',
            ['source', 'status']
        )
        
        self.request_duration = Histogram(
            'scraping_request_duration_seconds',
            'Time spent on scraping requests',
            ['source']
        )
        
        self.active_scrapers = Gauge(
            'active_scrapers',
            'Number of active scrapers'
        )
        
        self.extracted_numbers = Counter(
            'extracted_numbers_total',
            'Total numbers extracted',
            ['source', 'type']
        )
        
        self.data_quality_score = Gauge(
            'data_quality_score',
            'Data quality score (0-1)',
            ['source']
        )
    
    def record_request(self, source: str, status: str, duration: float):
        """Record a scraping request"""
        self.requests_total.labels(source=source, status=status).inc()
        self.request_duration.labels(source=source).observe(duration)
    
    def record_extraction(self, source: str, number_type: str, count: int):
        """Record number extractions"""
        self.extracted_numbers.labels(source=source, type=number_type).inc(count)
    
    def update_quality_score(self, source: str, score: float):
        """Update data quality score"""
        self.data_quality_score.labels(source=source).set(score)
    
    def start_metrics_server(self, port: int = 8001):
        """Start Prometheus metrics server"""
        start_http_server(port)
        print(f"Metrics server started on port {port}")
```

### Dashboard Configuration

```python
# dashboard/components/monitoring.py
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

class MonitoringDashboard:
    def __init__(self, data_manager):
        self.data_manager = data_manager
    
    def render_overview(self):
        """Render overview metrics"""
        st.header("📊 System Overview")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_sources = self.data_manager.get_active_sources_count()
            st.metric("Active Sources", total_sources)
        
        with col2:
            daily_collections = self.data_manager.get_daily_collection_count()
            st.metric("Daily Collections", daily_collections)
        
        with col3:
            success_rate = self.data_manager.get_success_rate()
            st.metric("Success Rate", f"{success_rate:.1%}")
        
        with col4:
            avg_quality = self.data_manager.get_average_quality_score()
            st.metric("Avg Quality Score", f"{avg_quality:.2f}")
    
    def render_collection_trends(self):
        """Render collection trend charts"""
        st.header("📈 Collection Trends")
        
        # Get trend data
        trend_data = self.data_manager.get_collection_trends(days=7)
        
        # Create trend chart
        fig = px.line(
            trend_data, 
            x='timestamp', 
            y='count',
            color='source',
            title="Data Collection Trends (Last 7 Days)"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    def render_quality_metrics(self):
        """Render data quality metrics"""
        st.header("🎯 Data Quality")
        
        quality_data = self.data_manager.get_quality_metrics()
        
        # Quality score distribution
        fig = px.histogram(
            quality_data,
            x='quality_score',
            nbins=20,
            title="Quality Score Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Quality by source
        source_quality = quality_data.groupby('source')['quality_score'].mean().reset_index()
        fig2 = px.bar(
            source_quality,
            x='source',
            y='quality_score',
            title="Average Quality Score by Source"
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    def render_error_analysis(self):
        """Render error analysis"""
        st.header("🚨 Error Analysis")
        
        error_data = self.data_manager.get_error_summary()
        
        if not error_data.empty:
            # Error distribution
            fig = px.pie(
                error_data,
                values='count',
                names='error_type',
                title="Error Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Recent errors
            st.subheader("Recent Errors")
            recent_errors = self.data_manager.get_recent_errors(limit=10)
            st.dataframe(recent_errors)
        else:
            st.success("No errors in the recent period! 🎉")
```

## 🧪 Testing & Quality Assurance

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test categories
pytest tests/unit/ -v                    # Unit tests
pytest tests/integration/ -v             # Integration tests
pytest tests/performance/ -v             # Performance tests

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run load tests
locust -f tests/load/locustfile.py --host=http://localhost:8000
```

### Data Quality Testing

```python
# tests/integration/test_data_quality.py
import pytest
from src.processors.quality_checks import DataQualityChecker
from src.extractors.pattern_extractors import NumberExtractor

class TestDataQuality:
    def setup_method(self):
        self.quality_checker = DataQualityChecker()
        self.extractor = NumberExtractor()
    
    def test_number_extraction_accuracy(self):
        """Test accuracy of number extraction"""
        test_cases = [
            {
                'input': "The price is $123.45 and the discount is 15%",
                'expected': {
                    'currency': [123.45],
                    'percentage': [15.0]
                }
            },
            {
                'input': "Revenue increased to 1,500,000 from 1,200,000",
                'expected': {
                    'integer': [1500000, 1200000]
                }
            }
        ]
        
        for case in test_cases:
            result = self.extractor.extract_numbers(
                case['input'], 
                list(case['expected'].keys())
            )
            assert result == case['expected']
    
    def test_data_completeness(self):
        """Test data completeness checks"""
        complete_data = [
            {'value': 100, 'source': 'api1', 'timestamp': '2024-01-01'},
            {'value': 200, 'source': 'api2', 'timestamp': '2024-01-01'}
        ]
        
        incomplete_data = [
            {'value': 100, 'source': 'api1'},  # Missing timestamp
            {'source': 'api2', 'timestamp': '2024-01-01'}  # Missing value
        ]
        
        assert self.quality_checker.check_completeness(complete_data) == 1.0
        assert self.quality_checker.check_completeness(incomplete_data) < 1.0
    
    def test_anomaly_detection(self):
        """Test anomaly detection"""
        normal_data = [10, 12, 11, 13, 9, 14, 10, 12]
        anomalous_data = normal_data + [100]  # Add outlier
        
        normal_result = self.quality_checker.detect_anomalies(normal_data)
        anomalous_result = self.quality_checker.detect_anomalies(anomalous_data)
        
        assert len(normal_result['anomalies']) == 0
        assert len(anomalous_result['anomalies']) > 0
```

## 🤝 Contributing

### Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/your-username/NumberAggregator.git
cd NumberAggregator

# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Setup test database
python scripts/setup_test_db.py

# Create feature branch
git checkout -b feature/your-feature-name
```

### Code Quality Standards

```bash
# Format code
black src/ tests/
isort src/ tests/

# Lint code
flake8 src/ tests/
pylint src/

# Type checking
mypy src/

# Security scanning
bandit -r src/

# Documentation checks
pydocstyle src/

# Run all quality checks
make lint-all
```

### Adding New Data Sources

```python
# Example: Adding a new scraper
# src/scrapers/custom_scraper.py
from .base_scraper import BaseScraper
from typing import Dict, Any, List

class CustomWebsiteScraper(BaseScraper):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.base_url = config.get('base_url')
        self.custom_headers = config.get('headers', {})
    
    def scrape(self, url: str) -> Dict[str, Any]:
        """Implement custom scraping logic"""
        response = self.session.get(url, headers=self.custom_headers)
        response.raise_for_status()
        
        # Parse content using BeautifulSoup
        soup = self.get_soup(response.content)
        
        # Extract data using custom logic
        data = self.extract_custom_data(soup)
        
        return {
            'url': url,
            'timestamp': self.get_timestamp(),
            'data': data,
            'metadata': self.get_metadata(response)
        }
    
    def extract_custom_data(self, soup) -> List[Dict]:
        """Custom data extraction logic"""
        # Implement your extraction logic here
        pass
```

## 📚 API Documentation

### REST API Endpoints

```python
# api/routers/collection.py
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Optional
from ..models.requests import CollectionRequest
from ..models.responses import CollectionResponse

router = APIRouter(prefix="/api/v1", tags=["collection"])

@router.post("/collect", response_model=CollectionResponse)
async def trigger_collection(
    request: CollectionRequest,
    background_tasks: BackgroundTasks
):
    """Trigger data collection from specified sources"""
    try:
        # Validate sources
        valid_sources = validate_sources(request.sources)
        
        # Start background collection task
        background_tasks.add_task(
            start_collection_task,
            sources=valid_sources,
            config=request.config
        )
        
        return CollectionResponse(
            task_id=generate_task_id(),
            status="started",
            sources=valid_sources
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/status/{task_id}")
async def get_collection_status(task_id: str):
    """Get status of a collection task"""
    status = get_task_status(task_id)
    if not status:
        raise HTTPException(status_code=404, detail="Task not found")
    return status

@router.get("/data/{source}")
async def get_collected_data(
    source: str,
    limit: Optional[int] = 100,
    offset: Optional[int] = 0,
    format: Optional[str] = "json"
):
    """Retrieve collected data from a specific source"""
    data = get_data_from_source(source, limit, offset)
    
    if format == "csv":
        return convert_to_csv(data)
    elif format == "xml":
        return convert_to_xml(data)
    else:
        return data

@router.get("/metrics")
async def get_collection_metrics():
    """Get collection performance metrics"""
    return {
        "total_collections": get_total_collections(),
        "success_rate": get_success_rate(),
        "average_duration": get_average_duration(),
        "active_sources": get_active_sources_count(),
        "error_rate": get_error_rate()
    }
```

### WebSocket API for Real-time Updates

```python
# api/websocket.py
from fastapi import WebSocket, WebSocketDisconnect
from typing import List
import json
import asyncio

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(message))
            except:
                # Remove broken connections
                self.active_connections.remove(connection)

manager = ConnectionManager()

@router.websocket("/ws/updates")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and send updates
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Web Scraping Libraries**: BeautifulSoup, Selenium, Scrapy communities
- **Data Processing**: pandas, NumPy, Polars contributors
- **API Frameworks**: FastAPI, Streamlit teams
- **Monitoring Tools**: Prometheus, Grafana projects
- **Cloud Providers**: AWS, Azure, Google Cloud Platform
- **Open Source Community**: All contributors and maintainers
---

<div align="center">

**🌟 Star this repository if you find it helpful! 🌟**

*Aggregating the world's numbers, one source at a time* 🔢📊

**Made with ❤️ for the data community**

</div>
