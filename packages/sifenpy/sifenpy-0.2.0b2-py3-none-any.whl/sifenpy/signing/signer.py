import base64
import hashlib
from pathlib import Path
from lxml import etree
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.x509 import Certificate
from typing import Optional

# Namespaces requeridos por el estándar XML-DSig
NS_DSIG = "http://www.w3.org/2000/09/xmldsig#"
NS_MAP = {"ds": NS_DSIG}

class SifenSigner:
    """
    Gestiona la carga de certificados digitales y la firma de documentos XML.
    Implementa el estándar XML-DSig Enveloped según requisitos de SIFEN.
    """

    def __init__(self, archivo_p12: str | Path, password: str):
        self.archivo_p12 = Path(archivo_p12)
        self.password = password
        self._private_key: Optional[rsa.RSAPrivateKey] = None
        self._certificate: Optional[Certificate] = None
        self._load_certificate()

    def _load_certificate(self) -> None:
        if not self.archivo_p12.exists():
            raise FileNotFoundError(f"No se encontró el archivo: {self.archivo_p12}")

        try:
            with open(self.archivo_p12, "rb") as f:
                p12_data = f.read()

            private_key, certificate, _ = pkcs12.load_key_and_certificates(
                p12_data,
                self.password.encode("utf-8")
            )

            if not isinstance(private_key, rsa.RSAPrivateKey):
                raise ValueError("El certificado no contiene una clave privada RSA válida")

            self._private_key = private_key
            self._certificate = certificate

        except ValueError as e:
            if "Bad decrypt" in str(e) or "mac" in str(e).lower():
                raise ValueError("Contraseña del certificado incorrecta")
            raise e

    @property
    def certificate(self) -> Certificate:
        if self._certificate is None:
            raise RuntimeError("Certificado no cargado")
        return self._certificate

    # --- AGREGADO: Propiedad que faltaba para el test ---
    @property
    def private_key(self) -> rsa.RSAPrivateKey:
        if self._private_key is None:
            raise RuntimeError("Certificado no cargado")
        return self._private_key

    def get_certificate_b64(self) -> str:
        """Obtiene el certificado en Base64 limpio para el XML."""
        cert_pem = self.certificate.public_bytes(serialization.Encoding.PEM)
        lines = cert_pem.decode("ascii").splitlines()
        return "".join([line for line in lines if "-----" not in line])

    def firmar_xml(self, xml_content: str, id_cdc: str) -> str:
        """
        Firma un XML string usando XML-DSig Enveloped.

        Args:
            xml_content: El XML completo generado por los modelos (string).
            id_cdc: El CDC del documento (sin el prefijo '#').

        Returns:
            str: El XML final firmado.
        """
        # 1. Parsear el XML
        parser = etree.XMLParser(remove_blank_text=True)
        root = etree.fromstring(xml_content.encode("utf-8"), parser=parser)

        # 2. Buscar el nodo a firmar (<DE Id="...">)
        nodo_a_firmar = root.xpath(f"//*[@Id='{id_cdc}']")
        if not nodo_a_firmar:
            raise ValueError(f"No se encontró el nodo con Id='{id_cdc}' para firmar")

        element_to_sign = nodo_a_firmar[0]  # pyright: ignore[reportIndexIssue]

        # 3. Canonización (C14N) para el Hash
        canonical_xml = etree.tostring(element_to_sign, method="c14n", exclusive=False, with_comments=False)  # pyright: ignore[reportCallIssue, reportArgumentType]

        # 4. Calcular Digest (Hash SHA-256)
        digest = hashlib.sha256(canonical_xml).digest()
        digest_b64 = base64.b64encode(digest).decode("ascii")

        # 5. Construir la estructura <SignedInfo>
        signed_info = etree.Element(f"{{{NS_DSIG}}}SignedInfo", nsmap=NS_MAP)

        etree.SubElement(signed_info, f"{{{NS_DSIG}}}CanonicalizationMethod",
                         Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315")

        etree.SubElement(signed_info, f"{{{NS_DSIG}}}SignatureMethod",
                         Algorithm="http://www.w3.org/2001/04/xmldsig-more#rsa-sha256")

        reference = etree.SubElement(signed_info, f"{{{NS_DSIG}}}Reference", URI=f"#{id_cdc}")

        transforms = etree.SubElement(reference, f"{{{NS_DSIG}}}Transforms")
        etree.SubElement(transforms, f"{{{NS_DSIG}}}Transform",
                         Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature")
        etree.SubElement(transforms, f"{{{NS_DSIG}}}Transform",
                         Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#")

        etree.SubElement(reference, f"{{{NS_DSIG}}}DigestMethod",
                         Algorithm="http://www.w3.org/2001/04/xmlenc#sha256")
        digest_value_node = etree.SubElement(reference, f"{{{NS_DSIG}}}DigestValue")
        digest_value_node.text = digest_b64

        # 6. Calcular la Firma (SignatureValue)
        signed_info_c14n = etree.tostring(signed_info, method="c14n", exclusive=False, with_comments=False)

        private_key = self._private_key
        if private_key is None:
            raise RuntimeError("Certificado no cargado")

        signature = private_key.sign(
            signed_info_c14n,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        signature_b64 = base64.b64encode(signature).decode("ascii")

        # 7. Construir el bloque <Signature> final
        signature_node = etree.Element(f"{{{NS_DSIG}}}Signature", nsmap=NS_MAP)
        signature_node.append(signed_info)

        signature_value_node = etree.SubElement(signature_node, f"{{{NS_DSIG}}}SignatureValue")
        signature_value_node.text = signature_b64

        key_info = etree.SubElement(signature_node, f"{{{NS_DSIG}}}KeyInfo")
        x509_data = etree.SubElement(key_info, f"{{{NS_DSIG}}}X509Data")
        x509_certificate = etree.SubElement(x509_data, f"{{{NS_DSIG}}}X509Certificate")
        x509_certificate.text = self.get_certificate_b64()

        # 8. Insertar la firma
        if root.tag.endswith("rDE"):
             root.append(signature_node)
        else:
             root.append(signature_node)

        # 9. Retornar XML final
        return etree.tostring(root, encoding="UTF-8", xml_declaration=True).decode("utf-8")
