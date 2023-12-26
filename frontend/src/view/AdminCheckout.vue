<template>
    <div class="cart-container" style="margin-top: 350px;">
        <div class="pay-card">
            <h3 style="margin-bottom: 20px;">Checkout</h3>
            <p style="font-size: 24px; margin-bottom: 20px;">Pay {{ totalPrice }} and complete your order</p>
            <button class="btn btn-primary" @click="completeOrder(adminId)">Complete order</button>
        </div>
    </div>
</template>
<script>
import axios from 'axios';
export default {
    name: 'AdminCheckout',
    data() {
        return {
            totalPrice: 0,
            adminId: null,
        }
    },
    mounted() {
        axios.get('/admin/checkout', { headers: { Authorization: `Bearer ${localStorage.access_token}` } })
            .then(response => {
                this.totalPrice = response.data.total_price
                this.adminId = response.data.admin_id
            })
    },
    methods: {
        async completeOrder(adminId) {
            const confirmation =  window.confirm('Are you sure you want to pay and complete your order?')
            if (confirmation) {
                try {
                    await axios.post('/admin/orders', {admin_id: adminId, role: 'admin'})
                    alert("Orders completed successfully")
                    this.$router.push('/admin/dashboard')
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