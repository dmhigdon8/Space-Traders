"""Finish SpaceTraders contracts with one ship, then take the next one.

The first run registers LONESTARTIGER with the DOMINION faction. Later runs
reuse the saved agent token and pick up whatever contract is already accepted.

    python contract_runner.py

Stop with Ctrl+C. Starting the script again continues the same contract.
"""

import math
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

from client import ApiError, Client


CALLSIGN = "LONESTARTIGER"
FACTION = "DOMINION"
ROOT = Path(__file__).resolve().parent
ENV_PATH = ROOT / ".env"
CREDIT_RESERVE = 5_000
ASTEROID_TYPES = {"ENGINEERED_ASTEROID", "ASTEROID", "ASTEROID_BASE", "ASTEROID_FIELD"}
TYPE_RANK = {"ENGINEERED_ASTEROID": 0, "ASTEROID": 1, "ASTEROID_BASE": 2, "ASTEROID_FIELD": 3}
TRAIT_FOR_GOOD = {
    "QUARTZ_SAND": "MINERAL_DEPOSITS",
    "SILICON_CRYSTALS": "MINERAL_DEPOSITS",
    "PRECIOUS_STONES": "MINERAL_DEPOSITS",
    "DIAMONDS": "MINERAL_DEPOSITS",
    "IRON_ORE": "COMMON_METAL_DEPOSITS",
    "COPPER_ORE": "COMMON_METAL_DEPOSITS",
    "ALUMINUM_ORE": "COMMON_METAL_DEPOSITS",
    "SILVER_ORE": "PRECIOUS_METAL_DEPOSITS",
    "GOLD_ORE": "PRECIOUS_METAL_DEPOSITS",
    "PLATINUM_ORE": "PRECIOUS_METAL_DEPOSITS",
    "URANITE_ORE": "RARE_METAL_DEPOSITS",
    "MERITIUM_ORE": "RARE_METAL_DEPOSITS",
    "ICE_WATER": "ICE_CRYSTALS",
    "AMMONIA_ICE": "ICE_CRYSTALS",
}


def log(message):
    stamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{stamp}] {message}", flush=True)


def load_env():
    values = {}
    if not ENV_PATH.exists():
        return values
    for line in ENV_PATH.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def save_env(values):
    order = ["SPACETRADERS_ACCOUNT_TOKEN", "SPACETRADERS_TOKEN"]
    lines = [f"{key}={values[key]}" for key in order if values.get(key)]
    for key, value in values.items():
        if key not in order and value:
            lines.append(f"{key}={value}")
    ENV_PATH.write_text("\n".join(lines) + "\n")
    os.chmod(ENV_PATH, 0o600)


def ensure_agent_token():
    env = load_env()
    if env.get("SPACETRADERS_TOKEN"):
        return env["SPACETRADERS_TOKEN"]

    account = env.get("SPACETRADERS_ACCOUNT_TOKEN")
    if not account:
        raise SystemExit(
            "Registration needs an account token from https://my.spacetraders.io\n"
            "Add it to .env as SPACETRADERS_ACCOUNT_TOKEN=... and run this again.\n"
            "The script will register LONESTARTIGER with DOMINION and save the agent token."
        )

    log(f"Registering {CALLSIGN} with {FACTION}")
    response = requests.post(
        "https://api.spacetraders.io/v2/register",
        headers={"Authorization": f"Bearer {account}", "Content-Type": "application/json"},
        json={"symbol": CALLSIGN, "faction": FACTION},
        timeout=45,
    )
    try:
        body = response.json()
    except ValueError:
        body = {}
    if response.status_code != 201:
        error = body.get("error", {})
        raise SystemExit(f"Registration failed ({error.get('code')}): {error.get('message', response.text[:300])}")

    token = body["data"]["token"]
    env["SPACETRADERS_TOKEN"] = token
    save_env(env)
    agent = body["data"]["agent"]
    log(f"Registered {agent['symbol']} at {agent['headquarters']} with {agent['credits']} credits")
    return token


def parse_time(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def sleep_until(moment, label):
    remaining = (moment - datetime.now(timezone.utc)).total_seconds()
    if remaining <= 0:
        return
    log(f"{label} in {int(remaining)}s")
    while True:
        remaining = (moment - datetime.now(timezone.utc)).total_seconds()
        if remaining <= 1:
            break
        time.sleep(min(30, remaining))
    time.sleep(1)


def system_of(waypoint_symbol):
    return "-".join(waypoint_symbol.split("-")[:-1])


def fuel_cost(distance, mode):
    """Fuel for one hop. Cruise is round(distance), drift is 1, burn is double."""
    if distance <= 0:
        return 0
    rounded = max(1, round(distance))
    if mode == "DRIFT":
        return 1
    if mode == "BURN":
        return max(2, 2 * rounded)
    return rounded


def cargo_units(ship, good):
    return sum(item["units"] for item in ship["cargo"]["inventory"] if item["symbol"] == good)


def cargo_free(ship):
    return ship["cargo"]["capacity"] - ship["cargo"]["units"]


def trait_symbols(waypoint):
    return {trait["symbol"] for trait in waypoint.get("traits", [])}


def deposit_symbols(survey):
    symbols = []
    for deposit in survey.get("deposits", []):
        if isinstance(deposit, str):
            symbols.append(deposit)
        elif deposit.get("symbol"):
            symbols.append(deposit["symbol"])
    return symbols


def can_extract(ship, good):
    return any(good in mount.get("deposits", []) for mount in ship.get("mounts", []))


def has_surveyor(ship):
    return any(mount["symbol"].startswith("MOUNT_SURVEYOR") for mount in ship.get("mounts", []))


class Runner:
    def __init__(self, client):
        self.client = client
        self.fleet = {}
        self.agent = None
        self._waypoints = {}
        self._known_fuel = set()
        self._known_dry = set()
        self._sellers = {}

    def cycle(self):
        self.agent = self.client.agent()
        self.fleet = {ship["symbol"]: ship for ship in self.client.ships()}
        log(f"{self.agent['symbol']} has {self.agent['credits']} credits and {len(self.fleet)} ships")

        contract = self.current_contract()
        if contract is None:
            contract = self.negotiate_contract()
        if not contract["accepted"]:
            accepted = self.client.accept_contract(contract["id"])
            contract = accepted["contract"]
            payment = contract["terms"]["payment"]["onAccepted"]
            log(f"Accepted contract {contract['id']} for {payment} credits")

        for delivery in contract["terms"]["deliver"]:
            contract = self.fill_delivery(contract, delivery)

        fulfilled = self.client.fulfill(contract["id"])
        agent = fulfilled.get("agent") or self.client.agent()
        payment = contract["terms"]["payment"]["onFulfilled"]
        log(f"Fulfilled contract {contract['id']} for {payment} credits. Balance is {agent['credits']}")

    def current_contract(self):
        now = datetime.now(timezone.utc)
        contracts = self.client.contracts()
        usable = []
        for contract in contracts:
            if contract.get("fulfilled"):
                continue
            if parse_time(contract["terms"]["deadline"]) <= now:
                continue
            usable.append(contract)
        accepted = [contract for contract in usable if contract.get("accepted")]
        if accepted:
            return accepted[0]
        return usable[0] if usable else None

    def negotiate_contract(self):
        ship = self.hauler()
        headquarters = self.agent["headquarters"]
        log(f"No open contract. Negotiating at {headquarters}")
        ship = self.go_to(ship, headquarters)
        ship = self.dock(ship)
        data = self.client.negotiate(ship["symbol"])
        contract = data["contract"]
        goods = ", ".join(
            f"{item['unitsRequired']} {item['tradeSymbol']}" for item in contract["terms"]["deliver"]
        )
        log(f"New contract {contract['id']}: {goods}")
        return contract

    def fill_delivery(self, contract, delivery):
        good = delivery["tradeSymbol"]
        destination = delivery["destinationSymbol"]
        required = delivery["unitsRequired"]
        while True:
            contract = self.refresh_contract(contract["id"])
            delivery = self.matching_delivery(contract, good, destination)
            remaining = delivery["unitsRequired"] - delivery["unitsFulfilled"]
            if remaining <= 0:
                log(f"{good} delivery complete ({required} units)")
                return contract

            holder = self.ship_holding(good)
            worker = holder or self.pick_ship(good)
            worker = self.refresh(worker["symbol"])
            have = cargo_units(worker, good)
            log(f"Need {remaining} {good} at {destination}. {worker['symbol']} is carrying {have}")

            if have <= 0:
                if can_extract(worker, good):
                    worker = self.mine_load(worker, good, remaining)
                else:
                    worker = self.buy_load(worker, good, remaining)
                have = cargo_units(worker, good)
                if have <= 0:
                    raise RuntimeError(f"Could not acquire any {good}")

            before = delivery["unitsFulfilled"]
            worker, contract = self.deliver(worker, contract, good, destination)
            delivery = self.matching_delivery(contract, good, destination)
            if delivery["unitsFulfilled"] <= before:
                raise RuntimeError(f"Delivery of {good} made no progress")

    def mine_load(self, ship, good, units_needed):
        sites = self.mining_sites(ship, good)
        if not sites:
            raise RuntimeError(f"No extraction site for {good} in {ship['nav']['systemSymbol']}")

        for site in sites:
            log(f"Mining {good} at {site['symbol']} ({site['type']})")
            ship = self.go_to(ship, site["symbol"])
            ship = self.orbit(ship)
            before = cargo_units(ship, good)
            ship = self.extract_until(ship, good, units_needed)
            if cargo_units(ship, good) > before:
                return ship
            log(f"{site['symbol']} did not yield {good}. Trying another site")
        raise RuntimeError(f"Visited every likely site and never extracted {good}")

    def extract_until(self, ship, good, units_needed):
        misses = 0
        while cargo_units(ship, good) < units_needed:
            if cargo_free(ship) <= 0:
                ship = self.dump_others(ship, good)
                if cargo_free(ship) <= 0:
                    break
            ship, yield_item = self.extract_once(ship, good)
            if yield_item is None:
                misses += 1
            elif yield_item["symbol"] == good:
                misses = 0
                log(f"Extracted {yield_item['units']} {good}. Cargo {cargo_units(ship, good)}/{units_needed}")
            else:
                misses += 1
                log(f"Extracted {yield_item['units']} {yield_item['symbol']} instead of {good}")
                ship = self.jettison(ship, yield_item["symbol"], cargo_units(ship, yield_item["symbol"]))
            if misses >= 4 and cargo_units(ship, good) == 0:
                break
        return ship

    def extract_once(self, ship, good):
        ship = self.wait_ready(ship)
        if has_surveyor(ship):
            survey_data = self.client.survey(ship["symbol"])
            ship = self.apply(ship, survey_data)
            matches = [
                survey
                for survey in survey_data.get("surveys", [])
                if good in deposit_symbols(survey)
            ]
            if not matches:
                log("Survey did not find the contract good")
                return ship, None
            ship = self.wait_ready(ship)
            data = self.client.extract_survey(ship["symbol"], matches[0])
        else:
            data = self.client.extract(ship["symbol"])
        ship = self.apply(ship, data)
        return ship, data["extraction"]["yield"]

    def buy_load(self, ship, good, units_needed):
        sellers = self.sellers(ship["nav"]["systemSymbol"], good)
        if not sellers:
            raise RuntimeError(f"No market in {ship['nav']['systemSymbol']} sells {good}, and this ship cannot mine it")

        here = self.ship_xy(ship)
        sellers.sort(
            key=lambda market: (
                good not in market["exports"],
                math.hypot(market["waypoint"]["x"] - here[0], market["waypoint"]["y"] - here[1]),
            )
        )
        for market in sellers:
            waypoint = market["waypoint"]["symbol"]
            log(f"Buying {good} at {waypoint}")
            ship = self.go_to(ship, waypoint)
            ship = self.dock(ship)
            listing = self.price_listing(ship, good)
            if listing is None:
                log(f"{waypoint} is not selling {good} right now")
                continue
            ship = self.purchase_listing(ship, good, units_needed, listing)
            if cargo_units(ship, good) > 0:
                return ship
        raise RuntimeError(f"Could not buy {good}")

    def purchase_listing(self, ship, good, units_needed, listing):
        price = listing["purchasePrice"]
        volume = listing.get("tradeVolume") or 1
        while cargo_units(ship, good) < units_needed and cargo_free(ship) > 0:
            need = units_needed - cargo_units(ship, good)
            self.agent = self.client.agent()
            affordable = (self.agent["credits"] - CREDIT_RESERVE) // price
            units = min(need, cargo_free(ship), volume, affordable)
            if units <= 0:
                log(f"Stopping purchases. Credits {self.agent['credits']}, price {price}")
                break
            data = self.client.purchase(ship["symbol"], good, units)
            ship = self.apply(ship, data)
            if "agent" in data:
                self.agent = data["agent"]
            log(f"Bought {units} {good} at {price} each")
        return ship

    def deliver(self, ship, contract, good, destination):
        delivery = self.matching_delivery(contract, good, destination)
        remaining = delivery["unitsRequired"] - delivery["unitsFulfilled"]
        units = min(cargo_units(ship, good), remaining)
        ship = self.go_to(ship, destination)
        ship = self.dock(ship)
        log(f"Delivering {units} {good} to {destination}")
        data = self.client.deliver(contract["id"], ship["symbol"], good, units)
        ship = self.apply(ship, data)
        contract = data.get("contract") or self.refresh_contract(contract["id"])
        delivery = self.matching_delivery(contract, good, destination)
        log(
            f"Delivered. {delivery['unitsFulfilled']}/{delivery['unitsRequired']} {good}"
        )
        return ship, contract

    def go_to(self, ship, waypoint_symbol):
        ship = self.wait_ready(ship)
        ship_system = ship["nav"]["systemSymbol"]
        if system_of(waypoint_symbol) != ship_system:
            raise RuntimeError(
                f"{ship['symbol']} is in {ship_system} and cannot reach {waypoint_symbol} without a jump or warp"
            )
        for _ in range(8):
            ship = self.wait_ready(ship)
            if ship["nav"]["waypointSymbol"] == waypoint_symbol:
                return ship
            cost = fuel_cost(self.distance_to(ship, waypoint_symbol), "CRUISE")
            if cost > ship["fuel"]["capacity"]:
                hop = self.fuel_hop_toward(ship, waypoint_symbol)
                log(f"{waypoint_symbol} is beyond one tank. Refueling at {hop['symbol']} on the way")
                ship = self.ensure_fuel(ship, hop["symbol"])
                ship = self.travel(ship, hop["symbol"], "CRUISE")
                ship = self.refuel(ship)
                continue
            ship = self.ensure_fuel(ship, waypoint_symbol)
            return self.travel(ship, waypoint_symbol, "CRUISE")
        raise RuntimeError(f"Could not reach {waypoint_symbol} in 8 fuel hops")

    def travel(self, ship, waypoint_symbol, mode, refuel_on_fail=True):
        ship = self.wait_ready(ship)
        if ship["nav"]["waypointSymbol"] == waypoint_symbol:
            return ship
        ship = self.set_flight_mode(ship, mode)
        ship = self.orbit(ship)
        distance = self.distance_to(ship, waypoint_symbol)
        log(f"{ship['symbol']} {mode.lower()} to {waypoint_symbol} ({distance:.0f} away, fuel {ship['fuel']['current']})")
        try:
            data = self.client.navigate(ship["symbol"], waypoint_symbol)
        except ApiError as exc:
            if not refuel_on_fail or "fuel" not in exc.message.lower():
                raise
            log("Not enough fuel for that hop. Refueling, then trying again")
            ship = self.ensure_fuel(ship, waypoint_symbol, force=True)
            return self.travel(ship, waypoint_symbol, mode, refuel_on_fail=False)
        ship = self.apply(ship, data)
        return self.wait_ready(ship)

    def ensure_fuel(self, ship, waypoint_symbol, force=False):
        ship = self.wait_ready(ship)
        cost = fuel_cost(self.distance_to(ship, waypoint_symbol), "CRUISE")
        if not force and ship["fuel"]["current"] >= cost:
            return ship
        if ship["nav"]["waypointSymbol"] != waypoint_symbol and self.sells_fuel(ship["nav"]["waypointSymbol"]):
            log(f"Fuel is {ship['fuel']['current']}/{ship['fuel']['capacity']}. Refueling here before departure")
            return self.refuel(ship)

        station = self.nearest_fuel(ship)
        if station["symbol"] != ship["nav"]["waypointSymbol"]:
            hop = self.distance_to(ship, station["symbol"])
            mode = "CRUISE" if ship["fuel"]["current"] >= fuel_cost(hop, "CRUISE") else "DRIFT"
            if mode == "DRIFT" and ship["fuel"]["current"] < 1:
                raise RuntimeError(f"{ship['symbol']} is out of fuel and not at a fuel stop")
            log(f"Heading to {station['symbol']} for fuel")
            ship = self.travel(ship, station["symbol"], mode, refuel_on_fail=False)
        return self.refuel(ship)

    def fuel_hop_toward(self, ship, destination):
        """Pick a fuel stop we can reach that leaves us closer to the destination."""
        here = self.ship_xy(ship)
        dest = self.waypoints(ship["nav"]["systemSymbol"])[destination]
        current = math.hypot(dest["x"] - here[0], dest["y"] - here[1])
        options = []
        for waypoint in self.waypoints(ship["nav"]["systemSymbol"]).values():
            if waypoint["type"] != "FUEL_STATION" and waypoint["symbol"] != self.agent["headquarters"]:
                continue
            if not self.sells_fuel(waypoint["symbol"]):
                continue
            hop = math.hypot(waypoint["x"] - here[0], waypoint["y"] - here[1])
            if fuel_cost(hop, "CRUISE") > ship["fuel"]["capacity"]:
                continue
            remaining = math.hypot(dest["x"] - waypoint["x"], dest["y"] - waypoint["y"])
            if remaining + 1 < current:
                options.append((remaining, waypoint))
        if not options:
            raise RuntimeError(
                f"No fuel stop can bridge the gap to {destination}. The hop needs more fuel than the tank holds."
            )
        options.sort(key=lambda item: item[0])
        return options[0][1]

    def refuel(self, ship):
        ship = self.wait_ready(ship)
        if ship["fuel"]["current"] >= ship["fuel"]["capacity"]:
            return ship
        ship = self.dock(ship)
        data = self.client.refuel(ship["symbol"])
        ship = self.apply(ship, data)
        transaction = data.get("transaction") or {}
        if transaction:
            log(
                f"Bought {transaction.get('units')} fuel for {transaction.get('totalPrice')} credits"
            )
        return ship

    def orbit(self, ship):
        ship = self.wait_ready(ship)
        if ship["nav"]["status"] == "IN_ORBIT":
            return ship
        return self.apply(ship, self.client.orbit(ship["symbol"]))

    def dock(self, ship):
        ship = self.wait_ready(ship)
        if ship["nav"]["status"] == "DOCKED":
            return ship
        return self.apply(ship, self.client.dock(ship["symbol"]))

    def set_flight_mode(self, ship, mode):
        ship = self.wait_ready(ship)
        if ship["nav"].get("flightMode") == mode:
            return ship
        return self.apply(ship, self.client.set_flight_mode(ship["symbol"], mode))

    def dump_others(self, ship, keep):
        for item in list(ship["cargo"]["inventory"]):
            if item["symbol"] != keep and item["units"] > 0:
                ship = self.jettison(ship, item["symbol"], item["units"])
        return ship

    def jettison(self, ship, good, units):
        if units <= 0:
            return ship
        log(f"Jettisoning {units} {good}")
        data = self.client.jettison(ship["symbol"], good, units)
        return self.apply(ship, data)

    def wait_ready(self, ship):
        ship = self.refresh(ship["symbol"])
        nav = ship["nav"]
        if nav["status"] == "IN_TRANSIT":
            arrival = parse_time(nav["route"]["arrival"])
            sleep_until(arrival, f"{ship['symbol']} arriving at {nav['waypointSymbol']}")
            ship = self.refresh(ship["symbol"])
        remaining = (ship.get("cooldown") or {}).get("remainingSeconds") or 0
        expiration = (ship.get("cooldown") or {}).get("expiration")
        if remaining > 0 and expiration:
            sleep_until(parse_time(expiration), f"{ship['symbol']} cooldown")
            time.sleep(2)
            ship = self.refresh(ship["symbol"])
        return ship

    def refresh(self, symbol):
        ship = self.client.ship(symbol)
        self.fleet[symbol] = ship
        return ship

    def apply(self, ship, data):
        if not isinstance(data, dict):
            return self.refresh(ship["symbol"])
        changed = False
        for key in ("nav", "fuel", "cargo", "cooldown"):
            if data.get(key) is not None:
                ship[key] = data[key]
                changed = True
        self.fleet[ship["symbol"]] = ship
        if not changed:
            return self.refresh(ship["symbol"])
        return ship

    def refresh_contract(self, contract_id):
        for contract in self.client.contracts():
            if contract["id"] == contract_id:
                return contract
        raise RuntimeError(f"Contract {contract_id} is no longer listed")

    def matching_delivery(self, contract, good, destination):
        for delivery in contract["terms"]["deliver"]:
            if delivery["tradeSymbol"] == good and delivery["destinationSymbol"] == destination:
                return delivery
        raise RuntimeError(f"Contract {contract['id']} no longer asks for {good} at {destination}")

    def pick_ship(self, good):
        miners = [ship for ship in self.fleet.values() if can_extract(ship, good)]
        if miners:
            return max(miners, key=lambda ship: ship["cargo"]["capacity"])
        return self.hauler()

    def hauler(self):
        cargo_ships = [ship for ship in self.fleet.values() if ship["cargo"]["capacity"] > 0]
        if not cargo_ships:
            raise RuntimeError("No ship has cargo space")
        return max(cargo_ships, key=lambda ship: ship["cargo"]["capacity"])

    def ship_holding(self, good):
        for symbol in list(self.fleet):
            ship = self.refresh(symbol)
            if cargo_units(ship, good) > 0:
                return ship
        return None

    def waypoints(self, system_symbol):
        if system_symbol not in self._waypoints:
            listed = self.client.waypoints(system_symbol)
            self._waypoints[system_symbol] = {waypoint["symbol"]: waypoint for waypoint in listed}
            log(f"Loaded {len(listed)} waypoints in {system_symbol}")
        return self._waypoints[system_symbol]

    def ship_xy(self, ship):
        waypoint = self.waypoints(ship["nav"]["systemSymbol"])[ship["nav"]["waypointSymbol"]]
        return waypoint["x"], waypoint["y"]

    def distance_to(self, ship, waypoint_symbol):
        origin = self.ship_xy(ship)
        waypoint = self.waypoints(ship["nav"]["systemSymbol"])[waypoint_symbol]
        return math.hypot(waypoint["x"] - origin[0], waypoint["y"] - origin[1])

    def mining_sites(self, ship, good):
        wanted_trait = TRAIT_FOR_GOOD.get(good)
        here = self.ship_xy(ship)
        matched = []
        fallback = []
        for waypoint in self.waypoints(ship["nav"]["systemSymbol"]).values():
            if waypoint["type"] not in ASTEROID_TYPES and wanted_trait not in trait_symbols(waypoint):
                continue
            distance = math.hypot(waypoint["x"] - here[0], waypoint["y"] - here[1])
            rank = TYPE_RANK.get(waypoint["type"], 9)
            if wanted_trait and wanted_trait in trait_symbols(waypoint):
                matched.append((rank, distance, waypoint))
            elif waypoint["type"] in ASTEROID_TYPES:
                fallback.append((rank, distance, waypoint))
        chosen = matched or fallback
        chosen.sort(key=lambda item: (item[0], item[1]))
        return [waypoint for _, _, waypoint in chosen]

    def sells_fuel(self, waypoint_symbol):
        if waypoint_symbol in self._known_fuel:
            return True
        if waypoint_symbol in self._known_dry:
            return False
        system = system_of(waypoint_symbol)
        waypoint = self.waypoints(system)[waypoint_symbol]
        if "MARKETPLACE" not in trait_symbols(waypoint) and waypoint["type"] != "FUEL_STATION":
            self._known_dry.add(waypoint_symbol)
            return False
        if waypoint["type"] == "FUEL_STATION":
            self._known_fuel.add(waypoint_symbol)
            return True
        goods = self.market_symbols(system, waypoint_symbol)
        if "FUEL" in goods["exports"] or "FUEL" in goods["exchange"]:
            self._known_fuel.add(waypoint_symbol)
            return True
        self._known_dry.add(waypoint_symbol)
        return False

    def nearest_fuel(self, ship):
        here = self.ship_xy(ship)
        candidates = []
        for waypoint in self.waypoints(ship["nav"]["systemSymbol"]).values():
            if waypoint["type"] == "FUEL_STATION" or waypoint["symbol"] == self.agent["headquarters"]:
                distance = math.hypot(waypoint["x"] - here[0], waypoint["y"] - here[1])
                candidates.append((distance, waypoint))
        if not candidates:
            raise RuntimeError(f"No fuel stop found in {ship['nav']['systemSymbol']}")
        candidates.sort(key=lambda item: item[0])
        for _, waypoint in candidates:
            if self.sells_fuel(waypoint["symbol"]):
                return waypoint
        raise RuntimeError(f"No waypoint in {ship['nav']['systemSymbol']} is selling fuel")

    def sellers(self, system_symbol, good):
        if system_symbol not in self._sellers:
            self._sellers[system_symbol] = {}
        if good in self._sellers[system_symbol]:
            return self._sellers[system_symbol][good]

        found = []
        markets = [
            waypoint
            for waypoint in self.waypoints(system_symbol).values()
            if "MARKETPLACE" in trait_symbols(waypoint)
        ]
        log(f"Looking through {len(markets)} markets for {good}")
        for waypoint in markets:
            goods = self.market_symbols(system_symbol, waypoint["symbol"])
            if good in goods["exports"] or good in goods["exchange"]:
                found.append({"waypoint": waypoint, **goods})
        self._sellers[system_symbol][good] = found
        return found

    def market_symbols(self, system_symbol, waypoint_symbol):
        market = self.client.market(system_symbol, waypoint_symbol)
        return {
            "exports": [good["symbol"] for good in market.get("exports", [])],
            "exchange": [good["symbol"] for good in market.get("exchange", [])],
            "imports": [good["symbol"] for good in market.get("imports", [])],
        }

    def price_listing(self, ship, good):
        market = self.client.market(ship["nav"]["systemSymbol"], ship["nav"]["waypointSymbol"])
        for listing in market.get("tradeGoods") or []:
            if listing["symbol"] == good and listing.get("purchasePrice") is not None:
                return listing
        return None


def main():
    token = ensure_agent_token()
    runner = Runner(Client(token))
    log("Contract runner started. Ctrl+C leaves the contract in place.")
    while True:
        try:
            runner.cycle()
        except KeyboardInterrupt:
            log("Stopped. Run python contract_runner.py to continue.")
            return
        except ApiError as exc:
            detail = f" {exc.data}" if exc.data else ""
            log(f"API error ({exc.code}): {exc.message}{detail}. Retrying in 20s.")
            time.sleep(20)


if __name__ == "__main__":
    main()
