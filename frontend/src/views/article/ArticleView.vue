<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { marked } from 'marked'
import DOMPurify from 'dompurify'
import { getArticleById } from '@/api/article.api'
import type { ArticleResponse } from '@/types/article.types'
import SaveButton from '@/components/article/SaveButton.vue'

const props = defineProps<{ articleId: number }>()

const article = ref<ArticleResponse | null>(null)
const loading = ref(true)
const error = ref<string | null>(null)

const renderer = new marked.Renderer()
const _link = renderer.link.bind(renderer)
renderer.link = (token) => {
  const html = _link(token)
  return token.href?.startsWith('http')
    ? html.replace('<a ', '<a target="_blank" rel="noopener noreferrer" ')
    : html
}
marked.use({ renderer, breaks: true, gfm: true })

onMounted(async () => {
  try {
    article.value = await getArticleById(props.articleId)
  } catch {
    error.value = 'Статья не найдена'
  } finally {
    loading.value = false
  }
})

const renderedContent = computed(() => {
  if (!article.value?.text) return ''
  const html = marked.parse(article.value.text) as string
  return DOMPurify.sanitize(html, {
    ADD_TAGS: ['img', 'span'],
    ADD_ATTR: ['target', 'rel', 'src', 'alt', 'class', 'style', 'colspan', 'rowspan']
  })
})

function formatDate(dateStr: string) {
  return new Date(dateStr).toLocaleDateString('ru-RU', {
    year: 'numeric', month: 'long', day: 'numeric'
  })
}
</script>

<template>
  <div class="max-w-3xl mx-auto px-6 py-10">

    <div v-if="loading" class="flex justify-center py-20">
      <div class="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
    </div>

    <div v-else-if="error" class="text-center py-20 text-red-500">{{ error }}</div>

    <article v-else-if="article">

      <!-- Cover -->
      <img
        v-if="article.image"
        :src="article.image"
        :alt="article.title"
        class="w-full max-h-80 object-cover rounded-2xl mb-8"
      />

      <!-- Title + save -->
      <div class="flex items-start gap-3 mb-5">
        <h1 class="text-4xl font-bold text-gray-900 leading-tight flex-1">
          {{ article.title }}
        </h1>
        <SaveButton
          :article-id="article.articleId"
          :saved="article.statusSave"
          class="mt-2"
        />
      </div>

      <!-- Meta -->
      <div class="flex flex-wrap items-center gap-3 mb-8 pb-8 border-b border-gray-100">
        <RouterLink :to="`/profile/${article.users?.userId}`" class="flex items-center gap-2">
          <img
            v-if="article.users?.avatar"
            :src="article.users.avatar"
            :alt="article.users.username"
            class="w-8 h-8 rounded-full object-cover"
          />
          <div
            v-else
            class="w-8 h-8 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center text-sm font-bold"
          >
            {{ article.users?.username?.charAt(0)?.toUpperCase() ?? '?' }}
          </div>
          <span class="text-sm font-medium text-gray-700 hover:text-blue-600 transition-colors">
            {{ article.users?.username }}
          </span>
        </RouterLink>

        <span class="text-gray-200">·</span>
        <span class="text-sm text-gray-400">{{ formatDate(article.createdAt) }}</span>

        <span
          v-if="article.category"
          class="ml-auto px-2.5 py-0.5 text-xs font-medium bg-blue-50 text-blue-600 rounded-full"
        >
          {{ article.category.name }}
        </span>
      </div>

      <!-- Description -->
      <p v-if="article.description" class="text-lg text-gray-500 mb-8 leading-relaxed">
        {{ article.description }}
      </p>

      <!-- Content -->
      <div class="article-content prose prose-lg prose-gray max-w-none" v-html="renderedContent" />

    </article>
  </div>
</template>

<style scoped>
:deep(.article-content pre) {
  background: #282c34 !important;
  color: #abb2bf !important;
  border-radius: 0.75rem;
  padding: 1.25rem 1.5rem;
  overflow-x: auto;
  font-family: 'Fira Code', 'Consolas', 'Monaco', monospace;
  font-size: 0.875rem;
  line-height: 1.7;
}
:deep(.article-content pre code) {
  color: #abb2bf !important;
  background: transparent !important;
  padding: 0 !important;
  border-radius: 0 !important;
  font-size: inherit !important;
}
:deep(.article-content :not(pre) > code) {
  color: #e06c75 !important;
  background: #f3f4f6 !important;
  padding: 0.15em 0.4em !important;
  border-radius: 0.25rem !important;
  font-size: 0.875em !important;
}
:deep(.article-content table) {
  border-collapse: collapse;
  width: 100%;
  margin: 1.5rem 0;
  font-size: 0.95rem;
}
:deep(.article-content th) {
  background: #f9fafb;
  font-weight: 600;
  border: 1px solid #e5e7eb;
  padding: 0.6rem 1rem;
  text-align: left;
}
:deep(.article-content td) {
  border: 1px solid #e5e7eb;
  padding: 0.6rem 1rem;
}
:deep(.article-content tr:nth-child(even) td) {
  background: #fafafa;
}
</style>
