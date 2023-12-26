<template>
    <UserNav/>
    <!-- Product List By Category section -->
    <div class="product-container" v-for="category in productsByCategory" :key="category.category_name">
        <div class="category">
            <h3>{{ category.category_name }}</h3>
        </div>
        <div class="row">
            <ul class="col" v-for="product in category.products" :key="product.id">
                <li class="card">
                    <div class="card-body">
                        <img :src="product.image_path" alt="Product Image" />
                        <div class="name-price">
                            <h5 class="card-title"> {{ product.product_name }}</h5>
                            <p class="card-text"><strong>₹{{ product.price }} / {{ product.product_unit }}</strong></p>
                        </div>
                        <p class="card-text">Expiry Date: {{ product.expiry_date }}</p>
                        <p class="card-text">Quantity: {{ product.quantity }}</p>
                        <div>
                            <button class="btn btn-outline-success mr-10" v-if="product.quantity > 0 " @click="addToCart(product.id, product.product_name, product.price, product.product_unit, product.image_path)">ADD</button>
                            <button class="btn btn-outline-warning" style="margin-right: 7px;" v-if="product.quantity == 0">OUT OF STOCK</button>
                        </div>
                    </div>
                </li>
            </ul>
            <p class="text" v-if="category.products.length === 0">No product added</p>

        </div>
    </div>
</template>

<script>
import UserNav from '../components/UserNav.vue'
import { useStore } from 'vuex'
import { computed, onMounted } from 'vue'

export default {
    name: 'UserDashboard',
    components: {
        UserNav
    },
    setup() {
        const store = useStore();

        const productsByCategory = computed(() => store.state.productsByCategory)

        const fetchProductsByCategory = async () => {         
            await store.dispatch('fetchProductsByCategory')         
        }
        onMounted(() => {
            fetchProductsByCategory();
        });  

        const addToCart = async (product_id, product_name, price, product_unit, image_path, quantity) => {
            await store.dispatch('addToUserCart', {product_id, product_name, price, product_unit, image_path, quantity })
        };

        return { productsByCategory, addToCart };
    },
}
</script>
<style>
.product-container {
    margin-left: 30px;
    width: 100%;
}

.col {
    width: 280px;
    max-width: 320px;
}

.card {
    margin-bottom: 20px;
    box-shadow: 0px 14px 80px rgba(34, 35, 58, 0.2);
    border-radius: 10px;
    transition: all .3s;
    text-align: left;
    width: 280px;
}

img {
    width: 100%;
    height: 120px;
    margin-bottom: 15px;
}

.card-text {
    color: #666666;
}

.mr-10 {
    margin-right: 12px;
}
</style>