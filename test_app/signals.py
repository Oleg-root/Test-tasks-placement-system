from django.db.models.signals import post_save, post_delete, pre_save
from django.contrib.auth.models import User # sender
from django.dispatch import receiver
from .models import Notification, Solution, Vacancy, Response

@receiver(post_save, sender=Solution)
def save_solution(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(title='New Solution',
                                    receiver=instance.associated_vacancy.author,
                                    content='%s has sent you a test task solution for one of your vacancies!'
                                        ' \nCheck it in "Received Solutions" tab.' % instance.author)

@receiver(post_save, sender=Response)
def save_response(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(title='New Response',
                                    receiver=instance.associated_solution.author,
                                    content='%s has sent you a response for one of your solutions!'
                                        ' \nCheck it in "Responses" tab.' % instance.author)

# @receiver(post_save, sender=Vacancy)
# def vacancy_update(sender, instance, created, **kwargs):
#     if created:
#         print('lol')
#     else:
#         Notification.objects.create(title='Vacancy Updated',
#                                     receiver=instance.author,
#                                     content='Vacancy (%s) has been updated.' % instance.title)

@receiver(post_delete, sender=Vacancy)
def vacancy(sender, instance, **kwargs):
    Notification.objects.create(title='Vacancy Deleted',
                                receiver=instance.author,
                                content='Vacancy (%s) has been deleted.' % instance.title)

@receiver(pre_save, sender=Vacancy)
def delete_old_task(sender, instance, *args, **kwargs):
    try:
        old_task = Vacancy.objects.get(id=instance.id).task.path
        try:
            new_task = instance.task.path
        except:
            new_task = None
        if new_task != old_task:
            import os
            if os.path.exists(old_task):
                os.remove(old_task)
    except:
        pass