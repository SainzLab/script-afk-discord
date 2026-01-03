import discord
import asyncio
import ctypes.util
import sys

# ================= Config =================
TOKEN = "TXasdasdeSa............." # id User
VC_ID = 00000000000000000000000 # id Voice
STATUS_GAME = "Minecraft 2"  # Ganti nama game atau aktivitas
# ===============================================

# --- FIX UNTUK LINUX/LXC (fix error voice) ---
opus_path = ctypes.util.find_library('opus')
if opus_path:
    if not discord.opus.is_loaded():
        discord.opus.load_opus(opus_path)
else:
    try:
        discord.opus.load_opus('libopus.so.0')
    except:
        pass

class AFKClient(discord.Client):
    async def on_ready(self):
        print(f'Login: {self.user}')
        
        await self.change_presence(activity=discord.Game(name=STATUS_GAME))
        print(f"Status set ke: Playing {STATUS_GAME}")

        channel = self.get_channel(VC_ID)
        if not channel:
            print("Channel tidak ketemu.")
            return

        try:
            await channel.connect(self_deaf=True, self_mute=True)
            print(f"✅ SUKSES: Terhubung ke {channel.name}")
        except Exception as e:
            print(f"Error Voice: {e}")

# Loop agar bot jalan terus
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
client = AFKClient()

try:
    loop.run_until_complete(client.start(TOKEN))
except KeyboardInterrupt:
    loop.run_until_complete(client.close())
except Exception as e:
    print(f"Error: {e}")