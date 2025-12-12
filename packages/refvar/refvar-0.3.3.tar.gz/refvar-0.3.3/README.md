# refvar

`refvar` is a lightweight, reactive, and efficient library for managing shared values ​​in Python.

It allows you to create **reactive variables** that trigger callbacks whenever their content changes—even when the value is mutable, such as lists or dictionaries.

The library is ideal for situations where multiple parts of the code need to share the same centralized variable without losing the original reference.

---

## 🚀 Features

- Reactive variable (`Ref`)
- Automatic callbacks when the value changes
- Support for **immutable and mutable** values
- Intelligent interception of mutable methods (`append`, `pop`, `update`, etc.)
- Lightweight and efficient (`__slots__`)
- Zero external dependencies
- Simple and intuitive API:

- `ref(value)`

- `ref(new_value)` or `.set()`

- `ref()` or `.get()` to get the value

- `ref(..., raw=True)` to directly call the stored function

- `.bind()` / `.unbind()` for callbacks

---

## ✨ Functionalities

- **Complete reactivity:** any change triggers callbacks.

- **Compatible with mutable types:** unlike previous versions.

- **Python Syntax:** implements magic operators and methods.

- **Direct calls with `raw=True`:** execute the value as a function.

- **Maximum lightweight:** designed for performance and low memory usage.

---

## 🧩 What is `raw=True` mode?

The call:

```python
ref(..., raw=True)

```

allows you to **directly execute the internal value as a function**, without activating the normal *get/set* behavior of `Ref`.

### Examples:

#### 1. Ref to function
```python
log = Ref(print)

log("Hello world!", raw=True)

```

Output:

```
Hello world!

``` ```

#### 2. Ref for custom function
```python
def sum(a, b):

return a + b

f = Ref(sum)

print(f(10, 5, raw=True)) # 15
```

#### 3. Keeps reactivity completely separate
The `raw` mode **never triggers callbacks**, as it does not alter `ref.value`, it only calls the content.

### When to use `raw=True`?

- When you store a function inside a `Ref`

- When you want to use `Ref` as a functional proxy
- When you want to avoid reactive logic and just execute something

---

## ✅ Recommended Types

The `Ref` class works well with all types:

### Immutable:
- `str`
- `int`
- `float`
- `bool`

- `None`

### Mutable (fully supported in version 0.3.1):
- `list`
- `dict`
- `set`
- custom classes
- objects storable in any Python structure

---

## 📦 Installation

```bash`pip install refvar`
```

---

## 🔧 Basic Example (immutable)

```python``from refvar` ... `on_change(ref, new_value):`

`print("Value changed to:", new_value)`

`x.bind(on_change)`

`x(20)` # Updates and triggers callback

`print(x())` # 20
`print(x.get())` # 20
`print(x)` # Ref(20)`

```

---

## 🔧 Example with (mutable) Lists

```python
list = Ref([])`

`def on_change(ref, new_value):`

`print("List updated:", new_value)`

`list.bind(on_change)`

`list.append(1)` # triggers callback
`list.append(2)` # triggers callback
`list.pop()` # triggers callback
```

Output:

```
Updated list: [1]
Updated list: [1, 2]
Updated list: [1]

```

---

## 🔧 Example of Using `raw=True`

```python
from refvar import Ref

def double(n):

return n * 2

f = Ref(double)

print(f(5, raw=True)) # 10
```

---

## 📘 License

MIT License.