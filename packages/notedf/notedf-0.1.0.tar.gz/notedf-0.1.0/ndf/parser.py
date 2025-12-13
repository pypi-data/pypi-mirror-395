"""
NDF Parser - Note Data Format
Simple, compact, model-optimized data format

Usage:
    from ndf import NoteDataFormat
    
    parser = NoteDataFormat()
    data = parser.parse(ndf_text)
    ndf_text = parser.dumps(data)
"""

import re
from typing import Any, Dict, List, Union


class NoteDataFormat:
    """Parser for Note Data Format (NDF)"""
    
    def __init__(self):
        self.references = {}
    
    # ============= PUBLIC API =============
    
    def parse(self, text: str) -> Dict[str, Any]:
        """
        Parse NDF text into Python objects
        
        Args:
            text: NDF formatted string
            
        Returns:
            Parsed data as dictionary
        """
        self.references = {}  # Reset references for each parse
        lines = text.strip().split('\n')
        return self._parse_block(lines, 0)[0]
    
    def dumps(self, data: Dict[str, Any], indent: int = 0) -> str:
        """
        Convert Python dict to NDF format
        
        Args:
            data: Dictionary to convert
            indent: Starting indentation level
            
        Returns:
            NDF formatted string
        """
        lines = []
        indent_str = '  ' * indent
        
        for key, value in data.items():
            if isinstance(value, dict):
                lines.append(f'{indent_str}{key}:')
                lines.append(self.dumps(value, indent + 1))
            elif isinstance(value, list):
                lines.append(self._format_list(key, value, indent_str))
            elif isinstance(value, str) and '\n' in value:
                lines.append(self._format_multiline(key, value, indent_str))
            else:
                lines.append(f'{indent_str}{key}: {value}')
        
        return '\n'.join(lines)
    
    # ============= PARSING METHODS =============
    
    def _parse_block(self, lines: List[str], start_indent: int) -> tuple:
        """Parse a block of indented content"""
        result = {}
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # Skip empty lines and comments
            if not line.strip() or line.strip().startswith('#'):
                i += 1
                continue
            
            indent = self._get_indent(line)
            
            # Dedented - done with this block
            if indent < start_indent:
                break
            
            # Skip lines not at our level
            if indent > start_indent:
                i += 1
                continue
            
            # Clean line
            line = self._remove_inline_comment(line).strip()
            
            # Handle references
            if line.startswith('$'):
                i = self._handle_reference(line, i)
                continue
            
            # Parse key-value pair
            if ':' not in line:
                i += 1
                continue
            
            key, value = self._split_key_value(line)
            
            # Multi-line text
            if value == '|':
                result[key], i = self._parse_multiline(lines, i, indent)
                continue
            
            # Nested object
            if not value:
                result[key], i = self._parse_nested(lines, i, indent)
                continue
            
            # Parse value
            result[key] = self._parse_value(value)
            i += 1
        
        return result, i
    
    def _parse_multiline(self, lines: List[str], i: int, indent: int) -> tuple:
        """Parse multi-line text block"""
        text_lines = []
        i += 1
        
        while i < len(lines):
            next_line = lines[i]
            next_indent = self._get_indent(next_line)
            
            if next_indent <= indent and next_line.strip():
                break
            
            text_lines.append(next_line[indent + 2:] if len(next_line) > indent + 2 else '')
            i += 1
        
        return '\n'.join(text_lines).rstrip(), i
    
    def _parse_nested(self, lines: List[str], i: int, indent: int) -> tuple:
        """Parse nested object"""
        nested_start = i + 1
        nested_lines = []
        
        while nested_start < len(lines):
            next_line = lines[nested_start]
            
            if not next_line.strip() or next_line.strip().startswith('#'):
                nested_start += 1
                continue
            
            next_indent = self._get_indent(next_line)
            if next_indent <= indent:
                break
            
            nested_lines.append(next_line)
            nested_start += 1
        
        if nested_lines:
            return self._parse_block(nested_lines, indent + 2)[0], nested_start
        else:
            return None, i + 1
    
    def _parse_value(self, value: str) -> Any:
        """Parse a value into appropriate Python type"""
        value = value.strip()
        
        # Reference
        if value.startswith('$'):
            return self._resolve_reference(value)
        
        # Inline object
        if value.startswith('{') and value.endswith('}'):
            return self._parse_inline_object(value)
        
        # Array
        if value.startswith('[') and value.endswith(']'):
            return self._parse_array(value)
        
        # Type hints
        if value.startswith('@'):
            return self._parse_typed_value(value)
        
        # List (comma or space separated)
        if ',' in value or (' ' in value and not value.startswith('"')):
            items = [item.strip() for item in re.split(r'[,\s]+', value) if item.strip()]
            return [self._parse_simple_value(item) for item in items]
        
        return self._parse_simple_value(value)
    
    def _parse_simple_value(self, value: str) -> Any:
        """Parse a simple value (string, number, boolean, null)"""
        value = value.strip()
        
        # Remove quotes
        if (value.startswith('"') and value.endswith('"')) or \
           (value.startswith("'") and value.endswith("'")):
            return value[1:-1]
        
        # Boolean
        if value.lower() in ('yes', 'true'):
            return True
        if value.lower() in ('no', 'false'):
            return False
        
        # Null
        if value.lower() in ('null', 'none', '-'):
            return None
        
        # Number
        try:
            if '.' in value or 'e' in value.lower():
                return float(value)
            return int(value)
        except ValueError:
            return value
    
    def _parse_inline_object(self, text: str) -> Dict[str, Any]:
        """Parse inline object: {key: value, key2: value2}"""
        text = text.strip()[1:-1]
        result = {}
        
        pairs = text.split(',')
        for pair in pairs:
            if ':' not in pair:
                continue
            key, value = pair.split(':', 1)
            result[key.strip()] = self._parse_simple_value(value.strip())
        
        return result
    
    def _parse_array(self, text: str) -> List[Any]:
        """Parse array: [1, 2, 3] or [[1,2],[3,4]]"""
        text = text.strip()[1:-1]
        
        # Handle nested arrays
        if '[' in text:
            result = []
            depth = 0
            item = ''
            
            for char in text + ',':
                if char == '[':
                    depth += 1
                    item += char
                elif char == ']':
                    depth -= 1
                    item += char
                elif char == ',' and depth == 0:
                    if item.strip():
                        if item.strip().startswith('['):
                            result.append(self._parse_array(item.strip()))
                        else:
                            result.append(self._parse_simple_value(item.strip()))
                    item = ''
                else:
                    item += char
            
            return result
        
        # Simple array
        items = [item.strip() for item in text.split(',') if item.strip()]
        return [self._parse_simple_value(item) for item in items]
    
    def _parse_typed_value(self, value: str) -> Any:
        """Parse typed values with hints like @time, @f32[], etc."""
        parts = value.split(maxsplit=1)
        if len(parts) != 2:
            return value
        
        type_hint, actual_value = parts
        
        if type_hint == '@time':
            return {'_type': 'timestamp', 'value': actual_value}
        elif type_hint.startswith('@f') and '[' in type_hint:
            return [float(x.strip()) for x in actual_value.split(',')]
        elif type_hint == '@embedding':
            return {'_type': 'embedding', 'data': actual_value}
        
        return actual_value
    
    # ============= REFERENCE HANDLING =============
    
    def _handle_reference(self, line: str, i: int) -> int:
        """Handle reference definition"""
        key, value = line.split(':', 1)
        self.references[key.strip()] = self._parse_value(value.strip())
        return i + 1
    
    def _resolve_reference(self, value: str) -> Any:
        """Resolve reference with optional inline override"""
        ref_key = value.split()[0]
        
        if ref_key not in self.references:
            return value
        
        base = self.references[ref_key]
        if isinstance(base, dict):
            base = base.copy()
        
        # Handle inline overrides: $ref {key: value}
        if '{' in value:
            override = self._parse_inline_object(value[value.index('{'):])
            if isinstance(base, dict):
                base.update(override)
        
        return base
    
    # ============= FORMATTING METHODS =============
    
    def _format_list(self, key: str, value: List[Any], indent_str: str) -> str:
        """Format list for output"""
        if all(isinstance(x, (int, float, str, bool)) for x in value):
            # Simple list
            return f'{indent_str}{key}: {", ".join(map(str, value))}'
        else:
            # Complex list
            lines = [f'{indent_str}{key}:']
            for item in value:
                if isinstance(item, dict):
                    lines.append(self.dumps(item, len(indent_str) // 2 + 1))
                else:
                    lines.append(f'{indent_str}  - {item}')
            return '\n'.join(lines)
    
    def _format_multiline(self, key: str, value: str, indent_str: str) -> str:
        """Format multi-line string for output"""
        lines = [f'{indent_str}{key}: |']
        for line in value.split('\n'):
            lines.append(f'{indent_str}  {line}')
        return '\n'.join(lines)
    
    # ============= HELPER METHODS =============
    
    def _get_indent(self, line: str) -> int:
        """Get indentation level of a line"""
        return len(line) - len(line.lstrip())
    
    def _remove_inline_comment(self, line: str) -> str:
        """Remove inline comment from line"""
        if '#' in line:
            return line[:line.index('#')]
        return line
    
    def _split_key_value(self, line: str) -> tuple:
        """Split line into key and value"""
        key, value = line.split(':', 1)
        return key.strip(), value.strip()