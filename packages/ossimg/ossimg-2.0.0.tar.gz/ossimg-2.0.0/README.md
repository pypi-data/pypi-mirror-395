IMAGE PREPROCESSING LIBRARY 

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

[Project Status : Still Under Development]

This Python library provides a simple, code-based interface for apply various image editing features and predefined templates to pictures.

## 📋 Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Contributing](#contributing)

## FEATURES
The library currently include four primary image editing features and three prepared editing templates for quick application. 

Editing Features (Manual Use)
- [Feature 1]: ***Change Brightness***
- [Feature 2]: ***Adjust Saturation***
- [Feature 3]: ***Adjust Sharpness***
- [Feature 4]: ***Adjust Shadow***

Predefined Templates (Quick Use)
- |Template A|: `Golden Hour`
- |Template B|: `Gritty Contrast`
- |Template C|: `Pastel Matte`


## Installations

### Option 1: From GitHub (Recommended)
```bash
pip install git+https://github.com/wamos0922/OSFPLibrary.git
```
### Option 2: From Source (For Development)
1. Open your Command Prompt (CMD) and navigate to your preferred working directory

2. Clone the OSFPLibrary repository:

    git clone https://github.com/wamos0922/OSFPLibrary.git

3. Navigate into the OSFPLibrary directory:

    cd OSFPLibrary

4. Install the package:

    pip install -e .

5. Back to working directory:

    cd ..

6. Clone the OSFPDemo repository:

    git clone https://github.com/wamos0922/OSFPDemo.git

7. Navigate into the OSFPDemo folder:

    cd OSFPDemo

8. Run the demo.py file:

    python demo.py


### Requirements

- Python 3.7 or higher
- Pillow (PIL) 9.0.0 or higher

## 🧪 Testing

Run tests with pytest:
```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run with coverage
pytest --cov=ossimg tests/
```


## Contributing

If you're interested in contributing to this project, please feel free to fork the repository and submit a pull request! See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for more detail.
