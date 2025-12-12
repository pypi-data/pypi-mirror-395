# Serbian Python (Work in Progress)

A Python library providing Serbian language adaptations and utility functions for educational programming.

## Features

- **ispiši()** - Serbian adaptation of print()
- **input_tekst()** - Serbian adaptation of input() for text input
- **input_broj()** - Serbian adaptation for number input
- **unos_lista_sa_razmacima()** - Input list with space-separated values
- **unos_tuple_sa_razmacima()** - Input tuple with space-separated values
- **unos_set_sa_razmacima()** - Input set with space-separated values
- **unos_dict_sa_razmacima()** - Input dictionary with key:value pairs

## Installation

```bash
py -m pip install serbian-py
```

## Usage

```python
from serbian_py import ispiši, input_broj, input_tekst

# Print text in Serbian style
ispiši("Zdravo!")

# Get numeric input
broj = input_broj("Unesite broj: ")

# Get text input
tekst = input_tekst("Unesite tekst: ")
```

## License

MIT License - see LICENSE file for details
