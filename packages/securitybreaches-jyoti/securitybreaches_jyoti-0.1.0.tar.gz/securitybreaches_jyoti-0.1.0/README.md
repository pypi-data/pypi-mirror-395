# Security Breaches Documentation

This package contains security breaches notes and documentation.

## Installation

```bash
pip install securitybreaches-jyoti
```

## Usage

After installation, you can access the documentation files:

```python
import securitybreaches_data
import os

# Get the package directory
package_dir = os.path.dirname(securitybreaches_data.__file__)

# List all files
print(os.listdir(package_dir))

# Access the Word document
doc_path = os.path.join(package_dir, 'securitybreachesnotes.docx')
print(f"Document location: {doc_path}")
```

## Contents

- Security breaches notes (Word document)
- Additional documentation and resources

## Author

Jyoti Rahate
