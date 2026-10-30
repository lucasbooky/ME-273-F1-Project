# Python Cheat Sheet (for someone who knows MATLAB and C++)

Examples use things from this project. Columns: Python | MATLAB | C++.

## 1. Big differences to remember

- **Indentation is the syntax.** No `end` (MATLAB) and no `{ }` (C++). A block is the indented lines under a line ending in `:`.
- **Indexing starts at 0** (like C++, unlike MATLAB). `x[0]` is the first item, `x[-1]` is the last.
- **Slices exclude the end.** `x[0:3]` gives items 0, 1, 2 (3 items). MATLAB's `x(1:3)` includes 3.
- **No type declarations.** `a = 5` is fine (C++ would need `int a = 5;`). No semicolons needed.
- **Nothing prints unless you ask.** MATLAB prints when you leave off `;`. Python needs `print(x)`. In a notebook, only the last line of a cell is shown automatically.
- **Case matters, and `True`/`False`/`None` are capitalized.**
- **Comments** start with `#` (MATLAB uses `%`, C++ uses `//`).

## 2. Variables and basic types

| Python | MATLAB | C++ |
|---|---|---|
| `x = 5` (int) | `x = 5` (double) | `int x = 5;` |
| `x = 5.0` (float) | `x = 5.0` | `double x = 5.0;` |
| `s = "hello"` (str) | `s = "hello"` | `std::string s` |
| `ok = True` (bool) | `ok = true` | `bool ok = true;` |
| `f"lap {n}"` (f-string) | `sprintf("lap %d", n)` | `std::format` / `printf` |

Operators: `+ - * /` as usual. `**` is power (MATLAB `^`). `//` is integer division. `%` is remainder. `and`, `or`, `not` for logic on single values.

## 3. Collections

| Python | What it is | Closest equivalent |
|---|---|---|
| `[4, 1, 81]` list | ordered, any types, can grow | `std::vector`, MATLAB cell array |
| `(12, 4)` tuple | ordered, cannot be changed | `std::pair` / `std::tuple` |
| `{"a": 1, "b": 2}` dict | name -> value lookup | MATLAB struct, `std::map` |
| `np.array([1, 2, 3])` | numeric array for math | MATLAB matrix |

Common list/dict actions:

```python
nums = [4, 1, 81]
nums.append(63)         # add to the end (push_back)
len(nums)               # length (numel / size())
nums[0]                 # first item
nums[-1]                # last item
nums[:2]                # first two items

d = {}                  # empty dict
d[4] = "Norris"         # store
d[4]                    # look up
4 in d                  # is the key there? True/False
```

## 4. Control flow

```python
if x > 5:                       # MATLAB: if x > 5 ... end
    print("big")
elif x == 5:                    # elseif
    print("five")
else:
    print("small")

for n in numbers:               # goes through the values themselves
    print(n)

for i in range(5):              # i = 0,1,2,3,4   (MATLAB: for i = 0:4)
    print(i)

for i, n in enumerate(numbers): # index AND value together
    print(i, n)

while x > 0:
    x = x - 1

break                           # leave the loop
continue                        # skip to the next pass
```

- `range(5)` stops BEFORE 5. `range(1, 6)` gives 1 to 5.
- `==` equal, `!=` not equal (MATLAB `~=`).

## 5. Functions

```python
def lap_gap(a, b, scale=1.0):       # scale has a default value
    """Return the difference of a and b, times scale."""
    return (a - b) * scale

lap_gap(10, 4)                      # positional
lap_gap(10, 4, scale=2.0)           # named argument (MATLAB: 'scale', 2.0)
```

- Return several values: `return a, b` then `x, y = f()`.
- `**params` in a function definition collects named arguments into a dict.
- Functions need to be defined before they are called (run the definition cell first).

## 6. Importing (MATLAB toolboxes / C++ `#include`)

```python
import numpy as np                 # whole library, nickname np -> np.array(...)
import pandas as pd
import matplotlib.pyplot as plt
from f1.fetch import get_cached    # just one function from our own file
```

- **The dot means "look inside."** `np.mean(x)` = function `mean` inside numpy. `x.mean()` = method of the array `x`. (Like `obj.method()` in C++.)
- Our own file `f1/fetch.py` is imported as `f1.fetch` (folder, then file, no `.py`). A folder needs an `__init__.py` file to import from.

## 7. NumPy (arrays and matrix math)

| Python (`np` = numpy) | MATLAB |
|---|---|
| `a = np.array([1, 2, 3])` | `a = [1 2 3]` |
| `A = np.array([[1, 2], [3, 4]])` | `A = [1 2; 3 4]` |
| `np.zeros((3, 3))`, `np.ones(5)` | `zeros(3,3)`, `ones(1,5)` |
| `np.arange(0, 10, 2)` (0,2,4,6,8) | `0:2:8` |
| `np.linspace(0, 1, 5)` | `linspace(0,1,5)` |
| `A.shape` | `size(A)` |
| `A[0, 1]` (row 0, col 1) | `A(1, 2)` |
| `A[:, 0]` (whole first column) | `A(:, 1)` |
| `A[1, :]` (whole second row) | `A(2, :)` |
| `A[A > 5]` (logical indexing) | `A(A > 5)` |
| `A + B`, `A * B` (**elementwise**) | `A + B`, `A .* B` |
| `A @ B` (**matrix multiply**) | `A * B` |
| `A.T` | `A'` |
| `np.linalg.inv(A)` | `inv(A)` |
| `np.linalg.solve(A, b)` | `A \ b` |
| `a.mean()`, `a.max()`, `a.std()`, `a.sum()` | `mean(a)`, `max(a)`, `std(a)`, `sum(a)` |
| `np.sqrt(a)`, `np.sin(a)`, `np.abs(a)` | `sqrt(a)`, `sin(a)`, `abs(a)` |

Big trap: in NumPy `*` is elementwise (MATLAB's `.*`), and `@` is the matrix product (MATLAB's `*`).
Another trap: `b = a` does not copy an array. Use `b = a.copy()`.

## 8. Pandas (tables, like MATLAB `table`)

A **DataFrame** is a table with named columns.

```python
df["speed"]                       # one column (a Series)
df["speed"].to_numpy()            # that column as a NumPy array
df[["speed", "rpm"]]              # several columns (note double brackets)
df.shape, len(df), df.columns     # size, row count, column names
df.head()                         # first 5 rows
df.iloc[0]                        # first row by position
df["speed"].iloc[-1]              # last value of a column
df[df["speed"] > 300]             # rows where the condition is True
df[(df["a"] > 1) & (df["b"] < 5)] # combine with & and |, each in parentheses
df["new"] = df["speed"] * 0.62    # make a new column
df.to_csv("file.csv", index=False)
pd.read_csv("file.csv")
```

Dates: `pd.to_datetime(col, format="ISO8601")`. A length of time: `pd.Timedelta(seconds=90)`.

## 9. Matplotlib (plotting)

```python
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 4))       # new figure, width x height in inches
plt.plot(x, y, label="Norris")    # line plot (MATLAB: plot)
plt.scatter(x, y)                 # scatter
plt.bar(names, values)            # bar chart
plt.xlabel("Time"); plt.ylabel("Speed (km/h)"); plt.title("...")
plt.legend()
plt.grid(True)
plt.show()                        # draw it (MATLAB draws automatically)
```

Several plots in one figure (MATLAB `subplot`):

```python
fig, axes = plt.subplots(2, 1, figsize=(12, 6))
axes[0].plot(x, speed)            # on axes the calls are .plot, .set_xlabel, .set_title
axes[1].plot(x, throttle)
```

## 10. Classes (like C++ classes, simpler)

```python
class Driver:
    def __init__(self, number, name):     # constructor
        self.number = number              # self = this
        self.name = name

    def describe(self):                   # method
        return f"{self.name} (#{self.number})"

d = Driver(4, "Norris")
d.describe()
```

## 11. Errors you will see, and what they mean

| Error | Usual cause |
|---|---|
| `NameError: name 'x' is not defined` | A cell above was not run, or a typo, or a missing import |
| `ModuleNotFoundError` | Wrong kernel (use the `.venv` one) or the library is not installed |
| `KeyError: 'speed'` | That column or dict key does not exist (check `df.columns`) |
| `IndexError: index out of range` | Index past the end of the list or array |
| `IndentationError` | Inconsistent indentation inside a block |
| `ValueError` | Right type, bad value (like the date format one) |
| `TypeError` | Wrong kind of input to a function |

Read the **last line** of an error first. It says what went wrong. The lines above show where.

## 12. Notebook tips

- **Shift+Enter** runs a cell. Cells share variables, so run them top to bottom.
- Only the last expression in a cell is displayed. Use `print(...)` for others.
- Restart the kernel to clear everything, then run all cells from the top.
- Save with **Cmd+S**. Unsaved cells are not on disk or in git.
- Put reusable code in `f1/*.py` files and import it. Notebooks are for running and showing things.
