import json

def Read(link):
    try:
        with open(link, "r") as ReadFile:
            data = json.load(ReadFile)
            return data
    except:
        return None

def Write(id, arr, link):

    data = Read(link)
    data[id] = arr
    try:
        with open(link, "w") as WriteFile:
            json.dump(data, WriteFile)
        return True
    except:
        return False

def Write_parameter(id, parameter, number, link):

    data = Read(link)
    data[id][parameter] = number


    try:
        with open(link, "w") as WriteFile:
            json.dump(data, WriteFile)
        return True
    except:
        return False

if __name__ == '__main__':
    print(Read("data/UserData.json"))