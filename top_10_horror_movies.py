from bs4 import BeautifulSoup
import requests

url="https://editorial.rottentomatoes.com/article/the-10-scariest-horror-movies-ever/"

res = requests.get(url)
try:
    res_text = res.text
except res.raise_for_status():
    print(res.status_code)

soup = BeautifulSoup(res_text, "html.parser")
a = soup.find_all(name="strong")

print(a[0].getText())

movie_list = [movie.getText() for movie in a]

print(movie_list[3])

with open("movie_list.txt", mode='w') as file:
    for movie in movie_list:
        file.write(f"{movie} \n")
