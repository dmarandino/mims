import requests
import json
import random
import datetime
import time
from datetime import datetime, timedelta

def main():

    url = "http://ec2-54-81-254-121.compute-1.amazonaws.com:5000/products/"

    payload = ""
    headers = {
        'content-type': "application/json",
        'access-token': "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOjF9.-FE628IPFnkNhO3B-voWdeBZ4196HMfWUJ4edxvEYf0"
    }

    # Pull response from the URL
    try:
        x = requests.request("GET", url, data=payload, headers=headers)
        print(x.text)
        # Convert Response object to Json object
        response = x.json()
        print(response["data"])
        # Right here we have "success" = true, so we must get the inner array
        data = response["data"]
        print(data["products"])
        # We are going into the next nested dictionary object(key value object) to get products
        products=data["products"]
        # Object of PLU's
        items = []
        for item in products:
            # Grab PLU's from the product list
            # Products is a list of dictionaries. Each dictionary is a product with a PLU etc..
            print("Item Code: " + item["item_code"])
            items.append(item["item_code"])
        simtime = datetime.today() - timedelta(days=365)
        initialInventory(headers, items, (str(simtime.date()) + " " + str(simtime.time().isoformat(timespec='seconds'))))

        """Sets when the store is 
            either opened or closed
            """
        openclose = [[False, False, False, False, False, False, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False],
                     [False, False, False, False, False, False, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False],
                     [False, False, False, False, False, False, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False],
                     [False, False, False, False, False, False, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False],
                     [False, False, False, False, False, False, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False],
                     [False, False, False, False, False, False, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False],
                     [False, False, False, False, False, False, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False]]

        waitTimes = [[1,1,1,1,1,1,1,5,5,5,10,10,10,15,15,15,10,10,10,10,10,10,5,5,1],
                     [1,1,1,1,1,1,1,5,5,5,10,10,10,15,15,15,15,15,15,10,10,10,10,5,1],
                     [1,1,1,1,1,1,1,5,10,10,10,10,10,15,15,15,15,15,15,10,10,5,5,1],
                     [1,1,1,1,1,1,1,5,5,5,10,10,10,10,10,10,10,10,10,10,10,10,5, 5, 1],
                     [1,1,1,1,1,1,1,5,5,5,10,10,10,10,15,15,10,10,10,10,10,10,5,5,1],
                     [1,1,1,1,1,1,1,5,5,10,10,15,15,15,15,15,15,15,10,10,10,10,5,5,1],
                     [1,1,1,1,1,1,1,10, 5, 10, 15, 15, 15, 15, 15, 15, 15, 10, 10, 10, 10, 10, 10, 1, 1]]

        print(str(simtime.date()) + " " + str(simtime.time().isoformat(timespec='seconds')))

        wait = False
        waitTime = 0
        sales = 0
        last_time = simtime
        while(simtime < datetime.today()):
            if(simtime.weekday() == 6 and simtime.weekday() - last_time.weekday() == 1):
                changePrices(headers, items, (str(simtime.date()) + " " + str(simtime.time().isoformat(timespec='seconds'))))
            if (last_time.weekday() - simtime.weekday() != 0):
                newInventory(headers, items, (str(simtime.date()) + " " + str(simtime.time().isoformat(timespec='seconds'))))
            if(waitTime > 0):
                waitTime = waitTime - 1
            elif(waitTime==0):
                if(wait):
                    makeSale(headers, items, (str(simtime.date()) + " " + str(simtime.time().isoformat(timespec='seconds'))))
                    print (str(simtime.date()) + " " + str(simtime.time().isoformat(timespec='seconds')))
                    sales = sales + 1
                wait = False
                if(openclose[simtime.weekday()][simtime.hour]):
                    wait = True
                    waitTime = random.randint(5,(600/waitTimes[simtime.weekday()][simtime.hour]))
            last_time = simtime
            simtime = simtime + timedelta(minutes=1)
        print("Sales: " + str(sales))

        currentDT = datetime.now()

        while(True):
            time.sleep(waitTime * 60)
            last_time = currentDT
            currentDT = datetime.now()
            if(waitTime > 0):
                if (currentDT.weekday() == 6 and currentDT.weekday() - last_time.weekday() == 1):
                    changePrices(headers, items, (str(currentDT.date()) + " " + str(currentDT.time().isoformat(timespec='seconds'))))
                if (last_time.weekday() - currentDT.weekday() != 0):
                    newInventory(headers, items, (str(currentDT.date()) + " " + str(currentDT.time().isoformat(timespec='seconds'))))
                makeSale(headers, items, str(currentDT.date()) + " " + str(currentDT.time().isoformat(timespec='seconds')))
                print(str(currentDT.date()) + " " + str(currentDT.time().isoformat(timespec='seconds')))
                sales = sales + 1
            if (openclose[currentDT.weekday()][currentDT.hour]):
                wait = True
                waitTime = random.randint(5, (600/waitTimes[currentDT.weekday()][currentDT.hour]))
            else:
                waitTime = 0
    except json.decoder.JSONDecodeError:
        print("Couldn't Get Initial List")


def makeSale(headers, items, simtime):
    shopperType = random.randint(1,100)
    sale = []
    if(shopperType < 60):
        numItems = random.randint(1,3)
        for i in range(1,numItems):
            try:
                url = "http://ec2-54-81-254-121.compute-1.amazonaws.com:5000/products/"
                rng = random.randint(0, len(items) - 1)
                item = items[rng]
                url += item + "/"
                payload = ""
                print(item)
                x = requests.request("GET", url, data=payload, headers=headers)
                print(x.text)
                # Convert Response object to Json object
                response = x.json()
                print(response["data"])
                # Right here we have "success" = true, so we must get the inner array
                data = response["data"]
                print(data["product"])
                # We are going into the next nested dictionary object(key value object) to get products
                product = data["product"]
                inventory = product["current_inventory"]
                amount = 0
                if(inventory > 3):
                    amount = random.randint(1,3)
                elif (inventory > 0):
                    amount = random.randint(1, inventory)
                if(amount > 0):
                    newItem = {
                        "item_code": item,
                        "amount": amount,
                        "datetime": simtime
                    }
                    sale.append(newItem)
            except json.decoder.JSONDecodeError:
                print("Couldn't Get Amount Of Item")
    elif(shopperType < 90):
        numItems = random.randint(2, 5)
        for i in range(1, numItems):
            try:
                url = "http://ec2-54-81-254-121.compute-1.amazonaws.com:5000/products/"
                rng = random.randint(0, len(items) - 1)
                item = items[rng]
                url +=  item + "/"
                payload = ""
                print(item)
                x = requests.request("GET", url, data=payload, headers=headers)
                print(x.text)
                # Convert Response object to Json object
                response = x.json()
                print(response["data"])
                # Right here we have "success" = true, so we must get the inner array
                data = response["data"]
                print(data["product"])
                # We are going into the next nested dictionary object(key value object) to get products
                product = data["product"]
                inventory = product["current_inventory"]
                amount = 0
                if (inventory > 100):
                    amount = random.randint(1, int(inventory / 20))
                elif (inventory > 5):
                    amount = random.randint(1, 5)
                elif (inventory > 0):
                    amount = random.randint(1, inventory)
                if (amount > 0):
                    newItem = {
                        "item_code": item,
                        "amount": amount,
                        "datetime": simtime
                    }
                    sale.append(newItem)
            except json.decoder.JSONDecodeError:
                print("Couldn't Get Amount Of Item")
    else:
        numItems = random.randint(5, 10)
        for i in range(1, numItems):
            try:
                url = "http://ec2-54-81-254-121.compute-1.amazonaws.com:5000/products/"
                rng = random.randint(0, len(items) - 1)
                item = items[rng]
                url += item + "/"
                payload = ""
                print(url)
                x = requests.request("GET", url, data=payload, headers=headers)
                print(x.text)
                # Convert Response object to Json object
                response = x.json()
                print(response["data"])
                # Right here we have "success" = true, so we must get the inner array
                data = response["data"]
                print(data["product"])
                # We are going into the next nested dictionary object(key value object) to get products
                product = data["product"]
                inventory = product["current_inventory"]
                amount = 0
                if (inventory > 100):
                    amount = random.randint(1,int(inventory / 10))
                elif (inventory > 5):
                    amount = random.randint(1, int(inventory / 5))
                if (amount > 0):
                    newItem = {
                        "item_code": item,
                        "amount": amount,
                        "datetime": simtime
                    }
                    sale.append(newItem)
            except json.decoder.JSONDecodeError:
                print("Couldn't Get Amount Of Item")
    data = {
        "items": sale
    }
    payload = json.dumps(data)
    print(data)
    try:
        url = "http://ec2-54-81-254-121.compute-1.amazonaws.com:5000/sales/"
        x = requests.request("POST", url, data=payload, headers=headers)
    except json.decoder.JSONDecodeError:
        print("Couldn't Make Sale")

def newInventory(headers, items, simtime):
    for item in items:
        try:
            url = "http://ec2-54-81-254-121.compute-1.amazonaws.com:5000/products/"
            url += item + "/"
            payload = ""
            print(url)
            x = requests.request("GET", url, data=payload, headers=headers)
            print(x.text)
            # Convert Response object to Json object
            response = x.json()
            print(response["data"])
            # Right here we have "success" = true, so we must get the inner array
            data = response["data"]
            print(data["product"])
            # We are going into the next nested dictionary object(key value object) to get products
            product = data["product"]
            inventory = product["current_inventory"]
            per = product["units_per_case"]
            if inventory < per * 10:
                amount = random.randint(1,10)
                data = {
                    "item_code": item,
                    "amount": amount,
                    "unit": 3,
                    "datetime": simtime
                }
                payload = json.dumps(data)
                print(data)
                try:
                    url = "http://ec2-54-81-254-121.compute-1.amazonaws.com:5000/inventory/"
                    x = requests.request("POST", url, data=payload, headers=headers)
                except json.decoder.JSONDecodeError:
                    print("Couldn't Make New Inventory")
        except json.decoder.JSONDecodeError:
            print("Couldn't Get Case Size Of Item")

def initialInventory(headers, items, simtime):
    url = "http://ec2-54-81-254-121.compute-1.amazonaws.com:5000/inventory/"
    for item in items:
        amount = random.randint(5,10)
        data = {
                "item_code": item,
                "amount": amount,
                "unit": 3,
                "datetime": simtime
                }
        payload = json.dumps(data)
        print(data)
        try:
            x = requests.request("POST", url, data=payload, headers=headers)
        except json.decoder.JSONDecodeError:
            print("Couldn't Set Initial Inventory")



def changePrices(headers, items, simtime):
    for i in range(1,10):
        try:
            url = "http://ec2-54-81-254-121.compute-1.amazonaws.com:5000/products/"
            rng = random.randint(0,len(items) - 1)
            item = items[rng]
            url += item + "/"
            payload = ""
            x = requests.request("GET", url, data=payload, headers=headers)
            print(x.text)
            # Convert Response object to Json object
            response = x.json()
            print(response["data"])
            # Right here we have "success" = true, so we must get the inner array
            data = response["data"]
            print(data["product"])
            # We are going into the next nested dictionary object(key value object) to get products
            product = data["product"]
            initPrice = product["price"]
            newPrice = initPrice * 1.1
            data = {
                "price": newPrice
            }
            payload = json.dumps(data)
            print(data)
            try:
                x = requests.request("PUT", url, data=payload, headers=headers)
            except json.decoder.JSONDecodeError:
                print("Couldn't Set New Price")
        except json.decoder.JSONDecodeError:
            print("Couldn't Get Price Of Item")
    for i in range(1,10):
        try:
            url = "http://ec2-54-81-254-121.compute-1.amazonaws.com:5000/products/"
            rng = random.randint(0,len(items) - 1)
            item = items[rng]
            url += item + "/"
            payload = ""
            x = requests.request("GET", url, data=payload, headers=headers)
            print(x.text)
            # Convert Response object to Json object
            response = x.json()
            print(response["data"])
            # Right here we have "success" = true, so we must get the inner array
            data = response["data"]
            print(data["product"])
            # We are going into the next nested dictionary object(key value object) to get products
            product = data["product"]
            initPrice = product["price"]
            newPrice = initPrice * .9
            data = {
                "price": newPrice
            }
            payload = json.dumps(data)
            print(data)
            try:
                x = requests.request("PUT", url, data=payload, headers=headers)
            except json.decoder.JSONDecodeError:
                print("Couldn't Set New Price")
        except json.decoder.JSONDecodeError:
            print("Couldn't Get Price Of Item")


if __name__ == "__main__":
    main()