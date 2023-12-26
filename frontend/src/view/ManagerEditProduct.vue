<template>
    <div class="auth-wrapper">
        <div class="auth-inner">
            <form @submit.prevent="editProduct">
                <h3>Edit Product</h3>
                <div class="form-group">
                    <label for="name">Product Name</label>
                    <input type="text" id="name" class="form-control" v-model="productName" required />
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

                <button class="btn btn-primary btn-block" type="submit">Edit Product</button>
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
    name: 'ManagerEditProduct',
    setup() {
        const productName = ref('');
        const price = ref(0);
        const expiryDate = ref('');
        const productUnit = ref('');
        const quantity = ref(0);
        const imageUrl = ref('');
        const selectedCategory = ref(null);
        const product_id = ref('')

        const store = useStore();

        const categories = computed(() => store.state.categories)


        const fetchCategories = async () => {
            await store.dispatch('fetchCategories')
        }

        onMounted(() => {
            fetchCategories();
            product_id.value = router.currentRoute.value.params.product_id
        
            axios.get(`/edit_product/${product_id.value}`, {
                headers: {
                    'Content-Type': 'application/json'
                },
            })
                .then(response => {
                    const product = response.data.product
                    productName.value = product[1];
                    price.value = product[2];
                    productUnit.value = product[3];
                    expiryDate.value = product[4];
                    imageUrl.value = product[5];
                    quantity.value = product[6];
                    selectedCategory.value = product[7];
                    categories.value = response.data.categories
                })
                
                .catch(error => {
                    console.error('Error fetching categories', error)
                })
        });
        const editProduct = async() => {
            product_id.value = router.currentRoute.value.params.product_id
            // Send the category name to backend
            try {
                const response = await axios.put(`/edit_product/${product_id.value}`, {
                    product_name: productName.value,
                    price: price.value,
                    product_unit: productUnit.value,
                    expiry_date: expiryDate.value,
                    image_path: imageUrl.value,
                    quantity: quantity.value,
                    category_id: selectedCategory.value
                })
                alert(response.data.message)
                productName.value = '',
                price.value = 0,
                productUnit.value = '',
                expiryDate.value = '',
                imageUrl.value = '',
                quantity.value = 0,
                selectedCategory.value = null
            }
            catch (error) {
                alert('Failed to updated product')
            }
            router.push('/store-manager/dashboard')
        }
        return {productName, price, productUnit, expiryDate, imageUrl, quantity, selectedCategory, categories, editProduct}
    }
}

</script>
