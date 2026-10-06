from pydantic import BaseModel, Field


class Response(BaseModel):
    '''    Ответ на запросы UI    '''
    status_code: int = Field(
        ...,
        ge=100,
        le=599,
        description="Код результата в стиле HTTP",
    )
    message: str = Field(
        default="",
        max_length=4096,
        description="Сообщение для пользователя",
    )
    exception: str | None = Field(
        default=None,
        max_length=8192,
        description="Текст ошибки для отладки",
    )
