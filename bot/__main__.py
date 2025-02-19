import shutil, psutil
import time
from signal import signal, SIGINT
from os import path as ospath, remove as osremove, execl as osexecl
from subprocess import run as srun, check_output
from datetime import datetime
from pyrogram import idle
from sys import executable
from telegram import InlineKeyboardMarkup
from telegram.ext import CommandHandler
from telegram import ParseMode

from bot import bot, app, dispatcher, updater, botStartTime, IGNORE_PENDING_REQUESTS, LOGGER, Interval, rss_session, INCOMPLETE_TASK_NOTIFIER, DB_URI, app, main_loop
from .helper.ext_utils.fs_utils import start_cleanup, clean_all, exit_clean_up
from .helper.ext_utils.telegraph_helper import telegraph
from .helper.ext_utils.bot_utils import get_readable_file_size, get_readable_time
from .helper.ext_utils.db_handler import DbManger
from .helper.telegram_helper.bot_commands import BotCommands
from .helper.telegram_helper.message_utils import sendMessage, sendMarkup, editMessage, sendLogFile
from .helper.telegram_helper.filters import CustomFilters
from .helper.telegram_helper.button_build import ButtonMaker

from .modules import authorize, list, cancel_mirror, mirror_status, mirror, clone, watch, shell, eval, delete, count, leech_settings, search, rss



def stats(update, context):
    currentTime = get_readable_time(time.time() - botStartTime)
    total, used, free = shutil.disk_usage('.')
    total = get_readable_file_size(total)
    used = get_readable_file_size(used)
    free = get_readable_file_size(free)
    sent = get_readable_file_size(psutil.net_io_counters().bytes_sent)
    recv = get_readable_file_size(psutil.net_io_counters().bytes_recv)
    cpuUsage = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    stats = f'<b>⌈➳ 💝 𝙾𝙽𝙻𝙸𝙽𝙴 𝚃𝙸𝙼𝙴 ⌚ : </b> <code>{currentTime}</code>\n' \
            f'<b>⌈➳ 📇 𝙳𝙸𝚂𝙺 𝚂𝙿𝙰𝙲𝙴 ☠️ : </b> <code>{total}</code>\n' \
            f'<b>⌈➳ 🗃 𝙳𝙸𝚂𝙺 𝚂𝙿𝙰𝙲𝙴 𝚄𝚂𝙴𝙳 📄 : </b> <code>{used}</code>\n' \
            f'<b>⌈➳ 💌 𝙳𝙸𝚂𝙺 𝚂𝙿𝙰𝙲𝙴 𝙵𝚁𝙴𝙴  : </b> <code>{free}</code>\n\n' \
            f'<b>⌈➳ 👻 𝚄𝙿𝙻𝙾𝙰𝙳 𝙳𝙰𝚃𝙰 💞 ... ⇆⏫ :</b> <code>{sent}</code>\n' \
            f'<b>⌈➳ 💃 𝙳𝙾𝚆𝙽𝙻𝙾𝙰𝙳 𝙳𝙰𝚃𝙰 💔 ... ⇆⏬ :</b> <code>{recv}</code>\n\n' \
            f'<b>⌈➳ 🖥 𝙲𝙿𝚄 𝚄𝚂𝙰𝙶𝙴↹  : </b> <code>{cpuUsage}% Ϟ</code>\n' \
            f'<b>⌈➳ 👰 𝚄𝚂𝙰𝙶𝙴 𝙾𝙵 𝙼𝙴𝙼𝙾𝚁𝚈  : </b> <code>{memory}%</code>\n' \
            f'<b>⌈➳ 👸 𝙳𝙸𝚂𝙺 𝚄𝚂𝙴𝙳 : </b> <code>{disk}% </code>\n' \
            f'<b>⌈➳ 🧰 𝙾𝚂 𝚂𝙿𝙰𝙲𝙴 : </b> <code>⇉7.2% ♲</code>\n' \
            f'<b>⌈➳ 📡 𝚂𝙴𝚁𝚅𝙴𝚁 : </b>Global ≼<code> </code><b>🌬 : </b><code>28%</code>\n<b>⌈➳ 💽 𝙳𝙸𝚂𝙺 𝙷𝙾𝚂𝚃 ⊫ : </b><code>SSD⋖</code>\n\n' \
            f'<b>⌈➳ 🧭 𝚃𝙸𝙼𝙴 𝚉𝙾𝙽𝙴 : </b><code>Asia/Kolkata</code>\n<b>⌈➳ 🇮🇳 𝚃𝙸𝙼𝙴 𝚂𝚃𝙰𝚃𝙴 : </b><code>INDIA-(GMT+:05:30)</code>\n<b>⌈➳ ☁ 𝙳𝚁𝙸𝚅𝙴 𝚂𝙿𝙰𝙲𝙴 => </b><code>495-TB𖥫</code>\n<b>⌈➳ 🛠 𝚃𝚂𝚁 : </b><code>2.53 GB</code><b> 🎄 : </b><code>76.48% ≛</code>\n<b>⌈➳ ✳ ᴘʏᴛʜᴏɴ ᴠᴇʀsɪᴏɴ : </b><code>3.9.7∝</code>\n<b>⌈➳ 🍥 ɪᴘ ᴀᴅᴅʀᴇss 𖣃 </b><code>Encrypted</code>\n\n<b>⌈➳ π- Bot Update Info..! </b>'"<a href='https://telegra.ph/file/9d9703906724616cf42ef.jpg'>😎</a>"
            
            
    sendMessage(stats, context.bot, update)


def start(update, context):
    buttons = ButtonMaker()
    buttons.buildbutton("🔥 Repo", "https://github.com/Spark-X-Cloud/SparkXcloud-Gdrive-MirrorBot")
    buttons.buildbutton("😎 Channel", "https://t.me/+R2czcPeMkUc1NDI1")
    reply_markup = InlineKeyboardMarkup(buttons.build_menu(2))
    if CustomFilters.authorized_user(update) or CustomFilters.authorized_chat(update):
        start_string = f'''
☠️ https://t.me/SparkXcloud        
This bot can mirror all your links to Google Drive!
Type /{BotCommands.HelpCommand} to get a list of available commands
'''
        sendMarkup(start_string, context.bot, update.message, reply_markup)
    else:
        sendMarkup(f"Oops! not an Authorized user.\nPlease deploy your own <b>SparkXcloud-Gdrive-MirrorBot</b>.", context.bot, update, reply_markup)

def restart(update, context):
    restart_message = sendMessage("Restarting, Please wait!..👻👻", context.bot, update.message)
    if Interval:
        Interval[0].cancel()
    alive.kill()
    clean_all()
    srun(["pkill", "-f", "gunicorn|aria2c|qbittorrent-nox"])
    srun(["python3", "update.py"])
    with open(".restartmsg", "w") as f:
        f.truncate(0)
        f.write(f"{restart_message.chat.id}\n{restart_message.message_id}\n")
    osexecl(executable, executable, "-m", "bot")


def ping(update, context):
    start_time = int(round(time() * 1000))
    reply = sendMessage("Starting_Ping ☠️", context.bot, update.message)
    end_time = int(round(time() * 1000))
    editMessage(f'{end_time - start_time} 𝙿𝙸𝙽𝙶 𝚄𝙿𝙳𝙰𝚃𝙴 𝙸𝚗𝚏𝚘 => 𝙼𝚂 🔥', reply)


def log(update, context):
    sendLogFile(context.bot, update.message)


help_string_telegraph = f'''<br>
<b>/{BotCommands.HelpCommand}</b>: To get this message
<br><br>
<b>/{BotCommands.MirrorCommand}</b> [download_url][magnet_link]: Start mirroring to Google Drive. Send <b>/{BotCommands.MirrorCommand}</b> for more help
<br><br>
<b>/{BotCommands.ZipMirrorCommand}</b> [download_url][magnet_link]: Start mirroring and upload the file/folder compressed with zip extension
<br><br>
<b>/{BotCommands.UnzipMirrorCommand}</b> [download_url][magnet_link]: Start mirroring and upload the file/folder extracted from any archive extension
<br><br>
<b>/{BotCommands.QbMirrorCommand}</b> [magnet_link][torrent_file][torrent_file_url]: Start Mirroring using qBittorrent, Use <b>/{BotCommands.QbMirrorCommand} s</b> to select files before downloading
<br><br>
<b>/{BotCommands.QbZipMirrorCommand}</b> [magnet_link][torrent_file][torrent_file_url]: Start mirroring using qBittorrent and upload the file/folder compressed with zip extension
<br><br>
<b>/{BotCommands.QbUnzipMirrorCommand}</b> [magnet_link][torrent_file][torrent_file_url]: Start mirroring using qBittorrent and upload the file/folder extracted from any archive extension
<br><br>
<b>/{BotCommands.LeechCommand}</b> [download_url][magnet_link]: Start leeching to Telegram, Use <b>/{BotCommands.LeechCommand} s</b> to select files before leeching
<br><br>
<b>/{BotCommands.ZipLeechCommand}</b> [download_url][magnet_link]: Start leeching to Telegram and upload the file/folder compressed with zip extension
<br><br>
<b>/{BotCommands.UnzipLeechCommand}</b> [download_url][magnet_link][torent_file]: Start leeching to Telegram and upload the file/folder extracted from any archive extension
<br><br>
<b>/{BotCommands.QbLeechCommand}</b> [magnet_link][torrent_file][torrent_file_url]: Start leeching to Telegram using qBittorrent, Use <b>/{BotCommands.QbLeechCommand} s</b> to select files before leeching
<br><br>
<b>/{BotCommands.QbZipLeechCommand}</b> [magnet_link][torrent_file][torrent_file_url]: Start leeching to Telegram using qBittorrent and upload the file/folder compressed with zip extension
<br><br>
<b>/{BotCommands.QbUnzipLeechCommand}</b> [magnet_link][torrent_file][torrent_file_url]: Start leeching to Telegram using qBittorrent and upload the file/folder extracted from any archive extension
<br><br>
<b>/{BotCommands.CloneCommand}</b> [drive_url][gdtot_url]: Copy file/folder to Google Drive
<br><br>
<b>/{BotCommands.CountCommand}</b> [drive_url][gdtot_url]: Count file/folder of Google Drive
<br><br>
<b>/{BotCommands.DeleteCommand}</b> [drive_url]: Delete file/folder from Google Drive (Only Owner & Sudo)
<br><br>
<b>/{BotCommands.WatchCommand}</b> [yt-dlp supported link]: Mirror yt-dlp supported link. Send <b>/{BotCommands.WatchCommand}</b> for more help
<br><br>
<b>/{BotCommands.ZipWatchCommand}</b> [yt-dlp supported link]: Mirror yt-dlp supported link as zip
<br><br>
<b>/{BotCommands.LeechWatchCommand}</b> [yt-dlp supported link]: Leech yt-dlp supported link
<br><br>
<b>/{BotCommands.LeechZipWatchCommand}</b> [yt-dlp supported link]: Leech yt-dlp supported link as zip
<br><br>
<b>/{BotCommands.LeechSetCommand}</b>: Leech settings
<br><br>
<b>/{BotCommands.SetThumbCommand}</b>: Reply photo to set it as Thumbnail
<br><br>
<b>/{BotCommands.RssListCommand}</b>: List all subscribed rss feed info
<br><br>
<b>/{BotCommands.RssGetCommand}</b>: [Title] [Number](last N links): Force fetch last N links
<br><br>
<b>/{BotCommands.RssSubCommand}</b>: [Title] [Rss Link] f: [filter]: Subscribe new rss feed
<br><br>
<b>/{BotCommands.RssUnSubCommand}</b>: [Title]: Unubscribe rss feed by title
<br><br>
<b>/{BotCommands.RssSettingsCommand}</b>: Rss Settings
<br><br>
<b>/{BotCommands.CancelMirror}</b>: Reply to the message by which the download was initiated and that download will be cancelled
<br><br>
<b>/{BotCommands.CancelAllCommand}</b>: Cancel all downloading tasks
<br><br>
<b>/{BotCommands.ListCommand}</b> [query]: Search in Google Drive(s)
<br><br>
<b>/{BotCommands.SearchCommand}</b> [query]: Search for torrents with API
<br>sites: <code>rarbg, 1337x, yts, etzv, tgx, torlock, piratebay, nyaasi, ettv</code><br><br>
<b>/{BotCommands.StatusCommand}</b>: Shows a status of all the downloads
<br><br>
<b>/{BotCommands.StatsCommand}</b>: Show Stats of the machine the bot is hosted on
'''

help = telegraph.create_page(
        title='😄 𝐒𝐩𝐚𝐫𝐤𝐗𝐜𝐥𝐨𝐮𝐝-𝐆𝐝𝐫𝐢𝐯𝐞-𝐌𝐢𝐫𝐫𝐨𝐫𝐁𝐨𝐭 𝐇𝐞𝐥𝐩 😄',
        content=help_string_telegraph,
    )["path"]

help_string = f'''
/{BotCommands.PingCommand}: Check how long it takes to Ping the Bot
/{BotCommands.AuthorizeCommand}: Authorize a chat or a user to use the bot (Can only be invoked by Owner & Sudo of the bot)
/{BotCommands.UnAuthorizeCommand}: Unauthorize a chat or a user to use the bot (Can only be invoked by Owner & Sudo of the bot)
/{BotCommands.AuthorizedUsersCommand}: Show authorized users (Only Owner & Sudo)
/{BotCommands.AddSudoCommand}: Add sudo user (Only Owner)
/{BotCommands.RmSudoCommand}: Remove sudo users (Only Owner)
/{BotCommands.RestartCommand}: Restart and update the bot
/{BotCommands.LogCommand}: Get a log file of the bot. Handy for getting crash reports
/{BotCommands.ShellCommand}: Run commands in Shell (Only Owner)
/{BotCommands.ExecHelpCommand}: Get help for Executor module (Only Owner)
'''

def bot_help(update, context):
    button = ButtonMaker()
    button.buildbutton("📝 ᴄᴍᴅ-ɪɴғᴏ ", f"https://telegra.ph/{help}")
    reply_markup = InlineKeyboardMarkup(button.build_menu(1))
    sendMarkup(help_string, context.bot, update.message, reply_markup)

botcmds = [

        (f'{BotCommands.MirrorCommand}', 'Mirror'),
        (f'{BotCommands.ZipMirrorCommand}','Mirror and upload as zip'),
        (f'{BotCommands.UnzipMirrorCommand}','Mirror and extract files'),
        (f'{BotCommands.QbMirrorCommand}','Mirror torrent using qBittorrent'),
        (f'{BotCommands.QbZipMirrorCommand}','Mirror torrent and upload as zip using qb'),
        (f'{BotCommands.QbUnzipMirrorCommand}','Mirror torrent and extract files using qb'),
        (f'{BotCommands.WatchCommand}','Mirror yt-dlp supported link'),
        (f'{BotCommands.ZipWatchCommand}','Mirror yt-dlp supported link as zip'),
        (f'{BotCommands.CloneCommand}','Copy file/folder to Drive'),
        (f'{BotCommands.LeechCommand}','Leech'),
        (f'{BotCommands.ZipLeechCommand}','Leech and upload as zip'),
        (f'{BotCommands.UnzipLeechCommand}','Leech and extract files'),
        (f'{BotCommands.QbLeechCommand}','Leech torrent using qBittorrent'),
        (f'{BotCommands.QbZipLeechCommand}','Leech torrent and upload as zip using qb'),
        (f'{BotCommands.QbUnzipLeechCommand}','Leech torrent and extract using qb'),
        (f'{BotCommands.LeechWatchCommand}','Leech yt-dlp supported link'),
        (f'{BotCommands.LeechZipWatchCommand}','Leech yt-dlp supported link as zip'),
        (f'{BotCommands.CountCommand}','Count file/folder of Drive'),
        (f'{BotCommands.DeleteCommand}','Delete file/folder from Drive'),
        (f'{BotCommands.CancelMirror}','Cancel a task'),
        (f'{BotCommands.CancelAllCommand}','Cancel all downloading tasks'),
        (f'{BotCommands.ListCommand}','Search in Drive'),
        (f'{BotCommands.LeechSetCommand}','Leech settings'),
        (f'{BotCommands.SetThumbCommand}','Set thumbnail'),
        (f'{BotCommands.StatusCommand}','Get mirror status message'),
        (f'{BotCommands.StatsCommand}','Bot usage stats'),
        (f'{BotCommands.PingCommand}','Ping the bot'),
        (f'{BotCommands.RestartCommand}','Restart the bot'),
        (f'{BotCommands.LogCommand}','Get the bot Log'),
        (f'{BotCommands.HelpCommand}','Get detailed help')
    ]

def main():
    # bot.set_my_commands(botcmds)
    start_cleanup()
    if INCOMPLETE_TASK_NOTIFIER and DB_URI is not None:
        notifier_dict = DbManger().get_incomplete_tasks()
        if notifier_dict:
            for cid, data in notifier_dict.items():
                if ospath.isfile(".restartmsg"):
                    with open(".restartmsg") as f:
                        chat_id, msg_id = map(int, f)
                    msg = '😎Restarted successfully❗'
                else:
                    msg = 'Bot Restarted!'
                for tag, links in data.items():
                     msg += f"\n\n{tag}: "
                     for index, link in enumerate(links, start=1):
                         msg += f" <a href='{link}'>{index}</a> |"
                         if len(msg.encode()) > 4000:
                             if '😎Restarted successfully❗' in msg and cid == chat_id:
                                 bot.editMessageText(msg, chat_id, msg_id, parse_mode='HTMl', disable_web_page_preview=True)
                                 osremove(".restartmsg")
                             else:
                                 bot.sendMessage(cid, msg, 'HTML')
                             msg = ''
                if '😎Restarted successfully❗' in msg and cid == chat_id:
                     bot.editMessageText(msg, chat_id, msg_id, parse_mode='HTMl', disable_web_page_preview=True)
                     osremove(".restartmsg")
                else:
                    bot.sendMessage(cid, msg, 'HTML')

    if ospath.isfile(".restartmsg"):
        with open(".restartmsg") as f:
            chat_id, msg_id = map(int, f)
        bot.edit_message_text("😎Restarted successfully❗", chat_id, msg_id)
        osremove(".restartmsg")

    start_handler = CommandHandler(BotCommands.StartCommand, start, run_async=True)
    ping_handler = CommandHandler(BotCommands.PingCommand, ping,
                                  filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
    restart_handler = CommandHandler(BotCommands.RestartCommand, restart,
                                     filters=CustomFilters.owner_filter | CustomFilters.sudo_user, run_async=True)
    help_handler = CommandHandler(BotCommands.HelpCommand,
                                  bot_help, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
    stats_handler = CommandHandler(BotCommands.StatsCommand,
                                   stats, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
    log_handler = CommandHandler(BotCommands.LogCommand, log, filters=CustomFilters.owner_filter | CustomFilters.sudo_user, run_async=True)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(ping_handler)
    dispatcher.add_handler(restart_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(stats_handler)
    dispatcher.add_handler(log_handler)
    updater.start_polling(drop_pending_updates=IGNORE_PENDING_REQUESTS)
    LOGGER.info("💥𝐁𝐨𝐭 𝐒𝐭𝐚𝐫𝐭𝐞𝐝❗")
    signal(SIGINT, exit_clean_up)

main()
app.start()

main_loop.run_forever()