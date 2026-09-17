import discord
from discord.ext import commands

# إعدادات البوت والـ Intents
intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# استدعاء ملف الزر
from tagPanel import TagButtonView

@bot.event
async def on_ready():
    print(f"تم تسجيل الدخول بنجاح باسم: {bot.user.name}")
    bot.add_view(TagButtonView(bot))

@bot.command()
@commands.has_permissions(administrator=True)
async def sendpanel(ctx, channel: discord.TextChannel = None):
    channel = channel or ctx.channel
    
    # حذف رسالة الأمر لترتيب الشات
    try:
        await ctx.message.delete()
    except:
        pass

    # مميزات الرتبة
    perks_text = (
        "**💎 | مميزات الرتبة:**\n"
        "• وصول لروم الخاصات الفخمة والـ Giveaways الحصرية.\n"
        "• إمكانية إرسال الصور والروابط بحرية أكبر.\n"
        "• لون خاص واسمك يرتفع فوق الأعضاء.\n"
        "• دعمك المستمر لمجتمعنا الراقي 💙"
    )

    embed = discord.Embed(
        title="✨ | نظام استلام رتبة تاق سيرفر SOUL",
        description=(
            "**أهلاً بك يا مبدع في مجتمع SOUL!** 🌟\n\n"
            "ضع تاق السيرفر في بروفايلك واضغط على الزر بالأسفل لاستلام رتبتك فوراً وتفعيل المميزات.\n\n"
            f"{perks_text}\n\n"
            "> 📌 **ملاحظة:** النظام يفحص التاق تلقائياً، وإذا أزلته ستنسحب الرتبة تلقائياً."
        ),
        color=discord.Color.from_rgb(30, 144, 255)
    )
    
    # استخدام رابط البنر المباشر
    banner_url = "https://cdn.discordapp.com/attachments/1550166048920313996/1550176588333719742/7-1.png?ex=6aad61f3&is=6aac1073&hm=e8cdabedc9358596fa2cf8befa89bfebe10ad6555c1394d1494f5c2f3369494a&"
    embed.set_image(url=banner_url)
    
    await channel.send(embed=embed, view=TagButtonView(bot))

# ضع توكن البوت الخاص بك هنا بين علامتي التنصيص
bot.run(TOKEN)
