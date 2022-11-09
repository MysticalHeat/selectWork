<template>

  <div class="app">
    <message-dialog>
      <div class="modal-header">
        <h5 class="modal-title" id="exampleModalLabel">Обрабатываемое сообщение</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>
      </div>
      <div class="modal-body">
        ID = {{ this.procData.id }} Важность = {{ this.procData.sev }} Название = {{ this.procData.name }}
      </div>
      <div class="modal-footer">
        <button type="button" id="isDeviceExist" class="btn btn-primary" disabled>Добавить</button>
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
        <button type="button" id="procDataSubmit" class="btn btn-primary">Пометить как обработанное</button>
      </div>
    </message-dialog>
    <div class="container-fluid">
      <div class="row">
        <div class="col-1 navigBar">
          <nav-bar></nav-bar>
        </div>
        <div class="col-11 mainDiv">
          <div class="row menuBar">
            <menu-bar v-bind:status="status"></menu-bar>
          </div>
          <div class="row statusPage">
            <status-page v-bind:procData="procData"></status-page>
          </div>
          <div class="row main" style="display: none">
            <event-form @updateStatus="setStatus" @updateProcData="setProcData" v-bind:procData="procData"></event-form>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
import navBar from "@/components/navBar";
import menuBar from "@/components/menuBar";
import eventForm from "@/pages/eventForm";
import messageDialog from "@/components/messageDialog";
import statusPage from "@/pages/statusPage"


export default {
  components: {
    navBar,
    menuBar,
    eventForm,
    messageDialog,
    statusPage
  },
  data() {
    return {
      status: {
        very_low: 0,
        low: 0,
        mid: 0,
        high: 0
      },
      procData: {
        id: null,
        sev: null,
        device_id: null,
        s_ra: null,
        s_rd: null,
        name: null
      }
    }
  },
  methods: {
    setStatus(data) {
      for (var key in this.status) {
        this.status[key] = data[key]
      }
    },
    setProcData(data) {
      this.procData.id = data.id;
      this.procData.sev = data.severity;
      var device = data.extension.match(/device_id=(.*)\ss_ra=(.*)\ss_rd=(.*)\sdevice_name=(.*)$/);
      this.procData.device_id = device[1];
      this.procData.s_ra = device[2];
      this.procData.s_rd = device[3];
      this.procData.name = device[4];
    }
  }
}
</script>

<style>
@import '../public/resources/css/jquery.dataTables.css';
@import '../public/resources/css/bootstrap.min.css';
@import '../public/resources/css/jquery.datetimepicker.css';
@import '../public/resources/css/Treant.css';
@import '../public/resources/css/perfect-scrollbar.css';
@import '../public/resources/css/style.css';
@import '../public/resources/css/treeview.min.css';

.navigBar {
  width: 64px;
  margin-right: -12px;
}

.app {
  margin: 0 auto;
}

.menuBar {
  height: 100px;
  width: 100%;
  margin: 0;
  padding: 0;
  border: solid #0b5ed7;
  border-width: 0 2px 2px 2px;
}

.container-fluid {
  margin: 0;
  padding-left: 0;
  width: 100%;
}

.col-11 {
  padding: 0;
  width: calc(100% - 64px);
}

.main {
  margin: 0 12px;
}

.statusPage {
  margin: 0 12px;
}


.circles {
  background-color: limegreen;
  display: flex;
  justify-content: center;
  align-items: center;
  float: left;
  margin: 3px;
  width: 15px;
  height: 15px;
  -moz-border-radius: 50px;
  -webkit-border-radius: 50px;
  border-radius: 50px;
  position: absolute;
}


</style>
