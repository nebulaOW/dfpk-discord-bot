import discord
import os
import re
import datetime
from dotenv import load_dotenv
from discord.ext import commands
from pymongo import MongoClient
from mongosanitizer.sanitizer import sanitize

intents = discord.Intents.default()
intents.messages = True

# dotenv setup
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DB_CONNECTION = os.getenv("DB_CONNECTION")

# Discord bot setup
help_command = commands.DefaultHelpCommand(no_category="Commands")
bot = commands.Bot(command_prefix="/", help_command=help_command)

# MongoDB setup
cluster = MongoClient(DB_CONNECTION)
MapData = cluster["MapData"]["MapData"]  # database
WorldRecords = cluster["WorldRecords"]["WorldRecords"]


# Map names | CUSTOMIZE ACCEPTABLE NAMES
Ayutthaya = ["ayutthaya"]
BlackForest = ["blackforest", "bf"]
BlizzardWorld = ["blizz", "bw", "blizzardworld", "blizzworld"]
Busan = ["busan"]
Castillo = ["castillo"]
ChateauGuillard = ["chateauguillard", "chateau", "guillard"]
Dorado = ["dorado"]
Eichenwald = ["eichenwald", "eich", "eichen"]
Hanamura = ["hanamura", "hana"]
Havana = ["havana"]
Hollywood = ["hollywood", "holly"]
HorizonLunarColony = ["horizon", "hlc", "horizonlunarcolony"]
Ilios = ["ilios"]
Junkertown = ["junkertown"]
LijiangTower = ["lijiang", "lijiangtower"]
Necropolis = ["necropolis"]
Nepal = ["nepal"]
Numbani = ["numbani"]
Oasis = ["oasis"]
Paris = ["paris"]
Rialto = ["rialto"]
Route66 = ["route66", "r66"]
TempleOfAnubis = ["templeofanubis", "anubis"]
VolskayaIndustries = ["volskayaindustries", "volskaya"]
WatchpointGibraltar = ["watchpointgibraltar", "gibraltar"]
KingsRow = ["kingsrow", "kr"]
Petra = ["petra"]
EcopointAntarctica = ["ecopointantarctica", "ecopoint", "antarctica"]
Kanezaka = ["kanezaka", "kz", "kane", "zaka"]
WorkshopChamber = ["workshopchamber", "chamber"]
WorkshopExpanse = ["workshopexpanse", "expanse"]
WorkshopGreenScreen = ["workshopgreenscreen", "green", "greenscreen"]
WorkshopIsland = ["workshopisland", "island"]

# combined map names
long_list_of_map_names = [
    Ayutthaya,
    BlackForest,
    BlizzardWorld,
    Busan,
    Castillo,
    ChateauGuillard,
    Dorado,
    Eichenwald,
    Hanamura,
    Havana,
    Hollywood,
    HorizonLunarColony,
    Ilios,
    Junkertown,
    LijiangTower,
    Necropolis,
    Nepal,
    Numbani,
    Oasis,
    Numbani,
    Oasis,
    Paris,
    Rialto,
    Route66,
    TempleOfAnubis,
    VolskayaIndustries,
    WatchpointGibraltar,
    KingsRow,
    Petra,
    EcopointAntarctica,
    Kanezaka,
    WorkshopChamber,
    WorkshopExpanse,
    WorkshopGreenScreen,
    WorkshopIsland,
]

"""
CUSTOMIZE MAP TYPES AND MOD ROLES HERE
"""

types_of_map = ["multi", "pio"]
role_whitelist = ["Mod", "Tester", "dfpk_bot"]


"""
CUSTOMIZE DISCORD CHANNEL ID NUMBERS HERE
"""


def is_map_channel():
    async def predicate(ctx):
        return ctx.channel.id == 802362144506511400

    return commands.check(predicate)


def is_record_channel():
    async def predicate(ctx):
        return ctx.channel.id == 801496775390527548

    return commands.check(predicate)


def is_map_submit_channel():
    async def predicate(ctx):
        return ctx.channel.id == 802624308726726707

    return commands.check(predicate)


"""
Utilities
"""
time_regex = re.compile(r"(?<!.)(\d{1,2})?:?(\d{2})?:?(?<!\d)(\d{1,2})\.?\d{1,2}?(?!.)")  # noqa: E501


def is_time_format(s):
    return bool(time_regex.match(s))


def date_func(s):
    if s.count(":") == 0 and s.count(".") == 0:
        return datetime.datetime.strptime(s, "%S").time()
    elif s.count(":") == 0 and s.count(".") == 1:
        return datetime.datetime.strptime(s, "%S.%f").time()
    elif s.count(":") == 1 and s.count(".") == 1:
        return datetime.datetime.strptime(s, "%M:%S.%f").time()
    elif s.count(":") == 1 and s.count(".") == 0:
        return datetime.datetime.strptime(s, "%M:%S").time()
    elif s.count(":") == 2 and s.count(".") == 1:
        return datetime.datetime.strptime(s, "%H:%M:%S.%f").time()
    elif s.count(":") == 2 and s.count(".") == 0:
        return datetime.datetime.strptime(s, "%H:%M:%S").time()


def isEnglish(s):
    return s.isascii()


def map_name_converter(map_name):
    if map_name in Ayutthaya:
        return "ayutthaya"
    elif map_name in BlizzardWorld:
        return "blizzardworld"
    elif map_name in Busan:
        return "busan"
    elif map_name in Castillo:
        return "castillo"
    elif map_name in ChateauGuillard:
        return "chateauguillard"
    elif map_name in Dorado:
        return "dorado"
    elif map_name in Eichenwald:
        return "eichenwald"
    elif map_name in Hanamura:
        return "hanamura"
    elif map_name in Havana:
        return "havana"
    elif map_name in Hollywood:
        return "hollywood"
    elif map_name in HorizonLunarColony:
        return "horizonlunarcolony"
    elif map_name in Ilios:
        return "ilios"
    elif map_name in Junkertown:
        return "junkertown"
    elif map_name in LijiangTower:
        return "lijiangtower"
    elif map_name in Necropolis:
        return "necropolis"
    elif map_name in Nepal:
        return "nepal"
    elif map_name in Numbani:
        return "numbani"
    elif map_name in Oasis:
        return "oasis"
    elif map_name in Paris:
        return "paris"
    elif map_name in Rialto:
        return "rialto"
    elif map_name in Route66:
        return "route66"
    elif map_name in TempleOfAnubis:
        return "templeofanubis"
    elif map_name in VolskayaIndustries:
        return "volskayaindustries"
    elif map_name in WatchpointGibraltar:
        return "watchpointgibraltar"
    elif map_name in KingsRow:
        return "kingsrow"
    elif map_name in EcopointAntarctica:
        return "ecopointantarctica"
    elif map_name in Petra:
        return "petra"
    elif map_name in Kanezaka:
        return "kanezaka"
    elif map_name in WorkshopChamber:
        return "workshopchamber"
    elif map_name in WorkshopExpanse:
        return "workshopexpanse"
    elif map_name in WorkshopGreenScreen:
        return "workshopgreenscreen"
    elif map_name in WorkshopIsland:
        return "workshopisland"


"""
Basic bot startup / error checking
"""


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing required arguments, try again.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Bad arguments, try again.")


"""
MAP CODES - SUBMISSIONS, DELETIONS
"""


# Submit map codes
@bot.command(
    help=("Submit map code with optional description.\n\n"
          "WARNING: If multiple entries for <creator>,"
          " wrap both in a single set of quotation marks!\n"
          "example: \"name1 & name2\"\n\n<type> can be multi or pio\n"
          "[desc] is optional, no need to wrap in quotation marks."
          " Use this to add # of levels, checkpoints, etc."),
    brief="Submit map code",
)
@is_map_submit_channel()
async def submitmap(ctx, map_code, map_name, type, creator, *, desc=""):
    if not isEnglish(map_code):
        await ctx.channel.send(("Only letters A-Z and "
                                "numbers 0-9 allowed in <map_code>"))
        return
    sanitize(map_code)
    sanitize(map_name)
    sanitize(creator)
    sanitize(type)
    sanitize(desc)

    map_code = map_code.upper()
    map_name = map_name.lower()
    type = type.lower()

    if (
        MapData.count_documents({"_id": map_code}) == 0
        and type in types_of_map
        and any(map_name in sublist for sublist in long_list_of_map_names)
    ):
        new_map_name = map_name_converter(map_name)
        new_submission = {
            "_id": map_code,
            "creator": creator,
            "map_name": new_map_name,
            "desc": desc,
            "posted_by": ctx.author.id,
            "type": type,
        }
        MapData.insert_one(new_submission)
        await ctx.channel.send(
            ("Map submission accepted:\n"
             f"{map_code} - {map_name} {type} {desc} - Created by {creator}")
        )
    else:
        await ctx.channel.send("Map submission rejected.")


# Delete map code
@bot.command(
    help="Delete map code",
    brief="Delete map code",
)
@is_map_submit_channel()
async def deletemap(ctx, map_code):
    sanitize(map_code)
    map_code = map_code.upper()
    if MapData.count_documents({"_id": map_code}) == 1 and (
        MapData.find_one({"_id": map_code})["posted_by"] == ctx.author.id
        or any(role in ctx.author.roles for role in role_whitelist)
    ):
        MapData.delete_one({"_id": map_code})
        await ctx.channel.send(f"Map deleted:\n{map_code}")
    else:
        await ctx.channel.send("Map was not deleted.")


# View Maps commands
@bot.command(aliases=["bf"])
@is_map_channel()
async def blackforest(ctx, type=""):
    type = type.lower()
    post = "Black Forest\n"
    type.lower()
    for entry in MapData.find(
        {"map_name": "blackforest", "type": type}
        if type in types_of_map
        else {"map_name": "blackforest"}
    ):
        post += (f"{entry['_id']} - {entry['type']} {entry['desc']}"
                 f" - Created by {entry['creator']}\n")

    if post.count("\n") > 1:
        await ctx.send(post)
    else:
        await ctx.send("No codes for Black Forest!")


"""
MAP CODES - VIEWING SPECIFIC MAPS
"""


@bot.command()
@is_map_channel()
async def ayutthaya(ctx, type=""):
    post = "Ayutthaya\n"
    type.lower()
    for entry in MapData.find(
        {"map_name": "ayutthaya", "type": type}
        if type in types_of_map
        else {"map_name": "ayutthaya"}
    ):
        post += (f"{entry['_id']} - {entry['type']} {entry['desc']}"
                 f" - Created by {entry['creator']}\n")
    if post.count("\n") > 1:
        await ctx.send(post)
    else:
        await ctx.send("No codes for Ayutthaya!")


@bot.command(aliases=["blizz", "bw", "blizzworld"])
@is_map_channel()
async def blizzardworld(ctx, type=""):
    post = "Blizzard World\n"
    type.lower()
    for entry in MapData.find(
        {"map_name": "blizzardworld", "type": type}
        if type in types_of_map
        else {"map_name": "blizzardworld"}
    ):
        post += (f"{entry['_id']} - {entry['type']} {entry['desc']}"
                 f" - Created by {entry['creator']}\n")
    if post.count("\n") > 1:
        await ctx.send(post)
    else:
        await ctx.send("No codes for Blizzard World!")


@bot.command()
@is_map_channel()
async def busan(ctx, type=""):
    post = "Busan\n"
    type.lower()
    for entry in MapData.find(
        {"map_name": "busan", "type": type}
        if type in types_of_map
        else {"map_name": "busan"}
    ):
        post += (f"{entry['_id']} - {entry['type']} {entry['desc']}"
                 f" - Created by {entry['creator']}\n")
    if post.count("\n") > 1:
        await ctx.send(post)
    else:
        await ctx.send("No codes for Busan!")


@bot.command()
@is_map_channel()
async def castillo(ctx, type=""):
    post = "Castillo\n"
    type.lower()
    for entry in MapData.find(
        {"map_name": "castillo", "type": type}
        if type in types_of_map
        else {"map_name": "castillo"}
    ):
        post += (f"{entry['_id']} - {entry['type']} {entry['desc']}"
                 f" - Created by {entry['creator']}\n")
    if post.count("\n") > 1:
        await ctx.send(post)
    else:
        await ctx.send("No codes for Castillo!")


@bot.command(aliases=["chateau", "guillard"])
@is_map_channel()
async def chateauguillard(ctx, type=""):
    post = "Chateau Guillard\n"
    type.lower()
    for entry in MapData.find(
        {"map_name": "chateauguillard", "type": type}
        if type in types_of_map
        else {"map_name": "chateauguillard"}
    ):
        post += (f"{entry['_id']} - {entry['type']} {entry['desc']}"
                 f" - Created by {entry['creator']}\n")
    if post.count("\n") > 1:
        await ctx.send(post)
    else:
        await ctx.send("No codes for Chateau Guillard!")


@bot.command()
@is_map_channel()
async def dorado(ctx, type=""):
    post = "Dorado\n"
    type.lower()
    for entry in MapData.find(
        {"map_name": "dorado", "type": type}
        if type in types_of_map
        else {"map_name": "dorado"}
    ):
        post += (f"{entry['_id']} - {entry['type']} {entry['desc']}"
                 f" - Created by {entry['creator']}\n")
    if post.count("\n") > 1:
        await ctx.send(post)
    else:
        await ctx.send("No codes for Dorado!")


@bot.command(aliases=["eich", "eichen"])
@is_map_channel()
async def eichenwald(ctx, type=""):
    post = "Eichenwald\n"
    type.lower()
    for entry in MapData.find(
        {"map_name": "eichenwald", "type": type}
        if type in types_of_map
        else {"map_name": "eichenwald"}
    ):
        post += (f"{entry['_id']} - {entry['type']} {entry['desc']}"
                 f" - Created by {entry['creator']}\n")
    if post.count("\n") > 1:
        await ctx.send(post)
    else:
        await ctx.send("No codes for Eichenwald!")


@bot.command(aliases=["hana"])
@is_map_channel()
async def hanamura(ctx, type=""):
    post = "Hanamura\n"
    type.lower()
    for entry in MapData.find(
        {"map_name": "hanamura", "type": type}
        if type in types_of_map
        else {"map_name": "hanamura"}
    ):
        post += (f"{entry['_id']} - {entry['type']} {entry['desc']}"
                 f" - Created by {entry['creator']}\n")
    if post.count("\n") > 1:
        await ctx.send(post)
    else:
        await ctx.send("No codes for Hanamura!")


@bot.command()
@is_map_channel()
async def havana(ctx, type=""):
    post = "Havana\n"
    type.lower()
    for entry in MapData.find(
        {"map_name": "havana", "type": type}
        if type in types_of_map
        else {"map_name": "havana"}
    ):
        post += (f"{entry['_id']} - {entry['type']} {entry['desc']}"
                 f" - Created by {entry['creator']}\n")
    if post.count("\n") > 1:
        await ctx.send(post)
    else:
        await ctx.send("No codes for Havana!")


@bot.command(aliases=["holly"])
@is_map_channel()
async def hollywood(ctx, type=""):
    post = "Hollywood\n"
    type.lower()
    for entry in MapData.find(
        {"map_name": "hollywood", "type": type}
        if type in types_of_map
        else {"map_name": "hollywood"}
    ):
        post += (f"{entry['_id']} - {entry['type']} {entry['desc']}"
                 f" - Created by {entry['creator']}\n")
    if post.count("\n") > 1:
        await ctx.send(post)
    else:
        await ctx.send("No codes for Hollywood!")


@bot.command(aliases=["hlc", "horizon"])
@is_map_channel()
async def horizonlunarcolony(ctx, type=""):
    post = "Horizon Lunar Colony\n"
    type.lower()
    for entry in MapData.find(
        {"map_name": "horizonlunarcolony", "type": type}
        if type in types_of_map
        else {"map_name": "horizonlunarcolony"}
    ):
        post += (f"{entry['_id']} - {entry['type']} {entry['desc']}"
                 f" - Created by {entry['creator']}\n")
    if post.count("\n") > 1:
        await ctx.send(post)
    else:
        await ctx.send("No codes for Horizon Lunar Colony!")


@bot.command()
@is_map_channel()
async def ilios(ctx, type=""):
    post = "Ilios\n"
    type.lower()
    for entry in MapData.find(
        {"map_name": "ilios", "type": type}
        if type in types_of_map
        else {"map_name": "ilios"}
    ):
        post += (f"{entry['_id']} - {entry['type']} {entry['desc']}"
                 f" - Created by {entry['creator']}\n")
    if post.count("\n") > 1:
        await ctx.send(post)
    else:
        await ctx.send("No codes for Ilios!")


@bot.command()
@is_map_channel()
async def junkertown(ctx, type=""):
    post = "Junkertown\n"
    type.lower()
    for entry in MapData.find(
        {"map_name": "junkertown", "type": type}
        if type in types_of_map
        else {"map_name": "junkertown"}
    ):
        post += (f"{entry['_id']} - {entry['type']} {entry['desc']}"
                 f" - Created by {entry['creator']}\n")
    if post.count("\n") > 1:
        await ctx.send(post)
    else:
        await ctx.send("No codes for Junkertown!")


@bot.command(aliases=["lijiang"])
@is_map_channel()
async def lijiangtower(ctx, type=""):
    post = "Lijiang Tower\n"
    type.lower()
    for entry in MapData.find(
        {"map_name": "lijiangtower", "type": type}
        if type in types_of_map
        else {"map_name": "lijiangtower"}
    ):
        post += (f"{entry['_id']} - {entry['type']} {entry['desc']}"
                 f" - Created by {entry['creator']}\n")
    if post.count("\n") > 1:
        await ctx.send(post)
    else:
        await ctx.send("No codes for Lijiang Tower!")


@bot.command()
@is_map_channel()
async def necropolis(ctx, type=""):
    post = "Necropolis\n"
    type.lower()
    for entry in MapData.find(
        {"map_name": "necropolis", "type": type}
        if type in types_of_map
        else {"map_name": "necropolis"}
    ):
        post += (f"{entry['_id']} - {entry['type']} {entry['desc']}"
                 f" - Created by {entry['creator']}\n")
    if post.count("\n") > 1:
        await ctx.send(post)
    else:
        await ctx.send("No codes for Necropolis!")


@bot.command()
@is_map_channel()
async def nepal(ctx, type=""):
    post = "Nepal\n"
    type.lower()
    for entry in MapData.find(
        {"map_name": "nepal", "type": type}
        if type in types_of_map
        else {"map_name": "nepal"}
    ):
        post += (f"{entry['_id']} - {entry['type']} {entry['desc']}"
                 f" - Created by {entry['creator']}\n")
    if post.count("\n") > 1:
        await ctx.send(post)
    else:
        await ctx.send("No codes for Nepal!")


@bot.command()
@is_map_channel()
async def numbani(ctx, type=""):
    post = "Numbani\n"
    type.lower()
    for entry in MapData.find(
        {"map_name": "numbani", "type": type}
        if type in types_of_map
        else {"map_name": "numbani"}
    ):
        post += (f"{entry['_id']} - {entry['type']} {entry['desc']}"
                 f" - Created by {entry['creator']}\n")
    if post.count("\n") > 1:
        await ctx.send(post)
    else:
        await ctx.send("No codes for Numbani!")


@bot.command()
@is_map_channel()
async def oasis(ctx, type=""):
    post = "Oasis\n"
    type.lower()
    for entry in MapData.find(
        {"map_name": "oasis", "type": type}
        if type in types_of_map
        else {"map_name": "oasis"}
    ):
        post += (f"{entry['_id']} - {entry['type']} {entry['desc']}"
                 f" - Created by {entry['creator']}\n")
    if post.count("\n") > 1:
        await ctx.send(post)
    else:
        await ctx.send("No codes for Oasis!")


@bot.command()
@is_map_channel()
async def paris(ctx, type=""):
    post = "Paris\n"
    type.lower()
    for entry in MapData.find(
        {"map_name": "paris", "type": type}
        if type in types_of_map
        else {"map_name": "paris"}
    ):
        post += (f"{entry['_id']} - {entry['type']} {entry['desc']}"
                 f" - Created by {entry['creator']}\n")
    if post.count("\n") > 1:
        await ctx.send(post)
    else:
        await ctx.send("No codes for Paris!")


@bot.command()
@is_map_channel()
async def rialto(ctx, type=""):
    post = "Rialto\n"
    type.lower()
    for entry in MapData.find(
        {"map_name": "rialto", "type": type}
        if type in types_of_map
        else {"map_name": "rialto"}
    ):
        post += (f"{entry['_id']} - {entry['type']} {entry['desc']}"
                 f" - Created by {entry['creator']}\n")
    if post.count("\n") > 1:
        await ctx.send(post)
    else:
        await ctx.send("No codes for Rialto!")


@bot.command(aliases=["r66"])
@is_map_channel()
async def route66(ctx, type=""):
    post = "Route 66\n"
    type.lower()
    for entry in MapData.find(
        {"map_name": "route66", "type": type}
        if type in types_of_map
        else {"map_name": "route66"}
    ):
        post += (f"{entry['_id']} - {entry['type']} {entry['desc']}"
                 f" - Created by {entry['creator']}\n")
    if post.count("\n") > 1:
        await ctx.send(post)
    else:
        await ctx.send("No codes for Route 66!")


@bot.command(aliases=["anubis"])
@is_map_channel()
async def templeofanubis(ctx, type=""):
    post = "Temple of Anubis\n"
    type.lower()
    for entry in MapData.find(
        {"map_name": "templeofanubis", "type": type}
        if type in types_of_map
        else {"map_name": "templeofanubis"}
    ):
        post += (f"{entry['_id']} - {entry['type']} {entry['desc']}"
                 f" - Created by {entry['creator']}\n")
    if post.count("\n") > 1:
        await ctx.send(post)
    else:
        await ctx.send("No codes for Temple of Anubis!")


@bot.command(aliases=["volskaya"])
@is_map_channel()
async def volskayaindustries(ctx, type=""):
    post = "Volskaya Industries\n"
    type.lower()
    for entry in MapData.find(
        {"map_name": "volskayaindustries", "type": type}
        if type in types_of_map
        else {"map_name": "volskayaindustries"}
    ):
        post += (f"{entry['_id']} - {entry['type']} {entry['desc']}"
                 f" - Created by {entry['creator']}\n")
    if post.count("\n") > 1:
        await ctx.send(post)
    else:
        await ctx.send("No codes for Volskaya Industries!")


@bot.command(aliases=["gibraltar"])
@is_map_channel()
async def watchpointgibraltar(ctx, type=""):
    post = "Watchpoint: Gibraltar\n"
    type.lower()
    for entry in MapData.find(
        {"map_name": "watchpointgibraltar", "type": type}
        if type in types_of_map
        else {"map_name": "watchpointgibraltar"}
    ):
        post += (f"{entry['_id']} - {entry['type']} {entry['desc']}"
                 f" - Created by {entry['creator']}\n")
    if post.count("\n") > 1:
        await ctx.send(post)
    else:
        await ctx.send("No codes for Watchpoint Gibraltar!")


@bot.command(aliases=["kr"])
@is_map_channel()
async def kingsrow(ctx, type=""):
    post = "King's Row\n"
    type.lower()
    for entry in MapData.find(
        {"map_name": "kingsrow", "type": type}
        if type in types_of_map
        else {"map_name": "kingsrow"}
    ):
        post += (f"{entry['_id']} - {entry['type']} {entry['desc']}"
                 f" - Created by {entry['creator']}\n")
    if post.count("\n") > 1:
        await ctx.send(post)
    else:
        await ctx.send("No codes for King's Row!")


@bot.command()
@is_map_channel()
async def petra(ctx, type=""):
    post = "Petra\n"
    type.lower()
    for entry in MapData.find(
        {"map_name": "petra", "type": type}
        if type in types_of_map
        else {"map_name": "petra"}
    ):
        post += (f"{entry['_id']} - {entry['type']} {entry['desc']}"
                 f" - Created by {entry['creator']}\n")
    if post.count("\n") > 1:
        await ctx.send(post)
    else:
        await ctx.send("No codes for Petra!")


@bot.command(aliases=["ecopoint", "antarctica"])
@is_map_channel()
async def ecopointantarctica(ctx, type=""):
    post = "Ecopoint: Antarctica\n"
    type.lower()
    for entry in MapData.find(
        {"map_name": "ecopointantarctica", "type": type}
        if type in types_of_map
        else {"map_name": "ecopointantarctica"}
    ):
        post += (f"{entry['_id']} - {entry['type']} {entry['desc']}"
                 f" - Created by {entry['creator']}\n")
    if post.count("\n") > 1:
        await ctx.send(post)
    else:
        await ctx.send("No codes for Ecopoint: Antarctica!")


@bot.command(aliases=["kz", "kane", "zaka"])
@is_map_channel()
async def kanezaka(ctx, type=""):
    post = "Kanezaka\n"
    type.lower()
    for entry in MapData.find(
        {"map_name": "kanezaka", "type": type}
        if type in types_of_map
        else {"map_name": "kanezaka"}
    ):
        post += (f"{entry['_id']} - {entry['type']} {entry['desc']}"
                 f" - Created by {entry['creator']}\n")
    if post.count("\n") > 1:
        await ctx.send(post)
    else:
        await ctx.send("No codes for Kanezaka!")


@bot.command(aliases=["chamber"])
@is_map_channel()
async def workshopchamber(ctx, type=""):
    post = "Workshop Chamber\n"
    type.lower()
    for entry in MapData.find(
        {"map_name": "workshopchamber", "type": type}
        if type in types_of_map
        else {"map_name": "workshopchamber"}
    ):
        post += (f"{entry['_id']} - {entry['type']} {entry['desc']}"
                 f" - Created by {entry['creator']}\n")
    if post.count("\n") > 1:
        await ctx.send(post)
    else:
        await ctx.send("No codes for Workshop Chamber!")


@bot.command(aliases=["expanse"])
@is_map_channel()
async def workshopexpanse(ctx, type=""):
    post = "Workshop Expanse\n"
    type.lower()
    for entry in MapData.find(
        {"map_name": "workshopexpanse", "type": type}
        if type in types_of_map
        else {"map_name": "workshopexpanse"}
    ):
        post += (f"{entry['_id']} - {entry['type']} {entry['desc']}"
                 f" - Created by {entry['creator']}\n")
    if post.count("\n") > 1:
        await ctx.send(post)
    else:
        await ctx.send("No codes for Workshop Expanse!")


@bot.command(aliases=["greenscreen", "green"])
@is_map_channel()
async def workshopgreenscreen(ctx, type=""):
    post = "Workshop Green Screen\n"
    type.lower()
    for entry in MapData.find(
        {"map_name": "workshopgreenscreen", "type": type}
        if type in types_of_map
        else {"map_name": "workshopgreenscreen"}
    ):
        post += (f"{entry['_id']} - {entry['type']} {entry['desc']}"
                 f" - Created by {entry['creator']}\n")
    if post.count("\n") > 1:
        await ctx.send(post)
    else:
        await ctx.send("No codes for Workshop Green Screen!")


@bot.command(aliases=["island"])
@is_map_channel()
async def workshopisland(ctx, type=""):
    post = "Workshop Island\n"
    type.lower()
    for entry in MapData.find(
        {"map_name": "workshopisland", "type": type}
        if type in types_of_map
        else {"map_name": "workshopisland"}
    ):
        post += (f"{entry['_id']} - {entry['type']} {entry['desc']}"
                 f" - Created by {entry['creator']}\n")
    if post.count("\n") > 1:
        await ctx.send(post)
    else:
        await ctx.send("No codes for Workshop Island!")


"""
PERSONAL BESTS / WORLD RECORDS / LEADERBOARDS - SUBMISSIONS, DELETIONS, VIEWING
"""


# Submit personal best records
@bot.command(
    help=("Submit personal bests."
          " Upload a screenshot with this message for proof!\n"
          "There will be a link in the world record"
          " leaderboards to the original post.\n"
          "Also updates a personal best if it is faster.\n\n"
          "<record> must be in this format '00:00:00.00'\n"
          "Remove leading zeroes and colons if they are not needed."),
    brief="Submit personal best",
)
@is_record_channel()
async def submitpb(ctx, map_code, level, record):
    sanitize(map_code)
    sanitize(record)
    sanitize(level)
    if not level.isnumeric() or int(level) not in range(0, 41):
        await ctx.channel.send("Level must be a number between 0 and 40")
        return
    if not isEnglish(map_code):
        await ctx.channel.send("Only letters A-Z and numbers 0-9 allowed.")
        return
    if record.isalnum() and isEnglish(record):
        await ctx.channel.send(
            ("Format the time correctly. 00:00:00.00 - "
             "Consider using the _/convertseconds <seconds>_ command."))
        return
    if is_time_format(record):
        map_code = map_code.upper()
        if (
            WorldRecords.count_documents(
                {
                    "map_code": map_code,
                    "name": ctx.author.name,
                    "level": level,
                    "posted_by": ctx.author.id,
                }
            )
            == 0
        ):

            newSubmission = {
                "map_code": map_code,
                "name": ctx.author.name,
                "record": record,
                "level": level,
                "posted_by": ctx.author.id,
                "message_id": ctx.message.id,
            }
            WorldRecords.insert_one(newSubmission)
            await ctx.channel.send(
                ("Personal best submission accepted:\n"
                 f"{map_code} level {level} - {ctx.author.name} - {record}")
            )

        elif (
            WorldRecords.count_documents(
                {
                    "map_code": map_code,
                    "name": ctx.author.name,
                    "level": level,
                    "posted_by": ctx.author.id,
                }
            )
            == 1
        ):
            search = WorldRecords.find_one(
                {
                    "map_code": map_code,
                    "name": ctx.author.name,
                    "level": level,
                    "posted_by": ctx.author.id,
                }
            )
            # convert strings into datetime obj to compare
            try:
                new_record = date_func(record)

                searched_record = date_func(search["record"])

                if new_record < searched_record:

                    # store normal string, not datetime obj.
                    WorldRecords.update_one(
                        search,
                        {
                            "$set": {
                                "record": record,
                                "level": level,
                                "message_id": ctx.message.id,
                            }
                        },
                    )
                    await ctx.channel.send(
                        ("Personal best update accepted:\n"
                         f"{map_code} level {level} - "
                         f"{ctx.author.name} - {record}")
                    )
                else:

                    await ctx.channel.send(
                        "Personal best needs to be faster to update."
                    )
            except ValueError:
                await ctx.channel.send(
                    ("Format the time correctly."
                     " 00:00:00.00 - Consider using "
                     "the _/convertseconds <seconds>_ command.")
                )
    else:
        await ctx.channel.send(
            ("Format the time correctly. 00:00:00.00 - "
             "Consider using the _/convertseconds <seconds>_ command.")
        )


# view a pb
@bot.command(
    help="View personal best record for a particular map code",
    brief="View personal best record",
)
@is_record_channel()
async def pb(ctx, map_code, level, name=""):
    sanitize(map_code)
    sanitize(name)
    if name == "":
        name = ctx.author.name
    map_code = map_code.upper()
    if (
        WorldRecords.count_documents(
            {"map_code": map_code, "name": name, "level": level}
        )
        == 1
    ):
        search = WorldRecords.find_one(
            {"map_code": map_code, "name": name, "level": level}
        )
        await ctx.channel.send(
            (f"{name}'s personal best for {map_code} level {level}:"
             f" {search['record']} - "
             f"https://discord.com/channels/195387617972322306/801496775390527548/{search['message_id']}")  # noqa: E501
        )
    else:
        await ctx.channel.send("Personal best doesn't exist.")


# Delete pb
@bot.command(
    help="Delete personal best record for a particular map code",
    brief="Delete personal best record",
)
@is_record_channel()
async def deletepb(ctx, map_code, level, name=""):
    map_code = map_code.upper()
    sanitize(map_code)
    sanitize(name)
    if name == "":
        name = ctx.author.name
    if WorldRecords.count_documents({"map_code": map_code, "name": name}) == 1:

        search = WorldRecords.find_one({"map_code": map_code, "name": name})

        if ctx.author.id == search["posted_by"] or any(
            role in ctx.author.roles for role in role_whitelist
        ):

            WorldRecords.delete_one({"map_code": map_code, "name": name})
            await ctx.channel.send("Personal best deleted succesfully.")
        else:
            await ctx.channel.send("You cannot delete that!")
    else:
        await ctx.channel.send(
            "Personal best deletion was unsuccesful. Record doesn't exist."
        )


# view world record
@bot.command(
    help=("View world record for a particular map code. "
          "Link to original post is included"),
    brief="View world record",
)
@is_record_channel()
async def wr(ctx, map_code, level=""):
    sanitize(map_code)
    map_code = map_code.upper()

    if level == "":
        post = f"CODE: {map_code} - WORLD RECORDS:\n"
        for entry in (
            WorldRecords.find({"map_code": map_code.upper(), "level": level})
            .sort("record", 1)
            .limit(1)
        ):
            post += (f"{entry['name']} - {entry['record']} - {entry['level']} - "
                    f"https://discord.com/channels/195387617972322306/801496775390527548/{entry['message_id']}\n")  # noqa: E501
    else:
        post = f"CODE: {map_code} LEVEL {level} - WORLD RECORD:\n"
        for entry in (
            WorldRecords.find({"map_code": map_code.upper(), "level": level})
            .sort("record", 1)
            .limit(1)
        ):
            post += (f"{entry['name']} - {entry['record']} - "
                    f"https://discord.com/channels/195387617972322306/801496775390527548/{entry['message_id']}\n")  # noqa: E501
        
    
    if post.count("\n") > 1:
        await ctx.send(post)
    else:
        await ctx.send(f"No world record for {map_code} level {level}!")


# view leaderboard
@bot.command(
    help=("View top 10 records for a particular map code. "
          "Links to original posts are included"),
    brief="View top 10 records",
    aliases=["top10"],
)
@is_record_channel()
async def lb(ctx, map_code, level):
    sanitize(map_code)
    map_code = map_code.upper()
    post = f"CODE: {map_code} LEVEL {level} - TOP 10 RECORDS:\n"
    for entry in (
        WorldRecords.find({"map_code": map_code.upper(), "level": level})
        .sort("record", 1)
        .limit(10)
    ):
        post += (f"{entry['name']} - {entry['record']} - "
                 f"https://discord.com/channels/195387617972322306/801496775390527548/{entry['message_id']}\n")  # noqa: E501
    if post.count("\n") > 1:
        await ctx.send(post)
    else:
        await ctx.send(f"No leaderboard for {map_code} level {level}!")


@bot.command(
    help="Converts seconds to 00:00:00.00 format",
    brief="Converts seconds to 00:00:00.00 format",
)
async def convertseconds(ctx, s):
    await ctx.send(str(datetime.timedelta(seconds=float(s)))[: -4 or None])


"""
AUTO CLEAN-UP - REMOVES PERSONAL BEST IF ORIGINAL POST IS DELETED
"""


@bot.event
async def on_message_delete(message):
    if WorldRecords.count_documents({"message_id": message.id}) == 1:

        WorldRecords.delete_one({"message_id": message.id})


"""
DISPLAY ALL ACCEPTABLE MAP NAMES FOR COMMANDS
"""


@commands.check_any(is_map_submit_channel(), is_map_channel())
@bot.command(
    help="Shows all acceptable map names for commands",
    brief="Shows map names for commands",
)
async def maps(ctx):
    await ctx.send(
        """```Acceptable map names:
    ayutthaya
    blackforest | bf
    blizzardworld | blizzworld | blizz | bw
    bsan
    castillo
    chateauguillard | chateau | guillard
    dorado
    ecopointantarctica | ecopoint | antarctica
    eichenwald | eichen | eich
    hanamura | hana
    havana
    hollywood | holly
    horizonlunarcolony | horizon | hlc
    ilios
    junkertown
    kanezaka | kane | zaka | kz
    kingsrow | kr
    lijiangtower | lijiang
    necropolis
    nepal
    numbani
    oasis
    paris
    petra
    rialto
    route66 | r66
    templeofanubis | anubis
    volskayaindustries | volskaya
    watchpointbilbraltar | gibraltar
    workshopchamber | chamber
    workshopexpanse | expanse
    workshopgreenScreen | greenscreen | green
    workshopisland | island```
    """
    )


"""
RUN DISCORD BOT
"""
bot.run(DISCORD_TOKEN)
