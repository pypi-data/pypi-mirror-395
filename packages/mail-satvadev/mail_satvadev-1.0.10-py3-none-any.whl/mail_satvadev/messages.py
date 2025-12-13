import abc

from django.template import Context, Template


class BaseMail(abc.ABC):
    """Базовый класс отправления email"""

    def __init__(self, **kwargs):
        context = self._prepare_context(**kwargs)
        self._text = self._generate_text(context)
        self._text += self.footer
        self._subject = self._generate_subject(context)

    @property
    def text(self) -> str:
        """Текстовое содержимое письма"""
        return self._text

    @property
    def subject(self) -> str:
        """Тема письма"""
        return self._subject

    @property
    @abc.abstractmethod
    def template(self) -> Template:
        """Шаблон письма"""
        pass

    @property
    @abc.abstractmethod
    def subject_template(self) -> Template:
        """Шаблон заголовка письма"""
        pass

    @property
    def footer(self) -> str:
        """Стандартное окончание письма"""
        return ''

    def _prepare_context(self, **kwargs) -> Context:
        """Подготовка контекста для шаблона

        По-умолчанию - передача kwargs из конструктора.
        Переопределяется в зависимости от требуемого функционала
        """
        return Context(kwargs)

    def _generate_text(self, context):
        """Подстановка данных в шаблон тела письма"""
        if not isinstance(self.template, Template):
            raise ValueError('template must be a Template')

        return self.template.render(context)

    def _generate_subject(self, context):
        """Подстановка данных в шаблон заголовка письма"""
        if not isinstance(self.template, Template):
            raise ValueError('subject template must be a Template')

        return self.subject_template.render(context)
