import discord
from discord.ext import commands
import os
import json

SETTINGS_FILE = "settings.json"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

def save_settings(data):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=4)

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
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s).")
    except Exception as e:
        print(e)

# 1. أمر تحديد الرتبة عبر السلاش
@bot.tree.command(name="setrole", description="تحديد رتبة التاق الخاصة بالسيرفر")
@discord.app_commands.describe(role="اختر رتبة التاق التي ستمنح للعضويات")
@discord.app_commands.checks.has_permissions(administrator=True)
async def setrole(interaction: discord.Interaction, role: discord.Role):
    settings = load_settings()
    guild_id = str(interaction.guild.id)
    
    if guild_id not in settings:
        settings[guild_id] = {}
        
    settings[guild_id]["role_id"] = str(role.id)
    save_settings(settings)
    
    await interaction.response.send_message(f"تم تعيين رتبة تاق السيرفر بنجاح لتكون: {role.mention}", ephemeral=True)

# 2. أمر إرسال اللوحة بالبنر والنص الرسمي بدون إيموجيات
@bot.tree.command(name="sendpanel", description="إرسال لوحة استلام رتبة تاق السيرفر مع البنر")
@discord.app_commands.checks.has_permissions(administrator=True)
async def sendpanel(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    
    banner_path = "banner.png"
    
    embed = discord.Embed(
        title="نظام التحقق من تاق سيرفر SOUL",
        description=(
            "عضو SOUL الكريم،\n\n"
            "حرصاً منا على تنظيم السيرفر وتقدير الأعضاء الداعمين، تم تفعيل النظام التلقائي لمنح رتبة التاق الخاصة بالسيرفر.\n\n"
            "--- \n\n"
            "شروط وضوابط الحصول على الرتبة:\n"
            "• وضع التاق: يجب إدراج تاق السيرفر في الملف الشخصي (البروفايل).\n"
            "• التحقق التلقائي: يتم التحقق من وجود التاق بشكل آلي فور الضغط على زر الاستلام.\n"
            "• الاستمرارية: في حال إزالة التاق من الملف الشخصي، سيقوم النظام بسحب الرتبة تلقائياً.\n\n"
            "--- \n\n"
            "خطوات الاستلام:\n"
            "1. قم بإضافة تاق السيرفر في بروفايلك الشخصي.\n"
            "2. اضغط على الزر أدناه (استلام رتبة التاق).\n\n"
            "ملاحظة: لأي استفسارات أو مواجهة مشاكل تقنية، يرجى فتح تذكرة دعم فني لدى الإدارة."
        ),
        color=discord.Color.from_rgb(30, 144, 255)
    )
    
    if os.path.exists(banner_path):
        file = discord.File(banner_path, filename="banner.png")
        embed.set_image(url="attachment://banner.png")
        await interaction.channel.send(embed=embed, file=file, view=TagButtonView(bot))
    else:
        await interaction.channel.send(embed=embed, view=TagButtonView(bot))
        
    await interaction.followup.send("تم إرسال اللوحة بنجاح إلى الشات.", ephemeral=True)

TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)

