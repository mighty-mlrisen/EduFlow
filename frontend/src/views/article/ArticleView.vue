<script setup lang="ts">
// Страница одной статьи
// Props: articleId: number
// Store: useArticleStore → fetchArticleById, toggleReaction, toggleSave, fetchComments, postComment
defineProps<{ articleId: number }>()
</script>

<template>
  <div>
    <h1 class="text-2xl font-bold mb-4">Статья</h1>
    <!-- TODO: заголовок, текст, автор, лайки, сохранение, комментарии -->
  </div>
</template>
