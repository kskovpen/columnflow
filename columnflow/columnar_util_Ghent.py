# coding: utf-8

"""
Helpers and utilities for working with columnar libraries (Ghent cms group)
"""

from __future__ import annotations
from typing import Literal

__all__ = [
    "TetraVec", "safe_concatenate",
]

from columnflow.util import maybe_import
from columnflow.types import Sequence

ak = maybe_import("awkward")
coffea = maybe_import("coffea")

# ORIGINAL
# def TetraVec(arr: ak.Array, keep: Sequence | str | Literal[-1] = -1) -> ak.Array:
#     """
#     create a Lorentz for fector from an awkward array with pt, eta, phi, and mass fields
#     """
#     mandatory_fields = ("pt", "eta", "phi", "mass")
#     exclude_fields = ("x", "y", "z", "t")
#     for field in mandatory_fields:
#         assert hasattr(arr, field), f"Provided array is missing {field} field"
#     if isinstance(keep, str):
#         keep = [keep]
#     elif keep == -1:
#         keep = arr.fields
#     keep = [*keep, *mandatory_fields]
#     return ak.zip(
#         {p: getattr(arr, p) for p in keep if p not in exclude_fields},
#         with_name="PtEtaPhiMLorentzVector",
#         behavior=coffea.nanoevents.methods.vector.behavior,
#     )

def TetraVec(arr: ak.Array, prefix: str = "", keep: Sequence | str | Literal[-1] = -1,) -> ak.Array:
    components = ("pt", "eta", "phi", "mass")
    fields = tuple(f"{prefix}{c}" for c in components)

    if not all(f in arr.fields for f in fields):
        raise ValueError(f"Missing required fields: {fields}")

    if isinstance(keep, str):
        keep = [keep]
    elif keep == -1:
        keep = arr.fields
    keep = [*keep, *fields]
    
    return ak.zip(
        {c: getattr(arr, f) for c, f in zip(components, fields)},
        with_name="PtEtaPhiMLorentzVector",
        behavior=coffea.nanoevents.methods.vector.behavior,
    )


def Vector3D_xyz(arr: ak.Array, prefix: str = "") -> ak.Array:
    components = ("x", "y", "z")
    fields = (f"{prefix}x", f"{prefix}y", f"{prefix}z")

    if not all(f in arr.fields for f in fields):
        raise ValueError(f"Missing required fields: {fields}")

    return ak.zip(
        {c: getattr(arr, f) for c, f in zip(components, fields)},
        with_name="Vector3D",
        behavior=coffea.nanoevents.methods.vector.behavior,
    )


def safe_concatenate(arrays, *args, **kwargs):
    n = len(arrays)
    if n > 2 ** 7:
        c1 = safe_concatenate(arrays[:n // 2], *args, **kwargs)
        c2 = safe_concatenate(arrays[n // 2:], *args, **kwargs)
        return ak.concatenate([c1, c2], *args, **kwargs)
    return ak.concatenate(arrays, *args, **kwargs)
