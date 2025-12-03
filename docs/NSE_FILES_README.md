# NSE India Data Files Documentation

This document describes the default files that HomeStock downloads from the National Stock Exchange (NSE) India website.

## Overview

HomeStock automatically downloads historical market data files from NSE India. These files contain trading data for equities and derivatives markets, including prices, volumes, open interest, and delivery information.

## Default Files Downloaded

The application attempts to download **6 file types** for each trading day (some may be duplicates):

### 1. F&O Bhavcopy (Derivatives Market Data)
- **File Type**: `fo_bhavcopy`
- **Format**: ZIP archive containing CSV
- **URL Pattern**: 
  ```
  https://www.nseindia.com/content/historical/DERIVATIVES/{YEAR}/{MONTH}/fo{DD}{MONTH}{YEAR}bhav.csv.zip
  ```
- **Example**: `fo01DEC2023bhav.csv.zip`
- **Contents**: 
  - Futures and Options (F&O) market bhavcopy
  - Contains all derivative contracts traded on NSE
  - Includes: Symbol, Expiry Date, Strike Price, Option Type, Open, High, Low, Close, Settle Price, Contracts, Value, Open Interest
- **Use Case**: Analysis of derivatives trading, options strategies, futures data

### 2. CM Bhavcopy (Cash Market Equity Data)
- **File Type**: `cm_bhavcopy` / `cm_udiff`
- **Format**: ZIP archive containing CSV
- **URL Pattern**:
  ```
  https://www.nseindia.com/content/historical/EQUITIES/{YEAR}/{MONTH}/cm{DD}{MONTH}{YEAR}bhav.csv.zip
  ```
- **Example**: `cm01DEC2023bhav.csv.zip`
- **Contents**:
  - Cash Market (Equity) bhavcopy
  - Contains all equity stocks traded on NSE
  - Includes: Symbol, Series, Open, High, Low, Close, Last, Prev Close, Total Traded Quantity, Total Traded Value, Timestamp
- **Use Case**: Equity market analysis, stock price history, volume analysis

### 3. F&O Open Interest (Combined OI)
- **File Type**: `fo_udiff` / `fo_participant_oi`
- **Format**: ZIP archive
- **URL Pattern**:
  ```
  https://www.nseindia.com/archives/nsccl/mwpl/combineoi_{DD}{MM}{YYYY}.zip
  ```
- **Example**: `combineoi_01122023.zip`
- **Contents**:
  - Combined Open Interest data for F&O contracts
  - Market-wide position limits (MWPL) data
  - Open Interest by participant category
- **Use Case**: Options trading analysis, open interest trends, market sentiment

### 4. CM Delivery Data (Market Turnover)
- **File Type**: `cm_delivery`
- **Format**: DAT file (text format)
- **URL Pattern**:
  ```
  https://www.nseindia.com/archives/equities/mto/MTO_{DD}{MM}{YYYY}.DAT
  ```
- **Example**: `MTO_01122023.DAT`
- **Contents**:
  - Market Turnover and Delivery data
  - Delivery percentage, turnover, traded quantity
  - Stock-wise delivery statistics
- **Use Case**: Delivery analysis, identifying stocks with high delivery percentage, understanding buying/selling patterns

### 5. F&O Participant OI (Same as Combined OI)
- **File Type**: `fo_participant_oi`
- **Note**: Currently uses the same URL as `fo_udiff` (Combined OI)
- **Future Enhancement**: May be separated to download participant-wise OI data

## File Naming Convention

### Date Format in URLs
- **Day**: `{DD}` - Two-digit day (01-31)
- **Month**: `{MONTH}` - Three-letter month abbreviation (JAN, FEB, MAR, etc.)
- **Year**: `{YEAR}` - Four-digit year (2023, 2024, etc.)
- **Month Number**: `{MM}` - Two-digit month number (01-12)

### Examples
For date: **December 1, 2023**
- Day: `01`
- Month: `DEC`
- Year: `2023`
- Month Number: `12`

## File Storage Structure

When downloaded, files are organized as follows:

```
raw_path/
├── 2023/
│   ├── 12/
│   │   ├── fo01DEC2023bhav.csv.zip
│   │   ├── cm01DEC2023bhav.csv.zip
│   │   ├── combineoi_01122023.zip
│   │   └── MTO_01122023.DAT
│   └── ...
└── ...
```

## Data Availability

### Trading Days Only
- Files are available only for **trading days** (weekdays excluding holidays)
- NSE India observes market holidays (national holidays, festivals, etc.)
- Attempting to download files for non-trading days will result in 404 errors

### Historical Data
- Historical data is typically available for several years
- Older data may be archived or removed by NSE
- Current year and previous 1-2 years are most reliably available

## Rate Limiting

HomeStock implements rate limiting to respect NSE's servers:
- **Maximum 5 requests per 60 seconds**
- Automatic delays between downloads
- Prevents overwhelming NSE servers

## File Processing

After download, files can be:
1. **Extracted**: ZIP files are automatically extracted
2. **Parsed**: CSV files are normalized and processed
3. **Stored**: Processed data is saved to configured output folders

## Custom URLs

You can override default URLs by providing custom URLs in the download request:
```json
{
  "start_date": "2023-12-01",
  "end_date": "2023-12-01",
  "urls": {
    "fo_bhavcopy": "custom_url_here",
    "cm_bhavcopy": "custom_url_here"
  },
  "raw_path": "/path/to/raw"
}
```

## Troubleshooting

### File Not Found (404)
- **Cause**: Date is a non-trading day (weekend/holiday)
- **Solution**: Check NSE trading calendar, skip non-trading days

### Download Fails
- **Cause**: Network issues, rate limiting, or NSE server issues
- **Solution**: Use retry functionality, check internet connection

### Incomplete Files
- **Cause**: Network interruption during download
- **Solution**: Delete incomplete file and retry download

## References

- **NSE India Official Website**: https://www.nseindia.com
- **NSE Historical Data**: https://www.nseindia.com/market-data/historical-data
- **NSE Archives**: https://www.nseindia.com/archives

## Notes

- All file downloads respect NSE's terms of service
- Data is for personal/educational use only
- Commercial use may require NSE licensing
- File formats and URLs may change; HomeStock will be updated accordingly

