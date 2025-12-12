from pydantic import BaseModel, Field
import openai
import json
from typing import Literal

class QatarIDInfo(BaseModel):
    """
    Extract info from ocr-extracted text from a Qatar ID
    """
    name: str = Field(..., description="Full name in English")
    name_ar: str = Field(..., description="Full name in Arabic")
    nationality: str = Field(...,
                             description="Nationality in ISO 3166-1 alpha-3 format (e.g., 'PAK' 'QAT', 'SYR', 'PHL')",
                             example="SYR")
    id_number: str = Field(..., description="National ID number")
    dob: str = Field(..., description="Date of birth")
    expiry_date: str = Field(..., description="Card expiry date")
    occupation: str = Field(..., description="Occupation in Arabic")
    occupation_en: str = Field(..., description="Occupation, translated from Arabic to English")
    is_header_verified: Literal["True", "False",""] = Field(..., description="Return True if it is a valid Qatar ID front side, else False")


def extract_qat_front_id(base64_image: str):
    """
    Extracts QAT ID front fields using OpenAI's vision model and function calling.
    Args:
        openai_api_key (str): OpenAI API key.
        base64_image (str): Base64-encoded image of the UAE ID front.
    Returns:
        QATIDExtractionResult: Extracted fields in Pydantic model.
    Raises:
        Exception: If extraction or parsing fails.
    """

    # Define the function schema for OpenAI function calling
    function_schema = {
        "name": "extract_qatar_id_info",
        "description": "Extract info from OCR-extracted text from a Qatar ID",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Full name in English"
                },
                "name_ar": {
                    "type": "string",
                    "description": "Full name in Arabic"
                },
                "nationality": {
                    "type": "string",
                    "description": "Nationality in ISO 3166-1 alpha-3 format (e.g., 'PAK', 'QAT', 'SYR', 'PHL')",
                    "example": "SYR"
                },
                "id_number": {
                    "type": "string",
                    "description": "National ID number"
                },
                "dob": {
                    "type": "string",
                    "description": "Date of birth"
                },
                "expiry_date": {
                    "type": "string",
                    "description": "Card expiry date"
                },
                "occupation": {
                    "type": "string",
                    "description": "Occupation in Arabic"
                },
                "occupation_en": {
                    "type": "string",
                    "description": "Occupation, translated from Arabic to English"
                },
                "is_header_verified": {
                    "type": "string",
                    "description": "Return True if it is a valid Qatar ID front side, else False"
                }
            },
            "required": ["name", "name_ar", "nationality", "id_number", "dob", "expiry_date", "occupation",
                         "occupation_en","is_header_verified"]
        }
    }

    prompt = (
        "You are an expert at extracting information from QAT ID cards. "
        "Given an image of the front side of a QAT ID, extract the relevant fields. "
        "If the id_number is not found, set it to an empty string. "
        "Set is_header_verified to True if the image is the front side of a QAT ID, else False."
        "The front side of a QAT NID ID No., D.O.B, Nationality and Date of Expiry."
        "If the picture of the person is not there, return is_header_verified as false."
        "If the QAT NID contains MRZ lines then return is_header_verified as false."
        "Set is_uae_id to true if the exact phrase 'STATE OF QATAR' appears anywhere in the readable text on the card (case-insensitive); otherwise set it to false."
        "Return empty string where information is not found."
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                },
            ],
            functions=[function_schema],
            function_call={"name": "extract_qatar_id_info"},
            max_tokens=300,
        )
        message = response.choices[0].message
        if message.function_call and message.function_call.arguments:
            args = json.loads(message.function_call.arguments)
            results = QatarIDInfo(**args)
            results_dict = {}
            results_dict["name"] = results.name
            results_dict["name_ar"] = results.name_ar
            results_dict["occupation"] = results.occupation
            results_dict["occupation_en"] = results.occupation_en
            results_dict["nationality"] = results.nationality
            results_dict["dob"] = results.dob
            results_dict["expiry_date"] = results.expiry_date
            results_dict["id_number"] = results.id_number
            results_dict["is_header_verified"] = results.is_header_verified

            if results.is_header_verified != "True":
                return "not_front_id"
            return results_dict
        else:
            return "covered_photo"
    except Exception as e:
        return "covered_photo"

import base64
from io import BytesIO
from PIL import Image

import base64
from io import BytesIO
from PIL import Image


def compress_base64_image(b64_string, quality=50, size_threshold_mb=2):
    # Convert threshold to bytes
    threshold_bytes = size_threshold_mb * 1024 * 1024

    # Decode base64 → image data
    image_data = base64.b64decode(b64_string)

    # If image size is below threshold, return original
    if len(image_data) <= threshold_bytes:
        return b64_string

    # Otherwise compress
    image = Image.open(BytesIO(image_data))

    buffer = BytesIO()
    image.save(buffer, format="JPEG", quality=quality)

    compressed_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return compressed_b64



