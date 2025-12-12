# DragoHan's Grimoire 🔥

My personal AI automation library - built by an automation god, for automation gods.

## Installation
```bash
pip install git+https://github.com/farhanistopG1/my_grimoire.git --break-system-packages
```

## Libraries

### JSON Mage
Master any JSON structure without bullshit.
```python
from json_mage import modify

# Convert any JSON to powerful object
response = api.get_data()
data = modify(response)

# Use it
print(data.first)
print(data.last)
print(data.get('email'))
print(data.all('name'))
```

### Simple File
File handling made stupid simple.
```python
import simple_file

# Save anything
simple_file.save('config', {'key': 'value'})

# Load anything
config = simple_file.load('config')

# Delete, rewrite, append
simple_file.delete('old_file')
simple_file.rewrite('note', 'New content')
simple_file.add('log', 'Error message')

# Check, list, backup
simple_file.exists('config')
simple_file.list_files()
simple_file.backup('important.json')
```

## Author

DragoHan - AI Automation God
