<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { getProfileById } from '@/api/user.api'
import type { ProfileResponse } from '@/types/user.types'

const props = defineProps<{ userId: number }>()

const profile = ref<ProfileResponse | null>(null)
const loading = ref(true)
const error = ref<string | null>(null)

onMounted(async () => {
  try {
    profile.value = await getProfileById(props.userId)
  } catch {
    error.value = 'Пользователь не найден'
  } finally {
    loading.value = false
  }
})

const initials = computed(() => {
  const name = profile.value?.username || profile.value?.login || '?'
  return name.charAt(0).toUpperCase()
})

function formatDate(dateStr: string) {
  return new Date(dateStr).toLocaleDateString('ru-RU', {
    year: 'numeric', month: 'long', day: 'numeric'
  })
}
</script>

<template>
  <div class="max-w-2xl mx-auto px-6 py-10">

    <!-- Loading -->
    <div v-if="loading" class="flex justify-center py-20">
      <div class="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
    </div>

    <!-- Error -->
    <div v-else-if="error" class="text-center py-20 text-red-500">{{ error }}</div>

    <!-- Profile -->
    <div v-else-if="profile">
      <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
        <div class="flex items-start gap-5">

          <!-- Avatar -->
          <div class="flex-shrink-0">
            <img
              v-if="profile.avatar"
              :src="profile.avatar"
              :alt="profile.username"
              class="w-20 h-20 rounded-full object-cover border border-gray-200"
            />
            <div
              v-else
              class="w-20 h-20 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center text-3xl font-bold"
            >
              {{ initials }}
            </div>
          </div>

          <!-- Info -->
          <div class="flex-1 min-w-0">
            <h1 class="text-xl font-bold text-gray-900 leading-tight">
              {{ profile.username || 'Без имени' }}
            </h1>
            <p class="text-sm text-gray-400 mt-0.5">{{ profile.login }}</p>

            <div class="flex flex-wrap gap-2 mt-2">
              <span class="px-2.5 py-0.5 text-xs font-medium bg-blue-50 text-blue-700 rounded-full">
                Пользователь
              </span>
              <span
                :class="profile.status ? 'bg-green-50 text-green-700' : 'bg-gray-100 text-gray-500'"
                class="px-2.5 py-0.5 text-xs font-medium rounded-full"
              >
                {{ profile.status ? 'Активен' : 'Неактивен' }}
              </span>
            </div>

            <p v-if="profile.createdAt" class="text-xs text-gray-400 mt-2">
              Зарегистрирован {{ formatDate(profile.createdAt) }}
            </p>
          </div>
        </div>

        <!-- Bio -->
        <div
          v-if="profile.profile || profile.cardDetails"
          class="mt-4 pt-4 border-t border-gray-100"
        >
          <p v-if="profile.profile" class="text-sm text-gray-600 leading-relaxed">
            {{ profile.profile }}
          </p>
          <p v-if="profile.cardDetails" class="text-xs text-gray-400 mt-2">
            {{ profile.cardDetails }}
          </p>
        </div>
      </div>
    </div>

  </div>
</template>
