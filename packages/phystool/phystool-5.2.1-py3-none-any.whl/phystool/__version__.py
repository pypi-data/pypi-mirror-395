class Version:
    def __init__(self):
        self._version = ""

    def _get_current(self) -> str:
        if not self._version:
            from importlib.metadata import version

            self._version = version("phystool")
        return self._version

    def __str__(self) -> str:
        return self._get_current()

    def get_status(self) -> tuple[str, dict[str, str]]:
        import requests

        info = requests.get("https://pypi.org/pypi/phystool/json").json()["info"]
        could_update = any(
            latest > version
            for latest, version in zip(
                info["version"].split("."), self._get_current().split(".")
            )
        )
        status = (
            f"Version {info["version"]} disponible"
            if could_update
            else "Pas de nouvelle version"
        )
        return status, info["project_urls"]


__version__ = Version()
