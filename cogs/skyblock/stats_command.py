import discord
from discord.ext import commands
import discord.utils 
from discord import app_commands
import json
import requests
from datetime import datetime, timedelta
import math 
import datetime
from settings import HYPIXEL_API_KEY


async def username_data(username):
    mojang_url = f"https://api.minetools.eu/uuid/{username}"
    uuid_data = await fetch_data(mojang_url)
    return uuid_data['id'], uuid_data['name']

def get_player_minecraft_skin(uuid):
    skin_url = f"https://starlightskins.lunareclipse.studio/render/ultimate/{uuid}/full"
    return skin_url


async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
        

async def get_guild_player_data(uuid):
    try:
        url =  f"https://api.hypixel.net/v2/guild?key={HYPIXEL_API_KEY}&player={uuid}"
        data = await fetch_data(url)
        guild_name = data["guild"]["name"]
        guild_join_date = data["guild"]["created"]
        guild_tag = data["guild"]["tag"]
        guild_members = len(data['guild']['members'])

        guild_rank = None
        for member in data['guild']['members']:
            if member['uuid'] == uuid:
                guild_rank = member['rank']
                break

        for member in data['guild']['members']:
            if member['uuid'] == uuid:
                guild_join_date_ms = member['joined']
                break

        guild_join_date = datetime.datetime.utcfromtimestamp(guild_join_date_ms / 1000).strftime('%Y-%m-%d %H:%M EDT')

        return guild_name, guild_join_date, guild_tag, guild_members, guild_rank
    except:
        return None, None, None, None, None

def calculate_bedwars_level_prestige(bedwars_level):
    if bedwars_level < 100:
        return "None Prestige"
    elif bedwars_level < 1100:
        prestiges = ["Iron", "Gold", "Diamond", "Emerald", "Sapphire", "Ruby", "Crystal", "Opal", "Amethyst", "Rainbow"]
        index = (bedwars_level - 100) // 100
        return f"⚝{prestiges[index]} Prestige"
    elif bedwars_level < 2000:
        prestiges = ["Iron Prime", "Gold Prime", "Diamond Prime", "Emerald Prime", "Sapphire Prime", "Ruby Prime", "Crystal Prime", "Opal Prime", "Amethyst Prime", "Mirror"]
        index = (bedwars_level - 1100) // 100
        return f"⚝{prestiges[index]} Prestige"
    elif bedwars_level < 3000:
        prestiges = ["Light", "Dawn", "Dusk", "Air", "Wind", "Nebula", "Thunder", "Earth", "Water", "Fire"]
        index = (bedwars_level - 2000) // 100
        return f"⚝{prestiges[index]} Prestige"
    else:
        return "Max Prestige"


def skywars_xp_tolevel(xp):
    xps = [0, 20, 70, 150, 250, 500, 1000, 2000, 3500, 6000, 10000, 15000]
    if xp >= 15000:
        return (xp - 15000) / 10000. + 12
    else:
        for i in range(len(xps)):
            if xp < xps[i]:
                return i + float(xp - xps[i-1]) / (xps[i] - xps[i-1])


def get_basic_player_data(uuid, player_skin, data, player_rank, username):
    first_login_ms = data["player"].get("firstLogin", 0)
    last_login_ms = data["player"].get("lastLogin", 0)
    player_karma = data["player"].get("karma", 0)
    network_experience = data["player"]["networkExp"]
    if first_login_ms != 0:
        first_login = datetime.datetime.utcfromtimestamp(first_login_ms / 1000).strftime('%Y-%m-%d %H:%M EDT')
    else:
        first_login = "Not Listed"
    if last_login_ms !=0:
        last_login = datetime.datetime.utcfromtimestamp(last_login_ms / 1000).strftime('%Y-%m-%d %H:%M EDT')
    else:
        last_login = "Not Listed"


    player_karma_formatted = "{:,}".format(player_karma)
    network_level = round((math.sqrt((2 * network_experience) + 30625) / 50) - 2.5, 2)
    
    guild_name, guild_join_date, guild_tag, guild_members, guild_rank = get_guild_player_data(uuid)

    if guild_tag is not None:
        if player_rank is not None:
            embed = discord.Embed(title=f"[{player_rank}] {username} [{guild_tag}]", color=discord.Color.purple())
        else:
            embed = discord.Embed(title=f"{username} [{guild_tag}]", color=discord.Color.purple())

        embed.add_field(name="Guild Name", value=guild_name)
        embed.add_field(name="Guild Members", value=guild_members)
        embed.add_field(name='\u200b', value='\u200b')
        embed.add_field(name="Rank", value=guild_rank)
        embed.add_field(name="Joined", value=guild_join_date)
        embed.add_field(name='\u200b', value='\u200b')

    else:
        if player_rank is not None:
            embed = discord.Embed(title=f"[{player_rank}] {username}", color=discord.Color.purple())
        else:
            embed = discord.Embed(title=f"{username}", color=discord.Color.purple())

    embed.set_thumbnail(url=player_skin)
    embed.insert_field_at(index = 0, name="Player level", value=network_level)
    embed.insert_field_at(index = 1, name="Player Krama", value=player_karma_formatted)
    embed.insert_field_at(index = 2, name='\u200b', value='\u200b')

    embed.insert_field_at(index = 3, name="First Login", value=first_login)
    embed.insert_field_at(index = 4, name="Last Login", value=last_login)
    embed.insert_field_at(index = 5, name='\u200b', value='\u200b')    

    return embed

def get_bedwars_player_data(uuid, player_skin, data, player_rank, username):
    bedwars_stats = data["player"]["stats"].get("Bedwars", {})
    bedwars_level = data["player"]["achievements"].get("bedwars_level", 0)
    winstreak = bedwars_stats.get("winstreak", 0)
    bedwars_prestige = calculate_bedwars_level_prestige(bedwars_level)

    # Solo Bedwars
    solo_bedwars_wins = bedwars_stats.get("eight_one_wins_bedwars", 0)
    solo_bedwars_losses = bedwars_stats.get("eight_one_games_played_bedwars", 0)
    solo_bedwars_final_kills = bedwars_stats.get("eight_one_final_kills_bedwars", 0)
    solo_bedwars_final_deaths = bedwars_stats.get("eight_one_final_deaths_bedwars", 0)
    solo_bedwars_beds_broken = bedwars_stats.get("eight_one_beds_broken_bedwars", 0)
    solo_bedwars_final_kill_ratio = round(solo_bedwars_final_kills / solo_bedwars_final_deaths, 2) if solo_bedwars_final_deaths else 0
    solo_bedwars_win_loss_ratio = round(solo_bedwars_wins / solo_bedwars_losses, 2) if solo_bedwars_losses else 0

    # Doubles Bedwars
    doubles_bedwars_wins = bedwars_stats.get("eight_two_wins_bedwars", 0)
    doubles_bedwars_losses = bedwars_stats.get("eight_two_games_played_bedwars", 0)
    doubles_bedwars_final_kills = bedwars_stats.get("eight_two_final_kills_bedwars", 0)
    doubles_bedwars_final_deaths = bedwars_stats.get("eight_two_final_deaths_bedwars", 0)
    doubles_bedwars_beds_broken = bedwars_stats.get("eight_two_beds_broken_bedwars", 0)
    doubles_bedwars_final_kill_ratio = round(doubles_bedwars_final_kills / doubles_bedwars_final_deaths, 2) if doubles_bedwars_final_deaths else 0
    doubles_bedwars_win_loss_ratio = round(doubles_bedwars_wins / doubles_bedwars_losses, 2) if doubles_bedwars_losses else 0

    # Triples Bedwars
    triples_bedwars_wins = bedwars_stats.get("four_three_wins_bedwars", 0)
    triples_bedwars_losses = bedwars_stats.get("four_three_games_played_bedwars", 0)
    triples_bedwars_final_kills = bedwars_stats.get("four_three_final_kills_bedwars", 0)
    triples_bedwars_final_deaths = bedwars_stats.get("four_three_final_deaths_bedwars", 0)
    triples_bedwars_beds_broken = bedwars_stats.get("four_three_beds_broken_bedwars", 0)
    triples_bedwars_final_kill_ratio = round(triples_bedwars_final_kills / triples_bedwars_final_deaths, 2) if triples_bedwars_final_deaths else 0
    triples_bedwars_win_loss_ratio = round(triples_bedwars_wins / triples_bedwars_losses, 2) if triples_bedwars_losses else 0

    # Fours Bedwars
    fours_bedwars_wins = bedwars_stats.get("four_four_wins_bedwars", 0)
    fours_bedwars_losses = bedwars_stats.get("four_four_games_played_bedwars", 0)
    fours_bedwars_final_kills = bedwars_stats.get("four_four_final_kills_bedwars", 0)
    fours_bedwars_final_deaths = bedwars_stats.get("four_four_final_deaths_bedwars", 0)
    fours_bedwars_beds_broken = bedwars_stats.get("four_four_beds_broken_bedwars", 0)
    fours_bedwars_final_kill_ratio = round(fours_bedwars_final_kills / fours_bedwars_final_deaths, 2) if fours_bedwars_final_deaths else 0
    fours_bedwars_win_loss_ratio = round(fours_bedwars_wins / fours_bedwars_losses, 2) if fours_bedwars_losses else 0


    if player_rank is not None:
        embed = discord.Embed(title=f"[{player_rank}] {username} Bedwars Stats", color=discord.Color.purple())
    else:
        embed = discord.Embed(title=f"{username} Bedwars Stats", color=discord.Color.purple())
        
    embed.set_thumbnail(url=player_skin)

    embed.add_field(name="Level", value=bedwars_level)
    embed.add_field(name="Prestige", value=bedwars_prestige)
    embed.add_field(name="Current Winstreak ", value=winstreak)

    embed.add_field(name="Solo Win/Loss Ratio", value=solo_bedwars_win_loss_ratio)
    embed.add_field(name="Solo FKDR", value=solo_bedwars_final_kill_ratio)
    embed.add_field(name="Solo Beds Broken", value=solo_bedwars_beds_broken)

    embed.add_field(name="Doubles Win/Loss Ratio", value=doubles_bedwars_win_loss_ratio)
    embed.add_field(name="Doubles FKDR", value=doubles_bedwars_final_kill_ratio)
    embed.add_field(name="Doubles Beds Broken", value=doubles_bedwars_beds_broken)

    embed.add_field(name="Triples Win/Loss Ratio", value=triples_bedwars_win_loss_ratio)
    embed.add_field(name="Triples FKDR", value=triples_bedwars_final_kill_ratio)
    embed.add_field(name="Triples Beds Broken", value=triples_bedwars_beds_broken)

    embed.add_field(name="Fours Win/Loss Ratio", value=fours_bedwars_win_loss_ratio)
    embed.add_field(name="Fours FKDR", value=fours_bedwars_final_kill_ratio)
    embed.add_field(name="Fours Beds Broken", value=fours_bedwars_beds_broken)
    return embed

def get_tnt_games_player_data(uuid, player_skin, data, player_rank, username):
    tnt_games_stats = data["player"]["stats"].get("TNTGames", {})
    tnt_tag_wins = tnt_games_stats.get("wins_tntag", 0)
    tnt_tag_kills = tnt_games_stats.get("kills_tntag", 0)

    tnt_run_wins = tnt_games_stats.get("wins_tntrun", 0)
    tnt_run_record_seconds = tnt_games_stats.get("record_tntrun", 0)
    if tnt_run_record_seconds != 0:
        tnt_run_record = round(tnt_run_record_seconds / 60, 2)
    else:
        tnt_run_record = 0

    pvp_run_wins = tnt_games_stats.get("eight_one_wins_bedwars", 0)  # Assuming this is the correct property
    pvp_run_record_seconds = tnt_games_stats.get("record_pvprun", 0)
    if pvp_run_record_seconds != 0:
        pvp_run_record = round(pvp_run_record_seconds / 60, 2)
    else:
        pvp_run_record = 0


    if player_rank is not None:
        embed = discord.Embed(title=f"[{player_rank}] {username} TNT Game Stats", color=discord.Color.purple())
    else:
        embed = discord.Embed(title=f"{username} TNT Game Stats", color=discord.Color.purple())


    embed.set_thumbnail(url=player_skin)
    embed.add_field(name="TNT Tag wins", value=tnt_tag_wins)
    embed.add_field(name="TNT Tag Kills", value=tnt_tag_kills)
    embed.add_field(name='\u200b', value='\u200b')

    embed.add_field(name="TNT Run wins", value=tnt_run_wins)
    embed.add_field(name="TNT Record", value=tnt_run_record)
    embed.add_field(name='\u200b', value='\u200b')

    embed.add_field(name="TNT Tag wins", value=tnt_tag_wins)
    embed.add_field(name="TNT Tag Kills", value=tnt_tag_kills)
    embed.add_field(name='\u200b', value='\u200b')

    embed.add_field(name="PVP Run Wins", value=pvp_run_wins)
    embed.add_field(name="PVP Run Record", value=pvp_run_record)
    embed.add_field(name='\u200b', value='\u200b')

    return embed

def get_build_battle_player_data(uuid, player_skin, data, player_rank, username):
    build_battle_stats = data["player"]["stats"].get("BuildBattle", {})
    build_battle_games_played = build_battle_stats.get("games_played", 0)
    build_battle_score = build_battle_stats.get("score", 0)
    normal_solo_wins = build_battle_stats.get("wins_solo_normal", 0)
    pro_solo_wins = 0  # cant find in api call so its a 0
    normal_team_wins = build_battle_stats.get("wins_teams_normal", 0)
    guess_build_wins = build_battle_stats.get("wins_guess_the_build", 0)

    if player_rank is not None:
        embed = discord.Embed(title=f"[{player_rank}] {username} Build Battle Stats", color=discord.Color.purple())
    else:
        embed = discord.Embed(title=f"{username} Build Battle Stats", color=discord.Color.purple())

    embed.set_thumbnail(url=player_skin)
    embed.add_field(name="Games Played", value=build_battle_games_played)
    embed.add_field(name="Score", value=build_battle_score)
    embed.add_field(name='\u200b', value='\u200b')

    embed.add_field(name="Solo Wins", value=normal_solo_wins)
    embed.add_field(name="Pro Mode Wins", value=pro_solo_wins)
    embed.add_field(name='\u200b', value='\u200b')

    embed.add_field(name="Team Wins", value=normal_team_wins)
    embed.add_field(name="Guess The build Wins", value=guess_build_wins)
    embed.add_field(name='\u200b', value='\u200b')

    return embed 

def get_duels_player_data(uuid, player_skin, data, player_rank, username):
    duels_stats = data["player"]["stats"].get("Duels", {})
    duels_kills = duels_stats.get("kills", 0)
    duels_deaths = duels_stats.get("deaths", 0)
    if duels_deaths != 0:
        duels_kill_death_ratio = round(duels_kills / duels_deaths, 2)
    else:
        duels_kill_death_ratio = 0

    duels_wins = duels_stats.get("wins", 0)
    duels_losses = duels_stats.get("losses", 0)
    if duels_losses != 0:
        duels_win_loss_ratio = round(duels_wins / duels_losses, 2)
    else:
        duels_win_loss_ratio = 0

    uhc_one_vs_one_wins = duels_stats.get("uhc_duel_wins", 0)
    uhc_one_vs_one_losses = duels_stats.get("uhc_duel_losses", 0)
    if uhc_one_vs_one_losses != 0:
        uhc_one_vs_one_win_loss_ratio = round(uhc_one_vs_one_wins / uhc_one_vs_one_losses, 2)
    else: 
        uhc_one_vs_one_win_loss_ratio = 0

    sumo_wins = duels_stats.get("sumo_duel_wins", 0)
    sumo_losses = duels_stats.get("sumo_duel_losses", 0)
    if sumo_losses != 0:
        sumo_win_loss_ratio = round(sumo_wins / sumo_losses, 2)
    else:
        sumo_win_loss_ratio = 0

    classic_wins = duels_stats.get("classic_duel_wins", 0)
    classic_losses = duels_stats.get("classic_duel_losses", 0)
    if classic_losses != 0:
        classic_win_loss_ratio = round(classic_wins / classic_losses, 2)
    else:
        classic_win_loss_ratio = 0

    bridge_one_vs_one_wins = duels_stats.get("bridge_duel_wins", 0)
    bridge_one_vs_one_losses = duels_stats.get("bridge_duel_losses", 0)
    if bridge_one_vs_one_losses != 0:
        bridge_one_vs_one_win_loss_ratio = round(bridge_one_vs_one_wins / bridge_one_vs_one_losses, 2)
    else: 
        bridge_one_vs_one_win_loss_ratio = 0

    if player_rank is not None:
        embed = discord.Embed(title=f"[{player_rank}] {username} Duels Stats", color=discord.Color.purple())
    else:
        embed = discord.Embed(title=f"{username} Duels Stats", color=discord.Color.purple())    

    embed.set_thumbnail(url=player_skin)
    embed.add_field(name="Kills", value=duels_kills)
    embed.add_field(name="Deaths", value=duels_deaths)
    embed.add_field(name="Kill/Death Ratio", value=duels_kill_death_ratio)


    embed.add_field(name="Wins", value=duels_wins)
    embed.add_field(name="Losses", value=duels_losses)
    embed.add_field(name="Win/Loss Ratio", value=duels_win_loss_ratio)

    embed.add_field(name="UHC 1v1 Wins", value=uhc_one_vs_one_wins)
    embed.add_field(name="UHC 1v1 Losses", value=uhc_one_vs_one_losses)
    embed.add_field(name="UHC 1v1 Win/Loss Ratio", value=uhc_one_vs_one_win_loss_ratio)

    embed.add_field(name="Sumo Wins", value=sumo_wins)
    embed.add_field(name="Sumo Losses", value=sumo_losses)
    embed.add_field(name="Sumo Win/Loss Ratio", value=sumo_win_loss_ratio)

    embed.add_field(name="Classic Wins", value=classic_wins)
    embed.add_field(name="Classic Losses", value=classic_losses)
    embed.add_field(name="Classic Win/Loss Ratio", value=classic_win_loss_ratio)

    embed.add_field(name="Bridge 1v1 Wins", value=bridge_one_vs_one_wins)
    embed.add_field(name="Bridge 1v1 Losses", value=bridge_one_vs_one_losses)
    embed.add_field(name="Bridge 1v1 Win/Loss Ratio", value=bridge_one_vs_one_win_loss_ratio)

    return embed

def get_uhc_player_data(uuid, player_skin, data, player_rank, username):
    uhc_stats = data["player"]["stats"].get("UHC", {})

    score = uhc_stats.get("score", 0)
    coins = uhc_stats.get("coins", 0)
    solo_kills = uhc_stats.get("kills_solo", 0)
    solo_deaths = uhc_stats.get("deaths_solo", 0)
    solo_wins = uhc_stats.get("wins_solo", 0)
    teams_kills = uhc_stats.get("kills", 0)
    teams_deaths = uhc_stats.get("deaths", 0)
    team_wins = uhc_stats.get("wins", 0)

    if player_rank is not None:
        embed = discord.Embed(title=f"[{player_rank}] {username} UHC Stats", color=discord.Color.purple())
    else:
        embed = discord.Embed(title=f"{username} UHC Stats", color=discord.Color.purple())    

    embed.set_thumbnail(url=player_skin)
    embed.add_field(name="Score", value=score)
    embed.add_field(name="Coins", value=coins)
    embed.add_field(name='\u200b', value='\u200b')

    embed.add_field(name="Solo Kills", value=solo_kills)
    embed.add_field(name="Solo Deaths", value=solo_deaths)
    embed.add_field(name="Solo Wins", value=solo_wins)

    embed.add_field(name="Team Kills", value=teams_kills)
    embed.add_field(name="Team Deaths", value=teams_deaths)
    embed.add_field(name="Team Wins", value=team_wins)

    return embed


def get_skywars_player_data(uuid, player_skin, data, player_rank, username):
    skywars_stats = data["player"]["stats"].get("SkyWars", {})
    skywars_xp = skywars_stats.get("skywars_experience", 0)
    skywars_level = skywars_xp_tolevel(skywars_xp)

    skywars_wins = skywars_stats.get("wins", 0)
    skywars_losses = skywars_stats.get("losses", 0)
    if skywars_losses != 0:
        skywars_win_loss_raito = round(skywars_wins / skywars_losses, 2)
    else: 
        skywars_win_loss_raito = 0

    skywars_kills = skywars_stats.get("kills", 0)
    skywars_deaths = skywars_stats.get("deaths", 0)
    if skywars_deaths != 0:
        skywars_kill_death_ratio = round(skywars_kills / skywars_deaths, 2)
    else: 
        skywars_kill_death_ratio = 0

    solo_insane_wins = skywars_stats.get("wins_solo_insane", 0)
    solo_insane_losses = skywars_stats.get("losses_solo_insane", 0)
    solo_insane_kills = skywars_stats.get("kills_solo_insane", 0)
    solo_insane_deaths = skywars_stats.get("deaths_solo_insane", 0)
    if solo_insane_deaths != 0:
        solo_insane_kill_death_ratio = round(solo_insane_kills / solo_insane_deaths, 2)
    else: 
        solo_insane_kill_death_ratio = 0

    teams_insane_wins = skywars_stats.get("wins_team_insane", 0)
    teams_insane_losses = skywars_stats.get("losses_team_insane", 0)
    teams_insane_kills = skywars_stats.get("kills_team_insane", 0)
    teams_insane_deaths = skywars_stats.get("deaths_team_insane", 0)
    if teams_insane_deaths != 0:
        teams_insane_kill_death_ratio = round(teams_insane_kills / teams_insane_deaths, 2)
    else: 
        teams_insane_kill_death_ratio = 0

    ranked_wins = skywars_stats.get("wins_ranked", 0)
    ranked_losses = skywars_stats.get("losses_ranked", 0)
    ranked_kills = skywars_stats.get("kills_ranked", 0)
    ranked_deaths = skywars_stats.get("deaths_ranked", 0)
    if ranked_deaths != 0:
        ranked_kill_death_ratio = round(ranked_kills / ranked_deaths, 2)
    else: 
        ranked_kill_death_ratio = 0


    if player_rank is not None:
        embed = discord.Embed(title=f"[{player_rank}] {username} UHC Stats", color=discord.Color.purple())
    else:
        embed = discord.Embed(title=f"{username} UHC Stats", color=discord.Color.purple())    

    embed.set_thumbnail(url=player_skin)

    embed.add_field(name="Level", value=skywars_level)
    embed.add_field(name="Win/Loss Raito", value=skywars_win_loss_raito)
    embed.add_field(name="Kill/Death Raito", value=skywars_kill_death_ratio)
 
    embed.add_field(name="Solo Insane Wins", value=solo_insane_wins)
    embed.add_field(name="Solo Insane Losses", value=solo_insane_losses)
    embed.add_field(name="Kill/Death Raito", value=solo_insane_kill_death_ratio)  

    embed.add_field(name="Teams Insane Wins", value=teams_insane_wins)
    embed.add_field(name="Teams Insane Losses", value=teams_insane_losses)
    embed.add_field(name="Kill/Death Ratio", value=teams_insane_kill_death_ratio)

    embed.add_field(name="Ranked Wins", value=ranked_wins)
    embed.add_field(name="Ranked Losses", value=ranked_losses)
    embed.add_field(name="Kill/Death Ratio", value=ranked_kill_death_ratio)

    return embed

class stats_menu(discord.ui.Select):
    def __init__(self, uuid, player_skin, data, player_rank, username):
        super().__init__(placeholder="Select a game", min_values=1, max_values=1, options=[
            discord.SelectOption(label="Main", value="main", emoji="<:compas:1215407414808027247>"),
            discord.SelectOption(label="Bedwars", value="bedwars", emoji="<:bedwars:1213961433176477696>"),
            discord.SelectOption(label="TNT Games", value="tnt_games", emoji="<:tnt:1213966739789058119>"),
            discord.SelectOption(label="Build Battle", value="build_battle", emoji="<:crafting_bench:1213979037764952064>"),
            discord.SelectOption(label="Duels", value="duels", emoji="<:fishing_rod:1213979036988997732>"),
            discord.SelectOption(label="UHC", value="uhc", emoji="<:golden_apple:1214004683257942016>"),
            discord.SelectOption(label="Skywars", value="skywars", emoji="<:Bow:1153821678506364990>")
        ])
        self.uuid = uuid
        self.player_skin = player_skin
        self.data = data
        self.player_rank = player_rank
        self.username = username
        
        
    async def callback(self, interaction: discord.Interaction):
        try:
            view = SelectView(self.uuid, self.player_skin, self.data, self.player_rank, self.username)
            game = interaction.data["values"][0]
            get_player_data_func = {
                "main": get_basic_player_data,
                "bedwars": get_bedwars_player_data,
                "tnt_games": get_tnt_games_player_data,
                "build_battle": get_build_battle_player_data,
                "duels": get_duels_player_data,
                "uhc": get_uhc_player_data,
                "skywars": get_skywars_player_data}.get(game, get_basic_player_data)
            embed = get_player_data_func(self.uuid, self.player_skin, self.data, self.player_rank, self.username)
            await interaction.response.edit_message(embed=embed, view=view)
        except Exception as e:
            print(e)

class SelectView(discord.ui.View):
    def __init__(self, uuid, player_skin, data, player_rank, username):
        super().__init__(timeout=30)
        self.add_item(stats_menu(uuid, player_skin, data, player_rank, username))
        
    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)
        
class stats_command(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
            

    @app_commands.checks.has_permissions(send_messages = True)
    @app_commands.command(
        name = "stats",
        description= "very basic stats of players")

    async def stats(self, interaction: discord.Interaction, username: str):
        try:
            uuid, username = await username_data(username)
            player_skin = get_player_minecraft_skin(uuid)
            url = f"https://api.hypixel.net/v2/player?key={HYPIXEL_API_KEY}&uuid={uuid}"
            data = await fetch_data(url)

            player_rank = data["player"].get("newPackageRank", None)
            rank = data["player"].get("rank", None)

            if rank is not None:
                player_rank = rank

            
            if player_rank == "MVP_PLUS":
                player_rank = "MVP+"
            if player_rank == "VIP_PLUS":
                player_rank = "VIP+"

            embed = get_basic_player_data(uuid, player_skin, data, player_rank, username)
            view = SelectView(uuid, player_skin, data, player_rank, username)
            await interaction.response.send_message(embed=embed, view=view)
            view.message = await interaction.original_response()
        except KeyError:
            embed = discord.Embed(description=f"❌ '{username}' cannot be found", color=discord.Color.red())
            await interaction.response.send_message(embed=embed, view=view)
        except Exception:
            embed = discord.Embed(description=f"❌ Command Failure", color=discord.Color.red())
            await interaction.response.send_message(embed=embed, view=view)




async def setup(bot):
    await bot.add_cog(stats_command(bot))
    