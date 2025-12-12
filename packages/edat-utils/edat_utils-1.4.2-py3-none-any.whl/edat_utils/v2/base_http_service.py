from abc import ABC, abstractmethod
import asyncio
import logging
from typing import Any, Dict, List, Literal, Optional, Union
import warnings

import httpx


class BaseHTTPService(ABC):
    """
    Classe base assíncrona para consumo de APIs HTTP usando httpx.

    Funcionalidades:
    - Retry automático em caso de falhas de rede ou status HTTP 5xx.
    - Backoff exponencial entre tentativas.
    - Retorno do motivo do erro em caso de falha.
    - Gerenciamento automático de conexões com context manager.
    - Aceita logger externo para customização de logs.
    """

    def __init__(
        self,
        base_url: str,
        max_retries: int = 3,
        timeout: float = 10.0,
        logger: Optional[logging.Logger] = None,
    ):
        warnings.warn(
            "BaseHTTPService está depreciado e será removido em breve. Use a classe BaseHTTP.",
            DeprecationWarning,
            stacklevel=2,
        )
        self.base_url = base_url.rstrip("/")
        self.max_retries = max_retries
        self.timeout = timeout
        # Usa o logger passado ou cria um interno
        self.logger = logger or logging.getLogger(self.__class__.__name__)

    async def _get_token(self) -> None:
        """
        Hook opcional para atualização de token antes de
        cada requisição, se necessário.
        Subclasses podem sobrescrever se precisarem renovar tokens dinâmicos.
        """
        return None

    @abstractmethod
    async def _prepare_headers(self) -> Dict[str, str]:
        """
        Método abstrato para fornecer headers personalizados.
        Deve ser implementado na classe filha.
        """
        raise NotImplementedError()

    async def request(
        self,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH"],
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Realiza uma requisição HTTP com retry automático em caso de erro 5xx ou falha de rede.
        Gerencia o cliente HTTP internamente usando context manager.

        Parâmetros:
        ----------
        method: str
            Método HTTP ('GET', 'POST', etc.)
        endpoint: str
            Endpoint da API (ex: '/users')
        params: dict, opcional
            Parâmetros de query string.
        json: dict, opcional
            Corpo JSON da requisição.

        Retorno:
        -------
        dict
            Resposta JSON da API ou dicionário com chave 'error' caso todas as tentativas falhem.
        """
        headers = await self._prepare_headers() or {}

        async with httpx.AsyncClient(
            base_url=self.base_url, timeout=self.timeout
        ) as client:
            last_error: str | None = None
            status_error: int | None = None

            for attempt in range(0, self.max_retries):
                try:
                    response = await client.request(
                        method=method,
                        url=endpoint,
                        headers=headers,
                        params=params,
                        json=json,
                    )

                    # --- Erro do cliente ---
                    if response.status_code >= 400 and response.status_code < 500:
                        try:
                            return {
                                "status": response.status_code,
                                "error": "Erro na requisição",
                                "body": response.json(),
                            }
                        except:
                            return {
                                "status": response.status_code,
                                "error": "Erro na requisição",
                                "body": response.text,
                            }

                    # --- Erro do servidor, tentar novamente ---
                    if response.status_code >= 500:
                        status_error = response.status_code
                        raise httpx.HTTPStatusError(
                            f"Server error ({response.status_code})",
                            request=response.request,
                            response=response,
                        )

                    return response.json()

                except (httpx.RequestError, httpx.HTTPStatusError) as e:
                    self.logger.warning(f"Tentativa {attempt} falhou: {str(e)}")
                    last_error = str(e)
                    await asyncio.sleep(2**attempt)

            # Se chegar aqui, todas as tentativas falharam
            # return {"error": last_error or "Erro desconhecido"}
            return {
                "status": status_error,
                "error": "Erro na requisição",
                "body": last_error or "Erro desconhecido",
            }
