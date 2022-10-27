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
        <form v-bind:action="'http://' + host" id="select_form" @submit.prevent="send_load">
          <div class="row">
            <h1>Имитатор событий</h1>
          </div>
          <div class="row">
            <div class="col-4">
              <select class="form-select" id="device_severity">
                <option selected disabled>Важность</option>
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
                <option value="4">4</option>
              </select>
            </div>
            <div class="col-8">
              <select class="form-select" id="device_select">
                <option selected disabled>Оборудование</option>
                <option v-for="item in tree_option" :key="item[3]" :value="item[0]" :disabled="item[2]"
                        :style="item[2] ? {'color': 'red'}: false">{{ item[1] }}
                </option>
              </select>
            </div>
          </div>
          <br>
          <div class="row" id="select_button">
            <button type="submit" class="btn btn-info">Отправить</button>
          </div>
        </form>
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
      tree_option: [],
      counter: 0
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
            class: 'circles'
          }));
          $(this).children('.circles').css({'margin-left': '150px'});
        }
      });

      var count = '';
      this.tree_filtering(data, count);
      this.counter = 0;

      if (!$('#hidden_device_id').length) {
        $('#device_select').append('<option hidden id="hidden_device_id" value="hidden">Hidden</option>');
      }
    },
    tree_filtering(tree_recur, count, isRecursed = false, parent = null) {
      tree_recur.forEach((value) => {
        if (value.children.length === 0) {
          this.tree_option.push([this.counter + ' _' + parent + ' _' + value.name, isRecursed ? '-' + count + value.name : count + value.name, false, this.counter]);
          this.counter += 1;
        }

        if (value.children.length > 0) {
          isRecursed ? count += '-' : false;
          this.tree_option.push([this.counter, '-' + count + value.name, true, this.counter]);
          this.counter += 1;
          this.tree_filtering(value.children, count + '-', true, value.name);
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
    send_load() {
      axios
        .post(this.host + '/send_imitator', {
          device_severity: $('#device_severity').val(),
          device_select: $('#device_select').val()
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

    $('#device_select').change(function () {
      var selected_option = $('#device_select option:selected');
      $('#hidden_device_id').removeAttr('selected').val(selected_option.val()).text(selected_option.text().replace(/[-+()]/g, '')).attr('selected', 'selected');
    });

    $('#exampleModal').on('shown.bs.modal', function () {
      $('#isDeviceExist').attr('disabled', 'disabled');
      var found = false;
      JSON.stringify(tree_config, (k, v) => {
        if (!found) {
          if (v.name && v.children.length > 0 && v.name === self.procData.parent) {
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
          if (v.name && v.children.length > 0 && v.name === self.procData.parent) {
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
