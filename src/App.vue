<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>


export default {
  name: 'app'
}
</script>

<style>
  @import url('https://fonts.googleapis.com/css?family=Montserrat:400,700');

  body.intro {
  background-image: url("assets/background.jpg");
  background-size: cover;
  background-position: center center;
  background-repeat: no-repeat;
  background-color: #AAA0A0;
  font-family: 'Montserrat', sans-serif;
  display: grid;
  grid-template-rows: auto;
  justify-items: center;
  }
  body.main {
  background-size: cover;
  background-position: center center;
  background-repeat: no-repeat;
  background-color: #FFFFFF;
  font-family: 'Montserrat', sans-serif;
  display: grid;
  grid-template-rows: auto;
  justify-items: center;
  }
  body, html {
    margin: 0;
    height: 100%;
  }
  #app {
    width: 100%;
  }

  .title-label {
    font-size: 15pt;
    padding-bottom: 10px;
  }
</style>
