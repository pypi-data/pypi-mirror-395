from __future__ import annotations
from typing import TYPE_CHECKING
from zempy.zosapi.core.im_adapter import (
    BaseAdapter, Z, N, run_native, validate_cast,
    dataclass, logging,
)

from zempy.zosapi.core.property_scalar import PropertyScalar
from zempy.zosapi.tools.general.adapters.quickfocus.quick_focus import QuickFocus
from zempy.zosapi.tools.general.protocols.quickfocus.i_quick_focus import IQuickFocus
from zempy.zosapi.tools.raytrace.adapters.batch_ray_trace import BatchRayTrace
from zempy.zosapi.tools.raytrace.protocols.i_batch_ray_trace import IBatchRayTrace

if TYPE_CHECKING:
    from zempy.zosapi.tools.protocols.i_system_tool import ISystemTool


log = logging.getLogger(__name__)
@dataclass()
class OpticalSystemTools(BaseAdapter[Z, N]):
    """ Concrete adapter over native ZOSAPI.Tools.IOpticalSystemTools."""

    IsRunning     = PropertyScalar("IsRunning",  coerce_get=bool)
    Progress      = PropertyScalar("Progress",   coerce_get=int)
    Status    = PropertyScalar("Status", coerce_get=str)


    def CurrentTool(self) -> ISystemTool:
        native_tool = run_native(
            "Tools.CurrentTool",
            lambda: self.native.CurrentTool(),
            ensure=self.ensure_native,
        )
        log.debug("SystemTools.CurrentTool() call")
        return native_tool

    def OpenQuickFocus(self) -> IQuickFocus:
        """Open the Quick Focus tool and return its adapter."""
        native_qf = run_native(
            "Tools.OpenQuickFocus",
            lambda: self.native.OpenQuickFocus(),
            ensure=self.ensure_native,
        )
        log.debug("SystemTools.OpenQuickFocus() created")
        return validate_cast(QuickFocus(self.zosapi, native_qf), IQuickFocus)

    def OpenBatchRayTrace(self) -> IBatchRayTrace:
        """Open the BatchRayTrace tool and return its adapter."""
        native_qf = run_native(
            "Tools.OpenBatchRayTrace",
            lambda: self.native.OpenBatchRayTrace(),
            ensure=self.ensure_native,
        )
        log.debug("SystemTools.OpenQuickFocus() created")
        return validate_cast(BatchRayTrace(self.zosapi, native_qf), IBatchRayTrace)




    def RemoveAllVariables(self) -> bool:
        """Remove all lens/system variables. Returns True on success."""
        ok = run_native(
            "Tools.RemoveAllVariables",
            lambda: getattr(self.native, "RemoveAllVariables")(),
            ensure=self.ensure_native,
        )
        log.debug("SystemTools.RemoveAllVariables() is completed")
        return bool(ok)