<script setup>
import { Sidebar } from "frappe-ui"

const sidebarHeader = {
  title: 'Frappe CRM',
  subtitle: 'Jane Doe',
  logo: 'https://raw.githubusercontent.com/frappe/crm/develop/.github/logo.svg',
  menuItems: [
    {
      label: 'Toggle Theme',
      icon: { name: 'lucide-moon' },
      onClick: () => {
        const currentTheme = document.documentElement.getAttribute("data-theme")
        const newTheme = currentTheme === "dark" ? "light" : "dark"
        document.documentElement.setAttribute("data-theme", newTheme)
      }
    },
    {
      label: 'Help',
      to: '/help',
      icon: { name: 'lucide-settings' },
      onClick: () => alert("Help clicked!")
    },
    {
      label: 'Logout',
      to: '/logout',
      icon: { name: 'lucide-user' },
      onClick: () => alert("Logging out...")
    }
  ]
}
</script>
<template>
    <div class="flex h-screen w-full flex-col bg-surface-white shadow">
  <Sidebar
    :header="sidebarHeader" />
  />
  </div>
</template>
