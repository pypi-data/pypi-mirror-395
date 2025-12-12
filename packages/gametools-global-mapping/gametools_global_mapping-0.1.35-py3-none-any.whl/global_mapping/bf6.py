SEASONS = {"Season1": "Season 1"}
PLATFORM = {
    0: "unknown",
    1: "pc",
    2: "ps4",
    3: "xboxone",
    4: "ps5",
    5: "xboxseries",
    6: "common",
    7: "steam",
}
STATS_PLATFORM = {
    1: "pc",
    3: "xboxone",
    2: "ps4",
    5: "xboxseries",
    4: "ps5",
    6: "common",
    7: "steam",
}
PLATFORM_REVERSE = {
    "unknown": 0,
    "pc": 1,
    "ps4": 2,
    "xboxone": 3,
    "ps5": 4,
    "xboxseries": 5,
    "common": 6,
    "steam": 7,
}
PLATFORM_FESL = {
    0: "pc",
    1: "pc",
    2: "ps4",
    3: "xboxone",
    4: "ps4",
    5: "xboxone",
    6: "pc",
    7: "pc",
}
STATS_PLATFORM_REVERSE = {
    "pc": 1,
    "xboxone": 3,
    "ps4": 2,
    "xboxseries": 5,
    "ps5": 4,
    "xbox": 5,
    "psn": 4,
    "steam": 7,
}
REGIONS = {
    "aws-hkg": "Asia",
    "aws-icn": "Asia",
    "aws-nrt": "Asia",
    "aws-sin": "Asia",
    "aws-iad": "North America",
    "aws-pdx": "North America",
    "aws-sjc": "North America",
    "aws-brz": "South America",
    "aws-fra": "Europe",
    "aws-lhr": "Europe",
    "aws-syd": "Oceania",
}
REGIONSLIST = {
    "asia": ["aws-hkg", "aws-icn", "aws-nrt", "aws-sin"],
    "nam": ["aws-iad", "aws-pdx", "aws-sjc"],
    "sam": ["aws-brz"],
    "eu": ["aws-fra", "aws-lhr"],
    "oc": ["aws-syd"],
    "all": [
        "aws-iad",
        "aws-pdx",
        "aws-sjc",
        "aws-brz",
        "aws-fra",
        "aws-lhr",
        "aws-hkg",
        "aws-icn",
        "aws-nrt",
        "aws-sin",
        "aws-syd",
    ],
}
SHORT_REGIONS = {
    "aws-hkg": "asia",
    "aws-icn": "asia",
    "aws-nrt": "asia",
    "aws-sin": "asia",
    "aws-iad": "nam",
    "aws-pdx": "nam",
    "aws-sjc": "nam",
    "aws-brz": "sam",
    "aws-fra": "eu",
    "aws-lhr": "eu",
    "aws-syd": "oc",
}
MAPS = {
    "MP_Abbasid": "Siege of Cairo",
    "MP_Aftermath": "Empire State",
    "MP_Battery": "Iberian Offensive",
    "MP_Capstone": "Liberation Peak",
    "MP_Dumbo": "Manhattan Bridge",
    "MP_FireStorm": "Operation Firestorm",
    "MP_Limestone": "Saints Quarter",
    "MP_Outskirts": "New Sobek City",
    "MP_Tungsten": "Mirak Valley",
    "MP_Granite_ClubHouse_Portal": "Club House",
    "MP_Granite_TechCampus_Portal": "Tech Center",
}
TO_GAME_MAPS = {
    "siege of cairo": "MP_Abbasid",
    "empire state": "MP_Aftermath",
    "iberian offensive": "MP_Battery",
    "liberation peak": "MP_Capstone",
    "manhattan bridge": "MP_Dumbo",
    "operation firestorm": "MP_FireStorm",
    "saints quarter": "MP_Limestone",
    "new sobek city": "MP_Outskirts",
    "mirak valley": "MP_Tungsten",
    "club house": "MP_Granite_ClubHouse_Portal",
    "tech center": "MP_Granite_TechCampus_Portal",
}
MAP_TRANSLATION_IDS = {
    "MP_Abbasid": "ID_MP_LVL_ABBASID_NAME",
    "MP_Aftermath": "ID_MP_LVL_AFTERMATH_NAME",
    "MP_Battery": "ID_MP_LVL_BATTERY_NAME",
    "MP_Capstone": "ID_ARRIVAL_MAP_CAPSTONE",
    "MP_Dumbo": "ID_MP_LVL_DUMBO_NAME",
    "MP_FireStorm": "ID_MP_LVL_FIRESTORM_NAME",
    "MP_Limestone": "ID_MP_LVL_LIMESTONE_NAME",
    "MP_Outskirts": "ID_MP_LVL_OUTSKIRTS_NAME",
    "MP_Tungsten": "ID_MP_LVL_TUNGSTEN_NAME",
    "MP_Granite_ClubHouse_Portal": "ID_ARRIVAL_MAP_GRANITE_CLUB_HOUSE",
    "MP_Granite_TechCampus_Portal": "ID_ARRIVAL_MAP_GRANITE_TECH_CENTER",
}
MAP_PICTURES = {
    "MP_Abbasid": "https://cdn.gametools.network/maps/bf6/T_UI_Abbasid_Large_OPT-49a3761a.webp",
    "MP_Aftermath": "https://cdn.gametools.network/maps/bf6/T_UI_Aftermath_Large_OPT-bf883df1.webp",
    "MP_Battery": "https://cdn.gametools.network/maps/bf6/T_UI_Battery_Large_OPT-034d4636.webp",
    "MP_Capstone": "https://cdn.gametools.network/maps/bf6/T_UI_Capstone_Large_OPT-2ccae694.webp",
    "MP_Dumbo": "https://cdn.gametools.network/maps/bf6/T_UI_Dumbo_Large_OPT-20de031f.webp",
    "MP_FireStorm": "https://cdn.gametools.network/maps/bf6/T_UI_Firestorm_Large_OPT-45d582ad.webp",
    "MP_Limestone": "https://cdn.gametools.network/maps/bf6/T_UI_Limestone_Large_OPT-c9160897.webp",
    "MP_Outskirts": "https://cdn.gametools.network/maps/bf6/T_UI_Outskirts_Large_OPT-bf08f756.webp",
    "MP_Tungsten": "https://cdn.gametools.network/maps/bf6/T_UI_Tungsten_Large_OPT-935da06b.webp",
    "MP_Granite_ClubHouse_Portal": "https://cdn.gametools.network/maps/bf6/T_UI_Granite_Portal_05_Thumb_SML-74ea7be7.webp",
    "MP_Granite_TechCampus_Portal": "https://cdn.gametools.network/maps/bf6/T_UI_Granite_Portal_06_Thumb_SML-80099ba6.webp",
}
SMALLMODES = {
    "Breakthrough0": "BT",
    "BreakthroughSmall0": "BS",
    "ConquestSmall0": "CQ",
    "ModBuilderCustom0": "CM",
    "Rush0": "RS",
    "Conquest0": "CL",
    "GraniteDuo0": "RD",
    "GraniteSquad0": "RQ",
    "GraniteGauntlet0": "RG",
}
MODES = {
    "Breakthrough0": "Breakthrough Large",
    "BreakthroughSmall0": "Breakthrough",
    "ConquestSmall0": "Conquest",
    "ModBuilderCustom0": "Custom",
    "Rush0": "Rush",
    "Conquest0": "Conquest large",
    "GraniteDuo0": "Redsec Duos",
    "GraniteSquad0": "Redsec Quads",
    "GraniteGauntlet0": "Redsec Gauntlet",
}
REDSEC_MODES = {
    "GraniteDuo0": "Duos",
    "GraniteSquad0": "Quads",
    "GraniteGauntlet0": "Gauntlet",
}
TO_GAME_MODES = {
    "breakthrough large": "Breakthrough0",
    "breakthrough": "BreakthroughSmall0",
    "conquest": "ConquestSmall0",
    "custom": "ModBuilderCustom0",
    "rush": "Rush0",
    "conquest large": "Conquest0",
    "redsec duos": "GraniteDuo0",
    "redsec quads": "GraniteSquad0",
    "redsec gauntlet": "GraniteGauntlet0",
}
STAT_MAPS = {
    "mpabbasid": {
        "mapName": "Siege of Cairo",
        "image": "https://cdn.gametools.network/maps/bf6/T_UI_Abbasid_Large_OPT-49a3761a.webp",
    },
    "mpaftermath": {
        "mapName": "Empire State",
        "image": "https://cdn.gametools.network/maps/bf6/T_UI_Aftermath_Large_OPT-bf883df1.webp",
    },
    "mpbattery": {
        "mapName": "Iberian Offensive",
        "image": "https://cdn.gametools.network/maps/bf6/T_UI_Battery_Large_OPT-034d4636.webp",
    },
    "mpcapstone": {
        "mapName": "Liberation Peak",
        "image": "https://cdn.gametools.network/maps/bf6/T_UI_Capstone_Large_OPT-2ccae694.webp",
    },
    "mpdumbo": {
        "mapName": "Manhattan Bridge",
        "image": "https://cdn.gametools.network/maps/bf6/T_UI_Dumbo_Large_OPT-20de031f.webp",
    },
    "mpfirestorm": {
        "mapName": "Operation Firestorm",
        "image": "https://cdn.gametools.network/maps/bf6/T_UI_Firestorm_Large_OPT-45d582ad.webp",
    },
    "mplimestone": {
        "mapName": "Saints Quarter",
        "image": "https://cdn.gametools.network/maps/bf6/T_UI_Limestone_Large_OPT-c9160897.webp",
    },
    "mpoutskirts": {
        "mapName": "New Sobek City",
        "image": "https://cdn.gametools.network/maps/bf6/T_UI_Outskirts_Large_OPT-bf08f756.webp",
    },
    "mptungsten": {
        "mapName": "Mirak Valley",
        "image": "https://cdn.gametools.network/maps/bf6/T_UI_Tungsten_Large_OPT-935da06b.webp",
    },
    "mpbadlands": {
        "mapName": "Blackwell Fields",
        "image": "https://cdn.gametools.network/maps/bf6/Battlefield_6_Blackwell_Fields.webp",
    },
    "ftpgranite": {
        "mapName": "REDSEC",
        "image": "https://cdn.gametools.network/maps/bf6/Battlefield_6_Redsec.webp",
    },
}
STAT_GAMEMODE = {
    "MP_Escalation0": {"gamemodeName": "Escalation", "image": ""},
    "MP_TeamDM0": {"gamemodeName": "Team deathmatch", "image": ""},
    "Conquest0": {"gamemodeName": "Conquest", "image": ""},
    "MP_KOTH0": {"gamemodeName": "King of the hill", "image": ""},
    "MP_SquadDM0": {"gamemodeName": "Squad deathmatch", "image": ""},
    "Breakthrough0": {"gamemodeName": "Breakthrough", "image": ""},
    "Rush0": {"gamemodeName": "Rush", "image": ""},
}
CLASSES = {
    "assault": {
        "className": "Assault",
        "image": "https://cdn.gametools.network/classes/bf6/white/Assault.svg",
        "altImage": "https://cdn.gametools.network/classes/bf6/black/Assault.svg",
    },
    "engineer": {
        "className": "Engineer",
        "image": "https://cdn.gametools.network/classes/bf6/white/Engineer.svg",
        "altImage": "https://cdn.gametools.network/classes/bf6/black/Engineer.svg",
    },
    "support": {
        "className": "Support",
        "image": "https://cdn.gametools.network/classes/bf6/white/Support.svg",
        "altImage": "https://cdn.gametools.network/classes/bf6/black/Support.svg",
    },
    "recon": {
        "className": "Recon",
        "image": "https://cdn.gametools.network/classes/bf6/white/Recon.svg",
        "altImage": "https://cdn.gametools.network/classes/bf6/black/Recon.svg",
    },
}
VEHICLES = {
    "air_panthera": {
        "type": "Air Combat",
        "vehicleName": "Panthera KHT",
        "image": "https://cdn.gametools.network/vehicles/bf6/T_UI_MDV_Eurocopter_VSD0001-8003028d.webp",
        "altImage": "https://cdn.gametools.network/vehicles/bf6/white/T_UI_MDV_Eurocopter_VSD0001-8003028d.webp",
    },
    "air_m77efalchio": {
        "type": "Air Combat",
        "vehicleName": "M77E Falchion",
        "image": "https://cdn.gametools.network/vehicles/bf6/T_UI_MDV_AH64E_VSD0001-dd0a7df6.webp",
        "altImage": "https://cdn.gametools.network/vehicles/bf6/white/T_UI_MDV_AH64E_VSD0001-dd0a7df6.webp",
    },
    "sur_leoa4": {
        "type": "Ground Combat",
        "vehicleName": "Leo A4",
        "image": "https://cdn.gametools.network/vehicles/bf6/T_UI_MDV_Leopard_VSD0001-f8da51ee.webp",
        "altImage": "https://cdn.gametools.network/vehicles/bf6/white/T_UI_MDV_Leopard_VSD0001-f8da51ee.webp",
    },
    "sur_strf09a4": {
        "type": "Ground Combat",
        "vehicleName": "Strf 09 A4",
        "image": "https://cdn.gametools.network/vehicles/bf6/T_UI_CV90_VSD0001-acd942b6.webp",
        "altImage": "https://cdn.gametools.network/vehicles/bf6/white/T_UI_CV90_VSD0001-acd942b6.webp",
    },
    "sur_m1a2sepv3": {
        "type": "Ground Combat",
        "vehicleName": "M1A2 SEPv3",
        "image": "https://cdn.gametools.network/vehicles/bf6/T_UI_MDV_Abrams_VSD0001-5412a78d.webp",
        "altImage": "https://cdn.gametools.network/vehicles/bf6/white/T_UI_MDV_Abrams_VSD0001-5412a78d.webp",
    },
    "sur_cheetah1a2": {
        "type": "Ground Combat",
        "vehicleName": "Cheetah 1A2",
        "image": "https://cdn.gametools.network/vehicles/bf6/T_UI_MDV_Gepard_VSD0001-d796732f.webp",
        "altImage": "https://cdn.gametools.network/vehicles/bf6/white/T_UI_MDV_Gepard_VSD0001-d796732f.webp",
    },
    "sur_glider96": {
        "type": "Ground Combat",
        "vehicleName": "Glider 96",
        "image": "https://cdn.gametools.network/vehicles/bf6/T_UI_MDV_Flyer60_VSD0005-1569869f.webp",
        "altImage": "https://cdn.gametools.network/vehicles/bf6/white/T_UI_MDV_Flyer60_VSD0005-1569869f.webp",
    },
    "sur_bradley": {
        "type": "Ground Combat",
        "vehicleName": "M3A3 Bradley",
        "image": "https://cdn.gametools.network/vehicles/bf6/T_UI_OB_VEH_Tank_Bradley_VSD0001_Dressing-66f252ca.webp",
        "altImage": "https://cdn.gametools.network/vehicles/bf6/white/T_UI_OB_VEH_Tank_Bradley_VSD0001_Dressing-66f252ca.webp",
    },
    "air_su57": {
        "type": "Air Combat",
        "vehicleName": "Su-57",
        "image": "https://cdn.gametools.network/vehicles/bf6/T_UI_MDV_SU57_VSD0001-1b5aa5ee.webp",
        "altImage": "https://cdn.gametools.network/vehicles/bf6/white/T_UI_MDV_SU57_VSD0001-1b5aa5ee.webp",
    },
    "air_f61v": {
        "type": "Air Combat",
        "vehicleName": "F-61V",
        "image": "https://cdn.gametools.network/vehicles/bf6/T_UI_MDV_F16_VSD0001-5f951ec9.webp",
        "altImage": "https://cdn.gametools.network/vehicles/bf6/white/T_UI_MDV_F16_VSD0001-5f951ec9.webp",
    },
    "air_f39e": {
        "type": "Air Combat",
        "vehicleName": "F-39E",
        "image": "https://cdn.gametools.network/vehicles/bf6/T_UI_MDV_JAS39_VSD0001-9313d717.webp",
        "altImage": "https://cdn.gametools.network/vehicles/bf6/white/T_UI_MDV_JAS39_VSD0001-9313d717.webp",
    },
    "air_m77efalchion": {
        "type": "Air Combat",
        "vehicleName": "M77E Falchion",
        "image": "https://cdn.gametools.network/vehicles/bf6/T_UI_MDV_AH64E_VSD0001-dd0a7df6.webp",
        "altImage": "https://cdn.gametools.network/vehicles/bf6/white/T_UI_MDV_AH64E_VSD0001-dd0a7df6.webp",
    },
    "sur_vector": {
        "type": "Ground Transport",
        "vehicleName": "VECTOR",
        "image": "https://cdn.gametools.network/vehicles/bf6/T_UI_MDV_Vector_VSD0002-241efa80.webp",
    },
}
VEHICLE_GROUPS = {
    "air": {"groupName": "Air Combat"},
    "sur": {"groupName": "Ground Combat"},
}
WEAPONS = {
    "mg_l110": {
        "type": "Machine Guns",
        "weaponName": "L110",
        "image": "https://cdn.gametools.network/weapons/bf6/T_UI_Minimi_PKG_Factory_MED-0e29fce7.webp",
        "altImage": "https://cdn.gametools.network/weapons/bf6/white/T_UI_Minimi_PKG_Factory_MED-0e29fce7.webp",
    },
    "smg_pw5a3": {
        "type": "SMG-PDWs",
        "weaponName": "PW5A3",
        "image": "https://cdn.gametools.network/weapons/bf6/T_UI_MP5MLI_PKG_Factory_MED-2d1944b7.webp",
        "altImage": "https://cdn.gametools.network/weapons/bf6/white/T_UI_MP5MLI_PKG_Factory_MED-2d1944b7.webp",
    },
    "ar_m433": {
        "type": "Assault Rifles",
        "weaponName": "M433",
        "image": "https://cdn.gametools.network/weapons/bf6/T_UI_HK433_PKG_Factory_MED-b06f02f7.webp",
        "altImage": "https://cdn.gametools.network/weapons/bf6/white/T_UI_HK433_PKG_Factory_MED-b06f02f7.webp",
    },
    "mg_rpkm": {
        "type": "Machine Guns",
        "weaponName": "RPKM",
        "image": "https://cdn.gametools.network/weapons/bf6/T_UI_RPKM_PKG_Factory_MED-755b785f.webp",
        "altImage": "https://cdn.gametools.network/weapons/bf6/white/T_UI_RPKM_PKG_Factory_MED-755b785f.webp",
    },
    "sg_m87a1": {
        "type": "Shotguns",
        "weaponName": "M87A1",
        "image": "https://cdn.gametools.network/weapons/bf6/T_UI_590A1_PKG_Factory_MED-4b387330.webp",
        "altImage": "https://cdn.gametools.network/weapons/bf6/white/T_UI_590A1_PKG_Factory_MED-4b387330.webp",
    },
    "pst_p18": {
        "type": "Pistols",
        "weaponName": "P18",
        "image": "https://cdn.gametools.network/weapons/bf6/T_UI_M18_PKG_Factory_MED-88261bf8.webp",
        "altImage": "https://cdn.gametools.network/weapons/bf6/white/T_UI_M18_PKG_Factory_MED-88261bf8.webp",
    },
    "crb_x277": {
        "type": "Carbines",
        "weaponName": "M277",
        "image": "https://cdn.gametools.network/weapons/bf6/T_UI_XM7_PKG_Factory_MED-26271094.webp",
        "altImage": "https://cdn.gametools.network/weapons/bf6/white/T_UI_XM7_PKG_Factory_MED-26271094.webp",
    },
    "ar_b36a4": {
        "type": "Assault Rifles",
        "weaponName": "B36A4",
        "image": "https://cdn.gametools.network/weapons/bf6/T_UI_G36_PKG_Factory_MED-fb5466ec.webp",
        "altImage": "https://cdn.gametools.network/weapons/bf6/white/T_UI_G36_PKG_Factory_MED-fb5466ec.webp",
    },
    "ar_l85a3": {
        "type": "Assault Rifles",
        "weaponName": "L85A3",
        "image": "https://cdn.gametools.network/weapons/bf6/T_UI_L85A3_PKG_Factory_MED-9bd0deaa.webp",
        "altImage": "https://cdn.gametools.network/weapons/bf6/white/T_UI_L85A3_PKG_Factory_MED-9bd0deaa.webp",
    },
    "snp_m2010": {
        "type": "Rifles",
        "weaponName": "M2010 ESR",
        "image": "https://cdn.gametools.network/weapons/bf6/T_UI_M2010ESR_PKG_Factory_MED-f94fdae6.webp",
        "altImage": "https://cdn.gametools.network/weapons/bf6/white/T_UI_M2010ESR_PKG_Factory_MED-f94fdae6.webp",
    },
    "sg_m1014": {
        "type": "Shotguns",
        "weaponName": "M1014",
        "image": "https://cdn.gametools.network/weapons/bf6/T_UI_M1014_PKG_Factory_MED-e011854a.webp",
        "altImage": "https://cdn.gametools.network/weapons/bf6/white/T_UI_M1014_PKG_Factory_MED-e011854a.webp",
    },
    "crb_ak205": {
        "type": "Carbines",
        "weaponName": "AK-205",
        "image": "https://cdn.gametools.network/weapons/bf6/T_UI_AK205_PKG_Factory_MED-6d376081.webp",
        "altImage": "https://cdn.gametools.network/weapons/bf6/white/T_UI_AK205_PKG_Factory_MED-6d376081.webp",
    },
    "dmr_svk86": {
        "type": "DMRs",
        "weaponName": "SVK-8.6",
        "image": "https://cdn.gametools.network/weapons/bf6/T_UI_SVCh_PKG_Factory_MED-bb06d385.webp",
        "altImage": "https://cdn.gametools.network/weapons/bf6/white/T_UI_SVCh_PKG_Factory_MED-bb06d385.webp",
    },
    "smg_sgx": {
        "type": "SMG-PDWs",
        "weaponName": "SGX",
        "image": "https://cdn.gametools.network/weapons/bf6/T_UI_MPX_PKG_Factory_MED-e822f017.webp",
        "altImage": "https://cdn.gametools.network/weapons/bf6/white/T_UI_MPX_PKG_Factory_MED-e822f017.webp",
    },
    "dmr_lmr27": {
        "type": "DMRs",
        "weaponName": "LMR27",
        "image": "https://cdn.gametools.network/weapons/bf6/T_UI_ARADMR_PKG_Factory_MED-dfe224de.webp",
        "altImage": "https://cdn.gametools.network/weapons/bf6/white/T_UI_ARADMR_PKG_Factory_MED-dfe224de.webp",
    },
    "crb_qbz192": {
        "type": "Carbines",
        "weaponName": "QBZ-192",
        "image": "https://cdn.gametools.network/weapons/bf6/T_UI_QBZ192_PKG_Factory_MED-dc0a546b.webp",
        "altImage": "https://cdn.gametools.network/weapons/bf6/white/T_UI_QBZ192_PKG_Factory_MED-dc0a546b.webp",
    },
    "crb_m417a2": {
        "type": "Carbines",
        "weaponName": "M417 A2",
        "image": "https://cdn.gametools.network/weapons/bf6/T_UI_HK417A2_PKG_Factory_MED-494ffe6e.webp",
        "altImage": "https://cdn.gametools.network/weapons/bf6/white/T_UI_HK417A2_PKG_Factory_MED-494ffe6e.webp",
    },
    "mg_drsiar": {
        "type": "Machine Guns",
        "weaponName": "DRS-IAR",
        "image": "https://cdn.gametools.network/weapons/bf6/T_UI_M27IAR_PKG_Factory_MED-ae6675cd.webp",
        "altImage": "https://cdn.gametools.network/weapons/bf6/white/T_UI_M27IAR_PKG_Factory_MED-ae6675cd.webp",
    },
    "ar_kord6p67": {
        "type": "Assault Rifles",
        "weaponName": "KORD 6P67",
        "image": "https://cdn.gametools.network/weapons/bf6/T_UI_6P67_PKG_Factory_MED-827b9414.webp",
        "altImage": "https://cdn.gametools.network/weapons/bf6/white/T_UI_6P67_PKG_Factory_MED-827b9414.webp",
    },
    "smg_usg90": {
        "type": "SMG-PDWs",
        "weaponName": "USG-90",
        "image": "https://cdn.gametools.network/weapons/bf6/T_UI_P90_PKG_Factory_MED-2ab1db64.webp",
        "altImage": "https://cdn.gametools.network/weapons/bf6/white/T_UI_P90_PKG_Factory_MED-2ab1db64.webp",
    },
    "crb_m4a1": {
        "type": "Carbines",
        "weaponName": "M4A1",
        "image": "https://cdn.gametools.network/weapons/bf6/T_UI_M4A1_PKG_Factory_MED-34529a82.webp",
        "altImage": "https://cdn.gametools.network/weapons/bf6/white/T_UI_M4A1_PKG_Factory_MED-34529a82.webp",
    },
    "mg_kts100mk8": {
        "type": "Machine Guns",
        "weaponName": "KTS100 MK8",
        "image": "https://cdn.gametools.network/weapons/bf6/T_UI_Ultimax_PKG_Factory_MED-a8ebb482.webp",
        "altImage": "https://cdn.gametools.network/weapons/bf6/white/T_UI_Ultimax_PKG_Factory_MED-a8ebb482.webp",
    },
    "pst_m45a1": {
        "type": "Pistols",
        "weaponName": "M45A1",
        "image": "https://cdn.gametools.network/weapons/bf6/T_UI_M45A1_PKG_Factory_MED-8c41691b.webp",
        "altImage": "https://cdn.gametools.network/weapons/bf6/white/T_UI_M45A1_PKG_Factory_MED-8c41691b.webp",
    },
    "smg_kv9": {
        "type": "SMG-PDWs",
        "weaponName": "KV9",
        "image": "https://cdn.gametools.network/weapons/bf6/T_UI_Vector_PKG_Factory_MED-b5631ed7.webp",
        "altImage": "https://cdn.gametools.network/weapons/bf6/white/T_UI_Vector_PKG_Factory_MED-b5631ed7.webp",
    },
    "ar_sor556mk2": {
        "type": "Assault Rifles",
        "weaponName": "SOR-556 Mk2",
        "image": "https://cdn.gametools.network/weapons/bf6/T_UI_SCARL_PKG_Factory_MED-b44467bb.webp",
        "altImage": "https://cdn.gametools.network/weapons/bf6/white/T_UI_SCARL_PKG_Factory_MED-b44467bb.webp",
    },
    "smg_pw7a2": {
        "type": "SMG-PDWs",
        "weaponName": "PW7A2",
        "image": "https://cdn.gametools.network/weapons/bf6/T_UI_MP7A2_PKG_Factory_MED-406bc965.webp",
        "altImage": "https://cdn.gametools.network/weapons/bf6/white/T_UI_MP7A2_PKG_Factory_MED-406bc965.webp",
    },
    "mg_m123k": {
        "type": "Machine Guns",
        "weaponName": "M123K",
        "image": "https://cdn.gametools.network/weapons/bf6/T_UI_MG4K_PKG_Factory_MED-cc064690.webp",
        "altImage": "https://cdn.gametools.network/weapons/bf6/white/T_UI_MG4K_PKG_Factory_MED-cc064690.webp",
    },
    "pst_m44": {
        "type": "Pistols",
        "weaponName": "M44",
        "image": "https://cdn.gametools.network/weapons/bf6/T_UI_RagingHunter_PKG_Factory_MED-f9773307.webp",
        "altImage": "https://cdn.gametools.network/weapons/bf6/white/T_UI_RagingHunter_PKG_Factory_MED-f9773307.webp",
    },
    "mg_xm250": {
        "type": "Machine Guns",
        "weaponName": "M250",
        "image": "https://cdn.gametools.network/weapons/bf6/T_UI_M250_PKG_Factory_MED-6e230a71.webp",
        "altImage": "https://cdn.gametools.network/weapons/bf6/white/T_UI_M250_PKG_Factory_MED-6e230a71.webp",
    },
    "smg_umg40": {
        "type": "SMG-PDWs",
        "weaponName": "UMG-40",
        "image": "https://cdn.gametools.network/weapons/bf6/T_UI_UMP40_PKG_Factory_MED-22afa646.webp",
        "altImage": "https://cdn.gametools.network/weapons/bf6/white/T_UI_UMP40_PKG_Factory_MED-22afa646.webp",
    },
    "ar_tr7": {
        "type": "Assault Rifles",
        "weaponName": "TR-7",
        "image": "https://cdn.gametools.network/weapons/bf6/T_UI_Tavor7_PKG_Factory_MED-e682f267.webp",
        "altImage": "https://cdn.gametools.network/weapons/bf6/white/T_UI_Tavor7_PKG_Factory_MED-e682f267.webp",
    },
    "smg_sl9": {
        "type": "SMG-PDWs",
        "weaponName": "SL9",
        "image": "https://cdn.gametools.network/weapons/bf6/T_UI_APDW_PKG_Factory_MED-c4d1b829.webp",
        "altImage": "https://cdn.gametools.network/weapons/bf6/white/T_UI_APDW_PKG_Factory_MED-c4d1b829.webp",
    },
    "mg_m240l": {
        "type": "Machine Guns",
        "weaponName": "M240L",
        "image": "https://cdn.gametools.network/weapons/bf6/T_UI_M240L_PKG_Factory_MED-1fa18e0c.webp",
        "altImage": "https://cdn.gametools.network/weapons/bf6/white/T_UI_M240L_PKG_Factory_MED-1fa18e0c.webp",
    },
    "smg_scw10": {
        "type": "SMG-PDWs",
        "weaponName": "SCW-10",
        "image": "https://cdn.gametools.network/weapons/bf6/T_UI_APC10_PKG_Factory_MED-716a97fb.webp",
        "altImage": "https://cdn.gametools.network/weapons/bf6/white/T_UI_APC10_PKG_Factory_MED-716a97fb.webp",
    },
    "ar_nvo228e": {
        "type": "Assault Rifles",
        "weaponName": "NVO-228E",
        "image": "https://cdn.gametools.network/weapons/bf6/T_UI_ACE32_PKG_Factory_MED-39a97220.webp",
        "altImage": "https://cdn.gametools.network/weapons/bf6/white/T_UI_ACE32_PKG_Factory_MED-39a97220.webp",
    },
    "mg_m60": {
        "type": "Machine Guns",
        "weaponName": "M/60",
        "image": "https://cdn.gametools.network/weapons/bf6/T_UI_M60E6_PKG_Factory_MED-e600bb28.webp",
        "altImage": "https://cdn.gametools.network/weapons/bf6/white/T_UI_M60E6_PKG_Factory_MED-e600bb28.webp",
    },
    "snp_psr": {
        "type": "Rifles",
        "weaponName": "PSR",
        "image": "https://cdn.gametools.network/weapons/bf6/T_UI_MRAD_PKG_Factory_MED-5035ce99.webp",
        "altImage": "https://cdn.gametools.network/weapons/bf6/white/T_UI_MRAD_PKG_Factory_MED-5035ce99.webp",
    },
    "dmr_svdm": {
        "type": "DMRs",
        "weaponName": "SVDM",
        "image": "https://cdn.gametools.network/weapons/bf6/T_UI_SVDM_PKG_Factory_MED-b6c9aa50.webp",
        "altImage": "https://cdn.gametools.network/weapons/bf6/white/T_UI_SVDM_PKG_Factory_MED-b6c9aa50.webp",
    },
    "ar_ak4d": {
        "type": "Assault Rifles",
        "weaponName": "AK4D",
        "image": "https://cdn.gametools.network/weapons/bf6/T_UI_G3A4_PKG_Factory_MED-0575cf00.webp",
        "altImage": "https://cdn.gametools.network/weapons/bf6/white/T_UI_G3A4_PKG_Factory_MED-0575cf00.webp",
    },
    "crb_sor300sc": {
        "type": "Carbines",
        "weaponName": "SOR-300SC",
        "image": "https://cdn.gametools.network/weapons/bf6/T_UI_SCARSC_PKG_Factory_MED-7a6a50ff.webp",
        "altImage": "https://cdn.gametools.network/weapons/bf6/white/T_UI_SCARSC_PKG_Factory_MED-7a6a50ff.webp",
    },
    "crb_sg553r": {
        "type": "Carbines",
        "weaponName": "SG 553R",
        "image": "https://cdn.gametools.network/weapons/bf6/T_UI_SIG553R_PKG_Factory_MED-afc2dfa8.webp",
        "altImage": "https://cdn.gametools.network/weapons/bf6/white/T_UI_SIG553R_PKG_Factory_MED-afc2dfa8.webp",
    },
    "crb_grtbc": {
        "type": "Carbines",
        "weaponName": "GRT-BC",
        "image": "https://cdn.gametools.network/weapons/bf6/T_UI_MSBSGROTB_PKG_Factory_MED-25acf006.webp",
        "altImage": "https://cdn.gametools.network/weapons/bf6/white/T_UI_MSBSGROTB_PKG_Factory_MED-25acf006.webp",
    },
    "sg_185ksk": {
        "type": "Shotguns",
        "weaponName": "18.5KS-K",
        "image": "https://cdn.gametools.network/weapons/bf6/T_UI_185KSK_PKG_Factory_MED-432c353f.webp",
        "altImage": "https://cdn.gametools.network/weapons/bf6/white/T_UI_MSBSGROTB_PKG_Factory_MED-25acf006.webp",
    },
    "pst_es57": {
        "type": "Pistols",
        "weaponName": "ES 5.7",
        "image": "https://cdn.gametools.network/weapons/bf6/T_UI_M18_PKG_Factory_MED-88261bf8.webp",  # incorrect image!
    },
    "dmr_m39emr": {
        "type": "DMRs",
        "weaponName": "M39 EMR",
        "image": "https://cdn.gametools.network/weapons/bf6/T_UI_SVCh_PKG_Factory_MED-bb06d385.webp",  # incorrect image!
    },
    "snp_sv98": {
        "type": "Rifles",
        "weaponName": "SV-98",
        "image": "https://cdn.gametools.network/weapons/bf6/T_UI_M2010ESR_PKG_Factory_MED-f94fdae6.webp",  # incorrect image!
    },
}
WEAPON_GROUPS = {
    "snp": {"groupName": "Rifles"},
    "crb": {"groupName": "Carbines"},
    "mg": {"groupName": "Machine Guns"},
    "sg": {"groupName": "Shotguns"},
    "ar": {"groupName": "Assault Rifles"},
    "smg": {"groupName": "SMG-PDWs"},
    "dmr": {"groupName": "DMRs"},
}
GADGETS = {
    "callin_airstrike": {
        "type": "Strike Packages",
        "gadgetName": "Air Strike",
        "image": "https://cdn.gametools.network/gadgets/bf6/T_UI_CALLINS_Airstrike_Thumb-638b4ee1.png",
    }
}
