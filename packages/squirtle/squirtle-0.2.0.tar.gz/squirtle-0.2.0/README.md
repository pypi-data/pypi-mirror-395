# Squirtle

<div align="center">

**S**chema **Q**uery **U**tility **I**nterface **R**untime **T**ransformation **L**ibrary **E**ngine

[![PyPI version](https://badge.fury.io/py/squirtle.svg)](https://badge.fury.io/py/squirtle)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> Convert between Polars schemas and SQLAlchemy/SQLModel classes with ease.

[Features](#-features) • [Installation](#-installation) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

Squirtle provides simple, bidirectional conversion functions to transform schemas between Polars and SQLAlchemy, as well as SQLModel (optional dependency), supporting all common types. Perfect for data engineering workflows that need to bridge Polars' high-performance data processing with ORM capabilities.

## ✨ Features

- 🔄 **Bidirectional Conversion**: Convert schemas in both directions seamlessly
- 📊 **Comprehensive Type Support**: Supports all common primitive types with precision preservation
- 🔧 **SQLModel Support**: Optional SQLModel integration for modern Python type hints
- 🛡️ **Type Safety**: Clear error messages for unsupported types and invalid schemas
- 🎯 **Simple API**: Functional, stateless functions with minimal dependencies
- ✅ **Schema Validation**: Automatic validation of schemas before conversion
- 🔑 **Explicit Primary Keys**: Specify primary key fields explicitly for clarity and control
- ⚡ **Zero Runtime Overhead**: Lightweight with no performance impact

## 📦 Installation

### Basic Installation

```bash
pip install squirtle
```

### With SQLModel Support

For SQLModel integration (optional):

```bash
pip install squirtle[sqlmodel]
```

### Development Installation

```bash
git clone https://github.com/eddiethedean/squirtle.git
cd squirtle
pip install -e ".[dev]"
```

## 📋 Requirements

- **Python** >= 3.8
- **polars** >= 0.19.0
- **sqlalchemy** >= 1.4.0
- **sqlmodel** >= 0.0.8 (optional, for SQLModel support)

## 🚀 Quick Start

Get started with Squirtle in just a few lines of code. Here are the most common conversion patterns:

### Converting Polars Schema to SQLAlchemy Model

```python
import polars as pl
from squirtle import to_sqlalchemy_model
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# Define a Polars schema
polars_schema = pl.Schema({
    "name": pl.String,
    "age": pl.Int32,
    "score": pl.Float64,
})

# Convert to SQLAlchemy model
Person = to_sqlalchemy_model(polars_schema, primary_key="name", class_name="Person", base=Base)
print(Person.__tablename__)  # Output: 'person'
print(Person.name)  # Output: Person.name
```

### Converting SQLAlchemy Model to Polars Schema

```python
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import DeclarativeBase
from squirtle import to_polars_schema
import polars as pl

class Base(DeclarativeBase):
    pass

class Person(Base):
    __tablename__ = "person"
    
    name = Column(String, primary_key=True)
    age = Column(Integer)
    score = Column(Float)

# Convert to Polars schema
polars_schema = to_polars_schema(Person)
print(polars_schema)
# Output: Schema([('name', String), ('age', Int32), ('score', Float64)])
```

### Converting Polars Schema to SQLModel Class

```python
import polars as pl
from squirtle import to_sqlmodel_class

# Define a Polars schema
polars_schema = pl.Schema({
    "id": pl.Int64,
    "name": pl.String,
    "age": pl.Int32,
})

# Convert to SQLModel class
Person = to_sqlmodel_class(polars_schema, primary_key="id", class_name="Person")
print(Person.__tablename__)  # Output: 'person'

# Use the class
person = Person(id=1, name="Alice", age=30)
print(person)  # Output: id=1 name='Alice' age=30
```

## 📚 Supported Types

Squirtle supports bidirectional conversion between the following types:

| Polars Type | SQLAlchemy Type | SQLModel Type | Notes |
|------------|----------------|---------------|-------|
| `Int8`, `Int16` | `SmallInteger` | `int` | 8-bit and 16-bit integers |
| `Int32` | `Integer` | `int` | 32-bit integer |
| `Int64` | `BigInteger` | `int` | 64-bit integer |
| `UInt8`, `UInt16` | `SmallInteger` | `int` | Unsigned integers |
| `UInt32` | `Integer` | `int` | Unsigned 32-bit integer |
| `UInt64` | `BigInteger` | `int` | Unsigned 64-bit integer |
| `Float32`, `Float64` | `Float` | `float` | Floating point numbers |
| `String`, `Utf8` | `String` | `str` | Text strings |
| `Boolean` | `Boolean` | `bool` | Boolean values |
| `Date` | `Date` | `date` | Date values |
| `Datetime` | `DateTime` | `datetime` | Datetime values |
| `Time` | `Time` | `time` | Time values |
| `Decimal` | `Numeric` | `Decimal` | Decimal numbers |

### Nullable Fields

Both Polars and SQLAlchemy support nullable fields:

- **Polars**: Polars types in schemas are typically non-nullable by default. Nullable types can be detected by checking for `Null` wrappers or inner attributes.
- **SQLAlchemy**: Use `nullable=True` in Column definition
- **SQLModel**: Use `Optional[Type]` or `Type | None` type hints

Squirtle automatically detects and handles nullability when converting from Polars to SQLAlchemy/SQLModel. When converting from SQLAlchemy to Polars, nullability information is preserved in the SQLAlchemy model but Polars schemas don't explicitly track nullability (all Polars DataFrame columns can contain nulls).

### Unsupported Types

The following types are currently not supported and will raise `UnsupportedTypeError`:

- `List` / `Array` types
- `Struct` types (nested structures)
- `Map` types

## 💡 Use Cases

### Data Pipeline Integration

Convert Polars schemas to SQLAlchemy models for database operations:

```python
import polars as pl
from squirtle import to_sqlalchemy_model
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# Define schema from your data processing pipeline
df = pl.DataFrame({
    "user_id": [1, 2, 3],
    "name": ["Alice", "Bob", "Charlie"],
    "score": [95.5, 87.0, 92.3],
})

# Get schema from DataFrame
schema = df.schema

# Convert to SQLAlchemy model for database operations
User = to_sqlalchemy_model(schema, primary_key="user_id", class_name="User", base=Base)
print(User.__tablename__)  # Output: 'user'
print(list(User.__table__.columns.keys()))  # Output: ['user_id', 'name', 'score']

# Now you can use User model with SQLAlchemy
```

### API Development

Convert existing SQLAlchemy models to Polars schemas for data validation:

```python
from squirtle import to_polars_schema
import polars as pl
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# Your existing SQLAlchemy model
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)

# Convert to Polars schema for validation
schema = to_polars_schema(Product)
print(schema)  # Output: Schema([('id', Int32), ('name', String), ('price', Float64)])

# Use with Polars for data processing
# df = pl.DataFrame(your_data, schema=schema)
```

### Schema Migration

Use Squirtle to migrate schemas between systems:

```python
import polars as pl
from squirtle import to_polars_schema, to_sqlalchemy_model
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# Example: Convert from SQLAlchemy to Polars for analysis
class MyModel(Base):
    __tablename__ = "mymodel"
    id = Column(Integer, primary_key=True)
    name = Column(String)

polars_schema = to_polars_schema(MyModel)

# Process data with Polars (example data)
df = pl.DataFrame({"id": [1, 2], "name": ["Alice", "Bob"]}, schema=polars_schema)

# Convert back to SQLAlchemy for database storage
NewModel = to_sqlalchemy_model(df.schema, primary_key="id", class_name="NewModel", base=Base)
print(NewModel.__tablename__)  # Output: 'new_model'
```

## 🎓 Advanced Examples

### Custom Base Class

```python
from sqlalchemy.orm import DeclarativeBase
from squirtle import to_sqlalchemy_model
import polars as pl

class CustomBase(DeclarativeBase):
    pass

schema = pl.Schema({
    "id": pl.Int64,
    "name": pl.String,
})

Model = to_sqlalchemy_model(schema, primary_key="id", class_name="MyModel", base=CustomBase)
```

### Round-Trip Conversion

```python
import polars as pl
from squirtle import to_polars_schema, to_sqlalchemy_model
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# Start with Polars schema
original = pl.Schema({
    "name": pl.String,
    "age": pl.Int32,
})

# Convert to SQLAlchemy and back
model = to_sqlalchemy_model(original, primary_key="name", base=Base)
converted_back = to_polars_schema(model)

# Verify types match
print(f"Original: {original}")
# Output: Original: Schema([('name', String), ('age', Int32)])
print(f"Converted back: {converted_back}")
# Output: Converted back: Schema([('name', String), ('age', Int32)])
assert len(converted_back) == len(original)  # True
assert "name" in converted_back  # True
assert "age" in converted_back  # True
```

### Working with Nullable Fields

```python
import polars as pl
from squirtle import to_sqlalchemy_model
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# Schema with fields
# Note: Polars schemas don't explicitly track nullability in the DataType itself
# Squirtle detects nullable types by checking for Null wrappers or inner attributes
schema = pl.Schema({
    "id": pl.Int64,  # Will be used as primary key (must be specified explicitly)
    "name": pl.String,  # Type nullability is detected automatically
    "email": pl.String,
})

Model = to_sqlalchemy_model(schema, primary_key="id", class_name="User", base=Base)

# id is primary key
print(Model.id.primary_key)  # Output: True
print(Model.id.nullable)     # Output: True
print(Model.name.nullable)   # Output: True
print(Model.email.nullable)  # Output: True
```

### Dictionary Schema Format

You can also use dictionary format instead of `pl.Schema`:

```python
from squirtle import to_sqlalchemy_model
import polars as pl

# Dictionary format works too
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

schema_dict = {
    "id": pl.Int64,
    "name": pl.String,
    "created_at": pl.Datetime,
}

Model = to_sqlalchemy_model(schema_dict, primary_key="id", class_name="User", base=Base)
print(Model.__tablename__)  # Output: 'user'
print(list(Model.__table__.columns.keys()))  # Output: ['id', 'name', 'created_at']
```

### Composite Primary Keys

SQLAlchemy supports composite primary keys (multiple fields). You can specify multiple fields as a list:

```python
from squirtle import to_sqlalchemy_model
import polars as pl
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

schema = pl.Schema({
    "user_id": pl.Int64,
    "session_id": pl.Int64,
    "data": pl.String,
})

# Use a list for composite primary key
Session = to_sqlalchemy_model(
    schema, 
    primary_key=["user_id", "session_id"], 
    class_name="UserSession", 
    base=Base
)

# Both fields are primary keys
print(Session.user_id.primary_key)    # Output: True
print(Session.session_id.primary_key)  # Output: True
```

**Note**: SQLModel only supports single primary keys, so `to_sqlmodel_class()` requires a string, not a list.

## ⚠️ Limitations

1. **Complex Types**: List, Struct, and Map types are not supported
2. **Nested Structures**: Only flat schemas are supported
3. **Custom Types**: Custom SQLAlchemy types may not convert correctly
4. **Type Precision**: Some precision information may be lost in conversion:
   - **Datetime**: When converting SQLAlchemy DateTime to Polars, time unit defaults to microseconds ("us")
   - **Decimal**: Precision and scale information from SQLAlchemy Numeric/Decimal types is not preserved when converting to Polars Decimal

## 🛡️ Error Handling

Squirtle provides clear error messages through custom exceptions:

```python
from squirtle import ConversionError, UnsupportedTypeError, SchemaError

try:
    schema = to_sqlalchemy_model(invalid_schema, primary_key="id")
except SchemaError as e:
    print(f"Invalid schema: {e}")
except UnsupportedTypeError as e:
    print(f"Unsupported type: {e}")
except ConversionError as e:
    print(f"Conversion error: {e}")
```

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `SchemaError` | Empty schema, duplicate fields, invalid field names | Ensure schema has at least one field, no duplicates, valid names |
| `UnsupportedTypeError` | Unsupported Polars type (List, Struct, Map) | Use supported primitive types only |
| `ImportError` | Missing dependencies | Install required packages: `pip install polars sqlalchemy` |

## 📖 API Reference

### `to_sqlalchemy_model(polars_schema, primary_key, class_name="GeneratedModel", base=None)`

Convert a Polars schema to a SQLAlchemy model class.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `polars_schema` | `dict[str, DataType]` or `pl.Schema` | _required_ | Polars schema to convert |
| `primary_key` | `str` or `list[str]` | _required_ | Field name(s) to use as primary key. Can be a single string or list for composite keys. |
| `class_name` | `str` | `"GeneratedModel"` | Name for the generated model class |
| `base` | `Type[DeclarativeBase]` | `DeclarativeBase` | Base class for the model (optional) |

**Returns:**

- `Type[DeclarativeBase]`: SQLAlchemy model class with `__tablename__` attribute

**Raises:**

- `SchemaError`: If the schema structure is invalid (duplicate fields, empty names, etc.)
- `UnsupportedTypeError`: If a type cannot be converted (List, Struct, Map types)
- `ImportError`: If required dependencies are not installed

**Example:**

```python
import polars as pl
from squirtle import to_sqlalchemy_model
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

schema = pl.Schema({
    "name": pl.String,
    "age": pl.Int32,
})

Person = to_sqlalchemy_model(schema, primary_key="name", class_name="Person", base=Base)
# Person is now a SQLAlchemy model class
```

---

### `to_polars_schema(model)`

Convert a SQLAlchemy model class, instance, or SQLModel class to a Polars schema.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `model` | `Type` or instance | SQLAlchemy model class/instance or SQLModel class |

**Returns:**

- `pl.Schema`: Polars schema with all fields converted

**Raises:**

- `SchemaError`: If the model structure is invalid (no `__table__` attribute, etc.)
- `UnsupportedTypeError`: If a type cannot be converted
- `ImportError`: If required dependencies are not installed

**Example:**

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase
from squirtle import to_polars_schema

class Base(DeclarativeBase):
    pass

class Person(Base):
    __tablename__ = "person"
    name = Column(String, primary_key=True)
    age = Column(Integer)

schema = to_polars_schema(Person)
# Returns pl.Schema with name and age fields
```

---

### `to_sqlmodel_class(polars_schema, primary_key, class_name="GeneratedModel")`

Convert a Polars schema to a SQLModel class with type annotations.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `polars_schema` | `dict[str, DataType]` or `pl.Schema` | _required_ | Polars schema to convert |
| `primary_key` | `str` | _required_ | Field name to use as primary key (must be a single string) |
| `class_name` | `str` | `"GeneratedModel"` | Name for the generated model class |

**Returns:**

- `Type[SQLModel]`: SQLModel class with type annotations and default values

**Raises:**

- `SchemaError`: If the schema structure is invalid
- `UnsupportedTypeError`: If a type cannot be converted
- `ImportError`: If SQLModel is not installed

**Example:**

```python
import polars as pl
from squirtle import to_sqlmodel_class

schema = pl.Schema({
    "id": pl.Int64,
    "name": pl.String,
    "age": pl.Int32,
})

Person = to_sqlmodel_class(schema, primary_key="id", class_name="Person")
# Person is now a SQLModel class with type annotations
person = Person(id=1, name="Alice", age=30)
```

## 🛠️ Development

### Setup

Clone the repository and install in development mode:

```bash
git clone https://github.com/eddiethedean/squirtle.git
cd squirtle
pip install -e ".[dev]"
```

### Running Tests

Run the full test suite:

```bash
pytest
```

Run tests in parallel for faster execution:

```bash
pytest -n 10
```

Run tests with coverage:

```bash
pytest --cov=squirtle --cov-report=html
```

### Code Quality

Format code with Ruff:

```bash
ruff format .
```

Lint code with Ruff:

```bash
ruff check .
```

Type check with mypy:

```bash
mypy .
```

### Project Structure

```
squirtle/
├── squirtle/                # Main package
│   ├── __init__.py          # Public API exports
│   ├── converters.py        # Core conversion functions
│   ├── type_mappings.py     # Type mapping dictionaries
│   └── errors.py            # Custom exceptions
├── tests/                   # Test suite
│   ├── test_converters.py   # Conversion function tests
│   ├── test_type_mappings.py # Type mapping tests
│   ├── test_errors.py       # Error handling tests
│   └── test_comprehensive.py # Comprehensive integration tests
├── pyproject.toml           # Package configuration
├── README.md                # This file
└── LICENSE                  # MIT License
```

## 🤝 Contributing

Contributions are welcome! We appreciate your help in making Squirtle better.

### How to Contribute

1. **Fork the repository** and create a new branch for your feature or bugfix
2. **Make your changes** following the existing code style
3. **Add tests** for new functionality or bug fixes
4. **Run the test suite** to ensure everything passes:
   ```bash
   ruff format .
   ruff check .
   mypy .
   pytest
   ```
5. **Submit a Pull Request** with a clear description of your changes

### Development Guidelines

- Follow the existing code style (Ruff formatting, 100 character line length)
- Write tests for all new features and bug fixes
- Update documentation as needed
- Ensure all tests pass before submitting
- Use type hints where appropriate

### Reporting Issues

If you find a bug or have a feature request, please open an issue on GitHub with:

- A clear description of the problem or feature
- Steps to reproduce (for bugs)
- Expected vs actual behavior
- Python version and dependency versions

## 🎨 Inspiration

This project is part of a family of schema conversion libraries:

- 🦎 **charmander** - Convert between Polars and PySpark schemas
- 🐢 **poldantic** - Convert between Pydantic models and Polars schemas
- 🌱 **bulbasaur** - Convert between PySpark and SQLAlchemy/SQLModel schemas
- 🐢 **squirtle** - Convert between Polars and SQLAlchemy/SQLModel schemas

## 📝 About

Squirtle provides a bridge between Polars' high-performance data processing and SQLAlchemy's ORM capabilities, enabling seamless schema conversion for data engineering workflows. Whether you're building data pipelines, APIs, or migration tools, Squirtle makes it easy to work with schemas across different ecosystems.

---

<div align="center">

**Made with ❤️ by [Odos Matthews](https://github.com/eddiethedean)**

[Repository](https://github.com/eddiethedean/squirtle) • [Issues](https://github.com/eddiethedean/squirtle/issues) • [License](LICENSE)

</div>
