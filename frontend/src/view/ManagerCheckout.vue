<template>
    <div class="cart-container" style="margin-top: 350px;">
        <div class="pay-card">
            <h3 style="margin-bottom: 20px;">Checkout</h3>
            <p style="font-size: 24px; margin-bottom: 20px;">Pay {{ totalPrice }} and complete your order</p>
            <button class="btn btn-primary" @click="completeOrder(managerId)">Complete order</button>
        </div>
    </div>
</template>
<script>
import axios from 'axios';
export default {
    name: 'ManagerCheckout',
    data() {
        return {
            totalPrice: 0,
            managerId: null,
        }
    },
    mounted() {
        axios.get('/store_manager/checkout', { headers: { Authorization: `Bearer ${localStorage.access_token}` } })
            .then(response => {
                this.totalPrice = response.data.total_price
                this.managerId = response.data.manager_id

            })
    },
    methods: {
        async completeOrder(managerId) {
            const confirmation =  window.confirm('Are you sure you want to pay and complete your order?')
            if (confirmation) {
                try {
                    await axios.post('/store_manager/orders', {manager_id: managerId})
                    alert("Orders completed successfully")
                    this.$router.push('/store-manager/dashboard')
                }
                catch(error) {
                    console.error(error)
                }
            }
        }
    }
}

</script>
<style>
.pay-card {
    height: 200px;
    width: 450px;
    box-sizing: border-box;
    box-shadow: 0px 4px 10px rgba(34, 35, 58, 0.2);
    border-radius: 10px;
    transition: all .3s;
    padding: 20px;
    border-radius: 0px;
    margin-top: 20px;
    margin-left: 20px;
}
</style>