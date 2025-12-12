import re

# Read the test file
with open('tests/test_methods.py', 'r') as f:
    content = f.read()

# Fix the assertions
# Change: assert widget_instance.geojson_data == geojson
# To:     assert widget_instance.geojson_data == [geojson]
content = re.sub(
    r'assert widget_instance\.geojson_data == (sample_geojson|geojson|new_geojson)([^\[])',
    r'assert widget_instance.geojson_data == [\1]\2',
    content
)

# Fix: assert len(widget_instance.geojson_data["features"]) == 2
# To:   assert len(widget_instance.geojson_data[0]["features"]) == 2
content = re.sub(
    r'widget_instance\.geojson_data\["features"\]',
    r'widget_instance.geojson_data[0]["features"]',
    content
)

# Write back
with open('tests/test_methods.py', 'w') as f:
    f.write(content)

print("Fixed test_methods.py")

# Also fix test_widget.py
with open('tests/test_widget.py', 'r') as f:
    content = f.read()

# Change: assert widget_instance.geojson_data is None
# To:     assert widget_instance.geojson_data == []
content = re.sub(
    r'assert widget_instance\.geojson_data is None',
    r'assert widget_instance.geojson_data == []',
    content
)

with open('tests/test_widget.py', 'w') as f:
    f.write(content)

print("Fixed test_widget.py")

# Fix test_integration.py
with open('tests/test_integration.py', 'r') as f:
    content = f.read()

# Change: assert widget_instance.geojson_data == geojson
# To:     assert widget_instance.geojson_data == [geojson]
content = re.sub(
    r'assert widget_instance\.geojson_data == (empty_geojson|geojson)([^\[])',
    r'assert widget_instance.geojson_data == [\1]\2',
    content
)

with open('tests/test_integration.py', 'w') as f:
    f.write(content)

print("Fixed test_integration.py")
