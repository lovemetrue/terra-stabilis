from .models import BotLead

def bot_data_context(request):
    if request.user.is_authenticated:
        return {
            'leads_count': BotLead.objects.count(),
        }
    return {}