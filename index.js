"use strict";
exports.__esModule = true;
var express = require("express");
var https = require("https");
var qs = require("querystring");
var path = require('path');
var PORT = process.env.PORT || 5000;
express()
    .use(express.static(path.join(__dirname, 'public')))
    .get('/', function (req, res) { return res.send('HELLO!'); })
    .get('/api/prices/:symbols', handleStockRequest)
    .listen(PORT, function () { return console.log("Listening on " + PORT); });
var baseUrl = 'https://api.iextrading.com/1.0/stock/market/batch';
function handleStockRequest(req, res) {
    var symbols = req.params.symbols;
    getStocks(symbols).then(function (a) {
        return res.send(a);
    });
}
function getStocks(symbols) {
    return new Promise(function (res, rej) {
        var querystring = qs.stringify({ symbols: symbols, types: 'chart', range: '6m' });
        var reqUrl = baseUrl + "?" + querystring;
        https.get(reqUrl, function (response) {
            var body = '';
            response.on("error", function (error) { return rej(error); });
            response.on("data", function (data) { return body += data; });
            response.on("end", function () {
                res(body);
            });
        });
    });
}
