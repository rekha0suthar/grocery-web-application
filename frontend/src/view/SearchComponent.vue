<template>
    <!-- Search Product section -->
    <div class="product-container"  v-for="productsByCategory in searchProduct" :key="productsByCategory.category_id">
        <div class="category"><h3>{{ productsByCategory.category_name }}</h3></div>

        <div class="row">
            <ul class="col" v-for="product in productsByCategory.products" :key="product[0]">
                <li class="card" >
                    <div class="card-body">
                        <img :src="product[5]" alt="Product Image" />
                        <h5 class="card-title"> {{ product[1] }}</h5>
                        <p class="card-text">Price: ₹ {{ product[2] }} / {{ product[3] }}</p>
                        <p class="card-text">Expiry Date: {{ product[4] }}</p>
                        <p class="card-text">Quantity: {{ product[6] }}</p>
                        <div>
                            <button class="btn btn-outline-success mr-10">ADD</button>

                        </div>
                    </div>
                </li>
            </ul>
            <p class="text" v-if="searchProduct.length === 0">No product found</p>

        </div>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    name: 'SearchComponent',
    data() {
        return {
            searchProduct: [],
        }
    },
    mounted() {
        const query = this.$route.query.query
        // Retrieve categories from API
        axios.get(`/search/${query}`, {
            headers: {
                'Content-Type': 'application/json'
            },
        })
            .then(response => {
                this.searchProduct = response.data.query;
            })
            .catch(error => {
                console.log('Error fetching categories', error)
            })
    },
}
</script>
