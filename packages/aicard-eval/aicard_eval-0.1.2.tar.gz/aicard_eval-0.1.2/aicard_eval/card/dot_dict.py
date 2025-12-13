from .fields import Field


class DotDict(dict):
    def __init__(self, **kwargs):
        super().__init__({k: v for k,v in kwargs.items()})

    def __getattr__(self, attr):
        try:
            ret = self[attr]
            return ret.get() if isinstance(ret, Field) else ret
        except KeyError: raise AttributeError

    def __setattr__(self, attr, value):
        assert attr in self, f"Can only set an existing attribute among: {', '.join(self.keys())}"
        if isinstance(self[attr], Field): self[attr].set(value)
        else: self[attr] = value

    def __delattr__(self, attr):
        try: del self[attr]
        except KeyError: raise AttributeError

    def validate_integrity(self):
        for k, v in self.items():
            if isinstance(v, DotDict): v.validate_integrity()
            else: assert isinstance(v, Field), f"{k} was overwritten with non-expected {type(v)}"

    def validate_assign(self, other: dict):
        self.validate_integrity()
        assert isinstance(other, dict), f"Can only assign dictionaries to field, not {type(other)}"
        for k in other:
            if k not in self: raise AssertionError(f"Cannot assign to field {k}. Candidates: "+",".join(self.keys()))
            if isinstance(self[k], DotDict): self[k].validate_assign(other[k])

    def _assign(self, other: dict):
        for k in self:
            if k in other:
                field = self[k]
                if isinstance(field, DotDict): field._assign(other[k])
                else: field.set(other[k])

    def assign(self, other: dict):
        self._assign(other)
        return self

    def _append(self, other: dict, message:str):
        self.validate_integrity()
        for k in self:
            if k in other:
                if isinstance(self[k], DotDict): self[k]._append(other[k], message)
                elif message is None:
                    if other.get(k): self[k].set(other[k])
                else:
                    existing = str(self.get(k, ""))
                    if not existing.endswith("\n"): existing += "\n"
                    if existing: existing += "\n"
                    self[k].set(existing+message+str(other[k]))

    def append(self, other: dict, message: str):
        self.validate_assign(other)
        self._append(other, message)
        return self

    def flatten(self):
        self.validate_integrity()
        flattened = dict()
        for k, v in self.items():
            if isinstance(v, DotDict):
                for k2, v2 in v.flatten().items(): flattened[f"{k}__{k2}"] = v2.get() if isinstance(v2, Field) else v2
            else: flattened[k] = v.get() if isinstance(v, Field) else v
        return flattened

    def assign_flattened(self, all_items: dict, prefix=""):
        self.validate_integrity()
        assert not isinstance(all_items, DotDict)
        for k in list(self.keys()):
            query = f"{prefix}__{k}" if prefix else k
            v = self[k]
            if isinstance(v, DotDict): v.assign_flattened(all_items, query)
            elif query in all_items: v.set(all_items[query])
        return self
