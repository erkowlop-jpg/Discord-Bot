import os
import asyncio
import discord
from discord.ext import commands
from datetime import timedelta

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# معرف الرتبة المسموح لها باستخدام الأوامر
ALLOWED_ROLE_ID = 1554391694068420728

@bot.event
async def on_ready():
    print(f'البوت متصل حالياً باسم: {bot.user}')

# ==========================================
# 1. أمر القوانين (يرسل في الروم مباشرة)
# اختصارات: !قوانين ، !القوانين ، !rules
# ==========================================
@bot.command(name="قوانين", aliases=["القوانين", "rules"])
@commands.has_role(ALLOWED_ROLE_ID)
async def rules(ctx):
    # مسح أمر الاستدعاء لتنظيف الروم
    try:
        await ctx.message.delete()
    except Exception:
        pass

    rules_description = (
        "⚖️ **اللوائح والتنظيمات العامة للسيرفر**\n"
        "يرجى الالتزام التام بالتالي لتجنب اتخاذ الإجراءات الإدارية:\n\n"
        "**1 ─ الاحترام المتبادل:** يمنع السب، الشتم، أو التلفظ بألفاظ غير لائمة بأي شكل.\n\n"
        "**2 ─ الأنشطة التجارية:** يمنع البيع، الشراء، والتجارة بكافة أنواعها داخل السيرفر.\n\n"
        "**3 ─ الإعلانات والترويج:** يمنع نشر إعلانات لسيرفرات، متاجر، أو حسابات شخصية.\n\n"
        "**4 ─ المواضيع الحساسة:** يمنع الخوض في النقاشات السياسية، الدينية، أو المذهبية.\n\n"
        "**5 ─ المحتوى المخالف:** يمنع نشر أو وضع صور/مقاطع مخلة بالأدب أو إلحادية.\n\n"
        "**6 ─ تشفير الكلمات:** يمنع التحايل بتشفير المصطلحات المحظورة (تطبق العقوبة بغض النظر عن النية).\n\n"
        "**7 ─ الروابط والوسائط:** يمنع مشاركة الروابط العشوائية أو غير الموثوقة.\n\n"
        "**8 ─ التسول وطلب المال:** يمنع طلب الأموال أو الأغراض سواء داخل الألعاب أو الواقع.\n\n"
        "**9 ─ مكافحة العنصرية:** يمنع التمييز أو السخرية (العرق، الدين، المادة، طريقة الكلام، الأمراض).\n\n"
        "**10 ─ الرتب والتواصل الإداري:** يمنع طلب الرتب، ويمنع إزعاج الإدارة العليا إلا للضرورة القصوى.\n\n"
        "**11 ─ السلوك العام:** يمنع السبام، التشهير، ذِكر سيرفرات أخرى، أو انتحال الشخصيات.\n\n"
        "**12 ─ الخصوصية:** مشاركة الصور/المعلومات الخاصة للآخرين تعرضك للحظر النهائي (Ban).\n\n"
        "**13 ─ التخصص والرومات الصوتية:** التزم بتخصص كل روم، ويمنع استخدام المايك للفتيات في الرومات العامة.\n\n"
        "──────────────────────────────\n"
        "⚠️ **تنبيهات إدارية مهمة:**\n"
        "• عدم علمك بالقوانين لا يعفيك من المسؤولية والعقوبة.\n"
        "• المتسبب الأول هو المسؤول المباشر عن تصاعد المشكلة.\n"
        "• الاستهانة أو المزاح أثناء التحقيق الإداري يضاعف العقوبة."
    )

    my_embed = discord.Embed(
        title="📜 قواعد وأنظمة السيرفر | Server Rules",
        description=rules_description,
        color=discord.Color.dark_grey()
    )

    my_embed.set_image(url="https://cdn.discordapp.com/attachments/1555159023924289536/1555171435432124476/1790756933339.jpg?backend=b2&ex=6abf8dc3&is=6abe3c43&hm=86d6dc594bee62e9d3a9c9706f180890058761bd8837c833db3e6706f7b2f6db&")
    my_embed.set_footer(text="by zilks المز")

    # إرسال لوحة القوانين في الروم مباشرة
    await ctx.send(embed=my_embed)


# ==========================================
# 2. أمر الحذف / الكلير
# اختصارات: !مسح ، !حذف ، !clear
# ==========================================
@bot.command(name="مسح", aliases=["حذف", "clear", "احذف"])
@commands.has_role(ALLOWED_ROLE_ID)
async def clear(ctx, amount: int = 10):
    await ctx.channel.purge(limit=amount + 1)
    confirm = await ctx.send(f"من الرسائل بنجاح هذا العدد تم حذف `{amount}`")
    await asyncio.sleep(3)
    await confirm.delete()


# ==========================================
# 3. أمر التايم أوت / اسكات
# اختصارات: !ميوت ، !عزل ، !timeout
# ==========================================
@bot.command(name="ميوت", aliases=["اصه", "اسكت"])
@commands.has_role(ALLOWED_ROLE_ID)
async def timeout(ctx, member: discord.Member, duration: str = "10m", *, reason: str = "غير محدد"):
    unit = duration[-1]
    try:
        time_val = int(duration[:-1])
    except ValueError:
        await ctx.send("❌ الصيغة غلط يقلبي! استخدم مثلاً: `10m` أو `1h` أو `1d`")
        return

    if unit == "s":
        delta = timedelta(seconds=time_val)
    elif unit == "m":
        delta = timedelta(minutes=time_val)
    elif unit == "h":
        delta = timedelta(hours=time_val)
    elif unit == "d":
        delta = timedelta(days=time_val)
    else:
        await ctx.send("❌ الوحدة غير صحيحة! استخدم: (s(ثانيه),m(دقيقة),h(ساعة),d(يوم))")
        return

    try:
        await member.timeout(delta, reason=reason)
        await ctx.send(f"🔇 تم إعطاء تايم أوت لـ {member.mention} لمدة `{duration}` | السبب: **{reason}**")
    except Exception as e:
        await ctx.send(f"❌ تعذر تطبيق التايم أوت: {e}")


# ==========================================
# معالجة الأخطاء
# ==========================================
@rules.error
@clear.error
@timeout.error
async def command_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        msg = await ctx.send("❌ ماعندك صلاحية لاستخدام هذا الأمر يغالي.")
        await asyncio.sleep(4)
        await msg.delete()
    elif isinstance(error, commands.MissingRequiredArgument):
        msg = await ctx.send("❌ تأكد من كتابة الأمر بالشكل الصحيح مع المنشن أو العدد.")
        await asyncio.sleep(4)
        await msg.delete()

TOKEN = os.getenv("BOT_TOKEN")
bot.run(TOKEN)
