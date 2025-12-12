# Bit-vector sets

Efficient implementation of immutable sets using bit-vectors.

It follow the same specification as `set` and `frozenset`.

```
A = BitVectorSet((0,2,4))
# {0, 2, 4}

B = BitVectorSet((0,1,2))
# {0, 1, 2}

print("Intersection:", A & B)
# {0, 2}
```

See [the demo and tests](demo.ipynb) for further informations.