# e-dostavka
Check delivery intervals for e-dostavka.by

1. Install requests
2. Create telegram chat and bot (@botfather)
3. Get chat id (@myidbot)
4. Find your ZONE as description in popup on https://e-dostavka.by/#/dzone/?city_active=Минск+и+Минская+область
4. Run like
BOT_TOKEN=... TG_CHAT_ID=-... ZONE='Интернет-магазин 50160 Минск (Западный промузел, ТЭЦ 4), зона обслуживания А, интервал доставки 2 часа' python checker.py
5. Add to cron