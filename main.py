import os
import sys
import traceback

print("🎯 === ПРИЛОЖЕНИЕ ЗАПУЩЕНО ===")
print(f"📁 Текущая директория: {os.getcwd()}")
print(f"📋 Файлы в директории: {os.listdir('.')}")

# Логируем системную информацию
print(f"🐍 Python версия: {sys.version}")
print(f"🔍 Python path: {sys.path}")

try:
    print("1. Пытаюсь импортировать kivy.config...")
    from kivy.config import Config

    print("   ✅ kivy.config - УСПЕХ")

    print("2. Настраиваю конфиг Kivy...")
    Config.set('graphics', 'fullscreen', 'auto')
    print("   ✅ Конфиг установлен")

    print("3. Импортирую основные модули Kivy...")
    from kivy.app import App

    print("   ✅ kivy.app - УСПЕХ")
    from kivy.uix.boxlayout import BoxLayout

    print("   ✅ BoxLayout - УСПЕХ")
    from kivy.uix.floatlayout import FloatLayout

    print("   ✅ FloatLayout - УСПЕХ")
    from kivy.animation import Animation

    print("   ✅ Animation - УСПЕХ")
    from kivy.uix.button import Button

    print("   ✅ Button - УСПЕХ")
    from kivy.properties import ObjectProperty

    print("   ✅ ObjectProperty - УСПЕХ")
    from kivy.uix.label import Label

    print("   ✅ Label - УСПЕХ")

    print("4. Импортирую graphics...")
    from kivy.graphics import Color, RoundedRectangle, Rectangle

    print("   ✅ Graphics - УСПЕХ")

    print("5. Импортирую сетевые модули...")
    from kivy.network.urlrequest import UrlRequest

    print("   ✅ UrlRequest - УСПЕХ")

    print("6. Импортирую стандартные библиотеки...")
    from datetime import datetime, timedelta

    print("   ✅ datetime - УСПЕХ")

    print("🎉 === ВСЕ ИМПОРТЫ УСПЕШНЫ! ===")

except Exception as e:
    print(f"💥 === КРИТИЧЕСКАЯ ОШИБКА ИМПОРТА ===")
    print(f"❌ Ошибка: {e}")
    print(f"📝 Тип ошибки: {type(e).__name__}")
    traceback.print_exc()
    print("💀 === ПРИЛОЖЕНИЕ ОСТАНОВЛЕНО ===")
    sys.exit(1)

# Дополнительная проверка Kivy
try:
    import kivy

    print(f"ℹ️  Версия Kivy: {kivy.__version__}")
    print(f"ℹ️  Kivy модуль пути: {kivy.__file__}")
except Exception as e:
    print(f"⚠️  Не удалось получить информацию о Kivy: {e}")

print("🚀 === НАЧИНАЮ ВЫПОЛНЕНИЕ ОСНОВНОГО КОДА ===")


class Container(FloatLayout):
    def __init__(self, **kwargs):
        print("🔧 === Container.__init__() ===")
        super().__init__(**kwargs)
        self.is_visible = False
        print("🔧 === Container инициализирован ===")

    def on_kv_post(self, base_widget):
        print("📋 === on_kv_post() ===")
        super().on_kv_post(base_widget)
        print("📋 === KV файл загружен ===")
        try:
            self.create_subject_buttons()
            print("📋 === Кнопки созданы ===")
        except Exception as e:
            print(f"❌ Ошибка создания кнопок: {e}")
            traceback.print_exc()

    def show_subjects(self, fl):
        y_pos = self.height * 0.295
        if not self.is_visible:
            fl.pos = (-fl.width, y_pos)
            anim = Animation(pos=(0, y_pos), duration=0.3)
            self.is_visible = True

            # Затемняем основной фон
            self.darken_main_background()

        else:
            anim = Animation(pos=(-fl.width, y_pos), duration=0.3)
            self.is_visible = False

            # Возвращаем обычный фон
            self.lighten_main_background()

        anim.start(fl)

    def darken_main_background(self):
        """Затемняет основной фон контейнера"""
        # Сохраняем оригинальный цвет
        self.original_bg_color = [0.95, 0.96, 0.98, 1]

        # Устанавливаем затемненный цвет
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.95, 0.96, 0.98, 0.5)  # Затемненный цвет
            Rectangle(pos=self.pos, size=self.size)

    def lighten_main_background(self):
        """Возвращает оригинальный фон"""
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.original_bg_color)
            Rectangle(pos=self.pos, size=self.size)

    def on_touch_down(self, touch):
        if self.is_visible:
            fl = self.ids.list_subjects
            if fl.collide_point(*touch.pos):
                return super(Container, self).on_touch_down(touch)
            else:
                self.show_subjects(fl)
                return True
        return super(Container, self).on_touch_down(touch)

    @staticmethod
    def get_subjects():
        list_subjects = ['Информатика', 'Иностранный язык', 'Инженерная и компьютерная графика',
                         'Математика', 'Рабочая профессия', 'Цифровая грамотность', 'Физическая культура и спорт',
                         'Основы проектной деятельности', 'Основы российской государственности']
        return list_subjects

    def create_subject_buttons(self):
        buttons_container = self.ids.buttons_container
        buttons_container.clear_widgets()

        for subject in self.get_subjects():
            btn = Button(
                size_hint_y=None,
                height=50,
                text=subject,
                background_color=(0.35, 0.51, 0.69, 0.8),
                color=(1, 1, 1, 1),
                shorten=False
            )
            btn.bind(on_release=lambda instance, subj=subject: self.on_subject_click(subj))
            buttons_container.add_widget(btn)

    def on_subject_click(self, subject):
        if self.is_visible:
            self.show_subjects(self.ids.list_subjects)
        self.schedule_collecting(subject)

    def schedule_collecting(self, subject):
        monday, sunday = self.get_monday_and_sunday_dates()
        monday_str = monday.strftime("%Y.%m.%d")
        sunday_str = sunday.strftime("%Y.%m.%d")

        url = f"https://rasp.omgtu.ru/api/schedule/group/980?start={monday_str}&finish={sunday_str}&lng=1"

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Android; Mobile)"
        }

        def on_success(request, result):
            result_lessons = []
            for lesson in result:
                if subject in lesson.get('discipline', ''):
                    result_lessons.append(lesson)

            print(f"Найдено занятий по предмету '{subject}': {len(result_lessons)}")
            self.create_schedule_boxes(result_lessons, subject)

        def on_error(request, error):
            print(f"Ошибка при получении расписания: {error}")

        UrlRequest(
            url,
            on_success=on_success,
            on_error=on_error,
            req_headers=headers,
            method='POST'
        )

    @staticmethod
    def get_monday_and_sunday_dates():
        today = datetime.now()
        monday = today - timedelta(days=today.weekday())
        sunday = monday + timedelta(days=6)
        return monday, sunday

    def create_schedule_boxes(self, lessons, subject):
        schedule_container = self.ids.schedule_container
        schedule_container.clear_widgets()

        if not lessons:
            no_lessons_label = Label(
                text=f"Занятий по предмету '{subject}' не найдено",
                size_hint_y=None,
                height=100,
                color=(0.5, 0.5, 0.5, 1)
            )
            schedule_container.add_widget(no_lessons_label)
            return

        # Сортируем занятия по дате (от старых к новым)
        lessons_sorted = sorted(lessons, key=lambda x: x.get('date', ''))

        # ДОБАВЛЯЕМ В ОБРАТНОМ ПОРЯДКЕ - от новых к старым
        for lesson in reversed(lessons_sorted):
            self.create_schedule_card(lesson, schedule_container)

    def color_of_work(self, work_type):
        """Возвращает цвет в зависимости от типа работы"""
        color_dict = {
            'Практические занятия': (1, 0.76, 0.42, 1),  # #ffc26b
            'Лекция': (0.70, 0.88, 0.52, 1),  # #b3e185
            'Лабораторные работы': (0.47, 0.82, 1, 1)  # #78d2ff
        }
        return color_dict.get(work_type, (0.8, 0.8, 0.8, 1))  # Серый по умолчанию

    def create_schedule_card(self, lesson, container):
        """Создает одну карточку расписания"""
        # Создаем основную обертку с горизонтальной ориентацией
        main_wrapper = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=200,
            spacing=0  # Убираем отступ между полосой и контентом
        )

        # Цветная полоса слева
        color_strip = BoxLayout(
            size_hint_x=None,
            width=15  # Ширина цветной полосы
        )

        # Добавляем цвет к полосе
        with color_strip.canvas.before:
            work_type = lesson.get('kindOfWork', '')
            color = self.color_of_work(work_type)
            Color(*color)
            Rectangle(
                pos=color_strip.pos,
                size=color_strip.size
            )

        # Функция для обновления позиции цветной полосы
        def update_color_strip(instance, value):
            instance.canvas.before.clear()
            with instance.canvas.before:
                work_type = lesson.get('kindOfWork', '')
                color = self.color_of_work(work_type)
                Color(*color)
                Rectangle(
                    pos=instance.pos,
                    size=instance.size
                )

        color_strip.bind(pos=update_color_strip, size=update_color_strip)

        # Контейнер для контента с тенью
        content_wrapper = BoxLayout(
            orientation='vertical',
            size_hint_x=1,
            padding=[15, 10],
            spacing=5
        )

        # Добавляем тень и фон к контейнеру контента
        with content_wrapper.canvas.before:
            Color(0, 0, 0, 0.15)
            RoundedRectangle(
                pos=(content_wrapper.x + 3, content_wrapper.y - 3),
                size=(content_wrapper.width, content_wrapper.height),
                radius=[0, 10, 10, 0]  # Закругляем только правые углы
            )
            Color(1, 1, 1, 1)
            RoundedRectangle(
                pos=content_wrapper.pos,
                size=content_wrapper.size,
                radius=[0, 8, 8, 0]  # Закругляем только правые углы
            )

        # Функция для обновления тени
        def update_shadow(instance, value):
            instance.canvas.before.clear()
            with instance.canvas.before:
                Color(0, 0, 0, 0.15)
                RoundedRectangle(
                    pos=(instance.x + 3, instance.y - 3),
                    size=instance.size,
                    radius=[0, 10, 10, 0]
                )
                Color(1, 1, 1, 1)
                RoundedRectangle(
                    pos=instance.pos,
                    size=instance.size,
                    radius=[0, 8, 8, 0]
                )

        content_wrapper.bind(pos=update_shadow, size=update_shadow)

        # СОЗДАЕМ ЛЕЙБЛЫ
        subject_label = Label(
            text=lesson.get('discipline', ''),
            size_hint_y=None,
            height=40,
            color=(0.1, 0.1, 0.1, 1),
            text_size=(None, None),
            halign='left',
            valign='middle',
            shorten=False
        )

        subject_kind_of_work = Label(
            text=lesson.get('kindOfWork', ''),
            size_hint_y=None,
            height=30,
            color=(0.4, 0.4, 0.4, 1),
            text_size=(None, None),
            halign='left',
            valign='middle',
            shorten=False
        )

        date_time_label = Label(
            text=f"Дата: {lesson.get('date', '')} • Время: {lesson.get('beginLesson', '')}",
            size_hint_y=None,
            height=25,
            color=(0.3, 0.3, 0.3, 1),
            text_size=(None, None),
            halign='left',
            valign='middle',
            shorten=False
        )

        room_label = Label(
            text=f"Аудитория: {lesson.get('auditorium', '')}",
            size_hint_y=None,
            height=25,
            color=(0.3, 0.3, 0.3, 1),
            text_size=(None, None),
            halign='left',
            valign='middle',
            shorten=False
        )

        lecturer_label = Label(
            text=f"Преподаватель: {lesson.get('lecturer', '')}",
            size_hint_y=None,
            height=30,
            color=(0.3, 0.3, 0.3, 1),
            text_size=(None, None),
            halign='left',
            valign='middle',
            shorten=False
        )

        # ДОБАВЛЯЕМ ЛЕЙБЛЫ В КОНТЕЙНЕР КОНТЕНТА
        content_wrapper.add_widget(subject_label)
        content_wrapper.add_widget(subject_kind_of_work)
        content_wrapper.add_widget(date_time_label)
        content_wrapper.add_widget(room_label)
        content_wrapper.add_widget(lecturer_label)

        # Функция для обновления размеров текста
        def update_text_size(instance, value):
            available_width = instance.width - 30
            for child in instance.children:
                if hasattr(child, 'text_size'):
                    child.text_size = (available_width, None)

        content_wrapper.bind(size=update_text_size)

        # СОБИРАЕМ ОСНОВНОЙ КОНТЕЙНЕР
        main_wrapper.add_widget(color_strip)  # Цветная полоса слева
        main_wrapper.add_widget(content_wrapper)  # Контент справа

        # Добавляем в контейнер расписания
        container.add_widget(main_wrapper)


class MainApp(App):
    def build(self):
        print("🏗️  === MainApp.build() ===")
        try:
            container = Container()
            print("🏗️  === Контейнер создан ===")
            return container
        except Exception as e:
            print(f"💥 Ошибка в build(): {e}")
            traceback.print_exc()
            return Label(text=f'Ошибка: {e}')


if __name__ == '__main__':
    print("⭐ === ЗАПУСК MainApp() ===")
    try:
        MainApp().run()
        print("⭐ === ПРИЛОЖЕНИЕ ЗАВЕРШЕНО ===")
    except Exception as e:
        print(f"💥 === КРИТИЧЕСКАЯ ОШИБКА В MAIN ===")
        print(f"❌ Ошибка: {e}")
        traceback.print_exc()