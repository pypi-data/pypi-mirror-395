from datetime import datetime
from typing import List
from pydantic import Field, field_validator, EmailStr
from sifenpy.models.base import SifenBaseModel
from sifenpy.models.enums import (
    TipoEmision, TipoDocumento, TipoContribuyente,
    CondicionOperacion, AfectacionIVA
)

# =============================================================================
# GRUPO B: Operación
# =============================================================================
class GrupoOperacion(SifenBaseModel):
    """Datos operativos de la emisión (gOpeDE)"""
    tipo_emision: TipoEmision = Field(..., serialization_alias="iTipEmi")
    descripcion: str = Field(..., serialization_alias="dDesTipEmi", min_length=6, max_length=12)
    codigo_seguridad: str = Field(..., serialization_alias="dCodSeg", min_length=9, max_length=9, pattern=r"^\d+$")
    # FIX: Usar default=None explícito
    info_adicional_emisor: str | None = Field(default=None, serialization_alias="dInfoEmi", max_length=3000)
    info_adicional_fisco: str | None = Field(default=None, serialization_alias="dInfoFisc", max_length=3000)

    @field_validator("codigo_seguridad")
    def validar_seguridad(cls, v):
        if v == "000000000": raise ValueError("El código de seguridad debe ser aleatorio")
        return v

# =============================================================================
# GRUPO C: Timbrado
# =============================================================================
class GrupoTimbrado(SifenBaseModel):
    """Datos de autorización de la SET (gTimb)"""
    tipo_documento: TipoDocumento = Field(..., serialization_alias="iTiDE")
    descripcion: str = Field(..., serialization_alias="dDesTiDE", max_length=60)
    numero_timbrado: int = Field(..., serialization_alias="dNumTim")
    establecimiento: str = Field(..., serialization_alias="dEst", pattern=r"^\d{3}$")
    punto_expedicion: str = Field(..., serialization_alias="dPunExp", pattern=r"^\d{3}$")
    numero_documento: str = Field(..., serialization_alias="dNumDoc", pattern=r"^\d{7}$")
    serie: str | None = Field(default=None, serialization_alias="dSerieNum", min_length=2, max_length=2)
    fecha_inicio_vigencia: str = Field(..., serialization_alias="dFeIniT", pattern=r"^\d{4}-\d{2}-\d{2}$")

    @field_validator("numero_timbrado")
    def validar_largo_timbrado(cls, v):
        if len(str(v)) != 8:
            raise ValueError("El número de timbrado debe tener 8 dígitos")
        return v

# =============================================================================
# GRUPO D: Emisor y Receptor
# =============================================================================
class GrupoEmisor(SifenBaseModel):
    """Datos de quien emite la factura (gEmis)"""
    ruc: str = Field(..., serialization_alias="dRucEm", min_length=3, max_length=8)
    digito_verificador: int = Field(..., serialization_alias="dDVEmi", ge=0, le=9)
    tipo_contribuyente: TipoContribuyente = Field(..., serialization_alias="iTipCont")
    tipo_regimen: int | None = Field(default=None, serialization_alias="cTipReg")
    razon_social: str = Field(..., serialization_alias="dNomEmi", max_length=255)
    nombre_fantasia: str | None = Field(default=None, serialization_alias="dNomFanEmi", max_length=255)
    direccion: str = Field(..., serialization_alias="dDirEmi", max_length=255)
    numero_casa: int = Field(..., serialization_alias="dNumCas")
    departamento_id: int = Field(..., serialization_alias="cDepEmi")
    departamento_desc: str = Field(..., serialization_alias="dDesDepEmi")
    distrito_id: int | None = Field(default=None, serialization_alias="cDisEmi")
    distrito_desc: str | None = Field(default=None, serialization_alias="dDesDisEmi")
    ciudad_id: int = Field(..., serialization_alias="cCiuEmi")
    ciudad_desc: str = Field(..., serialization_alias="dDesCiuEmi")
    telefono: str = Field(..., serialization_alias="dTelEmi", min_length=6, max_length=15)
    email: EmailStr = Field(..., serialization_alias="dEmailE")
    denominacion_sucursal: str | None = Field(default=None, serialization_alias="dDenSuc")

class GrupoReceptor(SifenBaseModel):
    """Datos del cliente (gDatRec)"""
    naturaleza: int = Field(..., serialization_alias="iNatRec", description="1=Contribuyente, 2=No")
    tipo_operacion: int = Field(..., serialization_alias="iTiOpe", description="1=B2B, 2=B2C, 3=B2G, 4=B2F")
    pais_codigo: str = Field(..., serialization_alias="cPaisRec", min_length=3, max_length=3)
    pais_desc: str = Field(..., serialization_alias="dDesPaisRe")
    tipo_contribuyente_receptor: int | None = Field(default=None, serialization_alias="iTiContRec")
    ruc: str | None = Field(default=None, serialization_alias="dRucRec")
    digito_verificador: int | None = Field(default=None, serialization_alias="dDVRec")
    razon_social: str = Field(..., serialization_alias="dNomRec", max_length=255)

    direccion: str | None = Field(default=None, serialization_alias="dDirRec", max_length=255)
    numero_casa: int | None = Field(default=None, serialization_alias="dNumCasRec")
    departamento_id: int | None = Field(default=None, serialization_alias="cDepRec")
    departamento_desc: str | None = Field(default=None, serialization_alias="dDesDepRec")
    distrito_id: int | None = Field(default=None, serialization_alias="cDisRec")
    distrito_desc: str | None = Field(default=None, serialization_alias="dDesDisRec")
    ciudad_id: int | None = Field(default=None, serialization_alias="cCiuRec")
    ciudad_desc: str | None = Field(default=None, serialization_alias="dDesCiuRec")
    telefono: str | None = Field(default=None, serialization_alias="dTelRec")
    email: str | None = Field(default=None, serialization_alias="dEmailRec")
    codigo_cliente: str | None = Field(default=None, serialization_alias="dCodCliente")

class GrupoDatosGenerales(SifenBaseModel):
    """Contenedor de Emisor y Receptor (gDatGralOpe)"""
    fecha_emision: datetime = Field(..., serialization_alias="dFeEmiDE")
    emisor: GrupoEmisor = Field(..., serialization_alias="gEmis")
    receptor: GrupoReceptor = Field(..., serialization_alias="gDatRec")

# =============================================================================
# GRUPO E: Detalles e Ítems
# =============================================================================
class GrupoFacturaElectronica(SifenBaseModel):
    """Datos específicos de FE (gCamFE)"""
    ind_presencia: int = Field(..., serialization_alias="iIndPres", description="1=Presencial, etc")
    descripcion: str = Field(..., serialization_alias="dDesIndPres")

class GrupoCondicion(SifenBaseModel):
    """Condición de venta (gCamCond)"""
    tipo: CondicionOperacion = Field(..., serialization_alias="iCondOpe")
    descripcion: str = Field(..., serialization_alias="dDCondOpe")

class CamposDescuentosItem(SifenBaseModel):
    """
    Grupo E8.1.1: Descuentos y anticipos por ítem.
    Manual Técnico: gValorRestaItem
    """
    descuento_item: float = Field(default=0, serialization_alias="dDescItem")
    porcentaje_descuento: float = Field(default=0, serialization_alias="dPorcDesIt")
    descuento_global_item: float = Field(default=0, serialization_alias="dDescGloItem")
    anticipo_pre_uni: float | None = Field(default=0, serialization_alias="dAntPreUniIt")
    anticipo_global_pre_uni: float | None = Field(default=0, serialization_alias="dAntGloPreUniIt")
    total_operacion_item: float = Field(..., serialization_alias="dTotOpeItem")
    total_operacion_gs: float | None = Field(default=None, serialization_alias="dTotOpeGs")

class ValoresItem(SifenBaseModel):
    """Precios (gValorItem)"""
    precio_unitario: float = Field(..., serialization_alias="dPUniProSer")
    total_bruto: float = Field(..., serialization_alias="dTotBruOpeItem")
    valor_resta: CamposDescuentosItem | None = Field(default=None, serialization_alias="gValorRestaItem")

class IvaItem(SifenBaseModel):
    """Impuestos del ítem (gCamIVA)"""
    afectacion: AfectacionIVA = Field(..., serialization_alias="iAfecIVA")
    descripcion: str = Field(..., serialization_alias="dDesAfecIVA")
    proporcion: int = Field(..., serialization_alias="dPropIVA")
    tasa: int = Field(..., serialization_alias="dTasaIVA")
    base_gravada: float = Field(..., serialization_alias="dBasGravIVA")
    liquidacion: float = Field(..., serialization_alias="dLiqIVAItem")

class Item(SifenBaseModel):
    """Un producto o servicio (gCamItem)"""
    codigo: str = Field(..., serialization_alias="dCodInt", max_length=20)
    descripcion: str = Field(..., serialization_alias="dDesProSer", max_length=120)
    unidad_medida: int = Field(..., serialization_alias="cUniMed")
    unidad_desc: str = Field(..., serialization_alias="dDesUniMed")
    cantidad: float = Field(..., serialization_alias="dCantProSer")
    info_item: str | None = Field(default=None, serialization_alias="dInfItem")
    valores: ValoresItem = Field(..., serialization_alias="gValorItem")
    iva: IvaItem = Field(..., serialization_alias="gCamIVA")

class GrupoDetalle(SifenBaseModel):
    """Lista de ítems (gDtipDE)"""
    datos_fe: GrupoFacturaElectronica | None = Field(default=None, serialization_alias="gCamFE")
    condicion: GrupoCondicion | None = Field(default=None, serialization_alias="gCamCond")
    items: List[Item] = Field(..., serialization_alias="gCamItem")

# =============================================================================
# GRUPO F: Totales
# =============================================================================
class GrupoTotales(SifenBaseModel):
    """Resumen financiero (gTotSub)"""
    # Subtotales
    subtotal_exenta: float = Field(..., serialization_alias="dSubExe")
    subtotal_5: float = Field(..., serialization_alias="dSub5")
    subtotal_10: float = Field(..., serialization_alias="dSub10")
    # Totales
    total_operacion: float = Field(..., serialization_alias="dTotOpe")
    total_general: float = Field(..., serialization_alias="dTotGralOpe")
    # Liquidación IVA
    iva_5: float = Field(..., serialization_alias="dIVA5")
    iva_10: float = Field(..., serialization_alias="dIVA10")
    total_iva: float = Field(..., serialization_alias="dTotIVA")
    # Bases
    base_5: float = Field(..., serialization_alias="dBaseGrav5")
    base_10: float = Field(..., serialization_alias="dBaseGrav10")
    total_base: float = Field(..., serialization_alias="dTBasGraIVA")

    # Campos obligatorios técnicos (con default 0)
    subtotal_exo: float = Field(default=0, serialization_alias="dSubExo")
    total_desc: float = Field(default=0, serialization_alias="dTotDesc")
    total_desc_gl: float = Field(default=0, serialization_alias="dTotDescGlotem")
    total_ant_item: float = Field(default=0, serialization_alias="dTotAntItem")
    total_ant: float = Field(default=0, serialization_alias="dTotAnt")
    porc_desc_total: float = Field(default=0, serialization_alias="dPorcDescTotal")
    desc_total: float = Field(default=0, serialization_alias="dDescTotal")
    anticipo: float = Field(default=0, serialization_alias="dAnticipo")
    redondeo: float = Field(default=0, serialization_alias="dRedon")

    total_guaranies: float | None = Field(default=None, serialization_alias="dTotalGs")

# =============================================================================
# DOCUMENTO ELECTRÓNICO (RAÍZ)
# =============================================================================
class DE(SifenBaseModel):
    """Estructura completa de la Factura (A001)"""
    id_cdc: str = Field(..., serialization_alias="Id")
    digito_verificador: int = Field(..., serialization_alias="dDVId")
    fecha_firma: datetime = Field(..., serialization_alias="dFecFirma")
    sistema_facturacion: int = Field(default=1, serialization_alias="dSisFact")

    operacion: GrupoOperacion = Field(..., serialization_alias="gOpeDE")
    timbrado: GrupoTimbrado = Field(..., serialization_alias="gTimb")
    general: GrupoDatosGenerales = Field(..., serialization_alias="gDatGralOpe")
    detalle: GrupoDetalle = Field(..., serialization_alias="gDtipDE")
    totales: GrupoTotales = Field(..., serialization_alias="gTotSub")

    @field_validator("id_cdc")
    def validar_cdc(cls, v):
        if len(v) != 44: raise ValueError("CDC debe tener 44 caracteres")
        return v

class RootDE(SifenBaseModel):
    """Contenedor XML (rDE)"""
    version: int = Field(default=150, serialization_alias="dVerFor")
    de: DE = Field(..., serialization_alias="DE")

    @field_validator("version")
    def validar_version(cls, v):
        if v != 150: raise ValueError("La versión del formato debe ser 150")
        return v
