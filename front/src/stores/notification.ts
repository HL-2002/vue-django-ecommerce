import { ref } from 'vue'
import { defineStore } from 'pinia'
import type { NotificationSooner } from '@/types/types'

export const useNotificationStore = defineStore('notification', () => {
  const notifications = ref<NotificationSooner[]>([])
  function notify(notification: NotificationSooner) {
    notifications.value.push(notification)
    setTimeout(() => {
      removeNotification(notifications.value.indexOf(notification))
    }
    , 3000)

  }

  function removeNotification(index: number) {
    notifications.value.splice(index, 1)
  }


  return { notifications, notify, removeNotification }
})
