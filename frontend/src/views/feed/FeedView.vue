<script setup lang="ts">
import { useAuthStore } from '@/stores/auth.store'

const auth = useAuthStore()
</script>

<template>
  <div class="max-w-6xl mx-auto px-6 py-12">

    <!-- Hero для незарегистрированного пользователя -->
    <template v-if="!auth.isAuthenticated">
      <div class="flex flex-col items-center text-center py-16 gap-6">
        <h1 class="text-5xl font-bold text-gray-900 leading-tight">
          Добро пожаловать в <span class="text-blue-600">EduFlow</span>
        </h1>
        <p class="text-lg text-gray-500 max-w-xl">
          Платформа для IT-статей и обмена знаниями.
          Читайте, пишите, подписывайтесь на авторов.
        </p>
        <div class="flex gap-3 mt-2">
          <RouterLink
            to="/register"
            class="px-6 py-2.5 bg-blue-600 text-white font-medium rounded-full hover:bg-blue-700 transition-colors"
          >
            Начать бесплатно
          </RouterLink>
          <RouterLink
            to="/login"
            class="px-6 py-2.5 border border-gray-300 text-gray-700 font-medium rounded-full hover:border-blue-400 hover:text-blue-600 transition-colors"
          >
            Войти
          </RouterLink>
        </div>
      </div>
    </template>

    <!-- Заглушка для авторизованного -->
    <template v-else>
      <h1 class="text-2xl font-bold text-gray-900 mb-6">Все статьи</h1>
      <p class="text-gray-400">Здесь появятся статьи...</p>
    </template>

  </div>
</template>
