"""Small SpaceTraders HTTP client.

Gameplay calls use the agent token. Registration uses a separate account token
and lives in contract_runner.py.
"""

import time

import requests


class ApiError(Exception):
    def __init__(self, status, code, message, data=None):
        super().__init__(f"{code}: {message}")
        self.status = status
        self.code = code
        self.message = message
        self.data = data or {}


class Client:
    def __init__(self, token, base_url="https://api.spacetraders.io/v2"):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers["Authorization"] = f"Bearer {token}"
        self._next_request_at = 0.0

    def request(self, method, path, params=None, body=None):
        url = f"{self.base_url}{path}"
        for attempt in range(6):
            self._pace()
            response = self.session.request(method, url, params=params, json=body, timeout=45)
            if response.status_code == 429:
                retry_after = float(response.headers.get("Retry-After", "2"))
                time.sleep(max(retry_after, 1.0))
                continue
            try:
                payload = response.json()
            except ValueError:
                payload = {}
            if response.status_code >= 400:
                error = payload.get("error", {}) if isinstance(payload, dict) else {}
                code = error.get("code", response.status_code)
                message = error.get("message", response.text[:300])
                # A burst can still slip through as a structured rate-limit error.
                if response.status_code == 429 or code == 429:
                    time.sleep(2 + attempt)
                    continue
                raise ApiError(response.status_code, code, message, error.get("data"))
            return payload
        raise ApiError(429, 429, "Rate limit persisted after retries")

    def _pace(self):
        wait = self._next_request_at - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        self._next_request_at = time.monotonic() + 0.55

    def get_data(self, path, params=None):
        return self.request("GET", path, params=params).get("data")

    def list_data(self, path, params=None):
        page = 1
        items = []
        while True:
            query = dict(params or {})
            query.update({"page": page, "limit": 20})
            payload = self.request("GET", path, params=query)
            batch = payload.get("data") or []
            items.extend(batch)
            total = (payload.get("meta") or {}).get("total", len(items))
            if not batch or len(items) >= total:
                return items
            page += 1

    def agent(self):
        return self.get_data("/my/agent")

    def ships(self):
        return self.list_data("/my/ships")

    def ship(self, symbol):
        return self.get_data(f"/my/ships/{symbol}")

    def contracts(self):
        return self.list_data("/my/contracts")

    def accept_contract(self, contract_id):
        return self.request("POST", f"/my/contracts/{contract_id}/accept").get("data")

    def deliver(self, contract_id, ship_symbol, trade_symbol, units):
        body = {"shipSymbol": ship_symbol, "tradeSymbol": trade_symbol, "units": units}
        return self.request("POST", f"/my/contracts/{contract_id}/deliver", body=body).get("data")

    def fulfill(self, contract_id):
        return self.request("POST", f"/my/contracts/{contract_id}/fulfill").get("data")

    def negotiate(self, ship_symbol):
        return self.request("POST", f"/my/ships/{ship_symbol}/negotiate/contract").get("data")

    def orbit(self, ship_symbol):
        return self.request("POST", f"/my/ships/{ship_symbol}/orbit").get("data")

    def dock(self, ship_symbol):
        return self.request("POST", f"/my/ships/{ship_symbol}/dock").get("data")

    def navigate(self, ship_symbol, waypoint_symbol):
        return self.request(
            "POST",
            f"/my/ships/{ship_symbol}/navigate",
            body={"waypointSymbol": waypoint_symbol},
        ).get("data")

    def set_flight_mode(self, ship_symbol, flight_mode):
        return self.request(
            "PATCH",
            f"/my/ships/{ship_symbol}/nav",
            body={"flightMode": flight_mode},
        ).get("data")

    def refuel(self, ship_symbol):
        return self.request("POST", f"/my/ships/{ship_symbol}/refuel").get("data")

    def extract(self, ship_symbol):
        return self.request("POST", f"/my/ships/{ship_symbol}/extract").get("data")

    def survey(self, ship_symbol):
        return self.request("POST", f"/my/ships/{ship_symbol}/survey").get("data")

    def extract_survey(self, ship_symbol, survey):
        # The survey object is the body. Wrapping it fails signature validation.
        return self.request(
            "POST",
            f"/my/ships/{ship_symbol}/extract/survey",
            body=survey,
        ).get("data")

    def jettison(self, ship_symbol, trade_symbol, units):
        return self.request(
            "POST",
            f"/my/ships/{ship_symbol}/jettison",
            body={"symbol": trade_symbol, "units": units},
        ).get("data")

    def purchase(self, ship_symbol, trade_symbol, units):
        return self.request(
            "POST",
            f"/my/ships/{ship_symbol}/purchase",
            body={"symbol": trade_symbol, "units": units},
        ).get("data")

    def waypoints(self, system_symbol):
        return self.list_data(f"/systems/{system_symbol}/waypoints")

    def market(self, system_symbol, waypoint_symbol):
        return self.get_data(f"/systems/{system_symbol}/waypoints/{waypoint_symbol}/market")
