from requests import Response


class BaseApi:
    BASE_URL = "https://apihub.kma.go.kr/api/typ01/url"

    @staticmethod
    def _preprocess_data(response: Response) -> list[str]:
        data = response.text.splitlines()
        data = [elem for elem in data if not elem.startswith("#")]
        return data
