class EvolutionAPIError(Exception):
    """Erro genérico da API Evolution."""

    pass


class EvolutionAuthenticationError(EvolutionAPIError):
    """Erro de autenticação com a API Evolution."""

    pass


class EvolutionNotFoundError(EvolutionAPIError):
    """Recurso não encontrado na API Evolution."""

    pass
