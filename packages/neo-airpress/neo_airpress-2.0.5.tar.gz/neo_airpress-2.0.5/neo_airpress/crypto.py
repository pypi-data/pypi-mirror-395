# SPDX-License-Identifier: MIT
from cryptography import x509
from cryptography.hazmat.bindings.openssl.binding import Binding
from cryptography.hazmat.primitives import hashes, serialization
from .pkcs7 import PKCS7SignatureBuilder, PKCS7Options

copenssl = Binding.lib
cffi = Binding.ffi


def pkcs7_sign(
    certcontent,
    keycontent,
    wwdr_certificate,
    data,
    key_password=None,
):
    """
    Creates a PKCS#7 detached signature for the given data using provided certificates and private key.

    Args:
        certcontent (bytes): The signer's certificate in PEM format.
        keycontent (bytes): The signer's private key in PEM format.
        wwdr_certificate (bytes): Apple's Worldwide Developer Relations (WWDR) certificate in DER format.
        data (bytes): The data to be signed.
        key_password (bytes, optional): Password for the private key if it's encrypted. Defaults to None.

    Returns:
        bytes: The PKCS#7 signature in DER format.

    The function performs the following steps:
    1. Loads the signer's certificate from PEM format
    2. Loads the private key (with optional password)
    3. Loads the WWDR certificate from DER format
    4. Creates a detached PKCS#7 signature using SHA256 as the hash algorithm

    Example:
        signature = pkcs7_sign(
            cert_data,
            key_data,
            wwdr_cert_data,
            content_to_sign,
            key_password=b'optional_password'
        )
    """

    cert = x509.load_pem_x509_certificate(certcontent)
    priv_key = serialization.load_pem_private_key(keycontent, password=key_password)
    wwdr_cert = x509.load_pem_x509_certificate(wwdr_certificate)

    options = [PKCS7Options.DetachedSignature]
    return (
        PKCS7SignatureBuilder()
        .set_data(data)
        .add_signer(cert, priv_key, hashes.SHA1())
        .add_certificate(wwdr_cert)
        .sign(serialization.Encoding.DER, options)
    )
