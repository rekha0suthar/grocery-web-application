import {createRouter, createWebHistory} from 'vue-router'
import HomePage from './view/Home.vue'
import UserLogin from './view/UserLogin.vue'
import UserRegister from './view/UserRegister.vue'
import UserDashboard from './view/UserDashboard.vue'
import ManagerLogin from './view/ManagerLogin.vue'
import ManagerRegister from './view/ManagerRegister.vue'
import AdminRegister from './view/AdminRegister.vue'
import AdminLogin from './view/AdminLogin.vue'
import AdminDashboard from './view/AdminDashboard.vue'
import AdminAddProduct from './view/AdminAddProduct.vue'
import ManagerAddProduct from './view/ManagerAddProduct.vue'
import AddCategory from './view/AddCategory.vue'
import EditCategory from './view/EditCategory.vue'
import AdminEditProduct from './view/AdminEditProduct.vue'
import ManagerEditProduct from './view/ManagerEditProduct.vue'
import SearchComponent from './view/SearchComponent.vue'
import AdminProfile from './view/AdminProfile.vue'
import UserProfile from './view/UserProfile.vue'
import AdminCart from './view/AdminCart.vue'
import UserCart from './view/UserCart.vue'
import AdminCheckout from './view/AdminCheckout.vue'
import AdminOrders from './view/AdminOrders.vue'
import UserCheckout from './view/UserCheckout.vue'
import UserOrders from './view/UserOrders.vue'
import RequestPage from './view/Requests.vue'
import ManagerDashboard from './view/ManagerDashboard.vue'
import ManagerCart from './view/ManagerCart.vue'
import ManagerCheckout from './view/ManagerCheckout.vue'
import ManagerOrders from './view/ManagerOrders.vue'
import ManagerProfile from './view/ManagerProfile.vue'
import RequestAddCategory from './view/RequestAddCategory.vue'
import RequestEditCategory from './view/RequestEditCategory.vue'

const routes = [
    { path: '/', component: HomePage },
    { path: '/user/login', component: UserLogin },
    { path: '/user/register', component: UserRegister },
    { path: '/user/dashboard', component: UserDashboard },
    { path: '/admin/login', component: AdminLogin },
    { path: '/admin/register', component: AdminRegister },
    { path: '/admin/dashboard', component: AdminDashboard },
    { path: '/store-manager/login', component: ManagerLogin },
    { path: '/store-manager/register', component: ManagerRegister},
    { path: '/admin/add-product', component: AdminAddProduct },
    { path: '/admin/add-category', component: AddCategory },
    { path: '/admin/edit-category/:category_id', name: 'edit-category', component: EditCategory },
    { path: '/admin/edit-product/:product_id', name: 'edit-product', component: AdminEditProduct },
    { path: '/search', name: 'search-product', component: SearchComponent, props: (route) => ({ query: route.query.query}) },
    { path: '/admin/profile', component: AdminProfile },
    { path: '/user/profile', component: UserProfile },
    { path: '/admin/cart', component: AdminCart },
    { path: '/user/cart', component: UserCart },
    { path: '/admin/checkout', component: AdminCheckout},
    { path: '/admin/orders', component: AdminOrders },
    { path: '/user/checkout', component: UserCheckout },
    { path: '/user/orders', component: UserOrders },
    { path: '/requests', component: RequestPage },
    { path: '/store-manager/dashboard', component: ManagerDashboard },
    { path: '/store-manager/add-product', component: ManagerAddProduct },
    { path: '/store-manager/add-category', component: AddCategory },
    { path: '/store-manager/edit-product/:product_id', name: 'store-manager-edit-product', component: ManagerEditProduct },
    { path: '/store-manager/cart', component: ManagerCart },
    { path: '/store-manager/checkout', component: ManagerCheckout },
    { path: '/store-manager/orders', component: ManagerOrders },
    { path: '/store-manager/profile', component: ManagerProfile },
    { path: '/store-manager/request-add-category', component: RequestAddCategory },
    { path: '/store-manager/request-edit-category/:category_id', name: 'store-manager-edit-category', component: RequestEditCategory },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})
export default router