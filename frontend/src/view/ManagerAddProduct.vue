<template>
    <div class="auth-wrapper">
        <div class="auth-inner">
            <form @submit.prevent="addProduct">
                <h3>Add Product</h3>
                <div class="form-group">
                    <label for="name">Product Name</label>
                    <input type="text" id="name" class="form-control" v-model="productName"
                        placeholder="Enter product name..." required />
                </div>

                <div class="form-group">
                    <label for="price">Price</label>
                    <input type="number" id="price" class="form-control" v-model="price"
                        placeholder="Enter product price..." required />
                </div>

                <div class="form-group">
                    <label for="expiryDate">Expiry Date</label>
                    <input type="date" id="expiryDate" class="form-control" v-model="expiryDate"
                        placeholder="Enter product expiry date..." required />
                </div>

                <div class="form-group">
                    <label for="unit">Unit</label>
                    <input type="text" id="unit" class="form-control" v-model="productUnit"
                        placeholder="Enter product unit..." required />
                </div>

                <div class="form-group">
                    <label for="quantity">Quantity</label>
                    <input type="number" id="quantity" class="form-control" v-model="quantity"
                        placeholder="Enter product quantity..." required />
                </div>

                <div class="form-group">
                    <label for="imageUrl">Image URL</label>
                    <input type="url" id="imageUrl" class="form-control" v-model="imageUrl"
                        placeholder="Enter product image url..." required />
                </div>

                <div class="form-group">
                    <label for="category">Category</label>
                    <select id="category" class="form-control" v-model="selectedCategory" required>
                        <option v-for="category in categories" :key="category[0]" :value="category[0]">{{ category[1] }}
                        </option>
                    </select>
                </div>

                <button class="btn btn-primary btn-block" type="submit">Add Product</button>
            </form>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { useStore } from 'vuex'
import { computed, onMounted, ref } from 'vue'
import router from '@/router'

export default {
    name: 'ManagerAddProduct',
    setup(){
        const productName = ref('');
        const price = ref(0);
        const expiryDate = ref('');
        const productUnit = ref('');
        const quantity = ref(0);
        const imageUrl=  ref('');
        const selectedCategory = ref(null);

        const store = useStore();

        const categories = computed(() => store.state.categories)

        const fetchCategories = async () => {
            await store.dispatch('fetchCategories')
        }

        onMounted(() => {
            fetchCategories();
        });

        const addProduct = async () => {
            try {
                const response = await axios.post('/add_product', {
                    product_name: productName.value,
                    price: price.value,
                    product_unit: productUnit.value,
                    expiry_date: expiryDate.value,
                    image_path: imageUrl.value,
                    quantity: quantity.value,
                    category_id: selectedCategory.value,
                    role: 'manager'
                }, { headers: { Authorization: `Bearer ${localStorage.access_token}` } })
                alert(response.data.message)
                productName.value = '',
                price.value = 0,
                productUnit.value = '',
                expiryDate.value = '',
                imageUrl.value = '',
                quantity.value = 0,
                selectedCategory.value = null

                router.push('/store-manager/dashboard')
            }
            catch (error) {
                // handle errors
                alert('Product already exists')
            }
        }

        return { productName, price, productUnit, expiryDate, quantity, imageUrl, selectedCategory, categories, addProduct }
    }
}

</script>
