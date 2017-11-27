import telebot
import config
import datetime
import requests
from bs4 import BeautifulSoup
from jinja2 import Template

singleDayTemplate = Template(open('templates/single_day.html').read())
nearLessonTemplate = Template(open('templates/near_lesson.html').read())

bot = telebot.TeleBot(config.token)

def get_page(group, week=''):
    if week:
        week = str(week) + '/'
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=config.domain, 
        week=week, 
        group=group)
    response = requests.get(url)
    web_page = response.text
    return web_page

def getWeekNumber(date):
    weekNumber = datetime.date(date.year, date.month, date.day).isocalendar()[1]
    if (weekNumber % 2 == 0):
        return 1
    else:
        return 2

def getTommorow():
    today = datetime.datetime.now()
    tommorow = today
    if (today.weekday() == 5):
        tommorow += datetime.timedelta(days=2)
    else:
        tommorow += datetime.timedelta(days=1)

    return tommorow

def transformInterval(interval):
    now = datetime.datetime.now()
    start, end = interval.split('-')

    hour, minute = start.split(':')
    start = now.replace(hour=int(hour), minute=int(minute))

    hour, minute = end.split(':')
    end = now.replace(hour=int(hour), minute=int(minute))

    return start, end

def dayIndex(day):
    days = ['/monday', '/tuesday', '/wednesday', '/thursday', '/friday', '/saturday', '/sunday']
    
    return days.index(day)


def getScheduleByDay(web_page, day_number):

    soup = BeautifulSoup(web_page, "html5lib")

    schedule_table = soup.find("table", attrs={"id": "{}day".format(day_number)})

    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]

    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text for room in locations_list]

    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.replace('\n', '').replace('\t', '') for lesson in lessons_list]

    return zip(times_list, locations_list, lessons_list)


def getNearLesson(schedule):
    resp = None
    now = datetime.datetime.now()
    #now = datetime.datetime.now() - datetime.timedelta(hours=8)

    for item in list(schedule):
        time, location, lesson = item
        start, end = transformInterval(time)
        if (now < end):
            resp = (time, location, lesson)
            break

    return resp


@bot.message_handler(commands=['near_lesson'])
def handle_near_lesson(message):
    _, group = message.text.split()
    today = datetime.datetime.now()
    web_page = get_page(group, getWeekNumber(today))
    near_lesson = getNearLesson(getScheduleByDay(web_page, today.weekday() + 1))
    if not near_lesson:
        resp = "На сегодня больше нет занятий"
    else:
        resp = nearLessonTemplate.render(lesson=near_lesson)

    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['tommorow'])
def handle_tommorow(message):
    _, group = message.text.split()

    tommorow = getTommorow()
    week_number = getWeekNumber(tommorow)
    tommorow_num = tommorow.weekday()

    web_page = get_page(group, week_number)
    schedule = getScheduleByDay(web_page, tommorow_num + 1)
    resp = singleDayTemplate.render(schedule=schedule, num=tommorow_num + 1)

    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['all'])
def handle_all(message):
    _, week_number, group = message.text.split()
    week_number = int(week_number) - 1
    web_page = get_page(group, week_number + 1)

    resp = ""
    for i in range(6):
        schedule = getScheduleByDay(web_page, i+1)
        resp += singleDayTemplate.render(schedule=schedule, num=i+1)

    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                               'saturday'])
def handle_monday(message):
    day, week_number, group = message.text.split()
    dayNumber = dayIndex(day) + 1
    web_page = get_page(group, int(week_number))
    schedule = getScheduleByDay(web_page, dayNumber)
    resp = singleDayTemplate.render(schedule=schedule, num=dayNumber)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


if __name__ == '__main__':
    bot.polling(none_stop=True)
