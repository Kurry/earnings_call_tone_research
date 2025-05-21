# Earnings Call Tone Research

This project analyzes the tone/sentiment of company earnings call transcripts using natural language processing.

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install datasets transformers
   ```

3. Set up API keys:
   - This project uses real data sources and does not support mocking
   - You must obtain API keys for Pinecone and Financial Modeling Prep
   - Update the API keys in `research/config.yml`

4. Generate sentiment anchor vector:
   ```bash
   python research/create_sentiment_anchor.py
   ```

## Features

- **Sentiment analysis** of earnings call transcripts using NLTK's VADER sentiment analyzer
- **Batch processing** of multiple transcript files
- **Metadata extraction** from transcript filenames and content
- **Visualization tools** for sentiment distribution and trends
- **Strategy analysis** for potential financial applications
- **Hugging Face dataset integration** for real earnings call transcript data

## Usage

### Basic Analysis

Run the full pipeline to generate tone dispersion signals and backtest:

```bash
# Step 1: Download sentence data from Pinecone
python research/01_pinecone_download.py

# Step 2: Compute tone dispersion signal
python research/02_signal_compute.py

# Step 3: Run backtest
python research/03_backtest.py
```

### Alternative Data Source

If you don't have Pinecone access, you can use the Hugging Face dataset:

```bash
# Process Hugging Face dataset into sentence data
python research/hf_to_sentence_data.py --tickers AAPL,MSFT,AMZN,GOOG
```

### Download Stock Price Data

Download historical stock prices using Financial Modeling Prep API:

```bash
python research/download_stock_data.py
```

## Data Sources

This project uses real data sources:

1. **Earnings Call Transcripts**:
   - Pinecone index with processed transcripts (requires API key)
   - Hugging Face dataset `kurry/sp500_earnings_transcripts`

2. **Stock Price Data**:
   - Financial Modeling Prep API (requires API key)

3. **Factor Data**:
   - French Data Library (manual download)

## Using Real Data vs. Mocking

This project has been updated to use real data sources exclusively and does not support mocked data:

- No mock data is generated as fallbacks
- Scripts will exit with appropriate error messages if required data or API keys are missing
- Each step in the pipeline requires the previous step to have been completed successfully

## Clean Cache Files

To clean up cache directories and temporary files:

```bash
python clean.py
```

## Documentation

See the [GitHub Pages website](https://financial-research.github.io/earnings-call-tone-research/) for more detailed documentation.

## License

MIT
 