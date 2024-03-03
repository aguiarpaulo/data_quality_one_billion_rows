import pandera as pa
from pandera.typing import DataFrame, Series

email_regex = r"[^@]+@[^@]+\.[^@]+"

class  ProductSchema(pa.SchemaModel):
    id_product: Series[int]
    name: Series[str]
    quantity: Series[int] = pa.Field(ge=20, le=200)
    price: Series[float] = pa.Field(ge=05.0, le=120.0)
    category: Series[str]
    email: Series[str] = pa.Field(regex=email_regex)

    class Config:
        coerce = True
        strict = True

class ProductSchemaKPI(ProductSchema):
    total_stock_value: Series[float] = pa.Field(ge=0)
    category_normalized: Series[str]
    avalability: Series[bool]