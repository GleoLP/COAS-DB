import discord
import asyncio
import os
from datetime import datetime, timedelta

# Definiere die benötigten Intents
intents = discord.Intents.default()
intents.typing = False
intents.presences = False

# Verbindung zum Discord-Client herstellen
client = discord.Client(intents=intents)

async def check_logs():
    channel_id = ID
    log_paths = {
        "acc1": "/home/pi0/.local/share/PrismLauncher/instances/1.8.9 acc1/.minecraft/logs/latest.log",
        "acc2": "/home/pi0/.local/share/PrismLauncher/instances/1.8.9 acc2/.minecraft/logs/latest.log"}

    target_phrases = [
        "You were spawned in Limbo.",
        "A disconnect occurred in your connection, so you were put in the SkyBlock Lobby!",
        "You are being transferred to the",
        "Evacuating to Hub..."]

    while True:
        for account, log_file_path in log_paths.items():
            try:
                today_date = datetime.now().date()
                last_modified_time = os.path.getmtime(log_file_path)
                if last_modified_time > check_logs.last_checked_time.get(account, 0):
                    with open(log_file_path, 'r') as file:
                        lines = file.readlines()
                        for line in lines:
                            for target_phrase in target_phrases:
                                if target_phrase in line:
                                    timestamp = line.split('] ')[0][1:]
                                    log_time = datetime.strptime(timestamp, "%H:%M:%S")
                                    log_timestamp = datetime.combine(today_date, log_time.time())
                                    current_time = datetime.now().replace(microsecond=0)
                                    if -60 <= (current_time - log_timestamp).total_seconds() <= 1 * 25:
                                        message = f"<@&number> Since {timestamp} {account} Account not on island"
                                        channel = client.get_channel(channel_id)
                                        await channel.send(message)
                                        check_logs.last_checked_time[account] = last_modified_time
                                        break  # Breche die aktuelle Zeile ab und suche in der nächsten
            except FileNotFoundError:
                print(f"File for {account} not found.")
            except Exception as e:
                print(f"error: {e}")
            await asyncio.sleep(1)
        await asyncio.sleep(20)

    check_logs.last_checked_time = {}

async def delete_old_messages():
    delall = 0
    if(delall == 1):
        channel_id = ID  # Ersetze dies mit der Channel-ID, in dem du die Nachrichten löschen möchtest
        channel = client.get_channel(channel_id)  # Kanalobjekt abrufen

        messages_to_keep = 2 # Anzahl der Nachrichten, die behalten werden sollen
        messages = []

        # Nachrichten im Kanal sammeln
        async for message in channel.history(limit=None):
            messages.append(message)

        # Die ältesten Nachrichten löschen, außer den neuesten 'messages_to_keep'
        for message in messages[:-messages_to_keep]:
            await message.delete()
            await asyncio.sleep(0.5)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    print(f'{datetime.now()} Bot joined')

    # Führe die Funktion zum Löschen aller Nachrichten aus
    await delete_old_messages()

    # Starte die Log-Überprüfung
    await check_logs()

# Token deines Discord-Bots einfügen
client.run('YourToken')
