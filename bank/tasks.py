import channels.layers
from asgiref.sync import async_to_sync
from django.core.cache import cache

from fruit_shop.celery import app

channel_layer = channels.layers.get_channel_layer()


@app.task(bind=True)
def task_check_warehouse(self, user_id):
    for i in range(1, 26):
        math_operations = [9999999**99999 for x in range(3)]
        current = i * 4
        self.update_state(state='PROGRESS', meta={'current': current, 'total': 100})

        async_to_sync(channel_layer.group_send)(
            f'shop_audit_{user_id}',
            {
                "type": "update.progress.bar",
                "progress": current
            }
        )
    cache.delete(f'user_{user_id}')
    return {'current': 100, 'total': 100}