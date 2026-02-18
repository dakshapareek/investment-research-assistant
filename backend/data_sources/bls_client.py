import requests
from datetime import datetime
from config import BLS_API_KEY, BLS_CPI_SERIES, BLS_UNEMPLOYMENT_SERIES

class BLSClient:
    BASE_URL = 'https://api.bls.gov/publicAPI/v2/timeseries/data/'
    
    def __init__(self):
        self.api_key = BLS_API_KEY
    
    def fetch_series(self, series_id, start_year=None, end_year=None):
        """Fetch BLS time series data"""
        if not start_year:
            start_year = datetime.now().year - 1
        if not end_year:
            end_year = datetime.now().year
        
        payload = {
            'seriesid': [series_id],
            'startyear': str(start_year),
            'endyear': str(end_year)
        }
        
        if self.api_key:
            payload['registrationkey'] = self.api_key
        
        response = requests.post(self.BASE_URL, json=payload)
        response.raise_for_status()
        return response.json()
    
    def get_macro_data(self):
        """Get CPI and Unemployment data"""
        cpi_data = self.fetch_series(BLS_CPI_SERIES)
        unemployment_data = self.fetch_series(BLS_UNEMPLOYMENT_SERIES)
        
        return {
            'cpi': self._parse_latest(cpi_data),
            'unemployment': self._parse_latest(unemployment_data)
        }
    
    def _parse_latest(self, data):
        """Extract latest value from BLS response"""
        try:
            series = data['Results']['series'][0]
            latest = series['data'][0]
            return {
                'value': float(latest['value']),
                'period': latest['period'],
                'year': latest['year']
            }
        except (KeyError, IndexError):
            return None
