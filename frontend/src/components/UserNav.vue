<template>
    <nav class="navbar navbar-expand-lg navbar-light fixed-nav">
        <a class="navbar-brand" href="/user/dashboard">Dashboard</a>
        <SearchBar />
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav ml-auto">
                <li class="nav-item">
                    <a href="/user/cart" class="nav-link">Cart</a>
                </li>
                <li class="nav-item">
                    <a href="/user/orders" class="nav-link">Orders</a>
                </li>
                <li class="nav-item">
                    <a href="/user/profile" class="nav-link">Profile</a>
                </li>
            </ul>
        </div>
    </nav>
</template>

<script>
import SearchBar from './SearchBar.vue';
export default {
    name: "UserNav",
    components: {
        SearchBar
    }
}
</script>

