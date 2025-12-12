import asyncio
import datetime
import logging
import re
import json

from global_mapping import bf2042 as BF2042
from global_mapping.readability.bf2042.languages.settingValues.main import (
    selectLanguage as settingsLanguage,
)
from global_mapping.readability.bf2042.saved_items.progresstion_types import (
    getProgressionType,
)
from global_mapping.readability.exceptions import NotFoundException
from global_mapping.readability.shared import format_percentage_value

logger = logging.getLogger("api")


async def settingTranslation(settings_translation: dict, settings: list[dict]):
    for setting in settings:
        for value in setting.get("values", []):
            try:
                value["readableSettingName"] = settings_translation[
                    value["settingName"]
                ]
            except KeyError:
                logger.warning(f"new setting, bf2042: {value.get('settingName', '')}")
                value["readableSettingName"] = ""


async def extraMapInfo(maps):
    for current_map in maps:
        internal_map_name = current_map.get("mapname", "")
        try:
            current_map["mapname"] = BF2042.MAPS[internal_map_name]
            current_map["image"] = BF2042.MAP_PICTURES[internal_map_name]
        except KeyError:
            logger.warning(f"new map, bf2042: {internal_map_name}")
            current_map["mapname"] = internal_map_name
            current_map["image"] = ""
        try:
            current_map["mode"] = BF2042.MODES[current_map["mode"]]
        except KeyError:
            logger.warning(f"new mode, bf2042: {current_map.get('mode', '')}")
            current_map["mode"] = current_map.get("mode", "")


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
            server["currentMap"] = BF2042.MAPS[internal_map_name]
            server["url"] = BF2042.MAP_PICTURES[internal_map_name]
        except KeyError:
            logger.warning(f"new map, bf2042: {internal_map_name}")
            server["currentMap"] = internal_map_name
            server["url"] = ""
        try:
            server["mode"] = BF2042.MODES[internal_mode_name]
            server["smallMode"] = BF2042.SMALLMODES[internal_mode_name]
        except KeyError:
            logger.warning(f"new mode, bf2042: {internal_mode_name}")
            server["mode"] = internal_mode_name
            server["smallMode"] = ""
        try:
            server["owner"]["platform"] = BF2042.PLATFORM[server["owner"]["platformId"]]
        except KeyError:
            server_owner = server.get("owner")
            logger.warning(f"new platform, bf2042: {server_owner.get('platformId', 0)}")
            server["owner"]["platform"] = server_owner.get("platformId", 0)
        try:
            server["region"] = BF2042.REGIONS[internal_region_name]
        except KeyError:
            logger.warning(f"new region, bf2042: {internal_region_name}")
            server["region"] = ""
    return servers


async def detailedServer(server, server_id, lang: str):
    server_info = server.get("server_info", {})
    map_rotation = server_info.get("rotation", {})

    try:
        current_map = map_rotation.get("maps", [])[server_info.get("currentMapId", 0)]
    except IndexError:
        current_map = None

    if (
        current_map is not None
        and BF2042.MAP_FACTIONS.get(current_map.get("mapname", "")) is not None
    ):
        teams = BF2042.MAP_FACTIONS.get(
            current_map.get("mapname", ""),
            [{"name": "team 1", "image": None}, {"name": "team 2", "image": None}],
        )
        server_info["teams"] = {
            "teamOne": BF2042.FACTIONS.get(teams[0], {"name": "team 1", "image": None}),
            "teamTwo": BF2042.FACTIONS.get(teams[1], {"name": "team 2", "image": None}),
        }
    else:
        server_info["teams"] = {
            "teamOne": {"name": "team 1", "image": None},
            "teamTwo": {"name": "team 2", "image": None},
        }

    # mapnames and modes
    await extraMapInfo(map_rotation.get("maps", {}))

    server_info["currentMap"] = current_map.get("mapname", "")
    server_info["currentMapImage"] = current_map.get("image", "")

    # current map
    server_info["rotation"] = server_info.get("rotation", {}).get("maps", [])
    internal_region_name = server_info.get("pingSite", "")

    # platform name
    if server_info.get("owner", None) is not None:
        server_owner = server_info.get("owner", {})
        server_owner["id"] = server_owner.get("personaId", 0)
        try:
            server_owner["platform"] = BF2042.PLATFORM[server_owner["platformId"]]
        except KeyError:
            logger.warning(
                f"new platform, bf2042: {server['server_info']['owner']['platformId']}"
            )
            server_owner["platform"] = server_owner["platformId"]
    if server_info.get("configCreator", None) is not None:
        config_creator = server_info.get("configCreator", {})
        config_creator["id"] = config_creator.get("personaId", 0)
        try:
            config_creator["platform"] = BF2042.PLATFORM[config_creator["platformId"]]
        except KeyError:
            logger.warning(
                f"new platform, bf2042: {config_creator.get('platformId', 0)}"
            )
            config_creator["platform"] = config_creator.get("platformId", 0)

    # regionname
    try:
        server_info["region"] = BF2042.SHORT_REGIONS[internal_region_name]
    except KeyError:
        logger.warning(f"new region, bf2042: {internal_region_name}")
        server_info["region"] = ""

    extra_info = server_info.get("serverInfo", {})

    # to make it closer to bf1:
    server_info["prefix"] = extra_info.get("serverName", "")
    server_info["description"] = extra_info.get("serverDescription", "")
    server_info["serverId"] = server_id

    settings_translation = await settingsLanguage(lang)
    # server settings
    await settingTranslation(settings_translation, server_info.get("settings", {}))

    regexp = re.compile(r"^ID_.*_DESC$")
    if extra_info is not None:
        if regexp.search(extra_info.get("configDescription", "")):
            extra_info["configNameTranslation"] = settings_translation.get(
                extra_info.get("configName", ""), None
            )
            extra_info["configDescriptionTranslation"] = settings_translation.get(
                extra_info.get("configDescription", ""), None
            )
        else:
            extra_info["configNameTranslation"] = ""
            extra_info["configDescriptionTranslation"] = ""

    return server


async def tagTranslation(settings_translation: dict, tags: list[dict]):
    for tag in tags:
        metadata = tag.get("metadata", None)
        if metadata is not None:
            for translation in metadata["translations"]:
                try:
                    translation["localizedText"] = settings_translation.get(
                        translation.get("translationId", ""), ""
                    )
                    translation["localizedTextDesc"] = settings_translation.get(
                        f"{translation.get('translationId', '')}_DESC", ""
                    )
                except KeyError:
                    logger.warning(
                        f"blueprint assetCategories, bf2042: {translation['translationId']}"
                    )
                    translation["localizedText"] = ""
                    translation["localizedTextDesc"] = ""
            for resource in metadata["resources"]:
                try:
                    resource["location"]["url"] = (
                        resource["location"]
                        .get("url", "")
                        .replace(
                            "[BB_PREFIX]",
                            "https://eaassets-a.akamaihd.net/battlelog/battlebinary",
                        )
                    )
                except KeyError:
                    pass
                except AttributeError:
                    pass


async def players(player_list):
    for player in player_list.get("results", []):
        player["platformId"] = player.get("platform", 0)
        player["platform"] = BF2042.STATS_PLATFORM.get(player.get("platform", 0), "pc")
    return player_list


async def playground(current_playground, lang: str, playground_web_data: bytes):
    if playground_web_data is not None:
        try:
            decoded = playground_web_data.decode("utf8", "ignore")
            item = re.findall('{".*?"}', decoded)
            web_data = json.loads(item[0])
        except:
            web_data = {"mainWorkspace": "", "variables": ""}
    else:
        web_data = playground_web_data

    settings_translation = await settingsLanguage(lang)
    # server settings

    tasks = []

    if current_playground["playground"].get("tag", None) is not None:
        tasks.append(
            tagTranslation(
                settings_translation, current_playground["playground"]["tag"]
            )
        )
    if current_playground["playground"].get("originalPlayground", None) is not None:
        tasks.append(
            extraMapInfo(
                current_playground["playground"]["originalPlayground"]["mapRotation"][
                    "maps"
                ]
            )
        )
    if current_playground["playground"].get("validatedPlayground", None) is not None:
        tasks.append(
            extraMapInfo(
                current_playground["playground"]["validatedPlayground"]["mapRotation"][
                    "maps"
                ]
            )
        )
    await asyncio.gather(*tasks)

    if current_playground["playground"].get("progressionMode", None) is not None:
        current_playground["playground"]["progressionMode"][
            "progressibles"
        ] = await getProgressionType(
            current_playground["playground"]["progressionMode"]["value"]
        )

    current_playground["playground"]["blocklyData"] = web_data
    return current_playground["playground"]


async def blueprintTranslation(settingsTranslation: dict, settings: list[dict]):
    for translation in settings:
        try:
            translation["localizedText"] = settingsTranslation[
                translation["translationId"]
            ]
        except KeyError:
            logger.warning(
                f"blueprint new settings, bf2042: {translation.get('translationId', '')}"
            )
            translation["localizedText"] = ""


async def gameDataTranslation(settingsTranslation: dict, settings: list[dict]):
    for setting in settings:
        await blueprintTranslation(
            settingsTranslation, setting["metadata"]["translations"]
        )


async def blueprint(blueprintData, lang: str):
    settings_translation = await settingsLanguage(lang)

    for blueprint_data in blueprintData["blueprint"]:
        tasks = [
            blueprintTranslation(
                settings_translation, blueprint_data["metadata"]["translations"]
            ),
            gameDataTranslation(
                settings_translation, blueprint_data["availableGameData"]["maps"]
            ),
            gameDataTranslation(
                settings_translation, blueprint_data["availableGameData"]["mutators"]
            ),
            tagTranslation(
                settings_translation,
                blueprint_data["availableGameData"]["assetCategories"]["tags"],
            ),
        ]
        for available_tag in blueprint_data["availableTags"]:
            tasks.append(
                blueprintTranslation(
                    settings_translation, available_tag["metadata"]["translations"]
                )
            )

        await asyncio.gather(*tasks)

    return blueprintData


async def getBackground(resources: list[dict]):
    for resource in resources:
        if (
            resource.get("url", None) is not None
            and resource["url"].get("value", None) is not None
        ):
            resource["url"]["value"] = resource["url"]["value"].replace(
                "[BB_PREFIX]", "https://eaassets-a.akamaihd.net/battlelog/battlebinary"
            )


async def available_tags(tag_data, lang: str):
    tag_translation = await settingsLanguage(lang)
    for tag in tag_data.get("availableTags", []):
        await blueprintTranslation(tag_translation, tag["metadata"]["translations"])
    return tag_data


async def getBackgroundSubitem(resources: list[dict]):
    for resource in resources:
        if (
            resource.get("item", None) is not None
            and resource["item"].get("string", None) is not None
        ):
            resource["item"]["string"] = resource["item"]["string"].replace(
                "[BB_PREFIX]", "https://eaassets-a.akamaihd.net/battlelog/battlebinary"
            )


async def scheduled_collections(collections_data, lang: str):
    collection_translations = await settingsLanguage(lang)
    tasks = []
    for collection in collections_data.get("collectionList", []):
        for value in collection.get("collectionValues", []):
            for mix in value.get("mixes", []):
                tasks.append(
                    blueprintTranslation(
                        collection_translations, mix["assets"]["item"]["translations"]
                    )
                )
                tasks.append(getBackgroundSubitem(mix["assets"]["item"]["info"]))
                if mix["mixInfo"] is not None:
                    tasks.append(
                        blueprintTranslation(
                            collection_translations,
                            mix["mixInfo"]["meta"]["item"]["translations"],
                        )
                    )
            if value["main"] is not None:
                tasks.append(
                    blueprintTranslation(
                        collection_translations,
                        value["main"]["subEntry"]["translations"],
                    )
                )
                tasks.append(getBackground(value["main"]["subEntry"]["resource"]))
            if value["secondary"] is not None:
                tasks.append(
                    blueprintTranslation(
                        collection_translations,
                        value["secondary"]["menuEntry"]["subEntry"]["translations"],
                    )
                )
                tasks.append(
                    getBackground(
                        value["secondary"]["menuEntry"]["subEntry"]["resource"]
                    )
                )
    await asyncio.gather(*tasks)
    return collections_data


async def mix_info(mix_data):
    for mix in mix_data.get("mixes", []):
        await extraMapInfo(mix["mapRotation"]["maps"])
    return mix_data


async def get_offers(offer_data, lang: str):
    offer_translation = await settingsLanguage(lang)
    for value in offer_data.get("items", []):
        value["readableTitle"] = offer_translation.get(value.get("title", ""), "")
        value["readableDescription"] = offer_translation.get(
            value.get("description", ""), ""
        )
        for name, art_item in value.get("art", {}).items():
            if art_item is not None:
                value["art"][name]["art"] = art_item.get("art", "").replace(
                    "[BB_PREFIX]",
                    "https://eaassets-a.akamaihd.net/battlelog/battlebinary",
                )

    for bundle in offer_data.get("bundles", []):
        for featured in bundle.get("featured", []):
            for layout in featured.get("layout", []):
                layout["readableTitle"] = offer_translation.get(
                    layout.get("title", ""), ""
                )
        battlepass_banner = bundle.get("battlepassBanner", {})
        if battlepass_banner is not None:
            battlepass_banner["url"] = battlepass_banner.get("url", "").replace(
                "[BB_PREFIX]", "https://eaassets-a.akamaihd.net/battlelog/battlebinary"
            )
            battlepass_banner["localizedText"] = offer_translation.get(
                battlepass_banner.get("translationId", ""), ""
            )

    return offer_data


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
        kills = stats_dict.get(f"kw_vh_{_id}", 0)
        seconds = stats_dict.get(f"tp_vh_{_id}", 0)
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
                "damage": stats_dict.get(f"dmg_vh_{_id}", 0),
                "spawns": stats_dict.get(f"spawns_vh_{_id}", 0),
                "roadKills": stats_dict.get(f"roadkills_vh_{_id}", 0),
                "passengerAssists": stats_dict.get(f"assists_p_vh_{_id}", 0),
                "multiKills": stats_dict.get(f"mkw_vh_{_id}", 0),
                "distanceTraveled": stats_dict.get(f"disttrv_vh_{_id}", 0),
                "driverAssists": stats_dict.get(f"assists_d_vh_{_id}", 0),
                "vehiclesDestroyedWith": stats_dict.get(f"vdw_vh_{_id}", 0),
                "assists": stats_dict.get(f"assists_vh_{_id}", 0),
                "callIns": stats_dict.get(f"callins_vh_{_id}", 0),
                "damageTo": stats_dict.get(f"dmgTo_vh_{_id}", 0),
                "destroyed": stats_dict.get(f"vd_vh_{_id}", 0),
                # "idk": stats_dict.get(f"eor_vh_{_id}"),
                "timeIn": seconds,
            }
        )
    return vehicles


async def get_classes(stats_dict: dict):
    kits = []
    for kit_id, extra in BF2042.CLASSES.items():
        kills = stats_dict.get(f"kw_char_{kit_id}", 0)
        deaths = stats_dict.get(f"deaths_char_{kit_id}", 0)
        seconds = stats_dict.get(f"tp_char_{kit_id}", 0)
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
                "spawns": stats_dict.get(f"spawns_char_{kit_id}", 0),
                "revives": stats_dict.get(f"revives_char_{kit_id}", 0),
                "assists": stats_dict.get(f"assists_char_{kit_id}", 0),
                "hazardZoneStreaks": stats_dict.get(f"hz_streak_char_{kit_id}", 0),
                "secondsPlayed": seconds,
            }
        )
    return kits


async def get_gamemodes(stats_dict: dict, format_values: bool = False):
    gamemodes = []
    for _id, extra in BF2042.STAT_GAMEMODE.items():
        wins = stats_dict.get(f"wins_gm_{_id}", 0)
        losses = stats_dict.get(f"losses_gm_{_id}", 0)
        kills = stats_dict.get(f"kills_gm_{_id}", 0)
        seconds = stats_dict.get(f"tp_gm_{_id}", 0)
        try:
            kills_per_minute = round(kills / (seconds / 60), 2)
        except (ZeroDivisionError, KeyError):
            kills_per_minute = 0.0
        try:
            win_percent = round(wins / (wins + losses) * 100, 2)
        except ZeroDivisionError:
            win_percent = 0.0

        gamemodes.append(
            {
                **extra,
                "id": _id,
                "kills": kills,
                "assists": stats_dict.get(f"assists_gm_{_id}", 0),
                "revives": stats_dict.get(f"revives_gm_{_id}", 0),
                "bestSquad": stats_dict.get(f"bestsquad_gm_{_id}", 0),
                "wins": wins,
                "losses": losses,
                "mvp": stats_dict.get(f"mvp_gm_{_id}", 0),
                "matches": stats_dict.get(f"matches_gm_{_id}", 0),
                "sectorDefend": stats_dict.get(f"sectordef_gm_{_id}", 0),
                "objectivesArmed": stats_dict.get(f"obj_armed_gm_{_id}", 0),
                "objectivesDisarmed": stats_dict.get(f"obj_disarmed_gm_{_id}", 0),
                "objectivesDefended": stats_dict.get(f"obj_defended_gm_{_id}", 0),
                "objectivesCaptured": stats_dict.get(f"obj_captured_gm_{_id}", 0),
                "objectivesDestroyed": stats_dict.get(f"obj_destroyed_gm_{_id}", 0),
                "objetiveTime": stats_dict.get(f"obj_time_gm_{_id}", 0),
                "kpm": kills_per_minute,
                "winPercent": format_percentage_value(win_percent, format_values),
                "secondsPlayed": seconds,
            }
        )
    return gamemodes


async def get_maps(stats_dict: dict, format_values: bool = False):
    maps = []
    for _id, extra in BF2042.STAT_MAPS.items():
        wins = stats_dict.get(f"wins_lvl_{_id}", 0)
        losses = stats_dict.get(f"losses_lvl_{_id}", 0)
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
                "matches": stats_dict.get(f"matches_lvl_{_id}", 0),
                "winPercent": format_percentage_value(win_percent, format_values),
                "secondsPlayed": stats_dict.get(f"tp_lvl_{_id}", 0),
            }
        )
    return maps


async def get_gadgets(stats_dict: dict):
    gadgets = []
    for _id, extra in BF2042.GADGETS.items():
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
                "spawns": stats_dict.get(f"spawns_gad_{_id}", 0),
                "damage": damage,
                "uses": stats_dict.get(f"uses_gad_{_id}", 0),
                "multiKills": stats_dict.get(f"mkw_gad_{_id}", 0),
                "vehiclesDestroyedWith": stats_dict.get(f"vdw_gad_{_id}", 0),
                "kpm": kills_per_minute,
                "dpm": damage_per_minute,
                "secondsPlayed": seconds,
            }
        )
    return gadgets


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
        "squadmateRespawn": stats_dict.get("Respawns_Squadmates_Total", 0),
        "thrownThrowables": stats_dict.get("thrown_throwables_total", 0),
        "inRound": {
            "revives": stats_dict.get("revives_inround_cb", 0),
            "resupplies": stats_dict.get("resupply_teammates_inround_cb", 0),
            "squadmateRevive": stats_dict.get("revives_squadmates_inround_cb", 0),
            "spotAssists": stats_dict.get("spot_assist_inround_cb", 0),
            "thrownThrowables": stats_dict.get("thrown_throwables_inround_cb", 0),
            "playerTakeDowns": stats_dict.get("players_taken_down_inround_cb", 0),
            "gadgetsDestoyed": stats_dict.get("disable_gadget_inround_cb", 0),
        },
        "gadgetsDestoyed": stats_dict.get("destroy_gadget_total", 0),
        "callIns": stats_dict.get("call_ins_total", 0),
        "playerTakeDowns": (stats_dict.get("Players_Taken_Down_Total", 0)),
        "matchesPlayed": matches_played,
        "secondsPlayed": seconds,
        "dividedSecondsPlayed": {
            "flying": stats_dict.get("flying_time_total", 0),
            "driving": stats_dict.get("driving_time_total", 0),
        },
        "bestSquad": stats_dict.get("best_squad_total", 0),
        "teammatesSupported": stats_dict.get("supported_teammates_total", 0),
        "saviorKills": stats_dict.get("savior_kills_total", 0),
        "shotsFired": shots_fired,
        "shotsHit": shots_hit,
        "killAssists": stats_dict.get("assists_total", 0),
        "vehiclesDestroyed": stats_dict.get("Destroyed_Veh_Total", 0),
        "enemiesSpotted": stats_dict.get("Spotted_Enemies_Total", 0),
        "mvp": stats_dict.get("mvp_total", 0),
        "dividedKills": {
            "ads": stats_dict.get("Kills_ADS_Total", 0),
            "grenades": stats_dict.get("Kills_Grenade_Total", 0),
            "hipfire": stats_dict.get("Kills_Hipfire_Total", 0),
            "longDistance": stats_dict.get("Kills_LongDist_Total", 0),
            "melee": stats_dict.get("Kills_Melee_Total", 0),
            "multiKills": stats_dict.get("Kills_Multi_Total", 0),
            "parachute": stats_dict.get("Kills_Parachute_Total", 0),
            "passenger": stats_dict.get("Kills_Psgr_Total", 0),
            "vehicle": stats_dict.get("Kills_wVeh_Total", 0),
            "roadkills": stats_dict.get("kill_road_total", 0),
            "ai": stats_dict.get("AI_kills_total", 0),
            "human": human_kills,
            "turret": stats_dict.get("kills_turret_total", 0),
            "ranger": stats_dict.get("kills_ranger_total", 0),
            "weapons": {
                "BAR": stats_dict.get("kills_bar_total", 0),
                "SMG": stats_dict.get("kills_smg_total", 0),
                "LMG": stats_dict.get("kills_lmg_total", 0),
                "DMR": stats_dict.get("kills_dmr_total", 0),
                "Sidearm": stats_dict.get("kills_sa_total", 0),
                "Crossbows": stats_dict.get("kills_cb_total", 0),
                "Shotguns": stats_dict.get("kills_sg_total", 0),
                "Assault Rifles": stats_dict.get("kills_sg_total", 0),
            },
            "inRound": {
                "total": stats_dict.get("kills_inround_cb", 0),
                "turret": stats_dict.get("kills_turret_inround_cb", 0),
                "killsAndAssists": stats_dict.get("kills_and_assists_inround_cb", 0),
                "drone": stats_dict.get("kills_drone_inround_cb", 0),
                "grenade": stats_dict.get("kills_grenade_inround_cb", 0),
                "headshots": stats_dict.get("kills_headshots_inround_cb", 0),
                "hipfire": stats_dict.get("kills_hipfire_inround_cb", 0),
                "longDistance": stats_dict.get("kills_longdist_inround_cb", 0),
                "melee": stats_dict.get("kills_melee_inround_cb", 0),
                "multiKills": stats_dict.get("kills_multi_inround_cb", 0),
                "parachute": stats_dict.get("kills_parachute_inround_cb", 0),
                "passenger": stats_dict.get("kills_psgr_inround_cb", 0),
                "weapons": {
                    "Sidearm": stats_dict.get("kills_sa_inround_cb", 0),
                    "BAR": stats_dict.get("kills_bar_inround_cb", 0),
                    "SMG": stats_dict.get("kills_smg_inround_cb", 0),
                    "AR": stats_dict.get("kills_ar_inround_cb", 0),
                    "DMR": stats_dict.get("kills_dmr_inround_cb", 0),
                },
            },
        },
        "devidedDamage": {
            "explosion": stats_dict.get("dmg_expl_total", 0),
            "passenger": stats_dict.get("dmg_psgr_total", 0),
            "vehicleDriver": stats_dict.get("dmg_vehdriver_total", 0),
            "toVehicle": stats_dict.get("dmgto_veh_total", 0),
            "inRound": {
                "passenger": stats_dict.get("dmg_psgr_inround_cb", 0),
                "explosion": stats_dict.get("dmg_expl_inround_cb", 0),
                "toVehicle": stats_dict.get("dmgto_veh_inround_cb", 0),
                "asVehicle": stats_dict.get("dmgwith_veh_inround_cb", 0),
            },
        },
        "devidedAssists": {
            "driver": stats_dict.get("Assists_Driver_Total", 0),
            "passenger": stats_dict.get("Assists_Psgr_Total", 0),
            "spot": stats_dict.get("Assists_Spot_Total", 0),
            "pilot": stats_dict.get("assists_pilot_total", 0),
            "ai": stats_dict.get("AI_assists_total", 0),
            "inRound": {
                "total": stats_dict.get("assist_inround_cb", 0),
                "passenger": stats_dict.get("assists_psgr_inround_cb", 0),
                "pilot": stats_dict.get("assists_pilot_inround_cb", 0),
            },
        },
        "distanceTraveled": {
            "foot": stats_dict.get("distrav_foot_total", 0),
            "grapple": stats_dict.get("distrav_grapple_total", 0),
            "passenger": stats_dict.get("distrav_psgr_total", 0),
            "vehicle": stats_dict.get("distrav_veh_total", 0),
        },
        "sector": {
            "captured": stats_dict.get("sect_cap_total", 0),
            "defended": stats_dict.get("sect_def_total", 0),
        },
        "objective": {
            "time": {
                "total": stats_dict.get("obj_time_total", 0),
                "attacked": stats_dict.get("attobj_time_Total", 0),
                "defended": stats_dict.get("defobj_time_Total", 0),
            },
            "armed": stats_dict.get("obj_arm_total", 0),
            "captured": stats_dict.get("cap_obj_total", 0),
            "neutralized": stats_dict.get("neutralized_obj_total", 0),
            "defused": stats_dict.get("obj_defuse_total", 0),
            "destroyed": stats_dict.get("destroyed_obj_total", 0),
            "inRound": {
                "time": stats_dict.get("obj_time_inround_cb", 0),
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
                "ribbons": {
                    "total": stats_dict.get("xp_ribbons", 0),
                    "squad": stats_dict.get("xp_ribbons_Squad", 0),
                    "combat": stats_dict.get("xp_ribbons_combat", 0),
                    "intel": stats_dict.get("xp_ribbons_intel", 0),
                    "objective": stats_dict.get("xp_ribbons_objective", 0),
                    "support": stats_dict.get("xp_ribbons_support", 0),
                },
            },
        ),
        "squadOrders": {
            "attack": {
                "placed": stats_dict.get("sqorder_attack_placed_total", 0),
                "completed": stats_dict.get("sqorder_attack_comp_total", 0),
            },
            "defence": {
                "placed": stats_dict.get("sqorder_defend_placed_total", 0),
                "completed": stats_dict.get("sqorder_defend_comp_total", 0),
            },
            "placed": stats_dict.get("sqorder_placed_total", 0),
            "completed": stats_dict.get("sqorder_comp_total", 0),
        },
        "intel": {
            "squad": {
                "extracted": stats_dict.get("intel_ext_squad_total", 0),
            },
            "pickup": {
                "squad": stats_dict.get("intel_pickup_squad_total", 0),
                "total": stats_dict.get("intel_pickup_total", 0),
                "gamemodes": {
                    "all": stats_dict.get("intel_pickup_gm_all", 0),
                    "hazardZone": stats_dict.get("intel_pickup_gm_hz", 0),
                },
            },
            "extracted": stats_dict.get("intel_ext_total", 0),
        },
        "seasons": {
            "1": {
                "kills": stats_dict.get("season1_kills", 0),
                "deaths": stats_dict.get("season1_death", 0),
                "wins": stats_dict.get("season1_matches_won", 0),
                "loses": stats_dict.get("season1_rounds_played", 0)
                - stats_dict.get("season1_matches_won", 0),
                "roundsPlayed": stats_dict.get("season1_rounds_played", 0),
                "heals": stats_dict.get("season1_teammate_healed", 0),
                "revives": stats_dict.get("season1_revives", 0),
                "resupplies": stats_dict.get("season1_teammate_resupplied", 0),
                "assists": stats_dict.get("season1_assists", 0),
                "headshots": stats_dict.get("season1_headshot_kills", 0),
                "enemiesSpotted": stats_dict.get("season1_enemies_spotted", 0),
                "vehiclesDestroyed": stats_dict.get("season1_veh_destroyed", 0),
                "ribbons": stats_dict.get("season1_ribbons", 0),
                "objective": {
                    "armed": stats_dict.get("season1_object_armed", 0),
                    "captured": stats_dict.get("season1_object_captured", 0),
                    "defused": stats_dict.get("season1_object_defused", 0),
                    "destroyed": stats_dict.get("season1_object_destroyed", 0),
                    "neutralized": stats_dict.get("season1_object_neutralized", 0),
                },
                "missionsCompleted": stats_dict.get("season1_missions_comp", 0),
                "intelExtracted": stats_dict.get("season1_intel_extracted", 0),
                "timesExtracted": stats_dict.get("season1_times_extracted", 0),
                "vehiclesHPRepaired": stats_dict.get("season1_veh_hp_repaired", 0),
            }
        },
    }


async def get_stats(
    data: dict,
    raw_loadout: dict = {},
    format_values: bool = True,
    multiple: bool = False,
):
    # get the level of each player to their id
    loadouts = {}
    for player in (
        raw_loadout.get("result", {"inventory": {"loadouts": []}})
        .get("inventory", {"loadouts": []})
        .get("loadouts", [])
    ):
        loadouts[player.get("player", {"personaId": 0}).get("personaId", 0)] = (
            player.get("level", 0)
        )

    result = []
    for player in data.get("playerStats", []):
        current_result = {}
        current_player = player.get("player", {"personaId": 0})
        stats_dict = {}
        for category in player.get("categories", []):
            for item in category.get("catFields", {"fields": []}).get("fields", []):
                stats_dict[item["name"]] = item["value"]

        current_result["hasResults"] = len(stats_dict) > 0

        tasks = []
        tasks.append(get_weapons(stats_dict, BF2042.WEAPONS, format_values))
        tasks.append(get_vehicles(stats_dict, BF2042.VEHICLES))
        tasks.append(get_weapons(stats_dict, BF2042.WEAPON_GROUPS, format_values))
        tasks.append(get_vehicles(stats_dict, BF2042.VEHICLE_GROUPS))
        tasks.append(get_classes(stats_dict))
        tasks.append(get_gamemodes(stats_dict, format_values))
        tasks.append(get_maps(stats_dict, format_values))
        tasks.append(get_gadgets(stats_dict))

        if multiple:
            platform_id = current_player.get("platformId", 0)
            current_result["id"] = current_player.get("personaId", 0)
            current_result["userId"] = current_player.get("nucleusId", 0)
            current_result["platform"] = BF2042.STATS_PLATFORM.get(
                current_player.get("platformId", 0), "pc"
            )
            current_result["platformId"] = 0 if platform_id is None else platform_id

        (
            current_result["weapons"],
            current_result["vehicles"],
            current_result["weaponGroups"],
            current_result["vehicleGroups"],
            current_result["classes"],
            current_result["gamemodes"],
            current_result["maps"],
            current_result["gadgets"],
        ) = await asyncio.gather(*tasks)

        kit_best_kills = 0
        best_kit = 0
        for kit in current_result["classes"]:
            if kit["kills"] > kit_best_kills:
                kit_best_kills = kit["kills"]
                best_kit = kit["characterName"]
        current_result["bestClass"] = best_kit

        current_result.update(await get_main_stats(stats_dict, format_values))
        # add fetched level
        current_result["level"] = loadouts.get(current_player.get("personaId", 0), 0)
        result.append(current_result)

    if len(result) < 1:
        raise NotFoundException("player not found")
    if len(result) > 1:
        return {"data": result}
    return result[0]
