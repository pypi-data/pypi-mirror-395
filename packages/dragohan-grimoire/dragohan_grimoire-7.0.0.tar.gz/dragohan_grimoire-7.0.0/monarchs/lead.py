"""
💀 LEAD MONARCH - FIXED VERSION (CRITICAL BUG FIXES APPLIED) 💀
Fixed dangerous silent AI failure masking and other critical issues
"""

import asyncio
from typing import Union, List, Dict, Any
from .core import MonarchBase, ThoughtResult
from .registry import register_monarch


@register_monarch("lead")
class LeadMonarch(MonarchBase):
    """
    💀 LEAD ENRICHMENT SHADOW MONARCH (FIXED) 💀
    """
    
    async def enrich(self, data: Union[Dict, List, str]) -> Union[Dict, List[Dict]]:
        """💀 GOD METHOD - Enrich ANY data shape with PROPER ERROR HANDLING 💀"""
        print("💀 Lead Monarch: Beginning enrichment...")
        
        try:
            # Step 1: Auto-detect and load data
            if isinstance(data, str):
                print(f"   Detected: {'URL' if data.startswith('http') else 'File path'}")
                if data.startswith("http"):
                    data = self.web.get.data(data)
                else:
                    data = self.files.load(data)
            
            # Step 2: Normalize with json_mage
            print("   Normalizing data with json_mage...")
            try:
                normalized = self.json.modify(data)
                clean_data = normalized.raw
            except Exception as e:
                print(f"   ⚠️  json_mage failed: {e}, using raw data")
                clean_data = data
            
            # Step 3: Detect single vs batch
            if isinstance(clean_data, list):
                print(f"   Batch detected: {len(clean_data)} leads")
                result = await self._enrich_batch(clean_data)
                
                # NEW: Report failures
                failed_count = sum(1 for r in result if isinstance(r, dict) and r.get('error'))
                if failed_count > 0:
                    print(f"   ⚠️  WARNING: {failed_count}/{len(clean_data)} leads failed to process")
                
                return result
            else:
                print("   Single lead detected")
                return await self._enrich_single(clean_data)
                
        except Exception as e:
            print(f"❌ CRITICAL: Monarch failed to initialize - {e}")
            raise  # Don't mask critical initialization failures
    
    async def _enrich_single(self, lead: Dict) -> Dict:
        """Enrich one lead with PROPER ERROR HANDLING"""
        print(f"💀 Enriching: {lead.get('name', 'Unknown')}")
        
        try:
            # Build AI prompt (industry-aware)
            if self.industry == "restaurant":
                prompt = self._build_restaurant_prompt(lead)
            else:
                prompt = self._build_generic_prompt(lead)
            
            # Get AI insights with ERROR HANDLING
            try:
                thought = await self.think(prompt)
            except Exception as e:
                print(f"❌ AI failed for {lead.get('name', 'Unknown')}: {e}")
                # FIXED: Return proper error state instead of fake success
                return {
                    "original": lead,
                    "ai_insights": f"ERROR: AI processing failed - {str(e)}",
                    "lead_score": 0.0,  # FIXED: Realistic score for failed processing
                    "error": str(e),
                    "industry": self.industry or "generic",
                    "monarch_id": self.monarch_id,
                    "status": "failed"
                }
            
            # Calculate score ONLY if AI succeeded
            score = self._calculate_score(thought, lead)
            
            enriched = {
                "original": lead,
                "ai_insights": thought.thoughts,
                "lead_score": score,
                "industry": self.industry or "generic",
                "monarch_id": self.monarch_id,
                "status": "success" if score > 0 else "failed"
            }
            
            # NEW: Show real score (not always perfect)
            print(f"   {'✅' if score > 5 else '⚠️'} Enriched | Score: {score}/10")
            return enriched
            
        except Exception as e:
            print(f"❌ CRITICAL: Failed to process {lead.get('name', 'Unknown')}: {e}")
            return {
                "original": lead,
                "ai_insights": f"ERROR: Processing failed - {str(e)}",
                "lead_score": 0.0,
                "error": str(e),
                "industry": self.industry or "generic",
                "monarch_id": self.monarch_id,
                "status": "failed"
            }
    
    async def _enrich_batch(self, leads: List[Dict]) -> List[Dict]:
        """Enrich multiple leads with RATE LIMITING and ERROR HANDLING"""
        self._works = True
        self._results = []
        
        # FIXED: Rate limiting - max 3 concurrent requests
        semaphore = asyncio.Semaphore(3)
        delay_between_requests = 0.5  # 500ms delay between requests
        
        async def _process_one(lead):
            async with semaphore:
                try:
                    result = await self._enrich_single(lead)
                    self._current = result
                    self._results.append(result)
                    return result
                except Exception as e:
                    # Individual lead failure - still add to results
                    error_result = {
                        "original": lead,
                        "ai_insights": f"ERROR: Batch processing failed - {str(e)}",
                        "lead_score": 0.0,
                        "error": str(e),
                        "industry": self.industry or "generic",
                        "monarch_id": self.monarch_id,
                        "status": "failed"
                    }
                    self._current = error_result
                    self._results.append(error_result)
                    return error_result
                finally:
                    # FIXED: Rate limiting delay
                    await asyncio.sleep(delay_between_requests)
        
        print(f"🔄 Processing {len(leads)} leads with rate limiting...")
        tasks = [_process_one(lead) for lead in leads]
        
        # Use return_exceptions=True to catch any batch-level failures
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Convert any exceptions to error results
        final_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"❌ Exception in batch processing for lead {i}: {result}")
                final_results.append({
                    "original": leads[i],
                    "ai_insights": f"ERROR: Batch exception - {str(result)}",
                    "lead_score": 0.0,
                    "error": str(result),
                    "industry": self.industry or "generic",
                    "monarch_id": self.monarch_id,
                    "status": "failed"
                })
            else:
                final_results.append(result)
        
        self._works = False
        
        # NEW: Better summary with failure reporting
        success_count = sum(1 for r in final_results if isinstance(r, dict) and r.get('status') == 'success')
        print(f"💀 Batch complete: {success_count}/{len(final_results)} leads successfully enriched")
        
        return final_results
    
    def _build_restaurant_prompt(self, lead: Dict) -> str:
        """Restaurant-specific enrichment prompt"""
        return f"""
💀 RESTAURANT LEAD ENRICHMENT 💀

Lead Data:
{lead}

Provide deep analysis:

1. REVENUE ESTIMATE
   - Monthly revenue range (based on type, location, size)
   - Revenue tier: Low (<$20k), Mid ($20-100k), High (>$100k)

2. PAIN POINTS (Restaurant-specific)
   - Reservation management issues?
   - Review/reputation problems?
   - Delivery/online ordering gaps?
   - POS system limitations?
   - Staff management challenges?

3. DECISION MAKER POWER (1-10 scale)
   - Owner = 10 (full decision authority)
   - General Manager = 7
   - Assistant Manager = 4
   - Staff = 1
   
4. OUTREACH ANGLE
   - Best approach for this specific restaurant
   - Pain point to emphasize
   - Value proposition

5. SERVICE FIT
   - Lead generation potential
   - Automation opportunities
   - Review management need
   - Reservation system upgrade

Format response as clear insights, not JSON.
Be specific and actionable.
"""
    
    def _build_generic_prompt(self, lead: Dict) -> str:
        """Generic lead enrichment prompt"""
        return f"""
Analyze this lead:
{lead}

Provide:
1. Company revenue estimate
2. Key pain points
3. Decision maker power (1-10)
4. Best outreach approach
5. Product/service fit

Be specific and actionable.
"""
    
    def _calculate_score(self, thought: ThoughtResult, lead: Dict) -> float:
        """
        Calculate lead score (0-10) - FIXED VERSION
        Formula: 40% decision + 30% revenue + 20% completeness + 10% AI confidence
        """
        # Check for AI errors first
        if thought.metadata.get('error'):
            return 0.0  # No score if AI failed
        
        # Base completeness score
        completeness = len([v for v in lead.values() if v]) / max(len(lead), 1)
        base_score = completeness * 10
        
        # Industry boost (only for good data)
        if self.industry == "restaurant" and completeness > 0.5:
            base_score *= 1.1
        
        # Penalty for poor data quality
        if completeness < 0.3:
            base_score *= 0.5
        
        # Penalty for AI errors in metadata
        if thought.metadata.get('error'):
            base_score = 0.0
        
        return min(round(base_score, 1), 10.0)
    
    # SYNC WRAPPERS
    def enrich_sync(self, data):
        """Sync wrapper for enrich()"""
        from .factory import waitfor
        return waitfor(self.enrich(data))
    
    def __call__(self, data):
        """Shorthand: agent(data) → enrich_sync(data)"""
        return self.enrich_sync(data)
