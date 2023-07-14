import datetime
import channels.layers
import httpx
# import translators as ts # noqa
from asgiref.sync import async_to_sync
from django.core.cache import cache
from django_celery_beat.models import IntervalSchedule, PeriodicTasks, PeriodicTask

from fruit_shop.celery import app


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    cache.clear()
    sender.add_periodic_task(90, task_jocker.s(), name='generate_joke')



@app.task
def task_jocker():
    from django.contrib.auth.models import User
    from users.models import Message

    channel_layer = channels.layers.get_channel_layer()
    jocker = User.objects.get(username='jocker')

    response = httpx.get('https://v2.jokeapi.dev/joke/Any?type=single')
    joke = response.json().get('joke')
    joke_message = Message.objects.create(user=jocker, text=joke, date=datetime.datetime.now())

    async_to_sync(channel_layer.group_send)(
        'shop_chat',
        {
            "type": "chat.message",
            "username": jocker.first_name,
            "message": joke_message.text,
            "date": joke_message.date.strftime('%H:%M')
        }
    )

    schedule, created = IntervalSchedule.objects.get_or_create(
        every=len(joke),
        period=IntervalSchedule.SECONDS,
    )
    task = PeriodicTask.objects.get(task='users.tasks.task_jocker')
    task.interval = schedule
    task.save()
    PeriodicTasks.changed(task)

    return joke
