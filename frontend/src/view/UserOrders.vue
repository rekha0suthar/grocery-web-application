<template>
    <UserNav />
    <div class="cart-container row">
        <div class="cart-items" v-if="orders.length > 0">
            <h3 class="cart-title">Your Orders</h3>
            <hr />
            <div v-for="product in orders" :key="product[3]">
                <div class="width">
                    <div class="card-body" style="display: flex;">
                        <img :src="product[7]" alt="Product Image" />
                        <div class="product-detail">
                            <h5 class="card-title"> {{ product[4] }}</h5>
                            <p class="card-text"><strong>₹{{ product[5] }} / {{ product[6] }} </strong></p>
                            <p class="card-text">Qty: {{ product[8] }}</p>
                        </div>
                    </div>
                </div>
                <hr />
            </div>
            <p class="price-text" v-if="orders.length > 0">Subtotal: <strong>₹{{ totalPrice }}</strong></p>
        </div>
        <p class="cart-empty" v-if="orders.length === 0">No Orders found</p>
    </div>
</template>
<script>
import UserNav from '@/components/UserNav.vue';
import { useStore } from 'vuex'
import { computed, onMounted } from 'vue'

export default {
    name: 'UserOrders',
    components: {
        UserNav
    },
    setup() {
        const store = useStore();

        const orders = computed(() => store.state.userOrders);
        const totalPrice = computed(() => store.state.userOrderTotal)

        onMounted(() => {
            store.dispatch('fetchUserOrders')
        })

        return { orders, totalPrice }
    }
}
</script>