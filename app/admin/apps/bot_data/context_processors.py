from .models import BotLead, BotPotentialLead

def bot_data_context(request):
    if request.user.is_authenticated:
        return {
            'leads_count': BotLead.objects.count(),
            'potential_leads_count': BotPotentialLead.objects.count(),
        }
    return {}