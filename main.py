import discord
from discord.ext import commands
import os

# إعدادات البوت والـ Intents الأساسية
intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

from tagPanel import TagButtonView

@bot.event
async def on_ready():
    print(f"Logged in successfully as {bot.user.name}")
    bot.add_view(TagButtonView(bot))
    try:
        # مزامنة أوامر الـ Slash مع ديسكورد لتظهر فوراً
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s).")
    except Exception as e:
        print(e)

# أمر الـ Slash الجديد
@bot.tree.command(name="sendpanel", description="إرسال لوحة استلام رتبة تاق السيرفر مع البنر")
@discord.app_commands.checks.has_permissions(administrator=True)
async def sendpanel(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    
    banner_path = "banner.png"
    
    if os.path.exists(banner_path):
        file = discord.File(banner_path, filename="banner.png")
        embed = discord.Embed(
            title="✨ | نظام استلام رتبة تاق السيرفر",
            description=(
                "**أهلاً بك في مجتمع SOUL!** 💙\n\n"
                "لحصولك على الرتبة الخاصة بتاق السيرفر، يرجى وضع التاق في بروفايلك الشخصي ثم الضغط على الزر بالأسفل.\n\n"
                "> 📌 **ملاحظة:** النظام يتحقق تلقائياً، وفي حال إزالة التاق ستتم إزالة الرتبة منك."
            ),
            color=discord.Color.from_rgb(30, 144, 255)
        )
        embed.set_image(url="attachment://banner.png")
        
        # إرسال البنر والزر للشات الحالي
        await interaction.channel.send(embed=embed, file=file, view=TagButtonView(bot))
        await interaction.followup.send("✅ تم إرسال اللوحة بنجاح!", ephemeral=True)
    else:
        embed = discord.Embed(
            title="استلام رتبة التاق",
            description="اضغط على الزر بالأسفل لاستلام رتبة تاق السيرفر.",
            color=discord.Color.blue()
        )
        await interaction.channel.send(embed=embed, view=TagButtonView(bot))
        await interaction.followup.send("⚠️ تم الإرسال بدون بنر (لعدم وجود ملف banner.png).", ephemeral=True)

TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)

