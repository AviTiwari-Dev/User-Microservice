"""
Defines the API router for user-related endpoints.
"""

from fastapi import APIRouter

router = APIRouter(
    prefix="/user",
    deprecated=False,
    include_in_schema=True,
    tags=["User"],
)
