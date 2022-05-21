#https://github.com/Spark-X-Cloud/SparkXcloud-Gdrive-MirrorBot

from telegram import Message
import os
from subprocess import run
from bot.helper.ext_utils.shortenurl import short_url
from telegram.ext import CommandHandler
from bot import LOGGER, dispatcher, app
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.message_utils import editMessage, sendMessage
from bot.helper.ext_utils.telegraph_helper import telegraph


def mediainfo(update, context):
    message:Message = update.effective_message
    mediamessage = message.reply_to_message
    # mediainfo control +
    process = run('mediainfo', capture_output=True, shell=True)
    if process.stderr.decode(): return LOGGER.error("mediainfo not installed. Read readme.")
    # mediainfo control -
    help_msg = "\n<b>𝐁𝐲 𝐫𝐞𝐩𝐥𝐲𝐢𝐧𝐠 𝐭𝐨 𝐦𝐞𝐬𝐬𝐚𝐠𝐞 (including media):</b>"
    help_msg += f"\n<code>/{BotCommands.MediaInfoCommand}" + " {message}" + "</code>"
    if not mediamessage: return sendMessage(help_msg, context.bot, update)
    file = None
    media_array = [mediamessage.document, mediamessage.video, mediamessage.audio, mediamessage.document, \
        mediamessage.video, mediamessage.photo, mediamessage.audio, mediamessage.voice, \
        mediamessage.animation, mediamessage.video_note, mediamessage.sticker]
    for i in media_array:
        if i is not None:
            file = i
            break
    if not file: return sendMessage(help_msg, context.bot, update)
    sent = sendMessage('𝐑𝐮𝐧𝐧𝐢𝐧𝐠 𝐦𝐞𝐝𝐢𝐚𝐢𝐧𝐟𝐨. 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠 𝐲𝐨𝐮𝐫 𝐟𝐢𝐥𝐞.', context.bot, update)
    try:
        VtPath = os.path.join("Mediainfo", str(message.from_user.id))
        if not os.path.exists("Mediainfo"): os.makedirs("Mediainfo")
        if not os.path.exists(VtPath): os.makedirs(VtPath)
        try: filename = os.path.join(VtPath, file.file_name)
        except: filename = None
        file = app.download_media(message=file, file_name=filename)
    except Exception as e:
        LOGGER.error(e)
        try: os.remove(file)
        except: pass
        file = None
    if not file: return editMessage("𝐄𝐫𝐫𝐨𝐫 𝐰𝐡𝐞𝐧 𝐝𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠. 𝐓𝐫𝐲 𝐚𝐠𝐚𝐢𝐧 𝐥𝐚𝐭𝐞𝐫.", sent)
    cmd = f'mediainfo "{os.path.basename(file)}"'
    LOGGER.info(cmd)
    process = run(cmd, capture_output=True, shell=True, cwd=VtPath)
    reply = f"<b>MediaInfo: {os.path.basename(file)}</b><br>"
    stderr = process.stderr.decode()
    stdout = process.stdout.decode()
    if len(stdout) != 0:
        reply += f"<b>Stdout:</b><br><br><pre>{stdout}</pre><br>"
        # LOGGER.info(f"mediainfo - {cmd} - {stdout}")
    if len(stderr) != 0:
        reply += f"<b>Stderr:</b><br><br><pre>{stderr}</pre>"
        # LOGGER.error(f"mediainfo - {cmd} - {stderr}")
    try: os.remove(file)
    except: pass
    help = telegraph.create_page(title='MediaInfo', content=reply)["path"]
    editMessage(short_url(f"https://telegra.ph/{help}"), sent)


mediainfo_handler = CommandHandler(BotCommands.MediaInfoCommand, mediainfo,
    filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
dispatcher.add_handler(mediainfo_handler)