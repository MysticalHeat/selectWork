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
    }
  },
  mounted() {

    if (localStorage.tree_config) {
      tree_config = $.parseJSON(localStorage.tree_config)
    }

    JSON.stringify(tree_config, (k, v) => {
      if (v.name && v.children.length > 0) {
      } else return v;

    });

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

</style>
