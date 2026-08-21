Import sys, types

# تجاوز مكتبة الصوت في البيئات السحابية (لتفادي الأخطاء أثناء التشغيل)
class DummyAudio: pass
sys.modules['audioop'] = DummyAudio()
sys.modules['_audioop'] = DummyAudio()

import random, asyncio, discord, os
from discord import app_commands
from discord.ext import commands

# تحديد صلاحيات البوت (Intents)
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# لون أسود مدمج مع خلفية ديسكورد الداكنة
EMBED_COLOR = 0x2b2d31

# ----------------- حدث بدء تشغيل البوت ومزامنة الأوامر -----------------
@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Sync error: {e}")
    print(f"Bot is online as {bot.user}")

# ----------------- حدث الرد التلقائي عند المنشن -----------------
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message):
        reply_text = f"هلا والله {message.author.mention}! 🤖\nكيف أقدر أساعدك؟ اكتب `/` لمشاهدة قائمة الأوامر."
        await message.channel.send(reply_text)

    await bot.process_commands(message)

# ----------------- أوامر السلاش باللغة الإنجليزية -----------------

# 1. أمر نسبة التوافق
@bot.tree.command(name="ship", description="Calculate love or friendship compatibility between two members")
@app_commands.rename(first_user="first_member", second_user="second_member")
@app_commands.guild_only()
async def ship(interaction: discord.Interaction, first_user: discord.Member, second_user: discord.Member):
    percentage = random.randint(1, 100)
    blocks = int(percentage / 10)
    bar = "1️⃣" * blocks + "2️⃣" * (10 - blocks)
    embed = discord.Embed(
        title="✨ نسبة التوافق",
        description=f"{first_user.mention} + {second_user.mention}\n\n**النسبة:** `{percentage}%`\n{bar}",
        color=EMBED_COLOR
    )
    await interaction.response.send_message(embed=embed)

# 3. أمر سرقة الأفتار (مُعدّل)
@bot.tree.command(name="steal_avatar", description="Steal and display another member's avatar")
@app_commands.rename(target_user="target_member")
@app_commands.guild_only()
async def steal_avatar(interaction: discord.Interaction, target_user: discord.Member):
    embed = discord.Embed(
        title="تم سرقة الأفتار بنجاح!",
        description=f"قام {interaction.user.mention} بسرقة أفتار {target_user.mention}! \n\n🔗 [اضغط هنا لتحميل الصورة]({target_user.display_avatar.url})",
        color=EMBED_COLOR
    )
    embed.set_image(url=target_user.display_avatar.url)
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    embed.set_footer(text=f"المافيات | طلب بواسطة: {interaction.user.name}")
    await interaction.response.send_message(embed=embed)

# 4. أمر إحصائيات السيرفر
@bot.tree.command(name="server_stats", description="Display full server stats including members and channel counts")
@app_commands.guild_only()
async def server_stats(interaction: discord.Interaction):
    guild = interaction.guild
    embed = discord.Embed(title=f"📊 إحصائيات {guild.name}", color=EMBED_COLOR)
    embed.add_field(name="عدد الأعضاء", value=f"`{guild.member_count}`", inline=True)
    embed.add_field(name="عدد القنوات", value=f"`{len(guild.channels)}`", inline=True)
    embed.add_field(name="عدد الرتب", value=f"`{len(guild.roles)}`", inline=True)
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    await interaction.response.send_message(embed=embed)

# 5. أمر البرودكاست (للخاص لجميع الأعضاء)
@bot.tree.command(name="broadcast", description="Send a mass direct message to all server members (Admins only)")
@app_commands.rename(message="announcement_text")
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
                color=EMBED_COLOR
            )
            await member.send(embed=embed)
            success += 1
            await asyncio.sleep(1.5)
        except Exception: failed += 1
    await interaction.followup.send(f"✅ تم الإرسال بنجاح: {success} | فشل: {failed}", ephemeral=True)

# 6. أمر إرسال رسالة خاصة لعضو محدد
@bot.tree.command(name="send_dm", description="Send a direct message from the server to a specific user (Admins only)")
@app_commands.rename(target_user="user", message="text")
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
            color=EMBED_COLOR
        )
        embed.set_footer(text=f"أُرسلت بواسطة: {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
        await target_user.send(embed=embed)
        await interaction.response.send_message(f"✅ تم إرسال الرسالة بنجاح إلى {target_user.mention}!", ephemeral=True)
    except Exception:
        await interaction.response.send_message(f"❌ فشل الإرسال إلى {target_user.mention} (الخاص مغلق لديه).", ephemeral=True)

# 7. أمر لعبة الروليت (4 لاعبين)
@bot.tree.command(name="roulette", description="Start a 4-player spin game to randomly select a challenger and target")
@app_commands.rename(
    player1="first_player",
    player2="second_player",
    player3="third_player",
    player4="fourth_player"
)
@app_commands.guild_only()
async def roulette(
    interaction: discord.Interaction, 
    player1: discord.Member, 
    player2: discord.Member, 
    player3: discord.Member, 
    player4: discord.Member
):
    players = [player1, player2, player3, player4]
    
    if any(p.bot for p in players):
        await interaction.response.send_message("❌ لا يمكنك إدخال البوتات في اللعبة!", ephemeral=True)
        return

    embed = discord.Embed(
        title="🎊 لعبة الروليت",
        description="**اللاعبين المشاركين:**\n" + "\n".join([f"• {p.mention}" for p in players]) + "\n\n⏳ **جاري تدوير عجلة الحظ...** 🔄",
        color=EMBED_COLOR
    )
    await interaction.response.send_message(embed=embed)

    await asyncio.sleep(2.5)

    asker, target = random.sample(players, 2)

    result_embed = discord.Embed(
        title="🎉 نتيجة عجلة الحظ!",
        description=(
            f"🎯 **السائل:** {asker.mention}\n"
            f"👤 **المطلوب منه:** {target.mention}\n\n"
            f"يا {asker.mention}، دورك الحين! اختر (صراحة / أمر / لو خيروك) واسأل {target.mention} السؤال اللي تبيه! 💬"
        ),
        color=EMBED_COLOR
    )
    result_embed.set_thumbnail(url=target.display_avatar.url)
    
    await interaction.edit_original_response(embed=result_embed)

# تشغيل البوت
bot.run(os.environ.get("BOT_TOKEN"))
