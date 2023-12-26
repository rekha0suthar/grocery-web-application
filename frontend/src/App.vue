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
body,
html,
#app,
#root,
.auth-wrapper {
  width: 100%;
  height: 100%;
}

#app {
  text-align: center;
  background-color: #ffffff;
}

h3 {
  text-align: center !important;
  font-weight: bold;
}

.navbar-light {
  background-color: black;
  box-shadow: 0px 14px 80px rgba(34, 35, 58, 0.2);
}

.navbar-light .navbar-nav .nav-link, .navbar-light .navbar-brand {
    color: white !important;
    font-size: 18px;
}

.navbar-light .navbar-nav .nav-link:hover, .navbar-light .navbar-brand:hover {
    color: white !important;
    font-size: 18px;
}

.navbar-light .navbar-toggler {
    background-color: white;
}


.auth-wrapper {
  display: flex;
  text-align: left;
  justify-content: center;
  flex-direction: column;
}

.auth-inner {
  width: 100%;
  max-width: 550px;
  margin: auto;
  background: #ffffff;
  box-shadow: 0px 14px 80px rgba(34, 35, 58, 0.2);
  padding: 40px 55px 45px 55px;
  border-radius: 15px;
  transition: all .3s;
}

.link {
    color: #212529;
    display: inline-block;
    margin-bottom: 0.5rem;
    font-size: 1rem;
}

@media screen and (max-width: 500px) {
  .auth-inner {
    margin: auto 10px;
  }
}
</style>
