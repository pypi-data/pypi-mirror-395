from django.utils.formats import number_format


def timedelta_format(value, force_grouping=False):
    pieces = []
    seconds = value.total_seconds()

    if seconds >= 3600:
        hours = int(seconds // 3600)
        seconds = seconds - hours * 3600
        pieces.append(
            "%s h" % number_format(hours, force_grouping=force_grouping)
        )

    if seconds >= 60:
        minutes = int(seconds // 60)
        seconds = seconds - minutes * 60
        pieces.append("%d min" % minutes)

    if seconds > 0:
        pieces.append("%d s" % seconds)

    return " ".join(pieces)


def duration_format(value, empty_text="—"):
    return timedelta_format(value, force_grouping=True) if value else empty_text


def distance_format(value, unit="km", empty_text="—"):
    return (
        "%s %s"
        % (
            number_format(value, decimal_pos=2, force_grouping=True),
            unit,
        )
        if value
        else empty_text
    )
