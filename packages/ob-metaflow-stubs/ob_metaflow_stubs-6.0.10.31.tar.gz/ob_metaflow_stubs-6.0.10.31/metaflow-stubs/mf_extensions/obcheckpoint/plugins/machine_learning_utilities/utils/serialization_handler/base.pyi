######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.13.1+obcheckpoint(0.2.8);ob(v1)                                                   #
# Generated on 2025-12-09T00:44:36.625942                                                            #
######################################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import typing


class SerializationHandler(object, metaclass=type):
    def serialze(self, *args, **kwargs) -> typing.Union[str, bytes]:
        ...
    def deserialize(self, *args, **kwargs) -> typing.Any:
        ...
    ...

