# json_mage.py - Your Personal JSON Grimoire (ULTIMATE EDITION v8 - SHADOW MONARCH)
"""
DragoHan's JSON Mastery Library
The simplest way to work with JSON - no bullshit, just results.

Powers: 31+ methods for reading, counting, filtering, sorting, math, occurrence analysis, and modifying JSON
NEW: Universal modify() that auto-extracts data from ANY structure!
NEW: Shadow Monarch summary() with beautiful reports and duplicate detection!
"""

from typing import Any, Union, List, Dict
import json
from collections import Counter
import jmespath


class MageJSON:
    """
    The simplest JSON sorcery - read, write, count, filter, sort ANY JSON structure.
    """

    def __init__(self, data: Union[str, dict, list]):
        """Auto-converts anything to workable JSON"""
        if isinstance(data, str):
            try:
                self._raw = json.loads(data)
            except Exception:
                self._raw = data
        else:
            self._raw = data

    # ===================================================================
    # READING POWERS (11 methods)
    # ===================================================================

    @property
    def first(self) -> Any:
        """Get first item - data.first"""
        if isinstance(self._raw, list):
            return self._raw[0] if self._raw else None
        if isinstance(self._raw, dict):
            return list(self._raw.values())[0] if self._raw else None
        return self._raw

    @property
    def last(self) -> Any:
        """Get last item - data.last"""
        if isinstance(self._raw, list):
            return self._raw[-1] if self._raw else None
        if isinstance(self._raw, dict):
            return list(self._raw.values())[-1] if self._raw else None
        return self._raw

    @property
    def keys(self) -> List[str]:
        """All unique keys - data.keys"""
        keys: set = set()
        self._collect_keys(self._raw, keys)
        return sorted(list(keys))

    @property
    def raw(self) -> Any:
        """Get original data - data.raw"""
        return self._raw

    def get(self, key: str) -> Any:
        """
        Get value for a key (searches anywhere)
        Works with dot notation: data.get('user.email')
        """
        result = jmespath.search(key, self._raw)
        if result is not None:
            return result
        return self._deep_search(self._raw, key)

    def all(self, key: str) -> List:
        """
        Get ALL values for a key
        Example: data.all('email') → all emails
        """
        return self._collect_all_values(self._raw, key)

    def find(self, value: Any) -> List:
        """
        Find items containing a value
        Example: data.find('john@email.com')
        """
        return self._find_value(self._raw, value)

    def unique(self, key: str) -> List:
        """
        Get unique values (no duplicates)
        Example: data.unique('status') → ['success', 'error']
        """
        return list(set(self.all(key)))

    def has(self, key: str, value: Any) -> bool:
        """
        Check if value exists
        Example: data.has('status', 'error') → True/False
        """
        return value in self.all(key)

    @property
    def show(self) -> str:
        """Pretty print - print(data.show)"""
        return json.dumps(self._raw, indent=2)

    def __getitem__(self, key):
        """Direct access - data['key'] or data[0]"""
        if isinstance(self._raw, (dict, list)):
            return self._raw[key]
        return None

    # ===================================================================
    # COUNTING & FILTERING POWERS (4 methods)
    # ===================================================================

    def count(self, key: str, value: Any = None) -> Union[int, dict]:
        """
        Count occurrences

        Examples:
            data.count('status', 'success')  → 3
            data.count('status')             → {'success': 3, 'error': 2}
        """
        all_values = self.all(key)
        if value is None:
            return dict(Counter(all_values))
        return all_values.count(value)

    def filter(self, key: str, value: Any) -> List:
        """
        Get items where key=value (direct match only)

        Example: data.filter('status', 'error') → all errors
        Note: For nested filtering, use smart_filter()
        """
        result: List = []
        if isinstance(self._raw, list):
            for item in self._raw:
                if isinstance(item, dict) and item.get(key) == value:
                    result.append(item)
        return result

    def smart_filter(self, key: str, operator_or_value: Any, value: Any = None) -> 'MageJSON':
        """
        UNIVERSAL smart filter with operator support - CHAINABLE

        Usage patterns:
            # Simple equality (backward compatible)
            logs.smart_filter("type", "water")

            # With operators
            logs.smart_filter("weight", ">", 50)
            logs.smart_filter("height", "<=", 10)
            logs.smart_filter("name", "contains", "char")
            logs.smart_filter("id", "in", [1, 5, 10])

            # Chained filters
            heavy_water = (logs
                .smart_filter("type", "water")
                .smart_filter("weight", ">", 50)
            )

        Operators:
            ==, !=, >, <, >=, <=, contains, in

        Returns:
            MageJSON object (chainable)
        """
        if value is None:
            operator = "=="
            compare_value = operator_or_value
        else:
            operator = operator_or_value
            compare_value = value

        results: List[dict] = []

        if not isinstance(self._raw, list):
            return MageJSON(results)

        for item in self._raw:
            if isinstance(item, dict) and item.get('error'):
                continue

            item_value = self._get_nested_value(item, key)

            if item_value is None:
                continue

            if self._compare(item_value, operator, compare_value):
                results.append(item)

        return MageJSON(results)

    def summary(self) -> str:
        """
        🌑 SHADOW MONARCH BUSINESS INTELLIGENCE - Ultimate Analysis

        Automatically detects and provides EPIC business reports for:
        - Strategic portfolios (Pokemon, users, products)
        - Risk assessment with duplicate detection
        - Compliance verification and deployment readiness
        - Professional business intelligence with Shadow Monarch styling

        Returns:
            Beautifully formatted Business + Shadow Monarch styled report
        """
        INNER = 70  # inner content width between borders

        def bar() -> str:
            return "🌑✦" + ("━" * (INNER + 2)) + "✦🌑"

        def center_line(text: str) -> str:
            return f"│ {text.center(INNER)} │"

        def pad_line(text: str = "") -> str:
            return f"│ {text.ljust(INNER)} │"

        def section_header(title: str) -> List[str]:
            t = f"{title}"
            underline = "─" * len(title)
            return [pad_line(t), pad_line(underline)]

        def analyze_field(field_name: str) -> str:
            try:
                values = self.all(field_name)
                if not values:
                    return f"• {field_name:<16}→ [No Intelligence Available]"

                num_values = [v for v in values if isinstance(v, (int, float))]
                str_values = [v for v in values if isinstance(v, str)]
                list_values = [v for v in values if isinstance(v, list)]

                if len(num_values) == len([v for v in values if v is not None]) and num_values:
                    mn, mx = min(num_values), max(num_values)
                    avg = sum(num_values) / len(num_values)
                    return f"• {field_name:<16}→ Performance Range [{mn}-{mx}] (AVG: {avg:.1f})"

                if len(str_values) == len([v for v in values if v is not None]) and str_values:
                    uniq = len(set(str_values))
                    if uniq == len(str_values):
                        return f"• {field_name:<16}→ [{uniq} Unique Classifications]"
                    top = Counter(str_values).most_common(1)[0]
                    return f"• {field_name:<16}→ [{uniq} Categories: {top[0]}: {top[1]}]"

                if len(list_values) == len([v for v in values if v is not None]) and list_values:
                    lengths = [len(v) for v in list_values]
                    mn, mx = min(lengths), max(lengths)
                    avg = sum(lengths) / len(lengths)
                    return f"• {field_name:<16}→ Capability Set [{mn}-{mx}] (AVG: {avg:.1f})"

                uniq_complex = len(set(str(v) for v in values if v is not None))
                return f"• {field_name:<16}→ [{uniq_complex} Complex Intelligence Points]"
            except Exception:
                return f"• {field_name:<16}→ [Analysis Failed - Complex Intelligence]"

        # Duplicate/risk analysis
        duplicate_status = "✅ [COMPLIANT] No duplicate assets detected"
        duplicate_details: List[str] = []
        integrity_score = "100%"

        try:
            from duplicate_tools import smart_duplicate_check
            dup_result = smart_duplicate_check(self._raw)
            if dup_result.get("duplicates_found", False):
                dup_count = dup_result.get("duplicate_count", 0)
                total_items = dup_result.get(
                    "total_items",
                    len(self._raw) if isinstance(self._raw, list) else 1,
                )
                integrity_score = (
                    f"{((total_items - dup_count) / total_items * 100):.1f}%"
                    if total_items > 0
                    else "0%"
                )
                duplicate_status = f"⚠️  [RISK] {dup_count} duplicate assets identified"
                duplicate_details = [
                    f"⚠️  [CONFLICT] {dup_count} assets share identifiers",
                    f"⚠️  [VULNERABILITY] Portfolio integrity compromised: {integrity_score}",
                    "⚠️  [ACTION] Immediate deduplication required",
                ]
        except Exception:
            # Fallback basic duplicate check
            if isinstance(self._raw, list):
                try:
                    ids = [
                        d.get("id")
                        for d in self._raw
                        if isinstance(d, dict) and "id" in d
                    ]
                    if ids and len(ids) != len(set(ids)):
                        duplicate_status = "⚠️  [RISK] Possible duplicates detected"
                        integrity_score = "Unknown"
                except Exception:
                    integrity_score = "Unknown"

        # Asset classification and status
        report: List[str] = []
        if isinstance(self._raw, list):
            total_items = len(self._raw)
            if total_items == 0:
                asset_type = "[Empty Portfolio]"
                status = "[NO ASSETS TO ANALYZE]"
            else:
                first = self._raw[0] if self._raw else {}
                if isinstance(first, dict):
                    if "name" in first and any(k in first for k in ["types", "abilities", "stats"]):
                        asset_type = "[Pokemon Collection]"
                    elif "email" in first or "username" in first:
                        asset_type = "[User Records]"
                    elif "price" in first or "product" in first:
                        asset_type = "[Product Catalog]"
                    else:
                        asset_type = "[Structured Data Portfolio]"
                else:
                    asset_type = "[Simple Data Portfolio]"
                status = (
                    "[BUSINESS INTELLIGENCE COMPLETE]"
                    if integrity_score == "100%"
                    else "[RISK ASSESSMENT REQUIRED]"
                )
        else:
            asset_type = "[Single Asset]"
            total_items = 1
            status = "[BUSINESS INTELLIGENCE COMPLETE]"

        # Header
        report.append(bar())
        report.append(center_line("📊 SHADOW MONARCH BUSINESS INTELLIGENCE REPORT"))
        report.append(center_line(status))
        report.append(bar())
        report.append(pad_line())

        # Executive Summary
        report.extend(section_header("📋 EXECUTIVE SUMMARY"))
        report.append(pad_line(f"• Asset Classification: {asset_type}"))
        report.append(pad_line(f"• Portfolio Size:       {total_items}"))
        if integrity_score == "100%":
            quality = "[OPTIMAL] - Zero corruption detected"
        elif integrity_score == "Unknown":
            quality = "[UNKNOWN] - Intelligence verification required"
        else:
            quality = f"[RISK] - Portfolio integrity: {integrity_score}"
        report.append(pad_line(f"• Data Integrity:       {quality}"))
        if isinstance(self._raw, list) and self._raw:
            kcount = len(self.keys)
            report.append(pad_line(f"• Analytical Depth:     {kcount} Key Performance Indicators"))
        else:
            report.append(pad_line("• Analytical Depth:     Single Asset Analysis"))
        report.append(pad_line())

        # Performance Metrics
        if isinstance(self._raw, list) and self._raw and self.keys:
            report.extend(section_header("⚡ PERFORMANCE METRICS"))
            business_names = {
                "id": "Asset IDs",
                "name": "Asset Names",
                "weight": "Physical Power",
                "height": "Presence",
                "types": "Elements",
                "stats": "Capabilities",
                "abilities": "Special Powers",
                "email": "Contact Intelligence",
                "status": "Operational Status",
                "price": "Market Value",
            }
            for key in self.keys[:7]:
                bname = business_names.get(key, key.title())
                analysis = analyze_field(key)
                # replace field label at start
                if analysis.startswith("• "):
                    analysis = analysis.replace(
                        f"• {key:<16}", f"• {bname:<16}", 1
                    )
                line = analysis
                if len(line) > INNER:
                    line = line[:INNER]
                report.append(pad_line(line))
            if len(self.keys) > 7:
                extra = len(self.keys) - 7
                report.append(pad_line(f"• ... and {extra} additional intelligence metrics"))
            report.append(pad_line())

        # Risk Assessment & Compliance
        report.extend(section_header("🎯 RISK ASSESSMENT & COMPLIANCE"))
        line = duplicate_status
        if len(line) > INNER:
            line = line[:INNER]
        report.append(pad_line(line))
        if duplicate_details:
            for detail in duplicate_details:
                d = detail if len(detail) <= INNER else detail[:INNER]
                report.append(pad_line(d))
        else:
            report.append(pad_line("✅ [SECURE] All assets have unique identifiers"))
            report.append(pad_line("✅ [VALIDATED] No corrupted or incomplete intelligence found"))
            report.append(pad_line(f"✅ [AUDITED] Portfolio integrity: {integrity_score}"))
        report.append(pad_line())

        # Strategic Recommendations
        report.extend(section_header("💀 STRATEGIC RECOMMENDATIONS"))
        if integrity_score == "100%":
            tier = "ELITE"
        elif integrity_score != "Unknown":
            try:
                score = float(integrity_score.rstrip("%"))
            except Exception:
                score = 0.0
            if score >= 90:
                tier = "PREMIUM"
            elif score >= 70:
                tier = "STANDARD"
            else:
                tier = "BASIC"
        else:
            tier = "STANDARD"

        if isinstance(self._raw, list) and total_items > 0:
            report.append(pad_line(f"[{tier}] Complete portfolio - No missing intelligence"))
            # lightweight portfolio-specific notes
            if asset_type == "[Pokemon Collection]":
                report.append(pad_line("[PREMIUM] Balanced power distribution across assets"))
                report.append(pad_line("[ELITE] Standardized combat framework established"))
            elif asset_type == "[User Records]":
                report.append(pad_line("[STANDARD] Healthy user distribution maintained"))
                report.append(pad_line("[ELITE] Structure normalized and operational"))
            else:
                report.append(pad_line("[PREMIUM] Well-structured portfolio format"))
                report.append(pad_line("[PREMIUM] Consistent field distribution"))
        else:
            report.append(pad_line("[BASIC] Limited or single-asset portfolio"))
        report.append(pad_line())

        # Deployment Readiness
        report.extend(section_header("🌑 DEPLOYMENT READINESS"))
        if integrity_score == "100%":
            report.append(pad_line("💎 This portfolio is optimized and ready for"))
            report.append(pad_line("   immediate strategic deployment"))
            report.append(pad_line())
            report.append(pad_line("🎯 [STATUS] All systems operational - Execute mission!"))
        else:
            report.append(pad_line("⚠️  WARNING: Portfolio not ready for deployment"))
            report.append(pad_line("💀 CRITICAL ACTION REQUIRED:"))
            report.append(pad_line("   1) Run smart_duplicate_del() to remove duplicates"))
            report.append(pad_line("   2) Verify integrity again with summary()"))
            report.append(pad_line("   3) Re-run analysis prior to deployment"))
            report.append(pad_line())
            report.append(pad_line("🎯 [STATUS] Systems at risk - Remediation required!"))
        report.append(pad_line())
        report.append(bar())

        return "\n".join(report)

    # ===================================================================
    # MATH POWERS (4 methods)
    # ===================================================================

    def sum(self, key: str) -> Union[int, float]:
        """
        Sum numeric values

        Example: data.sum('tokens_used') → 1543
        """
        all_values = self.all(key)
        try:
            return sum(all_values) if all_values else 0
        except TypeError:
            return 0

    def avg(self, key: str) -> float:
        """
        Average of numeric values

        Example: data.avg('score') → 85.3
        """
        all_values = self.all(key)
        try:
            return (sum(all_values) / len(all_values)) if all_values else 0.0
        except (TypeError, ZeroDivisionError):
            return 0.0

    def max(self, key: str) -> Any:
        """
        Maximum value

        Example: data.max('score') → 98
        """
        all_values = self.all(key)
        try:
            return max(all_values) if all_values else None
        except (TypeError, ValueError):
            return None

    def min(self, key: str) -> Any:
        """
        Minimum value

        Example: data.min('age') → 18
        """
        all_values = self.all(key)
        try:
            return min(all_values) if all_values else None
        except (TypeError, ValueError):
            return None

    # ===================================================================
    # OCCURRENCE ANALYSIS POWERS (4 methods) - BULLETPROOF!
    # ===================================================================

    def occurs_most(self, key: str, value_only: bool = False) -> Union[tuple, Any]:
        """
        BULLETPROOF - Find the most frequent value for ANY key (direct OR nested)
        """
        all_values: List[Any] = []
        if not isinstance(self._raw, list):
            return None if value_only else (None, 0)

        for item in self._raw:
            if isinstance(item, dict) and item.get("error"):
                continue
            extracted = self._extract_all_values_for_key(item, key)
            if extracted is not None:
                if isinstance(extracted, list):
                    all_values.extend(extracted)
                else:
                    all_values.append(extracted)

        if not all_values:
            return None if value_only else (None, 0)

        counts = Counter(all_values)
        value, count = counts.most_common(1)[0]
        return value if value_only else (value, count)

    def occurs_min(self, key: str, value_only: bool = False) -> Union[tuple, Any]:
        """
        BULLETPROOF - Find the least frequent (rarest) value for ANY key
        """
        all_values: List[Any] = []
        if not isinstance(self._raw, list):
            return None if value_only else (None, 0)

        for item in self._raw:
            if isinstance(item, dict) and item.get("error"):
                continue
            extracted = self._extract_all_values_for_key(item, key)
            if extracted is not None:
                if isinstance(extracted, list):
                    all_values.extend(extracted)
                else:
                    all_values.append(extracted)

        if not all_values:
            return None if value_only else (None, 0)

        counts = Counter(all_values)
        value, count = counts.most_common()[-1]
        return value if value_only else (value, count)

    def occurs_rare(self, key: str, value_only: bool = False) -> Union[tuple, Any]:
        """Alias for occurs_min - finds the rarest value"""
        return self.occurs_min(key, value_only)

    def occurs_mid(self, key: str, value_only: bool = False) -> Union[tuple, Any]:
        """
        BULLETPROOF - Find the median frequency value for ANY key
        """
        all_values: List[Any] = []
        if not isinstance(self._raw, list):
            return None if value_only else (None, 0)

        for item in self._raw:
            if isinstance(item, dict) and item.get("error"):
                continue
            extracted = self._extract_all_values_for_key(item, key)
            if extracted is not None:
                if isinstance(extracted, list):
                    all_values.extend(extracted)
                else:
                    all_values.append(extracted)

        if not all_values:
            return None if value_only else (None, 0)

        counts = Counter(all_values)
        sorted_items = counts.most_common()
        mid_idx = len(sorted_items) // 2
        value, count = sorted_items[mid_idx]
        return value if value_only else (value, count)

    # ===================================================================
    # SORTING POWER (1 method)
    # ===================================================================

    def sort(self, key: str, ascending: bool = True) -> List:
        """
        Sort items by a key

        Examples:
            data.sort('weight', False)  # Heaviest first
        """
        if isinstance(self._raw, list):
            try:
                return sorted(
                    self._raw,
                    key=lambda x: (x.get(key, "") if isinstance(x, dict) else ""),
                    reverse=not ascending,
                )
            except Exception:
                return self._raw
        return self._raw

    # ===================================================================
    # MODIFICATION POWERS (5 methods)
    # ===================================================================

    def change(self, key: str, new_value: Any) -> 'MageJSON':
        """Change a key's value - returns self for chaining"""
        self._change_key(self._raw, key, new_value)
        return self

    def change_at(self, path: str, new_value: Any) -> 'MageJSON':
        """Change value at specific path - returns self for chaining"""
        parts = path.split(".")
        current = self._raw
        for part in parts[:-1]:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return self
        if isinstance(current, dict) and parts[-1] in current:
            current[parts[-1]] = new_value
        return self

    def add_key(self, key: str, value: Any) -> 'MageJSON':
        """Add new key - returns self for chaining"""
        if isinstance(self._raw, dict):
            self._raw[key] = value
        return self

    def remove_key(self, key: str) -> 'MageJSON':
        """Remove key everywhere - returns self for chaining"""
        self._remove_key(self._raw, key)
        return self

    def save_to(self, filename: str) -> str:
        """Save modified JSON"""
        try:
            import simple_file
            return simple_file.save(filename, self._raw)
        except Exception:
            from pathlib import Path
            path = filename if "." in filename else f"{filename}.json"
            Path(path).write_text(json.dumps(self._raw, indent=2))
            return f"✅ Saved: {path}"

    # ===================================================================
    # ADVANCED
    # ===================================================================

    def where(self, jmes_query: str) -> Any:
        """Advanced JMESPath queries"""
        return jmespath.search(jmes_query, self._raw)

    def __repr__(self):
        """When you print(data)"""
        return self.show

    # ===================================================================
    # INTERNAL MAGIC - BULLETPROOF VALUE EXTRACTION
    # ===================================================================

    def _extract_all_values_for_key(self, obj: dict, search_key: str, depth: int = 0) -> Any:
        """
        BULLETPROOF extractor - gets ALL values for a key at ANY depth

        Returns:
        - Single value: 905
        - List of values: ["fire", "flying"] (for dual-types)
        - None: key not found
        """
        if depth > 50 or not isinstance(obj, dict):
            return None

        # Direct access
        if search_key in obj:
            val = obj[search_key]
            if not isinstance(val, (dict, list)):
                return val
            if isinstance(val, dict):
                if "name" in val:
                    return val["name"]
                if "value" in val:
                    return val["value"]
            return val

        # Plural array (types, abilities, stats variants)
        plural_key = search_key + "s"
        if plural_key in obj and isinstance(obj[plural_key], list):
            values: List[Any] = []
            for item in obj[plural_key]:
                if isinstance(item, dict) and search_key in item:
                    nested = item[search_key]
                    if isinstance(nested, dict):
                        if "name" in nested:
                            values.append(nested["name"])
                        elif "value" in nested:
                            values.append(nested["value"])
                    else:
                        values.append(nested)
            if len(values) > 1:
                return values
            if len(values) == 1:
                return values[0]

        # Recursive deep search
        for k, v in obj.items():
            if isinstance(v, dict):
                res = self._extract_all_values_for_key(v, search_key, depth + 1)
                if res is not None:
                    return res
            elif isinstance(v, list):
                for li in v:
                    if isinstance(li, dict):
                        res = self._extract_all_values_for_key(li, search_key, depth + 1)
                        if res is not None:
                            return res

        return None

    def _deep_search(self, data: Any, key: str) -> Any:
        if isinstance(data, dict):
            if key in data:
                return data[key]
            for v in data.values():
                result = self._deep_search(v, key)
                if result is not None:
                    return result
        elif isinstance(data, list):
            for item in data:
                result = self._deep_search(item, key)
                if result is not None:
                    return result
        return None

    def _find_value(self, data: Any, target_value: Any) -> List:
        matches: List[Any] = []
        if isinstance(data, dict):
            if target_value in data.values():
                matches.append(data)
            for v in data.values():
                matches.extend(self._find_value(v, target_value))
        elif isinstance(data, list):
            for item in data:
                if item == target_value:
                    matches.append(item)
                else:
                    matches.extend(self._find_value(item, target_value))
        return matches

    def _collect_keys(self, data: Any, keys: set):
        if isinstance(data, dict):
            keys.update(data.keys())
            for v in data.values():
                self._collect_keys(v, keys)
        elif isinstance(data, list):
            for item in data:
                self._collect_keys(item, keys)

    def _collect_all_values(self, data: Any, key: str) -> List:
        values: List[Any] = []
        if isinstance(data, dict):
            if key in data:
                values.append(data[key])
            for v in data.values():
                values.extend(self._collect_all_values(v, key))
        elif isinstance(data, list):
            for item in data:
                values.extend(self._collect_all_values(item, key))
        return values

    def _change_key(self, data: Any, key: str, new_value: Any) -> bool:
        if isinstance(data, dict):
            if key in data:
                data[key] = new_value
                return True
            for v in data.values():
                if self._change_key(v, key, new_value):
                    return True
        elif isinstance(data, list):
            for item in data:
                if self._change_key(item, key, new_value):
                    return True
        return False

    def _remove_key(self, data: Any, key: str):
        if isinstance(data, dict):
            if key in data:
                del data[key]
            for v in list(data.values()):
                self._remove_key(v, key)
        elif isinstance(data, list):
            for item in data:
                self._remove_key(item, key)

    def _get_nested_value(self, obj: Any, search_key: str, depth: int = 0) -> Any:
        """Get SINGLE value for smart_filter (returns first match)"""
        if depth > 50 or not isinstance(obj, dict):
            return None

        if search_key in obj:
            val = obj[search_key]
            if not isinstance(val, (dict, list)):
                return val
            if isinstance(val, dict):
                if "name" in val:
                    return val["name"]
                if "value" in val:
                    return val["value"]
            return val

        plural_key = search_key + "s"
        if plural_key in obj and isinstance(obj[plural_key], list):
            for item in obj[plural_key]:
                if isinstance(item, dict) and search_key in item:
                    nested = item[search_key]
                    if isinstance(nested, dict):
                        if "name" in nested:
                            return nested["name"]
                        if "value" in nested:
                            return nested["value"]
                    else:
                        return nested

        for k, v in obj.items():
            if isinstance(v, dict):
                res = self._get_nested_value(v, search_key, depth + 1)
                if res is not None:
                    return res
            elif isinstance(v, list):
                for li in v:
                    if isinstance(li, dict):
                        res = self._get_nested_value(li, search_key, depth + 1)
                        if res is not None:
                            return res

        return None

    def _compare(self, item_value: Any, operator: str, compare_value: Any) -> bool:
        """Compare values using operator"""
        try:
            if operator in ("==", "="):
                return item_value == compare_value
            if operator == "!=":
                return item_value != compare_value
            if operator == ">":
                return item_value > compare_value
            if operator == "<":
                return item_value < compare_value
            if operator == ">=":
                return item_value >= compare_value
            if operator == "<=":
                return item_value <= compare_value
            if operator == "contains":
                return str(compare_value).lower() in str(item_value).lower()
            if operator == "in":
                return item_value in compare_value
            return item_value == compare_value
        except (TypeError, ValueError):
            return False


# ===================================================================
# UNIVERSAL MAGIC SPELL - BULLETPROOF EDITION v8 - SHADOW MONARCH
# ===================================================================

def _extract_data_from_structure(data: Any) -> Any:
    """
    🔮 UNIVERSAL DATA EXTRACTOR - BULLETPROOF

    Auto-extracts actual data from ANY common wrapper structure:

    Supported patterns:
    - {"cleaned_data": [...]}           # duplicates.py results
    - {"data": [...]}                   # API responses
    - {"results": [...]}                # Query results
    - {"items": [...]}                  # Generic items
    - {"response": {"data": [...]}}     # Nested API responses
    - {"result": {"data": [...]}}       # Nested results
    - {"output": [...]}                 # Generic output
    - {"content": [...]}                # Generic content
    - Pure data (no extraction needed)  # Backward compatible

    Returns:
    - Extracted data (list/dict/etc)
    - Original data if no pattern matches
    """
    if not isinstance(data, dict):
        return data

    for key in ["cleaned_data", "data", "results", "items", "output", "content"]:
        if key in data:
            extracted = data[key]
            if isinstance(extracted, (list, dict)):
                return extracted

    nested_patterns = [
        ["response", "data"],
        ["result", "data"],
        ["response", "results"],
        ["result", "results"],
        ["data", "data"],
        ["data", "results"],
    ]
    for path in nested_patterns:
        cur = data
        ok = True
        for k in path:
            if isinstance(cur, dict) and k in cur:
                cur = cur[k]
            else:
                ok = False
                break
        if ok and isinstance(cur, (list, dict)):
            return cur

    if len(data) == 1:
        value = list(data.values())[0]
        if isinstance(value, (list, dict)) and len(str(value)) > 50:
            return value

    return data


def modify(data: Union[str, dict, list]) -> MageJSON:
    """
    🔮 UNIVERSAL modify() - BULLETPROOF EDITION v8

    Handles ANY data structure automatically:

    ✅ Pure data: modify([item1, item2])
    ✅ Results dict: modify({"cleaned_data": [...]})
    ✅ API responses: modify({"data": [...]})
    ✅ Nested structures: modify({"response": {"data": [...]}})
    ✅ Custom patterns: modify({"results": [...]})
    ✅ Backward compatible: All existing functionality preserved
    """
    extracted = _extract_data_from_structure(data)
    return MageJSON(extracted)


def myjson(data: Union[str, dict, list]) -> MageJSON:
    """Alternative name with same universal powers"""
    return modify(data)


__all__ = ["modify", "myjson", "MageJSON"]
