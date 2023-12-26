<template>
    <NavBar />
    <div class="auth-wrapper">
        <div class="auth-inner">
            <h3>Welcome to Our Grocery Store</h3>
        </div>
    </div>
</template>

<script>
import NavBar from '../components/Nav.vue';

export default {
    name: "HomePage",
    components: {
        NavBar,
    },
}
</script>