<template>
    <nav class="navbar navbar-expand-lg navbar-light fixed-nav">
        <a class="navbar-brand" href="/admin/dashboard">Dashboard</a>
        <SearchBar />
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav ml-auto">
                <li class="nav-item">
                    <a href="/admin/add-product" class="nav-link">Add Product</a>
                </li>
                <li class="nav-item">
                    <a href="/admin/add-category" class="nav-link">Add Category</a>
                </li>
                <li class="nav-item">
                    <a href="/admin/cart" class="nav-link">Cart</a>
                </li>
                <li class="nav-item">
                    <a href="/admin/orders" class="nav-link">Orders</a>
                </li>
                <li class="nav-item">
                    <a href="/requests" class="nav-link">Requests</a>
                </li>
                <li class="nav-item">
                    <a href="/admin/profile" class="nav-link">Profile</a>
                </li>
            </ul>
        </div>
    </nav>
</template>

<script>
import SearchBar from './SearchBar.vue';
export default {
    name: "AdminNav",
    components: {
        SearchBar
    }
}
</script>
