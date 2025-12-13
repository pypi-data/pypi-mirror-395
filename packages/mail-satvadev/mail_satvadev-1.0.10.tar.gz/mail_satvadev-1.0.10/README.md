# Django приложение шаблона письма email с поддержкой отправки через Celery task

## Конфигурация
Подключение приложения
```
INSTALLED_APPS = [
    'mail_satvadev',
]
```

## Использование базового класса шаблона письма
Для использования необходимо переопределить абстрактные свойства класса:
```
    @property
    @abc.abstractmethod
    def title(self):
        """Тема письма"""
        pass

    @property
    @abc.abstractmethod
    def template(self):
        """Шаблон письма"""
        pass
```

Для динамического формирования содержимого поддерживается подстановка значений
в текстовый шаблон с требуемым форматированием.

Данные контекста в формате словаря передаются в конструктор при инициализации
класса, и могут быть обработаны и преобразованы в переопределяемом методе
```
    _prepare_context(self, **kwargs)
```
по-умолчанию метод возвращает переданные `kwargs` без изменения.

Форматирование и подстановка контекста в текстовый шаблон может быть
произведена в переопределяемом методе
```
    _generate_text(self, context)
```
по-умолчанию метод подставляет данные контекста в шаблон template.

Базовый класс поддерживает подстановку стандартного окончания в содержимое
шаблона.
Завершающий текст задается через свойство
```
    @property
    def footer(self):
        """Стандартное окончание письма"""
```
по-умолчанию - пустая строка.

## Проверка формата электронной почты получателей письма

Поддерживается валидация списка получателей письма на корректность формата
адресов электронной почты.
```
from mail_satvadev.filters import RecipientFilter


validator = RecipientFilter()
emails = validator.filter_emails(emails)  # Только корректные адреса email
```

## Отправление письма получателем через Celery task
Для отправки письма через Celery task в файле настроек проекта settings.py
должны быть прописаны
```
# Почта отправителя
EMAIL_HOST_USER=my.smtp.provider@.email.com
# Максимальное кол-во повторных попыток отправки
CELERY_MAX_RETRIES_COUNT=3
```
Отправление письма
- `subject` - тема письма
- `emails_list` - список электронных адресов получателей
- `text` - содержимое письма в текстовом формате

опционально
- параметр `backoff` - для повторных отправлений в случае неудачи
(по алгоритму exponential backoff),
по-умолчанию не задан.
```
from mail_satvadev.tasks import send_email

subject = `Тема письма`
emails_list = ['admin@example.com', 'user@example.com']
text = 'Содержимое письма'
send_email.delay(subject, emails_list, text, backoff)
```


## Примеры использования
Письмо с проверочным кодом сброса пароля
```
from mail_satvadev.messages import BaseMail


class ResetPasswordMail(BaseMail):
    """Письмо с проверочным кодом сброса пароля"""
    subject = '<ERP SatvaSpace> Сброс пароля'
    template = r'Проверочный код: {code}'
    
<...>

from authentication.mail import ResetPasswordMail
from mail_satvadev.tasks import send_email


class ResetPasswordView(APIView):
    def post(self, request):
        <...>
        code = SystemRandom().randint(100000, 999999)
        mail = ResetPasswordMail(code=code)
        send_email.delay(mail.subject, ['user@example.com'], mail.text)
```

Письмо-напоминание
```
class BirthdayNotificationMail(BaseMail):
    """Письмо напоминание о днях рождения"""
    subject = 'Дни рождения'
    template = ''

    def __init__(self, birthdays: list[tuple[str, str]], **kwargs) -> None:
        self.template = self._get_template(birthdays)
        super().__init__(**kwargs)

    @staticmethod
    def _get_template(lines: list[str]) -> str:
        string = ''
        for line in lines:
            string += f'День рождения {line[0]} у сотрудника {line[1]} \n'
        return string.rstrip()
        
<...>       

from birthday_notification.mail import BirthdayNotificationMail
from mail_satvadev.tasks import send_email


def send_reminders():
    birthdate_list = []
    mail = BirthdayNotificationMail(birthdate_list)
    send_email.delay(mail.subject, ['user@example.com'], mail.text, 40)
```

