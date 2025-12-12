from typing import Any
from ...fable_modules.fable_library.int32 import parse
from ...fable_modules.fable_library.option import map
from ...fable_modules.fable_library.reg_exp import (match, create, get_item, groups)
from ...fable_modules.fable_library.string_ import replace

def Pattern_handleGroupPatterns(pattern: str) -> str:
    return replace(pattern, "(?<", "(?P<")


Pattern_ExcelNumberFormat: str = ("\"(?<" + "numberFormat") + ">(.*?))\""

Pattern_TermAnnotationShortPattern: str = ((("(?<" + "idspace") + ">\\w+?):(?<") + "localid") + ">\\w+)"

Pattern_TermAnnotationURIPattern: str = ((("http://purl.obolibrary.org/obo/(?<" + "idspace") + ">\\w+?)_(?<") + "localid") + ">\\w+)"

Pattern_TermAnnotationURIPattern_lessRestrictive: str = (((".*\\/(?<" + "idspace") + ">\\w+?)[:_](?<") + "localid") + ">\\w+)"

Pattern_TermAnnotationURIPattern_MS_RO_PO: str = (((".*252F(?<" + "idspace") + ">\\w+?)_(?<") + "localid") + ">\\w+)"

Pattern_IOTypePattern: str = ("(Input|Output)\\s*\\[(?<" + "iotype") + ">.+)\\]"

Pattern_InputPattern: str = ("Input\\s*\\[(?<" + "iotype") + ">.+)\\]"

Pattern_OutputPattern: str = ("Output\\s*\\[(?<" + "iotype") + ">.+)\\]"

Pattern_CommentPattern: str = ("Comment\\s*\\[(?<" + "commentKey") + ">.+)\\]"

def ActivePatterns__007CRegex_007C__007C(pattern: str, input: str) -> Any | None:
    m: Any = match(create(Pattern_handleGroupPatterns(pattern)), input.strip())
    if m is not None:
        return m

    else: 
        return None



def ActivePatterns__007CReferenceColumnHeader_007C__007C(input: str) -> dict[str, Any] | None:
    active_pattern_result: Any | None = ActivePatterns__007CRegex_007C__007C("(Term Source REF|Term Accession Number)\\s*\\((?<id>.*)\\)", input)
    if active_pattern_result is not None:
        r: Any = active_pattern_result
        return {
            "Annotation": get_item(groups(r), "id") or ""
        }

    else: 
        return None



def ActivePatterns__007CTermColumn_007C__007C(input: str) -> dict[str, Any] | None:
    active_pattern_result: Any | None = ActivePatterns__007CRegex_007C__007C("(?<termcolumntype>.+?)\\s*\\[(?<termname>.+)\\]", input)
    if active_pattern_result is not None:
        r: Any = active_pattern_result
        return {
            "TermColumnType": get_item(groups(r), "termcolumntype") or "",
            "TermName": get_item(groups(r), "termname") or ""
        }

    else: 
        return None



def ActivePatterns__007CUnitColumnHeader_007C__007C(input: str) -> str | None:
    active_pattern_result: Any | None = ActivePatterns__007CRegex_007C__007C("Unit", input)
    if active_pattern_result is not None:
        o: Any = active_pattern_result
        return o[0]

    else: 
        return None



def ActivePatterns__007CParameterColumnHeader_007C__007C(input: str) -> str | None:
    active_pattern_result: dict[str, Any] | None = ActivePatterns__007CTermColumn_007C__007C(input)
    if active_pattern_result is not None:
        r: dict[str, Any] = active_pattern_result
        match_value: str = r["TermColumnType"]
        (pattern_matching_result,) = (None,)
        if match_value == "Parameter":
            pattern_matching_result = 0

        elif match_value == "Parameter Value":
            pattern_matching_result = 0

        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return r["TermName"]

        elif pattern_matching_result == 1:
            return None


    else: 
        return None



def ActivePatterns__007CFactorColumnHeader_007C__007C(input: str) -> str | None:
    active_pattern_result: dict[str, Any] | None = ActivePatterns__007CTermColumn_007C__007C(input)
    if active_pattern_result is not None:
        r: dict[str, Any] = active_pattern_result
        match_value: str = r["TermColumnType"]
        (pattern_matching_result,) = (None,)
        if match_value == "Factor":
            pattern_matching_result = 0

        elif match_value == "Factor Value":
            pattern_matching_result = 0

        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return r["TermName"]

        elif pattern_matching_result == 1:
            return None


    else: 
        return None



def ActivePatterns__007CCharacteristicColumnHeader_007C__007C(input: str) -> str | None:
    active_pattern_result: dict[str, Any] | None = ActivePatterns__007CTermColumn_007C__007C(input)
    if active_pattern_result is not None:
        r: dict[str, Any] = active_pattern_result
        match_value: str = r["TermColumnType"]
        (pattern_matching_result,) = (None,)
        if match_value == "Characteristic":
            pattern_matching_result = 0

        elif match_value == "Characteristics":
            pattern_matching_result = 0

        elif match_value == "Characteristics Value":
            pattern_matching_result = 0

        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return r["TermName"]

        elif pattern_matching_result == 1:
            return None


    else: 
        return None



def ActivePatterns__007CComponentColumnHeader_007C__007C(input: str) -> str | None:
    active_pattern_result: dict[str, Any] | None = ActivePatterns__007CTermColumn_007C__007C(input)
    if active_pattern_result is not None:
        r: dict[str, Any] = active_pattern_result
        match_value: str = r["TermColumnType"]
        (pattern_matching_result,) = (None,)
        if match_value == "Component":
            pattern_matching_result = 0

        elif match_value == "Component Value":
            pattern_matching_result = 0

        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return r["TermName"]

        elif pattern_matching_result == 1:
            return None


    else: 
        return None



def ActivePatterns__007CTermAnnotationShort_007C__007C(input: str) -> dict[str, Any] | None:
    active_pattern_result: Any | None = ActivePatterns__007CRegex_007C__007C(Pattern_TermAnnotationShortPattern, input)
    if active_pattern_result is not None:
        value: Any = active_pattern_result
        return {
            "IDSpace": get_item(groups(value), "idspace") or "",
            "LocalID": get_item(groups(value), "localid") or ""
        }

    else: 
        return None



def ActivePatterns__007CTermAnnotation_007C__007C(input: str) -> dict[str, Any] | None:
    (pattern_matching_result, value) = (None, None)
    active_pattern_result: Any | None = ActivePatterns__007CRegex_007C__007C(Pattern_TermAnnotationShortPattern, input)
    if active_pattern_result is not None:
        pattern_matching_result = 0
        value = active_pattern_result

    else: 
        active_pattern_result_1: Any | None = ActivePatterns__007CRegex_007C__007C(Pattern_TermAnnotationURIPattern, input)
        if active_pattern_result_1 is not None:
            pattern_matching_result = 0
            value = active_pattern_result_1

        else: 
            active_pattern_result_2: Any | None = ActivePatterns__007CRegex_007C__007C(Pattern_TermAnnotationURIPattern_lessRestrictive, input)
            if active_pattern_result_2 is not None:
                pattern_matching_result = 0
                value = active_pattern_result_2

            else: 
                active_pattern_result_3: Any | None = ActivePatterns__007CRegex_007C__007C(Pattern_TermAnnotationURIPattern_MS_RO_PO, input)
                if active_pattern_result_3 is not None:
                    pattern_matching_result = 0
                    value = active_pattern_result_3

                else: 
                    pattern_matching_result = 1




    if pattern_matching_result == 0:
        return {
            "IDSpace": get_item(groups(value), "idspace") or "",
            "LocalID": get_item(groups(value), "localid") or ""
        }

    elif pattern_matching_result == 1:
        return None



def ActivePatterns__007CTSRColumnHeader_007C__007C(input: str) -> dict[str, Any] | None:
    active_pattern_result: Any | None = ActivePatterns__007CRegex_007C__007C("Term Source REF\\s*\\((?<id>.*)\\)", input)
    if active_pattern_result is not None:
        r: Any = active_pattern_result
        match_value: str = get_item(groups(r), "id") or ""
        active_pattern_result_1: dict[str, Any] | None = ActivePatterns__007CTermAnnotation_007C__007C(match_value)
        if active_pattern_result_1 is not None:
            r_1: dict[str, Any] = active_pattern_result_1
            return r_1

        else: 
            return {
                "IDSpace": "",
                "LocalID": ""
            }


    else: 
        return None



def ActivePatterns__007CTANColumnHeader_007C__007C(input: str) -> dict[str, Any] | None:
    active_pattern_result: Any | None = ActivePatterns__007CRegex_007C__007C("Term Accession Number\\s*\\((?<id>.*)\\)", input)
    if active_pattern_result is not None:
        r: Any = active_pattern_result
        match_value: str = get_item(groups(r), "id") or ""
        active_pattern_result_1: dict[str, Any] | None = ActivePatterns__007CTermAnnotation_007C__007C(match_value)
        if active_pattern_result_1 is not None:
            r_1: dict[str, Any] = active_pattern_result_1
            return r_1

        else: 
            return {
                "IDSpace": "",
                "LocalID": ""
            }


    else: 
        return None



def ActivePatterns__007CInputColumnHeader_007C__007C(input: str) -> str | None:
    active_pattern_result: Any | None = ActivePatterns__007CRegex_007C__007C(Pattern_InputPattern, input)
    if active_pattern_result is not None:
        r: Any = active_pattern_result
        return get_item(groups(r), "iotype") or ""

    else: 
        return None



def ActivePatterns__007COutputColumnHeader_007C__007C(input: str) -> str | None:
    active_pattern_result: Any | None = ActivePatterns__007CRegex_007C__007C(Pattern_OutputPattern, input)
    if active_pattern_result is not None:
        r: Any = active_pattern_result
        return get_item(groups(r), "iotype") or ""

    else: 
        return None



def ActivePatterns__007CAutoGeneratedTableName_007C__007C(input: str) -> int | None:
    active_pattern_result: Any | None = ActivePatterns__007CRegex_007C__007C("^New\\sTable\\s(?<number>\\d+)$", input)
    if active_pattern_result is not None:
        r: Any = active_pattern_result
        return parse(get_item(groups(r), "number") or "", 511, False, 32)

    else: 
        return None



def ActivePatterns__007CComment_007C__007C(input: str) -> str | None:
    active_pattern_result: Any | None = ActivePatterns__007CRegex_007C__007C(Pattern_CommentPattern, input)
    if active_pattern_result is not None:
        r: Any = active_pattern_result
        return get_item(groups(r), "commentKey") or ""

    else: 
        return None



def try_parse_reference_column_header(str_1: str) -> dict[str, Any] | None:
    match_value: str = str_1.strip()
    active_pattern_result: dict[str, Any] | None = ActivePatterns__007CReferenceColumnHeader_007C__007C(match_value)
    if active_pattern_result is not None:
        v: dict[str, Any] = active_pattern_result
        return v

    else: 
        return None



def try_parse_term_annotation_short(str_1: str) -> dict[str, Any] | None:
    match_value: str = str_1.strip()
    active_pattern_result: Any | None = ActivePatterns__007CRegex_007C__007C(Pattern_TermAnnotationShortPattern, match_value)
    if active_pattern_result is not None:
        value: Any = active_pattern_result
        return {
            "IDSpace": get_item(groups(value), "idspace") or "",
            "LocalID": get_item(groups(value), "localid") or ""
        }

    else: 
        return None



def try_parse_term_annotation(str_1: str) -> dict[str, Any] | None:
    match_value: str = str_1.strip()
    (pattern_matching_result, value) = (None, None)
    active_pattern_result: Any | None = ActivePatterns__007CRegex_007C__007C(Pattern_TermAnnotationShortPattern, match_value)
    if active_pattern_result is not None:
        pattern_matching_result = 0
        value = active_pattern_result

    else: 
        active_pattern_result_1: Any | None = ActivePatterns__007CRegex_007C__007C(Pattern_TermAnnotationURIPattern, match_value)
        if active_pattern_result_1 is not None:
            pattern_matching_result = 0
            value = active_pattern_result_1

        else: 
            active_pattern_result_2: Any | None = ActivePatterns__007CRegex_007C__007C(Pattern_TermAnnotationURIPattern_lessRestrictive, match_value)
            if active_pattern_result_2 is not None:
                pattern_matching_result = 0
                value = active_pattern_result_2

            else: 
                active_pattern_result_3: Any | None = ActivePatterns__007CRegex_007C__007C(Pattern_TermAnnotationURIPattern_MS_RO_PO, match_value)
                if active_pattern_result_3 is not None:
                    pattern_matching_result = 0
                    value = active_pattern_result_3

                else: 
                    pattern_matching_result = 1




    if pattern_matching_result == 0:
        return {
            "IDSpace": get_item(groups(value), "idspace") or "",
            "LocalID": get_item(groups(value), "localid") or ""
        }

    elif pattern_matching_result == 1:
        return None



def try_get_term_annotation_short_string(str_1: str) -> str | None:
    def mapping(r: dict[str, Any], str_1: Any=str_1) -> str:
        return (r["IDSpace"] + ":") + r["LocalID"]

    return map(mapping, try_parse_term_annotation(str_1))


def get_term_annotation_short_string(str_1: str) -> str:
    match_value: str | None = try_get_term_annotation_short_string(str_1)
    if match_value is None:
        raise Exception(("Unable to parse \'" + str_1) + "\' to term accession.")

    else: 
        return match_value



def try_parse_excel_number_format(header_str: str) -> str | None:
    match_value: str = header_str.strip()
    active_pattern_result: Any | None = ActivePatterns__007CRegex_007C__007C(Pattern_ExcelNumberFormat, match_value)
    if active_pattern_result is not None:
        value: Any = active_pattern_result
        return get_item(groups(value), "numberFormat") or ""

    else: 
        return None



def try_parse_iotype_header(header_str: str) -> str | None:
    match_value: str = header_str.strip()
    active_pattern_result: Any | None = ActivePatterns__007CRegex_007C__007C(Pattern_IOTypePattern, match_value)
    if active_pattern_result is not None:
        value: Any = active_pattern_result
        return get_item(groups(value), "iotype") or ""

    else: 
        return None



def try_parse_term_column(input: str) -> dict[str, Any] | None:
    active_pattern_result: dict[str, Any] | None = ActivePatterns__007CTermColumn_007C__007C(input)
    if active_pattern_result is not None:
        r: dict[str, Any] = active_pattern_result
        return r

    else: 
        return None



def try_parse_unit_column_header(input: str) -> str | None:
    active_pattern_result: str | None = ActivePatterns__007CUnitColumnHeader_007C__007C(input)
    if active_pattern_result is not None:
        r: str = active_pattern_result
        return r

    else: 
        return None



def try_parse_parameter_column_header(input: str) -> str | None:
    active_pattern_result: str | None = ActivePatterns__007CParameterColumnHeader_007C__007C(input)
    if active_pattern_result is not None:
        r: str = active_pattern_result
        return r

    else: 
        return None



def try_parse_factor_column_header(input: str) -> str | None:
    active_pattern_result: str | None = ActivePatterns__007CFactorColumnHeader_007C__007C(input)
    if active_pattern_result is not None:
        r: str = active_pattern_result
        return r

    else: 
        return None



def try_parse_characteristic_column_header(input: str) -> str | None:
    active_pattern_result: str | None = ActivePatterns__007CCharacteristicColumnHeader_007C__007C(input)
    if active_pattern_result is not None:
        r: str = active_pattern_result
        return r

    else: 
        return None



def try_parse_component_column_header(input: str) -> str | None:
    active_pattern_result: str | None = ActivePatterns__007CComponentColumnHeader_007C__007C(input)
    if active_pattern_result is not None:
        r: str = active_pattern_result
        return r

    else: 
        return None



def try_parse_tsrcolumn_header(input: str) -> dict[str, Any] | None:
    active_pattern_result: dict[str, Any] | None = ActivePatterns__007CTSRColumnHeader_007C__007C(input)
    if active_pattern_result is not None:
        r: dict[str, Any] = active_pattern_result
        return r

    else: 
        return None



def try_parse_tancolumn_header(input: str) -> dict[str, Any] | None:
    active_pattern_result: dict[str, Any] | None = ActivePatterns__007CTANColumnHeader_007C__007C(input)
    if active_pattern_result is not None:
        r: dict[str, Any] = active_pattern_result
        return r

    else: 
        return None



def try_parse_input_column_header(input: str) -> str | None:
    active_pattern_result: str | None = ActivePatterns__007CInputColumnHeader_007C__007C(input)
    if active_pattern_result is not None:
        r: str = active_pattern_result
        return r

    else: 
        return None



def try_parse_output_column_header(input: str) -> str | None:
    active_pattern_result: str | None = ActivePatterns__007COutputColumnHeader_007C__007C(input)
    if active_pattern_result is not None:
        r: str = active_pattern_result
        return r

    else: 
        return None



__all__ = ["Pattern_handleGroupPatterns", "Pattern_ExcelNumberFormat", "Pattern_TermAnnotationShortPattern", "Pattern_TermAnnotationURIPattern", "Pattern_TermAnnotationURIPattern_lessRestrictive", "Pattern_TermAnnotationURIPattern_MS_RO_PO", "Pattern_IOTypePattern", "Pattern_InputPattern", "Pattern_OutputPattern", "Pattern_CommentPattern", "ActivePatterns__007CRegex_007C__007C", "ActivePatterns__007CReferenceColumnHeader_007C__007C", "ActivePatterns__007CTermColumn_007C__007C", "ActivePatterns__007CUnitColumnHeader_007C__007C", "ActivePatterns__007CParameterColumnHeader_007C__007C", "ActivePatterns__007CFactorColumnHeader_007C__007C", "ActivePatterns__007CCharacteristicColumnHeader_007C__007C", "ActivePatterns__007CComponentColumnHeader_007C__007C", "ActivePatterns__007CTermAnnotationShort_007C__007C", "ActivePatterns__007CTermAnnotation_007C__007C", "ActivePatterns__007CTSRColumnHeader_007C__007C", "ActivePatterns__007CTANColumnHeader_007C__007C", "ActivePatterns__007CInputColumnHeader_007C__007C", "ActivePatterns__007COutputColumnHeader_007C__007C", "ActivePatterns__007CAutoGeneratedTableName_007C__007C", "ActivePatterns__007CComment_007C__007C", "try_parse_reference_column_header", "try_parse_term_annotation_short", "try_parse_term_annotation", "try_get_term_annotation_short_string", "get_term_annotation_short_string", "try_parse_excel_number_format", "try_parse_iotype_header", "try_parse_term_column", "try_parse_unit_column_header", "try_parse_parameter_column_header", "try_parse_factor_column_header", "try_parse_characteristic_column_header", "try_parse_component_column_header", "try_parse_tsrcolumn_header", "try_parse_tancolumn_header", "try_parse_input_column_header", "try_parse_output_column_header"]

