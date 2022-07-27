import json
from os import listdir
from os.path import isfile, join

def main():
    onlyfiles = [f for f in listdir('./jsons/raw') if isfile(join('./jsons/raw', f))]

    dataG = {}
    dataG2 = {}

    for file_name in onlyfiles:
        with open(f'jsons/raw/{file_name}', 'r') as f:
            try:
                data = json.load(f)
                high = 1
                for i in data:
                    b1 = data[i]
                    for j in data:
                        b2 = data[j]
                        rd = b2 * 100 / b1 - 100
                        if (rd >= high and rd <= 20):
                            high = rd
                            #print(f'{file_name.replace(".json", "")} : {i} - {j} ({b1}$ - {b2}$) - {round(rd, 2)}%')
                            #dataG[file_name.replace(".json", "")] = {f'{i} - {j} ({b1}$ - {b2}$)' : round(rd, 2)}
                            dataG[file_name.replace(".json", "")] = round(rd, 2)
                            # dataG2[file_name.replace(".json", "")] = f'{i} - {j} ({b1}$ - {b2}$)'
                            dataG2[file_name.replace(".json", "")] = f'{file_name.replace(".json", "").replace("-", " ").capitalize()}\nBuy: {i} ({b1}$)\nSell: {j} ({b2}$)\nProfit: {round(rd, 2)}%'
            except Exception as e:
                print(str(e))
                continue


    dataG = {k: v for k, v in sorted(dataG.items(), key=lambda item: item[1], reverse=False)}

    dataF = {'data': []}

    nm = 0
    for i in dataG:
        #dataF[nm] = dataG2[i]
        dataF['data'].append(dataG2[i])
        nm += 1


    with open('jsons/final.json', 'w') as f:
        json.dump(dataF, f, indent=4)

if __name__ == '__main__':
    main()
