import requests
import csv
import pandas as pd
from datetime import datetime as dt

class trader:
    '''The trader provides the stock symbol'''
    def __init__(self, symbol):
        self.symbol = symbol
    
    
class broker(trader):
    '''The broker provides quotations for a stock asked by the trader after it is given the necessary info'''
    
    #1
    def __init__(self, symbol, timeseries, interval, outputsize, key):
        trader.__init__(self, symbol)
        self.timeseries = timeseries
        self.interval = interval
        self.outputsize = outputsize
        self.key = key
        print 'Broker is providing quotation for: {}'.format(self.symbol)
        
        if self.timeseries == 'TIME_SERIES_INTRADAY':
            print 'Chart type: {}, Interval: {} min'.format(self.timeseries, self.interval)
        else:
            print 'Chart type: {}'.format(self.timeseries, self.interval)
            
        print
        
    #2    
    def create_url(self):
        url = "https://www.alphavantage.co/query?"
        function = "function=" + self.timeseries
        symbol= "&symbol=" + self.symbol
        
        if self.timeseries == 'TIME_SERIES_INTRADAY':
            Interval =  '&interval=' + self.interval + 'min'
            
        elif self.timeseries == 'TIME_SERIES_DAILY':
            Interval = ''
            
        elif self.timeseries == 'TIME_SERIES_WEEKLY':
            Interval = ''
            outputsize = ''
            
        elif self.timeseries == 'TIME_SERIES_MONTHLY':
            Interval = ''
            outputsize = ''
        
        else:
            raise TypeError('The timeseries you entered is not supported.')
            
        APIkey = "&apikey=" + self.key
        
        # Piece together the URL for the API call
        URL = url + function + symbol + Interval + outputsize + APIkey
        #print URL
        
        return URL
       
    #3     
    def jsonify_quote(self):
        URL = self.create_url()
        quote = requests.get(URL)
        quote_json = quote.json()

        if self.timeseries == 'TIME_SERIES_INTRADAY':
            quote_json = quote_json['Time Series (' + self.interval + 'min)']
            
        elif self.timeseries == 'TIME_SERIES_DAILY':
            quote_json = quote_json['Time Series (Daily)']
            
        elif self.timeseries == 'TIME_SERIES_WEEKLY':
            quote_json = quote_json['Weekly Time Series']
            
        elif self.timeseries == 'TIME_SERIES_MONTHLY':
            quote_json = quote_json['Monthly Time Series']
        
        else:
            raise TypeError('The timeseries you entered is not supported.')
        
        return quote_json


class parser(trader, broker):
    '''The parser parses the quote provided by the broker and transforms it into a pandas dataframe'''
    
    #1
    def __init__(self,  symbol):
        trader.__init__(self, symbol)        
        #print "Storing quote for '{}' in a dataframe".format(self.symbol)
        
    
    #2    
    def store_quote(self, symbol, timeseries, interval, outputsize, key):
        broker.__init__(self, symbol, timeseries, interval, outputsize, key)
        parsed_data = self.jsonify_quote()
        data = pd.DataFrame(columns=['Date','Volume','Open','High','Low','Close'])
        
        for d, p in parsed_data.items():   # d = date, p = price
            
            if self.timeseries == 'TIME_SERIES_INTRADAY':
                date = dt.strptime(d, '%Y-%m-%d %H:%M:%S')
            else:
                date = dt.strptime(d, '%Y-%m-%d')
                
            data_row = [date,int(p['5. volume']),float(p['1. open']),float(p['2. high']),float(p['3. low']),float(p['4. close'])]
            data.loc[-1,:] = data_row
            data.index=data.index + 1
        
        data=data.sort_values('Date', ascending=False)
        data.set_index('Date', inplace=True)
        
        return data
        
    
    #3 get quote for a single symbol   
    def quote_to_csv(self, outfile, symbol, timeseries, interval, outputsize, key):
        nice_data = parser.store_quote(self, symbol, timeseries, interval, outputsize, key)
        nice_data.to_csv(outfile)
        
        return nice_data
        
    
    #4 get quote for multiple symbols from a watchlist
    def watchlist_to_csv (self, infile, outfilepath, timeseries, interval, outputsize, key):
        watchlist = csv.reader(open(infile))
                
        # Export quote to csv
        for s in watchlist:
            symbol = s[0]
            
            if timeseries == 'TIME_SERIES_INTRADAY':
                outfile_fullpath = outfilepath + symbol + '_' + timeseries + '_' + interval + '.csv'
            else:
                outfile_fullpath = outfilepath + symbol + '_' + timeseries + '.csv'
                
            nice_data = parser.store_quote(self, symbol, timeseries, interval, outputsize, key)
            nice_data.to_csv(outfile_fullpath)
            
        return nice_data
        
        
    #5
