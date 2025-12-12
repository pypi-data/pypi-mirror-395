"""
FormattingHandler for docx-json-replacer
Handles parsing and applying document formatting tags like titles, headings, and bullets.
"""
import re
from typing import List, Dict, Tuple, Any, Optional


class FormattingHandler:
    """Handles parsing and applying document formatting tags"""

    # Tag pattern to match [dx-xxx]
    TAG_PATTERN = re.compile(r'\[dx-(title|subtitle|h[1-4]|bullet|br|tab)\]')

    # Inline tag pattern for tabs (used for text replacement)
    INLINE_TAB_PATTERN = re.compile(r'\[dx-tab\]')

    # Bullet detection patterns
    ALPHA_LOWER_PATTERN = re.compile(r'^([a-z])\)\s*')   # a)
    ALPHA_UPPER_PATTERN = re.compile(r'^([A-Z])\)\s*')   # A)
    NUMBER_PATTERN = re.compile(r'^(\d+)[\.\)]\s*')      # 1. or 1)
    ROMAN_LOWER_PATTERN = re.compile(r'^([ivxlcdm]+)\)\s*', re.IGNORECASE)  # i) or I)

    # Word style mappings
    STYLE_MAP = {
        'title': 'Title',
        'subtitle': 'Subtitle',
        'h1': 'Heading 1',
        'h2': 'Heading 2',
        'h3': 'Heading 3',
        'h4': 'Heading 4',
    }

    # Bullet type constants
    BULLET_TYPE_BULLET = 'bullet'
    BULLET_TYPE_NUMBER = 'number'
    BULLET_TYPE_ALPHA_LOWER = 'alpha_lower'
    BULLET_TYPE_ALPHA_UPPER = 'alpha_upper'
    BULLET_TYPE_ROMAN_LOWER = 'roman_lower'
    BULLET_TYPE_ROMAN_UPPER = 'roman_upper'

    def has_formatting_tags(self, value: Any) -> bool:
        """Check if value contains any formatting tags"""
        if not isinstance(value, str):
            return False
        return bool(self.TAG_PATTERN.search(value))

    def replace_inline_tabs(self, text: str) -> str:
        """Replace [dx-tab] with actual tab characters"""
        if not isinstance(text, str):
            return text
        return self.INLINE_TAB_PATTERN.sub('\t', text)

    def parse_formatted_content(self, value: str) -> List[Dict[str, Any]]:
        """
        Parse value with formatting tags into list of paragraph specifications.

        Args:
            value: String containing formatting tags like [dx-title], [dx-h1], etc.

        Returns:
            List of dicts with keys:
            - 'style': Word style name (e.g., 'Heading 1', 'Title')
            - 'text': The content text
            - 'bullet_type': For bullets, the type ('bullet', 'number', 'alpha_lower', etc.)
            - 'is_bullet': Boolean indicating if this is a bullet item
        """
        if not isinstance(value, str):
            return []

        result = []

        # Split by [dx-br] to get individual segments
        segments = re.split(r'\[dx-br\]', value)

        for segment in segments:
            segment = segment.strip()
            if not segment:
                continue

            # Check for formatting tag at the start
            tag_match = self.TAG_PATTERN.match(segment)

            if tag_match:
                tag_type = tag_match.group(1)
                content = segment[tag_match.end():].strip()

                if tag_type == 'br':
                    # [dx-br] alone - skip (already handled by split)
                    continue
                elif tag_type == 'tab':
                    # [dx-tab] is handled inline, skip as block tag
                    continue
                elif tag_type == 'bullet':
                    # Detect bullet type and clean the text
                    bullet_type, cleaned_text = self.detect_bullet_type(content)

                    if cleaned_text:  # Only add if there's content
                        result.append({
                            'style': self._get_bullet_style(bullet_type),
                            'text': cleaned_text,
                            'bullet_type': bullet_type,
                            'is_bullet': True
                        })
                else:
                    # Title, subtitle, or heading
                    style = self.STYLE_MAP.get(tag_type, 'Normal')
                    if content:  # Only add if there's content
                        result.append({
                            'style': style,
                            'text': content,
                            'bullet_type': None,
                            'is_bullet': False
                        })
            else:
                # No tag - treat as normal paragraph
                if segment:
                    result.append({
                        'style': 'Normal',
                        'text': segment,
                        'bullet_type': None,
                        'is_bullet': False
                    })

        return result

    def detect_bullet_type(self, text: str) -> Tuple[str, str]:
        """
        Detect bullet type from text content and return cleaned text.

        The prefix (a), 1., i)) is stripped - Word will generate the numbers.

        Args:
            text: The text after [dx-bullet] tag

        Returns:
            Tuple of (bullet_type, cleaned_text)
            bullet_type is one of: 'bullet', 'number', 'alpha_lower', 'alpha_upper',
                                   'roman_lower', 'roman_upper'
        """
        if not text:
            return self.BULLET_TYPE_BULLET, ''

        text = text.strip()

        # Check for numbered list: 1. or 1)
        number_match = self.NUMBER_PATTERN.match(text)
        if number_match:
            cleaned = text[number_match.end():].strip()
            return self.BULLET_TYPE_NUMBER, cleaned

        # Check for roman numerals FIRST (before alpha, since i, v, x, etc. could be both)
        # Only treat as roman if it's a valid roman numeral pattern
        roman_match = self.ROMAN_LOWER_PATTERN.match(text)
        if roman_match:
            roman_str = roman_match.group(1)
            # Check if it's a valid roman numeral (not just single letters like 'a', 'b')
            if self._is_valid_roman(roman_str) and len(roman_str) > 1:
                # Multi-character roman numeral (ii, iii, iv, etc.)
                cleaned = text[roman_match.end():].strip()
                if roman_str == roman_str.lower():
                    return self.BULLET_TYPE_ROMAN_LOWER, cleaned
                else:
                    return self.BULLET_TYPE_ROMAN_UPPER, cleaned
            elif roman_str.lower() in ['i', 'v', 'x', 'l', 'c', 'd', 'm']:
                # Single roman numeral characters - only treat as roman if followed by )
                # and the context suggests a roman list (ambiguous - default to alpha for single chars)
                # For now, single letters default to alpha
                pass

        # Check for lowercase alpha: a)
        alpha_lower_match = self.ALPHA_LOWER_PATTERN.match(text)
        if alpha_lower_match:
            cleaned = text[alpha_lower_match.end():].strip()
            return self.BULLET_TYPE_ALPHA_LOWER, cleaned

        # Check for uppercase alpha: A)
        alpha_upper_match = self.ALPHA_UPPER_PATTERN.match(text)
        if alpha_upper_match:
            cleaned = text[alpha_upper_match.end():].strip()
            return self.BULLET_TYPE_ALPHA_UPPER, cleaned

        # Default: standard bullet
        return self.BULLET_TYPE_BULLET, text

    def _is_valid_roman(self, s: str) -> bool:
        """Check if string is a valid roman numeral"""
        s = s.upper()
        # Simple validation - only allow common roman numerals
        valid_roman = re.compile(r'^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$')
        return bool(valid_roman.match(s)) and len(s) > 0

    def _get_bullet_style(self, bullet_type: str) -> str:
        """
        Get the Word style name for a bullet type.

        For standard bullets and numbers, we use built-in styles.
        For alpha and roman, we'll need custom numbering (handled in docx_replacer).
        """
        if bullet_type == self.BULLET_TYPE_NUMBER:
            return 'List Number'
        elif bullet_type == self.BULLET_TYPE_BULLET:
            return 'List Bullet'
        else:
            # Alpha and Roman need custom handling but start with List Number
            return 'List Number'

    def get_numbering_format(self, bullet_type: str) -> Optional[str]:
        """
        Get the Word numbering format for custom bullet types.

        Returns:
            The numFmt value for Word XML, or None for standard bullet
        """
        format_map = {
            self.BULLET_TYPE_NUMBER: 'decimal',
            self.BULLET_TYPE_ALPHA_LOWER: 'lowerLetter',
            self.BULLET_TYPE_ALPHA_UPPER: 'upperLetter',
            self.BULLET_TYPE_ROMAN_LOWER: 'lowerRoman',
            self.BULLET_TYPE_ROMAN_UPPER: 'upperRoman',
            self.BULLET_TYPE_BULLET: None
        }
        return format_map.get(bullet_type)
