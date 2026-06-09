<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getSavedArticles } from '@/api/user.api'
import type { ArticleResponse } from '@/types/article.types'
import ArticleCard from '@/components/article/ArticleCard.vue'
import SortBar from '@/components/article/SortBar.vue'
import { useArticleSort } from '@/composables/useArticleSort'

const articles = ref<ArticleResponse[]>([])
const loading = ref(false)
const error = ref<string | null>(null)

const { sortKey, sorted } = useArticleSort(articles)

onMounted(async () => {
  loading.value = true
  try {
    articles.value = await getSavedArticles()
  } catch {
    error.value = 'Не удалось загрузить избранное'
  } finally {
    loading.value = false
  }
})

function onUnsaved(articleId: number) {
  articles.value = articles.value.filter((a) => a.articleId !== articleId)
}
</script>

<template>
  <div class="max-w-6xl mx-auto px-6 py-8">

    <h1 class="text-2xl font-bold text-gray-900 mb-8">Избранное</h1>

    <!-- Loading -->
    <div v-if="loading" class="flex justify-center py-20">
      <div class="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
    </div>

    <!-- Error -->
    <p v-else-if="error" class="text-red-500 text-sm py-10 text-center">{{ error }}</p>

    <!-- Empty -->
    <div v-else-if="articles.length === 0" class="text-center py-20">
      <svg class="w-12 h-12 mx-auto mb-3 text-gray-200" viewBox="0 0 24 24" fill="none" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
              d="M5 4a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 20V4z"/>
      </svg>
      <p class="text-sm font-medium text-gray-400">Избранных статей пока нет</p>
      <RouterLink to="/" class="mt-3 inline-block text-sm text-blue-600 hover:underline">
        Перейти к ленте
      </RouterLink>
    </div>

    <!-- Grid -->
    <div v-else>
      <SortBar v-model="sortKey" class="mb-5" />
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
      <ArticleCard
        v-for="article in sorted"
        :key="article.articleId"
        :article="article"
        @save-change="(saved: boolean) => { if (!saved) onUnsaved(article.articleId) }"
      />
      </div>
    </div>

  </div>
</template>
