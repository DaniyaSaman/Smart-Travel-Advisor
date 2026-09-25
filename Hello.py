import sys
import time

def type_lyric(text, char_delay=0.06):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(char_delay)
    print()

def print_lyrics():
    lyrics = [
        "Teri nazron ka dil pe asar",
        "Tu mera mehboob hai yaar",
        "Teri ulfat mein jeeta hoon",
        "Tu ik tohfa hai Khuda ka"
    ]

    delays = [1.6, 1.4, 1.8, 2.1]

    print("\nNow Playing - Ehsaas")
    time.sleep(1.5)

    for i, line in enumerate(lyrics):
        type_lyric(line)
        time.sleep(delays[i])

print_lyrics()
