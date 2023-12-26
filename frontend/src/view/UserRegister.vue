<template>
    <NavBar />
    <div class="auth-wrapper">
        <div class="auth-inner">
            <form @submit.prevent="handleSubmit">
                <h3>Register</h3>
                <div class="form-group">
                    <label>First Name</label>
                    <input type="text" class="form-control" v-model="first_name" placeholder="First Name" required>
                </div>
                <div class="form-group">
                    <label>Last Name</label>
                    <input type="text" class="form-control" v-model="last_name" placeholder="Last Name" required>
                </div>
                <div class="form-group">
                    <label>Username</label>
                    <input type="text" class="form-control" v-model="username" placeholder="Username" required>
                </div>
                <div class="form-group">
                    <label>Password</label>
                    <input type="password" class="form-control" v-model="password" placeholder="Password" required>
                </div>
                <div class="form-group">
                    <label>Confirm Password</label>
                    <input type="password" class="form-control" v-model="password_confirm" placeholder="Confirm Password"
                        required>
                </div>
                <div class="form-group">
                    <label>Email</label>
                    <input type="email" class="form-control" v-model="email" placeholder="Email" required>
                </div>
                <a href="/user/login" class="link">Click Here to Login</a>
                <button class="btn btn-primary btn-block">Register</button>
            </form>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import NavBar from '../components/Nav.vue';
import { ref } from 'vue';
import router from '@/router';

export default {
    name: 'UserRegister',
    components: {
        NavBar,
    },
    setup() {
        const first_name = ref('');
        const last_name = ref('');
        const username = ref('');
        const password = ref('');
        const password_confirm = ref('');
        const email = ref('')

        const handleSubmit = async () => {
            if (password.value !== password_confirm.value) {
                alert('Passwords do not match');
                return;
            }

            // Password strength check
            const passwordRegex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).{8,}$/;
            if (!passwordRegex.test(password.value)) {
                alert('Password must contain at least 8 characters, including one uppercase letter, one lowercase letter, one digit, and one special character (@#$%^&+=)');
                return;
            }

            // Email Validation
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email.value)) {
                alert('Invalid email format');
                return;
            }

            try {
                const response = await axios.post('/get_token', {
                    first_name: first_name.value,
                    last_name: last_name.value,
                    username: username.value,
                    password: password.value,
                    role: 'user',
                    email: email.value
                });

                // Assuming the server returns an access token upon successful registration.
                const accessToken = response.data.access_token;

                // Store the access token in localStorage or a secure location for future requests.
                localStorage.setItem('access_token', accessToken);

                // Redirect the user to the login page or any other page as needed.
                router.push('/user/login');
            } catch (error) {
                console.error(error);
                alert('Registration failed');
            }
        }
        return { first_name, last_name, username, password, password_confirm, email, handleSubmit}
    }
}
</script>
