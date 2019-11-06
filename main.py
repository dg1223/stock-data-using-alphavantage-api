import broker as bk


APIkey = raw_input("Copy/paste your API key here: ")
print

# Initialize broker
#quote = bk.broker('LGO.TO', 'TIME_SERIES_INTRADAY', '1', 'full', APIkey)
#q = quote.()

symbol = 'LGO.TO'
timeseries = 'TIME_SERIES_MONTHLY'
interval = '60'
outputsize = 'full'


filepath = 'D:\Trading\API'
filename = 'TSX_test.csv'
infile = filepath + '\\' + filename
outfile = filepath + '\\' + 'test\\' + symbol + '.csv'
outfilepath = filepath + '\\' + 'test\\'


quote = bk.parser(symbol)
#quote.quote_to_csv(outfile, symbol, timeseries, interval, outputsize, APIkey)
quote.watchlist_to_csv (infile, outfilepath, timeseries, interval, outputsize, APIkey)

#print
#print nice_data