# from pydantic import BaseModel, Field, field_validator
# from pydantic_core import PydanticCustomError
#
#
# class Pagination(BaseModel):
#     offset: int = Field(0, alias="offset")
#     limit: int = Field(1, alias="limit")
#
#     @field_validator("offset")
#     @staticmethod
#     def validate_offset(val: int) -> int:
#         if val < 0:
#             raise PydanticCustomError("Validation error", "Offset must be > 0")
#         return val
#
#     @field_validator("limit")
#     @staticmethod
#     def validate_offset(val: int) -> int:
#         if val < 1:
#             raise PydanticCustomError("Validation error", "Limit must be > 1")
#         return val
