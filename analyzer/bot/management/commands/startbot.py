from django.core.management import BaseCommand

from analyzer.bot.bot import bot


class Command(BaseCommand):
    help = 'Starts telegram bot'

    def handle(self, *args, **options):
        bot.polling()
