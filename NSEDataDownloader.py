import requests
import time
from enum import Enum

class DataType(Enum):
	CASH_MARKET = 'cash_market'
	FUTURE_OPTIONS = 'future_options'
	OPEN_INTEREST_COMBINED = 'open_interest_combined'
	EQUITY_DELIVERY = 'equity_delivery'

def getCurrentDateTime():
	day=int(time.strftime("%d"))
	year=time.strftime("%Y")
	monthinteger=int(time.strftime("%m"))
	monthDict={1:'JAN', 2:'FEB', 3:'MAR', 4:'APR', 5:'MAY', 6:'JUN', 7:'JUL', 8:'AUG', 9:'SEP', 10:'OCT', 11:'NOV', 12:'DEC'}
	month= monthDict[monthinteger]
	
	tu=(day,month,year,monthinteger)
	return tu

class NSEDataDownloader(): 
	
	def __init__(self, tu=getCurrentDateTime()):
		print("Setting up the extraction process....") 
		
		self.cash_market_url = 'https://www.nseindia.com/content/historical/EQUITIES/{2}/{1}/cm{0}{1}{2}bhav.csv.zip'.format(*tu)
		self.future_options_data_url = 'https://www.nseindia.com/content/historical/DERIVATIVES/{2}/{1}/fo{0}{1}{2}bhav.csv.zip'.format(*tu)
		self.open_interest_combined_url = 'https://www.nseindia.com/archives/nsccl/mwpl/combineoi_{0}{3}{2}.zip'.format(*tu)
		self.equity_delivery_url = 'https://www.nseindia.com/archives/equities/mto/MTO_{0}{3}{2}.DAT'.format(*tu)

	def download_data(self, data_type: DataType, output_path: str):
		if data_type == DataType.CASH_MARKET:
			url = self.cash_market_url
		elif data_type == DataType.FUTURE_OPTIONS:
			url = self.future_options_data_url
		elif data_type == DataType.OPEN_INTEREST_COMBINED:
			url = self.open_interest_combined_url
		elif data_type == DataType.EQUITY_DELIVERY:
			url = self.equity_delivery_url
		
		response = requests.get(url, stream=True)
		with open(output_path, 'wb') as f:
			for chunk in response.iter_content(chunk_size=1024):
				if chunk:
					f.write(chunk)

def main():
    tu = getCurrentDateTime()
    downloader = NSEDataDownloader()
    downloader.download_data(DataType.CASH_MARKET, 'output/cash_market_data_{0}_{1}_{2}.zip'.format(*tu))
    downloader.download_data(DataType.FUTURE_OPTIONS, 'output/future_options_data_{0}_{1}_{2}.zip'.format(*tu))
    downloader.download_data(DataType.OPEN_INTEREST_COMBINED, 'output/open_interest_combined_data_{0}_{1}_{2}.zip'.format(*tu))
    downloader.download_data(DataType.EQUITY_DELIVERY, 'output/equity_delivery_data_{0}_{1}_{2}.DAT'.format(*tu))	
 
if __name__ == '__main__':
	main()