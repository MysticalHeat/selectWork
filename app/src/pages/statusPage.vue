<template>
  <div class="container-fluid mt-5">
    <div id="tree">

    </div>
  </div>
</template>

<script>
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
  mounted() {
    var tree = new TreeView(tree_config, 'tree');

    $('div .tree-leaf-content').each(function (i) {
      var obj = $.parseJSON($(this).attr('data-item'));
      var block = parseInt($('div .tree-child-leaves').css('margin-left'), 10);

      if (obj.children.length === 0) {
        $(this).append($('<div>', {
          id: 'device_' + i,
          class: 'circles'
        }));
        if ($(this).closest('div .tree-child-leaves').length > 0) {
          $(this).children('.circles').css({'margin-left': 150-block+'px'});
        } else {
          $(this).children('.circles').css({'margin-left': '150px'});
        }
      }
    });
  }
}
</script>

<style scoped>

</style>
