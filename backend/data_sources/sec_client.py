import requests
from bs4 import BeautifulSoup
import re
import time

class SECClient:
    BASE_URL = 'https://www.sec.gov'
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'InvestmentResearch research@example.com',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'www.sec.gov'
        }
    
    def get_latest_filing(self, ticker, filing_type='10-K'):
        """Get latest 10-K or 10-Q filing"""
        try:
            print(f"Fetching SEC filing for {ticker}...")
            
            # Try to get CIK
            cik = self._get_cik(ticker)
            if not cik:
                print(f"✗ Could not find CIK for {ticker}")
                return self._get_fallback_data(ticker)
            
            print(f"✓ Found CIK: {cik}")
            
            # Try 10-K first, then 10-Q
            filing_data = self._fetch_filing(cik, '10-K')
            if not filing_data or filing_data.get('risk_factors') == 'N/A':
                print("10-K not found, trying 10-Q...")
                filing_data = self._fetch_filing(cik, '10-Q')
            
            if filing_data and filing_data.get('risk_factors') != 'N/A':
                print(f"✓ Successfully retrieved SEC filing")
                return filing_data
            
            print(f"✗ No valid filings found for {ticker}")
            return self._get_fallback_data(ticker)
            
        except Exception as e:
            print(f"✗ SEC filing error for {ticker}: {e}")
            return self._get_fallback_data(ticker)
    
    def _fetch_filing(self, cik, filing_type):
        """Fetch specific filing type"""
        try:
            filings_url = f'{self.BASE_URL}/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type={filing_type}&count=1'
            response = requests.get(filings_url, headers=self.headers, timeout=10)
            
            if response.status_code != 200:
                print(f"✗ SEC returned status {response.status_code}")
                return None
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            doc_link = soup.find('a', {'id': 'documentsbutton'})
            if not doc_link:
                return None
            
            time.sleep(0.1)  # Be nice to SEC servers
            return self._extract_filing_text(doc_link['href'])
            
        except Exception as e:
            print(f"✗ Error fetching {filing_type}: {e}")
            return None
    
    def _get_cik(self, ticker):
        """Get CIK from ticker"""
        try:
            # Method 1: Try SEC's company tickers JSON (more reliable)
            try:
                tickers_url = 'https://www.sec.gov/files/company_tickers.json'
                response = requests.get(tickers_url, headers=self.headers, timeout=10)
                if response.status_code == 200:
                    tickers_data = response.json()
                    ticker_upper = ticker.upper()
                    for item in tickers_data.values():
                        if item.get('ticker', '').upper() == ticker_upper:
                            cik = str(item.get('cik_str', '')).zfill(10)
                            print(f"✓ Found CIK via JSON API: {cik}")
                            return cik
            except Exception as e:
                print(f"JSON API method failed: {e}")
            
            # Method 2: Try the company search endpoint (fallback)
            url = f'{self.BASE_URL}/cgi-bin/browse-edgar?company={ticker}&action=getcompany'
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code != 200:
                return None
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for CIK in multiple ways
            cik_elem = soup.find('span', text=re.compile('CIK'))
            if cik_elem:
                cik_link = cik_elem.find_next('a')
                if cik_link:
                    return cik_link.text.strip()
            
            # Alternative: look for CIK in the page
            cik_match = re.search(r'CIK=(\d+)', response.text)
            if cik_match:
                return cik_match.group(1)
            
            return None
            
        except Exception as e:
            print(f"✗ Error getting CIK: {e}")
            return None
    
    def _extract_filing_text(self, doc_url):
        """Extract key sections from filing"""
        try:
            full_url = f'{self.BASE_URL}{doc_url}'
            response = requests.get(full_url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the actual document link
            doc_table = soup.find('table', {'class': 'tableFile'})
            if doc_table:
                htm_link = doc_table.find('a', href=re.compile(r'\.htm'))
                if htm_link:
                    time.sleep(0.1)  # Be nice to SEC servers
                    doc_response = requests.get(f"{self.BASE_URL}{htm_link['href']}", headers=self.headers, timeout=10)
                    return self._parse_sections(doc_response.text)
            
            return {'risk_factors': 'N/A', 'mda': 'N/A'}
            
        except Exception as e:
            print(f"✗ Error extracting filing text: {e}")
            return {'risk_factors': 'N/A', 'mda': 'N/A'}
    
    def _parse_sections(self, html_text):
        """Parse Risk Factors and MD&A sections"""
        try:
            soup = BeautifulSoup(html_text, 'html.parser')
            text = soup.get_text()
            
            # Clean up text
            text = re.sub(r'\s+', ' ', text)
            
            risk_match = re.search(r'RISK FACTORS(.*?)(?:ITEM|PART|$)', text, re.DOTALL | re.IGNORECASE)
            mda_match = re.search(r'MANAGEMENT.*?DISCUSSION.*?ANALYSIS(.*?)(?:ITEM|PART|$)', text, re.DOTALL | re.IGNORECASE)
            
            risk_text = 'N/A'
            mda_text = 'N/A'
            
            if risk_match:
                risk_text = risk_match.group(1).strip()[:1500]
                if len(risk_text) > 100:
                    risk_text = risk_text[:1500] + '...'
            
            if mda_match:
                mda_text = mda_match.group(1).strip()[:1500]
                if len(mda_text) > 100:
                    mda_text = mda_text[:1500] + '...'
            
            return {
                'risk_factors': risk_text,
                'mda': mda_text
            }
            
        except Exception as e:
            print(f"✗ Error parsing sections: {e}")
            return {'risk_factors': 'N/A', 'mda': 'N/A'}
    
    def _get_fallback_data(self, ticker):
        """Provide fallback data when SEC filing unavailable"""
        return {
            'risk_factors': f'SEC filing data temporarily unavailable for {ticker}. Common risks include market volatility, regulatory changes, competition, and economic conditions. Please check SEC EDGAR directly at sec.gov for detailed risk factors.',
            'mda': f'Management discussion and analysis not available. For detailed financial analysis and management commentary, please visit the SEC EDGAR database at sec.gov and search for {ticker} 10-K or 10-Q filings.'
        }
