import requests
from bs4 import BeautifulSoup
import json

a = 0
url = "https://www.imdb.com/calendar"
page = requests.get(url)
soup = BeautifulSoup(page.content,'html5lib')
list = soup.find("div",class_="pagecontent").findAll("li")

f = open('imdb_upcoming.json', "a")
temp = {}

with open('imdb_upcoming.json', 'a') as outf:
  json.dump(temp, outf, indent  = 4)

for movie in list:
  # movie name
  name = movie.a
  movie_name = name.text
  url_cnt = name["href"]
  url_2 = "https://www.imdb.com" + url_cnt

  # movie description
  page_2 = requests.get(url_2)
  soup_2 = BeautifulSoup(page_2.content,'html5lib')
  lists = soup_2.find('section', class_="ipc-page-section")
  description = lists.find("span", class_="sc-16ede01-0").text

  # movie release date
  date_list = soup_2.find('section',{"data-testid":"Details"}).find('li',{"data-testid":"title-details-releasedate"}).a
  url_cnt_date = date_list["href"]
  url_3 = "https://www.imdb.com" + url_cnt_date
  page_3 = requests.get(url_3)
  soup_3 = BeautifulSoup(page_3.content, 'html5lib')
  all_dates = soup_3.find('table', class_="ipl-zebra-list ipl-zebra-list--fixed-first release-dates-table-test-only").findAll("tr")
  date = ""
  for dates in all_dates:
    place = dates.find("td",class_="release-date-item__country-name")
    date_m = dates.find("td", class_="release-date-item__date").text
    element = dates.find("td", class_="release-date-item__attributes--empty")
    if "USA" in place.text:
      if element is not None:
        date = dates.find("td", class_="release-date-item__date")

  date = date.text.split()
  month = ""
  if (date[1] == "January"):
    month = "01"
  elif (date[1] == "February"):
    month = "02"
  elif (date[1] == "March"):
    month = "03"
  elif (date[1] == "April"):
    month = "04"
  elif (date[1] == "May"):
    month = "05"
  elif (date[1] == "June"):
    month = "06"
  elif (date[1] == "July"):
    month = "07"
  elif (date[1] == "August"):
    month = "08"
  elif (date[1] == "September"):
    month = "09"
  elif (date[1] == "October"):
    month = "10"
  elif (date[1] == "November"):
    month = "11"
  elif (date[1] == "December"):
    month = "12"
  day = date[0]
  year = date [2]
  release_date = year + "-(" + month + "-" + day + ")"


  # movie duration
  element = soup_2.find('section',{"data-testid":"TechSpecs"})
  if element is not None:
    duration = element.find('div',class_="ipc-metadata-list-item__content-container").text
    duration = duration.split()
    if len(duration)==4:
      hour = duration[0]
      minutes = duration[2]
      duration = hour+":"+minutes+":"+"0"
    else:
      duration = "not given"
  else:
    duration = "not given"

  # movie genres
  genres_list = soup_2.find('div',class_="ipc-chip-list__scroller").findAll("a")
  genres = ""
  for gen in genres_list:
    genres = genres + ", " + (gen.text)
  genres = genres[2:]

  # movie directors
  element = soup_2.find('section',{"data-testid":"title-cast"})
  if element is not None:
    directors_list = soup_2.find('section', {"data-testid": "title-cast"}).find('div',
                                                                                class_="ipc-metadata-list-item__content-container").findAll("a")
    directors = ""
    for dir in directors_list:
      directors = directors + ", " + (dir.text)
    directors = directors[2:]
  else:
    directors = "not given"


  # movie stars
  element = soup_2.find('li', {"class": "ipc-metadata-list__item ipc-metadata-list-item--link"}).find('div',class_="ipc-metadata-list-item__content-container")
  stars = ""

  if element is not None:
    stars_list = soup_2.find('li', {"class": "ipc-metadata-list__item ipc-metadata-list-item--link"}).find('div',class_="ipc-metadata-list-item__content-container").findAll("a")
    for star in stars_list:
      stars = stars + ", " + (star.text)
    stars = stars[2:]
  else:
    stars = "not given"


  if (year != "2022"):
    break

  a = a + 1
  b = "% s" % a
  date_last = b+") "+release_date

  data = {date_last: {"Movie Name": movie_name,
                           "Directors":directors,
                           "Stars": stars,
                           "Genres": genres,
                           "Duration": duration,
                           "Description": description}}





  with open('imdb_upcoming.json') as f:
    all_objects = json.load(f)
  all_objects.update(data)
  with open('imdb_upcoming.json', 'w') as outfile:
    json.dump(all_objects, outfile, indent = 4)
