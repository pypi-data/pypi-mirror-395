# commons
[![PyPI version](https://badge.fury.io/py/atlas-consortia-commons.svg)](https://badge.fury.io/py/atlas-consortia-commons)

This repository contains the code supporting several restful microservices used by the consortia.

### Getting Started

The Atlas Consortia Commons library is available through PyPi via the command:

```bash
pip install atlas-consortia-commons
```

The atlas-consortia-commons requirements can be found [here](requirements.txt)


### Contents

The code includes:
- [UBKG](atlas_consortia_commons/ubkg/README.md): For querying Unified Biomedical Knowledge Graph (UBKG) application interface
- [REST](atlas_consortia_commons/rest/README.md): For making standardised rest responses


### Coding Conventions
- Please use:
  - `snake_case` to name methods and variables. 
  - `PascalCase` for class names.
- Do follow any additional code formatting and styles as seen in the project


### Running Tests
- Install `pytest` using the command
```bash
pip install -r requirements.dev.txt
```
- Run the tests using the command
```bash
pytest
```