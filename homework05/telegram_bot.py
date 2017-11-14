import telebot
import config
import datetime
from bs4 import BeautifulSoup


bot = telebot.TeleBot(config.token)
days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
weeks = ["четную", "нечетную"]

def getWebPage():
    f = open('web_page.txt')
    web_page = f.read()
    f.close()

    return web_page

def getWeekNumber(date):
    weekNumber = datetime.date(date.year, date.month, date.day).isocalendar()[1]
    if (weekNumber % 2 == 0):
        return 1
    else:
        return 2

def getScheduleByDay(web_page, day_number):

    soup = BeautifulSoup(web_page, "html5lib")

    schedule_table = soup.find("table", attrs={"id": "{}day".format(day_number)})

    # Время проведения занятий
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]

    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text for room in locations_list]

    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.replace('\n', '').replace('\t', '') for lesson in lessons_list]

    return times_list, locations_list, lessons_list

@bot.message_handler(commands=['monday'])
def handle_monday(message):
    _, group = message.text.split()
    web_page = getWebPage()
    times_lst, locations_lst, lessons_lst = getScheduleByDay(web_page, 1)

    resp = ''
    for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
        resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)

    bot.send_message(message.chat.id, resp, parse_mode='HTML')

@bot.message_handler(commands=['near_lesson'])
def handle_near_lesson(message):
    pass


@bot.message_handler(commands=['tommorow'])
def handle_tommorow(message):
    _, group = message.text.split()

    today = datetime.datetime.now()
    week_number = getWeekNumber(today)
    tom_day_number = (today.weekday() + 1) % 7 % 6
    if not (tom_day_number):
        week_number = (week_number % 2) + 1

    web_page = getWebPage()
    times_lst, locations_lst, lessons_lst = getScheduleByDay(web_page, tom_day_number + 1)

    resp = '<b>{}</b>:\n'.format(days[tom_day_number])
    for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
        resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)

    bot.send_message(message.chat.id, resp, parse_mode='HTML')

@bot.message_handler(commands=['all'])
def handle_all(message):
    _, week_number, group = message.text.split()
    web_page = getWebPage()

    resp = '<strong>Расписание на {} неделю</strong>\n\n'.format(weeks[int(week_number) - 1])
    for i in range(6):
        times_lst, locations_lst, lessons_lst = getScheduleByDay(web_page, i + 1)

        resp += '<b>{}</b>:\n'.format(days[i])
        for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
            resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
        resp += '\n'

    bot.send_message(message.chat.id, resp, parse_mode='HTML')

if __name__ == '__main__':
    bot.polling(none_stop=True)