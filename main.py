import sys, types

class DummyAudio: pass
sys.modules['audioop'] = DummyAudio()
sys.modules['_audioop'] = DummyAudio()

import random, asyncio, discord, os
from discord import app_commands
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Sync error: {e}")
    print(f"Bot is online as {bot.user}")

@bot.tree.command(name="ship", description="Check compatibility with a member")
@app_commands.guild_only()
async def ship(interaction: discord.Interaction, first_user: discord.Member, second_user: discord.Member):
    percentage = random.randint(1, 100)
    blocks = int(percentage / 10)
    bar = "🟦" * blocks + "⬛" * (10 - blocks)
    embed = discord.Embed(
        title="✨ نسبة التوافق",
        description=f"{first_user.mention} + {second_user.mention}\n\n**النسبة:** `{percentage}%`\n{bar}",
        color=discord.Color.purple()
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="avatar_fusion", description="Combine two avatars together")
@app_commands.guild_only()
async def avatar_fusion(interaction: discord.Interaction, target_user: discord.Member):
    embed = discord.Embed(
        title="🎨 دمج الصور الشخصية",
        description=f"تم دمج صورة {interaction.user.mention} مع {target_user.mention}",
        color=discord.Color.gold()
    )
    embed.set_image(url=target_user.display_avatar.url)
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="server_stats", description="Display server statistics")
@app_commands.guild_only()
async def server_stats(interaction: discord.Interaction):
    guild = interaction.guild
    embed = discord.Embed(title=f"📊 إحصائيات {guild.name}", color=discord.Color.green())
    embed.add_field(name="عدد الأعضاء", value=f"`{guild.member_count}`", inline=True)
    embed.add_field(name="عدد القنوات", value=f"`{len(guild.channels)}`", inline=True)
    embed.add_field(name="عدد الرتب", value=f"`{len(guild.roles)}`", inline=True)
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="broadcast", description="Send broadcast message to all members")
@app_commands.guild_only()
@app_commands.checks.has_permissions(administrator=True)
async def broadcast(interaction: discord.Interaction, message: str):
    await interaction.response.send_message("⏳ جاري الإرسال...", ephemeral=True)
    success, failed = 0, 0
    for member in interaction.guild.members:
        if member.bot: continue
        try:
            embed = discord.Embed(
                title=f"📢 إعلان من {interaction.guild.name}",
                description=message,
                color=discord.Color.blue()
            )
            await member.send(embed=embed)
            success += 1
            await asyncio.sleep(1.5)
        except Exception: failed += 1
    await interaction.followup.send(f"✅ تم الإرسال بنجاح: {success} | فشل: {failed}", ephemeral=True)

@bot.tree.command(name="send_dm", description="Send a direct message to a specific member")
@app_commands.guild_only()
@app_commands.checks.has_permissions(administrator=True)
async def send_dm(interaction: discord.Interaction, target_user: discord.Member, message: str):
    if target_user.bot:
        await interaction.response.send_message("❌ لا يمكنك إرسال رسالة لبوت!", ephemeral=True)
        return
    try:
        embed = discord.Embed(
            title=f"📢 رسالة خاصة من إدارة {interaction.guild.name}",
            description=message,
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"أُرسلت بواسطة: {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
        await target_user.send(embed=embed)
        await interaction.response.send_message(f"✅ تم إرسال الرسالة بنجاح إلى {target_user.mention}!", ephemeral=True)
    except Exception:
        await interaction.response.send_message(f"❌ فشل الإرسال إلى {target_user.mention} (الخاص مغلق لديه).", ephemeral=True)

bot.run(os.environ.get("BOT_TOKEN"))
