"""Tests for builtin plugins."""

import pytest
from apilinker.plugins.builtin import (
    ArrayOperationsTransformer,
    JsonPathTransformer,
    TemplateTransformer,
)


class TestJsonPathTransformer:
    """Tests for JsonPathTransformer plugin."""

    def test_plugin_metadata(self):
        """Test plugin name and type."""
        transformer = JsonPathTransformer()
        assert transformer.plugin_name == "jsonpath"
        assert transformer.plugin_type == "transformer"

    def test_simple_path(self):
        """Test simple JSONPath extraction."""
        transformer = JsonPathTransformer()
        data = {"user": {"name": "John", "age": 30}}
        result = transformer.transform(data, path="user.name")
        assert result == "John"

    def test_nested_path(self):
        """Test nested JSONPath extraction."""
        transformer = JsonPathTransformer()
        data = {"user": {"profile": {"email": "john@example.com"}}}
        result = transformer.transform(data, path="user.profile.email")
        assert result == "john@example.com"

    def test_array_indexing(self):
        """Test array indexing in JSONPath."""
        transformer = JsonPathTransformer()
        data = {"items": [{"id": 1}, {"id": 2}, {"id": 3}]}
        result = transformer.transform(data, path="items[1].id")
        assert result == 2

    def test_array_indexing_simple(self):
        """Test simple array indexing."""
        transformer = JsonPathTransformer()
        data = ["a", "b", "c"]
        result = transformer.transform(data, path="[1]")
        assert result == "b"

    def test_array_out_of_bounds(self):
        """Test array indexing out of bounds."""
        transformer = JsonPathTransformer()
        data = {"items": [1, 2, 3]}
        result = transformer.transform(data, path="items[10]", default="not_found")
        assert result == "not_found"

    def test_missing_key(self):
        """Test missing key returns default."""
        transformer = JsonPathTransformer()
        data = {"user": {"name": "John"}}
        result = transformer.transform(data, path="user.email", default="no-email")
        assert result == "no-email"

    def test_empty_value(self):
        """Test empty value returns default."""
        transformer = JsonPathTransformer()
        result = transformer.transform(None, path="user.name", default="default")
        assert result == "default"

    def test_empty_path(self):
        """Test empty path returns default."""
        transformer = JsonPathTransformer()
        data = {"user": {"name": "John"}}
        result = transformer.transform(data, path="", default="default")
        assert result == "default"

    def test_invalid_path_structure(self):
        """Test invalid path structure returns default."""
        transformer = JsonPathTransformer()
        data = {"user": "string_not_dict"}
        result = transformer.transform(data, path="user.name", default="default")
        assert result == "default"

    def test_exception_handling(self):
        """Test exception handling returns default."""
        transformer = JsonPathTransformer()
        data = {"items": [1, 2, 3]}
        # Invalid index format should trigger exception handling
        result = transformer.transform(data, path="items[invalid]", default="error")
        assert result == "error"

    def test_array_with_name_and_index(self):
        """Test array access with both name and index."""
        transformer = JsonPathTransformer()
        data = {"users": [{"name": "Alice"}, {"name": "Bob"}]}
        result = transformer.transform(data, path="users[0].name")
        assert result == "Alice"

    def test_missing_array_field(self):
        """Test missing field before array index."""
        transformer = JsonPathTransformer()
        data = {"items": [1, 2, 3]}
        result = transformer.transform(data, path="missing[0]", default="not_found")
        assert result == "not_found"


class TestTemplateTransformer:
    """Tests for TemplateTransformer plugin."""

    def test_plugin_metadata(self):
        """Test plugin name and type."""
        transformer = TemplateTransformer()
        assert transformer.plugin_name == "template"
        assert transformer.plugin_type == "transformer"

    def test_simple_template(self):
        """Test simple template formatting."""
        transformer = TemplateTransformer()
        result = transformer.transform("John", template="Hello, {value}!")
        assert result == "Hello, John!"

    def test_template_with_kwargs(self):
        """Test template with additional kwargs."""
        transformer = TemplateTransformer()
        result = transformer.transform(
            "John", template="Hello, {value}! You are {age} years old.", age=30
        )
        assert result == "Hello, John! You are 30 years old."

    def test_empty_template(self):
        """Test empty template returns string value."""
        transformer = TemplateTransformer()
        result = transformer.transform("John", template="")
        assert result == "John"

    def test_none_value_empty_template(self):
        """Test None value with empty template."""
        transformer = TemplateTransformer()
        result = transformer.transform(None, template="")
        assert result == ""

    def test_none_value_with_template(self):
        """Test None value with template."""
        transformer = TemplateTransformer()
        result = transformer.transform(None, template="Value is {value}")
        assert result == "Value is None"

    def test_template_error_handling(self):
        """Test template error handling for missing keys."""
        transformer = TemplateTransformer()
        result = transformer.transform("John", template="Hello, {missing_key}!")
        assert "Template Error" in result

    def test_template_with_multiple_placeholders(self):
        """Test template with multiple placeholders."""
        transformer = TemplateTransformer()
        result = transformer.transform(
            "John",
            template="{greeting}, {value}! Welcome to {place}.",
            greeting="Hi",
            place="NYC",
        )
        assert result == "Hi, John! Welcome to NYC."

    def test_no_template_parameter(self):
        """Test when no template parameter is provided."""
        transformer = TemplateTransformer()
        result = transformer.transform(123)
        assert result == "123"


class TestArrayOperationsTransformer:
    """Tests for ArrayOperationsTransformer plugin."""

    def test_plugin_metadata(self):
        """Test plugin name and type."""
        transformer = ArrayOperationsTransformer()
        assert transformer.plugin_name == "array_ops"
        assert transformer.plugin_type == "transformer"

    def test_count_operation(self):
        """Test count operation."""
        transformer = ArrayOperationsTransformer()
        result = transformer.transform([1, 2, 3, 4, 5], operation="count")
        assert result == 5

    def test_count_empty_array(self):
        """Test count on empty array."""
        transformer = ArrayOperationsTransformer()
        result = transformer.transform([], operation="count")
        assert result == 0

    def test_sum_operation(self):
        """Test sum operation."""
        transformer = ArrayOperationsTransformer()
        result = transformer.transform([1, 2, 3, 4, 5], operation="sum")
        assert result == 15

    def test_sum_with_floats(self):
        """Test sum with float values."""
        transformer = ArrayOperationsTransformer()
        result = transformer.transform([1.5, 2.5, 3.0], operation="sum")
        assert result == 7.0

    def test_sum_with_strings(self):
        """Test sum with string numbers."""
        transformer = ArrayOperationsTransformer()
        result = transformer.transform(["1", "2", "3"], operation="sum")
        assert result == 6.0

    def test_avg_operation(self):
        """Test average operation."""
        transformer = ArrayOperationsTransformer()
        result = transformer.transform([1, 2, 3, 4, 5], operation="avg")
        assert result == 3.0

    def test_avg_empty_array(self):
        """Test average on empty array."""
        transformer = ArrayOperationsTransformer()
        result = transformer.transform([], operation="avg")
        assert result == 0

    def test_min_operation(self):
        """Test min operation."""
        transformer = ArrayOperationsTransformer()
        result = transformer.transform([5, 2, 8, 1, 9], operation="min")
        assert result == 1

    def test_min_empty_array(self):
        """Test min on empty array."""
        transformer = ArrayOperationsTransformer()
        result = transformer.transform([], operation="min")
        assert result is None

    def test_max_operation(self):
        """Test max operation."""
        transformer = ArrayOperationsTransformer()
        result = transformer.transform([5, 2, 8, 1, 9], operation="max")
        assert result == 9

    def test_max_empty_array(self):
        """Test max on empty array."""
        transformer = ArrayOperationsTransformer()
        result = transformer.transform([], operation="max")
        assert result is None

    def test_join_operation(self):
        """Test join operation."""
        transformer = ArrayOperationsTransformer()
        result = transformer.transform(["a", "b", "c"], operation="join")
        assert result == "a,b,c"

    def test_join_with_custom_separator(self):
        """Test join with custom separator."""
        transformer = ArrayOperationsTransformer()
        result = transformer.transform(
            ["a", "b", "c"], operation="join", separator=" - "
        )
        assert result == "a - b - c"

    def test_join_with_none_values(self):
        """Test join filtering out None values."""
        transformer = ArrayOperationsTransformer()
        result = transformer.transform(["a", None, "b", None, "c"], operation="join")
        assert result == "a,b,c"

    def test_non_array_value(self):
        """Test non-array value is converted to array."""
        transformer = ArrayOperationsTransformer()
        result = transformer.transform(5, operation="count")
        assert result == 1

    def test_none_value_becomes_empty_array(self):
        """Test None value is treated as empty array."""
        transformer = ArrayOperationsTransformer()
        result = transformer.transform(None, operation="count")
        assert result == 0

    def test_unknown_operation(self):
        """Test unknown operation returns original value."""
        transformer = ArrayOperationsTransformer()
        result = transformer.transform([1, 2, 3], operation="unknown")
        assert result == [1, 2, 3]

    def test_default_operation(self):
        """Test default operation is count."""
        transformer = ArrayOperationsTransformer()
        result = transformer.transform([1, 2, 3])
        assert result == 3

    def test_join_with_numbers(self):
        """Test join with numeric values."""
        transformer = ArrayOperationsTransformer()
        result = transformer.transform([1, 2, 3], operation="join")
        assert result == "1,2,3"

    def test_sum_with_whitespace_strings(self):
        """Test sum filters out empty/whitespace strings."""
        transformer = ArrayOperationsTransformer()
        result = transformer.transform(["1", "  ", "2", "", "3"], operation="sum")
        assert result == 6.0

    def test_avg_with_string_numbers(self):
        """Test average with string numbers."""
        transformer = ArrayOperationsTransformer()
        result = transformer.transform(["2", "4", "6"], operation="avg")
        assert result == 4.0

    def test_min_with_string_numbers(self):
        """Test min with string numbers."""
        transformer = ArrayOperationsTransformer()
        result = transformer.transform(["5", "2", "8"], operation="min")
        assert result == 2.0

    def test_max_with_string_numbers(self):
        """Test max with string numbers."""
        transformer = ArrayOperationsTransformer()
        result = transformer.transform(["5", "2", "8"], operation="max")
        assert result == 8.0

