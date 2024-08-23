import discord
from discord.ext import commands
import discord.utils 
import asyncio
from discord import app_commands
import requests
from datetime import datetime
import re
import json
import math
from collections import OrderedDict 
import asyncio
import aiohttp
from database import collection

from settings import HYPIXEL_API_KEY

item_names_to_check = OrderedDict()
armor_names_to_check = OrderedDict()
rarities_names_to_check = OrderedDict()
skyblock_prices_database = collection["item"]

item_prices = {}
for document in skyblock_prices_database.find():
    for item_name, item_data in document.items():
        if item_name != "_id": 
            price = item_data["buy"]
            item_prices[item_name] = price



with open("item_emojis.json", "r") as f:
    item_emojis = json.load(f)

with open('item_names.txt', 'r') as file:
    for line in file:
        item_names_to_check[line.strip()] = {}

with open('armor_names.txt', 'r') as file:
    for line in file:
        armor_names_to_check[line.strip()] = {}

with open('rarities_names.txt', 'r') as file:
    for line in file:
        rarities_names_to_check[line.strip()] = {}

with open('display_names.json', 'r') as file:
    display_name_mapping = json.load(file)

armor_file_count = len(armor_names_to_check)
item_file_count = len(item_names_to_check)
rarities_file_count = len(rarities_names_to_check)
total_museum_items = armor_file_count + item_file_count + rarities_file_count

async def username_data(username):
    mojang_url = f"https://api.minetools.eu/uuid/{username}"
    uuid_data = await fetch_data(mojang_url)
    return uuid_data['id'], uuid_data['name']

def get_player_minecraft_skin(uuid):
    skin_url = f"https://starlightskins.lunareclipse.studio/render/ultimate/{uuid}/full"
    return skin_url


def get_profile_emoji(game_mode):
    if game_mode == "ironman":
        return "<:iron_chestplate:1215464857151742002>"
    elif game_mode == "Bingo":
        return "<:golden_apple:1216141683893342289>"
    elif game_mode == "Stranded":
        return "<:emerald:1153934618479841320>"
    else: 
        return "<:grass_block:1216142547575898122>"

async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
        
async def fetch_profile_data(session, profile_id):
    api2_url = f"https://api.hypixel.net/skyblock/museum?key={HYPIXEL_API_KEY}&profile={profile_id}"
    async with session.get(api2_url) as response:
        return await response.json()

async def check_profiles_with_data(uuid):
    url = f"https://api.hypixel.net/skyblock/profiles?key={HYPIXEL_API_KEY}&uuid={uuid}"

    async with aiohttp.ClientSession() as session:
        try:
            data = await fetch_data(url)
            profiles = data.get("profiles", [])
            tasks = [fetch_profile_data(session, profile.get("profile_id")) for profile in profiles]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            profiles_with_data = []
            cute_names_with_data = []

            for idx, result in enumerate(results):
                if isinstance(result, dict) and result.get("success") and result.get("members"):
                    profiles_with_data.append(profiles[idx]["profile_id"])
                    cute_name = profiles[idx].get("cute_name")
                    if cute_name:
                        game_mode = profiles[idx].get("game_mode", "None")
                        cute_names_with_data.append(f"{cute_name}:{game_mode}")
        except aiohttp.ClientError:
            pass

    return profiles_with_data, cute_names_with_data


async def get_data(selected_profile_id, uuid):
    url = f"https://api.hypixel.net/skyblock/museum?key={HYPIXEL_API_KEY}&profile={selected_profile_id}"
    dataset = await fetch_data(url)
    data = dataset.get("members", {}).get(uuid, {}).get("items", [])
    return data

def read_item_conditions(filename):
    item_conditions = []
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith("#"):
                condition, dependency = line.split()
                item_conditions.append((condition, dependency))
    return item_conditions



def get_lowest_price(item_string):
    lowest_price_str = item_string.split("``")[1]
    if lowest_price_str == "N/A":
        return float("inf")
    else:
        lowest_price = int(lowest_price_str.replace(",", ""))
        return lowest_price

def initial_embed_creation(username, user_minecraft_skin, armor_percent, armor_count, item_percent, item_count, rarities_percent, rarities_count, total_items_percent, cute_name):
        embed = discord.Embed(title=f"{username}'s Skyblock Museum", description=f" ", type = 'rich', color=discord.Color.purple(), timestamp=datetime.now() )
        embed.set_thumbnail(url=user_minecraft_skin)    
        embed.set_footer(text= f"Selected Profile: {cute_name}")


        total_items_donated = armor_count + item_count + rarities_count
        total_museum_items = armor_file_count + item_file_count + rarities_file_count
        total_items_percent = (total_items_donated / total_museum_items * 100)

        embed.add_field(name=f"Items Donated: {total_items_percent:.2f}%", value=f"{total_items_donated}/{total_museum_items}", inline=False)
        embed.add_field(name = f"<:diamond_Sword:1153821139718635590> Weapons ``{item_percent:.2f}%``", value= f"{item_count}/{item_file_count}", inline=False)
        embed.add_field(name = f"<:diamond_chestplate:1155732360898293832> Armor ``{armor_percent:.2f}%``", value= f"{armor_count}/{armor_file_count}", inline=False)
        embed.add_field(name = f"<:emerald_block:1217611364131012719> Rarities ``{rarities_percent:.2f}%``", value= f"{rarities_count}/{rarities_file_count}", inline=False)


        return embed


def percentage_calculator(data):
    armor_count = 0
    item_count = 0
    rarities_count = 0
    unmatched_items = []  # Store unmatched items here

    for item_name in data:
        if item_name in armor_names_to_check:
            armor_count += 1
        elif item_name in item_names_to_check:
            item_count += 1
        elif item_name in rarities_names_to_check:
            rarities_count += 1
        else:
            unmatched_items.append(item_name)  # Store unmatched item

    armor_percent = (armor_count / armor_file_count) * 100
    item_percent = (item_count / item_file_count) * 100
    rarities_percent = (rarities_count / rarities_file_count) * 100

    total_items_donated = armor_count + item_count + rarities_count
    total_items_percent = (total_items_donated / total_museum_items * 100)

    print(unmatched_items)

    return armor_percent, armor_count, item_percent, item_count, rarities_percent, rarities_count, total_items_percent



class weapons(discord.ui.View):
    def __init__(self, data, user_minecraft_skin, username, cute_name, armor_percent, armor_count, item_percent, item_count, rarities_percent, rarities_count, total_items_percent):
        super().__init__(timeout=60)
        self.current_page = 1
        self.data = data
        self.show_filtered_items = False
        self.show_sorted_filtered_items = False
        self.filtered_item_names = []
        self.pages = 9
        self.user_minecraft_skin = user_minecraft_skin
        self.username = username
        self.cute_name = cute_name
        self.armor_percent = armor_percent
        self.armor_count = armor_count
        self.item_percent = item_percent
        self.item_count = item_count
        self.rarities_percent = rarities_percent
        self.rarities_count = rarities_count
        self.total_items_percent = total_items_percent
        self.remove_item(self.sorted_present_button)

    async def on_timeout(self):
        try:
            for item in self.children:
                item.disabled = True
            await self.message.edit(view=self)
        except:
            pass
        
    async def send(self, interaction: discord.Interaction):
        embed = self.create_embed()
        await interaction.response.edit_message(embed=embed, view=self)


    def calculate_page_number(self):
        self.filtered_item_names = []

        for item_name in item_names_to_check:
            if self.show_filtered_items and item_name not in self.data and item_name in item_names_to_check:
                self.filtered_item_names.append(item_name)

        if self.show_filtered_items:
            self.pages = math.ceil(len(self.filtered_item_names) / 14)
        else:
            self.pages = math.ceil(item_file_count / 14)

    def create_embed(self):
        item_names_to_check_list = list(item_names_to_check)
        all_items_to_display = []
        total_items = len(item_names_to_check_list)
        items_per_page = 14
        start_index = (self.current_page - 1) * items_per_page
        end_index = min(start_index + items_per_page, total_items)
        self.filtered_item_names = []

        for index in range(total_items):
            item_name = item_names_to_check_list[index]
            emoji = item_emojis.get(item_name, "<:grey_dye:1153937769022898196>")
            display_item_name = display_name_mapping.get(item_name, item_name)

            if item_name in self.data:
                value = "<:YesYesYes:1146507491568533544>"
            else:
                value = "<:NoNoNo:1146507501966204999>"
            
            if self.show_filtered_items and item_name not in self.data and item_name in item_names_to_check:
                if item_name not in self.data:
                    lowest_price = item_prices[item_name]
                    self.filtered_item_names.append(f"{emoji} {display_item_name} {value} \n <:coins_emoji:1217568780235047052> ``{lowest_price}`` coins")


            if not self.show_filtered_items:
                embed = discord.Embed(title=f"{self.username}'s Donated Weapons", description = f"Total Weapons Donated: {self.item_count} /{item_file_count} ``({self.item_percent:.2f}%)``", color=discord.Color.green())
                all_items_to_display.append(f"{emoji} {display_item_name} {value}")


        if self.show_filtered_items:
            if self.filtered_item_names:
                if self.show_sorted_filtered_items:
                    sorted_filtered_items = sorted(self.filtered_item_names, key=get_lowest_price)
                    embed = discord.Embed(title=f"{self.username}'s not donated Weapons sorted by lowest price", description=f"Total Weapons Donated: {self.item_count} / {item_file_count} ``({self.item_percent:.2f}%)``", color=discord.Color.red())
                    all_items_to_display.extend(sorted_filtered_items)
                else:
                    embed = discord.Embed(title=f"{self.username}'s not donated Weapons", description=f"Total Weapons Donated: {self.item_count} / {item_file_count} ``({self.item_percent:.2f}%)`` " , color=discord.Color.red())
                    all_items_to_display.extend(self.filtered_item_names)




        if self.show_filtered_items and not self.filtered_item_names:
            embed = discord.Embed(title=f"{self.username}'s Donated Weapons", description = f"Congrats, You are a Loser!", color=discord.Color.green())
            self.remove_item(self.sorted_present_button)
            self.remove_item(self.not_present_button)

        else:
            items_to_display = all_items_to_display[start_index:end_index]
            for item in items_to_display:
                embed.add_field(name=item, value = "", inline=False)



        embed.set_thumbnail(url="https://static.wikia.nocookie.net/minecraft_gamepedia/images/6/6a/Diamond_Sword_JE2_BE2.png/revision/latest?cb=20200217235945")
        embed.set_footer(text=f"Page {self.current_page}/{self.pages} • Selected Profile {self.cute_name}", icon_url=self.user_minecraft_skin)
        self.calculate_page_number()
        self.update_buttons()
        return embed

    @discord.ui.button(label="Main Menu", style=discord.ButtonStyle.primary)
    async def go_to_museum_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        embed = initial_embed_creation(self.username, self.user_minecraft_skin, self.item_percent, self.item_count, self.armor_percent, self.armor_count, self.rarities_percent, self.rarities_count, self.total_items_percent, self.cute_name)
        initial_menu = InitialMenu(self.data, self.user_minecraft_skin, self.username, self.cute_name, self.armor_percent, self.armor_count, self.item_percent, self.item_count, self.rarities_percent, self.rarities_count, self.total_items_percent)
        self.remove_item(self.go_to_museum_button)
        await interaction.edit_original_response(embed=embed, view=initial_menu)

    @discord.ui.button(label="<", style=discord.ButtonStyle.grey)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page -= 1
        if self.current_page < 1:
            self.current_page = 1
        await self.update_message(interaction)

    @discord.ui.button(label=">", style=discord.ButtonStyle.grey)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page += 1
        if self.current_page > self.pages:
            self.current_page = self.pages
        await self.update_message(interaction)

    @discord.ui.button(label="Not Donated", style=discord.ButtonStyle.red, custom_id="not_present_button")
    async def not_present_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page = 1
        self.show_filtered_items = not self.show_filtered_items
        self.calculate_page_number()
        if self.show_filtered_items:
            self.add_item(self.sorted_present_button)
        else:
            for item in self.children:
                if isinstance(item, discord.ui.Button) and item.custom_id == "sorted_present_button":
                    self.remove_item(item)
        button.label = "Not Donated" if not self.show_filtered_items else "Donated"
        button.style = discord.ButtonStyle.red if not self.show_filtered_items else discord.ButtonStyle.green
        await self.update_message(interaction)

    @discord.ui.button(label="Sort By Price", style=discord.ButtonStyle.red, custom_id="sorted_present_button")
    async def sorted_present_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page = 1
        self.show_sorted_filtered_items = not self.show_sorted_filtered_items
        self.calculate_page_number()
        button.label = "Sort By Price" if not self.show_sorted_filtered_items else "Unsorted"
        button.style = discord.ButtonStyle.red if not self.show_sorted_filtered_items else discord.ButtonStyle.green
        await self.update_message(interaction)


    async def update_message(self, interaction: discord.Interaction):
        await interaction.edit_original_response(embed=self.create_embed(), view=self)


    def update_buttons(self):
        if self.current_page == 1:
            self.prev_button.disabled = True
        else:
            self.prev_button.disabled = False
        if self.pages == 0:
            self.next_button.disabled = True
            self.prev_button.disabled = True
        elif self.current_page == self.pages:
            self.next_button.disabled = True
        else:
            self.next_button.disabled = False

    async def on_timeout(self):
        pass

class rarities(discord.ui.View):
    def __init__(self, data, user_minecraft_skin, username, cute_name, armor_percent, armor_count, item_percent, item_count, rarities_percent, rarities_count, total_items_percent):
        super().__init__(timeout=60)
        self.current_page = 1
        self.data = data
        self.show_filtered_rarities = False
        self.show_sorted_filtered_rarities = False
        self.filtered_rarity_names = []
        self.pages = 8
        self.user_minecraft_skin = user_minecraft_skin
        self.username = username
        self.cute_name = cute_name
        self.armor_percent = armor_percent
        self.armor_count = armor_count
        self.item_percent = item_percent
        self.item_count = item_count
        self.rarities_percent = rarities_percent
        self.rarities_count = rarities_count
        self.total_items_percent = total_items_percent
        self.remove_item(self.sorted_present_button)

    async def on_timeout(self):
        try:
            for item in self.children:
                item.disabled = True
            await self.message.edit(view=self)
        except:
            pass
        
    async def send(self, interaction: discord.Interaction):
        embed = self.create_embed()
        await interaction.response.edit_message(embed=embed, view=self)

    def calculate_page_number(self):
        self.filtered_rarity_names = []

        for rarity_name in rarities_names_to_check:
            if self.show_filtered_rarities and rarity_name not in self.data and rarity_name in rarities_names_to_check:
                self.filtered_rarity_names.append(rarity_name)

        if self.show_filtered_rarities:
            self.pages = math.ceil(len(self.filtered_rarity_names) / 14)
        else:
            self.pages = math.ceil(rarities_file_count / 14)


    def create_embed(self):
        rarities_names_to_check_list = list(rarities_names_to_check)
        all_rarities_to_display = []
        total_items = len(rarities_names_to_check_list)
        items_per_page = 14
        start_index = (self.current_page - 1) * items_per_page
        end_index = min(start_index + items_per_page, total_items)
        self.filtered_rarity_names = []

        for index in range(total_items):
            rarity_name = rarities_names_to_check_list[index]
            emoji = item_emojis.get(rarity_name, "❓")
            display_item_name = display_name_mapping.get(rarity_name, rarity_name)

            if rarity_name in self.data:
                value = "<:YesYesYes:1146507491568533544>"
            else:
                value = "<:NoNoNo:1146507501966204999>"

            if self.show_filtered_rarities and rarity_name not in self.data and rarity_name in rarities_names_to_check:
                if rarity_name not in self.data:
                    lowest_price = item_prices[rarity_name]
                self.filtered_rarity_names.append(f"{emoji} {display_item_name} \n <:coins_emoji:1217568780235047052> ``{lowest_price}`` coins")


            if not self.show_filtered_rarities:
                embed = discord.Embed(title=f"{self.username}'s Donated Rarities", description = f"Total Rarities Donated: {self.rarities_count} /{rarities_file_count} ``({self.rarities_percent:.2f}%)``", color=discord.Color.green())
                all_rarities_to_display.append(f"{emoji} {display_item_name} {value}")

        if self.show_filtered_rarities:
            if self.filtered_rarity_names:
                if self.show_sorted_filtered_rarities:
                    sorted_filtered_items = sorted(self.filtered_rarity_names, key=get_lowest_price)
                    embed = discord.Embed(title=f"{self.username}'s not donated Rarities sorted by lowest price", description = f"Total Rarities Donated: {self.rarities_count} /{rarities_file_count} ``({self.rarities_percent:.2f}%)``", color=discord.Color.red())
                    all_rarities_to_display.extend(sorted_filtered_items)
                else:
                    embed = discord.Embed(title=f"{self.username}'s not donated Rarities", description = f"Total Rarities Donated: {self.rarities_count} /{rarities_file_count} ``({self.rarities_percent:.2f}%)``", color=discord.Color.red())

                    all_rarities_to_display.extend(self.filtered_rarity_names)


        if self.show_filtered_rarities and not self.filtered_rarity_names:
            embed = discord.Embed(title=f"{self.username}'s Donated Weapons", description = f"Congrats, You are a Loser!", color=discord.Color.green())
            self.remove_item(self.sorted_present_button)
            self.remove_item(self.not_present_button)

        else:
            rarities_to_display = all_rarities_to_display[start_index:end_index]
            for rarity in rarities_to_display:
                embed.add_field(name=rarity, value = "", inline=False)



        embed.set_thumbnail(url="https://static.wikia.nocookie.net/minecraft_gamepedia/images/8/80/Block_of_Emerald_JE1_BE1.png/revision/latest?cb=20191229174639")
        embed.set_footer(text=f"Page {self.current_page}/{self.pages} • Selected Profile {self.cute_name}", icon_url=self.user_minecraft_skin)
        self.calculate_page_number()
        self.update_buttons()
        return embed

    @discord.ui.button(label="Main Menu", style=discord.ButtonStyle.primary)
    async def go_to_museum_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        embed = initial_embed_creation(self.username, self.user_minecraft_skin, self.item_percent, self.item_count, self.armor_percent, self.armor_count, self.rarities_percent, self.rarities_count, self.total_items_percent, self.cute_name)
        initial_menu = InitialMenu(self.data, self.user_minecraft_skin, self.username, self.cute_name, self.armor_percent, self.armor_count, self.item_percent, self.item_count, self.rarities_percent, self.rarities_count, self.total_items_percent)
        self.remove_item(self.go_to_museum_button)
        await interaction.edit_original_response(embed=embed, view=initial_menu)

    @discord.ui.button(label="<", style=discord.ButtonStyle.grey)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page -= 1
        if self.current_page < 1:
            self.current_page = 1
        await self.update_message(interaction)

    @discord.ui.button(label=">", style=discord.ButtonStyle.grey)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page += 1
        if self.current_page > self.pages:
            self.current_page = self.pages
        await self.update_message(interaction)


    @discord.ui.button(label="Not Donated", style=discord.ButtonStyle.red, custom_id="not_present_button")
    async def not_present_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page = 1
        self.show_filtered_rarities = not self.show_filtered_rarities
        self.calculate_page_number()
        if self.show_filtered_rarities:
            self.add_item(self.sorted_present_button)
        else:
            for item in self.children:
                if isinstance(item, discord.ui.Button) and item.custom_id == "sorted_present_button":
                    self.remove_item(item)
        button.label = "Not Donated" if not self.show_filtered_rarities else "Donated"
        button.style = discord.ButtonStyle.red if not self.show_filtered_rarities else discord.ButtonStyle.green
        await self.update_message(interaction)

    @discord.ui.button(label="Sort By Price", style=discord.ButtonStyle.red, custom_id="sorted_present_button")
    async def sorted_present_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page = 1
        self.show_sorted_filtered_rarities = not self.show_sorted_filtered_rarities
        self.calculate_page_number()
        button.label = "Sort By Price" if not self.show_sorted_filtered_rarities else "Unsorted"
        button.style = discord.ButtonStyle.red if not self.show_sorted_filtered_rarities else discord.ButtonStyle.green
        await self.update_message(interaction)

    async def update_message(self, interaction: discord.Interaction):
        await interaction.edit_original_response(embed=self.create_embed(), view=self)



    def update_buttons(self):
        if self.current_page == 1:
            self.prev_button.disabled = True
        else:
            self.prev_button.disabled = False
        if self.pages == 0:
            self.next_button.disabled = True
            self.prev_button.disabled = True
        elif self.current_page == self.pages:
            self.next_button.disabled = True
        else:
            self.next_button.disabled = False

class armor(discord.ui.View):
    def __init__(self, data, user_minecraft_skin, username, cute_name, armor_percent, armor_count, item_percent, item_count, rarities_percent, rarities_count, total_items_percent):
        super().__init__(timeout=60)
        self.current_page = 1
        self.data = data
        self.show_filtered_armor = False
        self.show_sorted_filtered_armor = False
        self.filtered_armor_names = []
        self.pages = 8
        self.user_minecraft_skin = user_minecraft_skin
        self.username = username
        self.cute_name = cute_name
        self.armor_percent = armor_percent
        self.armor_count = armor_count
        self.item_percent = item_percent
        self.item_count = item_count
        self.rarities_percent = rarities_percent
        self.rarities_count = rarities_count
        self.total_items_percent = total_items_percent
        self.remove_item(self.sorted_present_button)

    async def on_timeout(self):
        try:
            for item in self.children:
                item.disabled = True
            await self.message.edit(view=self)
        except:
            pass
        
    async def send(self, interaction: discord.Interaction):
        embed = self.create_embed()
        await interaction.response.edit_message(embed=embed, view=self)

    def calculate_page_number(self):
        self.filtered_armor_names = []

        for armor_name in armor_names_to_check:
            if self.show_filtered_armor and armor_name not in self.data and armor_name in armor_names_to_check:
                self.filtered_armor_names.append(armor_name)

        if self.filtered_armor_names:
            self.pages = math.ceil(len(self.filtered_armor_names) / 14)
        else:
            self.pages = math.ceil(armor_file_count / 14)



    def create_embed(self):
        armor_names_to_check_list = list(armor_names_to_check)
        all_armor_to_display = []
        total_items = len(armor_names_to_check_list)
        items_per_page = 14
        start_index = (self.current_page - 1) * items_per_page
        end_index = min(start_index + items_per_page, total_items)
        self.filtered_armor_names = []


        for index in range(total_items):
            armor_name = armor_names_to_check_list[index]
            emoji = item_emojis.get(armor_name, "❓")
            display_item_name = display_name_mapping.get(armor_name, armor_name)

            if armor_name in self.data:
                value = "<:YesYesYes:1146507491568533544>"
            else:
                value = "<:NoNoNo:1146507501966204999>"

            if self.show_filtered_armor and armor_name not in self.data and armor_name in armor_names_to_check:
                if armor_name not in self.data:
                    lowest_price = item_prices[armor_name]
                self.filtered_armor_names.append(f"{emoji} {display_item_name} \n <:coins_emoji:1217568780235047052> ``{lowest_price}`` coins")

            if not self.show_filtered_armor:
                embed = discord.Embed(title=f"{self.username}'s Donated Armor sets", description = f"Total Armor Sets Donated: {self.armor_count} /{armor_file_count} ``({self.armor_percent:.2f}%)``", color=discord.Color.green())
                all_armor_to_display.append(f"{emoji} {display_item_name} {value}")

        if self.show_filtered_armor:
                if self.filtered_armor_names:
                    if self.show_sorted_filtered_armor:
                        sorted_filtered_armor = sorted(self.filtered_armor_names, key=get_lowest_price)
                        embed = discord.Embed(title=f"{self.username}'s not donated Armor Sets sorted by lowest price", description=f"Total Armor Sets Donated: {self.armor_count} / {armor_file_count} ``({self.armor_percent:.2f}%)``", color=discord.Color.red(),)
                        all_armor_to_display.extend(sorted_filtered_armor)
                    else:
                        embed = discord.Embed(title=f"{self.username}'s not donated Armor Sets", description=f"Total Weapons Donated: {self.armor_count} / {armor_file_count} ``({self.armor_percent:.2f}%)``" , color=discord.Color.red(),)
                        all_armor_to_display.extend(self.filtered_armor_names)


        if self.show_filtered_armor and not self.filtered_armor_names:
            embed = discord.Embed(title=f"{self.username}'s Donated Weapons", description = f"Congrats, You are a Loser!", color=discord.Color.green())
        else:
            armors_to_display = all_armor_to_display[start_index:end_index]
            for armor in armors_to_display:
                embed.add_field(name=armor, value = "", inline=False)



        embed.set_thumbnail(url="https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/3d/Diamond_Chestplate_%28item%29_JE2_BE2.png/revision/latest?cb=20190406141332")
        embed.set_footer(text=f"Page {self.current_page}/{self.pages} • Selected Profile {self.cute_name}", icon_url=self.user_minecraft_skin)
        self.calculate_page_number()
        self.update_buttons()
        return embed

    @discord.ui.button(label="Main Menu", style=discord.ButtonStyle.primary)
    async def go_to_museum_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        embed = initial_embed_creation(self.username, self.user_minecraft_skin, self.item_percent, self.item_count, self.armor_percent, self.armor_count, self.rarities_percent, self.rarities_count, self.total_items_percent, self.cute_name)
        initial_menu = InitialMenu(self.data, self.user_minecraft_skin, self.username, self.cute_name, self.armor_percent, self.armor_count, self.item_percent, self.item_count, self.rarities_percent, self.rarities_count, self.total_items_percent)
        self.remove_item(self.go_to_museum_button)
        await interaction.edit_original_response(embed=embed, view=initial_menu)

    @discord.ui.button(label="<", style=discord.ButtonStyle.grey)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page -= 1
        if self.current_page < 1:
            self.current_page = 1
        await self.update_message(interaction)

    @discord.ui.button(label=">", style=discord.ButtonStyle.grey)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page += 1
        if self.current_page > self.pages:
            self.current_page = self.pages
        await self.update_message(interaction)

    @discord.ui.button(label="Not Donated", style=discord.ButtonStyle.red, custom_id="not_present_button")
    async def not_present_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page = 1
        self.show_filtered_armor = not self.show_filtered_armor
        self.calculate_page_number()
        if self.show_filtered_armor:
            self.add_item(self.sorted_present_button)
        else:
            for item in self.children:
                if isinstance(item, discord.ui.Button) and item.custom_id == "sorted_present_button":
                    self.remove_item(item)
        button.label = "Not Donated" if not self.show_filtered_armor else  "Donated"
        button.style = discord.ButtonStyle.red if not self.show_filtered_armor else discord.ButtonStyle.green
        await self.update_message(interaction)

    @discord.ui.button(label="Sort By Price", style=discord.ButtonStyle.red, custom_id="sorted_present_button")
    async def sorted_present_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page = 1
        self.show_sorted_filtered_armor = not self.show_sorted_filtered_armor
        self.calculate_page_number()
        button.label = "Sort By Price" if not self.show_sorted_filtered_armor else "Unsorted"
        button.style = discord.ButtonStyle.red if not self.show_sorted_filtered_armor else discord.ButtonStyle.green
        await self.update_message(interaction)


    async def update_message(self, interaction: discord.Interaction):
        await interaction.edit_original_response(embed=self.create_embed(), view=self)


    def update_buttons(self):
        if self.current_page == 1:
            self.prev_button.disabled = True
        else:
            self.prev_button.disabled = False
        if self.pages == 0:
            self.next_button.disabled = True
            self.prev_button.disabled = True
        elif self.current_page == self.pages:
            self.next_button.disabled = True
        else:
            self.next_button.disabled = False

class InitialMenu(discord.ui.View):
    def __init__(self, data, user_minecraft_skin, username, cute_name, armor_percent, armor_count, item_percent, item_count, rarities_percent, rarities_count, total_items_percent):
        super().__init__(timeout=300)
        self.view_museum_button = None
        self.data = data
        self.user_minecraft_skin = user_minecraft_skin
        self.username = username
        self.cute_name = cute_name
        self.armor_percent = armor_percent
        self.armor_count = armor_count
        self.item_percent = item_percent
        self.item_count = item_count
        self.rarities_percent = rarities_percent
        self.rarities_count = rarities_count
        self.total_items_percent = total_items_percent

    async def on_timeout(self):
        try:
            for item in self.children:
                item.disabled = True
            await self.message.edit(view=self)
        except:
            pass
        
    @discord.ui.button(label="Weapons", style=discord.ButtonStyle.blurple)
    async def view_museum(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await self.paginate(interaction)
        except Exception as e:
            print("Error in view_museum:", e)

    @discord.ui.button(label="Armor", style=discord.ButtonStyle.blurple)
    async def menu1(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await self.paginate2(interaction)
        except Exception as e:
            print("Error in menu1:", e)

    @discord.ui.button(label="Rarities", style=discord.ButtonStyle.blurple)
    async def menu3(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await self.paginate3(interaction)
        except Exception as e:
            print("Error in menu1:", e)

    async def paginate(self, interaction: discord.Interaction):
        pagination_view = weapons(self.data, self.user_minecraft_skin, self.username, self.cute_name, self.armor_percent, self.armor_count, self.item_percent, self.item_count, self.rarities_percent, self.rarities_count, self.total_items_percent)
        try:
            await pagination_view.send(interaction)
        except Exception as e:
            print("Error in paginate:", e)

    async def paginate2(self, interaction: discord.Interaction):
        pagination_view = armor(self.data, self.user_minecraft_skin, self.username, self.cute_name, self.armor_percent, self.armor_count, self.item_percent, self.item_count, self.rarities_percent, self.rarities_count, self.total_items_percent)
        try:
            await pagination_view.send(interaction)
        except Exception as e:
            print("Error in paginate3:", e)

    async def paginate3(self, interaction: discord.Interaction):
        pagination_view = rarities(self.data, self.user_minecraft_skin, self.username, self.cute_name, self.armor_percent, self.armor_count, self.item_percent, self.item_count, self.rarities_percent, self.rarities_count, self.total_items_percent)
        try:
            await pagination_view.send(interaction)
        except Exception as e:
            print("Error in paginate3:", e)



class ProfileMenu(discord.ui.Select):
    def __init__(self, username, user_minecraft_skin, uuid):
        super().__init__(
            placeholder="Select a cute name",
        )
        self.username = username
        self.user_minecraft_skin = user_minecraft_skin
        self.uuid = uuid

    async def setup_select(self):
        profiles_with_data, cute_names_with_data = await check_profiles_with_data(self.uuid)

        for cute_name, profile_id in zip(cute_names_with_data, profiles_with_data):
            cute_name, game_mode = cute_name.split(":")
            self.add_option(label=cute_name, value=f"{profile_id}:{cute_name}", emoji=get_profile_emoji(game_mode))



    async def callback(self, interaction: discord.Interaction):
        selected_option = self.values[0]
        profile_id, cute_name = selected_option.split(':')
        data = await get_data(profile_id, self.uuid)
        item_conditions = read_item_conditions("item_conditions.txt")

        for condition, dependency in item_conditions:
            if condition in data and dependency not in data:
                data[dependency] = True

        armor_percent, armor_count, item_percent, item_count, rarities_percent, rarities_count, total_items_percent = percentage_calculator(data)
        embed = initial_embed_creation(self.username, self.user_minecraft_skin, armor_percent, armor_count, item_percent, item_count, rarities_percent, rarities_count, total_items_percent, cute_name)
        initial_menu = InitialMenu(data, self.user_minecraft_skin, self.username, cute_name, armor_percent, armor_count, item_percent, item_count, rarities_percent, rarities_count, total_items_percent)
        await interaction.response.edit_message(embed=embed, view=initial_menu)
        initial_menu.message = await interaction.original_response()


class SelectView(discord.ui.View):
    def __init__(self, username, user_minecraft_skin, uuid):
        super().__init__()
        self.add_item(ProfileMenu(username, user_minecraft_skin, uuid))



        

class museum_command(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="museum",
        description="Access the museum information"
    )
    
    async def show_initial_menu(self, interaction: discord.Interaction, username: str,):
        uuid, username = await username_data(username)
        user_minecraft_skin = get_player_minecraft_skin(uuid)
        await interaction.response.defer(thinking=True)
        try:
            initial_menu = SelectView(username, user_minecraft_skin, uuid)
            await initial_menu.children[0].setup_select()
            embed = discord.Embed(title=f"{username}'s Skyblock Museum", description=f"Displaying skyblock profiles with Museum API on", color=discord.Color.purple(), timestamp=datetime.now())
            embed.set_thumbnail(url=user_minecraft_skin)
            await interaction.followup.send(embed=embed, view=initial_menu)
        except TypeError or discord.errors.HTTPException:
                embed = discord.Embed(title=f"{username}'s Skyblock Museum", description="The username you entered does not have any profiles on SkyBlock.", type='rich', color=discord.Color.red(), timestamp=datetime.now())
                embed.set_footer(text=f"{interaction.user}")
                embed.set_thumbnail(url=user_minecraft_skin)
                await interaction.response.send_message(embed=embed, ephemeral = True)
                print(e)
        except KeyError: 
                embed = discord.Embed(title=f"{username}'s Skyblock Museum", description="The username does not exist.", type='rich', color=discord.Color.red(), timestamp=datetime.now())
                embed.set_footer(text=f"{interaction.user}")
                embed.set_thumbnail(url=user_minecraft_skin)
                await interaction.response.send_message(embed=embed, ephemeral = True)
        except Exception as e:
            await interaction.response.send_message(content="There has been an error with this command. Please try again at another time." , ephemeral = True)




async def setup(bot):
    await bot.add_cog(museum_command(bot))
