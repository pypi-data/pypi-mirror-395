"""
The Getter - Gets data from the internet, YOUR way
"""
import httpx
import asyncio
from .converter import to_json

class DataGetter:
    """Gets data and always returns JSON"""
    
    def data(self, url, timeout=30):
        """
        Get data from ONE URL, returns JSON
        
        Args:
            url (str): The URL to fetch
            timeout (int): How long to wait in seconds (default: 30)
            
        Returns:
            dict: Clean JSON data, always
        """
        try:
            response = httpx.get(url, timeout=timeout, follow_redirects=True)
            
            if response.status_code != 200:
                return {
                    "error": True,
                    "status_code": response.status_code,
                    "message": f"HTTP {response.status_code}: Failed to get data from {url}",
                    "url": url
                }
            
            content_type = response.headers.get('content-type', 'text/plain')
            json_data = to_json(response.content, content_type)
            
            if not isinstance(json_data, dict):
                json_data = {"data": json_data}
            
            return json_data
            
        except httpx.TimeoutException:
            return {
                "error": True,
                "message": f"Request timeout after {timeout} seconds",
                "url": url
            }
        except httpx.RequestError as e:
            return {
                "error": True,
                "message": f"Network error: {str(e)}",
                "url": url
            }
        except Exception as e:
            return {
                "error": True,
                "message": f"Unexpected error: {str(e)}",
                "url": url
            }
    
    def many(self, urls, timeout=30):
        """
        Get data from MANY URLs at once (10x faster!)
        
        Args:
            urls (list): List of URLs to fetch
            timeout (int): How long to wait per request
            
        Returns:
            list: List of JSON data (one per URL)
            
        Example:
            >>> from internet import *
            >>> urls = ["url1", "url2", "url3"]
            >>> results = get.many(urls)
            >>> for data in results:
            ...     print(data['name'])
        """
        return asyncio.run(self._fetch_many(urls, timeout))
    
    async def _fetch_many(self, urls, timeout):
        """Internal async function to fetch multiple URLs"""
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
            tasks = [self._fetch_one(client, url) for url in urls]
            return await asyncio.gather(*tasks)
    
    async def _fetch_one(self, client, url):
        """Internal async function to fetch one URL"""
        try:
            response = await client.get(url)
            
            if response.status_code != 200:
                return {
                    "error": True,
                    "status_code": response.status_code,
                    "message": f"HTTP {response.status_code}: Failed",
                    "url": url
                }
            
            content_type = response.headers.get('content-type', 'text/plain')
            json_data = to_json(response.content, content_type)
            
            if not isinstance(json_data, dict):
                json_data = {"data": json_data}
            
            return json_data
            
        except Exception as e:
            return {
                "error": True,
                "message": f"Error: {str(e)}",
                "url": url
            }

# Create the singleton instance
get = DataGetter()
