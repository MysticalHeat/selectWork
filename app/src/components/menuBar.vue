<template>
  <div class="col-3 menu">
    <div class="row table_name">
      <div class="input-group">
        <input id="change_input" type="text" class="form-control" v-model="table_name" disabled>
        <button id="change_btn" class="btn btn-primary" style="float: right" @click="change_table">Сменить</button>
      </div>
    </div>
  </div>
  <div class="col-9 status">
    <div>
      <div style="background-color: red" class="circle">
        <div class="textCir"> {{ status.high }}</div>
      </div>
      <span v-if="status.high > 0" class="badge badge-pill bg-primary p-2 rounded-circle border border-light count-notif">
        <span class="visually-hidden">New alerts</span>
      </span>
    </div>
    <div>
      <div style="background-color: orange" class="circle">
        <div class="textCir"> {{ status.mid }}</div>
      </div>
      <span v-if="status.mid > 0" class="badge badge-pill bg-primary p-2 rounded-circle border border-light count-notif">
        <span class="visually-hidden">New alerts</span>
      </span>
    </div>
    <div>
      <div style="background-color: yellow" class="circle">
        <div class="textCir"> {{ status.low }}</div>
      </div>
      <span v-if="status.low > 0" class="badge badge-pill bg-primary p-2 rounded-circle border border-light count-notif">
        <span class="visually-hidden">New alerts</span>
      </span>
    </div>
    <div style="background-color: green" class="circle">
      <div class="textCir"> {{ status.very_low }}</div>
    </div>
  </div>
</template>

<script>
export default {
  name: "menuBar",
  data() {
    return {
      table_name: localStorage.table_name ? localStorage.table_name: 'table_cef',
      host: window.location.hostname + ':5000'
    }
  },
  props: {
    status: {
      type: Object,
      required: true
    }
  },
  methods: {
    change_table() {
      var change_table = $('#change_input');
      if (change_table.is(':disabled')) {
        change_table.removeAttr('disabled')
      } else {
        localStorage.setItem('table_name', this.table_name);
        change_table.attr('disabled', true);
        $.ajax({
          type: 'POST',
          url: 'http://' + this.host + '/change_table',
          data: {table_name: this.table_name},
          success: (response) => {
          }
        });
      }
    }
  }
}
</script>

<style scoped>

.menu {
  display: table;
  height: 100px;
  margin: 0;
  padding: 5px;
  border-right: 2px solid #0b5ed7
}

.status {
  display: flex;
  justify-content: center;
  height: 100px;
  margin: 0;
  padding: 0;
}

.circle {
  background-color: lightgrey;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 10px;
  float: left;
  width: 80px;
  height: 80px;
  -moz-border-radius: 50px;
  -webkit-border-radius: 50px;
  border-radius: 50px;
  font-size: 18px;
}

.count-notif {
  vertical-align: middle;
  margin-left: -32px;
  margin-top: 10px;
  font-size: 13px;
}

.table_name {
  padding: 5px;
}

</style>
