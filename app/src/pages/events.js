export function upload(form_ajax) {
  var form = $("#" + form_ajax);
  var form_data = new FormData(form[0]);

  $.ajax({
    type: form.attr('method'),
    url: form.attr('action'),
    data: form_data,
    contentType: false,
    cache: false,
    processData: false,
    success: function (data) {
      $('#form2')[0].reset();
      alert('Данные успешно записаны.');
    }
  });
}

function generateLoad() {
  var stLoad;
  var form = $("#form1");
  var arrForm = form.serializeArray();
  var validate;
  arrForm.forEach(function (item) {
    if ((item === null || item === void 0 ? void 0 : item.value.length) > 0) {
      validate = true;
    }
  });

  if (validate) {
    $.ajax({
      type: form.attr('method'),
      url: form.attr('action'),
      data: form.serialize() + '&dwnldreq=1',
      async: false,
      success: function success(response) {
        stLoad = response.data;
      }
    });
  }

  var load = [];

  stLoad.slice().reverse().forEach(function (item) {
    var nTime = moment(item.writing_utc).format("MMM DD YYYY HH:mm:ss.SSSS");
    if (!item.original_message.includes('wr_t')) {
      load.push(item.original_message + ' wr_t=' + nTime + ' copied=1|\n');
    } else {
      load.push(item.original_message + '|\n')
    }
  });

  return load;
}

export function sendLoad(curHost) {
  var jsonData = generateLoad();
  var jsonString = JSON.stringify(jsonData);
  $.ajax({
    type: "POST",
    url: 'http://' + curHost + "/download",
    data: {data: jsonString},
    success: function (data) {
      var blob = new Blob([data], {type: "application/octetstream"});
      var isIE = false || !!document.documentMode;
      if (isIE) {
        window.navigator.msSaveBlob(blob, 'cef.log');
      } else {
        var now = moment();
        var new_time = now.format('DD-MM-YYYY_HH-mm-SS')
        var url = window.URL || window.webkitURL;
        var link = url.createObjectURL(blob);
        var a = $("<a />");
        a.attr("download", 'cef_' + new_time + '.log');
        a.attr("href", link);
        $("body").append(a);
        a[0].click();
        $("body").remove(a);
      }
    }
  });
}


export function sendAjaxForm(form_ajax, curHost, myChart, table) {
  var form = $("#" + form_ajax);
  var arrForm = form.serializeArray();
  var validate;
  arrForm.forEach(function (item) {
    if ((item === null || item === void 0 ? void 0 : item.value.length) > 0) {
      validate = true;
    }
  });

  if (validate) {
    $.ajax({
      type: form.attr('method'),
      url: form.attr('action'),
      data: form.serialize(),
      success: function success(response) {
        $('#count').html('Количество строк: ' + response.db_count + ' Отображено: ' + response.resp_count);
        table
          .clear()
          .rows.add(response.data.slice(0, 1000))
          .draw();
        myChart.data.labels = ['Запрос', 'Всего'];
        myChart.data.datasets[0].data = [response.resp_count, response.db_count - response.resp_count];
        myChart.update();
      },
      error: function error(_error) {
        console.log(_error);
      }
    });
  } else {
    $.ajax({
      type: 'POST',
      url: 'http://' + curHost + '/',
      data: 'validate=true',
      success: function success(response) {
        $('#count').html('Количество строк: 0');
        table
          .clear()
          .draw()
        myChart.data.labels = [];
        myChart.data.datasets[0].data = [];
        myChart.update();
      },
      error: function error(_error2) {
        console.log(_error2);
      }
    });
  }
}



