<template>
  <div class="container-fluid mt-5">
    <div class="row">
      <div class="col-3">
        <h1>Выборка из бд</h1>
        <form v-bind:action="'http://' + host + ':5000/'" @submit.prevent="sendAjax" id="form1" method="post">
          <div class="input-group">
            <span class="input-group-text">c</span><input type="text" name="time0" id="time0"
                                                          class="form-control form-control-sm">
            <span class="input-group-text">по</span><input type="text" name="time1" id="time1"
                                                           class="form-control form-control-sm">
          </div>
          <br>
          <input type="text" name="message" id="message" placeholder="сообщение"
                 class="form-control form-control-sm"><br>
          <select id="lasttime" name="lasttime" class="form-select form-select-sm"
                  aria-label=".form-select-sm example">
            <option selected value="6">Последние 100 записей</option>
            <option value="">За интервал времени</option>
            <option value="1">За последние 10 минут</option>
            <option value="2">За последние 30 минут</option>
            <option value="3">За последний час</option>
            <option value="4">За последние сутки</option>
            <option value="5">За последние 30 дней</option>
          </select><br>
          <div class="row">
            <div class="col-8">
              <input type="submit" class="btn btn-primary" value="Применить">
              <input type="reset" class="btn btn-secondary" value="Сбросить">
            </div>
            <div class="col-4 form-check form-switch">
              <input class="form-check-input" type="checkbox" role="switch" id="autoUpdate">
              <label class="form-check-label" for="autoUpdate">Авто-обновление</label>
            </div>
          </div>
          <br>
          <div class="row">
            <div class="col">
              <div class="btn-group-vertical">
                <button type="button" class="btn btn-info" id="import" @click="FindFile">Импорт
                  сообщений из файла CEF
                </button>
                <button type="button" class="btn btn-info" @click="sendLoad" id="export">Экспорт сообщений в файл CEF
                </button>
              </div>
            </div>
          </div>
          <br>

        </form>
        <div class="col">
          <div style="width:275px; height: 275px; margin: auto">
            <canvas id="myChart"></canvas>
          </div>
        </div>

      </div>
      <div class="col-9">
        <div class="">
          <div class="row">
            <div class="col">
              <div id="count">Количество строк: 0</div>
            </div>

            <div style="text-align:right" class="col-3">
              <span style="cursor:pointer" @click.prevent="togglevis"
                    class="toggle-vis">Отобразить/скрыть все колонки</span>
            </div>
          </div>
          <div id="tabledrag">
            <table id="table" class="table table-sm caption-top hover">
              <thead>
              <tr>
                <th scope="col">№</th>
                <th scope="col">Время записи</th>
                <th scope="col">Время события</th>
                <th scope="col">Источник</th>
                <th scope="col">Версия</th>
                <th scope="col">Поставщик устройств</th>
                <th scope="col">Продукт</th>
                <th scope="col">Версия устройства</th>
                <th scope="col">Идентификатор события</th>
                <th scope="col">Наименование события</th>
                <th scope="col">Приоритет</th>
                <th scope="col">Дополнительно</th>
                <th scope="col">Оригинал</th>
              </tr>
              </thead>
            </table>
          </div>
        </div>
      </div>
    </div>

    <form id="form2" :action="'http://' + host + ':5000/upload'" @submit="upload" target="rFrame" method="POST"
          enctype="multipart/form-data">
      <div class="hiddenInput">
        <input type="file" id="my_hidden_file" name="loadfile" @change="LoadFile">
        <input type="submit" id="my_hidden_load" style="display: none" value='Загрузить'>
      </div>
    </form>
    <iframe id="rFrame" name="rFrame" style="display: none"></iframe>

  </div>
</template>

<script>
import * as eventRdy from './events'
import axios from "axios";

var originalSetItem = localStorage.setItem;
localStorage.setItem = function (key, value) {
  const event = new Event('itemInserted');

  event.value = value;
  event.key = key;

  document.dispatchEvent(event);

  originalSetItem.apply(this, arguments);
}

var data = {
  labels: [],
  datasets: [{
    label: 'My First dataset',
    backgroundColor: ['rgb(83,95,201)', 'rgb(255,0,0)'],
    borderColor: ['rgb(83,95,201)', 'rgb(255,0,0)'],
    data: []
  }]
};
var config = {
  type: 'doughnut',
  data: data
};

var status = {
  high: 0,
  mid: 0,
  low: 0,
  very_low: 0
}

var table, myChart, timer, processed_data;

export default {
  data() {
    return {
      host: window.location.hostname,
      curHost: window.location.hostname + ':5000',
      processed_data_local: {
        id: null,
        sev: null,
        device_id: null,
        s_ra: null,
        s_rd: null,
        name: null
      }
    }
  },
  props: {
    procData: {
      type: Object,
      default: false
    }
  },
  watch: {
    procData: function (newVal) {
      this.processed_data_local = newVal;
    }
  },
  methods: {
    FindFile() {
      document.getElementById('my_hidden_file').click();
    },
    LoadFile() {
      document.getElementById('my_hidden_load').click();
    },
    sendAjax() {
      eventRdy.sendAjaxForm('form1', this.curHost, myChart, table);
    },
    upload() {
      eventRdy.upload('form2')
    },
    togglevis() {
      var columns = table.columns([2, 4, 6, 7, 9, 10, 12]);
      columns.visible(!columns.visible()[0]);
    },
    sendLoad() {
      eventRdy.sendLoad(this.curHost);
    },
    updateProcessedData() {
      $.ajax({
        type: 'POST',
        url: 'http://' + this.curHost + '/',
        data: 'select_processed=True',
        success: response => {
          processed_data = response.data
        },
        error: error => {
          console.log(error)
        }
      })
    },
    axi_status() {
      $.ajax({
        type: 'POST',
        url: 'http://' + this.curHost + '/',
        data: 'count_severity=true&processed=true',
        success: data => {
          var counter = 0;
          if (!localStorage.db_count_severity) {
            localStorage.setItem('db_count_severity', JSON.stringify(status));
          }
          var storage_count = JSON.parse(localStorage.db_count_severity);
          for (var key in status) {
            status[key] = data.severity[counter];
            if (parseInt(storage_count[key]) !== data.severity[counter]) {
              localStorage.setItem('db_count_severity', JSON.stringify(status));
              this.updateProcessedData();
            }
            counter += 1;
          }
        }
      });
      this.$emit('updateStatus', status);
      $.ajax({
        type: 'POST',
        url: 'http://' + this.curHost + '/count',
        success: response => {
          if (parseInt(localStorage.db_count) !== response.data) {
            localStorage.setItem('db_count', response.data);
          }
        }
      });
    }
  },
  mounted() {

    var self = this;
    var thisRow;

    this.updateProcessedData();

    if (table === undefined) {
      table = $('#table').DataTable(
        {
          language: {
            url: 'resources/js/datatables.ru.json'
          },
          searching: false,
          autoWidth: false,
          paging: true,
          info: false,
          scrollX: true,
          sScrollY: ($(window).height() - 300),
          scrollCollapse: true,
          lengthMenu: [20, 50, 100],
          createdRow: function (row, data, dataIndex) {
            if (processed_data.find(o => o.processed_id === data.id)) {
              $(row).addClass('read');
            }
          },
          columnDefs: [{
            targets: [11, 12],
            render: function (data, type, row) {
              if (type === 'display' && data != null) {
                data = data.replace(/<(?:.|\\n)*?>/gm, '');
                if (data.length > 50) {
                  return '<span title="' + data + '" class=\"show-ellipsis\">' + data.substr(0, 50) + '</span><span class=\"no-show\">' + data.substr(50) + '</span>';
                } else {
                  return data;
                }
              } else {
                return data;
              }
            }
          }],
          columns: [
            {data: '#'},
            {data: 'writing_utc'},
            {
              data: 'date_time',
              visible: false
            },
            {data: 'host'},
            {
              data: 'version',
              visible: false
            },
            {data: 'device_vendor'},
            {
              data: 'device_product',
              visible: false
            },
            {
              data: 'device_version',
              visible: false
            },
            {data: 'signature_id'},
            {
              data: 'name',
              visible: false
            },
            {
              data: 'severity',
              visible: false
            },
            {data: 'extension'},
            {
              data: 'original_message',
              visible: false
            },
            {
              data: 'id',
              visible: false
            }
          ],
        }
      );
      myChart = new Chart(document.getElementById('myChart'), config);
    }

    table.on('click', 'tbody tr', function () {
      $('#exampleModal').modal('show');
      self.$emit('updateProcData', table.row(this).data());
      thisRow = this;
    });

    setInterval(this.axi_status, 500);

    $('#procDataSubmit, #status_data_submit').click(function () {
      var comp_id = null;
      if (thisRow) {
        comp_id = table.row(thisRow).data()['id']
      }
      if (!processed_data.find(o => o.processed_id === comp_id) || $('#msgArea').val() !== '') {
        $.ajax({
          type: 'POST',
          url: 'http://' + self.curHost + '/',
          async: false,
          data: {
            processed_id: self.processed_data_local.id,
            severity: self.processed_data_local.sev,
            device_id: parseInt(self.processed_data_local.device_id)
          },
          success: function success(response) {
            var device = `#device_${self.processed_data_local.s_ra}_${self.processed_data_local.s_rd}_${self.processed_data_local.device_id}`;
            switch (self.processed_data_local.sev) {
              case 1: {
                $(device).css({'background-color': 'limegreen'});
                status.very_Low -= 1;
                break;
              }
              case 2: {
                $(device).css({'background-color': 'limegreen'});
                status.low -= 1;
                break;
              }
              case 3: {
                $(device).css({'background-color': 'limegreen'});
                status.mid -= 1;
                break;
              }
              case 4: {
                $(device).css({'background-color': 'limegreen'});
                status.high -= 1;
                break;
              }
            }
          }
        });
        $('#msgArea').val('').trigger('change');
        $(thisRow).addClass('read');
        processed_data.push({
          processed_id: self.processed_data_local.id,
          device_id: self.processed_data_local.device_id
        });
      }
      $('#exampleModal').modal('hide');
      thisRow = '';
      localStorageSetHandler();
    })

    $(window).resize(function () {
      $('.dataTables_scrollBody').css('height', ($(window).height() - 300));
    });

    $.datetimepicker.setLocale('ru');
    $('#time0').datetimepicker();
    $('#time1').datetimepicker();

    $('.tree-leaf-text').click(function () {
      var [, selected_s_ra, selected_s_rd, selected_id] = $(this).parent().children('.circles').first().attr('id').split('_');
      var isMsgExist = false;
      $.ajax({
        type: 'POST',
        url: 'http://' + self.curHost + '/',
        data: {time0: '', time1: '', message: '', lasttime: 6},
        success: (response) => {
          var table_response = response.data;
          table_response.every((value) => {
            var [device_info, device_id, device_s_ra, device_s_rd, device_name] = value.extension.match(/device_id=(.*)\ss_ra=(.*)\ss_rd=(.*)\sdevice_name=(.*)$/);
            if (!device_info) return true;
            if (selected_id === device_id && selected_s_ra === device_s_ra && selected_s_rd === device_s_rd  && !processed_data.find(o => o.processed_id === value.id)) {
              self.processed_data_local = {
                id: value.id,
                sev: value.severity,
                device_id: device_id,
                s_ra: device_s_ra,
                s_rd: device_s_rd,
                name: device_name
              }
              isMsgExist = true;
              $('#msgArea').val(value.original_message).trigger('change');
              return false
            } else return true;
          });
          if (!isMsgExist) {
            $('#msgArea').val('').trigger('change');
          }
        },
        error: function error(_error) {
          console.log(_error);
        }
      });
    });

    const localStorageSetHandler = function (e) {
      $.ajax({
        type: 'POST',
        url: 'http://' + self.curHost + '/',
        data: {time0: '', time1: '', message: '', lasttime: 6},
        success: (response) => {
          var table_response = response.data;
          table_response.reverse().forEach((value) => {
            var device_info = value.extension.match(/device_id=(.*)\ss_ra=(.*)\ss_rd=(.*)\sdevice_name=(.*)\s/);
            if (!device_info) return;
            var device_id = parseInt(device_info[1]);
            var device_severity = value.severity;
            var data_id = value.id;
            var circle_id = `device_${device_info[2]}_${device_info[3]}_${device_id}`;
            if (!processed_data.find(o => o.processed_id === data_id)) {
              switch (device_severity) {
                case 1: {
                  $('#' + circle_id).css({'background-color': 'limegreen'});
                  break
                }
                case 2: {
                  $('#' + circle_id).css({'background-color': 'yellow'});
                  break
                }
                case 3: {
                  $('#' + circle_id).css({'background-color': 'orange'});
                  break
                }
                case 4: {
                  $('#' + circle_id).css({'background-color': 'red'});
                  break
                }
              }
            }
          });
        },
        error: function error(_error) {
          console.log(_error);
        }
      });
    }

    localStorageSetHandler();

    document.addEventListener('itemInserted', localStorageSetHandler, false);

    $('#autoUpdate').change(function () {
      var chkbx = document.getElementById('autoUpdate');
      if (chkbx.checked) {
        timer = setInterval(eventRdy.sendAjaxForm, 5000, 'form1', self.curHost, myChart, table);
      } else {
        clearInterval(timer);
      }
    });
    $('#time0').change(function () {
      $('#lasttime').val(null);
    });
    $('#time1').change(function () {
      $('#lasttime').val(null);
    });
    $('#message').change(function () {
      var val = document.getElementsByName('lasttime')[0].value;
      if (val === '6') {
        $('#lasttime').val(null);
      }
    });
    $('#lasttime').change(function () {
      var startDate = new Date();
      var now = new Date();
      var val = document.getElementsByName('lasttime')[0].value;

      switch (val) {
        case '1': {
          startDate.setMinutes(startDate.getMinutes() - 10);
          document.getElementsByName('time0')[0].value = moment(startDate).format('yyyy/MM/DD HH:mm');
          document.getElementsByName('time1')[0].value = moment(now).format('yyyy/MM/DD HH:mm');
          break;
        }

        case '2': {
          startDate.setMinutes(startDate.getMinutes() - 30);
          document.getElementsByName('time0')[0].value = moment(startDate).format('yyyy/MM/DD HH:mm');
          document.getElementsByName('time1')[0].value = moment(now).format('yyyy/MM/DD HH:mm');
          break;
        }

        case '3': {
          startDate.setHours(startDate.getHours() - 1);
          document.getElementsByName('time0')[0].value = moment(startDate).format('yyyy/MM/DD HH:mm');
          document.getElementsByName('time1')[0].value = moment(now).format('yyyy/MM/DD HH:mm');
          break;
        }

        case '4': {
          startDate.setHours(startDate.getHours() - 24);
          document.getElementsByName('time0')[0].value = moment(startDate).format('yyyy/MM/DD HH:mm');
          document.getElementsByName('time1')[0].value = moment(now).format('yyyy/MM/DD HH:mm');
          break;
        }

        case '5': {
          startDate.setDate(startDate.getDate() - 30);
          document.getElementsByName('time0')[0].value = moment(startDate).format('yyyy/MM/DD HH:mm');
          document.getElementsByName('time1')[0].value = moment(now).format('yyyy/MM/DD HH:mm');
          break;
        }
        case '6': {
          $('#time0').val(null)
          $('#time1').val(null)
          $('#message').val(null)
        }
      }
    });
  }

}
</script>

<style>
span.no-show {
  display: none;
}

span.show-ellipsis:after {
  content: "...";
}

.container-fluid {
  font-size: 90%
}

tbody tr:hover {
  cursor: pointer;
}

.read {
  background-color: #e9e9e9 !important;
}

</style>
