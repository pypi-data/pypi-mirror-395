from scorb_api.models.endpoints.endpoint_customizado import EndpointCustomizado


class EntidadeCustomizada(EndpointCustomizado):
    def __init__(self, header_auth, cenario_code, custom) -> None:
        super().__init__(
            header_auth=header_auth, cenario_code=cenario_code, custom=custom
        )
