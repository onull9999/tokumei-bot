import discord
from discord import app_commands
from discord.ext import commands
import asyncio  # asyncioをインポート

# Botのトークンを入力
TOKEN = "MTMyNTY4NTgyMzQ0NTc5NDgyNw.GXpyC9.61zrtnEaJFgHBdb-N7EVhgxHYIgjL8WgQchbhA"

# 指定したチャンネルID
TARGET_CHANNEL_ID = 1326010589847486545

# Botの初期設定
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Botの準備完了時の処理
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

# スラッシュコマンドの実装
@bot.tree.command(name="a", description="送信したいメッセージをBotが送ります")
async def send_message(interaction: discord.Interaction, message: str):
    # インタラクションに即応答を返す
    await interaction.response.send_message("メッセージを送信しました！", ephemeral=True)

    # 指定したチャンネルIDを使ってチャンネルを取得
    target_channel = bot.get_channel(TARGET_CHANNEL_ID)

    if target_channel:
        # チャンネルが見つかった場合、「送信しました」メッセージを送信
        await target_channel.send("送信しました")
    else:
        # チャンネルが見つからなかった場合のエラーメッセージ
        await interaction.channel.send("指定したチャンネルが見つかりませんでした。")

    # メッセージを送ったチャンネルに通常のメッセージとして送信
    await interaction.channel.send(message)

    # 3秒後に「メッセージを送信しました！」メッセージを削除
    await asyncio.sleep(1)  # 3秒待機
    await interaction.delete_original_response()  # インタラクションの元のメッセージを削除

# Botの起動
bot.run(TOKEN)
