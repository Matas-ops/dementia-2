from googletrans import Translator

translator = Translator()


async def translate_string(text, dest='zh', src='en'):
    translation = await translator.translate(text, dest, src)
    print(f"Translated {text} to {translation.text}")

    return translation.text
