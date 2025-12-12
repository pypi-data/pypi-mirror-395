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
    
    def batch(self, urls, batch_size=20, timeout=30, save_to=None):
        """
        Process URLs in BATCHES - memory efficient, auto-saves progress!
        
        Perfect for large datasets (200+ URLs). Processes in chunks, saves progressively.
        
        Args:
            urls (list): List of URLs to fetch
            batch_size (int): How many URLs per batch (default: 20)
            timeout (int): Timeout per request (default: 30)
            save_to (str): Optional file to save results (auto-appends each batch)
            
        Returns:
            list: Complete list of all fetched data
            
        Example:
            >>> # Process 200 URLs in batches of 25
            >>> results = get.many.batch(urls, 25)
            
            >>> # With auto-save
            >>> results = get.many.batch(urls, 25, save_to="pokemon_data")
            
        Why batching?
        - Memory efficient: Doesn't load all 200 at once
        - Progress saving: Won't lose data if it crashes
        - Better control: Can monitor progress
        - Network friendly: Doesn't overwhelm servers
        """
        from simple_file import save as sf_save, exists, load
        
        all_results = []
        total_batches = (len(urls) + batch_size - 1) // batch_size
        
        print(f"🚀 Processing {len(urls)} URLs in {total_batches} batches of {batch_size}")
        
        for batch_num in range(0, len(urls), batch_size):
            batch_urls = urls[batch_num:batch_num + batch_size]
            current_batch = (batch_num // batch_size) + 1
            
            print(f"📦 Batch {current_batch}/{total_batches}: Fetching {len(batch_urls)} URLs...")
            
            # Fetch this batch
            batch_results = asyncio.run(self._fetch_many(batch_urls, timeout))
            all_results.extend(batch_results)
            
            # Save progress if file specified
            if save_to:
                if batch_num == 0:
                    # First batch: create new file
                    sf_save(save_to, batch_results)
                    print(f"💾 Saved batch {current_batch} to {save_to}")
                else:
                    # Subsequent batches: append to existing
                    existing_data = load(save_to)
                    if isinstance(existing_data, list):
                        existing_data.extend(batch_results)
                    else:
                        existing_data = [existing_data] + batch_results
                    sf_save(save_to, existing_data)
                    print(f"💾 Appended batch {current_batch} to {save_to}")
            
            print(f"✅ Batch {current_batch} complete! ({len(all_results)}/{len(urls)} total)")
        
        print(f"🎉 All done! Processed {len(all_results)} URLs")
        return all_results
    
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

