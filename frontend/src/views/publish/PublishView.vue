<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getArticleById, getMyDrafts, getMyArticles } from '@/api/article.api'
import type { ArticleResponse } from '@/types/article.types'
import ArticleEditor from '@/components/editor/ArticleEditor.vue'
import ArticleCard from '@/components/article/ArticleCard.vue'

const route = useRoute()
const router = useRouter()

type Tab = 'editor' | 'drafts' | 'articles'

const TABS: { id: Tab; label: string }[] = [
  { id: 'editor', label: 'Опубликовать статью' },
  { id: 'drafts', label: 'Черновики' },
  { id: 'articles', label: 'Мои статьи' }
]

const activeTab = computed<Tab>(() => (route.query.tab as Tab) || 'editor')
const editId = computed(() => route.query.id ? Number(route.query.id) : null)

const editingArticle = ref<ArticleResponse | null>(null)
const loadingEdit = ref(false)

const drafts = ref<ArticleResponse[]>([])
const myArticles = ref<ArticleResponse[]>([])
const loadingList = ref(false)
const listError = ref<string | null>(null)

// Load article when editing
watch(editId, async (id) => {
  if (id) {
    loadingEdit.value = true
    editingArticle.value = null
    try {
      editingArticle.value = await getArticleById(id)
    } catch {
      editingArticle.value = null
    } finally {
      loadingEdit.value = false
    }
  } else {
    editingArticle.value = null
  }
}, { immediate: true })

// Load lists on tab change
watch(activeTab, (tab) => {
  if (tab === 'drafts') loadDrafts()
  else if (tab === 'articles') loadPublished()
}, { immediate: true })

async function loadDrafts() {
  loadingList.value = true
  listError.value = null
  try {
    drafts.value = await getMyDrafts()
  } catch {
    listError.value = 'Не удалось загрузить черновики'
  } finally {
    loadingList.value = false
  }
}

async function loadPublished() {
  loadingList.value = true
  listError.value = null
  try {
    const all = await getMyArticles()
    myArticles.value = all.filter((a) => !a.draft)
  } catch {
    listError.value = 'Не удалось загрузить статьи'
  } finally {
    loadingList.value = false
  }
}

function setTab(tab: Tab) {
  router.push({ name: 'publish', query: { tab } })
}

function editArticle(id: number) {
  router.push({ name: 'publish', query: { tab: 'editor', id: String(id) } })
}

const editorTabLabel = computed(() =>
  editId.value ? 'Редактировать' : 'Опубликовать статью'
)
</script>

<template>
  <div class="max-w-6xl mx-auto px-6 py-8">

    <!-- Tab switcher -->
    <div class="flex gap-1 bg-gray-100 rounded-xl p-1 mb-8 w-fit">
      <button
        v-for="tab in TABS"
        :key="tab.id"
        @click="setTab(tab.id)"
        class="px-5 py-2 text-sm font-medium rounded-lg transition-all"
        :class="activeTab === tab.id
          ? 'bg-white text-gray-900 shadow-sm'
          : 'text-gray-500 hover:text-gray-700'"
      >
        {{ tab.id === 'editor' ? editorTabLabel : tab.label }}
      </button>
    </div>

    <!-- ── Editor tab ── -->
    <template v-if="activeTab === 'editor'">
      <div v-if="loadingEdit" class="flex justify-center py-16">
        <div class="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
      </div>
      <ArticleEditor
        v-else
        :initial-data="editingArticle"
        :article-id="editId"
      />
    </template>

    <!-- ── Drafts tab ── -->
    <template v-else-if="activeTab === 'drafts'">
      <div v-if="loadingList" class="flex justify-center py-16">
        <div class="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
      </div>
      <p v-else-if="listError" class="text-red-500 text-sm">{{ listError }}</p>
      <div v-else-if="drafts.length === 0" class="text-center py-16">
        <svg class="w-12 h-12 mx-auto mb-3 text-gray-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
        </svg>
        <p class="text-sm font-medium text-gray-400">Черновиков пока нет</p>
        <button @click="setTab('editor')" class="mt-3 text-sm text-blue-600 hover:underline">
          Написать статью
        </button>
      </div>
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 gap-6">
        <ArticleCard
          v-for="article in drafts"
          :key="article.articleId"
          :article="article"
          :is-draft="true"
          @edit="editArticle"
        />
      </div>
    </template>

    <!-- ── My articles tab ── -->
    <template v-else>
      <div v-if="loadingList" class="flex justify-center py-16">
        <div class="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
      </div>
      <p v-else-if="listError" class="text-red-500 text-sm">{{ listError }}</p>
      <div v-else-if="myArticles.length === 0" class="text-center py-16">
        <svg class="w-12 h-12 mx-auto mb-3 text-gray-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"/>
        </svg>
        <p class="text-sm font-medium text-gray-400">Опубликованных статей пока нет</p>
        <button @click="setTab('editor')" class="mt-3 text-sm text-blue-600 hover:underline">
          Написать первую статью
        </button>
      </div>
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 gap-6">
        <ArticleCard
          v-for="article in myArticles"
          :key="article.articleId"
          :article="article"
          :show-edit="true"
          @edit="editArticle"
        />
      </div>
    </template>

  </div>
</template>
