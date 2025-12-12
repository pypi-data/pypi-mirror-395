import asyncio
from typing import Any
import datetime
import logging

from global_mapping import bf6 as BF6
from global_mapping.readability.exceptions import NotFoundException
from global_mapping.readability.shared import format_percentage_value

logger = logging.getLogger("api")
DEFAULT_SEASON = "Season1"


async def serverList(servers):
    for server in servers:
        internal_map_name = server.get("currentMap", "")
        internal_mode_name = server.get("mode", "")
        internal_region_name = server.get("region", "")
        server["regionId"] = internal_region_name
        # compat with bf1:
        try:
            server["ownerId"] = f"{server['owner']['personaId']}"
        except KeyError:
            server["ownerId"] = ""

        try:
            server["currentMap"] = BF6.MAPS[internal_map_name]
            server["url"] = BF6.MAP_PICTURES[internal_map_name]
        except KeyError:
            logger.warning(f"new map, bf2042: {internal_map_name}")
            server["currentMap"] = internal_map_name
            server["url"] = ""
        try:
            server["mode"] = BF6.MODES[internal_mode_name]
            server["smallMode"] = BF6.SMALLMODES[internal_mode_name]
        except KeyError:
            logger.warning(f"new mode, bf2042: {internal_mode_name}")
            server["mode"] = internal_mode_name
            server["smallMode"] = ""
        try:
            server["owner"]["platform"] = BF6.PLATFORM[server["owner"]["platformId"]]
        except KeyError:
            server_owner = server.get("owner")
            logger.warning(f"new platform, bf6: {server_owner.get('platformId', 0)}")
            server["owner"]["platform"] = server_owner.get("platformId", 0)
        try:
            server["region"] = BF6.REGIONS[internal_region_name]
        except KeyError:
            logger.warning(f"new region, bf6: {internal_region_name}")
            server["region"] = ""
    return servers


async def detailedServer(server, lang: str):
    server_info = server.get("server_info", {})

    # if (
    #     current_map is not None
    #     and BF2042.MAP_FACTIONS.get(current_map.get("mapname", "")) is not None
    # ):
    #     teams = BF2042.MAP_FACTIONS.get(
    #         current_map.get("mapname", ""),
    #         [{"name": "team 1", "image": None}, {"name": "team 2", "image": None}],
    #     )
    #     server_info["teams"] = {
    #         "teamOne": BF2042.FACTIONS.get(teams[0], {"name": "team 1", "image": None}),
    #         "teamTwo": BF2042.FACTIONS.get(teams[1], {"name": "team 2", "image": None}),
    #     }
    # else:
    #     server_info["teams"] = {
    #         "teamOne": {"name": "team 1", "image": None},
    #         "teamTwo": {"name": "team 2", "image": None},
    #     }

    # mapnames and modes

    internal_map_name = server_info.get("game", {}).get("gameMap", "")
    internal_mode_name = server_info.get("game", {}).get("gameMode", "")
    try:
        server_info["currentMap"] = BF6.MAPS[internal_map_name]
        server_info["currentMapImage"] = BF6.MAP_PICTURES[internal_map_name]
    except KeyError:
        logger.warning(f"new map, BF6: {internal_map_name}")
        server_info["currentMap"] = internal_map_name
        server_info["currentMapImage"] = ""
    try:
        server_info["mode"] = BF6.MODES[internal_mode_name]
    except KeyError:
        logger.warning(f"new mode, BF6: {internal_mode_name}")
        server_info["mode"] = internal_mode_name

    internal_region_name = server_info.get("pingSite", "")

    # platform name
    if server_info.get("owner", None) is not None:
        server_owner = server_info.get("owner", {})
        server_owner["id"] = server_owner.get("personaId", 0)
        try:
            server_owner["platform"] = BF6.PLATFORM[server_owner["platformId"]]
        except KeyError:
            logger.warning(
                f"new platform, bf2042: {server['server_info']['owner']['platformId']}"
            )
            server_owner["platform"] = server_owner["platformId"]
    if server_info.get("configCreator", None) is not None:
        config_creator = server_info.get("configCreator", {})
        config_creator["id"] = config_creator.get("personaId", 0)
        try:
            config_creator["platform"] = BF6.PLATFORM[config_creator["platformId"]]
        except KeyError:
            logger.warning(
                f"new platform, bf2042: {config_creator.get('platformId', 0)}"
            )
            config_creator["platform"] = config_creator.get("platformId", 0)

    # regionname
    try:
        server_info["region"] = BF6.SHORT_REGIONS[internal_region_name]
    except KeyError:
        logger.warning(f"new region, bf2042: {internal_region_name}")
        server_info["region"] = ""

    # extra_info = server_info.get("serverInfo", {})

    # to make it closer to bf1:
    # server_info["prefix"] = extra_info.get("serverName", "")
    # server_info["description"] = extra_info.get("serverDescription", "")

    # settings_translation = await settingsLanguage(lang)
    # # server settings
    # await settingTranslation(settings_translation, server_info.get("settings", {}))

    # regexp = re.compile(r"^ID_.*_DESC$")
    # if extra_info is not None:
    #     if regexp.search(extra_info.get("configDescription", "")):
    #         extra_info["configNameTranslation"] = settings_translation.get(
    #             extra_info.get("configName", ""), None
    #         )
    #         extra_info["configDescriptionTranslation"] = settings_translation.get(
    #             extra_info.get("configDescription", ""), None
    #         )
    #     else:
    #         extra_info["configNameTranslation"] = ""
    #         extra_info["configDescriptionTranslation"] = ""

    return server


async def get_stats(
    data: dict, category_name: str, format_values: bool = True, multiple: bool = False
):
    result = []
    for player in data.get("playerStats", []):
        current_result = {}
        current_player = player.get("player", {"personaId": 0})
        global_stats = {}
        result_count = 0
        # NEW: We're going to save all the catFields here for Redsec.
        all_fields: list[dict[str, Any]] = []

        for category in player.get("categories", []):
            all_fields.extend(category.get("catFields") or [])
            if category_name == category.get("catName", ""):
                result_count += len(category.get("catFields", []))
                for item in category.get("catFields", []):
                    fields: list[dict[str, str]] = item.get("fields", [])
                    if any(field.get("value", "") == "global" for field in fields):
                        global_stats[item["name"]] = item["value"]

        current_result["hasResults"] = result_count > 0
        tasks = []
        filtered_modes = {
            k: v for k, v in BF6.MODES.items() if k not in BF6.REDSEC_MODES.keys()
        }
        tasks.append(get_weapons(global_stats, BF6.WEAPONS, format_values))
        tasks.append(get_vehicles(global_stats, BF6.VEHICLES))
        tasks.append(get_weapons(global_stats, BF6.WEAPON_GROUPS, format_values))
        tasks.append(get_vehicles(global_stats, BF6.VEHICLE_GROUPS))
        tasks.append(get_classes(global_stats))
        tasks.append(get_maps(global_stats, format_values))
        tasks.append(get_seasons(all_fields, filtered_modes))
        tasks.append(get_gadgets(global_stats))
        tasks.append(get_seasons(all_fields, BF6.REDSEC_MODES))

        if multiple:
            platform_id = current_player.get("platformId", 0)
            current_result["id"] = current_player.get("personaId", 0)
            current_result["userId"] = current_player.get("nucleusId", 0)
            current_result["platform"] = BF6.STATS_PLATFORM.get(
                current_player.get("platformId", 0), "pc"
            )
            current_result["platformId"] = 0 if platform_id is None else platform_id

        (
            current_result["weapons"],
            current_result["vehicles"],
            current_result["weaponGroups"],
            current_result["vehicleGroups"],
            current_result["classes"],
            current_result["maps"],
            current_result["seasons"],
            current_result["gadgets"],
            current_result["redsec"],
        ) = await asyncio.gather(*tasks)

        kit_best_kills = 0
        best_kit = 0
        for kit in current_result["classes"]:
            if kit["kills"] > kit_best_kills:
                kit_best_kills = kit["kills"]
                best_kit = kit["className"]
        current_result["bestClass"] = best_kit

        current_result.update(await get_main_stats(global_stats, format_values))

        result.append(current_result)
    if len(result) < 1:
        raise NotFoundException("player not found")
    if len(result) > 1:
        return {"data": result}
    return result[0]


async def get_weapons(stats_dict: dict, constant: dict, format_values: bool = True):
    weapons = []
    for _id, extra in constant.items():
        kills = stats_dict.get(f"kw_wp_{_id}", 0)
        damage = stats_dict.get(f"dmg_wp_{_id}", 0)
        headshots = stats_dict.get(f"hsw_wp_{_id}", 0)
        shots_hit = stats_dict.get(f"shw_wp_{_id}", 0)
        shots_fired = stats_dict.get(f"sfw_wp_{_id}", 0)
        seconds = stats_dict.get(f"tp_wp_{_id}", 0)

        try:
            accuracy = round((shots_hit / shots_fired) * 100, 2)
        except ZeroDivisionError:
            accuracy = 0.0

        try:
            headshot_percentage = round(headshots / kills * 100, 2)
        except ZeroDivisionError:
            headshot_percentage = 0.0

        try:
            kills_per_minute = round(kills / (seconds / 60), 2)
        except (ZeroDivisionError, KeyError):
            kills_per_minute = 0.0

        try:
            damage_per_minute = round(damage / (seconds / 60), 2)
        except (ZeroDivisionError, KeyError):
            damage_per_minute = 0.0

        try:
            hits_per_kill = round(shots_hit / kills, 2)
        except ZeroDivisionError:
            hits_per_kill = 0.0

        weapons.append(
            {
                **extra,
                "id": _id,
                "kills": kills,
                "damage": damage,
                "assistsDamage": stats_dict.get(f"assdmg_wp_{_id}", 0),
                "bodyKills": stats_dict.get(f"bkw_wp_{_id}", 0),
                "headshotKills": headshots,
                "hipfireKills": stats_dict.get(f"hfkw_wp_{_id}", 0),
                "multiKills": stats_dict.get(f"mkw_wp_{_id}", 0),
                "accuracy": format_percentage_value(accuracy, format_values),
                "killsPerMinute": kills_per_minute,
                "damagePerMinute": damage_per_minute,
                "headshots": format_percentage_value(
                    headshot_percentage, format_values
                ),
                "hitVKills": hits_per_kill,
                "shotsHit": shots_hit,
                "shotsFired": shots_fired,
                "scopedKills": stats_dict.get(f"adskw_wp_{_id}", 0),
                "spawns": stats_dict.get(f"spawns_wp_{_id}", 0),
                "timeEquipped": seconds,
            }
        )
    return weapons


async def get_vehicles(stats_dict: dict, constant: dict):
    vehicles = []
    for _id, extra in constant.items():
        kills = stats_dict.get(f"kw_veh_{_id}", 0)
        seconds = stats_dict.get(f"tp_veh_{_id}", 0)
        try:
            kills_per_minute = round(kills / (seconds / 60), 2)
        except ZeroDivisionError:
            kills_per_minute = 0
        vehicles.append(
            {
                **extra,
                "id": _id,
                "kills": kills,
                "killsPerMinute": kills_per_minute,
                "damage": stats_dict.get(f"dmg_veh_{_id}", 0),
                "spawns": stats_dict.get(f"spawns_veh_{_id}", 0),
                "roadKills": stats_dict.get(f"roadkills_veh_{_id}", 0),
                "passengerAssists": stats_dict.get(f"assists_p_veh_{_id}", 0),
                "multiKills": stats_dict.get(f"mkw_veh_{_id}", 0),
                "distanceTraveled": stats_dict.get(f"disttrv_veh_{_id}", 0),
                "driverAssists": stats_dict.get(f"assists_d_veh_{_id}", 0),
                "vehiclesDestroyedWith": stats_dict.get(f"vdw_veh_{_id}", 0),
                "assists": stats_dict.get(f"assists_veh_{_id}", 0),
                "damageTo": stats_dict.get(f"dmgTo_veh_{_id}", 0),
                "destroyed": stats_dict.get(f"vd_veh_{_id}", 0),
                # "idk": stats_dict.get(f"eor_vh_{_id}"),
                "timeIn": seconds,
            }
        )
    return vehicles


async def get_classes(stats_dict: dict):
    kits = []
    for kit_id, extra in BF6.CLASSES.items():
        kills = stats_dict.get(f"kw_kit_{kit_id}", 0)
        deaths = stats_dict.get(f"deaths_kit_{kit_id}", 0)
        seconds = stats_dict.get(f"tp_kit_{kit_id}", 0)
        try:
            kill_death = round(kills / deaths, 2)
        except ZeroDivisionError:
            kill_death = 0.0
        try:
            kills_per_minute = round(kills / (seconds / 60), 2)
        except (ZeroDivisionError, KeyError):
            kills_per_minute = 0.0
        kits.append(
            {
                **extra,
                "id": kit_id,
                "kills": kills,
                "deaths": deaths,
                "kpm": kills_per_minute,
                "killDeath": kill_death,
                "spawns": stats_dict.get(f"spawns_kit_{kit_id}", 0),
                "score": stats_dict.get(f"scoreas_kit_{kit_id}", 0),
                "assists": stats_dict.get(f"assists_kit_{kit_id}", 0),
                "secondsPlayed": seconds,
            }
        )
    return kits


async def get_gadgets(stats_dict: dict):
    gadgets = []
    for _id, extra in BF6.GADGETS.items():
        damage = stats_dict.get(f"dmg_gad_{_id}", 0)
        kills = stats_dict.get(f"kw_gad_{_id}", 0)
        seconds = stats_dict.get(f"tp_gad_{_id}", 0)

        try:
            kills_per_minute = round(kills / (seconds / 60), 2)
        except (ZeroDivisionError, KeyError):
            kills_per_minute = 0.0

        try:
            damage_per_minute = round(damage / (seconds / 60), 2)
        except (ZeroDivisionError, KeyError):
            damage_per_minute = 0.0

        gadgets.append(
            {
                **extra,
                "id": _id,
                "kills": kills,
                "assistsDamage": stats_dict.get(f"assdmg_gad_{_id}", 0),
                "assists": stats_dict.get(f"assists_gad_{_id}", 0),
                "spawns": stats_dict.get(f"spawns3_gad_{_id}", 0),
                "damage": damage,
                "uses": stats_dict.get(f"uses_gad_{_id}", 0),
                "multiKills": stats_dict.get(f"mkw_gad_{_id}", 0),
                "vehiclesDestroyedWith": stats_dict.get(f"vehd_gad_{_id}", 0),
                "kpm": kills_per_minute,
                "dpm": damage_per_minute,
                "secondsPlayed": seconds,
            }
        )
    return gadgets


async def get_maps(stats_dict: dict, format_values: bool = False):
    maps = []
    for _id, extra in BF6.STAT_MAPS.items():
        wins = stats_dict.get(f"wins_lvl{_id}", 0)
        losses = stats_dict.get(f"losses_lvl{_id}", 0)
        try:
            win_percent = round(wins / (wins + losses) * 100, 2)
        except ZeroDivisionError:
            win_percent = 0.0

        maps.append(
            {
                **extra,
                "id": _id,
                "wins": wins,
                "losses": losses,
                "matches": stats_dict.get(f"matches_lvl{_id}", 0),
                "winPercent": format_percentage_value(win_percent, format_values),
                "secondsPlayed": stats_dict.get(f"tp_lvl{_id}", 0),
            }
        )
    return maps


async def get_main_stats(stats_dict: dict, format_values: bool = True):
    shots_fired = stats_dict.get("shots_fired_total", 0)
    shots_hit = stats_dict.get("shots_hit_total", 0)
    wins = stats_dict.get("won_match_total", 0)
    losses = stats_dict.get("lost_match_total", 0)
    kills = stats_dict.get("Kills_Total", 0)
    deaths = stats_dict.get("deaths_total", 0)
    seconds = stats_dict.get("tp_gm_all", 0)
    damage = stats_dict.get("dmg_total", 0)
    human_kills = stats_dict.get("human_kills_total", 0)
    headshot_amount = stats_dict.get("kills_Headshots_Total", 0)
    matches_played = stats_dict.get("played_match_total", 0)
    try:
        accuracy = round((shots_hit / shots_fired) * 100, 2)
    except ZeroDivisionError:
        accuracy = 0.0
    try:
        win_percent = round(wins / (wins + losses) * 100, 2)
    except ZeroDivisionError:
        win_percent = 0.0
    try:
        headshots = round((headshot_amount / kills) * 100, 2)
    except ZeroDivisionError:
        headshots = 0.0
    try:
        kill_death = round(kills / deaths, 2)
        infantry_kill_death = round(human_kills / deaths, 2)
    except ZeroDivisionError:
        kill_death = 0.0
        infantry_kill_death = 0.0
    try:
        kills_per_minute = round(kills / (seconds / 60), 2)
        damage_per_minute = round(damage / (seconds / 60), 2)
    except (ZeroDivisionError, KeyError):
        kills_per_minute = 0.0
        damage_per_minute = 0.0

    try:
        kills_per_match = round(kills / matches_played, 2)
        damage_per_match = round(damage / matches_played, 2)
    except (ZeroDivisionError, KeyError):
        kills_per_match = 0.0
        damage_per_match = 0.0

    try:
        human_precentage = round((human_kills / kills) * 100, 2)
    except ZeroDivisionError:
        human_precentage = 0.0

    return {
        "humanPrecentage": format_percentage_value(human_precentage, format_values),
        "kills": kills,
        "deaths": deaths,
        "wins": wins,
        "loses": losses,
        "killsPerMinute": kills_per_minute,
        "damagePerMinute": damage_per_minute,
        "killsPerMatch": kills_per_match,
        "damagePerMatch": damage_per_match,
        "headShots": headshot_amount,
        "winPercent": format_percentage_value(win_percent, format_values),
        "headshots": format_percentage_value(headshots, format_values),
        "killDeath": kill_death,
        "infantryKillDeath": infantry_kill_death,
        "damage": damage,
        "timePlayed": str(datetime.timedelta(seconds=stats_dict.get("tp_gm_all", 0))),
        "accuracy": format_percentage_value(accuracy, format_values),
        "revives": stats_dict.get("Revives_Teammates_Total", 0),
        "heals": stats_dict.get("Dmg_Healed_Total", 0),
        "resupplies": stats_dict.get("Resupply_Teammates_Total", 0),
        "repairs": stats_dict.get("Veh_RepairedHP_Total", 0),
        "squadmateRevive": stats_dict.get("Revives_Squadmates_Total", 0),
        "thrownThrowables": stats_dict.get("thrown_throwables_total", 0),
        "inRound": {
            "revives": stats_dict.get("revives_inround_cb", 0),
            "resupplies": stats_dict.get("resupply_teammates_inround_cb", 0),
            "spotAssists": stats_dict.get("spot_assist_inround_cb", 0),
            "thrownThrowables": stats_dict.get("thrown_throwables_inround_cb", 0),
            "playerTakeDowns": stats_dict.get("players_taken_down_inround_cb", 0),
        },
        "gadgetsDestoyed": stats_dict.get("destroy_gadget_total", 0),
        "playerTakeDowns": (stats_dict.get("Players_Taken_Down_Total", 0)),
        "matchesPlayed": matches_played,
        "secondsPlayed": seconds,
        "dividedSecondsPlayed": {
            "flying": stats_dict.get("flying_time_total", 0),
            "driving": stats_dict.get("driving_time_total", 0),
        },
        "saviorKills": stats_dict.get("savior_kills_total", 0),
        "shotsFired": shots_fired,
        "shotsHit": shots_hit,
        "killAssists": stats_dict.get("assists_gm_all", 0),
        "vehiclesDestroyed": stats_dict.get("Destroyed_Veh_Total", 0),
        "enemiesSpotted": stats_dict.get("Spotted_Enemies_Total", 0),
        "dividedKills": {
            "ads": stats_dict.get("Kills_ADS_Total", 0),
            "grenades": stats_dict.get("Kills_Grenade_Total", 0),
            "hipfire": stats_dict.get("Kills_Hipfire_Total", 0),
            "longDistance": stats_dict.get("Kills_LongDist_Total", 0),
            "melee": stats_dict.get("Kills_Melee_Total", 0),
            "multiKills": stats_dict.get("Kills_Multi_Total", 0),
            "passenger": stats_dict.get("Kills_Psgr_Total", 0),
            "vehicle": stats_dict.get("Kills_wVeh_Total", 0),
            "roadkills": stats_dict.get("kill_road_total", 0),
            "human": human_kills,
            "weapons": {
                "SMG": stats_dict.get("kills_smg_total", 0),
                "LMG": stats_dict.get("kills_lmg_total", 0),
                "DMR": stats_dict.get("kills_dmr_total", 0),
                "Shotguns": stats_dict.get("kills_sg_total", 0),
                "Assault Rifles": stats_dict.get("kills_sg_total", 0),
            },
            "inRound": {
                "total": stats_dict.get("kills_inround_cb", 0),
                "grenade": stats_dict.get("kills_grenade_inround_cb", 0),
                "headshots": stats_dict.get("kills_headshots_inround_cb", 0),
                "melee": stats_dict.get("kills_melee_inround_cb", 0),
                "multiKills": stats_dict.get("kills_multi_inround_cb", 0),
                "weapons": {
                    "SMG": stats_dict.get("kills_smg_inround_cb", 0),
                    "AR": stats_dict.get("kills_ar_inround_cb", 0),
                    "DMR": stats_dict.get("kills_dmr_inround_cb", 0),
                },
            },
        },
        "devidedDamage": {
            "passenger": stats_dict.get("Dmg_DealtPsgr_Total", 0),
            "vehicleDriver": stats_dict.get("dmg_vehdriver_total", 0),
            "toVehicle": stats_dict.get("Dmg_Dealt_To_Veh_Total", 0),
            "inRound": {
                "asVehicle": stats_dict.get("dmgwith_veh_inround_cb", 0),
            },
        },
        "devidedAssists": {
            "driver": stats_dict.get("Assists_Driver_Total", 0),
            "passenger": stats_dict.get("Assists_Psgr_Total", 0),
            "spot": stats_dict.get("Assists_Spot_Total", 0),
            "pilot": stats_dict.get("assists_pilot_total", 0),
            "inRound": {
                "total": stats_dict.get("assists_inround_cb", 0),
            },
        },
        "distanceTraveled": {
            "foot": stats_dict.get("distrav_foot_total", 0),
            "passenger": stats_dict.get("distrav_psgr_total", 0),
            "vehicle": stats_dict.get("distrav_veh_total", 0),
        },
        "sector": {
            "captured": stats_dict.get("sect_cap_total", 0),
        },
        "objective": {
            "time": {
                "total": stats_dict.get("Obj_Time_Total", 0),
                "attacked": stats_dict.get("obj_attack_time_Total", 0),
                "defended": stats_dict.get("Obj_DefendTime_Total", 0),
            },
            "armed": stats_dict.get("obj_arm_total", 0),
            "captured": stats_dict.get("Obj_Captured_Total", 0),
            "neutralized": stats_dict.get("obj_neutralized_total", 0),
            "defused": stats_dict.get("obj_defuse_total", 0),
            "destroyed": stats_dict.get("Obj_Destroyed_Total", 0),
            "inRound": {
                "armed": stats_dict.get("obj_arm_inround_cb", 0),
                "captured": stats_dict.get("cap_obj_inround_cb", 0),
                "neutralized": stats_dict.get("cap_neut_obj_inround_cb", 0),
                "defused": stats_dict.get("obj_defuse_inround_cb", 0),
                "destroyed": stats_dict.get("obj_dest_inround_cb", 0),
            },
        },
        "XP": (
            {
                "total": stats_dict.get("xp_all", 0),
                "performance": stats_dict.get("xp_performance", 0),
                "accolades": stats_dict.get("xp_accolades", 0),
            },
        ),
    }


async def players(player_list):
    for player in player_list.get("results", []):
        player["platformId"] = player.get("platform", 0)
        player["platform"] = BF6.STATS_PLATFORM.get(player.get("platform", 0), "pc")
    return player_list


async def get_seasons(all_fields: list[dict[str, Any]], MODES: dict):
    seasons = []
    for season_id, season in BF6.SEASONS.items():
        modes = []
        for internal_mode_name, mode_name in MODES.items():
            index: dict[str, int] = {}
            for item in all_fields:
                fields = item.get("fields", [])
                gm = None
                sn = None

                for f in fields:
                    fname = f.get("name")
                    if fname == "GameMode":
                        gm = f.get("value")
                    elif fname == "Season":
                        sn = f.get("value")

                if gm == internal_mode_name and sn == season_id:
                    index[item.get("name", "")] = item.get("value", 0)

            if not index:
                continue

            def first(names: list[str]) -> int:
                for n in names:
                    if n in index:
                        return index[n]
                return 0

            played = first(
                [
                    "played_match_total",
                    "matches_lvlftpgranite",
                    "matches_lvlftp",
                    "matches_level",
                ]
            )

            wins = first(
                [
                    "won_match_total",
                    "wins_lvlftpgranite",
                    "wins_lvlftp",
                    "wins_level",
                ]
            )

            losses = first(
                [
                    "lost_match_total",
                    "losses_lvlftpgranite",
                    "losses_lvlftp",
                    "losses_level",
                ]
            )

            kills = first(["human_kills_total"])
            deaths = first(["deaths_total"])
            score = first(["score_total"])
            time_played = first(["tp_level"])  # seconds
            extractions = first(["extract_extracted_total"])

            kd = round(kills / deaths, 2) if deaths else None
            # winrate = round((wins / played) * 100, 2) if played else None

            modes.append(
                {
                    "modeId": internal_mode_name,
                    "mode": mode_name,
                    "matches": played,
                    "wins": wins,
                    "losses": losses,
                    "kills": kills,
                    "deaths": deaths,
                    "killDeath": kd,
                    "score": score,
                    "secondsPlayed": time_played,
                    "timePlayed": str(datetime.timedelta(seconds=time_played)),
                    "extractions": extractions,
                }
            )

        seasons.append(
            {
                "seasonId": season_id,
                "season": season,
                "modes": modes,
            }
        )
    return seasons
