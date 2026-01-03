import discord
import asyncio
import ctypes.util
import sys

# ================= KONFIGURASI =================
TOKEN = "MTQ1NjkxOTQ2MDg4M/w......................"
VC_ID = 2143234253424543545
STATUS_GAME = "Minecraft 2" 
# ===============================================

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
            # set timeout (10s -> 30s)
            await channel.connect(self_deaf=True, self_mute=True, timeout=30.0)
            print(f"✅ SUKSES: Terhubung ke {channel.name}")
            
        except asyncio.TimeoutError:
            await asyncio.sleep(2)
            
            if channel.guild.me in channel.members:
                print("⚠️ Warning: Terdeteksi Timeout, TAPI akun berhasil masuk voice.")
                print("✅ Mengabaikan error dan lanjut jalan.")
            else:
                print("❌ Error: Timeout dan gagal masuk voice.")
                
        except Exception as e:
            print(f"Error Lain: {e}")

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
client = AFKClient()

try:
    loop.run_until_complete(client.start(TOKEN))
except KeyboardInterrupt:
    loop.run_until_complete(client.close())
except Exception as e:
    pass