from enum import IntEnum

class TipoEmision(IntEnum):
    """ Códigos para iTipEmi"""
    NORMAL = 1
    CONTINGENCIA = 2

class TipoDocumento(IntEnum):
    """ Códigos para iTiDE"""
    FACTURA_ELECTRONICA = 1
    FACTURA_EXPORTACION = 2
    FACTURA_IMPORTACION = 3
    AUTOFACTURA = 4
    NOTA_CREDITO = 5
    NOTA_DEBITO = 6
    NOTA_REMISION = 7
    COMPROBANTE_RETENCION = 8

class TipoContribuyente(IntEnum):
    """ Códigos para iTipCont"""
    PERSONA_FISICA = 1
    PERSONA_JURIDICA = 2

class CondicionOperacion(IntEnum):
    """ Códigos para iCondOpe"""
    CONTADO = 1
    CREDITO = 2

class AfectacionIVA(IntEnum):
    """ Códigos para iAfecIVA"""
    GRAVADO = 1
    EXONERADO = 2
    EXENTO = 3
    GRAVADO_PARCIAL = 4