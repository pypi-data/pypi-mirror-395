######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.13.1+obcheckpoint(0.2.8);ob(v1)                                                   #
# Generated on 2025-12-09T00:44:36.557812                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.decorators

from ...exception import MetaflowException as MetaflowException

class ExitHookDecorator(metaflow.decorators.FlowDecorator, metaclass=type):
    def flow_init(self, flow, graph, environment, flow_datastore, metadata, logger, echo, options):
        ...
    ...

