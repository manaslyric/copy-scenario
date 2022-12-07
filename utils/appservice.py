"""App Service"""
from pydantic import BaseModel, root_validator
from chainbrain.utils.http_request import HttpRequest, SUCCESS_CODES
from chainbrain.utils.logger import chainbrain_logger as logger
from ..config import get_settings

settings = get_settings()

#pylint: disable=too-few-public-methods
#pylint: disable=missing-class-docstring
class TableURLs(BaseModel):
    service_url: str
    scenario: str = "/scenarios/{id}"

    #pylint: disable=no-self-argument
    #pylint: disable=missing-function-docstring,no-self-use
    @root_validator(pre=False)
    def set_urls(cls, values):
        for value in values:
            if value != "service_url":
                values[value] = values[
                    "service_url"] + values[value]
        return values

class AppService:
    """
    App service api support of lyric
    """

    def __init__(self, service_url: str = None):
        self.client = HttpRequest()
        self.urls: TableURLs = TableURLs(service_url=service_url or settings.appservice_url)

    def update_scenario(self, scenario_id: str, status: str):
        """
        Update the scenario
        """
        response = self.client.patch(
            self.urls.scenario.format(id=scenario_id), json={
                "status": status
            }
        )
        if response.status_code in SUCCESS_CODES:
            return response.json()["data"]
        logger.error(
            """Unable to update status for the scenario, status code: %s, %s""",
            response.status_code,
            response.text
        )
        raise Exception(
            f"""Unable to update status for the scenario status code:""" \
            f""" {response.status_code}, {response.text}"""
        )
