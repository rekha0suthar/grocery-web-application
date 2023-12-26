<template>
    <ManagerNav />
    <div class="card profile-card">
      <h3>Store Manager Profile</h3>
      <hr />
      <div class="card-body">
        <p><strong>First Name:</strong> {{ managerProfile[1] }} </p>
        <p><strong>Last Name:</strong> {{ managerProfile[2] }}</p>
        <p><strong>Username:</strong> {{ managerProfile[3] }}</p>
      </div>
      <button class="btn btn-primary" @click="logout">Logout</button>
    </div>
  </template>
    
  <script>
import ManagerNav from '@/components/ManagerNav.vue';
import { useStore } from 'vuex'
import { computed, onMounted } from 'vue';
import axios from 'axios';
import router from '@/router';

  export default {
    name: 'ManagerProfile',
    components: {
      ManagerNav
    },
    setup() {
    const store = useStore();

    const managerProfile = computed(() => store.state.managerProfile);

    const fetchManagerProfile = async () => {
      await store.dispatch('fetchManagerProfile')
    }

    onMounted(() => {
      fetchManagerProfile();
    })

    const logout = async () => {
      try {
        console.log(localStorage.access_token)
        const response = await axios.post('/logout', null, { headers: { Authorization: `Bearer ${localStorage.access_token}`}});

        alert(response.data.message);

        localStorage.removeItem('access_token');
        router.push('/store-manager/login');
      }
      catch(error) {
        console.error(error.response.data.message);
        alert('Logout failed');
      }
    }

    return { managerProfile, fetchManagerProfile, logout}
  }
  
  };
  </script>
  <style>
  .profile-card {
    margin: auto;
    width: 450px;
    padding: 20px;
    margin-top: 250px;
  }
  
  .profile-card .card-body p {
    text-align: start;
    margin-left: 40px;
    font-size: 24px;
  }
  
  .profile-card strong {
    margin-right: 20px;
  }
  </style>
    