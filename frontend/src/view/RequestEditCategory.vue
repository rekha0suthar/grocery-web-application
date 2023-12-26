<template>
    <div class="auth-wrapper">
        <div class="auth-inner">
            <form @submit.prevent="requestEditCategory">
                <h3>Request Edit Category</h3>
                <div class="form-group">
                    <label for="categoryName">Category Name</label>
                    <input type="text" id="categoryName" class="form-control" v-model="categoryName" />
                </div>
                
                <button class="btn btn-primary btn-block" type="submit">Edit Category</button>

            </form>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { onMounted, ref } from 'vue'
import router from '@/router'
import { useStore } from 'vuex';

export default {
    name: 'RequestEditCategory',
    setup() {
        const category_id = ref('');

        const categoryName = ref('');

        const store = useStore();
        
        onMounted(() => {
            category_id.value = router.currentRoute.value.params.category_id

            axios.get(`/admin/edit_category/${category_id.value}`, { headers: {'Content-Type': 'application/json'},})
            .then(response => {
                categoryName.value = response.data.category;
            })
            .catch(error => {
                console.log('Error fetching categories', error)
            })
        })

        const requestEditCategory = async () => {
            const name = categoryName.value
            const id = category_id.value
            console.log(name, id)
            // Send the category name to backend
            await store.dispatch('requestEditCategory', {categoryName: name, category_id: id})
        }
        return { categoryName, requestEditCategory }
    }
    
}

</script>
