<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App',
}
</script>

<style>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}
body {
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  background: #f5f7fa;
  color: #303133;
}
#app {
  height: 100vh;
}
</style>
