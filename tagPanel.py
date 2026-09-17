import discord
from discord.ui import Button, View

class TagButtonView(View):
    def __init__(self, client):
        super().__init__(timeout=None)
        self.client = client

    @discord.ui.button(custom_id="tag_role_get", label="استلام الرتبة", style=discord.ButtonStyle.success)
    async def get_tag_role(self, interaction: discord.Interaction, button: Button):
        try:
            await interaction.response.defer(ephemeral=True)

            async def reply(title: str, desc: str):
                embed = discord.Embed(title=title, description=desc, color=discord.Color.blue())
                await interaction.followup.send(embed=embed, ephemeral=True)

            # استبدل الرقم هذا بـ ID الرتبة حق مميزات التاق في سيرفرك
            role_id = 123456789012345678  
            tag_text = "SOUL" # التاق المطلوب وضعه في البروفايل

            role = interaction.guild.get_role(role_id)
            if not role:
                return await reply("الاعدادات ناقصة", "❌ لم يتم تحديد الرتبة بعد أو الرتبة محذوفة.")

            me = interaction.guild.me
            if not me.guild_permissions.manage_roles or role.position >= me.top_role.position:
                return await reply(
                    "صلاحيات ناقصة",
                    "❌ لا أستطيع اعطاء هذه الرتبة، ارفع رتبة البوت فوقها وأعطني صلاحية Manage Roles."
                )

            member = interaction.user
            # ضع هنا كود التحقق من التاق الخاص بك
            has_tag = True 

            if not has_tag:
                if role in member.roles:
                    await member.remove_roles(role, reason="ازالة رتبة تاق السيرفر - التاق غير موجود")
                return await reply(
                    "ما عندك التاق",
                    f"❌ لازم تحط تاق السيرفر في بروفايلك ثم اضغط الزر مرة ثانية.\n\n**التاق المطلوب:** `{tag_text}`"
                )

            if role in member.roles:
                return await reply("عندك الرتبة", f"✅ رتبة {role.mention} موجودة عندك أصلاً.")

            await member.add_roles(role, reason="تاق السيرفر موجود في البروفايل")

            return await reply(
                "تم بنجاح",
                f"✅ تم اعطاؤك رتبة {role.mention}\n\n> ملاحظة: لو شلت التاق أو غيرته لسيرفر ثاني تنسحب الرتبة تلقائياً."
            )

        except Exception as error:
            print(error)
            if interaction.response.is_done():
                await interaction.followup.send("❌ صار خطأ، حاول مرة ثانية.", ephemeral=True)
            else:
                await interaction.response.send_message("❌ صار خطأ، حاول مرة ثانية.", ephemeral=True)
