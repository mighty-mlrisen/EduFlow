<script setup lang="ts">
// Статьи по категории
// Props: categoryId: number
// Store: useArticleStore → fetchByCategory(categoryId), articles, categories
defineProps<{ categoryId: number }>()
</script>

<template>
  <div>
    <h1 class="text-2xl font-bold mb-4">Категория</h1>
    <!-- TODO: список ArticleCard -->
  </div>
</template>
