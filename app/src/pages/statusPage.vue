<template>
  <div class="container-fluid mt-5">
    <div class="row">
      <div class="col-6">
        <div id="tree">

        </div>
        <div class="btn-group-vertical">
          <button type="button" @click="$refs.js_file.click()" class="btn btn-info">
            Импорт из json
          </button>
          <input type="file" ref="js_file" style="display: none" id="js_import">
          <button type="button" class="btn btn-info" @click="download" id="js_export">
            Экспорт в json
          </button>
          <a id="download_config" style="display: none"></a>
        </div>
      </div>
      <div class="col-6">
        <div class="form-group">
          <label for="msgArea">Сообщение</label>
          <textarea class="form-control" id="msgArea" rows="7" cols="10" readonly style="resize:none"></textarea>
          <button type="button" id="status_data_submit" class="btn btn-primary" style="float:right; margin-top: 5px" disabled>Пометить как обработанное</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

var TreeView = require('js-treeview');

var tree_config = [
  {
    name: 'Item 1', children: []
  },
  {
    name: 'Item 2', expanded: true, children: [
      {name: 'Sub Item 1', children: []},
      {name: 'Sub Item 2', children: []}
    ]
  }
];

export default {
  name: "statusPage",
  data() {
    return {
      host: 'http://' + window.location.hostname + ':5000',
    }
  },
  props: {
    procData: {
      type: Object,
      default: false
    }
  },
  methods: {
    createTree(data) {
      var tree = new TreeView(data, 'tree');

      $('div .tree-leaf-content').each(function (i) {
        var obj = $.parseJSON($(this).attr('data-item'));

        if (obj.children.length === 0) {
          $(this).append($('<div>', {
            id: 'device_' + i,
            class: 'circles',
            style: 'margin-left: 150px'
          }));
          $(this).append($('<div>', {
            id: 'device_red_' + i,
            class: 'circles send',
            style: 'margin-left: 200px; background-color: red'
          }));
          $(this).append($('<div>', {
            id: 'device_orange_' + i,
            class: 'circles send',
            style: 'margin-left: 220px; background-color: orange'
          }));
          $(this).append($('<div>', {
            id: 'device_yellow_' + i,
            class: 'circles send',
            style: 'margin-left: 240px; background-color: yellow'
          }));
          $(this).append($('<div>', {
            id: 'device_green_' + i,
            class: 'circles send',
            style: 'margin-left: 260px; background-color: limegreen'
          }));
        }
      });
    },
    download() {
      var textToWrite = JSON.stringify(tree_config, null, 3);
      var fileNameToSaveAs = 'tree_config.json';

      var textFileAsBlob = new Blob([textToWrite], {type: 'text/plain;charset=utf-8'});

      var downloadLink = document.getElementById('download_config');
      downloadLink.download = fileNameToSaveAs;
      downloadLink.innerHTML = "Download File";
      downloadLink.href = window.webkitURL.createObjectURL(textFileAsBlob);
      downloadLink.click();
    },
    send_load(device_id, severity, s_ra, s_rd, device_name) {
      axios
        .post(this.host + '/send_imitator', {
          device_severity: severity,
          device_select: device_id + ' _' + s_ra + ' _' + s_rd + ' _' + device_name
        })
        .then((response) => console.log(response))
    }
  },
  mounted() {

    if (localStorage.tree_config) {
      tree_config = $.parseJSON(localStorage.tree_config)
    }

    this.createTree(tree_config);

    var self = this;

    $('#js_import').change(function (data) {
      var reader = new FileReader();
      reader.onload = onReaderLoad;
      reader.readAsText(data.target.files[0]);

      $('#js_import').val('');
    });

    function onReaderLoad(event) {
      localStorage.tree_config = event.target.result;
      tree_config = $.parseJSON(event.target.result);
      self.tree_option = [];
      self.createTree(tree_config);
    }

    $('.send').click(function () {
      var [_, sever_color, device_id] = $(this).attr('id').split('_');
      var parent = $(this).parents().eq(3).children()[0];
      var obj = $.parseJSON($(parent).attr('data-item'));
      var device_name = $.parseJSON($(this).parent().attr('data-item')).name;
      self.send_load(device_id, sever_color, obj.s_ra, obj.s_rd, device_name);
    });

    $('#msgArea').change(function() {
      if ($(this).val() === '') {
        $('#status_data_submit').attr('disabled', true)
      } else {
        $('#status_data_submit').attr('disabled', false)
      }
    });

    $('#exampleModal').on('shown.bs.modal', function () {
      $('#isDeviceExist').attr('disabled', 'disabled');
      var found = false;
      JSON.stringify(tree_config, (k, v) => {
        if (!found) {
          if (v.name && v.children.length > 0 && v.s_ra === self.procData.s_ra && v.s_rd === self.procData.s_rd) {
            if (v.children.find(o => o.name === self.procData.name)) found = true;
          } else return v;
        }
      });
      if (found === false) {
        $('#isDeviceExist').removeAttr('disabled');
      }
    });

    $('#isDeviceExist').click(function () {
      var found = false;
      JSON.stringify(tree_config, (k, v) => {
        if (!found) {
          if (v.name && v.children.length > 0 && v.s_ra === self.procData.s_ra && v.s_rd === self.procData.s_rd) {
            v.children.push({
              name: self.procData.name,
              children: []
            });
            found = true;
          } else return v;
        }
      });
      self.createTree(tree_config);
      localStorage.tree_config = JSON.stringify(tree_config);
      $('#isDeviceExist').attr('disabled', 'disabled');
    });
  }
}
</script>

<style scoped>

#tree {
  zoom: 1.5;
}

#select_button {
  padding-left: 12px;
  padding-right: 12px;
}


</style>
