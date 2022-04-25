function calculateMA(dayCount, data) {
  var result = [];
  for (var i = 0, len = data.length; i < len; i++) {
    if (i < dayCount) {
      result.push("-");
      continue;
    }
    var sum = 0;
    for (var j = 0; j < dayCount; j++) {
      sum += data[i - j][1];
    }
    result.push(sum / dayCount);
  }
  return result;
}

const color_list = [
  "#c23531",
  "#2f4554",
  "green",
  "#d48265",
  "#91c7ae",
  "#749f83",
  "#ca8622",
  "#bda29a",
  "#6e7074",
  "#546570",
  "#c4ccd3",
];

function convertNumber(num) {
  return num ? parseFloat(num) : 0;
}

function getMyInvestment(trade, initial_money, numVolume = 1, margin=1) {
  $("#alert").html("");
  var overall_gain = 0;
  var sell_Y = [];
  var sell_X = [];
  var buy_Y = [];
  var buy_X = [];
  var output = [];
  var equity = convertNumber(initial_money) * margin;
  var balance = convertNumber(initial_money);
  for (var i = 0; i < trade.close_time.length; i++) {
    overall_gain += numVolume * convertNumber(trade.gain[i]);
    switch (trade.status[i]) {
      case "-1":
        sell_X.push(trade.close_time[i]);
        sell_Y.push(trade.price[i]);
        equity += numVolume * convertNumber(trade.price[i]);
        balance += numVolume * convertNumber(trade.price[i]);
        output.push(
          `<tr><td>${trade.close_time[i]}</td><td>Sell ${numVolume} unit</td><td>${trade.price[i]}</td><td>${trade.investment[i]}</td><td>${equity}</td><td>${balance}</td></tr>"`
        );
        break;
      default:
        buy_X.push(trade.close_time[i]);
        buy_Y.push(trade.price[i]);
        equity -= numVolume * convertNumber(trade.price[i]);
        balance -= numVolume * convertNumber(trade.price[i]);
        if (equity < 0) {
          $("#alert").append(
            `<div class="alert alert-danger">Day <strong>${trade.close_time[i]}</strong> equity less than 0</div>`
          );
        }
        output.push(
          `<tr><td>${trade.close_time[i]}</td><td>Buy ${numVolume} unit</td><td>${trade.price[i]}</td><td>${trade.investment[i]}</td><td>${equity}</td><td>${balance}</td></tr>"`
        );
    }
  }

  return {
    "overall gain": overall_gain,
    "overall investment": (
      (overall_gain * 100) /
      convertNumber(initial_money)
    ).toFixed(2),
    sell_Y: sell_Y,
    sell_X: sell_X,
    buy_Y: buy_Y,
    buy_X: buy_X,
    output: output,
  };
}

function getMarkPoints(my_investment, new_date) {
  var markpoints = [];
  for (var i = 0; i < my_investment.buy_X.length; i++) {
    ind = new_date.indexOf(my_investment.buy_X[i]);
    if (ind > 0)
      markpoints.push({
        name: "buy",
        value: "buy",
        xAxis: ind,
        yAxis: my_investment.buy_Y[i],
        itemStyle: { color: "green" },
      });
  }

  for (var i = 0; i < my_investment["sell_X"].length; i++) {
    ind = new_date.indexOf(my_investment.sell_X[i]);
    if (ind > 0)
      markpoints.push({
        name: "sell",
        value: "sell",
        xAxis: ind,
        yAxis: my_investment.sell_Y[i],
        itemStyle: { color: "#c23531" },
      });
  }
  return markpoints;
}

function getNextDay(isStock, somedate) {
  if (isStock) {
    switch (somedate.getDay()) {
      case 5:
        somedate.setDate(somedate.getDate() + 3);
        break;
      case 6:
        somedate.setDate(somedate.getDate() + 2);
        break;
      default:
        somedate.setDate(somedate.getDate() + 1);
    }
    return somedate;
  }
  somedate.setDate(somedate.getDate() + 1);
  return somedate;
}

function setTable(my_investment, initial_money) {
  $("#table-body").html("");
  $("#log-invest").html("");

  for (var i = 0; i < my_investment["output"].length; i++)
    $("#table-body").append(my_investment["output"][i]);
  $("#log-invest").append(
    "<h6 class='header'>Overall gain: " +
      my_investment["overall gain"] +
      ", Overall investment: " +
      my_investment["overall investment"] +
      "%, Init money: " +
      initial_money +
      "</h5>"
  );
}

function fetchMovies(url) {
  const response = fetch(url)
    .then(function (r) {
      return r.json();
    })
    .then(function (data) {
      var stocks = data.klines.data.reverse().map(function (el, idx) {
        return [
          convertNumber(el[0]),
          convertNumber(el[1]),
          convertNumber(el[2]),
          convertNumber(el[3]),
        ];
      });
      var stock_date = data.klines.date.reverse();
      var volume = data.klines.volume.reverse();
      var dataMA5, dataMA10, dataMA20, dataMA30;
      var predicted_val = data.klines.prediction.reverse();

      dataMA5 = calculateMA(5, stocks);
      dataMA10 = calculateMA(10, stocks);
      dataMA20 = calculateMA(20, stocks);
      dataMA30 = calculateMA(30, stocks);
      var my_investment = getMyInvestment(
        data.trade,
        data.coin_info.initial_money
      );

      var predictions = JSON.parse(data.coin_info.predictions);
      new_date = stock_date.slice();
      if (predictions) {
        for (var k = 0; k < predictions.length; k += 1) {
          predicted_val.push(predictions[k]);
          somedate = new Date(new_date[new_date.length - 1]);
          somedate = getNextDay(false, somedate);
          dd = somedate.getDate();
          mm = somedate.getMonth() + 1;
          y = somedate.getFullYear();
          new_date.push(
            y.toString() + "-" + mm.toString() + "-" + dd.toString()
          );
        }
      }

      var markpoints = getMarkPoints(my_investment, new_date);
      const option = {
        animation: false,
        color: color_list,
        title: {
          left: "center",
        },
        legend: {
          top: 30,
          data: [
            "STOCK",
            "MA5",
            "MA10",
            "MA20",
            "MA30",
            "predicted close",
            "sell",
            "buy",
          ],
        },
        tooltip: {
          trigger: "axis",
          position: function (pt) {
            return [pt[0], "10%"];
          },
        },
        axisPointer: {
          link: [
            {
              xAxisIndex: [0, 1],
            },
          ],
        },
        dataZoom: [
          {
            type: "slider",
            xAxisIndex: [0, 1],
            realtime: false,
            start: 0,
            end: 100,
            top: 65,
            height: 20,
            handleIcon:
              "M10.7,11.9H9.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4h1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z",
            handleSize: "120%",
          },
          {
            type: "inside",
            xAxisIndex: [0, 1],
            start: 40,
            end: 70,
            top: 30,
            height: 20,
          },
        ],
        xAxis: [
          {
            type: "category",
            data: new_date,
            boundaryGap: false,
            axisLine: { lineStyle: { color: "#777" } },
            axisLabel: {
              formatter: function (value) {
                return echarts.format.formatTime("MM-dd", value);
              },
            },
            min: "dataMin",
            max: "dataMax",
            axisPointer: {
              show: true,
            },
          },
          {
            type: "category",
            gridIndex: 1,
            data: stock_date,
            scale: true,
            boundaryGap: false,
            splitLine: { show: false },
            axisLabel: { show: false },
            axisTick: { show: false },
            axisLine: { lineStyle: { color: "#777" } },
            splitNumber: 20,
            min: "dataMin",
            max: "dataMax",
            axisPointer: {
              type: "shadow",
              label: { show: false },
              triggerTooltip: true,
              handle: {
                show: true,
                margin: 30,
                color: "#B80C00",
              },
            },
          },
        ],
        yAxis: [
          {
            scale: true,
            splitNumber: 2,
            axisLine: { lineStyle: { color: "#777" } },
            splitLine: { show: true },
            axisTick: { show: false },
            axisLabel: {
              inside: true,
              formatter: "{value}\n",
            },
          },
          {
            scale: true,
            gridIndex: 1,
            splitNumber: 2,
            axisLabel: { show: false },
            axisLine: { show: false },
            axisTick: { show: false },
            splitLine: { show: false },
          },
        ],
        grid: [
          {
            left: 20,
            right: 20,
            top: 110,
          },
          {
            left: 20,
            right: 20,
            top: 400,
          },
        ],
        graphic: [
          {
            type: "group",
            left: "center",
            top: 70,
            width: 300,
            bounding: "raw",
            children: [
              {
                id: "MA5",
                type: "text",
                style: { fill: color_list[1] },
                left: 0,
              },
              {
                id: "MA10",
                type: "text",
                style: { fill: color_list[2] },
                left: "center",
              },
              {
                id: "MA20",
                type: "text",
                style: { fill: color_list[3] },
                right: 0,
              },
            ],
          },
        ],
        series: [
          {
            name: "Volume",
            type: "bar",
            xAxisIndex: 1,
            yAxisIndex: 1,
            itemStyle: {
              normal: {
                color: "#7fbe9e",
              },
              emphasis: {
                color: "#140",
              },
            },
            data: volume,
          },
          {
            type: "candlestick",
            name: "STOCK",
            data: stocks,
            markPoint: {
              data: markpoints,
            },
            itemStyle: {
              normal: {
                color: "#14b143",
                color0: "#ef232a",
                borderColor: "#14b143",
                borderColor0: "#ef232a",
              },
              emphasis: {
                color: "black",
                color0: "#444",
                borderColor: "black",
                borderColor0: "#444",
              },
            },
          },
          {
            name: "MA5",
            type: "line",
            data: dataMA5,
            smooth: true,
            showSymbol: false,
            lineStyle: {
              normal: {
                width: 1,
              },
            },
          },
          {
            name: "MA10",
            type: "line",
            data: dataMA10,
            smooth: true,
            showSymbol: false,
            lineStyle: {
              normal: {
                width: 1,
              },
            },
          },
          {
            name: "MA20",
            type: "line",
            data: dataMA20,
            smooth: true,
            showSymbol: false,
            lineStyle: {
              normal: {
                width: 1,
              },
            },
          },
          {
            name: "MA30",
            type: "line",
            data: dataMA30,
            smooth: true,
            showSymbol: false,
            lineStyle: {
              normal: {
                width: 1,
              },
            },
          },
          {
            name: "predicted close",
            type: "line",
            data: predicted_val,
            smooth: false,
            showSymbol: false,
            lineStyle: {
              normal: {
                width: 2,
              },
            },
          },
        ],
      };

      var chart_stock = echarts.init(document.getElementById("div_output"));
      chart_stock.setOption(option, true);
      document.getElementById("initialmoney").value = data.coin_info.initial_money;
      setTable(my_investment, data.coin_info.initial_money);
      return {
        trade: data.trade,
        coin_info: data.coin_info,
      };
    });
  return response;
}

function findGetParameter(parameterName) {
  var result = null,
    tmp = [];
  var items = location.search.substr(1).split("&");
  for (var index = 0; index < items.length; index++) {
    tmp = items[index].split("=");
    if (tmp[0] === parameterName) result = decodeURIComponent(tmp[1]);
  }
  return result;
}
var symbol = findGetParameter("symbol");
var data = fetchMovies(`/admin/api/chart?symbol=${symbol}`);

function changeVolume() {
  var volume = document.getElementById("volumemax").value;
  var initial_money = document.getElementById("initialmoney").value;
  var margin = document.getElementById("margin").value;
  console.log(margin);
  data.then(function (dt) {
    var my_investment = getMyInvestment(dt.trade, initial_money, volume, margin);
    setTable(my_investment, initial_money);
  });
}
