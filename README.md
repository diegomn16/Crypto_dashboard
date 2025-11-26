# Crypto Dashboard & Serverless ETL Pipeline

Interactive dashboard for technical cryptocurrency analysis, powered by an automated and efficient data pipeline.

This system implements an incremental **ETL (Extract, Transform, Load)** architecture that executes daily via GitHub Actions. It optimizes storage and maintains the mathematical continuity of complex indicators (volatility, drawdown) without the need to recalculate the entire history.

##  Key Features

### 1. Robust Data Engineering
* **Incremental Loading (Delta Load):** The system downloads only new data since the last execution, minimizing API usage and computing time.
* **State Recovery:** To prevent "jumps" in charts when merging old and new data, the script recovers the mathematical context (initial prices, historical peaks for Drawdown) before processing new inputs.
* **Data Integrity:** Strict logic to prevent historical data corruption and "dirty candles" (incomplete data).

### 2. Financial Metrics
* **Normalized Prices:** Base-1 normalization for relative performance comparison across assets.
* **Rolling Volatility:** 30-day rolling standard deviation.
* **Historical Drawdown:** Calculation of the percentage drop from the last relative All-Time High.
* **Daily Returns:** Day-to-day percentage variation.

### 3. Visualization
* Built with **Streamlit** for web interactivity.
* Dynamic charts using **Plotly** (Zoom, Pan, Hover).
* Dynamic date range selectors and asset filtering.

---

##  System Architecture

The data flow follows an automated process defined in `daily_update.yml`:

1.  **Trigger:** Cron job at 00:00 UTC (GitHub Actions).
2.  **Extract:** Queries the Binance API (`src/data_fetcher.py`) fetching data starting from `last_timestamp` + 1ms.
3.  **Transform:**
    * Loads a context buffer (last 60 days).
    * Merges new data.
    * Calculates indicators (`src/features.py`) using vectorized operations.
4.  **Load:** *Appends* new rows to the master CSV (`data/processed/Joint_features.csv`).
5.  **Deploy:** Automatically commits the new data to the repository.

---

##  Local Installation & Usage

### Prerequisites
* Python 3.9+
* Git

### Steps
1.  Clone the repository:
    ```bash
    git clone https://github.com/diegomn16/Crypto_dashboard.git
    cd Crypto_dashboard
    ```

2.  Create a virtual environment and install dependencies:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  Run the Dashboard:
    ```bash
    streamlit run src/dashboard.py
    ```

4.  (Optional) Run the ETL manually:
    ```bash
    python src/download_data.py
    ```

---

##  Project Structure

```text
.
├── .github/workflows/  # CI/CD Automation config
├── data/
│   └── processed/      # Master CSV with incremental history
├── src/
│   ├── dashboard.py    # Web application entry point
│   ├── download_data.py# ETL Orchestrator
│   ├── features.py     # Financial logic (Vectorized calcs)
│   ├── utils.py        # I/O handling and Buffering
│   └── ...
└── requirements.txt