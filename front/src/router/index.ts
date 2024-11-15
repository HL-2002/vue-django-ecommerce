import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ProductFormView from '@/views/ProductFormView.vue'
import ReviewFromView from '@/views/ReviewFromView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },{
      path: '/form/products',
      name: 'form product',
      component: ProductFormView,
    },{

      path: '/form/reviews',
      name: 'form review',
      component: ReviewFromView  ,
    },
    {
      path: '/product/:id',
      name: 'product',
      component: () => import('../views/ProductView.vue')
    }
  ],
})

export default router
