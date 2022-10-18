<template>
  <div class="container min-vh-100">
    <div class="row">
      <div class="col">
        <nav class="nav nav-fill">
          <a id="status" class="nav-link" @click="tabChange('status')">Состояниe</a>
          <a id="events" class="nav-link active" @click="tabChange('events')">События</a>
          <a id="settings" class="nav-link" @click="tabChange('settings')">Настройки</a>
        </nav>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "navBar",
  data() {
    return {
      currentPage: window.location.pathname
    }
  },
  methods: {
    tabChange(id) {
      $('a').removeClass('active');
      $('#' + id).addClass('active');
    }
  }
}
</script>

<style scoped>
.active {
  background-color: #0b5ed7;
  color: white;
}

a {
  writing-mode: vertical-lr;
  transform: rotate(-180deg);
  border: 2px solid #0b5ed7;
  margin-top: -2px;
  margin-right: -1.5px;
  font-size: 24px;
  padding: 4px 0
}

a:hover {
  cursor: pointer;
  background-color: #eaeaea;
}

.container {
  padding: 0
}

nav {
  display: flex;
  flex-direction: column;
  height: 100vh;
  padding-top: 100px;
}

</style>
