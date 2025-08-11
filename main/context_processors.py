from .utils import get_text


def translations(request):
    lang = request.LANGUAGE_CODE if hasattr(request, 'LANGUAGE_CODE') else 'uz'
    return {
        't': get_text(lang)
    }