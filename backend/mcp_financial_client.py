"""
MCP Client for Financial Data
Uses Model Context Protocol to fetch stock data from MCP servers
"""

import asyncio
import json
from typing import Optional, Dict, Any
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class MCPFinancialClient:
    """Client to interact with financial data MCP servers"""
    
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.server_params = None
        
    async def connect(self, server_command: str, server_args: list = None):
        """Connect to an MCP server"""
        try:
            self.server_params = StdioServerParameters(
                command=server_command,
                args=server_args or [],
                env=None
            )
            
            # Create client session
            async with stdio_client(self.server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    self.session = session
                    
                    # Initialize the connection
                    await session.initialize()
                    
                    # List available tools
                    tools = await session.list_tools()
                    print(f"✓ Connected to MCP server")
                    print(f"  Available tools: {[tool.name for tool in tools.tools]}")
                    
                    return session
        except Exception as e:
            print(f"✗ MCP connection failed: {e}")
            return None
    
    async def get_stock_quote(self, ticker: str) -> Optional[Dict[str, Any]]:
        """Get stock quote using MCP server"""
        try:
            if not self.session:
                print("✗ MCP session not initialized")
                return None
            
            # Call the MCP tool
            result = await self.session.call_tool(
                "get_stock_quote",
                arguments={"symbol": ticker}
            )
            
            if result.content:
                # Parse the result
                data = json.loads(result.content[0].text)
                return self._format_quote_data(data)
            
            return None
            
        except Exception as e:
            print(f"✗ MCP get_stock_quote failed: {e}")
            return None
    
    async def get_historical_data(self, ticker: str, days: int = 365) -> Optional[Dict[str, Any]]:
        """Get historical stock data using MCP server"""
        try:
            if not self.session:
                print("✗ MCP session not initialized")
                return None
            
            # Call the MCP tool
            result = await self.session.call_tool(
                "get_historical_data",
                arguments={
                    "symbol": ticker,
                    "period": f"{days}d"
                }
            )
            
            if result.content:
                # Parse the result
                data = json.loads(result.content[0].text)
                return self._format_historical_data(data)
            
            return None
            
        except Exception as e:
            print(f"✗ MCP get_historical_data failed: {e}")
            return None
    
    def _format_quote_data(self, data: Dict) -> Dict[str, Any]:
        """Format MCP quote data to match our app's format"""
        return {
            'symbol': data.get('symbol'),
            'price': data.get('price'),
            'open': data.get('open'),
            'previousClose': data.get('previousClose'),
            'change': data.get('change'),
            'changePercent': data.get('changePercent'),
            'dayHigh': data.get('high'),
            'dayLow': data.get('low'),
            'volume': data.get('volume'),
            'marketCap': data.get('marketCap'),
            'pe': data.get('pe'),
            'eps': data.get('eps'),
            'fiftyTwoWeekHigh': data.get('fiftyTwoWeekHigh'),
            'fiftyTwoWeekLow': data.get('fiftyTwoWeekLow'),
            'avgVolume': data.get('avgVolume'),
            'source': 'MCP Server'
        }
    
    def _format_historical_data(self, data: Dict) -> Dict[str, Any]:
        """Format MCP historical data to match our app's format"""
        return {
            'timestamps': data.get('timestamps', []),
            'close': data.get('close', []),
            'open': data.get('open', []),
            'high': data.get('high', []),
            'low': data.get('low', []),
            'volume': data.get('volume', []),
            'source': 'MCP Server'
        }


# Synchronous wrapper for Flask
class MCPFinancialClientSync:
    """Synchronous wrapper for MCP client to use in Flask"""
    
    def __init__(self, server_command: str = "uvx", server_args: list = None):
        self.server_command = server_command
        self.server_args = server_args or ["mcp-server-fetch"]
        self.client = MCPFinancialClient()
    
    def get_stock_quote(self, ticker: str) -> Optional[Dict[str, Any]]:
        """Synchronous wrapper for get_stock_quote using fetch tool"""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            async def _get_quote():
                async with stdio_client(
                    StdioServerParameters(
                        command=self.server_command,
                        args=self.server_args,
                        env=None
                    )
                ) as (read, write):
                    async with ClientSession(read, write) as session:
                        await session.initialize()
                        
                        # Use fetch tool to get data from Yahoo Finance
                        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
                        result = await session.call_tool(
                            "fetch",
                            arguments={"url": url}
                        )
                        
                        if result.content:
                            # Parse Yahoo Finance response
                            content = result.content[0].text
                            
                            # Extract JSON from markdown (mcp-server-fetch wraps JSON in markdown)
                            import re
                            json_start = content.find('{"chart":')
                            if json_start == -1:
                                print(f"✗ No JSON found in MCP response")
                                return None
                            
                            # MCP may truncate the response, but we only need the meta section
                            # which is at the beginning. Extract just what we need.
                            json_str = content[json_start:]
                            
                            # Find the meta section
                            meta_start = json_str.find('"meta":{')
                            if meta_start == -1:
                                print(f"✗ No meta section found")
                                return None
                            
                            # Find the end of the meta section (next top-level key or end of result)
                            # Meta section ends at "timestamp" key
                            timestamp_pos = json_str.find(',"timestamp":', meta_start)
                            if timestamp_pos == -1:
                                print(f"✗ Could not find end of meta section")
                                return None
                            
                            # Extract just the meta section
                            meta_json = json_str[meta_start:timestamp_pos] + '}'
                            meta_json = '{' + meta_json  # Wrap in braces
                            
                            try:
                                meta_data = json.loads(meta_json)
                                meta = meta_data['meta']
                                
                                price = meta.get('regularMarketPrice')
                                prev_close = meta.get('previousClose', price)
                                
                                return {
                                    'symbol': meta.get('symbol', ticker),
                                    'price': price,
                                    'open': meta.get('regularMarketOpen', price),
                                    'previousClose': prev_close,
                                    'change': price - prev_close if price and prev_close else 0,
                                    'changePercent': ((price - prev_close) / prev_close * 100) if price and prev_close else 0,
                                    'dayHigh': meta.get('regularMarketDayHigh', price),
                                    'dayLow': meta.get('regularMarketDayLow', price),
                                    'volume': meta.get('regularMarketVolume', 0),
                                    'marketCap': None,
                                    'pe': None,
                                    'eps': None,
                                    'fiftyTwoWeekHigh': meta.get('fiftyTwoWeekHigh', price),
                                    'fiftyTwoWeekLow': meta.get('fiftyTwoWeekLow', price),
                                    'avgVolume': None,
                                    'source': 'MCP Server (Yahoo Finance)'
                                }
                            except json.JSONDecodeError as e:
                                print(f"✗ JSON parse error: {e}")
                                return None
                        return None
            
            return loop.run_until_complete(_get_quote())
        except Exception as e:
            print(f"✗ MCP sync get_stock_quote failed: {e}")
            return None
        finally:
            loop.close()
    
    def get_historical_data(self, ticker: str, days: int = 365) -> Optional[Dict[str, Any]]:
        """Synchronous wrapper for get_historical_data using fetch tool"""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            async def _get_historical():
                async with stdio_client(
                    StdioServerParameters(
                        command=self.server_command,
                        args=self.server_args,
                        env=None
                    )
                ) as (read, write):
                    async with ClientSession(read, write) as session:
                        await session.initialize()
                        
                        # Use fetch tool to get data from Yahoo Finance
                        # Calculate date range
                        from datetime import datetime, timedelta
                        end_date = datetime.now()
                        start_date = end_date - timedelta(days=days)
                        
                        period1 = int(start_date.timestamp())
                        period2 = int(end_date.timestamp())
                        
                        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?period1={period1}&period2={period2}&interval=1d"
                        
                        result = await session.call_tool(
                            "fetch",
                            arguments={"url": url}
                        )
                        
                        if result.content:
                            # Parse Yahoo Finance response
                            content = result.content[0].text
                            
                            # Extract JSON from markdown (mcp-server-fetch wraps JSON in markdown)
                            import re
                            json_start = content.find('{"chart":')
                            if json_start == -1:
                                print(f"✗ No JSON found in MCP response")
                                return None
                            
                            json_str = content[json_start:]
                            
                            # Find matching closing brace
                            brace_count = 0
                            end_idx = -1
                            for i, char in enumerate(json_str):
                                if char == '{':
                                    brace_count += 1
                                elif char == '}':
                                    brace_count -= 1
                                    if brace_count == 0:
                                        end_idx = i + 1
                                        break
                            
                            if end_idx == -1:
                                print(f"✗ Incomplete JSON in MCP response (brace count: {brace_count})")
                                return None
                            
                            json_str = json_str[:end_idx]
                            
                            try:
                                data = json.loads(json_str)
                            except json.JSONDecodeError as e:
                                print(f"✗ JSON parse error: {e}")
                                return None
                            
                            # Extract historical data from Yahoo Finance format
                            if 'chart' in data and 'result' in data['chart']:
                                chart_result = data['chart']['result'][0]
                                timestamps = chart_result.get('timestamp', [])
                                quotes = chart_result.get('indicators', {}).get('quote', [{}])[0]
                                
                                return {
                                    'timestamps': timestamps,
                                    'close': quotes.get('close', []),
                                    'open': quotes.get('open', []),
                                    'high': quotes.get('high', []),
                                    'low': quotes.get('low', []),
                                    'volume': quotes.get('volume', []),
                                    'source': 'MCP Server (Yahoo Finance)'
                                }
                        return None
            
            return loop.run_until_complete(_get_historical())
        except Exception as e:
            print(f"✗ MCP sync get_historical_data failed: {e}")
            return None
        finally:
            loop.close()

    def _extract_json_from_markdown(self, content: str) -> Optional[Dict]:
        """Extract JSON from markdown-wrapped response"""
        json_start = content.find('{"chart":')
        if json_start == -1:
            print(f"✗ No JSON found in MCP response")
            return None

        json_str = content[json_start:]

        # Find matching closing brace - handle nested structures and strings
        brace_count = 0
        end_idx = -1
        in_string = False
        escape_next = False

        for i, char in enumerate(json_str):
            if escape_next:
                escape_next = False
                continue

            if char == '\\':
                escape_next = True
                continue

            if char == '"' and not escape_next:
                in_string = not in_string
                continue

            if not in_string:
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        end_idx = i + 1
                        break

        if end_idx == -1:
            print(f"✗ Incomplete JSON in MCP response (brace count: {brace_count})")
            return None

        json_str = json_str[:end_idx]

        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"✗ JSON parse error: {e}")
            return None

