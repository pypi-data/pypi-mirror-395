"""
💀 DATA MONARCH v2.5 - ULTRA-ROBUST DATA ANALYSIS 💀
Handles ANY data structure the world can throw at it
"""

from typing import Dict, Any, Union, List
from .core import MonarchBase, ThoughtResult
from .registry import register_monarch


@register_monarch("data")
class DataMonarch(MonarchBase):
    """💀 DATA ANALYSIS SHADOW MONARCH v2.5 💀"""
    
    async def analyze(self, data: Union[str, Dict, list], 
                     sample_size: int = 500,
                     dedupe_threshold: float = 0.05) -> Dict[str, Any]:
        """💀 GOD-TIER DATA ANALYSIS - Handles ANYTHING 💀"""
        print("💀 Data Monarch: Beginning analysis...")
        
        # Step 1: Load from file if needed
        if isinstance(data, str):
            print(f"   Loading: {data}")
            try:
                data = self.files.load(data)
            except Exception as e:
                return self._error_report(f"Failed to load file: {e}")
        
        # Step 2: Normalize with json_mage
        print("   Normalizing data...")
        try:
            normalized = self.json.modify(data)
            clean_data = normalized.raw
        except Exception as e:
            print(f"   ⚠️  json_mage failed: {e}, using raw data")
            clean_data = data
        
        # Step 3: EXTRACT ARRAY FROM WRAPPER (THE CRITICAL FIX)
        clean_data = self._extract_data_array(clean_data)
        
        # Step 4: FILTER OUT INVALID ITEMS
        clean_data = self._filter_invalid_items(clean_data)
        
        print(f"   Analyzing {len(clean_data) if isinstance(clean_data, list) else 'non-list'} items...")
        
        # Step 5: Get summary
        try:
            summary = normalized.summary() if 'normalized' in locals() else {}
        except:
            summary = {"error": "Could not generate summary"}
        
        # Step 6: Find duplicates
        print("   Checking for duplicates...")
        dupe_count, dupe_rate, dupe_details = self._analyze_duplicates(clean_data)
        
        # Step 7: Sample for AI
        sample = self._get_sample(clean_data, sample_size)
        
        # Step 8: AI analysis
        print("   Generating AI insights...")
        ai_insights = await self._get_ai_insights(clean_data, sample, dupe_rate)
        
        # Step 9: Calculate quality score
        quality_score = self._calculate_quality_score(clean_data, dupe_rate)
        
        # Step 10: Build report
        report = {
            "data_quality_score": quality_score,
            "summary": {
                "total_items": len(clean_data) if isinstance(clean_data, list) else 1,
                "data_type": type(clean_data).__name__,
                "has_duplicates": dupe_count > 0
            },
            "duplicates": {
                "count": dupe_count,
                "rate": f"{dupe_rate:.1%}",
                "threshold_exceeded": dupe_rate > dedupe_threshold,
                "details": dupe_details
            },
            "ai_analysis": ai_insights,
            "recommended_actions": self._generate_recommendations(clean_data, dupe_rate),
            "monarch_id": self.monarch_id
        }
        
        print(f"💀 Analysis complete | Quality: {quality_score}/10")
        return report
    
    def _extract_data_array(self, data: Any) -> List:
        """
        CRITICAL: Extract actual data array from wrapper structures
        
        Handles:
        - {"users": [...]} → [...]
        - {"data": [...]} → [...]
        - {"items": [...], "metadata": {...}} → [...]
        - [...] → [...] (no change)
        """
        if not isinstance(data, dict):
            return data
        
        # Common wrapper keys
        array_keys = ["users", "data", "items", "records", "results", "list", "entries"]
        
        for key in array_keys:
            if key in data and isinstance(data[key], list):
                print(f"   📦 Extracted '{key}' array ({len(data[key])} items)")
                return data[key]
        
        # If dict has only one key and it's a list, extract it
        if len(data) == 1:
            only_value = list(data.values())[0]
            if isinstance(only_value, list):
                print(f"   📦 Extracted single-key array ({len(only_value)} items)")
                return only_value
        
        # If multiple keys but one is clearly the data
        list_values = [(k, v) for k, v in data.items() if isinstance(v, list)]
        if len(list_values) == 1:
            key, value = list_values[0]
            print(f"   📦 Extracted '{key}' array ({len(value)} items)")
            return value
        
        # Last resort: if dict, convert to list of one item
        print(f"   ⚠️  Dict structure, treating as single item")
        return [data]
    
    def _filter_invalid_items(self, data: Any) -> List:
        """Remove invalid items (None, empty strings, empty arrays)"""
        if not isinstance(data, list):
            return data
        
        valid_items = []
        invalid_count = 0
        
        for item in data:
            # Skip None
            if item is None:
                invalid_count += 1
                continue
            
            # Skip empty lists
            if isinstance(item, list) and len(item) == 0:
                invalid_count += 1
                continue
            
            # Skip standalone strings (unless everything is strings)
            if isinstance(item, str) and not all(isinstance(x, str) for x in data):
                invalid_count += 1
                continue
            
            valid_items.append(item)
        
        if invalid_count > 0:
            print(f"   🗑️  Filtered out {invalid_count} invalid items")
        
        return valid_items
    
    def _analyze_duplicates(self, data: Any) -> tuple:
        """
        Analyze duplicates robustly
        Returns: (count, rate, details)
        """
        if not isinstance(data, list) or len(data) == 0:
            return 0, 0.0, []
        
        try:
            # Use grimoire's smart_duplicate_check
            dupe_result = self.dupes.smart_duplicate_check(data)
            
            if isinstance(dupe_result, dict):
                dupe_count = dupe_result.get('duplicate_count', 0)
                total = dupe_result.get('total_items', len(data))
                dupe_rate = dupe_count / total if total > 0 else 0
                
                # Extract key details
                details = dupe_result.get('details', [])[:5]  # Top 5
                
                return dupe_count, dupe_rate, details
            else:
                return 0, 0.0, []
        
        except Exception as e:
            print(f"   ⚠️  Duplicate check failed: {e}")
            return 0, 0.0, []
    
    def _get_sample(self, data: Any, sample_size: int) -> Any:
        """Get sample of data for AI analysis"""
        if not isinstance(data, list):
            return data
        
        if len(data) <= sample_size:
            return data
        
        # Sample from beginning, middle, end
        step = len(data) // sample_size
        sample = [data[i] for i in range(0, len(data), max(step, 1))][:sample_size]
        
        print(f"   🔬 Sampled {len(sample)}/{len(data)} items for AI analysis")
        return sample
    
    async def _get_ai_insights(self, full_data: Any, sample: Any, dupe_rate: float) -> str:
        """Get AI insights with error handling"""
        
        # Build context
        data_type = type(full_data).__name__
        data_size = len(full_data) if isinstance(full_data, list) else 1
        
        prompt = f"""Analyze this dataset:

Data Type: {data_type}
Total Items: {data_size}
Duplicate Rate: {dupe_rate:.1%}
Sample (first few items): {str(sample)[:800]}

Provide BRUTALLY HONEST analysis:
1. Data Quality Score (0-10) - be harsh
2. Key Patterns (what's consistent)
3. Anomalies (what's broken)
4. Recommended Actions (what to fix NOW)
5. Business Impact (why this matters)

Be specific, actionable, and don't sugarcoat."""
        
        try:
            thought = await self.think(prompt, max_tokens=1000)
            return thought.thoughts
        except Exception as e:
            return f"AI analysis unavailable: {e}\n\nFallback analysis: {data_size} items with {dupe_rate:.1%} duplicates detected."
    
    def _calculate_quality_score(self, data: Any, dupe_rate: float) -> float:
        """
        FIXED SCORING v2.5
        
        Penalties:
        - Duplicates: -5 points max
        - Invalid items: Already filtered
        - Small dataset: -1 point if < 10 items
        """
        base_score = 10.0
        
        # Penalty for duplicates (heavy)
        if dupe_rate > 0.05:  # >5% dupes
            base_score -= min(dupe_rate * 50, 5.0)
        
        if dupe_rate > 0.30:  # >30% dupes (critical)
            base_score -= 2.0
        
        # Penalty for tiny datasets
        if isinstance(data, list) and len(data) < 10:
            base_score -= 1.0
        
        # Penalty for non-list data (dict or other)
        if not isinstance(data, list):
            base_score -= 2.0
        
        return max(round(base_score, 1), 0.0)
    
    def _generate_recommendations(self, data: Any, dupe_rate: float) -> List[str]:
        """Generate actionable recommendations"""
        recs = []
        
        # Duplicate recommendations
        if dupe_rate > 0.30:
            recs.append("🚨 CRITICAL: 30%+ duplicates - CLEAN IMMEDIATELY")
        elif dupe_rate > 0.10:
            recs.append("⚠️  Remove duplicates (>10% found)")
        elif dupe_rate > 0.05:
            recs.append("Remove duplicates (>5% found)")
        
        # Data structure recommendations
        if not isinstance(data, list):
            recs.append("Convert to list structure for better analysis")
        
        if isinstance(data, list) and len(data) < 10:
            recs.append("Dataset too small - collect more data")
        
        # Standard recommendations
        recs.append("Validate data types and formats")
        recs.append("Add data validation layer at input")
        recs.append("Implement data quality monitoring")
        
        return recs
    
    def _error_report(self, error_msg: str) -> Dict[str, Any]:
        """Generate error report"""
        return {
            "data_quality_score": 0.0,
            "summary": {"error": error_msg},
            "duplicates": {"count": 0, "rate": "0%", "threshold_exceeded": False},
            "ai_analysis": f"Analysis failed: {error_msg}",
            "recommended_actions": ["Fix data loading issue"],
            "monarch_id": self.monarch_id
        }
    
    # SYNC WRAPPERS
    def analyze_sync(self, data, **kwargs):
        from .factory import waitfor
        return waitfor(self.analyze(data, **kwargs))
    
    def __call__(self, data, **kwargs):
        return self.analyze_sync(data, **kwargs)
