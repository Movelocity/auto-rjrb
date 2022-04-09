import http.client
import pandas as pd
import json


def get_books():
    for i in range(1, 504):
        items = []
        con = http.client.HTTPSConnection('spa5.scrape.center', 443)
        limit = 18
        offset = (i-1)*limit
        con.request('GET', '/api/book/?limit={}&offset={}'.format(limit, offset))
        json_data = json.loads(con.getresponse().read().decode('utf-8'))

        books = json_data["results"]
        for book in books:
            item = {
                '书名': book["name"],
                '作者': ",".join(book["authors"]).strip(),
                '页码': i,
            }
            items.append(item)

        table = pd.DataFrame(items, columns=['书名', '作者', '页码'])
        if i == 1:
            table.to_csv("part2.csv", index=False)
        else:
            table.to_csv("part2.csv", mode='a', index=False, header=False)
        print("page "+str(i)+" completed.")


if __name__ == '__main__':
    get_books()
    print("done")
