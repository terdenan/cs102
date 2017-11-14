# import requests
# import config
# from bs4 import BeautifulSoup

# def get_schedule(web_page):
#     soup = BeautifulSoup(web_page, "html5lib")

#     # Получаем таблицу с расписанием на понедельник
#     schedule_table = soup.find("table", attrs={"id": "1day"})

#     # Время проведения занятий
#     times_list = schedule_table.find_all("td", attrs={"class": "time"})
#     times_list = [time.span.text for time in times_list]

#     # Место проведения занятий
#     locations_list = schedule_table.find_all("td", attrs={"class": "room"})
#     locations_list = [room.span.text for room in locations_list]

#     # Название дисциплин и имена преподавателей
#     lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
#     lessons_list = [lesson.text.replace('\n', '').replace('\t', '') for lesson in lessons_list]

#     return times_list, locations_list, lessons_list

# if __name__ == '__main__':
#     f = open('web_page.txt')
#     web_page = f.read()
#     times_list, locations_list, lessons_list = get_schedule(web_page)
#     print(lessons_list)

for i in range(6):
    print(i)