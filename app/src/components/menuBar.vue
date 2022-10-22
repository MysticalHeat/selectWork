<template>
  <div class="col-3 menu">
    <div class=""></div>
  </div>
  <div class="col-9 status">
    <div style="background-color: red" class="circle">
      <div class="textCir"> {{ status.high }} </div>
    </div>
    <div style="background-color: orange" class="circle">
      <div class="textCir"> {{ status.mid }} </div>
    </div>
    <div style="background-color: yellow" class="circle">
      <div class="textCir"> {{ status.low }} </div>
    </div>
    <div style="background-color: green" class="circle">
      <div class="textCir"> {{ status.very_low }} </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "menuBar",
  props: {
    status: {
      type: Object,
      required: true
    }
  }
}
</script>

<style scoped>

.menu {
  display: table;
  height: 100px;
  margin: 0;
  padding: 0;
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
</style>
