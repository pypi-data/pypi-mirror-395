import asyncio
import httpx
import logging
from abc import ABC, abstractmethod
from typing import Any, Optional


class BaseHTTPService(ABC):
    """
    Classe base assíncrona para consumo de APIs HTTP usando `httpx.AsyncClient`.

    Esta classe oferece uma camada reutilizável e resiliente para serviços HTTP,
    com suporte a:

    - Tentativas automáticas (retries) em falhas de rede ou erros 5xx.
    - Backoff exponencial entre tentativas.
    - Gerenciamento de conexões HTTP via context manager.
    - Log estruturado e injetável.
    - Retorno padronizado com status, sucesso, erro e corpo da resposta.

    Subclasses devem implementar o método :meth:`_prepare_headers` para
    definir cabeçalhos personalizados (por exemplo, tokens de autenticação).

    Exemplo de herança e uso:
        >>> class APIService(BaseHTTPService):
        ...     async def _prepare_headers(self) -> dict[str, str]:
        ...         return {"Authorization": "Bearer <TOKEN>"}
        ...
        ... async def main():
        ...     async with APIService("https://api.address.com") as svc:
        ...         resp = await svc.request("GET", "/users/octocat")
        ...         print(resp)
        ...
        >>> asyncio.run(main())

    Atributos:
        CLIENT_ERRORS (dict[int, str]): Mapeamento de códigos HTTP 4xx para descrições.
        RETRYABLE_STATUS (set[int]): Códigos HTTP considerados recuperáveis (para retry).

    """

    CLIENT_ERRORS = {
        400: "bad_request",
        401: "unauthorized",
        403: "access_denied",
        404: "not_found",
    }
    RETRYABLE_STATUS = {500, 502, 503, 504}

    def __init__(
        self,
        base_url: str,
        max_retries: int = 3,
        timeout: float = 10.0,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Inicializa a instância base do serviço HTTP.

        Args:
            base_url (str): URL base da API (ex: "https://api.example.com").
            max_retries (int, opcional): Número máximo de tentativas em caso de falha. Padrão: 3.
            timeout (float, opcional): Tempo máximo (segundos) para timeout de requisição. Padrão: 10.0.
            logger (logging.Logger, opcional): Logger customizado. Se não for fornecido, um logger interno é criado.
        """
        self.base_url = base_url.rstrip("/")
        self.max_retries = max_retries
        self.timeout = timeout
        self.logger = logger or logging.getLogger(self.__class__.__name__)
        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self):
        """
        Entra no contexto assíncrono, inicializando o cliente HTTP.

        Returns:
            BaseHTTPService: A própria instância, pronta para uso.
        """
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=httpx.Timeout(self.timeout),
        )
        return self

    async def __aexit__(self, exc_type, exc, tb):
        """
        Sai do contexto assíncrono, fechando o cliente HTTP e liberando recursos.
        """
        if self._client:
            await self._client.aclose()

    # -------------------------------------------------------------------------
    # Métodos abstratos
    # -------------------------------------------------------------------------
    @abstractmethod
    async def _prepare_headers(self) -> dict[str, str]:
        """
        Retorna os cabeçalhos HTTP a serem enviados em cada requisição.

        Este método deve ser implementado na subclasse para incluir tokens de
        autenticação, cabeçalhos de conteúdo ou outras informações específicas.

        Returns:
            dict[str, str]: Dicionário de cabeçalhos HTTP.
        """
        raise NotImplementedError()

    # -------------------------------------------------------------------------
    # Métodos principais
    # -------------------------------------------------------------------------
    async def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[dict[str, Any]] = None,
        json: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """
        Executa uma requisição HTTP com retry automático em caso de falhas
        temporárias ou status de erro 5xx.

        O retorno é sempre um dicionário padronizado com as chaves:
        - ``status``: código HTTP
        - ``success``: booleano indicando sucesso
        - ``error``: identificador do erro (caso aplicável)
        - ``body``: conteúdo da resposta (JSON ou texto)

        Args:
            method (str): Método HTTP (``GET``, ``POST``, ``PUT``, ``DELETE``, etc.).
            endpoint (str): Caminho relativo da API (ex: "/users").
            params (dict, opcional): Parâmetros de query string.
            json (dict, opcional): Corpo JSON da requisição.

        Returns:
            dict[str, Any]: Resultado padronizado da operação HTTP.
        """
        headers = await self._prepare_headers()
        client = self._client or httpx.AsyncClient(
            base_url=self.base_url, timeout=self.timeout
        )
        last_error: str | None = None
        status_code: int | None = None

        for attempt in range(self.max_retries):
            try:
                response = await client.request(
                    method,
                    endpoint,
                    headers=headers,
                    params=params,
                    json=json,
                )
                status_code = response.status_code

                # -------------------------------
                # Erros do cliente (4xx)
                # -------------------------------
                if 400 <= status_code < 500:
                    error_key = self.CLIENT_ERRORS.get(status_code, "request_error")
                    try:
                        body = response.json()
                    except ValueError:
                        body = response.text
                    return {
                        "status": status_code,
                        "success": False,
                        "error": error_key,
                        "body": body,
                    }

                # -------------------------------
                # Erros do servidor (5xx) → retry
                # -------------------------------
                if status_code in self.RETRYABLE_STATUS:
                    raise httpx.HTTPStatusError(
                        f"Server error {status_code}",
                        request=response.request,
                        response=response,
                    )

                # -------------------------------
                # Sucesso
                # -------------------------------
                try:
                    data = response.json()
                except ValueError:
                    data = {"raw_body": response.text}

                return {"status": status_code, "success": True, "body": data}

            except asyncio.CancelledError:
                raise
            except (httpx.RequestError, httpx.HTTPStatusError) as e:
                last_error = str(e)
                self.logger.warning(
                    f"Tentativa {attempt + 1}/{self.max_retries} falhou: {e}"
                )
                await asyncio.sleep(2**attempt)

        return {
            "status": status_code,
            "success": False,
            "error": "internal_server_error",
            "body": last_error or "Erro desconhecido",
        }
