def sanitize_url(content):
    if not content:
        return content
    elif 'spotify.com' in content:
        return content.split('?si=')[0]
    elif 'youtube.com' in content or 'youtu.be' in content:
        containsSI = '?si=' in content
        containsIS = '?is=' in content
        if containsSI or containsIS:
            sp = content.split('?si=' if containsSI else '?is=')
            if '&t=' in sp[1]:
                sp[1] = sp[1][sp[1].find('&t='):]
                return f'{sp[0]}{sp[1].replace("&t=", "?t=")}'
            else:
                return f'{sp[0]}'
    elif 'soundcloud.com' in content:
        return content.replace('?utm_source=clipboard&utm_medium=text&utm_campaign=social_sharing', '')

    return content


'''
https://youtu.be/nSOMOXcviZc?si=3aaa&t=59
https://youtu.be/nSOMOXcviZc?si=3aaa
https://youtube.com/watch?v=nSOMOXcviZc&si=3aaa&t=59
removes si= and is=
leaves t= and other query parameters intact

https://soundcloud.com/foggtracks/fogg-in-your-memory-ii-2?utm_source=clipboard&utm_medium=text&utm_campaign=social_sharing#t=0%3A15
converts to https://soundcloud.com/foggtracks/fogg-in-your-memory-ii-2#t=0%3A15
https://soundcloud.com/foggtracks/fogg-in-your-memory-ii-2?utm_source=clipboard&utm_medium=text&utm_campaign=social_sharing
converts to https://soundcloud.com/foggtracks/fogg-in-your-memory-ii-2

https://open.spotify.com/track/3bQoMbPYOvvseHaSOWAQ3Q?si=9aaaa
removes si=
'''