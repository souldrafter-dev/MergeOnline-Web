import os
from pydub import AudioSegment

# выравнивание RMS-громкости трека
def match_target_amplitude(sound, target_dBFS):          # Функция выравнивающая звук аудиодорожки
    change_in_dBFS = target_dBFS - sound.dBFS            # Находим сколько нужно добавить или вычесть децибел для выравнивания
    return sound.apply_gain(change_in_dBFS)

def merge_fnf_tracks(inst_bytes, voice_bytes, use_rms: bool):
    # Принимаем файлы в виде байтов из памяти сервера, чтобы склеить и вернуть готовый обьект
    inst = AudioSegment.from_file(inst_bytes) # Сам процесс загрузки файлов из байтов памяти, не сохраняя на жесткий диск
    voice = AudioSegment.from_file(voice_bytes) 
    
    # Проверяем состояние галочки что передал пользователь с сайта
    if use_rms:
        # Если галочка стоит то выполняется выравнивание звука
        inst = match_target_amplitude(inst, -20.0)
        voice = match_target_amplitude(voice, -20.0)

    # Накладываем дорожки друг на друга
    combined = inst.overlay(voice, position=0)

    return combined