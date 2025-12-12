import typing
from good_common.utilities import deep_attribute_get

T = typing.TypeVar("T")


class placeholder(typing.Generic[T]):
    def __init__(
        self,
        key,
        default: T | None = None,
        post_process: typing.Callable[[typing.Any], T] | None = None,
        **kwargs,
    ):
        self.key = key
        self.default = default
        self.post_process = post_process
        self.kwargs = kwargs

    def __call__(self, **kwargs) -> T | None:
        el = kwargs.get(self.key, self.default)

        if callable(el):
            val = typing.cast(T | None, el(**{**self.kwargs, **kwargs}))
        else:
            val = typing.cast(T | None, el)

        if self.post_process:
            return self.post_process(val)
        return val

    def __repr__(self):
        _type = "undefined"
        if _arg := deep_attribute_get(self, "__orig_class__.__args__[0]", default=[]):
            try:
                _type = _arg.__repr__()
            except TypeError:
                if hasattr(_arg, "__name__"):
                    _type = getattr(_arg, "__name__")
                else:
                    _type = str(_arg)
        return f"{{{self.key}[{_type}]: {self.default}}}"

    @staticmethod
    def resolve(data, **kwargs):
        _data = data.copy()
        for key, value in _data.items():
            if isinstance(value, placeholder):
                _data[key] = value(**kwargs)
            elif isinstance(value, dict):
                # placeholder._set_placeholder(value, **kwargs)
                _data[key] = placeholder.resolve(value, **kwargs)
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    if isinstance(item, dict):
                        _data[key][i] = placeholder.resolve(item, **kwargs)
        return _data
