from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

class SifenBaseModel(BaseModel):
    """
    Modelo base para todas las estructuras de SIFEN.
    Configura la conversión automática de snake_case a camelCase/PascalCase
    según lo requiere el esquema XSD.
    """
    model_config = ConfigDict(
        populate_by_name=True,
        # SIFEN usa nombres como dFeEmiDE, que no son camelCase estándar.
        # Usaremos 'alias' explícitos en los campos para mapear exactamente.
        # Esta config permite usar tanto el nombre python como el alias.
        arbitrary_types_allowed=True,
        extra="forbid"  # Rechazar campos extra que no estén en el manual
    )