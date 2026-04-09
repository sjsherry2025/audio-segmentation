from alive_progress import alive_bar

def progressBar(total):
    return alive_bar(
        total=total,
        manual=False,
        force_tty=True,
        stats=True,
        elapsed=True,
    )

def customProgressBar(total, manual=False, force_tty=True, status = True, elapsed = False):
    return alive_bar(
        total=total,
        manual=manual,
        force_tty=force_tty,
        stats=status,
        elapsed=elapsed,
    )