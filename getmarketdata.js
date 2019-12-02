function getMarketData() {
  
  var response = UrlFetchApp.fetch("https://steemmonsters.com/market/for_sale_grouped");
  Logger.log(response.getContentText());
  var data = JSON.parse(response.getContentText());
  var cardresponse = UrlFetchApp.fetch("https://steemmonsters.com/cards/get_details");
  var card_data = JSON.parse(cardresponse.getContentText());
  var sheet = SpreadsheetApp.getActiveSheet();
  var sorting_range = sheet.getRange("A2:L1000");
  sorting_range.sort([{column: 1, ascending: true}, {column: 4, ascending: false}, {column: 3, ascending: true}]);
  var max_bcx_table = {0: {0: {0: 379, 1: 86, 2: 32, 3: 8}, 1: {0: 31, 1: 17, 2: 8, 3: 3}}, 1: {0: {0: 505, 1: 115, 2: 46, 3: 11}, 1: {0: 38, 1: 22, 2: 10, 3: 4}}, 4: {0: {0: 400, 1: 115, 2: 46, 3: 11}, 1: {0: 38, 1: 22, 2: 10, 3: 4}}};
  for(var key in data) {
    var bcx_edition = 0
    var card_id = data[key]["card_detail_id"];
    var edition = "";
    if(data[key]["edition"] == 0){
      edition = "Alpha";
    }else if(data[key]["edition"] == 1){
      edition = "Beta";
      bcx_edition = 1;
    }else if(data[key]["edition"] == 2){
      edition = "Promo";
      if(data[key]["card_detail_id"] > 100){
        bcx_edition = 1;
      }
    }else if(data[key]["edition"] == 3){
      edition = "Reward";
      bcx_edition = 1;
    }else if(data[key]["edition"] == 4){
      edition = "Untamed";
      bcx_edition = 4;
    }
    var price = data[key]["low_price"];
    var bcx_price = data[key]["low_price_bcx"];
    var gold = "Regular";
    var bcx_gold = 0;
    if(data[key]["gold"]){
      gold = "Gold";
      bcx_gold = 1;
    }
    var card_name = card_data[parseInt(card_id) - 1]["name"];
    sheet.getRange(parseInt(key)+2, 1).setValue(card_id);
    sheet.getRange(parseInt(key)+2, 2).setValue(card_name);
    sheet.getRange(parseInt(key)+2, 3).setValue(edition);
    sheet.getRange(parseInt(key)+2, 4).setValue(gold);
    sheet.getRange(parseInt(key)+2, 5).setValue(price);
    sheet.getRange(parseInt(key)+2, 6).setValue(bcx_price);
    var rarity = card_data[parseInt(card_id) - 1]["rarity"] - 1;
    max_bcx = max_bcx_table[bcx_edition][bcx_gold][rarity];
    sheet.getRange(parseInt(key)+2, 7).setValue(max_bcx);

  }
  sheet.getRange("E:F").setNumberFormat("$####.00");
  sorting_range.sort([{column: 4, ascending: false}, {column: 3, ascending: true}, {column: 4, ascending: true}]);
}
