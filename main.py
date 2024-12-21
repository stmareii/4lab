import telebot
import requests
import webbrowser


bot = telebot.TeleBot("7581133164:AAEiGl1U5uaGAA_mXvbHwpbGmBBMQ-GbHFk")
API = "90e44b52ef895c6ccddd01d5c924de27"
URL = "http://ws.audioscrobbler.com/2.0/"



@bot.message_handler(commands=["start", "meow", "hello"])
def start(message):
    bot.send_message(
        message.chat.id,
        (
            "Приветик! Я ботик, который может найти справочную информацию о любой (нет) песне!\n"
            "Вообщем отправь мне название песни и исполнителя вот так:\n"
            '"Название песни + исполнитель"'
        ),
        parse_mode="Markdown",
    )


def get_track(song, artist):
    params = {
        "method": "track.getInfo",
        "api_key": API,
        "artist": artist,
        "track": song,
        "format": "json",
    }

    response = requests.get(URL, params=params)
    info = response.json()

    if "track" in info:
        track = info["track"]
        track_name = track.get("name", "Неизвестно")
        artist_name = track.get("artist", {}).get("name", "Неизвестно")
        album_name = track.get("album", {}).get("title", "Не указан")
        playcount = track.get("playcount", "Нет данных")
        listeners = track.get("listeners", "Нет данных")
        track_url = track.get("url", "Нет ссылки")

        return (
            f"🎵 *Название:* {track_name}\n"
            f"🎤 *Исполнитель:* {artist_name}\n"
            f"💿 *Альбом:* {album_name}\n"
            f"👥 *Котят (слушателей):* {listeners}\n"
            f"▶️ *Прослушивания:* {playcount}\n"
            f"🌐 [Ссылка на Last.fm]({track_url})"
        )
    else:
        return "Прости! Не удалось найти информацию... Может ты что-то неправильно ввел? ┐(￣∀￣)┌"


@bot.message_handler(commands=["ur_favourite_song"])
def cat_fav_song(message):
    bot.reply_to(
        message,
        (
            "Ой, я так рад, что ты спросил про мою любимую песню! Вот она:"
            "[ur_favourite_song](https://www.last.fm/music/lvusm/_/meow)"
        ),
        parse_mode="Markdown",
    )


@bot.message_handler(commands=["site", "last.fm"])
def site(message):
    bot.send_message(message.chat.id, ("Секундочку и ты уже на сайтике! Хихи-хаха 😈"))
    webbrowser.open("https://www.last.fm/home")


def get_top_tracks(artist_name):
    params = {
        'method': 'artist.getTopTracks',
        'artist': artist_name,
        'api_key': API,
        'format': 'json'
    }
    response = requests.get(URL, params=params)
    data = response.json()
    
    if 'toptracks' in data:
        tracks = data['toptracks']['track']
        return [{
            'name': track['name'],
            'listeners': track.get('listeners', '0'),
            'url': track['url']
        } for track in tracks[:10]]  #топ 10 возьму, мб поменяю
    else:
        return None

@bot.message_handler(commands=['toptracks'])
def send_top_tracks(message):
    artist_name = message.text.replace('/toptracks', '').strip()
    if artist_name:
        top_tracks = get_top_tracks(artist_name)
        if top_tracks:
            response = f"🎤 *Топ-10 треков для {artist_name}:*\n"
            for idx, track in enumerate(top_tracks, 1):
                response += f"{idx}. 🎵 [{track['name']}]({track['url']}) (Слушатели: {track['listeners']})\n"
            bot.reply_to(message, response, parse_mode='Markdown')
        else:
            bot.reply_to(message, "Не удалось найти топовые треки для указанного исполнителя.")
    else:
        bot.reply_to(message, "Введи имя исполнителя после команды! /toptracks.")


@bot.message_handler(func=lambda message: True)
def handle(message):
    user_message = message.text
    if "+" in user_message:
        song2, artist2 = map(str.strip, user_message.split("+", 1))
        result = get_track(song2, artist2)
        bot.reply_to(message, result, parse_mode="Markdown")
    else:
        bot.reply_to(
            message,
            (
                "Ты не так отправил запрос! Обязателен формат:\n"
                '"Название песни + исполнитель",\n я по-другому не умею...	(っ˘̩╭╮˘̩)っ'
            ),
        )



bot.infinity_polling()
