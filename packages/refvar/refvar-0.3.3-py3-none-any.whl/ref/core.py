# ===============================================================
# RefVar 0.3.1 — Ultra-light reactive reference container
# ===============================================================
def _safe_copy(value):
    """Return an efficient shallow copy for mutable types."""
    if isinstance(value, list):
        return value[:]              # fastest copy
    if isinstance(value, dict):
        return value.copy()
    if isinstance(value, set):
        return value.copy()
    return value                     # immutable types: no copy needed


def _on_update(ref, new_value, old_value):
    """Return True if changed, dispatch callbacks."""
    if new_value == old_value:
        return False

    for cb in ref.callbacks:
        cb(ref, new_value)

    return True


class Ref:
    """
    A lightweight reactive wrapper for Python values.
    Automatically triggers callbacks when the value changes.
    """

    __slots__ = ("value", "callbacks")

    def __init__(self, value=None):
        self.value = value
        self.callbacks = set()

    # ---------------------------------------------------------
    # Core API
    # ---------------------------------------------------------

    def get(self):
        """Return the stored value."""
        return self.value

    def set(self, new_value):
        """Update the value and trigger callbacks if changed."""
        if _on_update(self, new_value, self.value):
            self.value = new_value
        return self

    def bind(self, *callbacks):
        """Register a callback: callback(ref, new_value)."""
        for callback in callbacks:
            self.callbacks.add(callback)
        return callback

    def unbind(self, *callbacks):
        for callback in callbacks:
            self.callbacks.discard(callback)
        return callbacks

    def __call__(self, *new_value, raw=False, **kwargs):
        """
        Getter:  ref() → value
        Setter:  ref(new_value)
        Raw:     ref(..., raw=True) → call underlying value
        """
        if raw:
            return self.value(*new_value, **kwargs)

        if new_value == ():
            return self.value

        return self.set(new_value[0])

    # ---------------------------------------------------------
    # Delegation to underlying type (fast)
    # ---------------------------------------------------------

    def __repr__(self):
        return f"Ref({self.value!r})"

    def __str__(self):
        return str(self.value)

    def __bool__(self):
        return bool(self.value)

    def __getattr__(self, name):
        try:
            return getattr(self.value, name)
        except AttributeError:
            raise AttributeError(f"{type(self.value).__name__!r} has no attribute {name!r}")

    def __setattr__(self, name, value):
        # Internal attributes
        if name in ("value", "callbacks"):
            object.__setattr__(self, name, value)
            return

        # Delegate attribute assignment to underlying value
        try:
            old = _safe_copy(self.value)
            setattr(self.value, name, value)
            _on_update(self, self.value, old)
        except Exception:
            raise AttributeError(f"Cannot set attribute {name!r} on Ref({self.value!r})")


# -------------------------------------------------------------
# Automatic delegation of immutable operations
# -------------------------------------------------------------

_DELEGATE = (
    "__add__", "__radd__", "__sub__", "__rsub__", "__mul__", "__rmul__",
    "__truediv__", "__floordiv__", "__mod__", "__pow__", "__getitem__",
    "__delitem__", "__contains__", "__iter__", "__len__","__ne__",
    "__lt__", "__le__", "__gt__", "__ge__", "__str__", "__iadd__",
    "__imul__", "__isub__", "__eq__"
)

def _make_delegate(name):
    def method(self, *args, **kwargs):
        return getattr(self.value, name)(*args, **kwargs)
    return method

for _name in _DELEGATE:
    setattr(Ref, _name, _make_delegate(_name))


# -------------------------------------------------------------
# Interception of mutating operations
# -------------------------------------------------------------

_MUTATING = (
    "append", "remove", "pop", "add", "extend",
    "insert", "clear", "update"
)

def _make_mutating(name):
    def method(self, *args, **kwargs):
        old = _safe_copy(self.value)
        result = getattr(self.value, name)(*args, **kwargs)
        _on_update(self, self.value, old)
        return result
    return method

for _name in _MUTATING:
    setattr(Ref, _name, _make_mutating(_name))
