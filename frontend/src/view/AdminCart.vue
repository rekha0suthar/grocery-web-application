<template>
    <AdminNav />
    <div class="cart-container row">
        <!-- Cart item section -->
        <div class="cart-items" v-if="cartProducts.length > 0">
            <h3 class="cart-title">Your Cart</h3>
            <hr />
            <div v-for="product in cartProducts" :key="product[3]">
                <div class="width">
                    <div class="card-body" style="display: flex;">
                        <img :src="product[7]" alt="Product Image" />
                        <div class="product-detail">
                            <h5 class="card-title"> {{ product[4] }}</h5>
                            <p class="card-text"><strong>₹{{ product[5] }} / {{ product[6] }} </strong></p>
                            <p class="card-text">Qty: <input type="number" id="quantity" name="quantity" class="quantity"
                                    v-model="product[8]" min=1 @change="updateQuantity(product[3], product[8])" /></p>
                            <a class="remove" @click="removeFromCart(product[3])">Remove</a>
                        </div>

                    </div>
                </div>
                <hr />
            </div>
            <p class="price-text" v-if="cartProducts.length > 0">Subtotal ({{ totalItems }} items): <strong>₹{{ totalPrice
            }}</strong></p>
        </div>
        <p class="cart-empty" v-if="cartProducts.length === 0">Your cart is empty</p>
        <!-- Proceed to Checkout section -->
        <div class="card price-card" v-if="cartProducts.length > 0">
            <p class="text" style="font-size: 22px;">Subtotal ({{ totalItems }} items): <strong>₹{{ totalPrice }}</strong>
            </p>
            <button class="btn btn-primary" @click="checkout()">Proceed to Pay</button>
        </div>
    </div>
</template>
<script>
import AdminNav from '@/components/AdminNav.vue';
import { useStore } from 'vuex'
import { computed, onMounted } from 'vue'
import router from '@/router';

export default {
    name: 'AdminCart',
    components: {
        AdminNav
    },
    setup() {
        const store = useStore();

        const cartProducts = computed(() => store.state.adminCartProducts);
        const totalItems = computed(() => store.state.adminTotalItems);
        const totalPrice = computed(() => store.state.adminTotalPrice);

        onMounted(() => {
            store.dispatch('fetchAdminCartProducts')
        })

        const removeFromCart = async (product_id) => {
            await store.dispatch('removeFromCart', { product_id, role: 'admin'})               
        };

        const updateQuantity = async (product_id, newQuantity) => {
            await store.dispatch('updateQuantity', { product_id, newQuantity, role: 'admin' })
        };
        
        const checkout = () => {
            router.push('/admin/checkout')
        }

        return { cartProducts, totalItems, totalPrice, removeFromCart, updateQuantity, checkout }
    },
}

</script>
<style>
.cart-container {
    width: 100%;
    margin-top: 50px;
    display: flex;
    justify-content: space-evenly;

}

.cart-items {
    overflow: auto;
    box-sizing: border-box;
    box-shadow: 0px 4px 10px rgba(34, 35, 58, 0.2);
    border-radius: 10px;
    transition: all .3s;
    padding: 20px;
    border-radius: 0px;
    margin-left: 30px;

}

.price-card {
    height: 150px;
    width: 350px;
    box-sizing: border-box;
    box-shadow: 0px 4px 10px rgba(34, 35, 58, 0.2);
    border-radius: 10px;
    transition: all .3s;
    padding: 30px;
    border-radius: 0px;
    margin-top: 20px;
    margin-left: 30px;
}

.cart-title {
    text-align: left !important;
    margin-left: 20px;
    margin-bottom: 20px;
}

.product-detail {
    display: block;
    margin-left: 50px;
}

.width {
    width: 700px;
}

.price-text {
    text-align: end;
    padding-top: 10px;
}
.cart-empty {
    font-size: 28px;
}

img {
    width: 220px;
    height: 120px;
    margin-top: 10px;
}

.quantity {
    width: 40px;
    border-radius: 5px;
    margin-left: 5px;
    text-align: center;
    height: 25px;
}

.remove {
    cursor: pointer;
    color: red !important;
}
</style>