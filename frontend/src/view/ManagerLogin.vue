<template>
    <NavBar />
    <div class="auth-wrapper">
        <div class="auth-inner">
            <form @submit.prevent="handleSubmit">
                <h3>Login</h3>
                <div class="form-group">
                    <label>Username</label>
                    <input type="text" class="form-control" v-model="username" placeholder="Username" required>
                </div>
                <div class="form-group">
                    <label>Password</label>
                    <input type="password" class="form-control" v-model="password" placeholder="Password" required>
                </div>
                <a href="/store-manager/Register" class="link">Click Here to Register</a>
                <button class="btn btn-primary btn-block">Login</button>
            </form>
            <p v-if="message.length > 0">{{ message }}</p>

        </div>
    </div>
</template>
  
<script>
import axios from 'axios';
import NavBar from '../components/Nav.vue';
import { ref } from 'vue'
import router from '@/router'

export default {
    name: 'ManagerLogin',
    components: {
        NavBar,
    },
    setup() {
        const username = ref('');
        const password = ref('');
        const message = ref('');
        const status = ref('');

        const handleSubmit = async () => {
            try {
                const response = await axios.post('/store_manager/login', {
                    username: username.value,
                    password: password.value,
                });

                status.value = response.data.message[7]

                if (status.value == 'Approved') {
                    message.value = "Your request has been approved"
                    alert(message.value)
                    router.push('/store-manager/dashboard')
                }
                else if(status.value == 'Rejected'){
                    message.value = "Your request has been rejected"
                    alert(message.value)
                } 
                else {
                    message.value = "Your request is Pending"
                    alert(message.value)
                }


                const accessToken = response.data.access_token;

                // Store the access token in local storage
                localStorage.setItem('access_token', accessToken);

                // Now, include the access token in the headers for future requests
                const headers = {
                    Authorization: `Bearer ${accessToken}`,
                };

                // Fetch protected data using the access token
                await axios.get('/protected', {
                    headers,
                });

            } catch (error) {
                console.error(error);
                alert('Login failed');
            }
        }
        return { username, password, status, message, handleSubmit }

    },
};
</script>
