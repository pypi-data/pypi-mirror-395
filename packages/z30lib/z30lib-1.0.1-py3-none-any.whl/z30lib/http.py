import requests

class HTTP:
    """Einfaches HTTP-System für GET und POST Requests mit optionalem automatischem Output."""

    @staticmethod
    def get(url, params=None, headers=None, timeout=10, print_output=True):
        """
        HTTP GET Request.

        :param url: Ziel-URL
        :param params: Dictionary für Query-Parameter
        :param headers: Dictionary für HTTP-Header
        :param timeout: Timeout in Sekunden
        :param print_output: True = automatisch ausgeben
        :return: requests.Response Objekt oder None bei Fehler
        """
        try:
            response = requests.get(url, params=params, headers=headers, timeout=timeout)
            response.raise_for_status()

            if print_output:
                try:
                    print(f"GET Response: {response.json()} - URL {url}")
                except ValueError:
                    print(f"GET Response: {response.text} - URL {url}")

            return response

        except requests.RequestException as e:
            if print_output:
                print(f"[HTTP GET Error] {e} - URL {url}")
            return None

    @staticmethod
    def send(url, data=None, json=None, headers=None, timeout=10, print_output=True):
        """
        HTTP POST Request.

        :param url: Ziel-URL
        :param data: Dictionary oder bytes für Form-Daten
        :param json: Dictionary für JSON-Daten
        :param headers: Dictionary für HTTP-Header
        :param timeout: Timeout in Sekunden
        :param print_output: True = automatisch ausgeben
        :return: requests.Response Objekt oder None bei Fehler
        """
        try:
            response = requests.post(url, data=data, json=json, headers=headers, timeout=timeout)
            response.raise_for_status()

            if print_output:
                print(f"POST Response {response.status_code} - URL {url}")

            return response

        except requests.RequestException as e:
            if print_output:
                print(f"[HTTP POST Error] {e} - URL {url}")
            return None
