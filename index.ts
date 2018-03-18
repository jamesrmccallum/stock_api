import * as express from 'express';
import * as https from 'https';
import * as qs from 'querystring';
const path = require('path');
const PORT = process.env.PORT || 5000;

express()
  .use(express.static(path.join(__dirname, 'public')))
  .get('/', (req, res) => res.send('HELLO!'))
  .get('/api/prices/:symbols', handleStockRequest)
  .listen(PORT, () => console.log(`Listening on ${PORT}`))

const baseUrl = 'https://api.iextrading.com/1.0/stock/market/batch'

function handleStockRequest(req: Express.Request, res: Express.Response) {
  let symbols = req.params.symbols;

  getStocks(symbols).then(a =>
    res.send(a)
  )
}

function getStocks(symbols: string[]) {

  return new Promise<string>((res, rej) => {

    var querystring = qs.stringify({ symbols: symbols, types: 'chart', range: '6m' });
    let reqUrl = `${baseUrl}?${querystring}`;
    https.get(reqUrl, response => {
      let body = '';

      response.on("error", error => rej(error));
      response.on("data", data => body += data);
      response.on("end", () => {
        res(body);
      })
    }

    )

  });
}