

# 5. أمر البرودكاست
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

# 6. أمر إرسال رسالة خاصة
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

