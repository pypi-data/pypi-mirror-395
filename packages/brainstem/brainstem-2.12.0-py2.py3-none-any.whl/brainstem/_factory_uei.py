
from . import _BS_C
from .module import Entity

class _Factory_UEI(Entity):
    """ For internal use only.

    """
    def __init__(self, module, index):
        """Store initializer"""
        super(_Factory_UEI, self).__init__(module, _BS_C.cmdFACTORY_UEI, index)
