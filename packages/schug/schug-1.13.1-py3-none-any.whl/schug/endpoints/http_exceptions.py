from typing import Any, Optional

from fastapi import HTTPException, status


class SchugHttpException(Exception):
    @staticmethod
    def error_404(result: Any, query: Any) -> Optional[HTTPException]:
        """Handle exception http 404 error not found"""
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"{query} not found"
            )
        return None
