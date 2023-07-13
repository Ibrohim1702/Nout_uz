from django.core.management import BaseCommand
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

from Nout_uz.settings import TOKEN

from Tg_Nout_uz.views import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        updater = Updater(TOKEN)

        updater.dispatcher.add_handler(CommandHandler('start', start))
        updater.dispatcher.add_handler(MessageHandler(Filters.text, message_handler))
        updater.dispatcher.add_handler(MessageHandler(Filters.contact, contact_handler))
        updater.dispatcher.add_handler(CallbackQueryHandler(callback_handler))
        updater.start_polling()
        updater.idle()