<template>
    <form class="form-inline" @submit.prevent="search">
        <input class="form-control " type="text" v-model="searchQuery"
            placeholder="Search products" />
    </form>
</template>
<script>
export default {
    name: 'SearchBar',
    data() {
        return {
            searchQuery: '',
        }
    },
    methods: {
        search() {
            this.$router.push({ name: 'search-product', query: {query: this.searchQuery}})
        }
    }
}
</script>
