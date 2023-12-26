<template>
    <nav class="navbar navbar-expand-lg navbar-light fixed-nav">
        <a class="navbar-brand" href="/store-manager/dashboard">Dashboard</a>
        <SearchBar />
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav ml-auto">
                <li class="nav-item">
                    <a href="/store-manager/add-product" class="nav-link">Add Product</a>
                </li>
                <li class="nav-item">
                    <a href="/store-manager/request-add-category" class="nav-link">Add Category</a>
                </li>
                <li class="nav-item">
                    <a href="/store-manager/cart" class="nav-link">Cart</a>
                </li>
                <li class="nav-item">
                    <a href="/store-manager/orders" class="nav-link">Orders</a>
                </li>
                <li class="nav-item">
                    <a href="/store-manager/profile" class="nav-link">Profile</a>
                </li>
            </ul>
        </div>
    </nav>
</template>

<script>
import SearchBar from './SearchBar.vue';
export default {
    name: "ManagerNav",
    components: {
        SearchBar
    }
}
</script>

