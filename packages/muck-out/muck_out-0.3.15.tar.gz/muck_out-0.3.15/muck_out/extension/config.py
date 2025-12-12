from pydantic import BaseModel, Field


class MuckOutConfiguration(BaseModel):
    """Configures muck_out"""

    drop_context: bool = Field(
        default=True, description="If set to true sets the `@context` property to None"
    )
