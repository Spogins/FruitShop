from django.http import JsonResponse

from fruit_shop.celery import app


@app.task
def test():
    print("This is a test message from Celery Beat111111")
    return {'data': '200 OK'}

