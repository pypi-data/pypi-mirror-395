"""
NLP Analyzer for Enhanced Green Software Pattern Detection

Implements Natural Language Processing techniques from Soliman et al. (2017):
- Morphological analysis (stemming, lemmatization)
- Semantic matching (word embeddings, synonyms)
- Multi-term phrase matching

Addresses limitation: Current keyword matching misses variants like:
- optimize → optimizing, optimized, optimization
- cache → caching, cached, caches
- efficient → efficiency, efficiently
"""

from __future__ import annotations

import re
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass


@dataclass
class NLPMatch:
    """Represents an NLP-enhanced pattern match"""

    original_term: str
    matched_variant: str
    position: int
    context: str
    match_type: str  # 'exact', 'stemmed', 'semantic'


class NLPAnalyzer:
    """
    Enhanced pattern detection using NLP techniques.

    Implements:
    1. Stemming/Lemmatization (catch morphological variants)
    2. Synonym expansion (semantic matching)
    3. Phrase pattern matching (multi-word expressions)

    Based on Soliman et al. findings: 26/151 studies used NLP techniques
    """

    def __init__(self, enable_stemming: bool = True, enable_synonyms: bool = True):
        """
        Initialize NLP analyzer.

        Args:
            enable_stemming: Enable morphological analysis
            enable_synonyms: Enable semantic synonym matching
        """
        self.enable_stemming = enable_stemming
        self.enable_synonyms = enable_synonyms

        # Simple stemming rules (Porter-like)
        self._stemming_rules = {
            "optimization": "optim",
            "optimizing": "optim",
            "optimized": "optim",
            "optimize": "optim",
            "caching": "cache",
            "cached": "cache",
            "caches": "cache",
            "efficient": "effic",
            "efficiency": "effic",
            "efficiently": "effic",
            "compressed": "compress",
            "compressing": "compress",
            "compression": "compress",
            "scaling": "scale",
            "scaled": "scale",
            "scalable": "scale",
            "scalability": "scale",
            "monitoring": "monitor",
            "monitored": "monitor",
            "profiling": "profil",
            "profiled": "profil",
            "recycling": "recycl",
            "recycled": "recycl",
            "reducing": "reduc",
            "reduced": "reduc",
            "reduction": "reduc",
            "minimizing": "minim",
            "minimized": "minim",
            "minimization": "minim",
            "containerized": "container",
            "containerization": "container",
            "containerizing": "container",
        }

        # Semantic synonyms for green concepts
        self._synonyms = {
            "cache": ["buffer", "memoize", "store", "retain"],
            "optimize": ["improve", "enhance", "tune", "refine", "streamline"],
            "efficient": ["performant", "fast", "quick", "lean", "lightweight"],
            "reduce": ["decrease", "minimize", "lower", "cut", "shrink", "lessen"],
            "compress": ["compact", "shrink", "minify", "pack"],
            "monitor": ["track", "measure", "observe", "watch", "profile"],
            "scale": ["grow", "expand", "adapt", "resize"],
            "green": ["sustainable", "eco-friendly", "carbon-aware", "energy-efficient"],
            "power": ["energy", "electricity", "consumption", "usage"],
            "resource": ["memory", "cpu", "compute", "capacity"],
        }

        # Multi-word phrases (higher precision)
        self._phrase_patterns = [
            r"reduce\s+(memory|cpu|power|energy|resource)",
            r"optimize\s+(performance|efficiency|resource|memory)",
            r"improve\s+(efficiency|performance|throughput)",
            r"lazy\s+load(ing)?",
            r"connection\s+pool(ing)?",
            r"batch\s+process(ing)?",
            r"data\s+compress(ion)?",
            r"auto\s*scal(ing|e)",
            r"load\s+balanc(ing|er)",
            r"circuit\s+breaker",
            r"rate\s+limit(ing|er)",
            r"(horizontal|vertical)\s+scal(ing|e)",
            r"serverless\s+(function|architecture)",
            r"container\s+orchestration",
            r"micro\s*service",
            r"event\s+driven",
            r"reactive\s+(programming|stream)",
            r"asynchronous\s+process(ing)?",
            r"parallel\s+process(ing)?",
            r"distributed\s+(cache|caching)",
            r"in-memory\s+(cache|database)",
            r"edge\s+computing",
            r"cdn\s+(cache|integration)",
            r"database\s+(index|indexing)",
            r"query\s+(optimization|cache)",
            r"api\s+(rate|throttl)",
            r"graceful\s+degrad(ation|e)",
            r"back\s*pressure",
            r"bulkhead\s+pattern",
        ]

    def stem_word(self, word: str) -> str:
        """
        Apply simple stemming to word.

        Args:
            word: Input word (lowercase)

        Returns:
            Stemmed form of word
        """
        word_lower = word.lower()

        # Use predefined stems
        if word_lower in self._stemming_rules:
            return self._stemming_rules[word_lower]

        # Simple suffix removal
        for suffix in ["ing", "ed", "es", "s", "tion", "ation", "ment", "ity", "ly", "er"]:
            if word_lower.endswith(suffix) and len(word_lower) > len(suffix) + 2:
                return word_lower[: -len(suffix)]

        return word_lower

    def get_synonyms(self, word: str) -> Set[str]:
        """
        Get semantic synonyms for word.

        Args:
            word: Input word (lowercase)

        Returns:
            Set of synonyms including original word
        """
        word_lower = word.lower()
        synonyms = {word_lower}

        if word_lower in self._synonyms:
            synonyms.update(self._synonyms[word_lower])

        return synonyms

    def find_morphological_matches(self, text: str, base_keywords: List[str]) -> List[NLPMatch]:
        """
        Find keyword matches including morphological variants.

        Args:
            text: Text to search (commit message or code)
            base_keywords: List of base keywords to match

        Returns:
            List of NLPMatch objects with stemmed matches
        """
        if not self.enable_stemming:
            return []

        matches = []
        text_lower = text.lower()
        words = re.findall(r"\b\w+\b", text_lower)

        # Build stem lookup
        stemmed_keywords = {self.stem_word(kw): kw for kw in base_keywords}

        for i, word in enumerate(words):
            stemmed_word = self.stem_word(word)
            if stemmed_word in stemmed_keywords:
                original_kw = stemmed_keywords[stemmed_word]

                # Find position in original text
                position = text_lower.find(word)

                # Extract context (10 chars before and after)
                context_start = max(0, position - 10)
                context_end = min(len(text), position + len(word) + 10)
                context = text[context_start:context_end]

                matches.append(
                    NLPMatch(
                        original_term=original_kw,
                        matched_variant=word,
                        position=position,
                        context=context,
                        match_type="stemmed",
                    )
                )

        return matches

    def find_semantic_matches(self, text: str, base_keywords: List[str]) -> List[NLPMatch]:
        """
        Find keyword matches including semantic synonyms.

        Args:
            text: Text to search
            base_keywords: List of base keywords

        Returns:
            List of NLPMatch objects with semantic matches
        """
        if not self.enable_synonyms:
            return []

        matches = []
        text_lower = text.lower()

        for keyword in base_keywords:
            synonyms = self.get_synonyms(keyword)

            for synonym in synonyms:
                if synonym == keyword:  # Skip exact match (already covered)
                    continue

                # Find all occurrences
                pattern = r"\b" + re.escape(synonym) + r"\b"
                for match in re.finditer(pattern, text_lower, re.IGNORECASE):
                    position = match.start()
                    context_start = max(0, position - 10)
                    context_end = min(len(text), position + len(synonym) + 10)
                    context = text[context_start:context_end]

                    matches.append(
                        NLPMatch(
                            original_term=keyword,
                            matched_variant=synonym,
                            position=position,
                            context=context,
                            match_type="semantic",
                        )
                    )

        return matches

    def find_phrase_patterns(self, text: str) -> List[NLPMatch]:
        """
        Find multi-word phrase patterns indicating green practices.

        Args:
            text: Text to search

        Returns:
            List of NLPMatch objects with phrase matches
        """
        matches = []
        text_lower = text.lower()

        for pattern in self._phrase_patterns:
            for match in re.finditer(pattern, text_lower, re.IGNORECASE):
                matched_phrase = match.group(0)
                position = match.start()
                context_start = max(0, position - 10)
                context_end = min(len(text), position + len(matched_phrase) + 10)
                context = text[context_start:context_end]

                matches.append(
                    NLPMatch(
                        original_term="phrase_pattern",
                        matched_variant=matched_phrase,
                        position=position,
                        context=context,
                        match_type="phrase",
                    )
                )

        return matches

    def analyze_text(self, text: str, base_keywords: List[str]) -> Dict:
        """
        Comprehensive NLP analysis of text.

        Args:
            text: Text to analyze (commit message or code)
            base_keywords: Base keywords from GSF patterns

        Returns:
            Dictionary with:
            - morphological_matches: List of stemmed matches
            - semantic_matches: List of synonym matches
            - phrase_matches: List of phrase pattern matches
            - total_nlp_matches: Total unique matches
            - match_density: Matches per 100 words
        """
        morphological = self.find_morphological_matches(text, base_keywords)
        semantic = self.find_semantic_matches(text, base_keywords)
        phrases = self.find_phrase_patterns(text)

        # Calculate metrics
        word_count = len(re.findall(r"\b\w+\b", text))
        total_matches = len(morphological) + len(semantic) + len(phrases)
        match_density = (total_matches / word_count * 100) if word_count > 0 else 0

        return {
            "morphological_matches": morphological,
            "semantic_matches": semantic,
            "phrase_matches": phrases,
            "total_nlp_matches": total_matches,
            "match_density": round(match_density, 2),
            "word_count": word_count,
        }

    def enhance_pattern_detection(
        self, text: str, original_keywords: List[str]
    ) -> Tuple[bool, List[str]]:
        """
        Enhance original keyword detection with NLP techniques.

        Args:
            text: Text to analyze
            original_keywords: Keywords that were already detected

        Returns:
            Tuple of (has_additional_matches, additional_matched_terms)
        """
        analysis = self.analyze_text(text, original_keywords)

        additional_terms = []

        # Collect additional matched terms
        for match in analysis["morphological_matches"]:
            if match.matched_variant not in original_keywords:
                additional_terms.append(f"{match.matched_variant} (stem: {match.original_term})")

        for match in analysis["semantic_matches"]:
            additional_terms.append(f"{match.matched_variant} (synonym: {match.original_term})")

        for match in analysis["phrase_matches"]:
            additional_terms.append(f"'{match.matched_variant}' (phrase)")

        return len(additional_terms) > 0, additional_terms
