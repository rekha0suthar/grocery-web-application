import { createStore } from 'vuex';
import axios from 'axios';
import router from './router';

const store = createStore({
    state: {
        productsByCategory: [],
        categories: [],
        adminCartProducts: [],
        managerCartProducts: [],
        userCartProducts: [],
        adminTotalItems: 0,
        adminTotalPrice: 0,
        managerTotalItems: 0,
        managerTotalPrice: 0,
        userTotalItems: 0,
        userTotalPrice: 0,
        adminOrders: [],
        managerOrders: [],
        userOrders: [],
        userId: '',
        managerId: '',
        adminId: '',
        loginRequests: [],
        categoryRequests: [],
        adminProfile: [],
        managerProfile: [],
        userProfile: [],
        adminOrderTotal: 0,
        managerOrderTotal: 0,
        userOrderTotal: 0 
    },
    mutations: {
        // Define mutations to update state
        setProductsByCategory(state, products) {
            state.productsByCategory = products;
        },

        setCategories(state, categories) {
            state.categories = categories;
        },

        setAdminCartProducts(state, cartProducts) {
            state.adminCartProducts = cartProducts;
        },

        setManagerCartProducts(state, cartProducts) {
            state.managerCartProducts = cartProducts;
        },

        setUserCartProducts(state, cartProducts) {
            state.userCartProducts = cartProducts;
        },

        setAdminTotalItems(state, totalItems) {
            state.adminTotalItems = totalItems;
        },

        setAdminTotalPrice(state, totalPrice) {
            state.adminTotalPrice = totalPrice;
        },

        setManagerTotalItems(state, totalItems) {
            state.managerTotalItems = totalItems;
        },

        setManagerTotalPrice(state, totalPrice) {
            state.managerTotalPrice = totalPrice;
        },

        setUserTotalItems(state, totalItems) {
            state.userTotalItems = totalItems;
        },

        setUserTotalPrice(state, totalPrice) {
            state.userTotalPrice = totalPrice;
        },

        setAdminOrderTotal(state, totalPrice) {
            state.adminOrderTotal = totalPrice;
        },

        setManagerOrderTotal(state, totalPrice) {
            state.managerOrderTotal = totalPrice;
        },

        setUserOrderTotal(state, totalPrice) {
            state.userOrderTotal = totalPrice;
        },
        
        updateQuantity(state, { product_id, newQuantity, role }) {
            if (role == 'admin') {
                const productIndex = state.adminCartProducts.findIndex(product => product.product_id == product_id);
                if (productIndex !== -1) {
                    state.adminCartProducts[productIndex].quantity = newQuantity;
                }
            } else if (role == 'manager') {
                const productIndex = state.managerCartProducts.findIndex(product => product.product_id == product_id);
                if (productIndex !== -1) {
                    state.managerCartProducts[productIndex].quantity = newQuantity;
                }
            } else {
                const productIndex = state.userCartProducts.findIndex(product => product.product_id == product_id);
                if (productIndex !== -1) {
                    state.userCartProducts[productIndex].quantity = newQuantity;
                }
            }
        },

        setAdminOrders(state, orders) {
            state.adminOrders = orders;
        },

        setManagerOrders(state, orders) {
            state.managerOrders = orders;
        },

        setUserOrders(state, orders) {
            state.userOrders = orders;
        },

        setLoginRequests(state, requests) {
            state.loginRequests = requests;
        },

        setCategoryRequests(state, requests) {
            state.categoryRequests = requests;
        },

        setAdminProfile(state, profileData) {
            state.adminProfile = profileData;
        },

        setManagerProfile(state, profileData) {
            state.managerProfile = profileData;
        },

        setUserProfile(state, profileData) {
            state.userProfile = profileData;
        },

    },
    actions: {

        async fetchProductsByCategory({ commit }) {
            try {
                const response = await axios.get('/get_products');
                commit('setProductsByCategory', response.data.products);
            } catch (error) {
                console.error("Error fetching product by categories", error)
            }
        },

        async fetchCategories({ commit }) {
            try {
                const response = await axios.get('/get_categories');
                commit('setCategories', response.data.categories);
            } catch (error) {
                console.error("Error fetching categories", error)
            }
        },

        async deleteCategory({ dispatch }, { category_id }) {
            const confirmed = window.confirm('Are you sure you want to delete this category?')
            if (confirmed) {
                try {
                    await axios.delete(`/admin/delete_category/${category_id}`)
                    dispatch('fetchProductsByCategory')
                } catch (error) {
                    console.log(error)
                }
            }
        },

        async deleteProduct({ dispatch }, { product_id }) {
            const confirmed = window.confirm('Are you sure you want to delete this product?')
            if (confirmed) {
                try {
                    await axios.delete(`/delete_product/${product_id}`)
                    dispatch('fetchProductsByCategory')
                } catch (error) {
                    console.log(error)
                }
            }
        },

        async fetchAdminCartProducts({ commit }) {
            try {
                const response = await axios.get('/admin/cart', { headers: { Authorization: `Bearer ${localStorage.access_token}` } });
                commit('setAdminCartProducts', response.data.products)
                commit('setAdminTotalItems', response.data.total_count);
                commit('setAdminTotalPrice', response.data.total_price);
            }
            catch (error) {
                console.error(error);
            }
        },

        async fetchManagerCartProducts({ commit }) {
            try {
                const response = await axios.get('/store_manager/cart', { headers: { Authorization: `Bearer ${localStorage.access_token}` } });
                commit('setManagerCartProducts', response.data.products)
                commit('setManagerTotalItems', response.data.total_count);
                commit('setManagerTotalPrice', response.data.total_price);
            }
            catch (error) {
                console.error(error);
            }
        },

        async fetchUserCartProducts({ commit }) {
            try {
                const response = await axios.get('/user/cart', { headers: { Authorization: `Bearer ${localStorage.access_token}` } });
                commit('setUserCartProducts', response.data.products)
                commit('setUserTotalItems', response.data.total_count);
                commit('setUserTotalPrice', response.data.total_price);
            }
            catch (error) {
                console.error(error);
            }
        },

        async addToAdminCart({ dispatch }, { product_id, product_name, price, product_unit, image_path, quantity }) {
            try {
                const config = {
                    headers: {
                        Authorization: `Bearer ${localStorage.access_token}`
                    },
                };

                const data = {
                    product_id: product_id,
                    product_name: product_name,
                    price: price,
                    product_unit: product_unit,
                    image_path: image_path,
                    quantity: quantity,
                    role: 'admin'
                };
                await axios.post('/admin/cart', data, config)
                alert('Product added to cart successfully')
                dispatch('fetchAdminCartProducts')
            }
            catch (error) {
                alert('Product already exists in cart')
            }
        },

        async addToManagerCart({ dispatch }, { product_id, product_name, price, product_unit, image_path, quantity }) {
            try {
                const config = {
                    headers: {
                        Authorization: `Bearer ${localStorage.access_token}`
                    },
                };

                const data = {
                    product_id: product_id,
                    product_name: product_name,
                    price: price,
                    product_unit: product_unit,
                    image_path: image_path,
                    quantity: quantity,
                    role: 'manager'
                };
                await axios.post('/store_manager/cart', data, config)
                alert('Product added to cart successfully')
                dispatch('fetchManagerCartProducts')
            }
            catch (error) {
                alert('Product already exists in cart')
            }
        },

        async addToUserCart({ dispatch }, { product_id, product_name, price, product_unit, image_path, quantity }) {
            try {
                const config = {
                    headers: {
                        Authorization: `Bearer ${localStorage.access_token}`
                    },
                };

                const data = {
                    product_id: product_id,
                    product_name: product_name,
                    price: price,
                    product_unit: product_unit,
                    image_path: image_path,
                    quantity: quantity,
                    role: 'user'
                };
                await axios.post('/user/cart', data, config)
                alert('Product added to cart successfully')
                dispatch('fetchUserCartProducts')
            }
            catch (error) {
                alert('Product already exists in cart')
            }
        },

        async removeFromCart({ dispatch }, { product_id, role }) {
            const confirmed = window.confirm('Are you sure you want to remove this product from cart?')
            if (confirmed) {   
                try {
                    await axios.delete(`/remove_from_cart/${product_id}/${role}`, { headers: { Authorization: `Bearer ${localStorage.access_token}` } });
                    if (role == "admin") {
                        dispatch('fetchAdminCartProducts');
                    } else if (role == "manager") {
                        dispatch('fetchManagerCartProducts')
                    } else {
                        dispatch('fetchUserCartProducts')
                    }
                }
                catch (error) {
                    console.error(error);
                }
            }
        },

        async updateQuantity({ commit, dispatch }, { product_id, newQuantity, role }) {
            try {
                const response = await axios.put(`/update_quantity/${product_id}`, { quantity: newQuantity, role }, { headers: { Authorization: `Bearer ${localStorage.access_token}` } });
                if (role == 'admin') {
                    commit('updateQuantity', { product_id, newQuantity: response.data.quantity, role })
                    commit('setAdminTotalItems', response.data.total_items);
                    commit('setAdminTotalPrice', response.data.total_price);
                    console.log(response)
                    dispatch('fetchAdminCartProducts');
                } else if (role == 'manager') {
                    commit('updateQuantity', { product_id, newQuantity: response.data.quantity, role })
                    commit('setManagerTotalItems', response.data.total_items);
                    commit('setManagerTotalPrice', response.data.total_price);
                    dispatch('fetchManagerCartProducts');
                } else {
                    commit('updateQuantity', { product_id, newQuantity: response.data.quantity, role })
                    commit('setUserTotalItems', response.data.total_items);
                    commit('setUserTotalPrice', response.data.total_price);
                    dispatch('fetchUserCartProducts');
                    console.log(response)

                }
            }
            catch (error) {
                console.error(error);
            }
        },

        async fetchAdminOrders({ commit }) {
            try {
                const response = await axios.get('/admin/orders', { headers: { Authorization: `Bearer ${localStorage.access_token}` } })
                commit('setAdminOrders', response.data.orders);
                commit('setAdminOrderTotal', response.data.total_price)
            }
            catch (error) {
                console.error(error);
            }
        },

        async fetchManagerOrders({ commit }) {
            try {
                const response = await axios.get('/store_manager/orders', { headers: { Authorization: `Bearer ${localStorage.access_token}` } })
                commit('setManagerOrders', response.data.orders);
                commit('setManagerOrderTotal', response.data.total_price)
                console.log(response.data)
            }
            catch (error) {
                console.error(error);
            }
        },

        async fetchUserOrders({ commit }) {
            try {
                const response = await axios.get('/user/orders', { headers: { Authorization: `Bearer ${localStorage.access_token}` } })
                commit('setUserOrders', response.data.orders);
                commit('setUserOrderTotal', response.data.total_price)
            }
            catch (error) {
                console.error(error);
            }
        },

        async completeAdminOrder({ state, commit }) {
            const confirmation = window.confirm('Are you sure you want to pay and complete your order')
            if (confirmation) {
                try {
                    await axios.post('/admin/orders', { admin_id: state.adminId })
                    alert("Orders completed successfully")
                    commit('setAdminCheckout', null, 0)
                }
                catch (error) {
                    console.error(error)
                }
            }
        },

        async completeManagerOrder({ state, commit }) {
            const confirmation = window.confirm('Are you sure you want to pay and complete your order')
            if (confirmation) {
                try {
                    await axios.post('/store_manager/orders', { manager_id: state.managerId })
                    alert("Orders completed successfully")
                    commit('setManagerCheckout', null, 0)
                }
                catch (error) {
                    console.error(error)
                }
            }
        },

        async completeUserOrder({ state, commit }) {
            const confirmation = window.confirm('Are you sure you want to pay and complete your order')
            if (confirmation) {
                try {
                    await axios.post('/user/orders', { user_id: state.userId })
                    alert("Orders completed successfully")
                    commit('setUserCheckout', null, 0)
                }
                catch (error) {
                    console.error(error)
                }
            }
        },

        async fetchLoginRequests({ commit }) {
            try {
                const response = await axios.get('/admin/login_requests')
                commit('setLoginRequests', response.data.login_requests)
            }
            catch (error) {
                console.error(error)
            }

        },

        async fetchCategoryRequests({ commit }) {
            try {
                const response = await axios.get('/store_manager/request_add_category')
                commit('setCategoryRequests', response.data.cat_requests)
            }
            catch (error) {
                console.error(error)
            }

        },

        async approveLoginRequest({ commit, dispatch }, { token }) {
            try {
                await axios.post(`/approve_login_requests/${token}`)
                dispatch('fetchLoginRequests')
                commit('setRequestStatus', 'Approved')
            }
            catch (error) {
                console.error(error)
            }
        },

        async rejectLoginRequest({ commit, dispatch }, { token }) {
            try {
                await axios.post(`/reject_login_requests/${token}`)
                dispatch('fetchLoginRequests')
                commit('setRequestStatus', 'Rejected')

            }
            catch (error) {
                console.error(error)
            }
        },

        async addCategory({ dispatch }, { categoryName }) {
            try {
                const response = await axios.post('/admin/add_category', {
                    name: categoryName
                })
                alert(response.data.message)
                dispatch('fetchCategories')
            }
            catch (error) {
                alert('Category already exists')
            }
        },

        async requestAddCategory( { dispatch }, { categoryName }  ) {
            try {
                const response = await axios.post('/store_manager/request_add_category', {
                    name: categoryName
                }, { headers: { Authorization: `Bearer ${localStorage.access_token}` } })
                alert(response.data.message)
                dispatch('fetchCategories')
            }
            catch (error) {
                alert('Category already exists')
            }
        },

        async approveAddCategoryRequest({ dispatch }, { request_id, category_name }) {
            try {
                await axios.post('/approve/add_category_request', { request_id: request_id, category_name: category_name });
                dispatch('fetchCategoryRequests')
                dispatch('fetchCategories')
                dispatch('fetchProductsByCategory')
            }
            catch (error) {
                console.error(error)
            }
        },

        async rejectAddCategoryRequest({ dispatch }, { request_id }) {
            try {
                await axios.post('/reject/add_category_request', { request_id: request_id });
                dispatch('fetchCategoryRequests')
            }
            catch (error) {
                console.error(error)
            }
        },

        async requestDeleteCategory({ dispatch }, { category_id }) {
            const confirmed = window.confirm('Are you sure you want to delete this category?')
            if (confirmed) {
                try {
                    const response = await axios.post('/store_manager/request_delete_category', { category_id }, { headers: { Authorization: `Bearer ${localStorage.access_token}`}})
                    dispatch('fetchProductsByCategory')
                    dispatch('fetchCategoryRequests')
                    alert(response.data.message)
                } catch (error) {
                    alert('Request to delete this category is already sent, wait for approval')
                    console.log(error)
                }
            }
        },

        async approveDeleteCategoryRequest({ dispatch }, { request_id, category_name }) {
            try {
                console.log(request_id, category_name)
                await axios.delete(`/approve/delete_category_request/${category_name}/${request_id}`);
                dispatch('fetchCategoryRequests')
                dispatch('fetchCategories')
                dispatch('fetchProductsByCategory')
            }
            catch (error) {
                console.error(error)
            }
        },

        async rejectDeleteCategoryRequest({ dispatch }, { request_id }) {
            try {
                await axios.post(`/reject/delete_category_request/${request_id}`);
                dispatch('fetchCategoryRequests')
            }
            catch (error) {
                console.error(error)
            }
        },

        async requestEditCategory({ dispatch }, { categoryName, category_id }) {
            try {
                await axios.post('/store_manager/request_edit_category', {
                    category_name: categoryName,
                    category_id: category_id
                }, { headers: { Authorization: `Bearer ${localStorage.access_token}` } })
                alert("Your request has been sent")
                dispatch('fetchCategories')

            }
            catch(error) {
                alert('Failed to updated category')
            }
            router.push('/store-manager/dashboard')
        },

        async approveEditCategoryRequest({ dispatch }, { request_id, category_name }) {
            try {
                const response = await axios.put('/approve/edit_category_request', {category_name, request_id});
                dispatch('fetchCategoryRequests')
                dispatch('fetchCategories')
                dispatch('fetchProductsByCategory')
                console.log(request_id, category_name, response.data.message)

            }
            catch (error) {
                console.error(error)
            }
        },

        async rejectEditCategoryRequest({ dispatch }, { request_id }) {
            try {
                await axios.post(`/reject/edit_category_request/${request_id}`);
                dispatch('fetchCategoryRequests')
            }
            catch (error) {
                console.error(error)
            }
        },

        

        async fetchAdminProfile({ commit }) {
            try {
                const response = await axios.get('/admin/profile', { headers: { Authorization: `Bearer ${localStorage.access_token}` } })
                commit('setAdminProfile', response.data.profile_data)
            }
            catch (error) {
                console.error(error)
                router.push('/admin/login')
            }
        },

        async fetchManagerProfile({ commit }) {
            try {
                const response = await axios.get('/store_manager/profile', { headers: { Authorization: `Bearer ${localStorage.access_token}` } })
                commit('setManagerProfile', response.data.profile_data)
            }
            catch (error) {
                console.error(error)
                router.push('/store-manager/login')
            }
        },

        async fetchUserProfile({ commit }) {
            try {
                const response = await axios.get('/user/profile', { headers: { Authorization: `Bearer ${localStorage.access_token}` } })
                commit('setUserProfile', response.data.profile_data)
            }
            catch (error) {
                console.error(error)
                router.push('/user/login')
            }
        }
    },

})

export default store;