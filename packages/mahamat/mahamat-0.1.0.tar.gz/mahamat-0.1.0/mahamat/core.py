import sys
import time

def progress(iterable, prefix="Progress", length=40):
    """
    iterable : liste, range, générateur, etc.
    prefix : texte affiché avant la barre
    length : longueur de la barre (40 chars par défaut)
    """

    try:
        count = len(iterable)
    except TypeError:
        iterable = list(iterable)
        count = len(iterable)

    start_time = time.time()

    for i, item in enumerate(iterable, start=1):
        percent = i / count
        filled = int(length * percent)
        bar = "█" * filled + "░" * (length - filled)

        elapsed = time.time() - start_time
        eta = (elapsed / percent) - elapsed if percent > 0 else 0

        sys.stdout.write(
            f"\r{prefix} |{bar}| {percent*100:5.1f}% "
            f"( {i}/{count} ) ETA: {eta:4.1f}s"
        )
        sys.stdout.flush()

        yield item

    sys.stdout.write("\n")
    sys.stdout.flush()
