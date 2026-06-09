<script setup lang="ts">
import { useAuthStore } from '@/stores/auth.store'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

function logout() {
  auth.logout()
  router.push({ name: 'login' })
}
</script>

<template>
  <header class="bg-white border-b border-gray-200 sticky top-0 z-20 shadow-sm">
    <div class="max-w-6xl mx-auto px-6 h-14 flex items-center justify-between">

      <!-- Логотип -->
      <RouterLink
        to="/"
        class="text-xl font-bold text-blue-600 hover:text-blue-700 transition-colors tracking-tight"
      >
        EduFlow
      </RouterLink>

      <!-- Центральная навигация (авторизован) -->
      <nav v-if="auth.isAuthenticated" class="flex items-center gap-1">
        <RouterLink
          :to="{ name: 'publish' }"
          class="px-4 py-1.5 text-sm font-medium rounded-lg transition-colors"
          :class="$route.name === 'publish'
            ? 'bg-blue-50 text-blue-600'
            : 'text-gray-600 hover:text-blue-600 hover:bg-gray-100'"
        >
          Публикации
        </RouterLink>
      </nav>

      <!-- Правая часть -->
      <nav class="flex items-center gap-2">

        <!-- Гость -->
        <template v-if="!auth.isAuthenticated">
          <RouterLink
            to="/login"
            class="px-4 py-1.5 text-sm font-medium text-gray-700 hover:text-blue-600 transition-colors"
          >
            Войти
          </RouterLink>
          <RouterLink
            to="/register"
            class="px-4 py-1.5 text-sm font-medium bg-blue-600 text-white rounded-full hover:bg-blue-700 transition-colors"
          >
            Регистрация
          </RouterLink>
        </template>

        <!-- Авторизован -->
        <template v-else>
          <RouterLink
            to="/profile"
            class="flex items-center gap-2 px-3 py-1.5 text-sm font-medium text-gray-700 hover:text-blue-600 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <span class="w-7 h-7 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center text-xs font-bold uppercase">
              {{ auth.user?.username?.charAt(0) ?? auth.user?.login?.charAt(0) ?? '?' }}
            </span>
            <span>Профиль</span>
          </RouterLink>
          <button
            @click="logout"
            class="px-3 py-1.5 text-sm text-gray-500 hover:text-red-500 transition-colors"
          >
            Выйти
          </button>
        </template>

      </nav>
    </div>
  </header>
</template>
