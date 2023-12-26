<template>
    <AdminNav />
    <!-- Login Requests section -->
    <div class="cart-container row">
        <div class="cart-items requests-body" v-if="loginRequests.length > 0">
            <h3 class="cart-title">Store Manager Login Requests</h3>
            <hr />
            <div v-for="request in loginRequests" :key="request.id">
                <div class="card-body" style="display: flex; justify-content: space-between;">
                    <div style="text-align: left;">
                        <h5 class="card-title">Name: {{ request.first_name }} {{ request.last_name }}</h5>
                        <p class="card-text">Username: {{ request.username }}</p>
                    </div>
                    <div v-if="request.status == 'Pending'">
                        <button class="btn btn-success" style="margin-right: 10px;"
                            @click="approveRequest(request.token)">Approve</button>
                        <button class="btn btn-danger" @click="rejectRequest(request.token)">Reject</button>
                    </div>
                    <p v-if="request.status == 'Approved'">Approved</p>
                    <p v-if="request.status == 'Rejected'">Rejected</p>
                </div>
                <hr />
            </div>
        </div>
        <p class="cart-empty" v-if="loginRequests.length === 0">No requests</p>
    </div>
    <!-- Category Requests section -->
    <div class="cart-container row">
        <div class="cart-items requests-body" v-if="categoryRequests.length > 0">
            <h3 class="cart-title">Store Manager Category Requests</h3>
            <hr />
            <div v-for="categoryRequest in categoryRequests" :key="categoryRequest.id">
                <div class="card-body" style="display: flex; justify-content: space-between;">
                    <div style="text-align: left;">
                        <h5 class="card-title"> Category: {{ categoryRequest[1] }}</h5>
                        <p class="card-text">Manager Name: {{ categoryRequest[3] }}</p>
                        <p class="card-text">Request Type: {{ categoryRequest[4] }}</p>
                    </div>
                    <div v-if="categoryRequest[2] == 'Pending'">
                        <button class="btn btn-success" style="margin-right: 5px;"
                            @click="approveCategoryRequest(categoryRequest[0], categoryRequest[1], categoryRequest[4])">Approve</button>
                        <button class="btn btn-danger" style="margin-right: -20px;"
                            @click="rejectCategoryRequest(categoryRequest[0], categoryRequest[1], categoryRequest[4])">Reject</button>
                    </div>
                    <p v-if="categoryRequest[2] == 'Approved'">Approved</p>
                    <p v-if="categoryRequest[2] == 'Rejected'">Rejected</p>
                </div>
                <hr />
            </div>
        </div>
    </div>
</template>
<script>
import AdminNav from '@/components/AdminNav.vue';
import { useStore } from 'vuex'
import { computed, onMounted } from 'vue'

export default {
    name: 'RequestPage',
    components: {
        AdminNav
    },
    setup() {
        const store = useStore();

        const loginRequests = computed(() => store.state.loginRequests)
        const categoryRequests = computed(() => store.state.categoryRequests)

        const fetchLoginRequests = async () => {
            await store.dispatch('fetchLoginRequests')
        }

        const fetchCategoryRequests = async () => {
            await store.dispatch('fetchCategoryRequests')
        }
        onMounted(() => {
            fetchLoginRequests();
            fetchCategoryRequests();
        });

        const approveRequest = async (token) => {
            await store.dispatch('approveLoginRequest', { token })
        };

        const rejectRequest = async (token) => {
            await store.dispatch('rejectLoginRequest', { token })
        };

        const approveCategoryRequest = async (request_id, category_name, request_type) => {
            if(request_type == 'Add') {
                await store.dispatch('approveAddCategoryRequest', { request_id, category_name })
            } else if (request_type == 'Delete') {
                await store.dispatch('approveDeleteCategoryRequest', { request_id, category_name })
            } else {
                await store.dispatch('approveEditCategoryRequest', { request_id, category_name })
            }
        };

        const rejectCategoryRequest = async (request_id, category_name, request_type) => {
            if(request_type == 'Add') {
                await store.dispatch('rejectAddCategoryRequest', { request_id, category_name })
            } else if (request_type == 'Delete') {
                await store.dispatch('rejectDeleteCategoryRequest', { request_id })
            } else {
                await store.dispatch('rejectEditCategoryRequest', {request_id })
            }
        }

        return { loginRequests, categoryRequests, approveRequest, rejectRequest, approveCategoryRequest, rejectCategoryRequest}
    }
}
</script>
<style>
.requests-body {
    max-width: 700px;
    width: 100%;
    height: 500px;
    overflow-y: scroll;
}</style>