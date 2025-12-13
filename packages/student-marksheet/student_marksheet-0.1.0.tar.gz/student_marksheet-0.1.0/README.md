# student-marksheet

A simple Python library to generate student marksheets programmatically.

## Installation

pip install student-marksheet


## Usage

```python
from student_marksheet import Marksheet

m = Marksheet("Swami", 1)
m.add_mark("Math", 95)
m.add_mark("Science", 88)

print(m.export_text())
print(m.export_json())


