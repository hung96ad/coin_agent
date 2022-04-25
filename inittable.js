function convertNumber(num) {
  return num ? parseFloat(num) : 0;
}
fetch("/admin/api/coin_info")
  .then(function (response) {
    return response.json();
  })
  .then(function (data) {
    data = data.data;
    var url = "https://api.binance.com/api/v3/ticker/price";
    fetch(url)
      .then(function (response) {
        return response.json();
      })
      .then(function (dt) {
        var USDTs = [];
        dt.forEach((element) => {
          if (element.symbol.endsWith("USDT")) {
            USDTs.push({
              symbol: element.symbol,
              price: parseFloat(element.price),
            });
          }
        });
        var profitUSD = 0;
        var totalInitialMoney = 0;
        for (var i = 0; i < data.length; i++) {
          totalInitialMoney += convertNumber(data[i].initial_money);
          profitUSD += convertNumber(data[i].totalGain);
          var profitPer = (data[i].totalGain * 100) / data[i].initial_money;
          var result = USDTs.find(({ symbol }) => symbol === data[i].symbol);
          var htmlContent = `<tr> <td>${data[i].rank}</td> <td> <a href="chart.html?symbol=${data[i].symbol}">
              <img style='height: 24px; width: 24px; border-radius: 12px;' src='${data[i].image}'>
              ${data[i].symbol}</td> <td>${result.price}</td>`;

          // prediction
          if (result.price > data[i].prediction)
            htmlContent += `<td style='color: red;'>${data[i].prediction}</td>`;
          else if (result.price === data[i].prediction)
            htmlContent += `<td style='color: black;'>${data[i].prediction}</td>`;
          else
            htmlContent += `<td style='color: green;'>${data[i].prediction}</td>`;

          // action
          switch (data[i].suggestionType) {
            case "-1":
              htmlContent += `<td style='color: red; font-weight: bold;'>Sell at ${data[i].suggestionPrice} time ${data[i].date}</td>`;
              break;
            case "1":
              htmlContent += `<td style='color: green; font-weight: bold;'>Buy at ${data[i].suggestionPrice} time ${data[i].date}</td>`;
              break;
            default:
              htmlContent += `<td>No action</td>`;
          }
          var profitColor = data[i].totalGain > 0 ? "green" : "red";
          htmlContent += `<td style='color: ${profitColor};'>${
            data[i].totalGain
          }</td> <td style='color: ${profitColor};'>${profitPer.toFixed(
            2
          )}%</td>`;
          htmlContent += "</tr>";
          $("#table-body").append(htmlContent);
        }
        $("#totalCurrency").append(data.length);
        $("#totalProfitUSD").append("$" + profitUSD.toFixed(2));
        $("#totalInitialMoney").append("$" + totalInitialMoney.toFixed(2));
        $("#totalProfitPer").append(
          ((profitUSD * 100) / totalInitialMoney).toFixed(2) + "%"
        );
      });
  });

function sortTable(n) {
  var table,
    rows,
    switching,
    i,
    x,
    y,
    shouldSwitch,
    dir,
    switchcount = 0;
  table = document.getElementById("myTable");
  switching = true;
  //Set the sorting direction to ascending:
  dir = "asc";
  /*Make a loop that will continue until
    no switching has been done:*/
  while (switching) {
    switching = false;
    rows = table.rows;
    for (i = 1; i < rows.length - 1; i++) {
      shouldSwitch = false;
      x = rows[i].getElementsByTagName("TD")[n];
      y = rows[i + 1].getElementsByTagName("TD")[n];
      if (dir == "asc") {
        if (n == 1 || n == 4) {
          if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
            shouldSwitch = true;
            break;
          }
        } else {
          if (Number(x.innerHTML.replace("\%","")) > Number(y.innerHTML.replace("\%",""))) {
            shouldSwitch = true;
            break;
          }
        }
      } else if (dir == "desc") {
        if (n == 1 || n == 4) {
          if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
            shouldSwitch = true;
            break;
          }
        } else {
          if (Number(x.innerHTML.replace("\%","")) < Number(y.innerHTML.replace("\%",""))) {
            shouldSwitch = true;
            break;
          }
        }
      }
    }
    if (shouldSwitch) {
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      switchcount++;
    } else {
      if (switchcount == 0 && dir == "asc") {
        dir = "desc";
        switching = true;
      }
    }
  }
}
