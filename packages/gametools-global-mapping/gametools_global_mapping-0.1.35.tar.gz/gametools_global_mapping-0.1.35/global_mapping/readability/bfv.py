import asyncio
import datetime
from global_mapping import bf5 as BF5
from global_mapping.readability.shared import format_percentage_value


async def get_maps(stats_dict: dict):
    maps = []
    for _id, extra in BF5.STAT_MAPS.items():
        maps.append({**extra, "id": _id, "score": stats_dict.get(f"sc_lvl_{_id}", 0)})
    return maps


async def get_gamemodes(stats_dict: dict, format_values: bool = False):
    gamemodes = []
    for _id, extra in BF5.STAT_GAMEMODE.items():
        extra_str = BF5.STAT_GAMEMODE_EXTR.get(_id)
        wins = stats_dict.get(f"{_id}_wins", 0)
        losses = stats_dict.get(f"{_id}_losses", 0)

        try:
            win_percent = round(wins / (wins + losses) * 100, 2)
        except ZeroDivisionError:
            win_percent = 0.0

        gamemodes.append(
            {
                **extra,
                "id": _id,
                "score": stats_dict.get(f"sc_{extra_str}", 0),
                "wins": wins,
                "losses": losses,
                "winPercent": format_percentage_value(win_percent, format_values),
            }
        )
    return gamemodes


async def get_classes(stats_dict: dict, format_values: bool = True):
    kits = []
    for kit_id, extra in BF5.CLASSES.items():
        score = stats_dict.get(f"sc_{kit_id}", 0)
        kills = stats_dict.get(f"kit_{kit_id}_kills", 0)
        deaths = stats_dict.get(f"kit_{kit_id}_deaths", 0)
        seconds = stats_dict.get(f"kit_{kit_id}_time", 0)
        shots_hit = stats_dict.get(f"kit_{kit_id}_hits", 0)
        shots_fired = stats_dict.get(f"kit_{kit_id}_shots", 0)

        try:
            accuracy = round((shots_hit / shots_fired) * 100, 2)
        except ZeroDivisionError:
            accuracy = 0.0

        try:
            kill_death = round(kills / deaths, 2)
        except ZeroDivisionError:
            kill_death = 0.0
        try:
            kills_per_minute = round(kills / (seconds / 60), 2)
        except (ZeroDivisionError, KeyError):
            kills_per_minute = 0.0

        try:
            hits_per_kill = round(shots_hit / kills, 2)
        except ZeroDivisionError:
            hits_per_kill = 0.0

        try:
            score_per_minute = round(score / (seconds / 60), 2)
        except (ZeroDivisionError, KeyError):
            score_per_minute = 0.0
        except TypeError:
            score_per_minute = 0.0

        kits.append(
            {
                **extra,
                "id": kit_id,
                "score": score,
                "rank": stats_dict.get(f"rank_{kit_id}", 0),
                "kills": kills,
                "deaths": deaths,
                "kpm": kills_per_minute,
                "spm": score_per_minute,
                "killDeath": kill_death,
                "accuracy": format_percentage_value(accuracy, format_values),
                "hitVKills": hits_per_kill,
                "shotsHit": shots_hit,
                "shotsFired": shots_fired,
                "secondsPlayed": seconds,
            }
        )
    return kits


async def get_weapons(stats_dict: dict, constant: dict, format_values: bool = True):
    weapons = []
    for _id, extra in constant.items():
        kills = stats_dict.get(f"kw_{_id}", 0)
        score = stats_dict.get(f"scrw_{_id}", 0)
        headshots = stats_dict.get(f"hsw_{_id}", 0)
        shots_hit = stats_dict.get(f"shw_{_id}", 0)
        shots_fired = stats_dict.get(f"sfw_{_id}", 0)
        seconds = stats_dict.get(f"tpw_{_id}", 0)

        try:
            accuracy = round((shots_hit / shots_fired) * 100, 2)
        except ZeroDivisionError:
            accuracy = 0.0
        except TypeError:
            accuracy = 0.0

        try:
            headshot_percentage = round(headshots / kills * 100, 2)
        except ZeroDivisionError:
            headshot_percentage = 0.0
        except TypeError:
            headshot_percentage = 0.0

        try:
            kills_per_minute = round(kills / (seconds / 60), 2)
        except (ZeroDivisionError, KeyError):
            kills_per_minute = 0.0
        except TypeError:
            kills_per_minute = 0.0

        try:
            score_per_minute = round(score / (seconds / 60), 2)
        except (ZeroDivisionError, KeyError):
            score_per_minute = 0.0
        except TypeError:
            score_per_minute = 0.0

        try:
            hits_per_kill = round(shots_hit / kills, 2)
        except ZeroDivisionError:
            hits_per_kill = 0.0
        except TypeError:
            hits_per_kill = 0.0

        weapons.append(
            {
                **extra,
                "id": _id,
                "kills": kills,
                "score": score,
                "headshotKills": headshots,
                "accuracy": format_percentage_value(accuracy, format_values),
                "killsPerMinute": kills_per_minute,
                "scorePerMinute": score_per_minute,
                "headshots": format_percentage_value(
                    headshot_percentage, format_values
                ),
                "hitVKills": hits_per_kill,
                "shotsHit": shots_hit,
                "shotsFired": shots_fired,
                "timeEquipped": seconds,
            }
        )
    return weapons


async def get_vehicles(stats_dict: dict, constant: dict):
    vehicles = []
    for _id, extra in constant.items():
        kills = stats_dict.get(f"kw_{_id}", 0)
        seconds = stats_dict.get(f"tpw_{_id}", 0)
        try:
            kills_per_minute = round(kills / (seconds / 60), 2)
        except ZeroDivisionError:
            kills_per_minute = 0
        except TypeError:
            kills_per_minute = 0.0
        vehicles.append(
            {
                **extra,
                "id": _id,
                "kills": kills,
                "killsPerMinute": kills_per_minute,
                "vehiclesDestroyedWith": stats_dict.get(f"vdw_{_id}", 0),
            }
        )
    return vehicles


async def get_main_stats(stats_dict: dict, format_values: bool = True):
    shots_fired = stats_dict.get("shots", 0)
    shots_hit = stats_dict.get("hits", 0)
    wins = stats_dict.get("wins", 0)
    losses = stats_dict.get("losses", 0)
    kills = stats_dict.get("kills", 0)
    deaths = stats_dict.get("deaths", 0)
    headshot_amount = stats_dict.get("headshots", 0)
    matches_played = stats_dict.get("rounds_completed", 0)
    seconds = stats_dict.get("time", 0)
    score = stats_dict.get("sc_roundscore", 0)

    try:
        accuracy = round((shots_hit / shots_fired) * 100, 2)
    except ZeroDivisionError:
        accuracy = 0.0
    except TypeError:
        accuracy = 0.0

    try:
        win_percent = round(wins / (wins + losses) * 100, 2)
    except ZeroDivisionError:
        win_percent = 0.0
    except TypeError:
        win_percent = 0.0

    try:
        headshots = round((headshot_amount / kills) * 100, 2)
    except ZeroDivisionError:
        headshots = 0.0
    except TypeError:
        headshots = 0.0

    try:
        kill_death = round(kills / deaths, 2)
    except ZeroDivisionError:
        kill_death = 0.0
    except TypeError:
        kill_death = 0.0

    try:
        kills_per_minute = round(kills / (seconds / 60), 2)
        score_per_minute = round(score / (seconds / 60), 2)
    except (ZeroDivisionError, KeyError):
        kills_per_minute = 0.0
        score_per_minute = 0.0

    try:
        kills_per_match = round(kills / matches_played, 2)
    except (ZeroDivisionError, KeyError):
        kills_per_match = 0.0
    except TypeError:
        kills_per_match = 0.0

    return {
        "rank": stats_dict.get("rank", 0),
        "kills": kills,
        "deaths": deaths,
        "wins": wins,
        "loses": losses,
        "killsPerMatch": kills_per_match,
        "headShots": headshot_amount,
        "winPercent": format_percentage_value(win_percent, format_values),
        "headshots": format_percentage_value(headshots, format_values),
        "killDeath": kill_death,
        "timePlayed": str(datetime.timedelta(seconds=stats_dict.get("time", 0))),
        "secondsPlayed": seconds,
        "scorePerMinute": score_per_minute,
        "killsPerMinute": kills_per_minute,
        "longestHeadShot": stats_dict.get("longest_hs", 0),
        "dogtagsTaken": stats_dict.get("dogtags", 0),
        "awardScore": stats_dict.get("awardScore", 0),
        "bonusScore": stats_dict.get("bonusScore", 0),
        "squadScore": stats_dict.get("squadScore", 0),
        "avengerKills": stats_dict.get("avenger_kills", 0),
        "saviorKills": stats_dict.get("savior_kills", 0),
        "shotsFired": shots_fired,
        "shotsHit": shots_hit,
        "accuracy": format_percentage_value(accuracy, format_values),
        "killAssists": stats_dict.get("kill_assists", 0),
        "heals": stats_dict.get("heals", 0),
        "revives": stats_dict.get("revives", 0),
        "repairs": stats_dict.get("repairs", 0),
        "resupplies": stats_dict.get("resupplies", 0),
        "dividedResupplies": {
            "support": stats_dict.get("resupplies_support", 0),
            "medic": stats_dict.get("resupplies_medic", 0),
        },
        "devidedDamage": {
            "toVehicle": stats_dict.get("vehicle_damage", 0),
            "toSoldier": stats_dict.get("soldier_damages", 0),
        },
        "highestKillStreak": stats_dict.get("highest_ks", 0),
        "roundsPlayed": stats_dict.get("rounds", 0),
        "objective": {
            "score": stats_dict.get("sc_objective", 0),
            "armed": stats_dict.get("objective_armed", 0),
            "destroyed": stats_dict.get("objective_destroyed", 0),
            "disarmed": stats_dict.get("objective_disarmed", 0),
        },
        "dividedKills": {
            "nemesis": stats_dict.get("nemesis_kills", 0),
            "pvp": stats_dict.get("kills_pvp", 0),
            "offensive": stats_dict.get("kills_offensive", 0),
            "defensive": stats_dict.get("kills_defensive", 0),
            "aggregated": stats_dict.get("kills_aggregated", 0),
        },
        "devidedScore": {
            "weapons": {
                "general": stats_dict.get("sc_weapons", 0),
                "mmgs": stats_dict.get("sc_mmgs", 0),
                "lmgs": stats_dict.get("sc_lmgs", 0),
                "amrs": stats_dict.get("sc_amr", 0),
                "sniperRifles": stats_dict.get("sc_sniperrifles", 0),
                "assaultRifles": stats_dict.get("sc_assaultrifles", 0),
                "shotguns": stats_dict.get("sc_shotguns", 0),
                "sars": stats_dict.get("sc_sars", 0),
            },
            "vehicles": {
                "general": stats_dict.get("sc_vehicles", 0),
                "cars": stats_dict.get("sc_car", 0),
                "transportVehicles": stats_dict.get("sc_transportvehicles", 0),
                "tanks": stats_dict.get("sc_tanks", 0),
            },
            "awards": stats_dict.get("sc_award", 0),
            "objective": stats_dict.get("sc_objective", 0),
            "gamemode": stats_dict.get("sc_gamemode", 0),
            "combat": stats_dict.get("sc_combat", 0),
            "squad": stats_dict.get("sc_squad", 0),
            "defensive": stats_dict.get("sc_defensive", 0),
            "allAndVehicles": stats_dict.get("sc_alllandvehicles", 0),
        },
    }


async def get_stats(data: dict, format_values: bool = True):
    result = []
    for player in data.get("playerStats", []):
        stats_dict = {}
        for category in player.get("categories", []):
            if category["catName"] == "casablanca_mp_pc":
                for field in category.get("catFields", {"fields": []}).get(
                    "fields", []
                ):
                    stats_dict[field["name"]] = field.get("value", None)
                break

        current_result = {}

        tasks = []
        tasks.append(get_weapons(stats_dict, BF5.WEAPONS, format_values))
        tasks.append(get_vehicles(stats_dict, BF5.VEHICLES))
        tasks.append(get_classes(stats_dict, format_values))
        tasks.append(get_gamemodes(stats_dict, format_values))
        tasks.append(get_maps(stats_dict))

        (
            current_result["weapons"],
            current_result["vehicles"],
            current_result["classes"],
            current_result["gamemodes"],
            current_result["maps"],
        ) = await asyncio.gather(*tasks)

        current_result["id"] = player.get("player", 0)
        current_result.update(await get_main_stats(stats_dict, format_values))
        result.append(current_result)
    if len(result) > 1:
        return {"data": result}
    return result[0]
