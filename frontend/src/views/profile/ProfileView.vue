<script setup lang="ts">
// Профиль другого пользователя
// Props: userId: number
// Store: useUserStore → fetchProfileById(userId), toggleSubscription()
//        useArticleStore → fetchArticlesByUser(userId)
defineProps<{ userId: number }>()
</script>

<template>
  <div>
    <h1 class="text-2xl font-bold mb-4">Профиль пользователя</h1>
    <!-- TODO: аватар, имя, кнопка подписки, список статей, подписчики -->
  </div>
</template>
