<template>
    <UserNav/>
     <div class="card profile-card">
       <h3>User Profile</h3>
       <hr/>
       <div class="card-body">
         <p><strong>First Name:</strong> {{ userProfile[1] }} </p>
         <p><strong>Last Name:</strong> {{ userProfile[2] }}</p>
         <p><strong>Username:</strong> {{ userProfile[3] }}</p>
       </div>
       <button class="btn btn-primary" @click="logout">Logout</button>
     </div>
   </template>
<script>
import UserNav from '@/components/UserNav.vue';
import { useStore } from 'vuex'
import { computed, onMounted } from 'vue'
import axios from 'axios';
import router from '@/router';

export default {
    name: 'UserProfile',
    components: {
    UserNav
  },
  setup() {
    const store = useStore();

    const userProfile = computed(() => store.state.userProfile);

    const fetchUserProfile = async () => {
      await store.dispatch('fetchUserProfile')
    }

    onMounted(() => {
      fetchUserProfile();
    })

    const logout = async () => {
      try {
        console.log(localStorage.access_token)
        const response = await axios.post('/logout', null, { headers: { Authorization: `Bearer ${localStorage.access_token}`}});

        alert(response.data.message);

        localStorage.removeItem('access_token');
        router.push('/user/login');
      }
      catch(error) {
        console.error(error.response.data.message);
        alert('Logout failed');
      }
    }

    return { userProfile, fetchUserProfile, logout}
  }

}
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