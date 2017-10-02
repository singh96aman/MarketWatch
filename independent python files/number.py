'''
def convertnum(stockvalue):
    temp = ""
    for num in stockvalue:
        if(num != ','):
            temp+=num
    return temp

stock = "45,3434,23.78"
print convertnum(stock)
'''
i = 123.45
lol = float(i)
print i+1
