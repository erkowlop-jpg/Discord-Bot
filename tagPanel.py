import discord
from discord.ui import Button, View
import json
import os

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

class TagButtonView(View):
    def __init__(self, client):
        super().__init__(timeout=None)
        self.client = client

    @discord.ui.button(custom_id="tag_role_get", label="استلام رتبة التاق", style=discord.ButtonStyle.blurple)
    async def get_tag_role(self, interaction: discord.Interaction, button: Button):
        try:
            await interaction.response.defer(ephemeral=True)

            async def reply(title: str, desc: str):
                embed = discord.Embed(title=title, description=desc, color=discord.Color.from_rgb(30, 144, 255))
                await interaction.followup.send(embed=embed, ephemeral=True)

            settings = load_settings()
            guild_id = str(interaction.guild.id)
            guild_data = settings.get(guild_id, {})
            
            role_id = guild_data.get("role_id")
            tag_text = guild_data.get("tag_text", ".gg/soul")

            if not role_id:
                return reply("الاعدادات ناقصة", "لم يتم تحديد الرتبة بعد.\n\nيرجى من الإدارة تحديد الرتبة باستخدام الأمر:\n/setrole @الرتبة")

            role = interaction.guild.get_role(int(role_id))
            if not role:
                return reply("الرتبة غير موجودة", "الرتبة المحددة مسبقاً غير موجودة أو تم حذفها، يرجى إعادة تحديدها من قبل الإدارة.")

            me = interaction.guild.me
            if not me.guild_permissions.manage_roles or role.position >= me.top_role.position:
                return reply(
                    "صلاحيات ناقصة",
                    "لا أستطيع إعطاء هذه الرتبة.\n\nيرجى رفع رتبة البوت لتكون فوق رتبة التاق، ومنحه صلاحية إدارة الرتب (Manage Roles)."
                )

            # محاكاة فحص التاق (استبدل هذه القيمة بالتحقق الفعلي الخاص بك)
            has_tag = True 

            member = interaction.user

            if not has_tag:
                if role in member.roles:
                    await member.remove_roles(role, reason="إزالة رتبة تاق السيرفر - التاق غير موجود")
                return reply(
                    "التاق غير مضاف",
                    f"عذراً، يجب عليك وضع تاق السيرفر في بروفايلك الشخصي أولاً ثم المحاولة مرة أخرى.\n\nالتاق المطلوب: {tag_text}"
                )

            if role in member.roles:
                return reply("تنبيه", f"رتبة {role.mention} موجودة في ملفك الشخصي بالفعل.")

            await member.add_roles(role, reason="تم العثور على تاق السيرفر في البروفايل")

            return reply(
                "تم بنجاح",
                f"تم منحك رتبة {role.mention} بنجاح.\n\nملاحظة: في حال إزالة التاق من بروفايلك، سيتم سحب الرتبة منك تلقائياً."
            )

        except Exception as error:
            print(error)
            if interaction.response.is_done():
                await interaction.followup.send("حدث خطأ غير متوقع، حاول مرة أخرى لاحقاً.", ephemeral=True)
            else:
                await interaction.response.send_message("حدث خطأ غير متوقع، حاول مرة أخرى لاحقاً.", ephemeral=True)
