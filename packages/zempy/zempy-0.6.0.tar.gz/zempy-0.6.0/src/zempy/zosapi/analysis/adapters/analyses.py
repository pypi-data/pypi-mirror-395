from __future__ import annotations
from typing import Optional, Union
from dataclasses import dataclass
from zempy.zosapi.core.base_adapter import BaseAdapter
from zempy.zosapi.core.types_var import N, Z
from zempy.zosapi.core.property_scalar import PropertyScalar
from zempy.zosapi.analysis.protocols.ia_ import IA_
from zempy.zosapi.analysis.enums.analysis_idm import AnalysisIDM
from zempy.zosapi.analysis.adapters.ia import IA
from zempy.zosapi.core.interop import run_native
from zempy.zosapi.analysis.adapters.analysis_registry import get_analysis_class
from allytools.types.validate_cast import validate_cast

@dataclass
class Analyses(BaseAdapter[Z, N]):

    NumberOfAnalyses      = PropertyScalar("NumberOfAnalyses",   coerce_get=int)


    def CloseAnalysis(self, arg: Union[int, IA_]) -> bool:
        def _call() -> bool:
            if isinstance(arg, int):
                return bool(self.native.CloseAnalysis(int(arg)))
            # assume adapter with .analysis -> native window
            return bool(self.native.CloseAnalysis(getattr(arg, "analysis")))

        return run_native(
            "Analyses.CloseAnalysis",
            _call,
            ensure=self.ensure_native,
        )

    def Get_AnalysisAtIndex(self, index: int) -> Optional[IA_]:
        native_a = run_native(
            "Analyses.Get_AnalysisAtIndex",
            lambda: self.native.Get_AnalysisAtIndex(int(index)),
            ensure=self.ensure_native,
        )
        native_type = run_native(
            "ZOSAPI.Analysis.IA_.AnalysisType",
            lambda: native_a.AnalysisType)
        analysis_type = AnalysisIDM.from_native(self.zosapi, native_type)
        return None if native_a is None else IA(self.zosapi, native_a, analysis_type)

    def New_Analysis(self, analysis_type: AnalysisIDM) -> Optional[IA_]:
        native_a = run_native(
            "I_Analyses.New_Analysis",
            lambda: self.native.New_Analysis(analysis_type.to_native(self.zosapi, analysis_type)),
            ensure=self.ensure_native,
        )
        if native_a is None:
            return None
        AnalysisCls = get_analysis_class(analysis_type)
        return validate_cast(AnalysisCls(self.zosapi, native_a, analysis_type), IA_)

    def New_Analysis_SettingsFirst(self, analysis_type: AnalysisIDM) -> Optional[IA_]:
        native_a = run_native(
            "I_Analyses.New_Analysis_SettingsFirst",
            lambda: self.native.New_Analysis_SettingsFirst(analysis_type),
            ensure=self.ensure_native,
        )
        if native_a is None:
            return None
        # We didn’t pass idm before; resolve it from the native handle to be safe:
        native_type = run_native(
            "ZOSAPI.Analysis.IA_.AnalysisType get",
            lambda: native_a.AnalysisType,
            ensure=self.ensure_native,
        )
        resolved_idm = AnalysisIDM.from_native(self.zosapi, native_type)
        AnalysisCls = get_analysis_class(resolved_idm)
        return validate_cast(AnalysisCls(self.zosapi, native_a, resolved_idm), IA_)

    def New_FftPsf(self) -> Optional[IA_]:
        native_a = run_native(
            "I_Analyses.New_FftPsf",
            lambda: self.native.New_FftPsf(),
            ensure=self.ensure_native,
        )
        if native_a is None:
            return None
        idm = AnalysisIDM.FftPsf
        AnalysisCls = get_analysis_class(idm)
        return validate_cast(AnalysisCls(self.zosapi, native_a, idm), IA_)

    def  New_HuygensPsf (self) -> Optional[IA_]:
        native_a = run_native(
            "I_Analyses.New_HuygensPsf",
            lambda: self.native.New_HuygensPsf(),
            ensure=self.ensure_native,
        )
        if native_a is None:
            return None
        idm = AnalysisIDM.HuygensPsf
        AnalysisCls = get_analysis_class(idm)
        return validate_cast(AnalysisCls(self.zosapi, native_a, idm), IA_)


    def  New_ZernikeStandardCoefficients (self) -> Optional[IA_]:
        native_a = run_native(
            "I_Analyses.New_ZernikeStandardCoefficients",
            lambda: self.native.New_ZernikeStandardCoefficients(),
            ensure=self.ensure_native,
        )
        if native_a is None:
            return None
        idm = AnalysisIDM.ZernikeStandardCoefficients
        AnalysisCls = get_analysis_class(idm)
        return validate_cast(AnalysisCls(self.zosapi, native_a, idm), IA_)

