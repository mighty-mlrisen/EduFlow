<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user.store'

const userStore = useUserStore()

const isEditing = ref(false)
const saveLoading = ref(false)
const saveError = ref<string | null>(null)
const saveSuccess = ref(false)

const form = reactive({
  username: '',
  avatar: '',
  profile: '',
  cardDetails: ''
})

onMounted(() => {
  userStore.fetchMyProfile()
})

// Когда профиль загрузится — заполняем форму
const profile = computed(() => userStore.myProfile)

function startEditing() {
  if (!profile.value) return
  form.username = profile.value.username ?? ''
  form.avatar = profile.value.avatar ?? ''
  form.profile = profile.value.profile ?? ''
  form.cardDetails = profile.value.cardDetails ?? ''
  saveError.value = null
  saveSuccess.value = false
  isEditing.value = true
}

function cancelEditing() {
  isEditing.value = false
  saveError.value = null
}

async function handleSave() {
  if (!form.username.trim()) {
    saveError.value = 'Имя обязательно'
    return
  }
  saveLoading.value = true
  saveError.value = null
  saveSuccess.value = false
  try {
    await userStore.updateMyProfile({
      username: form.username.trim(),
      avatar: form.avatar.trim() || null,
      profile: form.profile.trim() || null,
      cardDetails: form.cardDetails.trim() || null
    })
    isEditing.value = false
    saveSuccess.value = true
    setTimeout(() => { saveSuccess.value = false }, 3000)
  } catch {
    saveError.value = 'Не удалось сохранить изменения'
  } finally {
    saveLoading.value = false
  }
}

// Инициалы для аватара-заглушки
const initials = computed(() => {
  const name = profile.value?.username || profile.value?.login || '?'
  return name.charAt(0).toUpperCase()
})

function formatDate(dateStr: string) {
  return new Date(dateStr).toLocaleDateString('ru-RU', {
    year: 'numeric', month: 'long', day: 'numeric'
  })
}

function roleLabel(_role: string) {
  return 'Пользователь'
}
</script>

<template>
  <div class="max-w-2xl mx-auto px-6 py-10">

    <!-- Загрузка -->
    <div v-if="userStore.loading && !profile" class="flex justify-center py-20">
      <div class="w-8 h-8 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" />
    </div>

    <!-- Ошибка загрузки -->
    <div v-else-if="userStore.error" class="text-center py-20 text-red-500">
      {{ userStore.error }}
    </div>

    <!-- Профиль -->
    <div v-else-if="profile">

      <!-- Шапка профиля -->
      <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-6 mb-4">
        <div class="flex items-start gap-5">

          <!-- Аватар -->
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

          <!-- Основная инфо -->
          <div class="flex-1 min-w-0">
            <h1 class="text-xl font-bold text-gray-900 leading-tight">
              {{ profile.username || 'Без имени' }}
            </h1>
            <p class="text-sm text-gray-400 mt-0.5">{{ profile.login }}</p>

            <div class="flex flex-wrap gap-2 mt-2">
              <span class="px-2.5 py-0.5 text-xs font-medium bg-blue-50 text-blue-700 rounded-full">
                {{ roleLabel(profile.userRole) }}
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

          <!-- Кнопка редактирования (вид) -->
          <button
            v-if="!isEditing"
            @click="startEditing"
            class="flex-shrink-0 px-4 py-1.5 text-sm font-medium border border-gray-300
                   rounded-lg text-gray-700 hover:border-blue-400 hover:text-blue-600 transition-colors"
          >
            Редактировать
          </button>
        </div>

        <!-- Описание профиля (вид) -->
        <div v-if="!isEditing && (profile.profile || profile.cardDetails)" class="mt-4 pt-4 border-t border-gray-100">
          <p v-if="profile.profile" class="text-sm text-gray-600 leading-relaxed">
            {{ profile.profile }}
          </p>
          <p v-if="profile.cardDetails" class="text-xs text-gray-400 mt-2">
            {{ profile.cardDetails }}
          </p>
        </div>

        <!-- Форма редактирования -->
        <form v-if="isEditing" @submit.prevent="handleSave" class="mt-4 pt-4 border-t border-gray-100 flex flex-col gap-4">

          <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">

            <!-- Имя -->
            <div class="flex flex-col gap-1">
              <label class="text-xs font-medium text-gray-600">
                Имя <span class="text-red-400">*</span>
              </label>
              <input
                v-model="form.username"
                type="text"
                placeholder="Иван Иванов"
                :disabled="saveLoading"
                class="input-field"
              />
            </div>

            <!-- URL аватара -->
            <div class="flex flex-col gap-1">
              <label class="text-xs font-medium text-gray-600">URL аватара</label>
              <input
                v-model="form.avatar"
                type="url"
                placeholder="https://example.com/avatar.jpg"
                :disabled="saveLoading"
                class="input-field"
              />
            </div>

          </div>

          <!-- Описание / bio -->
          <div class="flex flex-col gap-1">
            <label class="text-xs font-medium text-gray-600">О себе</label>
            <textarea
              v-model="form.profile"
              rows="3"
              placeholder="Расскажите о себе..."
              :disabled="saveLoading"
              class="input-field resize-none"
            />
          </div>

          <!-- Доп. данные -->
          <div class="flex flex-col gap-1">
            <label class="text-xs font-medium text-gray-600">Дополнительно</label>
            <input
              v-model="form.cardDetails"
              type="text"
              placeholder="Место работы, специализация..."
              :disabled="saveLoading"
              class="input-field"
            />
          </div>

          <!-- Ошибка сохранения -->
          <p v-if="saveError" class="text-sm text-red-500 bg-red-50 px-3 py-2 rounded-lg">
            {{ saveError }}
          </p>

          <!-- Кнопки -->
          <div class="flex gap-2 justify-end">
            <button
              type="button"
              @click="cancelEditing"
              :disabled="saveLoading"
              class="px-4 py-2 text-sm font-medium text-gray-600 border border-gray-300 rounded-lg
                     hover:bg-gray-50 disabled:opacity-50 transition-colors"
            >
              Отмена
            </button>
            <button
              type="submit"
              :disabled="saveLoading"
              class="px-4 py-2 text-sm font-medium bg-blue-600 text-white rounded-lg
                     hover:bg-blue-700 disabled:opacity-60 transition-colors"
            >
              <span v-if="saveLoading">Сохранение...</span>
              <span v-else>Сохранить</span>
            </button>
          </div>

        </form>
      </div>

      <!-- Уведомление об успехе -->
      <Transition name="fade">
        <div
          v-if="saveSuccess"
          class="fixed bottom-6 right-6 bg-green-600 text-white text-sm px-4 py-2 rounded-lg shadow-lg"
        >
          Профиль обновлён
        </div>
      </Transition>

    </div>
  </div>
</template>

<style scoped>
.input-field {
  @apply w-full px-3 py-2 rounded-lg border border-gray-300 text-sm outline-none
         focus:border-blue-500 focus:ring-2 focus:ring-blue-100
         disabled:bg-gray-50 disabled:text-gray-400 transition bg-white;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
