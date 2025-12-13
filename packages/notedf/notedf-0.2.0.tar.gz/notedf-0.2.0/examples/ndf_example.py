"""
NDF (Note Data Format) - Usage Examples
"""

from ndf import NoteDataFormat


def example_simple_values():
    """Example: Simple key-value pairs"""
    print("=" * 50)
    print("EXAMPLE 1: Simple Values")
    print("=" * 50)
    
    ndf_text = """
name: John Doe
age: 30
active: yes
score: 95.5
tags: python ai machine-learning
"""
    
    parser = NoteDataFormat()
    result = parser.parse(ndf_text)
    
    print("Input NDF:")
    print(ndf_text)
    print("\nParsed Result:")
    print(result)
    print()


def example_nested_objects():
    """Example: Nested objects with indentation"""
    print("=" * 50)
    print("EXAMPLE 2: Nested Objects")
    print("=" * 50)
    
    ndf_text = """
user:
  name: Alice
  email: alice@example.com
  settings:
    theme: dark
    notifications: yes
    privacy:
      profile: public
      messages: friends-only
"""
    
    parser = NoteDataFormat()
    result = parser.parse(ndf_text)
    
    print("Input NDF:")
    print(ndf_text)
    print("\nParsed Result:")
    print(result)
    print()


def example_inline_syntax():
    """Example: Inline objects and arrays"""
    print("=" * 50)
    print("EXAMPLE 3: Inline Objects & Arrays")
    print("=" * 50)
    
    ndf_text = """
point: {x: 10, y: 20, z: 30}
matrix: [[1,2,3],[4,5,6],[7,8,9]]
config: {timeout: 30, retry: 3, debug: yes}
"""
    
    parser = NoteDataFormat()
    result = parser.parse(ndf_text)
    
    print("Input NDF:")
    print(ndf_text)
    print("\nParsed Result:")
    print(result)
    print()


def example_multiline_text():
    """Example: Multi-line text with pipe operator"""
    print("=" * 50)
    print("EXAMPLE 4: Multi-line Text")
    print("=" * 50)
    
    ndf_text = """
prompt: |
  You are a helpful assistant.
  Answer questions clearly and concisely.
  Always be polite and professional.

description: |
  This is a multi-line description
  that preserves formatting and line breaks.
"""
    
    parser = NoteDataFormat()
    result = parser.parse(ndf_text)
    
    print("Input NDF:")
    print(ndf_text)
    print("\nParsed Result:")
    print(result)
    print()


def example_references():
    """Example: Template references for DRY data"""
    print("=" * 50)
    print("EXAMPLE 5: References & Templates")
    print("=" * 50)
    
    ndf_text = """
$user_template:
  role: member
  permissions: read
  active: yes

alice: $user_template {name: Alice, email: alice@example.com}
bob: $user_template {name: Bob, email: bob@example.com}
charlie: $user_template {name: Charlie, role: admin, permissions: write}
"""
    
    parser = NoteDataFormat()
    result = parser.parse(ndf_text)
    
    print("Input NDF:")
    print(ndf_text)
    print("\nParsed Result:")
    print(result)
    print()


def example_dumps():
    """Example: Converting Python dict to NDF"""
    print("=" * 50)
    print("EXAMPLE 6: Python to NDF (dumps)")
    print("=" * 50)
    
    data = {
        'server': {
            'host': 'localhost',
            'port': 8080,
            'ssl': True
        },
        'database': {
            'name': 'mydb',
            'user': 'admin',
            'timeout': 30
        },
        'features': ['auth', 'cache', 'logging']
    }
    
    parser = NoteDataFormat()
    ndf_output = parser.dumps(data)
    
    print("Python Dict:")
    print(data)
    print("\nConverted to NDF:")
    print(ndf_output)
    print()


def example_comments():
    """Example: Using comments"""
    print("=" * 50)
    print("EXAMPLE 7: Comments")
    print("=" * 50)
    
    ndf_text = """
# Server configuration
host: localhost  # local development
port: 8080

# Database settings
database:
  name: mydb
  # Connection pool size
  pool_size: 10
"""
    
    parser = NoteDataFormat()
    result = parser.parse(ndf_text)
    
    print("Input NDF:")
    print(ndf_text)
    print("\nParsed Result:")
    print(result)
    print()


def example_typed_values():
    """Example: Type hints for special values"""
    print("=" * 50)
    print("EXAMPLE 8: Typed Values")
    print("=" * 50)
    
    ndf_text = """
created: @time 2024-12-07T10:30:00
vector: @f32[] 0.1, 0.2, 0.3, 0.4, 0.5
embedding: @embedding dGVzdF9kYXRh
"""
    
    parser = NoteDataFormat()
    result = parser.parse(ndf_text)
    
    print("Input NDF:")
    print(ndf_text)
    print("\nParsed Result:")
    print(result)
    print()


def example_mixed_lists():
    """Example: Different list formats"""
    print("=" * 50)
    print("EXAMPLE 9: List Formats")
    print("=" * 50)
    
    ndf_text = """
# Space-separated
tags: python ai ml

# Comma-separated
colors: red, blue, green, yellow

# Inline array
coordinates: [10, 20, 30]

# Multi-dimensional
grid: [[1,2,3], [4,5,6], [7,8,9]]
"""
    
    parser = NoteDataFormat()
    result = parser.parse(ndf_text)
    
    print("Input NDF:")
    print(ndf_text)
    print("\nParsed Result:")
    print(result)
    print()


def example_practical_config():
    """Example: Real-world configuration file"""
    print("=" * 50)
    print("EXAMPLE 10: Practical Configuration")
    print("=" * 50)
    
    ndf_text = """
# Application Configuration
app:
  name: MyApp
  version: 1.2.3
  debug: yes

# Server settings
server:
  host: 0.0.0.0
  port: 8080
  workers: 4
  timeout: 30

# Database
database:
  engine: postgresql
  host: db.example.com
  port: 5432
  name: myapp_db
  pool:
    min: 5
    max: 20

# Cache
cache:
  type: redis
  host: cache.example.com
  ttl: 3600

# Feature flags
features:
  authentication: yes
  rate_limiting: yes
  analytics: no
  beta_features: no

# Logging
logging:
  level: info
  format: json
  outputs: console, file
"""
    
    parser = NoteDataFormat()
    result = parser.parse(ndf_text)
    
    print("Input NDF:")
    print(ndf_text)
    print("\nParsed Result:")
    print(result)
    print()


if __name__ == '__main__':
    # Run all examples
    example_simple_values()
    example_nested_objects()
    example_inline_syntax()
    example_multiline_text()
    example_references()
    example_dumps()
    example_comments()
    example_typed_values()
    example_mixed_lists()
    example_practical_config()