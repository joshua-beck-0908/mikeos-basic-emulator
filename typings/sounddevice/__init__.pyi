"""
This type stub file was generated by pyright.
"""


from typing import Optional
import numpy as np
import numpy.typing as npt



def play(
    data: npt.ArrayLike, 
    samplerate: Optional[int] = None,
    mapping: Optional[npt.ArrayLike] = None, 
    blocking: Optional[bool] = False,
    loop: Optional[bool] = False
    ) -> None:
    ...
    
def stop(
    ignore_errors: Optional[bool] = False
    ) -> None:
    ...
    
def wait(
    ignore_errors: Optional[bool] = False
    ) -> None:
    ...