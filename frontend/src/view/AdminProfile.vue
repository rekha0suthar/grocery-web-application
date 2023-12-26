<template>
  <AdminNav />
  <div class="card profile-card">
    <h3>Admin Profile</h3>
    <hr />
    <div class="card-body">
      <p><strong>First Name:</strong> {{ adminProfile[1] }} </p>
      <p><strong>Last Name:</strong> {{ adminProfile[2] }}</p>
      <p><strong>Username:</strong> {{ adminProfile[3] }}</p>
    </div>
    <button class="btn btn-primary" @click="logout">Logout</button>
  </div>
</template>
  
<script>
import AdminNav from '@/components/AdminNav.vue';
import { useStore } from 'vuex'
import { computed, onMounted } from 'vue'
import axios from 'axios';
import router from '@/router';

export default {
  name: 'AdminProfile',
  components: {
    AdminNav
  },
  setup() {
    const store = useStore();

    const adminProfile = computed(() => store.state.adminProfile);

    const fetchAdminProfile = async () => {
      await store.dispatch('fetchAdminProfile')
    }

    onMounted(() => {
      fetchAdminProfile();
    })

    const logout = async () => {
      try {
        console.log(localStorage.access_token)
        const response = await axios.post('/logout', null, { headers: { Authorization: `Bearer ${localStorage.access_token}`}});

        alert(response.data.message);

        localStorage.removeItem('access_token');
        router.push('/admin/login');
      }
      catch(error) {
        console.error(error.response.data.message);
        alert('Logout failed');
      }
    }

    return { adminProfile, fetchAdminProfile, logout}
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
  