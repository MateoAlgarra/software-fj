"""Clase Cliente con datos personales encapsulados y validados."""

import re

from entidades import EntidadBase
from excepciones import ClienteInvalidoError, ParametroFaltanteError

_PATRON_NOMBRE = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' ]{3,60}$")
_PATRON_EMAIL = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")


class Cliente(EntidadBase):
    """Cliente de Software FJ.

    Los atributos son privados; solo se cambian por las propiedades,
    que validan cada dato antes de guardarlo (encapsulación).
    """

    def __init__(self, nombre=None, documento=None, email=None, telefono=None):
        faltantes = [
            campo
            for campo, valor in (
                ("nombre", nombre),
                ("documento", documento),
                ("email", email),
                ("telefono", telefono),
            )
            if valor is None or str(valor).strip() == ""
        ]
        if faltantes:
            raise ParametroFaltanteError(
                f"Faltan datos obligatorios del cliente: {', '.join(faltantes)}"
            )
        self.nombre = nombre
        self.documento = documento
        self.email = email
        self.telefono = telefono
        super().__init__()  # el id se asigna solo si todos los datos son válidos

    # ---- nombre ----
    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or not _PATRON_NOMBRE.match(valor.strip()):
            raise ClienteInvalidoError(
                f"Nombre inválido: {valor!r} (solo letras, entre 3 y 60 caracteres)"
            )
        self._nombre = valor.strip().title()

    # ---- documento ----
    @property
    def documento(self) -> str:
        return self._documento

    @documento.setter
    def documento(self, valor):
        texto = str(valor).strip()
        if not texto.isdigit() or not 6 <= len(texto) <= 12:
            raise ClienteInvalidoError(
                f"Documento inválido: {valor!r} (solo números, de 6 a 12 dígitos)"
            )
        self._documento = texto

    # ---- email ----
    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, valor):
        if not isinstance(valor, str) or not _PATRON_EMAIL.match(valor.strip()):
            raise ClienteInvalidoError(f"Correo inválido: {valor!r}")
        self._email = valor.strip().lower()

    # ---- teléfono ----
    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        texto = str(valor).strip()
        if not texto.isdigit() or len(texto) != 10:
            raise ClienteInvalidoError(
                f"Teléfono inválido: {valor!r} (deben ser 10 dígitos)"
            )
        self._telefono = texto

    def describir(self) -> str:
        return f"Cliente #{self.id}: {self.nombre} (CC {self.documento}, {self.email})"
