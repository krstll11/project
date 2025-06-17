from pydantic import BaseModel

class FavoriteCreate(BaseModel):
    ad_id: int