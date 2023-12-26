<template>
    <div class="auth-wrapper">
        <div class="auth-inner">
            <form @submit.prevent="requestToAddCategory">
                <h3>Request New Category</h3>
                <div class="form-group">
                    <label for="categoryName">Category Name</label>
                    <input type="text" id="categoryName" class="form-control" v-model="categoryName"
                        placeholder="Enter product name..." required>
                </div>

                <button class="btn btn-primary btn-block" type="submit">Add Category</button>

            </form>
        </div>
    </div>
</template>

<script>
import { useStore } from 'vuex';
import { ref } from 'vue'
import router from '@/router'

export default {
    name: 'ReuestAddCategory',
    setup() {
        const categoryName = ref('');

        const store = useStore();

        const requestToAddCategory = async () => {
            // Send the category name to backend
            await store.dispatch('requestAddCategory', { categoryName: categoryName.value })
            router.push('/store-manager/dashboard')
        }
        return { categoryName, requestToAddCategory }
    }
}

</script>
