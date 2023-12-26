<template>
    <nav class="navbar navbar-expand-lg navbar-light">
            <a href="/" class="navbar-brand">Home</a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav ml-auto">
                    <li class="nav-item">
                        <a href="/user/login" class="nav-link">User</a>
                    </li>
                    <li class="nav-item">
                        <a href="/store-manager/login" class="nav-link">Store Manager</a>
                    </li>
                    <li class="nav-item">
                        <a href="/admin/login" class="nav-link">Admin</a>
                    </li>
                </ul>
            </div>
    </nav>
</template>

<script>
export default {
    name: "NavBar"
}
</script>
