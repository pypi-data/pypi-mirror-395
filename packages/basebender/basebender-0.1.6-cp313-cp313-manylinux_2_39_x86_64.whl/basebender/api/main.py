"""
This module defines the FastAPI application for the BaseBender API.

It provides endpoints for listing available digit sets and rebaseing text
between different digit sets.
"""

from typing import Dict, List, Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from basebender.rebaser.digit_set_rebaser import DigitSetRebaser
from basebender.rebaser.digit_sets import get_predefined_digit_sets
from basebender.rebaser.models import DigitSet

APP = FastAPI(
    title="BaseBender API",
    description=(
        "API for rebaseing text between different digit sets and "
        "listing available digit sets."
    ),
    version="1.0.0",
)

# Cache for digit sets to avoid reloading for every request
_DIGIT_SET_DATA: Optional[Dict[str, DigitSet]] = None


def _load_digit_set_data() -> Dict[str, DigitSet]:
    """
    Loads and caches predefined digit set data.

    This function retrieves the predefined digit sets and caches them
    in the `_DIGIT_SET_DATA` module-level variable to avoid redundant
    loading on subsequent calls.

    Returns:
        A dictionary mapping digit set IDs to DigitSet objects.
    """
    global _DIGIT_SET_DATA  # pylint: disable=global-statement
    if _DIGIT_SET_DATA is None:
        _DIGIT_SET_DATA = get_predefined_digit_sets()
    return _DIGIT_SET_DATA


@APP.get("/", include_in_schema=False)
async def redirect_to_docs() -> RedirectResponse:
    """
    Redirects the root URL ("/") to the API documentation page ("/docs").

    Returns:
        A RedirectResponse to the /docs endpoint.
    """
    return RedirectResponse(url="/docs")


class DigitSetInfo(BaseModel):
    """
    Pydantic model representing information about a digit set.

    Attributes:
        id: The unique identifier of the digit set (e.g., "binary", "decimal").
        name: A human-readable name for the digit set (e.g., "Binary", "Decimal").
        digits: The string containing all unique digits of the set in order.
        source: The origin of the digit set (e.g., "predefined", "cli_input", "api_input").
    """

    id: str
    name: str
    digits: str
    source: str


@APP.get(
    "/digitsets",
    response_model=List[DigitSetInfo],
    summary="List all available digit sets",
)
async def list_digit_sets() -> List[DigitSetInfo]:
    """
    Retrieves a list of all available digit sets, including their unique IDs,
    names, digits, and source.
    """
    digit_sets = _load_digit_set_data()
    digit_set_list: List[DigitSetInfo] = []
    for digit_set_id, digit_set_info in digit_sets.items():
        digit_set_list.append(
            DigitSetInfo(
                id=digit_set_id,
                name=digit_set_info.name,
                digits=digit_set_info.digits,
                source=digit_set_info.source,
            )
        )
    return digit_set_list


class RebaseRequest(BaseModel):
    """
    Pydantic model for a rebase operation request.

    Attributes:
        input_text: The string to be rebased. Defaults to an empty string.
        source_digit_set: An optional string representing the source digit set
            (e.g., "0123456789ABCDEF"). If provided, takes precedence over `source_digit_set_id`.
        source_digit_set_id: An optional ID of a predefined source digit set.
        target_digit_set: An optional string representing the target digit set.
            If provided, takes precedence over `target_digit_set_id`.
        target_digit_set_id: An optional ID of a predefined target digit set.
    """

    input_text: Optional[str] = ""
    source_digit_set: Optional[str] = None
    source_digit_set_id: Optional[str] = None
    target_digit_set: Optional[str] = None
    target_digit_set_id: Optional[str] = None


class ErrorResponse(BaseModel):
    """
    Pydantic model for standard API error responses.

    Attributes:
        message: A concise summary of the error.
        detail: An optional, more detailed explanation of the error.
    """

    message: str
    detail: Optional[str] = None


class RebaseResponse(BaseModel):
    """
    Pydantic model for the response of a rebase operation.

    Attributes:
        rebased_text: The string after the rebase operation.
        source_digit_set_used: A string indicating the source digit set that was used
            (e.g., "Binary", "Provided: '012'").
        target_digit_set_used: A string indicating the target digit set that was used
            (e.g., "Decimal", "Provided: 'abc'").
        error: An optional `ErrorResponse` object if an error occurred during rebase.
    """

    rebased_text: str
    source_digit_set_used: str
    target_digit_set_used: str
    error: Optional[ErrorResponse] = None


@APP.post(
    "/rebase",
    response_model=RebaseResponse,
    summary="Rebase text between digit sets",
)
async def rebase_text(request: RebaseRequest) -> RebaseResponse:
    """
    Rebasees input text from a source digit set to a target digit set.

    - If `input_text` is not provided, an empty string is used.
    - If `source_digit_set_id` is not provided, the source digit set is
      dynamically derived from `input_text`.
    - If `target_digit_set_id` is not provided, the input string is returned
      with digits not in the derived/provided source digit set removed. If the
      target digit set has a length of 1, an empty string will be returned.
    """
    digit_sets_data = _load_digit_set_data()

    input_text: str = (
        request.input_text if request.input_text is not None else ""
    )
    source_digit_set_obj: Optional[DigitSet] = None
    target_digit_set_obj: Optional[DigitSet] = None
    source_digit_set_name: str = "Dynamically Derived"
    target_digit_set_name: str = "Echo Input"

    # Determine source digit set
    if request.source_digit_set:  # Direct digit set string takes precedence
        source_digit_set_obj = DigitSet(
            name="Provided", digits=request.source_digit_set, source="api_input"
        )
        source_digit_set_name = f"Provided: '{request.source_digit_set}'"
    elif request.source_digit_set_id:
        source_digit_set_obj = digit_sets_data.get(request.source_digit_set_id)
        if source_digit_set_obj is None:
            raise HTTPException(
                status_code=400,
                detail=ErrorResponse(
                    message="Invalid Source Digit Set ID",
                    detail=(
                        "Source digit set with ID "
                        f"'{request.source_digit_set_id}' "
                        "not found."
                    ),
                ).model_dump(),
            ) from None
        source_digit_set_name = source_digit_set_obj.name

    # Determine target digit set
    if request.target_digit_set:  # Direct digit set string takes precedence
        target_digit_set_obj = DigitSet(
            name="Provided", digits=request.target_digit_set, source="api_input"
        )
        target_digit_set_name = f"Provided: '{request.target_digit_set}'"
    elif request.target_digit_set_id:
        target_digit_set_obj = digit_sets_data.get(request.target_digit_set_id)
        if target_digit_set_obj is None:
            raise HTTPException(
                status_code=400,
                detail=ErrorResponse(
                    message="Invalid Target Digit Set ID",
                    detail=(
                        "Target digit set with ID "
                        f"'{request.target_digit_set_id}' "
                        "not found."
                    ),
                ).model_dump(),
            ) from None
        target_digit_set_name = target_digit_set_obj.name

    rebased_text: str = ""
    error_response: Optional[ErrorResponse] = None

    try:
        rebaser = DigitSetRebaser(
            out_digit_set=target_digit_set_obj,
            in_digit_set=source_digit_set_obj,
        )
        rebased_text = rebaser.rebase(input_text)
    except ValueError as exc:
        error_response = ErrorResponse(
            message="Rebase Error",
            detail=f"A value error occurred during rebase: {exc}",
        )
        raise HTTPException(
            status_code=400, detail=error_response.model_dump()
        ) from exc
    except IndexError as exc:
        error_response = ErrorResponse(
            message="Rebase Error",
            detail=f"An index error occurred during rebase: {exc}",
        )
        raise HTTPException(
            status_code=400, detail=error_response.model_dump()
        ) from exc
    except Exception as exc:  # pylint: disable=broad-exception-caught
        # Catching broad exception as an isolation point for unexpected errors.
        error_response = ErrorResponse(
            message="Internal Server Error",
            detail=f"An unexpected error occurred: {exc}",
        )
        raise HTTPException(
            status_code=500, detail=error_response.model_dump()
        ) from exc

    return RebaseResponse(
        rebased_text=rebased_text,
        source_digit_set_used=source_digit_set_name,
        target_digit_set_used=target_digit_set_name,
        error=error_response,
    )


def start_api() -> None:
    """
    Starts the FastAPI server using uvicorn.
    """
    uvicorn.run(
        "basebender.api.main:APP", host="0.0.0.0", port=8000, reload=True
    )
