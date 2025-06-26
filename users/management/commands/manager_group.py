from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError


class Command(BaseCommand):
    help = "Создание группы Менеджеры и назначение прав"

    def handle(self, *args, **kwargs):
        try:
            group, created = Group.objects.get_or_create(name="Managers")

            permissions = [
                ("mailings", "mailing_recipient", "can_view_mailing_recipient"),
                ("mailings", "mailing", "can_view_mailing"),
            ]

            for app_label, model, codename in permissions:
                try:
                    content_type = ContentType.objects.get(app_label=app_label, model=model)
                    permission, _ = Permission.objects.get_or_create(
                        codename=codename,
                        content_type=content_type,
                        defaults={'name': f'Can {codename}'}
                    )
                    group.permissions.add(permission)
                except ContentType.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(
                            f"ContentType не найден для {app_label}.{model}"
                        )
                    )
                except IntegrityError:
                    self.stdout.write(
                        self.style.ERROR(
                            f"Ошибка создания права {codename} для {app_label}.{model}"
                        )
                    )

            group.save()
            self.stdout.write(
                self.style.SUCCESS(
                    "Группа 'Managers' создана/обновлена с необходимыми правами."
                )
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ошибка: {str(e)}"))
