<template>
    <ManagerNav />
    <!-- Product List By Category section -->
    <div class="product-container">
        <!-- Export Csv Report section -->
        <div style="display: flex; justify-content: end; margin-right: 40px;">
            <button class="btn btn-outline-warning" @click="exportCsvReport()">EXPORT CSV
                REPORT</button>
        </div>
        <div style="margin-top: -30px; margin-bottom: 20px;" v-for="category in productsByCategory" :key="category.category_id">
            <div class="category">
                <h3>{{ category.category_name }}</h3>
                <i class="fa fa-edit" @click="requestEditCategory(category.category_id)"
                    style="font-size:20px;color:blue; margin-top: 8px;"></i>
                <i class="fa fa-remove" @click="requestDeleteCategory(category.category_id)"
                    style="font-size:24px;color:red; margin-top: 4px;"></i>
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
                                <button class="btn btn-outline-success mr-10" v-if="product.quantity > 0"
                                    @click="addToCart(product.id, product.product_name, product.price, product.product_unit, product.image_path)">ADD</button>
                                <button class="btn btn-outline-warning" style="margin-right: 7px;"
                                    v-if="product.quantity == 0">SOLD</button>
                                <button class="btn btn-outline-primary mr-10" @click="editProduct(product.id)">EDIT</button>
                                <button class="btn btn-outline-danger" @click="deleteProduct(product.id)">DELETE</button>
                            </div>
                        </div>
                    </li>
                </ul>
                <p class="text" v-if="category.products.length === 0">No product added</p>
            </div>
        </div>
    </div>
</template>

<script>
import ManagerNav from '../components/ManagerNav.vue'
import { useStore } from 'vuex'
import { computed, onMounted } from 'vue'
import router from '@/router'
import axios from 'axios'

export default {
    name: 'ManagerDashboard',
    components: {
        ManagerNav
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

        const requestDeleteCategory = async (category_id) => {
            await store.dispatch('requestDeleteCategory', { category_id })
        }

        const requestEditCategory = async (category_id) => {
            router.push({ name: 'store-manager-edit-category', params: { category_id: category_id } })
        }

        const editProduct = (product_id) => {
            router.push({ name: 'store-manager-edit-product', params: { product_id: product_id } })
        };

        const deleteProduct = async (product_id) => {
            await store.dispatch('deleteProduct', { product_id })
        };

        const addToCart = async (product_id, product_name, price, product_unit, image_path, quantity) => {
            await store.dispatch('addToManagerCart', { product_id, product_name, price, product_unit, image_path, quantity })
        };

        const exportCsvReport = async () => {
            try {
                await axios.post('/store_manager/export_csv_report', {role: 'manager'}, { headers: { Authorization: `Bearer ${localStorage.access_token}` } })
                alert('Your Report has been download in csv folder')

            }
            catch (error) {
                console.error(error)
            }
        }

        return { productsByCategory, editProduct, deleteProduct, addToCart, requestDeleteCategory, requestEditCategory, exportCsvReport };
    },
}
</script>
<style>
.product-container {
    margin-left: 30px;
    width: 100%;
}

h5 {
    font-weight: bold;
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
}

img {
    width: 100%;
    height: 120px;
    margin-bottom: 15px;
}

.name-price {
    display: flex;
    justify-content: space-between;
}

.card-text {
    color: #666666;
}

.mr-10 {
    margin-right: 12px;
}

h3 {
    text-align: left;
}

.category {
    display: flex;
}

i {
    margin-left: 20px;
    cursor: pointer;
}

.text {
    margin-left: 30px;
}
</style>