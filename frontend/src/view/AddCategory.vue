<template>
    <div class="auth-wrapper">
        <div class="auth-inner">
            <form @submit.prevent="addCategory">
                <h3>Add Category</h3>
                <div class="form-group">
                    <label for="categoryName">Category Name</label>
                    <input type="text" id="categoryName" class="form-control" v-model="categoryName" placeholder="Enter product name..."
                        required>
                </div>
                
                <button class="btn btn-primary btn-block" type="submit">Add Category</button>

            </form>
        </div>
    </div>
</template>

<script>
import { ref } from 'vue'
import router from '@/router'
import { useStore } from 'vuex';

export default {
    name: 'AddCategory',
    setup() {
        const categoryName = ref('');

        const store = useStore(); 

        const addCategory = async () => {
            // Send the category name to backend
            await store.dispatch('addCategory', { categoryName: categoryName.value})
            router.push('/admin/dashboard')
        }
        return { categoryName, addCategory }
    }
}

</script>
