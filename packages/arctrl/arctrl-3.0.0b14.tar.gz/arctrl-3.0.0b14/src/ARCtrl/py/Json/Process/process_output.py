from __future__ import annotations
from typing import Any
from ...fable_modules.fable_library.list import of_array
from ...fable_modules.thoth_json_core.decode import (one_of, map)
from ...fable_modules.thoth_json_core.types import (IEncodable, Decoder_1)
from ...Core.data import Data
from ...Core.Process.material import Material
from ...Core.Process.process_output import ProcessOutput
from ...Core.Process.sample import Sample
from ..data import (ROCrate_encoder as ROCrate_encoder_1, ROCrate_decoder as ROCrate_decoder_2, ISAJson_encoder as ISAJson_encoder_1, ISAJson_decoder as ISAJson_decoder_2)
from .material import (ROCrate_encoder as ROCrate_encoder_2, ROCrate_decoder as ROCrate_decoder_3, ISAJson_encoder as ISAJson_encoder_2, ISAJson_decoder as ISAJson_decoder_3)
from .sample import (ROCrate_encoder as ROCrate_encoder_3, ROCrate_decoder as ROCrate_decoder_1, ISAJson_encoder as ISAJson_encoder_3, ISAJson_decoder as ISAJson_decoder_1)

def ROCrate_encoder(value: ProcessOutput) -> IEncodable:
    if value.tag == 1:
        return ROCrate_encoder_1(value.fields[0])

    elif value.tag == 2:
        return ROCrate_encoder_2(value.fields[0])

    else: 
        return ROCrate_encoder_3(value.fields[0])



def _arrow2921(Item: Sample) -> ProcessOutput:
    return ProcessOutput(0, Item)


def _arrow2922(Item_1: Data) -> ProcessOutput:
    return ProcessOutput(1, Item_1)


def _arrow2923(Item_2: Material) -> ProcessOutput:
    return ProcessOutput(2, Item_2)


ROCrate_decoder: Decoder_1[ProcessOutput] = one_of(of_array([map(_arrow2921, ROCrate_decoder_1), map(_arrow2922, ROCrate_decoder_2), map(_arrow2923, ROCrate_decoder_3)]))

def ISAJson_encoder(id_map: Any | None, value: ProcessOutput) -> IEncodable:
    if value.tag == 1:
        return ISAJson_encoder_1(id_map, value.fields[0])

    elif value.tag == 2:
        return ISAJson_encoder_2(id_map, value.fields[0])

    else: 
        return ISAJson_encoder_3(id_map, value.fields[0])



def _arrow2925(Item: Sample) -> ProcessOutput:
    return ProcessOutput(0, Item)


def _arrow2926(Item_1: Data) -> ProcessOutput:
    return ProcessOutput(1, Item_1)


def _arrow2927(Item_2: Material) -> ProcessOutput:
    return ProcessOutput(2, Item_2)


ISAJson_decoder: Decoder_1[ProcessOutput] = one_of(of_array([map(_arrow2925, ISAJson_decoder_1), map(_arrow2926, ISAJson_decoder_2), map(_arrow2927, ISAJson_decoder_3)]))

__all__ = ["ROCrate_encoder", "ROCrate_decoder", "ISAJson_encoder", "ISAJson_decoder"]

