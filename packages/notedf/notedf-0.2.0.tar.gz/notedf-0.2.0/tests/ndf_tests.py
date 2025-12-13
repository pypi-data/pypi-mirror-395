"""
NDF (Note Data Format) - Test Suite
Run with: python -m pytest ndf_tests.py
"""

import pytest
from ndf import NoteDataFormat


class TestBasicParsing:
    """Test basic value parsing"""
    
    def test_simple_string(self):
        parser = NoteDataFormat()
        result = parser.parse("name: John")
        assert result == {'name': 'John'}
    
    def test_integer(self):
        parser = NoteDataFormat()
        result = parser.parse("age: 30")
        assert result == {'age': 30}
    
    def test_float(self):
        parser = NoteDataFormat()
        result = parser.parse("score: 95.5")
        assert result == {'score': 95.5}
    
    def test_boolean_yes(self):
        parser = NoteDataFormat()
        result = parser.parse("active: yes")
        assert result == {'active': True}
    
    def test_boolean_no(self):
        parser = NoteDataFormat()
        result = parser.parse("active: no")
        assert result == {'active': False}
    
    def test_boolean_true(self):
        parser = NoteDataFormat()
        result = parser.parse("active: true")
        assert result == {'active': True}
    
    def test_boolean_false(self):
        parser = NoteDataFormat()
        result = parser.parse("active: false")
        assert result == {'active': False}
    
    def test_null_none(self):
        parser = NoteDataFormat()
        result = parser.parse("value: none")
        assert result == {'value': None}
    
    def test_null_null(self):
        parser = NoteDataFormat()
        result = parser.parse("value: null")
        assert result == {'value': None}
    
    def test_null_dash(self):
        parser = NoteDataFormat()
        result = parser.parse("value: -")
        assert result == {'value': None}


class TestLists:
    """Test list parsing"""
    
    def test_space_separated(self):
        parser = NoteDataFormat()
        result = parser.parse("tags: python ai ml")
        assert result == {'tags': ['python', 'ai', 'ml']}
    
    def test_comma_separated(self):
        parser = NoteDataFormat()
        result = parser.parse("colors: red, blue, green")
        assert result == {'colors': ['red', 'blue', 'green']}
    
    def test_inline_array(self):
        parser = NoteDataFormat()
        result = parser.parse("nums: [1, 2, 3]")
        assert result == {'nums': [1, 2, 3]}
    
    def test_nested_array(self):
        parser = NoteDataFormat()
        result = parser.parse("matrix: [[1,2],[3,4]]")
        assert result == {'matrix': [[1, 2], [3, 4]]}


class TestNestedObjects:
    """Test nested object parsing"""
    
    def test_simple_nested(self):
        parser = NoteDataFormat()
        ndf = """
user:
  name: Alice
  age: 30
"""
        result = parser.parse(ndf)
        assert result == {'user': {'name': 'Alice', 'age': 30}}
    
    def test_deep_nested(self):
        parser = NoteDataFormat()
        ndf = """
user:
  profile:
    name: Alice
    contact:
      email: alice@example.com
"""
        result = parser.parse(ndf)
        expected = {
            'user': {
                'profile': {
                    'name': 'Alice',
                    'contact': {'email': 'alice@example.com'}
                }
            }
        }
        assert result == expected


class TestInlineObjects:
    """Test inline object parsing"""
    
    def test_simple_inline(self):
        parser = NoteDataFormat()
        result = parser.parse("point: {x: 10, y: 20}")
        assert result == {'point': {'x': 10, 'y': 20}}
    
    def test_mixed_types_inline(self):
        parser = NoteDataFormat()
        result = parser.parse("config: {timeout: 30, debug: yes}")
        assert result == {'config': {'timeout': 30, 'debug': True}}


class TestMultilineText:
    """Test multi-line text parsing"""
    
    def test_basic_multiline(self):
        parser = NoteDataFormat()
        ndf = """
text: |
  Line 1
  Line 2
  Line 3
"""
        result = parser.parse(ndf)
        assert result == {'text': 'Line 1\nLine 2\nLine 3'}
    
    def test_multiline_with_empty_lines(self):
        parser = NoteDataFormat()
        ndf = """
text: |
  Line 1
  
  Line 3
"""
        result = parser.parse(ndf)
        assert result == {'text': 'Line 1\n\nLine 3'}


class TestComments:
    """Test comment handling"""
    
    def test_full_line_comment(self):
        parser = NoteDataFormat()
        ndf = """
# This is a comment
name: Alice
"""
        result = parser.parse(ndf)
        assert result == {'name': 'Alice'}
    
    def test_inline_comment(self):
        parser = NoteDataFormat()
        result = parser.parse("name: Alice  # user name")
        assert result == {'name': 'Alice'}
    
    def test_multiple_comments(self):
        parser = NoteDataFormat()
        ndf = """
# Comment 1
name: Alice
# Comment 2
age: 30
"""
        result = parser.parse(ndf)
        assert result == {'name': 'Alice', 'age': 30}


class TestReferences:
    """Test reference/template functionality"""
    
    def test_basic_reference(self):
        parser = NoteDataFormat()
        ndf = """
$template:
  role: member

user: $template
"""
        result = parser.parse(ndf)
        assert 'user' in result
        assert result['user'] == {'role': 'member'}
    
    def test_reference_with_override(self):
        parser = NoteDataFormat()
        ndf = """
$template:
  role: member
  active: yes

user: $template {name: Alice}
"""
        result = parser.parse(ndf)
        expected = {'user': {'role': 'member', 'active': True, 'name': 'Alice'}}
        assert result == expected


class TestDumps:
    """Test serialization (dumps)"""
    
    def test_simple_dumps(self):
        parser = NoteDataFormat()
        data = {'name': 'Alice', 'age': 30}
        result = parser.dumps(data)
        # Parse it back to verify
        parsed = parser.parse(result)
        assert parsed == data
    
    def test_nested_dumps(self):
        parser = NoteDataFormat()
        data = {
            'user': {
                'name': 'Alice',
                'settings': {'theme': 'dark'}
            }
        }
        result = parser.dumps(data)
        parsed = parser.parse(result)
        assert parsed == data
    
    def test_list_dumps(self):
        parser = NoteDataFormat()
        data = {'tags': ['python', 'ai', 'ml']}
        result = parser.dumps(data)
        parsed = parser.parse(result)
        assert parsed == data


class TestRoundTrip:
    """Test parse -> dumps -> parse consistency"""
    
    def test_simple_roundtrip(self):
        parser = NoteDataFormat()
        original = "name: Alice\nage: 30"
        parsed = parser.parse(original)
        dumped = parser.dumps(parsed)
        reparsed = parser.parse(dumped)
        assert reparsed == parsed
    
    def test_nested_roundtrip(self):
        parser = NoteDataFormat()
        original = """
user:
  name: Alice
  settings:
    theme: dark
"""
        parsed = parser.parse(original)
        dumped = parser.dumps(parsed)
        reparsed = parser.parse(dumped)
        assert reparsed == parsed


class TestEdgeCases:
    """Test edge cases and special scenarios"""
    
    def test_empty_string(self):
        parser = NoteDataFormat()
        result = parser.parse("")
        assert result == {}
    
    def test_only_comments(self):
        parser = NoteDataFormat()
        result = parser.parse("# Just a comment")
        assert result == {}
    
    def test_quoted_strings(self):
        parser = NoteDataFormat()
        result = parser.parse('name: "John Doe"')
        assert result == {'name': 'John Doe'}
    
    def test_scientific_notation(self):
        parser = NoteDataFormat()
        result = parser.parse("value: 1.5e10")
        assert result == {'value': 1.5e10}
    
    def test_negative_numbers(self):
        parser = NoteDataFormat()
        result = parser.parse("temp: -5.5")
        assert result == {'temp': -5.5}


class TestTypedValues:
    """Test type hints"""
    
    def test_time_type(self):
        parser = NoteDataFormat()
        result = parser.parse("created: @time 2024-12-07T10:30:00")
        assert result == {'created': {'_type': 'timestamp', 'value': '2024-12-07T10:30:00'}}
    
    def test_float_array_type(self):
        parser = NoteDataFormat()
        result = parser.parse("vector: @f32[] 0.1, 0.2, 0.3")
        assert result == {'vector': [0.1, 0.2, 0.3]}
    
    def test_embedding_type(self):
        parser = NoteDataFormat()
        result = parser.parse("embedding: @embedding abc123")
        assert result == {'embedding': {'_type': 'embedding', 'data': 'abc123'}}


if __name__ == '__main__':
    # Run tests with pytest
    pytest.main([__file__, '-v'])