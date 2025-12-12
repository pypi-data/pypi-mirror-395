"""
The Getter - Gets data from the internet, YOUR way
"""
import httpx
import asyncio
import time
import json
from datetime import datetime
from pathlib import Path
from .converter import to_json

class DataGetter:
    """Gets data and always returns JSON"""
    
    def _extract_urls_smart(self, data):
        """
        🔮 MEGA SUPERPOWER - Extract URLs from ANY format in the world!
        
        Handles:
        - String URL: "https://example.com" → ["https://example.com"]
        - List of strings: ["url1", "url2"] → ["url1", "url2"]
        - List of dicts: [{"url": "..."}, {"url": "..."}] → ["url1", "url2"]
        - Single dict: {"url": "..."} → ["url1"]
        - JSON string: '{"url": "..."}' → ["url1"]
        - Mixed formats: [{"url": "..."}, "url2"] → ["url1", "url2"]
        - Nested structures: [{"data": {"url": "..."}}] → ["url1"]
        - File paths: Loads JSON/txt files and extracts URLs
        
        Returns:
            list: List of URL strings (always a list, even for single URL)
        """
        import json as json_module
        from pathlib import Path
        
        # Handle None/empty
        if data is None:
            return []
        
        # Handle string - could be URL, JSON string, or file path
        if isinstance(data, str):
            # Check if it's a file path
            if Path(data).exists():
                try:
                    # Try loading as JSON
                    with open(data, 'r') as f:
                        content = f.read().strip()
                        if content.startswith('{') or content.startswith('['):
                            data = json_module.loads(content)
                        else:
                            # Plain text file - treat each line as URL
                            return [line.strip() for line in content.split('\n') if line.strip() and line.strip().startswith('http')]
                except:
                    # Not a valid file or can't parse - treat as URL
                    pass
            
            # Check if it's JSON string
            if data.strip().startswith('{') or data.strip().startswith('['):
                try:
                    data = json_module.loads(data)
                except:
                    # Not valid JSON - treat as URL
                    return [data] if data.startswith('http') else []
            
            # It's a plain URL string
            if data.startswith('http'):
                return [data]
            return []
        
        # Handle list
        if isinstance(data, list):
            urls = []
            for item in data:
                extracted = self._extract_urls_smart(item)
                urls.extend(extracted)
            return urls
        
        # Handle dict
        if isinstance(data, dict):
            # Priority 1: Direct 'url' key
            if 'url' in data:
                url_value = data['url']
                if isinstance(url_value, str) and url_value.startswith('http'):
                    return [url_value]
                # If url is nested, recurse
                if isinstance(url_value, (dict, list)):
                    return self._extract_urls_smart(url_value)
            
            # Priority 2: Common URL key variations
            for key in ['urls', 'link', 'links', 'endpoint', 'endpoints', 'href', 'src']:
                if key in data:
                    extracted = self._extract_urls_smart(data[key])
                    if extracted:
                        return extracted
            
            # Priority 3: Search all string values for URLs
            for value in data.values():
                if isinstance(value, str) and value.startswith('http'):
                    return [value]
                # Recurse into nested structures
                if isinstance(value, (dict, list)):
                    extracted = self._extract_urls_smart(value)
                    if extracted:
                        return extracted
        
        # Handle other types (int, float, etc.) - skip
        return []
    
    def _extract_single_url(self, data):
        """
        Extract single URL from any format (for get.data())
        
        Returns:
            str: Single URL string, or None if not found
        """
        urls = self._extract_urls_smart(data)
        return urls[0] if urls else None
    
    def _get_smart_timeout_multiplier(self, error_dict):
        """
        Smart timeout multiplier based on error type
        
        Returns multiplier for timeout increase:
        - Timeout errors: 2x (server slow)
        - 429 (rate limit): 3x (need to wait longer)
        - 500 errors: 2x (server issues)
        - Network errors: 1.5x (connection issues)
        - 404 errors: 1x (no point, but we'll try)
        - Other 4xx: 1.5x (might be temporary)
        """
        status_code = error_dict.get('status_code')
        message = error_dict.get('message', '').lower()
        
        if status_code == 429:
            return 3.0  # Rate limit - wait much longer
        elif status_code and status_code >= 500:
            return 2.0  # Server errors - give more time
        elif 'timeout' in message:
            return 2.0  # Timeout - server slow
        elif 'network' in message or 'connection' in message:
            return 1.5  # Network issues - moderate increase
        elif status_code == 404:
            return 1.0  # Not found - no point but try once
        elif status_code and 400 <= status_code < 500:
            return 1.5  # Client errors - might be temporary
        else:
            return 2.0  # Default - double timeout
    
    def _save_failed_url(self, url, error_dict, retries_attempted, save_to=None):
        """Save failed URL to per-file error tracking in failures_and_errors/ folder"""
        if not save_to:
            return  # No save_to specified, skip error saving

        error_folder = Path("failures_and_errors")
        error_folder.mkdir(exist_ok=True)

        # Create smart filename: save_to_failure_and_error, save_to(new)_failure_and_error, etc.
        base_name = f"{save_to}_failure_and_error"
        json_file = error_folder / f"{base_name}.json"
        txt_file = error_folder / f"{base_name}.txt"

        # If file exists, create numbered versions
        counter = 0
        while json_file.exists():
            if counter == 0:
                new_name = f"{save_to}(new)_failure_and_error"
            else:
                new_name = f"{save_to}(new_{counter})_failure_and_error"
            json_file = error_folder / f"{new_name}.json"
            txt_file = error_folder / f"{new_name}.txt"
            counter += 1

        error_entry = {
            "url": url,
            "error": error_dict.get('message', 'Unknown error'),
            "retries_attempted": retries_attempted,
            "last_status_code": error_dict.get('status_code'),
            "timestamp": datetime.now().isoformat(),
            "batch_file": save_to
        }

        # This is a new error file, so start with empty list
        errors = [error_entry]

        # Save JSON
        with open(json_file, 'w') as f:
            json.dump(errors, f, indent=2)

        # Save TXT with comments
        with open(txt_file, 'w') as f:
            f.write(f"# Failed URLs for batch file: {save_to}\n")
            f.write("# Failed URLs after max retries\n")
            f.write("# Format: URL | Error | Retries Attempted | Status Code\n\n")
            for err in errors:
                status = err.get('last_status_code', 'null')
                f.write(f"{err['url']} | {err['error']} | {err['retries_attempted']} | {status}\n")
    
    def _remove_recovered_url(self, url, save_to=None):
        """Remove successfully recovered URL from per-file error tracking"""
        if not save_to:
            return  # No save_to specified, skip

        error_folder = Path("failures_and_errors")
        if not error_folder.exists():
            return

        # Find the most recent error file for this save_to
        base_name = f"{save_to}_failure_and_error"
        json_file = None
        txt_file = None

        # Check for exact match first
        exact_json = error_folder / f"{base_name}.json"
        if exact_json.exists():
            json_file = exact_json
            txt_file = error_folder / f"{base_name}.txt"
        else:
            # Look for (new) variants, get the most recent one
            error_files = list(error_folder.glob(f"{save_to}*failure_and_error.json"))
            if error_files:
                # Sort by modification time, get most recent
                error_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                json_file = error_files[0]
                txt_base = json_file.stem  # Remove .json extension
                txt_file = error_folder / f"{txt_base}.txt"

        if not json_file or not json_file.exists():
            return

        try:
            with open(json_file, 'r') as f:
                errors = json.load(f)
        except:
            return

        # Remove URL
        original_count = len(errors)
        errors = [e for e in errors if e.get('url') != url]

        # If no errors left, delete the files
        if not errors:
            try:
                json_file.unlink()
                if txt_file and txt_file.exists():
                    txt_file.unlink()
            except:
                pass
            return

        # Save updated JSON
        with open(json_file, 'w') as f:
            json.dump(errors, f, indent=2)

        # Update TXT
        if txt_file:
            batch_file = errors[0].get('batch_file', save_to) if errors else save_to
            with open(txt_file, 'w') as f:
                f.write(f"# Failed URLs for batch file: {batch_file}\n")
                f.write("# Failed URLs after max retries\n")
                f.write("# Format: URL | Error | Retries Attempted | Status Code\n\n")
                for err in errors:
                    status = err.get('last_status_code', 'null')
                    f.write(f"{err['url']} | {err['error']} | {err['retries_attempted']} | {status}\n")
    
    def _get_smart_diagnostics(self, errors):
        """Generate smart diagnostics based on error patterns"""
        if not errors:
            return []
        
        diagnostics = []
        
        # Group by error type
        status_codes = {}
        error_types = {}
        
        for err in errors:
            status = err.get('last_status_code')
            error_msg = err.get('error', '').lower()
            
            if status:
                status_codes[status] = status_codes.get(status, 0) + 1
            
            if 'timeout' in error_msg:
                error_types['timeout'] = error_types.get('timeout', 0) + 1
            elif 'network' in error_msg or 'connection' in error_msg:
                error_types['network'] = error_types.get('network', 0) + 1
            elif '404' in error_msg or status == 404:
                error_types['404'] = error_types.get('404', 0) + 1
            elif status == 429:
                error_types['rate_limit'] = error_types.get('rate_limit', 0) + 1
            elif status and status >= 500:
                error_types['server_error'] = error_types.get('server_error', 0) + 1
        
        # Generate suggestions
        if error_types.get('404', 0) > 0:
            count = error_types['404']
            diagnostics.append(f"• {count} URL(s) returning 404 - These endpoints don't exist")
            diagnostics.append("  Suggestion: Check if URLs/IDs are valid")
        
        if error_types.get('timeout', 0) > 0:
            count = error_types['timeout']
            diagnostics.append(f"• {count} URL(s) timing out - Server might be slow or down")
            diagnostics.append("  Suggestion: Try again later or increase timeout")
        
        if error_types.get('rate_limit', 0) > 0:
            count = error_types['rate_limit']
            diagnostics.append(f"• {count} URL(s) rate limited (429) - Too many requests")
            diagnostics.append("  Suggestion: Add delays between requests or reduce batch size")
        
        if error_types.get('network', 0) > 0:
            count = error_types['network']
            diagnostics.append(f"• {count} URL(s) with network errors - Connection issues")
            diagnostics.append("  Suggestion: Check internet connection")
        
        if error_types.get('server_error', 0) > 0:
            count = error_types['server_error']
            diagnostics.append(f"• {count} URL(s) with server errors (5xx) - Server issues")
            diagnostics.append("  Suggestion: Try again later")
        
        if not diagnostics:
            diagnostics.append("• Review failures_and_errors/errors.json for detailed error information")
        
        return diagnostics
    
    def data(self, url, timeout=30, retry=0):
        """
        Get data from ONE URL, returns JSON
        
        🔮 MEGA SUPERPOWER: Handles ANY format!
        - String URL: "https://example.com"
        - Dict: {"url": "https://example.com"}
        - JSON string: '{"url": "https://example.com"}'
        - File path: "urls.json" (loads and extracts)
        
        Args:
            url: URL in ANY format (string, dict, JSON, file path)
            timeout (int): How long to wait in seconds (default: 30)
            retry (int): Number of retries on failure (default: 0)
            
        Returns:
            dict: Clean JSON data, always
        """
        # Smart URL extraction
        extracted_url = self._extract_single_url(url)
        if not extracted_url:
            return {
                "error": True,
                "message": f"Could not extract URL from: {url}",
                "url": str(url)
            }
        
        url = extracted_url
        last_error = None
        
        for attempt in range(retry + 1):
            try:
                response = httpx.get(url, timeout=timeout, follow_redirects=True)
                
                if response.status_code != 200:
                    error_dict = {
                        "error": True,
                        "status_code": response.status_code,
                        "message": f"HTTP {response.status_code}: Failed to get data from {url}",
                        "url": url
                    }
                    last_error = error_dict
                    
                    # If not last attempt, wait with exponential backoff
                    if attempt < retry:
                        wait_time = 2 ** attempt  # 1s, 2s, 4s, 8s...
                        time.sleep(wait_time)
                        continue
                    
                    # Last attempt failed - save to error file if retry > 0
                    if retry > 0:
                        self._save_failed_url(url, error_dict, retry)
                    
                    return error_dict
                
                # Success!
                content_type = response.headers.get('content-type', 'text/plain')
                json_data = to_json(response.content, content_type)
                
                if not isinstance(json_data, dict):
                    json_data = {"data": json_data}
                
                return json_data
                
            except httpx.TimeoutException:
                error_dict = {
                "error": True,
                "message": f"Request timeout after {timeout} seconds",
                "url": url
            }
                last_error = error_dict
                
                if attempt < retry:
                    wait_time = 2 ** attempt
                    time.sleep(wait_time)
                    continue
                
                if retry > 0:
                    self._save_failed_url(url, error_dict, retry)
                
                return error_dict
                
            except httpx.RequestError as e:
                error_dict = {
                "error": True,
                "message": f"Network error: {str(e)}",
                "url": url
            }
                last_error = error_dict
                
                if attempt < retry:
                    wait_time = 2 ** attempt
                    time.sleep(wait_time)
                    continue
                
                if retry > 0:
                    self._save_failed_url(url, error_dict, retry)
                
                return error_dict
                
            except Exception as e:
                error_dict = {
                "error": True,
                "message": f"Unexpected error: {str(e)}",
                "url": url
            }
                last_error = error_dict
                
                if attempt < retry:
                    wait_time = 2 ** attempt
                    time.sleep(wait_time)
                    continue
                
                if retry > 0:
                    self._save_failed_url(url, error_dict, retry)
                
                return error_dict
        
        # Should never reach here, but return last error if we do
        return last_error or {"error": True, "message": "Unknown error", "url": url}
    
    def many(self, urls, timeout=30, retry=0):
        """
        Get data from MANY URLs at once (10x faster!)
        
        🔮 MEGA SUPERPOWER: Handles ANY format!
        - List of strings: ["url1", "url2"]
        - List of dicts: [{"url": "url1"}, {"url": "url2"}]
        - Mixed: [{"url": "url1"}, "url2"]
        - JSON string: '[{"url": "url1"}]'
        - File path: "urls.json" (loads and extracts)
        - Single dict: {"url": "url1"} → extracts URL
        
        Args:
            urls: URLs in ANY format (list, dict, JSON, file path, mixed)
            timeout (int): How long to wait per request (default: 30)
            retry (int): Number of retries on failure (default: 0)
            
        Returns:
            list: List of JSON data (one per URL)
            
        Example:
            >>> from internet import *
            >>> # Works with ANY format!
            >>> results = get.many([{"url": "url1"}, "url2"], retry=3)
            >>> results = get.many("urls.json")  # Load from file
            >>> results = get.many([{"url": "..."}, {"url": "..."}])
        """
        # Smart URL extraction
        extracted_urls = self._extract_urls_smart(urls)
        if not extracted_urls:
            return [{
                "error": True,
                "message": f"Could not extract URLs from: {urls}",
                "url": str(urls)
            }]
        
        return asyncio.run(self._fetch_many(extracted_urls, timeout, retry))
    
    def batch(self, urls, batch_size=20, timeout=30, retry=0, save_to=None):
        """
        Process URLs in BATCHES - memory efficient, auto-saves progress!
        
        🔮 MEGA SUPERPOWER: Handles ANY format!
        - List of strings: ["url1", "url2", ...]
        - List of dicts: [{"url": "url1"}, {"url": "url2"}, ...]
        - Mixed formats: [{"url": "url1"}, "url2", {"data": {"url": "url3"}}]
        - JSON string: '[{"url": "url1"}]'
        - File path: "urls.json" (loads and extracts all URLs)
        - Single dict: {"url": "url1"} → extracts and processes
        
        Perfect for large datasets (200+ URLs). Processes in chunks, saves progressively.
        Includes automatic retry logic and two-phase recovery system.
        
        Args:
            urls: URLs in ANY format (list, dict, JSON, file path, mixed)
            batch_size (int): How many URLs per batch (default: 20)
            timeout (int): Timeout per request (default: 30)
            retry (int): Number of retries on failure (default: 0)
            save_to (str): Optional file to save results (auto-appends each batch)
            
        Returns:
            list: Complete list of all fetched data
            
        Example:
            >>> # Works with ANY format - just throw data at it!
            >>> results = get.batch([{"url": "..."}, {"url": "..."}], 20, retry=3)
            >>> results = get.batch("pokemon_urls.json", 20, retry=3, save_to="data")
            >>> results = get.batch(mixed_data, batch_size=20, timeout=30, retry=5)
            
        Why batching?
        - Memory efficient: Doesn't load all 200 at once
        - Progress saving: Won't lose data if it crashes
        - Better control: Can monitor progress
        - Network friendly: Doesn't overwhelm servers
        - Auto-recovery: Two-phase recovery system for failed URLs
        - Smart extraction: Handles ANY data format automatically
        """
        from simple_file import save as sf_save, exists, load
        
        # Smart URL extraction - handles ANY format!
        extracted_urls = self._extract_urls_smart(urls)
        if not extracted_urls:
            return [{
                "error": True,
                "message": f"Could not extract URLs from: {urls}",
                "url": str(urls)
            }]
        
        urls = extracted_urls  # Use extracted URLs
        all_results = []
        total_batches = (len(urls) + batch_size - 1) // batch_size
        
        print(f"🚀 Processing {len(urls)} URLs in {total_batches} batches of {batch_size}")
        
        for batch_num in range(0, len(urls), batch_size):
            batch_urls = urls[batch_num:batch_num + batch_size]
            current_batch = (batch_num // batch_size) + 1
            
            print(f"📦 Batch {current_batch}/{total_batches}: Fetching {len(batch_urls)} URLs...")
            
            # Fetch this batch with retry
            batch_results = asyncio.run(self._fetch_many(batch_urls, timeout, retry, save_to))
            
            # Separate successful and failed results
            successful_results = []
            failed_results = []

            for i, result in enumerate(batch_results):
                if result.get('error'):
                    failed_results.append({
                        'url': batch_urls[i],
                        'error_dict': result,
                        'retries_attempted': retry
                    })
                else:
                    successful_results.append(result)

            all_results.extend(batch_results)

            # Save failed URLs to per-file error tracking
            if failed_results and save_to:
                for failure in failed_results:
                    self._save_failed_url(
                        failure['url'],
                        failure['error_dict'],
                        failure['retries_attempted'],
                        save_to
                    )

            # Save progress if file specified (only successful ones)
            if save_to:
                if batch_num == 0:
                    # First batch: create new file with successful results
                    sf_save(save_to, successful_results)
                    print(f"💾 Saved batch {current_batch} to {save_to}")
                else:
                    # Subsequent batches: append successful results
                    existing_data = load(save_to)
                    if isinstance(existing_data, list):
                        existing_data.extend(successful_results)
                    else:
                        existing_data = [existing_data] + successful_results
                    sf_save(save_to, existing_data)
                    print(f"💾 Appended batch {current_batch} to {save_to}")

            print(f"✅ Batch {current_batch} complete! ({len(all_results)}/{len(urls)} total)")
        
        print(f"🎉 All done! Processed {len(all_results)} URLs")
        
        # Two-phase recovery system
        if retry > 0:
            self._recovery_system(save_to)
        
        return all_results
    
    def _recovery_system(self, save_to=None):
        """Two-phase recovery system for failed URLs - per-file error tracking"""
        if not save_to:
            return  # No save_to specified, no recovery needed

        error_folder = Path("failures_and_errors")
        if not error_folder.exists():
            return

        # Find the most recent error file for this save_to batch
        base_name = f"{save_to}_failure_and_error"
        json_file = None

        # Check for exact match first
        exact_json = error_folder / f"{base_name}.json"
        if exact_json.exists():
            json_file = exact_json
        else:
            # Look for (new) variants, get the most recent one
            error_files = list(error_folder.glob(f"{save_to}*failure_and_error.json"))
            if error_files:
                # Sort by modification time, get most recent
                error_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                json_file = error_files[0]

        if not json_file or not json_file.exists():
            return  # No error file for this batch

        try:
            with open(json_file, 'r') as f:
                failed_urls = json.load(f)
        except:
            return

        if not failed_urls:
            return

        print(f"\n🔧 Recovery Phase 1: Retrying {len(failed_urls)} failed URLs...")

        # Phase 1: Retry all failures with same settings
        urls_to_retry = [err['url'] for err in failed_urls]
        recovery_results = asyncio.run(self._fetch_many(urls_to_retry, 30, 1, save_to))  # 1 retry for recovery

        recovered_count = 0
        still_failing = []

        for i, result in enumerate(recovery_results):
            if not result.get('error'):
                # Successfully recovered!
                url = urls_to_retry[i]
                self._remove_recovered_url(url, save_to)
                recovered_count += 1

                # Add to main save file if specified
                if save_to:
                    from simple_file import load, save
                    existing_data = load(save_to)
                    if isinstance(existing_data, list):
                        existing_data.append(result)
                    else:
                        existing_data = [existing_data, result]
                    save(save_to, existing_data)
            else:
                still_failing.append(failed_urls[i])

        print(f"   ✅ Recovered: {recovered_count} URL(s)")
        print(f"   ❌ Still failing: {len(still_failing)} URL(s)")

        # If all recovered in phase 1, we're done!
        if not still_failing and recovered_count > 0:
            print(f"\n🎉 All URLs successfully recovered!")
            return

        # Phase 2: Retry remaining failures with smart timeout increase
        if still_failing:
            print(f"\n🔧 Recovery Phase 2: Retrying {len(still_failing)} URLs with increased timeout...")

            phase2_recovered = 0
            phase2_results = []

            for i, err in enumerate(still_failing):
                url = err['url']
                # Get smart timeout multiplier based on error type
                multiplier = self._get_smart_timeout_multiplier(err)
                new_timeout = int(30 * multiplier)  # Base timeout * multiplier

                # Retry with increased timeout (1 attempt)
                result = asyncio.run(self._fetch_one_single(url, new_timeout, 0))

                if not result.get('error'):
                    # Successfully recovered!
                    self._remove_recovered_url(url, save_to)
                    phase2_recovered += 1

                    # Add to main save file if specified
                    if save_to:
                        from simple_file import load, save
                        existing_data = load(save_to)
                        if isinstance(existing_data, list):
                            existing_data.append(result)
                        else:
                            existing_data = [existing_data, result]
                        save(save_to, existing_data)
                else:
                    phase2_results.append(err)

            total_recovered = recovered_count + phase2_recovered
            print(f"   ✅ Recovered: {phase2_recovered} URL(s)")
            print(f"   ❌ Still failing: {len(phase2_results)} URL(s)")

            # If all recovered in phase 2, show success
            if not phase2_results and total_recovered > 0:
                print(f"\n🎉 All URLs successfully recovered in recovery phase!")
                return

            # Final summary and diagnostics
            if phase2_results:
                self._print_final_summary(phase2_results, total_recovered, save_to)
    
    async def _fetch_one_single(self, url, timeout, retry):
        """Single fetch attempt for recovery phase 2"""
        try:
            async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
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
                "message": f"Error: {str(e)}",
                "url": url
            }
    
    def _print_final_summary(self, final_failures, total_recovered, save_to=None):
        """Print final summary with smart diagnostics - per-file error tracking"""
        error_file_name = f"{save_to}_failure_and_error.json" if save_to else "errors.json"
        error_path = f"failures_and_errors/{error_file_name}"

        print(f"\n📊 Final Summary:")
        print(f"   ✅ Total Success: {total_recovered} URL(s) recovered")
        print(f"   ❌ Final Failures: {len(final_failures)} URL(s) (saved to {error_path})")

        diagnostics = self._get_smart_diagnostics(final_failures)

        if diagnostics:
            print(f"\n💡 Smart Diagnostics:")
            for diag in diagnostics:
                print(f"   {diag}")

        print(f"\n   Next steps: Review {error_path} for details")
    
    async def _fetch_many(self, urls, timeout, retry=0, batch_save_to=None):
        """Internal async function to fetch multiple URLs with retry support"""
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
            tasks = [self._fetch_one(client, url, timeout, retry, batch_save_to) for url in urls]
            return await asyncio.gather(*tasks)
    
    async def _fetch_one(self, client, url, timeout, retry=0, batch_save_to=None):
        """Internal async function to fetch one URL with retry and exponential backoff"""
        last_error = None

        for attempt in range(retry + 1):
            try:
                response = await client.get(url)

                if response.status_code != 200:
                    error_dict = {
                        "error": True,
                        "status_code": response.status_code,
                        "message": f"HTTP {response.status_code}: Failed",
                        "url": url
                    }
                    last_error = error_dict

                    # If not last attempt, wait with exponential backoff
                    if attempt < retry:
                        wait_time = 2 ** attempt  # 1s, 2s, 4s, 8s...
                        await asyncio.sleep(wait_time)
                        continue

                    # Last attempt failed - save to error file if retry > 0 and not in batch context
                    # (batch operations handle error saving at the batch level)
                    if retry > 0 and not batch_save_to:
                        self._save_failed_url(url, error_dict, retry)

                    return error_dict

                # Success!
                content_type = response.headers.get('content-type', 'text/plain')
                json_data = to_json(response.content, content_type)

                if not isinstance(json_data, dict):
                    json_data = {"data": json_data}

                return json_data

            except httpx.TimeoutException:
                error_dict = {
                    "error": True,
                    "message": f"Request timeout after {timeout} seconds",
                    "url": url
                }
                last_error = error_dict

                if attempt < retry:
                    wait_time = 2 ** attempt
                    await asyncio.sleep(wait_time)
                    continue

                if retry > 0 and not batch_save_to:
                    self._save_failed_url(url, error_dict, retry)

                return error_dict

            except httpx.RequestError as e:
                error_dict = {
                    "error": True,
                    "message": f"Network error: {str(e)}",
                    "url": url
                }
                last_error = error_dict

                if attempt < retry:
                    wait_time = 2 ** attempt
                    await asyncio.sleep(wait_time)
                    continue

                if retry > 0 and not batch_save_to:
                    self._save_failed_url(url, error_dict, retry)

                return error_dict

            except Exception as e:
                error_dict = {
                    "error": True,
                    "message": f"Error: {str(e)}",
                    "url": url
                }
                last_error = error_dict

                if attempt < retry:
                    wait_time = 2 ** attempt
                    await asyncio.sleep(wait_time)
                    continue

                if retry > 0 and not batch_save_to:
                    self._save_failed_url(url, error_dict, retry)

                return error_dict

        # Should never reach here, but return last error if we do
        return last_error or {"error": True, "message": "Unknown error", "url": url}

# Create the singleton instance
get = DataGetter()

