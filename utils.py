

def stock_parser(symbol):
    sign = ''
    if symbol['valueChange'] > 0:
            sign = '+'
    info = f"```diff\n{symbol['issueName']} - {symbol['issueID']}\nPrecio: ${symbol['lastPrice']}\n{sign}{round(symbol['valueChange'],4)} {round(symbol['percentageChange'],2)}%\nVC: {symbol['bidVolume']} @ ${symbol['bidPrice']}\nVV: {symbol['askVolume']} @ ${symbol['askPrice']}```"
    return info