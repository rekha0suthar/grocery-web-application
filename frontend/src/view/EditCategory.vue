<template>
    <div class="auth-wrapper">
        <div class="auth-inner">
            <form @submit.prevent="editCategory">
                <h3>Edit Category</h3>
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

export default {
    name: 'EditCategory',
    setup() {
        const category_id = ref('');

        const categoryName = ref('')
        
        onMounted(() => {
            category_id.value = router.currentRoute.value.params.category_id

            // fetch category name 
            axios.get(`/admin/edit_category/${category_id.value}`, { headers: {'Content-Type': 'application/json'},})
            .then(response => {
                categoryName.value = response.data.category;
            })
            .catch(error => {
                console.log('Error fetching categories', error)
            })
        })

        const editCategory = async () => {
            // Send the category name to backend
            try {
                const response = await axios.put(`/admin/edit_category/${category_id.value}`, {
                    category_name: categoryName.value,
                    category_id: category_id.value
                })
                alert(response.data.message)
            }
            catch(error) {
                alert('Failed to updated category')
            }
            router.push('/admin/dashboard')
        }
        return { category_id, categoryName, editCategory }
    }
    
}

</script>
